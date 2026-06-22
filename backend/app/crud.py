from collections import defaultdict

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models import Foodstuff, InventoryItem
from app.schemas import FoodstuffCreate, InventoryItemCreate, InventoryItemUpdate, estimated_expiry_from_foodstuff


def create_foodstuff(db: Session, payload: FoodstuffCreate) -> Foodstuff:
    existing = db.scalar(select(Foodstuff).where(Foodstuff.name.ilike(payload.name)))
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Foodstuff already exists")
    foodstuff = Foodstuff(**payload.model_dump())
    db.add(foodstuff)
    db.commit()
    db.refresh(foodstuff)
    return foodstuff


def list_foodstuffs(db: Session, search: str | None = None) -> list[Foodstuff]:
    stmt = select(Foodstuff).order_by(Foodstuff.name.asc())
    if search:
        stmt = stmt.where(Foodstuff.name.ilike(f"%{search}%"))
    return list(db.scalars(stmt).all())


def get_foodstuff_or_404(db: Session, foodstuff_id: int) -> Foodstuff:
    foodstuff = db.get(Foodstuff, foodstuff_id)
    if foodstuff is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Foodstuff not found")
    return foodstuff


def _resolved_create_values(db: Session, payload: InventoryItemCreate) -> dict:
    values = payload.model_dump()
    foodstuff = None
    if payload.foodstuff_id is not None:
        foodstuff = get_foodstuff_or_404(db, payload.foodstuff_id)
        values["name"] = payload.name or foodstuff.name
        values["category"] = payload.category or foodstuff.category
        values["estimated_expiry_date"] = payload.estimated_expiry_date or estimated_expiry_from_foodstuff(
            payload.purchase_date, foodstuff.expiry_max_days
        )
    return values


def create_inventory_item(db: Session, payload: InventoryItemCreate) -> InventoryItem:
    item = InventoryItem(**_resolved_create_values(db, payload))
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def list_inventory_items(db: Session, category: str | None = None) -> list[InventoryItem]:
    stmt = (
        select(InventoryItem)
        .where(InventoryItem.is_active.is_(True))
        .options(selectinload(InventoryItem.foodstuff))
        .order_by(InventoryItem.estimated_expiry_date.asc(), InventoryItem.name.asc())
    )
    if category:
        stmt = stmt.where(InventoryItem.category == category)
    return list(db.scalars(stmt).all())


def grouped_inventory_items(db: Session) -> list[dict]:
    groups: dict[str, list[InventoryItem]] = defaultdict(list)
    for item in list_inventory_items(db):
        groups[item.category].append(item)
    return [{"category": category, "items": items} for category, items in sorted(groups.items())]


def get_inventory_item_or_404(db: Session, item_id: int) -> InventoryItem:
    item = db.scalar(
        select(InventoryItem)
        .where(InventoryItem.id == item_id, InventoryItem.is_active.is_(True))
        .options(selectinload(InventoryItem.foodstuff))
    )
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory item not found")
    return item


def update_inventory_item(db: Session, item_id: int, payload: InventoryItemUpdate) -> InventoryItem:
    item = get_inventory_item_or_404(db, item_id)
    values = payload.model_dump(exclude_unset=True)
    for key, value in values.items():
        setattr(item, key, value)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def remove_inventory_item(db: Session, item_id: int) -> None:
    item = get_inventory_item_or_404(db, item_id)
    item.is_active = False
    db.add(item)
    db.commit()

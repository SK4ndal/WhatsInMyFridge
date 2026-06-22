from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db
from app.schemas import CategoryGroup, InventoryItemCreate, InventoryItemRead, InventoryItemUpdate

router = APIRouter(prefix="/inventory", tags=["inventory"])


@router.get("", response_model=list[InventoryItemRead])
def list_inventory(category: str | None = None, db: Session = Depends(get_db)) -> list:
    return crud.list_inventory_items(db, category=category)


@router.get("/grouped-by-category", response_model=list[CategoryGroup])
def list_inventory_grouped_by_category(db: Session = Depends(get_db)) -> list[dict]:
    return crud.grouped_inventory_items(db)


@router.post("", response_model=InventoryItemRead, status_code=201)
def create_inventory_item(payload: InventoryItemCreate, db: Session = Depends(get_db)):
    return crud.create_inventory_item(db, payload)


@router.patch("/{item_id}", response_model=InventoryItemRead)
def update_inventory_item(item_id: int, payload: InventoryItemUpdate, db: Session = Depends(get_db)):
    return crud.update_inventory_item(db, item_id, payload)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_inventory_item(item_id: int, db: Session = Depends(get_db)) -> Response:
    crud.remove_inventory_item(db, item_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

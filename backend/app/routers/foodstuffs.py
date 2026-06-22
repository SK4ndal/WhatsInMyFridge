from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db
from app.schemas import FoodstuffCreate, FoodstuffRead

router = APIRouter(prefix="/foodstuffs", tags=["foodstuffs"])


@router.get("", response_model=list[FoodstuffRead])
def list_foodstuff_suggestions(search: str | None = None, db: Session = Depends(get_db)) -> list:
    return crud.list_foodstuffs(db, search=search)


@router.post("", response_model=FoodstuffRead, status_code=201)
def quick_create_foodstuff(payload: FoodstuffCreate, db: Session = Depends(get_db)):
    return crud.create_foodstuff(db, payload)

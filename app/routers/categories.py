from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas

router = APIRouter(tags=["categories"])

@router.get("/categories/", response_model=list[schemas.CategoryOut])
def list_categories(type: str | None = None, db: Session = Depends(get_db)):
    """Получить список категорий, можно фильтровать по типу (income/expense)."""
    return crud.get_categories(db, type)
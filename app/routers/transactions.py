from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas

router = APIRouter(tags=["transactions"])

@router.post("/transactions/", response_model=schemas.TransactionOut)
def add_transaction(tx: schemas.TransactionCreate, db: Session = Depends(get_db)):
    """Добавить новую транзакцию (доход или расход)."""
    return crud.create_transaction(db, tx)

@router.get("/transactions/", response_model=list[schemas.TransactionOut])
def list_transactions(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    """Получить последние транзакции."""
    return crud.get_transactions(db, skip=skip, limit=limit)

@router.get("/balance/", response_model=schemas.BalanceOut)
def balance(db: Session = Depends(get_db)):
    """Текущий баланс."""
    return {"balance": crud.get_balance(db)}
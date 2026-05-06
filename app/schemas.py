from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# ---------- Категории ----------
class CategoryOut(BaseModel):
    id: int
    name: str
    type: str

    class Config:
        from_attributes = True

# ---------- Транзакции ----------
class TransactionCreate(BaseModel):
    amount: float
    type: str          # "income" или "expense"
    category_id: int
    note: Optional[str] = None
    date: Optional[datetime] = None

class TransactionOut(BaseModel):
    id: int
    amount: float
    type: str
    category_id: int
    note: Optional[str]
    date: datetime

    class Config:
        from_attributes = True

class BalanceOut(BaseModel):
    balance: float
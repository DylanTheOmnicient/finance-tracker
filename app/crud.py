from sqlalchemy.orm import Session
from sqlalchemy import func
from app import models, schemas

# ------------- Категории -------------
def get_categories(db: Session, category_type: str | None = None):
    query = db.query(models.Category)
    if category_type:
        query = query.filter(models.Category.type == category_type)
    return query.all()

def seed_default_categories(db: Session):
    """Заполняет БД категориями, если их ещё нет."""
    defaults = [
        models.Category(name="Зарплата", type="income"),
        models.Category(name="Подработка", type="income"),
        models.Category(name="Прочее", type="income"),
        models.Category(name="Продукты", type="expense"),
        models.Category(name="Транспорт", type="expense"),
        models.Category(name="Развлечения", type="expense"),
        models.Category(name="Коммунальные платежи", type="expense"),
        models.Category(name="Прочее", type="expense"),
    ]
    for cat_data in defaults:
        exists = db.query(models.Category).filter_by(
            name=cat_data.name, type=cat_data.type
        ).first()
        if not exists:
            db.add(cat_data)
    db.commit()

# ------------- Транзакции -------------
def create_transaction(db: Session, tx: schemas.TransactionCreate) -> models.Transaction:
    db_tx = models.Transaction(**tx.model_dump())
    db.add(db_tx)
    db.commit()
    db.refresh(db_tx)
    return db_tx

def get_transactions(db: Session, skip: int = 0, limit: int = 50):
    return db.query(models.Transaction)\
             .order_by(models.Transaction.date.desc())\
             .offset(skip)\
             .limit(limit)\
             .all()

def get_balance(db: Session) -> float:
    income = db.query(func.coalesce(func.sum(models.Transaction.amount), 0))\
               .filter(models.Transaction.type == "income")\
               .scalar()
    expense = db.query(func.coalesce(func.sum(models.Transaction.amount), 0))\
                .filter(models.Transaction.type == "expense")\
                .scalar()
    return income - expense

def reset_transactions(db: Session):
    """
    Удаляет все транзакции. Баланс после этого = 0.
    Возвращает количество удалённых записей.
    """
    num_deleted = db.query(models.Transaction).delete()
    db.commit()
    return num_deleted
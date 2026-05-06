import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app import models, crud, schemas

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

def test_seed_categories(db):
    crud.seed_default_categories(db)
    cats = crud.get_categories(db)
    assert len(cats) > 0

def test_create_transaction(db):
    crud.seed_default_categories(db)
    cat = crud.get_categories(db, "expense")[0]
    tx = schemas.TransactionCreate(amount=100, type="expense", category_id=cat.id, note="тест")
    result = crud.create_transaction(db, tx)
    assert result.id is not None
    assert result.amount == 100

def test_balance(db):
    crud.seed_default_categories(db)
    inc_cat = crud.get_categories(db, "income")[0]
    exp_cat = crud.get_categories(db, "expense")[0]
    # Добавляем 1000 дохода и 300 расхода
    crud.create_transaction(db, schemas.TransactionCreate(amount=1000, type="income", category_id=inc_cat.id))
    crud.create_transaction(db, schemas.TransactionCreate(amount=300, type="expense", category_id=exp_cat.id))
    assert crud.get_balance(db) == 700.0
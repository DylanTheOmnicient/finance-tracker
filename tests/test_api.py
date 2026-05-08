from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app
from sqlalchemy.orm import Session

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_api.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def setup_module(module):
    Base.metadata.create_all(bind=engine)

def teardown_module(module):
    Base.metadata.drop_all(bind=engine)

def test_read_categories():
    response = client.get("/api/categories/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_add_and_read_transactions():
    # Получить id расходной категории
    cats = client.get("/api/categories/?type=expense").json()
    cat_id = cats[0]["id"]
    # Добавить транзакцию
    response = client.post("/api/transactions/", json={
        "amount": 50.0,
        "type": "expense",
        "category_id": cat_id,
        "note": "тест api"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["amount"] == 50.0

    # Проверить список
    list_resp = client.get("/api/transactions/")
    assert list_resp.status_code == 200
    assert len(list_resp.json()) > 0

def test_balance():
    resp = client.get("/api/balance/")
    assert resp.status_code == 200
    assert "balance" in resp.json()

def test_reset(client: TestClient, db_session: Session):
    # сначала добавляем пару транзакций
    # ...
    response = client.post("/api/reset")
    assert response.status_code == 200
    data = response.json()
    assert data["balance"] == 0
    assert data["deleted_count"] == 2

    # Проверяем, что база пуста
    from app.crud import get_transactions
    txs = get_transactions(db_session)
    assert len(txs) == 0
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.database import engine, Base, SessionLocal
from app.routers import transactions, categories
from app.crud import seed_default_categories

# Создаём таблицы при старте (для MVP ок, в продакшене использовать Alembic)
Base.metadata.create_all(bind=engine)

# Заполняем категории по умолчанию
db = SessionLocal()
seed_default_categories(db)
db.close()

app = FastAPI(title="Финансовый трекер MVP")

# API-роуты
app.include_router(transactions.router, prefix="/api")
app.include_router(categories.router, prefix="/api")

# Раздача статического фронтенда (PWA)
app.mount("/", StaticFiles(directory="static", html=True), name="static")
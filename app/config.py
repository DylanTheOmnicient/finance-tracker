import os

class Settings:
    PROJECT_NAME: str = "Финансовый трекер MVP"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./local_data/finance.db")
    # Секретный ключ для JWT (не используется в MVP, но задел на будущее)
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")

settings = Settings()
# 💰 Финансовый трекер (MVP)

Минималистичное приложение для учёта доходов и расходов, работающее как PWA на FastAPI.

## 🚀 Быстрый старт

1. Клонируйте репозиторий
2. Создайте виртуальное окружение: `python -m venv .venv && source .venv/bin/activate` (Windows: `.venv\Scripts\activate`)
3. Установите зависимости: `pip install -r requirements.txt`
4. Запустите: `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
5. Откройте в браузере телефона `http://<ваш-ip-компьютера>:8000`.
6. Установите как приложение через меню браузера («Добавить на главный экран»).

## 📦 Технологии
- FastAPI, SQLAlchemy, SQLite
- PWA (Service Worker + Web App Manifest)
- Чистый JavaScript (без фреймворков)
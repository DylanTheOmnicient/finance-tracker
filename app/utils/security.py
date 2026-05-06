# Заглушка. В MVP авторизация не используется, но файл готов для расширения.
# Пример JWT:
# from datetime import datetime, timedelta
# from jose import JWTError, jwt
# from passlib.context import CryptContext
# и т.д.

def fake_security():
    return {"user": "anonymous"}
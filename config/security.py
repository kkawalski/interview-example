from datetime import timedelta
import os

# Настройки CORS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# Настройки JWT
JWT_AUTH = {
    "JWT_SECRET_KEY": os.getenv("JWT_SECRET_KEY", "your-secret-key-here"),
    "JWT_ALGORITHM": "HS256",
    "JWT_ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "JWT_REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

# Настройки rate limiting
RATELIMIT_ENABLE = True
RATELIMIT_USE_CACHE = "default"
RATELIMIT_KEY_PREFIX = "ratelimit"

# Настройки паролей
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
]


import os

import dotenv

dotenv.load_dotenv()

# PostgreSQL
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("NOTIFICATION_POSTGRES_DB", "notification_db"),
        "USER": os.environ.get(
            "NOTIFICATION_POSTGRES_USER",
            "notification_user",
        ),
        "PASSWORD": os.environ.get("NOTIFICATION_POSTGRES_PASSWORD"),
        "HOST": os.environ.get("POSTGRES_HOST", "127.0.0.1"),
        "PORT": os.environ.get("POSTGRES_PORT", 5432),
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Redis
REDIS_DB = os.environ.get("NOTIFICATION_REDIS_DB", 0)
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")
REDIS_HOST = os.environ.get("REDIS_HOST", "127.0.0.1")
REDIS_PORT = os.environ.get("REDIS_PORT", 6379)
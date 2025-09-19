import os

import dotenv

dotenv.load_dotenv()


CELERY_BROKER_URL = "redis://:{password}@{host}:{port}/{db}".format(
    password=os.environ.get("REDIS_PASSWORD"),
    host=os.environ.get("REDIS_HOST", "127.0.0.1"),
    port=os.environ.get("REDIS_PORT", 6379),
    db=os.environ.get("NOTIFICATION_REDIS_DB", 0),
)
CELERY_RESULT_BACKEND = "redis://:{password}@{host}:{port}/{db}".format(
    password=os.environ.get("REDIS_PASSWORD"),
    host=os.environ.get("REDIS_HOST", "127.0.0.1"),
    port=os.environ.get("REDIS_PORT", 6379),
    db=os.environ.get("NOTIFICATION_REDIS_DB", 0),
)

import os
from pathlib import Path

import dotenv
from split_settings.tools import include

dotenv.load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DEBUG = os.environ.get("NOTIFICATION_SERVICE_DEBUG", False) == "True"

SECRET_KEY = os.environ.get("NOTIFICATION_SERVICE_SECRET_KEY")

ALLOWED_HOSTS = os.environ.get(
    "NOTIFICATION_SERVICE_ALLOWED_HOSTS",
    ["localhost", "127.0.0.1"],
)

ROOT_URLCONF = 'service_notification.urls'

WSGI_APPLICATION = 'service_notification.wsgi.application'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Components configs
include(
    "components/installed_apps.py",
    "components/middleware.py",
    "components/templates.py",
    "components/databases.py",
    "components/auth.py",
    "components/rest_framework.py",
    "components/open_api.py",
    "components/cors.py",
    "components/logging_format.py",
    "components/celery_confs.py",
    "components/notification_confs.py",
)

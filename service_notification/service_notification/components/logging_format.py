import os
import sys

import dotenv

dotenv.load_dotenv()


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{levelname}] {asctime} {name} {message}",
            "style": "{",
        },
        "simple": {
            "format": "[{levelname}] {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "verbose",
        },
    },
    "loggers": {
        # Django
        "django": {
            "handlers": ["console"],
            "level": os.environ.get(
                "NOTIFICATION_SERVICE_DJANGO_LOG_LVL",
                "DEBUG",
            ),
            "propagate": True,
        },
        # DRF
        "django.request": {
            "handlers": ["console"],
            "level": os.environ.get(
                "NOTIFICATION_SERVICE_DJANGO_REST_LOG_LVL",
                "DEBUG",
            ),
            "propagate": False,
        },
    },
}

import os

import dotenv

dotenv.load_dotenv()


CORS_ALLOW_ALL_ORIGINS = os.environ.get(
    "NOTIFICATION_CORS_ALLOW_ALL_ORIGINS",
    True,
) == "True"
CORS_ALLOW_CREDENTIALS = os.environ.get(
    "NOTIFICATION_CORS_ALLOW_CREDENTIALS",
    True,
) == "True"

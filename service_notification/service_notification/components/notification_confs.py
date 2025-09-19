import os

import dotenv

dotenv.load_dotenv()

# Email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("NOTIFICATION_EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.environ.get("NOTIFICATION_EMAIL_PORT", 587))
EMAIL_USE_TLS = os.environ.get("NOTIFICATION_EMAIL_USE_TLS", True) == "True"
EMAIL_HOST_USER = os.environ.get("NOTIFICATION_EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("NOTIFICATION_EMAIL_HOST_PASSWORD")

# SMS
TWILIO_SID = os.environ.get("NOTIFICATION_TWILIO_SID")
TWILIO_TOKEN = os.environ.get("NOTIFICATION_TWILIO_TOKEN")
TWILIO_PHONE = os.environ.get("NOTIFICATION_TWILIO_PHONE")

# Telegram
TELEGRAM_BOT_TOKEN = os.environ.get("NOTIFICATION_TELEGRAM_BOT_TOKEN")

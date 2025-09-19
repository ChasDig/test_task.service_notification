#!/usr/bin/env bash

set -e

echo "🔄 Выполнение миграций..."
python manage.py migrate
python manage.py collectstatic --no-input

echo "🚀 Запуск приложения..."
uvicorn service_notification.asgi:application --host 0.0.0.0 --port 8000 --workers 4

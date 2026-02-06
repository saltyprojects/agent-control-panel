#!/bin/bash
set -e

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Creating admin user..."
python manage.py create_admin || true

echo "Starting gunicorn..."
exec gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 60

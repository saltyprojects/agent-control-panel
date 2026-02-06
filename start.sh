#!/bin/bash
set -e

# Default PORT if not set
export PORT="${PORT:-8000}"

echo "========================================="
echo "Starting Agent Control Panel"
echo "========================================="

echo "Python version:"
python --version

echo ""
echo "Running migrations..."
python manage.py migrate --noinput || { echo "Migration failed"; exit 1; }

echo ""
echo "Collecting static files..."
python manage.py collectstatic --noinput || { echo "Collectstatic failed"; exit 1; }

echo ""
echo "Creating admin user (if needed)..."
python manage.py create_admin 2>&1 || echo "Admin user creation skipped"

echo ""
echo "========================================="
echo "Starting gunicorn on port $PORT..."
echo "========================================="
exec gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 60 --log-level info

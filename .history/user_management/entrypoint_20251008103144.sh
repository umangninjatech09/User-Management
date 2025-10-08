#!/bin/sh

echo "🚀 Waiting for PostgreSQL to start..."
sleep 5

echo "📦 Applying migrations..."
python manage.py makemigrations
python manage.py migrate

echo "🧱 Collecting static files..."
python manage.py collectstatic --noinput

echo "⚙️ Starting Gunicorn server..."
gunicorn user_management.wsgi:application --bind 0.0.0.0:8000

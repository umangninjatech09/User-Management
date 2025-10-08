#!/bin/sh
# wait-for-db.sh

echo "🚀 Waiting for PostgreSQL..."

# Loop until the database is ready
while ! nc -z db 5432; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 1
done

echo "✅ PostgreSQL is up and running!"

# Run migrations and start Gunicorn (or your preferred server)
echo "📦 Running migrations..."
python manage.py makemigrations 
python manage.py migrate --noinput 

echo "⚙️ Starting Django server..."
gunicorn user_management.wsgi:application --bind 0.0.0.0:8000
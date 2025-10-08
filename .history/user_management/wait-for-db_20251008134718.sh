#!/bin/sh
# wait-for-db.sh: Waits for PostgreSQL to be ready before starting the app.

set -e # Exit immediately if a command exits with a non-zero status

# Host and Port are taken from the environment variables set in docker-compose.yml
DB_HOST="db"
DB_PORT="5432"

echo "🚀 Waiting for PostgreSQL at $DB_HOST:$DB_PORT..."

# Loop until the PostgreSQL port is open (uses netcat 'nc')
while ! nc -z $DB_HOST $DB_PORT; do
  echo "PostgreSQL is unavailable - sleeping for 1 second"
  sleep 1
done

echo "✅ PostgreSQL is up and running!"

# Run Django database operations
echo "📦 Running migrations..."
python manage.py makemigrations 
python manage.py migrate --noinput 

# Start the production server (Gunicorn)
echo "⚙️ Starting Django server..."
exec gunicorn user_management.wsgi:application --bind 0.0.0.0:8000
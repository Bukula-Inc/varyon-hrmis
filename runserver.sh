#!/bin/bash

# chmod +x runserver.sh  =====> command to allow the bash file to execute

# Helper function to check if Redis is running
is_redis_running() {
    nc -z localhost 6379
}

echo "🔍 Checking if Redis is running..."
if is_redis_running; then
    echo "✅ Redis is already running on port 6379"
else
    echo "🚀 Redis is not running. Starting Redis..."
    redis-server &
    sleep 2
fi

echo "🚀 Starting Celery worker (gevent)..."
celery -A multitenancy worker --loglevel=info -P gevent &

echo "🚀 Starting Celery beat..."
celery -A multitenancy beat --loglevel=info &

# Optional: Start Flower (Celery monitoring tool)
# echo "🚀 Starting Flower..."
# celery -A multitenancy flower --port=5555 &

echo "🚀 Starting Django development server..."
python manage.py runserver 8001
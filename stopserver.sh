#!/bin/bash

echo "🛑 Stopping Django development server..."
pkill -f "manage.py runserver"

echo "🛑 Stopping Celery worker..."
pkill -f "celery -A multitenancy worker"

echo "🛑 Stopping Celery beat..."
pkill -f "celery -A multitenancy beat"

# Optional: Stop Flower if you're using it
# echo "🛑 Stopping Flower..."
# pkill -f "celery -A multitenancy flower"

# Only kill Redis if we know this script started it
# WARNING: This will kill Redis regardless of who started it!
echo "🛑 Stopping Redis server (localhost:6379)..."
pkill -f "redis-server"

echo "✅ All services have been stopped."

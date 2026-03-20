#!/bin/bash

#  chmod +x runserver.sh  =====> command to allow the bash file to execute



# Start Redis
redis-server &
# start Celery
# celery -A multitenancy worker --loglevel=info -B &
celery -A multitenancy worker --loglevel=info -P gevent &
celery -A multitenancy beat --loglevel=info &
# start flower server
# celery -A multitenancy flower &8001
# Start Django development server
python manage.py runserver 8001



# # Start Redis
# redis-server &
# redis_pid=$!
# if [ $? -ne 0 ]; then
#   echo "Failed to start Redis"
#   exit 1
# fi

# # Start Celery worker with gevent pool
# celery -A multitenancy worker --loglevel=info -P gevent &
# worker_pid=$!
# if [ $? -ne 0 ]; then
#   echo "Failed to start Celery worker"
#   kill $redis_pid
#   exit 1
# fi

# # Start Celery beat service
# celery -A multitenancy beat --loglevel=info &
# beat_pid=$!
# if [ $? -ne 0 ]; then
#   echo "Failed to start Celery beat"
#   kill $worker_pid
#   kill $redis_pid
#   exit 1
# fi

# # Start Django development server
# python manage.py runserver &
# django_pid=$!
# if [ $? -ne 0 ]; then
#   echo "Failed to start Django development server"
#   kill $beat_pid
#   kill $worker_pid
#   kill $redis_pid
#   exit 1
# fi

# # Wait for any of the services to exit
# while [ -d /proc/$redis_pid ] && [ -d /proc/$worker_pid ] && [ -d /proc/$beat_pid ] && [ -d /proc/$django_pid ]; do
#   sleep 1
# done

# # Stop remaining services
# kill $django_pid
# kill $beat_pid
# kill $worker_pid
# kill $redis_pid

# exit 0






#!/bin/bash

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

echo "Apply database migrate"
python manage.py migrate

# Apply database migrations
echo "Apply database createsuperuser"
python3 manage.py createsuperuser

echo "Apply database makemigrations"
python3 manage.py makemigrations

echo "Apply database migrations"
python manage.py migrate

# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8000
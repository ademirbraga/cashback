#!/bin/bash
# rodar somente se for em ambiente de dev
environment=${environment:-dev}
if [ $# -gt 0 ] ; then
  # Collect static files
  echo "Collect static files"
  python3 manage.py collectstatic --noinput

  echo "Apply database migrate"
  python3 manage.py migrate

  # Apply database migrations
  echo "Apply database createsuperuser"
  python3 manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')"

  echo "Apply database makemigrations"
  python3 manage.py makemigrations

  echo "Apply database migrations"
  python3 manage.py migrate

  # Start server
#  echo "Starting server"
#  python3 manage.py runserver 0.0.0.0:8000
fi
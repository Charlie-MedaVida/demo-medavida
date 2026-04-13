#!/bin/bash
python manage.py migrate --noinput

export DJANGO_SUPERUSER_USERNAME=admin
export DJANGO_SUPERUSER_EMAIL=admin@example.com
export DJANGO_SUPERUSER_PASSWORD=your_secure_password

python manage.py create_admin_user
python manage.py create_api_keys_for_all

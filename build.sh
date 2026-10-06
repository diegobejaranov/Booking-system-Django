#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate

# Comando profesional: crea el usuario usando variables invisibles que lee de Render
python manage.py createsuperuser --noinput || true
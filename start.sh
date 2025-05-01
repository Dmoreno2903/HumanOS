#!/bin/bash

# Esperar a que la base de datos esté lista
echo "Esperando a que la base de datos esté lista..."
sleep 5

# Aplicar migraciones
echo "Aplicando migraciones..."
uv run python manage.py migrate
uv run python manage.py collectstatic --noinput

# Iniciar Gunicorn
echo "Iniciando Gunicorn..."
uv run gunicorn humanos.wsgi:application --bind 0.0.0.0:8000
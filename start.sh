#!/bin/bash

# Esperar a que la base de datos esté lista
echo "Esperando a que la base de datos esté lista..."
sleep 5

# Aplicar migraciones
echo "Aplicando migraciones..."
python manage.py migrate

# Iniciar Gunicorn
echo "Iniciando Gunicorn..."
gunicorn humanos.wsgi:application --bind 0.0.0.0:8000
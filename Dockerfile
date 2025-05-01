# Usa una imagen oficial de Python como imagen base
FROM python:3.13.1-bullseye

# Establece variables de entorno
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Establece el directorio de trabajo
WORKDIR /app

# Instala las dependencias directamente con pip para asegurar su funcionamiento
RUN pip install uv

# Copia el código de la aplicación
COPY . /app/

RUN uv add -r requirements.txt
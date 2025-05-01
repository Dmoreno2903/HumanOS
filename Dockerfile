# Usa una imagen oficial de Python como imagen base
FROM python:3.13.1-bullseye

# Establece variables de entorno
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Establece el directorio de trabajo
WORKDIR /app

# Instala uv
RUN pip install uv

# Copia el código de la aplicación
COPY . /app/

# Instala dependencias usando uv
RUN uv sync
FROM python:3.13.1-bullseye

# Directorio de trabajo
WORKDIR /app
RUN pip install uv

RUN apt-get update && apt-get install -y \
    libreoffice \
    libreoffice-writer \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Copia pyproject.toml
COPY pyproject.toml .
# Instala dependencias
RUN uv pip install -r pyproject.toml --system

# Dependencias de playwright requeridas
RUN playwright install --with-deps

# Copia el resto del código
COPY . .
FROM python:3.13.1-bullseye

# Directorio de trabajo
WORKDIR /app
RUN pip install uv

# Copia pyproject.toml
COPY pyproject.toml .
# Instala dependencias
RUN uv pip install -r pyproject.toml --system

# Copia el resto del código
COPY . .
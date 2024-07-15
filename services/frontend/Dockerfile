FROM python:3.10-slim

WORKDIR /app

COPY . /app

# Actualizar pip
RUN pip install --upgrade pip

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Comando para ejecutar el servidor en modo producción
CMD ["gunicorn", "--bind", "0.0.0.0:5050", "src.app:app", "--workers", "4", "--timeout", "120"]
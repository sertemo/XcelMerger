FROM python:3.10-slim

WORKDIR /app

COPY . /app

# Actualizar pip
RUN pip install --upgrade pip

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

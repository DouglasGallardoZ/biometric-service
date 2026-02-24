FROM ubuntu:24.04

# Establecer variables de entorno
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive
ENV DB_USER=admin
ENV DB_PASSWORD=password123
ENV DB_HOST=biometric_db
ENV DB_PORT=5432
ENV DB_NAME=urbanizacion_db
ENV STORAGE_TYPE=gcs
ENV GCS_BUCKET_NAME=biometric-fotos
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/applied-pipe-308521-724bd62924dd.json

# Actualizar paquetes e instalar Python y dependencias
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos del proyecto
COPY . /app
COPY .env.example /app/.env

# Instalar dependencias de Python
RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt

# Exponer el puerto
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
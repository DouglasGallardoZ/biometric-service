FROM python:3.12-slim

# Establecer variables de entorno
ENV PYTHONUNBUFFERED=1

# Instalar dependencias del sistema necesarias para compilar C/C++ (para insightface)
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Establecer directorio de trabajo
WORKDIR /app

# Copiar solo requirements.txt para aprovechar el caché de Docker
COPY requirements.txt /app/

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del proyecto
COPY . /app

# Exponer el puerto
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
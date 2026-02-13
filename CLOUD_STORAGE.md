# 🌐 Cloud Storage - Guía de Integración

## Descripción

Tu arquitectura hexagonal permite cambiar **sin tocar el código de negocio**:

```
local ← cambiar entre → S3 ← cambiar entre → GCS
```

Solo configura una variable de entorno.

---

## Opción 1: AWS S3 (Recomendado)

### Setup

#### 1. Crear bucket en AWS

```bash
# Desde AWS Console o CLI
aws s3 mb s3://mi-biometric-fotos --region us-east-1
```

#### 2. Obtener credenciales

1. En AWS Console → IAM → Users
2. Crear usuario con permisos S3:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:DeleteObject"
            ],
            "Resource": "arn:aws:s3:::mi-biometric-fotos/*"
        }
    ]
}
```

3. Copiar access key y secret key

#### 3. Configurar .env

```bash
STORAGE_TYPE=s3
S3_BUCKET_NAME=mi-biometric-fotos
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
AWS_REGION=us-east-1
```

#### 4. Instalar dependencia

```bash
pip install boto3
# O ya está en requirements.txt
pip install -r requirements.txt
```

#### 5. Ejecutar

```bash
uvicorn app.main:app --reload
```

**¡Listo!** Las fotos se guardarán automáticamente en S3.

---

## Opción 2: Google Cloud Storage

### Setup

#### 1. Crear proyecto y bucket en GCP

```bash
# Desde GCP Console o gcloud CLI
gcloud storage buckets create gs://mi-biometric-fotos --location=us-central1
```

#### 2. Crear service account

1. En GCP Console → Service Accounts
2. Crear service account: `biometric-service`
3. Crear clave JSON
4. Descargar archivo `clave.json`

#### 3. Configurar .env

```bash
STORAGE_TYPE=gcs
GCS_BUCKET_NAME=mi-biometric-fotos
GOOGLE_APPLICATION_CREDENTIALS=/ruta/a/clave.json
```

#### 4. Instalar dependencia

```bash
pip install google-cloud-storage
# O ya está en requirements.txt
```

#### 5. Ejecutar

```bash
uvicorn app.main:app --reload
```

**¡Listo!** Las fotos se guardarán automáticamente en GCS.

---

## Opción 3: Seguir con Almacenamiento Local

Simplemente déjalo como está:

```bash
STORAGE_TYPE=local
UPLOADS_DIR=uploads
```

---

## Cambiar de Storage Dinámicamente

### Ejemplo: Migrar de Local a S3

Cambiar solo una variable:

```bash
# Antes (local)
STORAGE_TYPE=local

# Después (S3)
STORAGE_TYPE=s3
S3_BUCKET_NAME=mi-biometric-fotos
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
```

Reiniciar aplicación. **¡Eso es todo!**

El dominio y lógica de negocio **NO cambian**.

---

## Ventajas de Cada Opción

### 🏠 Local
- ✅ Fácil de desarrollar
- ✅ Sin costos
- ✅ Control total
- ❌ Mantenimiento manual
- ❌ Escalabilidad limitada

### ☁️ S3
- ✅ Escalable globalmente
- ✅ Highly available
- ✅ Pricing flexible
- ✅ Integración con CDN
- ❌ Requiere AWS
- ⚠️ Costo por uso

### 📦 GCS
- ✅ Integración con Google Cloud
- ✅ Excelente para ML
- ✅ Flexible
- ❌ Requiere GCP
- ⚠️ Costo por uso

---

## Monitorear Almacenamiento

### AWS S3
```bash
# Ver tamaño total
aws s3 ls s3://mi-biometric-fotos --recursive --summarize

# Ver archivos
aws s3 ls s3://mi-biometric-fotos/fotos/
```

### Google Cloud Storage
```bash
# Ver tamaño y archivos
gsutil du -sh gs://mi-biometric-fotos/

# Listar archivos
gsutil ls gs://mi-biometric-fotos/fotos/
```

---

## Obtener URLs de Descarga

Si quieres servir las imágenes a través de URLs:

### Para S3

```python
from app.adaptadores.s3 import AdaptadorS3

adaptador = AdaptadorS3("mi-biometric-fotos")

# URL válida por 1 hora
url = adaptador.obtener_url_descarga("persona_1_0_123456.jpg", expiracion=3600)
print(url)  # https://s3.amazonaws.com/...
```

### Para GCS

```python
from app.adaptadores.gcs import AdaptadorGoogleCloudStorage

adaptador = AdaptadorGoogleCloudStorage("mi-biometric-fotos")

# URL válida por 1 hora
url = adaptador.obtener_url_descarga("persona_1_0_123456.jpg", expiracion_horas=1)
print(url)  # https://storage.googleapis.com/...
```

---

## Crear Nuevo Adaptador de Storage

Si quieres usar otro proveedor (DigitalOcean Spaces, Azure Blob, etc.):

### 1. Crear el adaptador

```python
# app/adaptadores/mi_provider.py
from app.domain.puertos import PuertoSistemaArchivos

class AdaptadorMiProvider(PuertoSistemaArchivos):
    def guardar_imagen(self, contenido: bytes, ruta: str) -> bool:
        # Tu implementación
        pass
    
    def obtener_ruta_imagen(self, persona_titular_fk: int, indice: int) -> str:
        # Tu implementación
        pass
```

### 2. Actualizar configurador

```python
# app/infraestructura/configuracion.py
from app.adaptadores.mi_provider import AdaptadorMiProvider

def crear_sistema_archivos(self):
    if self.storage_type == "mi_provider":
        return AdaptadorMiProvider(...)
```

### 3. Usar

```bash
STORAGE_TYPE=mi_provider
```

**¡Sin cambios en el dominio!**

---

## Troubleshooting

### Error: S3 "Access Denied"
- Verifica AWS_ACCESS_KEY_ID y AWS_SECRET_ACCESS_KEY
- Verifica permisos del bucket en IAM

### Error: GCS "Credential not found"
- Verifica GOOGLE_APPLICATION_CREDENTIALS apunta a archivo válido
- Verifica permisos del service account

### Error: "bucket not found"
- Verifica nombre exacto del bucket
- Verifica que pertenece a la región configurada

### Las fotos no se guardan
- Revisa logs: `STORAGE_TYPE` configurado correctamente
- Verifica conectividad a internet
- Revisa credenciales

---

## Performance

| Métrica | Local | S3 | GCS |
|---------|-------|----|----|
| Escritura | < 10ms | 100-300ms | 100-300ms |
| Lectura | < 10ms | 100-300ms | 100-300ms |
| Escalabilidad | Local | Global | Global |
| Redundancia | Manual | Automática | Automática |

---

## Costos Estimados (mensual)

### AWS S3
- Almacenamiento: $0.023 por GB
- Transferencia: $0.09 por GB (salida)
- Requests: Negligible

**Ejemplo**: 1000 fotos × 500KB = 500GB = ~$12/mes

### Google Cloud Storage
- Almacenamiento: $0.020 por GB
- Transferencia: $0.12 por GB (salida)
- Requests: Negligible

**Ejemplo**: 1000 fotos × 500KB = 500GB = ~$10/mes

---

## Recomendación

**Para Producción**: AWS S3
- Mejor relación precio/rendimiento
- Amplia comunidad
- Excelente documentación

**Para Desarrollo**: Local
- Gratis
- Más rápido en tests
- No requiere credenciales

---

**Con la arquitectura hexagonal, cambiar de storage es trivial. Solo una variable de entorno. ¡Genial!** 🎉

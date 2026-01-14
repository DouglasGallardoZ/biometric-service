# Biometric Service (Face Recognition)

Microservicio en FastAPI que implementa enrolamiento y verificación facial usando InsightFace (modelo `buffalo_s`) corriendo exclusivamente en CPU con ONNX Runtime (`CPUExecutionProvider`).

Características:
- Enrolamiento (3 imágenes) -> promedio de embeddings, normalizado y almacenado en PostgreSQL usando `pgvector`.
- Verificación (1:1) -> compara embedding con el vector almacenado usando distancia coseno (umbral por defecto 0.6).
- Validación documento-rostro -> compara dos imágenes y devuelve distancia y booleano de match.

Requisitos:
- PostgreSQL con extensión `vector` (pgvector). Ejemplo: `CREATE EXTENSION IF NOT EXISTS vector;`
- Variables de entorno:
  - `DATABASE_URL` (ej: `postgresql://postgres:postgres@localhost:5432/biometric`)
  - `VERIFICATION_THRESHOLD` (opcional, por defecto `0.6`)

Arranque:
1. Instalar dependencias: `pip install -r requirements.txt`
2. Descargar modelos InsightFace en caso de que no lo haga automáticamente (InsightFace suele gestionar la descarga en `~/.insightface`).
3. Ejecutar el servidor: `uvicorn app.main:app --host 0.0.0.0 --port 8000`

API - Ejemplos de uso:

- Enrolamiento (3 imágenes):

```bash
curl -X POST "http://localhost:8000/enroll" \
  -F "user_id=resident_123" \
  -F "images=@/path/to/img1.jpg" \
  -F "images=@/path/to/img2.jpg" \
  -F "images=@/path/to/img3.jpg"
```

- Verificación (1:1):

```bash
curl -X POST "http://localhost:8000/verify" \
  -F "user_id=resident_123" \
  -F "image=@/path/to/probe.jpg"
```

- Validación documento-rostro:

```bash
curl -X POST "http://localhost:8000/validate" \
  -F "foto_cedula=@/path/to/id_photo.jpg" \
  -F "foto_rostro_vivo=@/path/to/live_face.jpg"
```

Notas de base de datos:

- Asegúrate de ejecutar `CREATE EXTENSION IF NOT EXISTS vector;` en la BD antes de usar el servicio o usa un usuario con permisos para crear extensiones.
- La tabla `residents` será creada automáticamente por la aplicación si no existe.

Notas sobre modelos y ONNX Runtime (CPU):

- Este proyecto usa `insightface` con el modelo `buffalo_s`. InsightFace descargará el modelo al primer uso en `~/.insightface` por defecto.
- Para forzar CPU se configura `FaceAnalysis(..., providers=["CPUExecutionProvider"])` y `prepare(ctx_id=-1)`.
- Asegúrate de tener `onnxruntime` instalado y compatible con `CPUExecutionProvider` (paquete `onnxruntime`).

Variables de entorno recomendadas:

- `DATABASE_URL` - URL de conexión a PostgreSQL (ej: `postgresql://postgres:postgres@localhost:5432/biometric`).
- `VERIFICATION_THRESHOLD` - umbral de distancia coseno para verificación (por defecto 0.6).

Ejemplo `.env`:

```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/biometric
VERIFICATION_THRESHOLD=0.6
```

Notas:
- Esta implementación usa llamadas de DB sincrónicas mediante SQLAlchemy; en producción se recomienda usar el modo asíncrono o ejecutar en threadpool (ya se usa `run_in_threadpool` en los endpoints para llamadas costosas).
- Asegúrate de tener `onnxruntime` compatible con el `CPUExecutionProvider`.

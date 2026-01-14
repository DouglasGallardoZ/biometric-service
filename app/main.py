import os
import logging
from typing import List

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from starlette.concurrency import run_in_threadpool

from app.core.face_engine import FaceEngine, ErrorSinRostroDetectado
from app.core.database import DataBase
from app.models.schemas import EnrollResponse, VerifyResponse, ValidateResponse
from app.utils.image_proc import leer_archivo_imagen

# Basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("biometric-service")


app = FastAPI(title="Biometric Service - Face Recognition (CPU)")

motor_rostros: FaceEngine = None
bd: DataBase = None
UMBRAL = float(os.getenv("VERIFICATION_THRESHOLD", "0.6"))


@app.on_event("startup")
def evento_inicio():
    global motor_rostros, bd
    # Initialize face engine (ONNX CPU)
    motor_rostros = FaceEngine(nombre_modelo="buffalo_s")

    # Initialize database
    url_base_datos = os.getenv("DATABASE_URL", "postgresql://admin:password123@localhost:5432/urbanizacion_db")
    bd = DataBase(url_base_datos)
    bd.inicializar_bd()


@app.post("/enroll", response_model=EnrollResponse)
async def registrar_residente(user_id: str = Form(...), images: List[UploadFile] = File(...)):
    if len(images) != 3:
        raise HTTPException(status_code=400, detail="Exactly 3 images are required for enrollment")

    # Read and compute embeddings
    embeddings = []
    for archivo in images:
        try:
            img = await leer_archivo_imagen(archivo)
        except ValueError as e:
            raise HTTPException(status_code=422, detail=str(e))
        try:
            emb = await run_in_threadpool(motor_rostros.obtener_incrustacion, img)
            embeddings.append(emb)
        except ErrorSinRostroDetectado as e:
            raise HTTPException(status_code=422, detail=str(e))

    # Average, normalize and store
    inc_promedio = await run_in_threadpool(motor_rostros.incrustacion_promedio, embeddings)
    try:
        await run_in_threadpool(bd.insertar_o_actualizar_residente, user_id, inc_promedio.tolist())
    except Exception as e:
        logger.exception("DB error during upsert_resident")
        raise HTTPException(status_code=500, detail="Database error during enrolment")

    logger.info(f"Enrolled user_id={user_id}")
    return EnrollResponse(user_id=user_id, status="enrolled")


@app.post("/verify", response_model=VerifyResponse)
async def verificar_residente(user_id: str = Form(...), image: UploadFile = File(...)):
    try:
        img = await leer_archivo_imagen(image)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    try:
        emb = await run_in_threadpool(motor_rostros.obtener_incrustacion, img)
    except ErrorSinRostroDetectado as e:
        raise HTTPException(status_code=422, detail=str(e))

    # Compare directly in DB using cosine distance
    try:
        inc2 = await run_in_threadpool(bd.obtener_incrustacion_residente, user_id)
    except Exception as e:
        logger.exception("DB error during get resident embedding")
        raise HTTPException(status_code=500, detail="Database error during verification")
    
    # compute cosine distance in Python
    distancia = motor_rostros.distancia_coseno(emb, inc2)
    coincide = distancia <= UMBRAL
    logger.info(f"Validation match={coincide} distance={distancia}")
    return VerifyResponse(user_id=user_id, match=coincide, distance=float(distancia))


@app.post("/validate", response_model=ValidateResponse)
async def validar_visita(foto_cedula: UploadFile = File(...), foto_rostro_vivo: UploadFile = File(...)):
    try:
        img1 = await leer_archivo_imagen(foto_cedula)
        img2 = await leer_archivo_imagen(foto_rostro_vivo)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    try:
        inc1 = await run_in_threadpool(motor_rostros.obtener_incrustacion, img1)
        inc2 = await run_in_threadpool(motor_rostros.obtener_incrustacion, img2)
    except ErrorSinRostroDetectado as e:
        raise HTTPException(status_code=422, detail=str(e))

    # compute cosine distance in Python
    distancia = motor_rostros.distancia_coseno(inc1, inc2)
    coincide = distancia <= UMBRAL
    logger.info(f"Validation match={coincide} distance={distancia}")
    return ValidateResponse(match=coincide, distance=float(distancia))

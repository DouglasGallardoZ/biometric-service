import os
import logging
from typing import List

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from starlette.concurrency import run_in_threadpool

from app.core.face_engine import FaceEngine, NoFaceDetectedError
from app.core.database import Database
from app.models.schemas import EnrollResponse, VerifyResponse, ValidateResponse
from app.utils.image_proc import read_imagefile

# Basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("biometric-service")


app = FastAPI(title="Biometric Service - Face Recognition (CPU)")

face_engine: FaceEngine = None
db: Database = None
THRESHOLD = float(os.getenv("VERIFICATION_THRESHOLD", "0.6"))


@app.on_event("startup")
def startup_event():
    global face_engine, db
    # Initialize face engine (ONNX CPU)
    face_engine = FaceEngine(model_name="buffalo_s")

    # Initialize database
    database_url = os.getenv("DATABASE_URL", "postgresql://admin:password123@localhost:5432/urbanizacion_db")
    db = Database(database_url)
    db.init_db()


@app.post("/enroll", response_model=EnrollResponse)
async def enroll_resident(user_id: str = Form(...), images: List[UploadFile] = File(...)):
    if len(images) != 3:
        raise HTTPException(status_code=400, detail="Exactly 3 images are required for enrollment")

    # Read and compute embeddings
    embeddings = []
    for f in images:
        try:
            img = await read_imagefile(f)
        except ValueError as e:
            raise HTTPException(status_code=422, detail=str(e))
        try:
            emb = await run_in_threadpool(face_engine.get_embedding, img)
            embeddings.append(emb)
        except NoFaceDetectedError as e:
            raise HTTPException(status_code=422, detail=str(e))

    # Average, normalize and store
    mean_emb = await run_in_threadpool(face_engine.mean_embedding, embeddings)
    try:
        await run_in_threadpool(db.upsert_resident, user_id, mean_emb.tolist())
    except Exception as e:
        logger.exception("DB error during upsert_resident")
        raise HTTPException(status_code=500, detail="Database error during enrolment")

    logger.info(f"Enrolled user_id={user_id}")
    return EnrollResponse(user_id=user_id, status="enrolled")


@app.post("/verify", response_model=VerifyResponse)
async def verify_resident(user_id: str = Form(...), image: UploadFile = File(...)):
    try:
        img = await read_imagefile(image)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    try:
        emb = await run_in_threadpool(face_engine.get_embedding, img)
    except NoFaceDetectedError as e:
        raise HTTPException(status_code=422, detail=str(e))

    # Compare directly in DB using cosine distance
    try:
        emb2 = await run_in_threadpool(db.get_resident_embedding, user_id)
    except Exception as e:
        logger.exception("DB error during get resident embedding")
        raise HTTPException(status_code=500, detail="Database error during verification")
    
    # compute cosine distance in Python
    dist = face_engine.cosine_distance(emb, emb2)
    match = dist <= THRESHOLD
    logger.info(f"Validation match={match} distance={dist}")
    return VerifyResponse(user_id=user_id, match=match, distance=float(dist))


@app.post("/validate", response_model=ValidateResponse)
async def validate_visit(foto_cedula: UploadFile = File(...), foto_rostro_vivo: UploadFile = File(...)):
    try:
        img1 = await read_imagefile(foto_cedula)
        img2 = await read_imagefile(foto_rostro_vivo)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    try:
        emb1 = await run_in_threadpool(face_engine.get_embedding, img1)
        emb2 = await run_in_threadpool(face_engine.get_embedding, img2)
    except NoFaceDetectedError as e:
        raise HTTPException(status_code=422, detail=str(e))

    # compute cosine distance in Python
    dist = face_engine.cosine_distance(emb1, emb2)
    match = dist <= THRESHOLD
    logger.info(f"Validation match={match} distance={dist}")
    return ValidateResponse(match=match, distance=float(dist))

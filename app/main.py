"""API principal - Capa de presentación."""

import logging
from typing import List

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from starlette.concurrency import run_in_threadpool

from app.infraestructura.configuracion import ConfiguradorAplicacion
from app.models.schemas import EnrollResponse, VerifyResponse, ValidateResponse
from app.domain.models import ErrorSinRostroDetectado, ErrorVerificacion
from app.domain.casos_uso import (
    CasoDeUsoEnrollamiento, CasoDeUsoVerificacion, CasoDeUsoValidacionVisita
)

# Configuración básica de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("biometric-service")


app = FastAPI(
    title="Biometric Service - Face Recognition (CPU)",
    openapi_prefix="/api/v1"
)

# Configuración de inyección de dependencias
config = ConfiguradorAplicacion()

# Casos de uso (inyectados)
caso_enrollamiento: CasoDeUsoEnrollamiento = None
caso_verificacion: CasoDeUsoVerificacion = None
caso_validacion_visita: CasoDeUsoValidacionVisita = None


@app.on_event("startup")
def evento_inicio():
    """Inicializar aplicación."""
    global caso_enrollamiento, caso_verificacion, caso_validacion_visita
    
    logger.info("Inicializando aplicación...")
    try:
        caso_enrollamiento = config.crear_caso_enrollamiento()
        caso_verificacion = config.crear_caso_verificacion()
        caso_validacion_visita = config.crear_caso_validacion_visita()
        logger.info("Aplicación inicializada correctamente")
    except Exception as e:
        logger.error(f"Error inicializando aplicación: {e}")
        raise


@app.post("/enroll", response_model=EnrollResponse)
async def registrar_residente(
    user_id: int = Form(...),
    usuario_creado: str = Form(...),
    images: List[UploadFile] = File(...)
):
    """Registrar una persona con sus fotos faciales.
    
    - **user_id**: ID de la persona a registrar
    - **usuario_creado**: Usuario que realiza el registro (auditoría)
    - **images**: Mínimo 3 imágenes faciales
    """
    try:
        if len(images) < 3:
            raise ValueError("Se requieren al menos 3 imágenes para enrollar")
        
        # Leer contenido de todas las imágenes
        imagenes_bytes = []
        for imagen in images:
            contenido = await imagen.read()
            imagenes_bytes.append(contenido)
        
        # Ejecutar caso de uso en threadpool
        resultado = await run_in_threadpool(
            caso_enrollamiento.ejecutar,
            user_id,
            usuario_creado,
            imagenes_bytes
        )
        
        logger.info(
            f"Persona {user_id} enrollada correctamente con "
            f"{resultado['fotos_guardadas']} fotos"
        )
        return EnrollResponse(user_id=str(user_id), status="enrolled")
        
    except ValueError as e:
        logger.warning(f"Error en enrollamiento: {str(e)}")
        raise HTTPException(status_code=422, detail=str(e))
    except ErrorSinRostroDetectado as e:
        logger.warning(f"No se detectó rostro: {str(e)}")
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.exception("Error en enrollamiento")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@app.post("/verify", response_model=VerifyResponse)
async def verificar_residente(
    user_id: int = Form(...),
    image: UploadFile = File(...)
):
    """Verificar identidad de una persona contra su registro.
    
    - **user_id**: ID de la persona a verificar
    - **image**: Imagen facial para verificación
    """
    try:
        # Leer imagen
        contenido = await image.read()
        
        # Ejecutar caso de uso en threadpool
        resultado = await run_in_threadpool(
            caso_verificacion.ejecutar,
            user_id,
            contenido
        )
        
        logger.info(
            f"Verificación de persona {user_id}: "
            f"coincide={resultado.coincide}, distancia={resultado.distancia:.4f}"
        )
        return VerifyResponse(
            user_id=str(user_id),
            match=resultado.coincide,
            distance=float(resultado.distancia)
        )
        
    except ErrorSinRostroDetectado as e:
        logger.warning(f"No se detectó rostro en imagen de verificación: {str(e)}")
        raise HTTPException(status_code=422, detail=str(e))
    except ErrorVerificacion as e:
        logger.warning(f"Error en verificación: {str(e)}")
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.exception("Error en verificación")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@app.post("/validate", response_model=ValidateResponse)
async def validar_visita(
    foto_cedula: UploadFile = File(...),
    foto_rostro_vivo: UploadFile = File(...)
):
    """Validar que el rostro vivo coincide con la foto de cédula.
    
    - **foto_cedula**: Foto del documento de identidad
    - **foto_rostro_vivo**: Foto del rostro en vivo
    """
    try:
        # Leer imágenes
        contenido_cedula = await foto_cedula.read()
        contenido_vivo = await foto_rostro_vivo.read()
        
        # Ejecutar caso de uso en threadpool
        resultado = await run_in_threadpool(
            caso_validacion_visita.ejecutar,
            contenido_cedula,
            contenido_vivo
        )
        
        logger.info(
            f"Validación de visita: "
            f"coincide={resultado.coincide}, distancia={resultado.distancia:.4f}"
        )
        return ValidateResponse(
            match=resultado.coincide,
            distance=float(resultado.distancia)
        )
        
    except ErrorSinRostroDetectado as e:
        logger.warning(f"No se detectó rostro en validación: {str(e)}")
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.exception("Error en validación")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@app.get("/health")
async def health_check():
    """Verificar estado de la aplicación."""
    return {"status": "healthy"}

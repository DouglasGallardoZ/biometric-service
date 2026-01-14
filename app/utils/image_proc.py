import cv2
import numpy as np
from fastapi import UploadFile


async def leer_archivo_imagen(archivo: UploadFile) -> np.ndarray:
    """Read UploadFile and return an RGB image as numpy array suitable for insightface.

    Raises ValueError if the image cannot be decoded.
    """
    contenido = await archivo.read()
    arreglo = np.frombuffer(contenido, dtype=np.uint8)
    img = cv2.imdecode(arreglo, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Could not decode image")
    # convert BGR -> RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img_rgb

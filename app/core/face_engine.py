from typing import List
from io import BytesIO

import numpy as np
from PIL import Image

from insightface.app import FaceAnalysis


class ErrorSinRostroDetectado(Exception):
    pass


class FaceEngine:
    def __init__(self, nombre_modelo: str = "buffalo_s"):
        """Inicializar FaceAnalysis usando ONNX CPUExecutionProvider.

        Nota: Asegurar que `onnxruntime` esté instalado y que `CPUExecutionProvider` esté disponible.
        """
        # Usar proveedor de ejecución CPU
        try:
            self.app = FaceAnalysis(name=nombre_modelo, providers=["CPUExecutionProvider"])
            # ctx_id=-1 forces CPU
            self.app.prepare(ctx_id=-1)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize FaceAnalysis: {e}")

    def obtener_incrustacion(self, img: np.ndarray) -> np.ndarray:
        """Retornar una incrustación normalizada para el rostro más grande detectado.

        Lanza ErrorSinRostroDetectado si no se encuentra ningún rostro.
        """
        rostros = self.app.get(img)
        if not rostros:
            raise ErrorSinRostroDetectado("No face detected in the provided image")

        # Seleccionar el rostro más grande (usualmente el primero) y obtener .embedding
        rostro = rostros[0]
        inc = np.asarray(rostro.embedding, dtype=np.float32)
        # Normalizar
        norma = np.linalg.norm(inc)
        if norma == 0:
            raise ErrorSinRostroDetectado("Invalid embedding (zero norm)")
        return inc / norma

    def obtener_incrustacion_desde_bytes(self, contenido: bytes) -> np.ndarray:
        """Convertir bytes de imagen a ndarray y retornar incrustación normalizada.
        
        Lanza ErrorSinRostroDetectado si no se encuentra ningún rostro.
        """
        try:
            img = Image.open(BytesIO(contenido)).convert('RGB')
            img_array = np.asarray(img)
            return self.obtener_incrustacion(img_array)
        except Exception as e:
            raise ErrorSinRostroDetectado(f"Failed to process image: {str(e)}")

    def incrustacion_promedio(self, incrustaciones: List[np.ndarray]) -> np.ndarray:
        """Calcular la incrustación promedio y normalizarla."""
        promedio = np.mean(np.stack(incrustaciones, axis=0), axis=0)
        norma = np.linalg.norm(promedio)
        if norma == 0:
            raise ValueError("Mean embedding has zero norm")
        return promedio / norma

    def distancia_coseno(self, a: np.ndarray, b: np.ndarray) -> float:
        """Retornar distancia coseno (1 - similitud_coseno)."""
        a = np.asarray(a, dtype=np.float32)
        b = np.asarray(b, dtype=np.float32)
        producto_punto = float(np.dot(a, b))
        norma_a = np.linalg.norm(a)
        norma_b = np.linalg.norm(b)
        if norma_a == 0 or norma_b == 0:
            return 1.0
        similitud_coseno = producto_punto / (norma_a * norma_b)
        # Distancia coseno
        return 1.0 - similitud_coseno

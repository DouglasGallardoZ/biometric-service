from typing import List

import numpy as np

from insightface.app import FaceAnalysis


class ErrorSinRostroDetectado(Exception):
    pass


class FaceEngine:
    def __init__(self, nombre_modelo: str = "buffalo_s"):
        """Initialize FaceAnalysis using ONNX CPUExecutionProvider.

        Note: Ensure that `onnxruntime` is installed and that `CPUExecutionProvider` is available.
        """
        # Uso extension de CPU
        try:
            self.app = FaceAnalysis(name=nombre_modelo, providers=["CPUExecutionProvider"])
            # ctx_id=-1 forces CPU
            self.app.prepare(ctx_id=-1)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize FaceAnalysis: {e}")

    def obtener_incrustacion(self, img: np.ndarray) -> np.ndarray:
        """Return a normalized embedding for the largest detected face.

        Raises ErrorSinRostroDetectado if no face is found.
        """
        rostros = self.app.get(img)
        if not rostros:
            raise ErrorSinRostroDetectado("No face detected in the provided image")

        # pick largest face (usually first) and get .embedding
        rostro = rostros[0]
        inc = np.asarray(rostro.embedding, dtype=np.float32)
        # normalize
        norma = np.linalg.norm(inc)
        if norma == 0:
            raise ErrorSinRostroDetectado("Invalid embedding (zero norm)")
        return inc / norma

    def incrustacion_promedio(self, incrustaciones: List[np.ndarray]) -> np.ndarray:
        """Compute mean embedding and normalize it."""
        promedio = np.mean(np.stack(incrustaciones, axis=0), axis=0)
        norma = np.linalg.norm(promedio)
        if norma == 0:
            raise ValueError("Mean embedding has zero norm")
        return promedio / norma

    def distancia_coseno(self, a: np.ndarray, b: np.ndarray) -> float:
        """Return cosine distance (1 - cosine_similarity)."""
        a = np.asarray(a, dtype=np.float32)
        b = np.asarray(b, dtype=np.float32)
        producto_punto = float(np.dot(a, b))
        norma_a = np.linalg.norm(a)
        norma_b = np.linalg.norm(b)
        if norma_a == 0 or norma_b == 0:
            return 1.0
        similitud_coseno = producto_punto / (norma_a * norma_b)
        # cosine distance
        return 1.0 - similitud_coseno

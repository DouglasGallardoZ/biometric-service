"""Adaptador para análisis de rostros usando InsightFace."""

from io import BytesIO
import numpy as np
from PIL import Image
from insightface.app import FaceAnalysis

from app.domain.models import Embedding, ErrorSinRostroDetectado
from app.domain.puertos import PuertoAnalizadorRostros


class AdaptadorInsightFaceAnalyzer(PuertoAnalizadorRostros):
    """Implementación usando InsightFace con ejecución en CPU."""
    
    def __init__(self, nombre_modelo: str = "buffalo_s"):
        """Inicializar FaceAnalysis usando ONNX CPUExecutionProvider."""
        try:
            self.app = FaceAnalysis(
                name=nombre_modelo,
                providers=["CPUExecutionProvider"]
            )
            self.app.prepare(ctx_id=-1)  # -1 forces CPU
        except Exception as e:
            raise RuntimeError(f"Error inicializando FaceAnalysis: {e}")
    
    def obtener_embedding_desde_bytes(self, contenido: bytes) -> Embedding:
        """Obtener embedding desde bytes de imagen."""
        try:
            img = Image.open(BytesIO(contenido)).convert('RGB')
            img_array = np.asarray(img)
            return self.obtener_embedding_desde_array(img_array)
        except Exception as e:
            raise ErrorSinRostroDetectado(f"Error procesando imagen: {str(e)}")
    
    def obtener_embedding_desde_array(self, img_array: np.ndarray) -> Embedding:
        """Obtener embedding desde array numpy de imagen."""
        rostros = self.app.get(img_array)
        if not rostros:
            raise ErrorSinRostroDetectado("No se detectó rostro en la imagen")
        
        # Usar el rostro más grande (usualmente el primero)
        rostro = rostros[0]
        embedding_vector = np.asarray(rostro.embedding, dtype=np.float32)
        
        # Normalizar
        norma = np.linalg.norm(embedding_vector)
        if norma == 0:
            raise ErrorSinRostroDetectado("Embedding inválido (norma cero)")
        
        embedding_normalizado = embedding_vector / norma
        return Embedding(vector=embedding_normalizado)
    
    def calcular_embedding_promedio(self, embeddings: list[Embedding]) -> Embedding:
        """Calcular embedding promedio de múltiples embeddings."""
        if not embeddings:
            raise ValueError("Se requiere al menos un embedding")
        
        vectores = np.array([e.vector for e in embeddings])
        promedio = np.mean(vectores, axis=0)
        
        # Normalizar
        norma = np.linalg.norm(promedio)
        if norma == 0:
            raise ValueError("Embedding promedio tiene norma cero")
        
        return Embedding(vector=promedio / norma)
    
    def calcular_distancia_coseno(self, embedding1: Embedding, embedding2: Embedding) -> float:
        """Calcular distancia coseno entre dos embeddings."""
        a = np.asarray(embedding1.vector, dtype=np.float32)
        b = np.asarray(embedding2.vector, dtype=np.float32)
        
        producto_punto = float(np.dot(a, b))
        norma_a = np.linalg.norm(a)
        norma_b = np.linalg.norm(b)
        
        if norma_a == 0 or norma_b == 0:
            return 1.0
        
        similitud_coseno = producto_punto / (norma_a * norma_b)
        # Distancia coseno
        return 1.0 - similitud_coseno

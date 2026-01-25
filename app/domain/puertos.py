"""Puertos (interfaces) para adaptadores externos."""

from abc import ABC, abstractmethod
from typing import Optional
import numpy as np

from app.domain.models import Embedding, PersonaFoto, PersonaEmbedding


class PuertoAnalizadorRostros(ABC):
    """Puerto para análisis de rostros (detector de caras, generador de embeddings)."""
    
    @abstractmethod
    def obtener_embedding_desde_bytes(self, contenido: bytes) -> Embedding:
        """Obtener embedding desde bytes de imagen."""
        pass
    
    @abstractmethod
    def obtener_embedding_desde_array(self, img_array: np.ndarray) -> Embedding:
        """Obtener embedding desde array numpy de imagen."""
        pass
    
    @abstractmethod
    def calcular_embedding_promedio(self, embeddings: list[Embedding]) -> Embedding:
        """Calcular embedding promedio de múltiples embeddings."""
        pass
    
    @abstractmethod
    def calcular_distancia_coseno(self, embedding1: Embedding, embedding2: Embedding) -> float:
        """Calcular distancia coseno entre dos embeddings."""
        pass


class PuertoAlmacenamientoFotos(ABC):
    """Puerto para almacenamiento de fotos de personas."""
    
    @abstractmethod
    def guardar_foto(self, foto: PersonaFoto) -> int:
        """Guardar foto y retornar el ID."""
        pass
    
    @abstractmethod
    def obtener_foto(self, foto_pk: int) -> Optional[PersonaFoto]:
        """Obtener foto por ID."""
        pass
    
    @abstractmethod
    def obtener_fotos_persona(self, persona_titular_fk: int) -> list[PersonaFoto]:
        """Obtener todas las fotos no eliminadas de una persona."""
        pass


class PuertoAlmacenamientoEmbeddings(ABC):
    """Puerto para almacenamiento de embeddings promedios."""
    
    @abstractmethod
    def guardar_embedding(self, persona_embedding: PersonaEmbedding) -> int:
        """Guardar embedding promedio y retornar el ID."""
        pass
    
    @abstractmethod
    def obtener_embedding(self, persona_titular_fk: int) -> Optional[PersonaEmbedding]:
        """Obtener embedding promedio de una persona."""
        pass


class PuertoSistemaArchivos(ABC):
    """Puerto para gestión del sistema de archivos."""
    
    @abstractmethod
    def guardar_imagen(self, contenido: bytes, ruta: str) -> bool:
        """Guardar imagen en disco y retornar éxito."""
        pass
    
    @abstractmethod
    def obtener_ruta_imagen(self, persona_titular_fk: int, indice: int) -> str:
        """Generar ruta para guardar una imagen."""
        pass

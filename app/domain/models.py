"""Domain models - Entidades de negocio puras sin dependencias externas."""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime
import numpy as np


@dataclass
class Embedding:
    """Modelo para representar un embedding de rostro."""
    vector: np.ndarray
    
    def to_list(self) -> list:
        """Convertir a lista para almacenamiento."""
        return self.vector.tolist()


@dataclass
class PersonaFoto:
    """Modelo para una foto de persona."""
    persona_titular_fk: int
    ruta_imagen: str
    formato: str
    embedding: Embedding
    usuario_creado: str
    foto_pk: Optional[int] = None
    eliminado: bool = False
    motivo_eliminado: Optional[str] = None
    fecha_creado: Optional[datetime] = None
    fecha_actualizado: Optional[datetime] = None
    usuario_actualizado: Optional[str] = None


@dataclass
class PersonaEmbedding:
    """Modelo para el embedding promedio de una persona."""
    persona_titular_fk: int
    embedding: Embedding
    embedding_pk: Optional[int] = None


@dataclass
class VerificacionFacial:
    """Modelo para resultado de verificación facial."""
    coincide: bool
    distancia: float


class ErrorSinRostroDetectado(Exception):
    """Excepción cuando no se detecta un rostro en una imagen."""
    pass


class ErrorVerificacion(Exception):
    """Excepción durante el proceso de verificación."""
    pass

"""Adaptador para sistema de archivos."""

import os
from datetime import datetime
import aiofiles

from app.domain.puertos import PuertoSistemaArchivos


class AdaptadorSistemaArchivosLocal(PuertoSistemaArchivos):
    """Implementación de almacenamiento en sistema de archivos local."""
    
    def __init__(self, directorio_base: str = "uploads"):
        """Inicializar adaptador con directorio base."""
        self.directorio_base = os.path.abspath(directorio_base)
        os.makedirs(self.directorio_base, exist_ok=True)
    
    def guardar_imagen(self, contenido: bytes, ruta: str) -> bool:
        """Guardar imagen en disco."""
        try:
            os.makedirs(os.path.dirname(ruta), exist_ok=True)
            with open(ruta, 'wb') as f:
                f.write(contenido)
            return True
        except Exception as e:
            raise IOError(f"Error guardando imagen: {e}")
    
    async def guardar_imagen_async(self, contenido: bytes, ruta: str) -> bool:
        """Guardar imagen de forma asíncrona."""
        try:
            os.makedirs(os.path.dirname(ruta), exist_ok=True)
            async with aiofiles.open(ruta, 'wb') as f:
                await f.write(contenido)
            return True
        except Exception as e:
            raise IOError(f"Error guardando imagen: {e}")
    
    def obtener_ruta_imagen(self, persona_titular_fk: int, indice: int) -> str:
        """Generar ruta para guardar una imagen."""
        timestamp = datetime.now().timestamp()
        nombre_archivo = f"persona_{persona_titular_fk}_{indice}_{timestamp}.jpg"
        return os.path.join(self.directorio_base, nombre_archivo)

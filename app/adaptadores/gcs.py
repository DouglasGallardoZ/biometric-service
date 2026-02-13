"""Adaptador para almacenamiento en Google Cloud Storage."""

import os
from datetime import datetime, timedelta
from google.cloud import storage
from google.oauth2 import service_account

from app.domain.puertos import PuertoSistemaArchivos


class AdaptadorGoogleCloudStorage(PuertoSistemaArchivos):
    """Implementación de almacenamiento en Google Cloud Storage."""
    
    def __init__(self, bucket_name: str = None, credenciales_path: str = None):
        """Inicializar cliente GCS.
        
        Args:
            bucket_name: Nombre del bucket (si no se proporciona, usa variable de entorno)
            credenciales_path: Ruta a archivo JSON de credenciales (si no se proporciona, usa GOOGLE_APPLICATION_CREDENTIALS)
        """
        self.bucket_name = bucket_name or os.getenv("GCS_BUCKET_NAME")
        
        if not self.bucket_name:
            raise ValueError("GCS_BUCKET_NAME no configurado")
        
        # Credenciales automáticas desde GOOGLE_APPLICATION_CREDENTIALS
        if credenciales_path:
            credenciales = service_account.Credentials.from_service_account_file(
                credenciales_path
            )
            self.client = storage.Client(credentials=credenciales)
        else:
            self.client = storage.Client()
        
        self.bucket = self.client.bucket(self.bucket_name)
    
    def guardar_imagen(self, contenido: bytes, ruta: str) -> bool:
        """Guardar imagen en GCS."""
        try:
            nombre_archivo = os.path.basename(ruta)
            ruta_gcs = f"fotos/{nombre_archivo}"
            
            blob = self.bucket.blob(ruta_gcs)
            blob.upload_from_string(
                contenido,
                content_type='image/jpeg'
            )
            return True
        except Exception as e:
            raise IOError(f"Error guardando en GCS: {e}")
    
    async def guardar_imagen_async(self, contenido: bytes, ruta: str) -> bool:
        """Guardar imagen en GCS de forma asincrónica.
        
        Nota: Para verdaderamente asincrónico, usa aiofiles con GCS
        """
        return self.guardar_imagen(contenido, ruta)
    
    def obtener_ruta_imagen(self, persona_titular_fk: int, indice: int) -> str:
        """Generar ruta para guardar una imagen."""
        timestamp = datetime.now().timestamp()
        nombre_archivo = f"persona_{persona_titular_fk}_{indice}_{timestamp}.jpg"
        return nombre_archivo
    
    def obtener_url_descarga(self, nombre_archivo: str, expiracion_horas: int = 1) -> str:
        """Generar URL de descarga (firma temporal).
        
        Args:
            nombre_archivo: Nombre del archivo en GCS
            expiracion_horas: Horas hasta que expira la URL
        
        Returns:
            URL firmada para descargar el archivo
        """
        try:
            ruta_gcs = f"fotos/{nombre_archivo}"
            blob = self.bucket.blob(ruta_gcs)
            
            url = blob.generate_signed_url(
                version="v4",
                expiration=timedelta(hours=expiracion_horas),
                method="GET"
            )
            return url
        except Exception as e:
            raise IOError(f"Error generando URL: {e}")
    
    def eliminar_imagen(self, nombre_archivo: str) -> bool:
        """Eliminar imagen de GCS."""
        try:
            ruta_gcs = f"fotos/{nombre_archivo}"
            blob = self.bucket.blob(ruta_gcs)
            blob.delete()
            return True
        except Exception as e:
            raise IOError(f"Error eliminando de GCS: {e}")

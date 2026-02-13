"""Adaptador para almacenamiento en AWS S3."""

import os
from datetime import datetime
import boto3
from botocore.exceptions import ClientError

from app.domain.puertos import PuertoSistemaArchivos


class AdaptadorS3(PuertoSistemaArchivos):
    """Implementación de almacenamiento en AWS S3."""
    
    def __init__(self, bucket_name: str = None, region: str = "us-east-1"):
        """Inicializar cliente S3.
        
        Args:
            bucket_name: Nombre del bucket (si no se proporciona, usa variable de entorno)
            region: Región AWS
        """
        self.bucket_name = bucket_name or os.getenv("S3_BUCKET_NAME")
        self.region = region
        
        if not self.bucket_name:
            raise ValueError("S3_BUCKET_NAME no configurado")
        
        # Credenciales desde variables de entorno
        self.access_key = os.getenv("AWS_ACCESS_KEY_ID")
        self.secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        
        # Crear cliente S3
        self.s3_client = boto3.client(
            's3',
            region_name=self.region,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key
        )
    
    def guardar_imagen(self, contenido: bytes, ruta: str) -> bool:
        """Guardar imagen en S3."""
        try:
            # Extraer solo el nombre del archivo (sin ruta local)
            nombre_archivo = os.path.basename(ruta)
            clave_s3 = f"fotos/{nombre_archivo}"
            
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=clave_s3,
                Body=contenido,
                ContentType='image/jpeg'
            )
            return True
        except ClientError as e:
            raise IOError(f"Error guardando en S3: {e}")
    
    async def guardar_imagen_async(self, contenido: bytes, ruta: str) -> bool:
        """Guardar imagen en S3 de forma asincrónica.
        
        Nota: Para verdaderamente asincrónico, usa aioboto3
        """
        return self.guardar_imagen(contenido, ruta)
    
    def obtener_ruta_imagen(self, persona_titular_fk: int, indice: int) -> str:
        """Generar ruta para guardar una imagen.
        
        En S3, retorna la clave que será usada.
        """
        timestamp = datetime.now().timestamp()
        nombre_archivo = f"persona_{persona_titular_fk}_{indice}_{timestamp}.jpg"
        return nombre_archivo
    
    def obtener_url_descarga(self, nombre_archivo: str, expiracion: int = 3600) -> str:
        """Generar URL de descarga (firma temporal).
        
        Args:
            nombre_archivo: Nombre del archivo en S3
            expiracion: Segundos hasta que expira la URL (default 1 hora)
        
        Returns:
            URL firmada para descargar el archivo
        """
        try:
            clave_s3 = f"fotos/{nombre_archivo}"
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': clave_s3},
                ExpiresIn=expiracion
            )
            return url
        except ClientError as e:
            raise IOError(f"Error generando URL: {e}")
    
    def eliminar_imagen(self, nombre_archivo: str) -> bool:
        """Eliminar imagen de S3."""
        try:
            clave_s3 = f"fotos/{nombre_archivo}"
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=clave_s3
            )
            return True
        except ClientError as e:
            raise IOError(f"Error eliminando de S3: {e}")

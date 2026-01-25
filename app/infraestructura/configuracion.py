"""Configuración de inyección de dependencias."""

import os
from app.domain.puertos import (
    PuertoAnalizadorRostros, PuertoAlmacenamientoFotos,
    PuertoAlmacenamientoEmbeddings, PuertoSistemaArchivos
)
from app.adaptadores.analizador_rostros import AdaptadorInsightFaceAnalyzer
from app.adaptadores.postgresql import AdaptadorPostgresEmbeddings, AdaptadorPostgresFotos
from app.adaptadores.sistema_archivos import AdaptadorSistemaArchivosLocal
from app.domain.casos_uso import (
    CasoDeUsoEnrollamiento, CasoDeUsoVerificacion, CasoDeUsoValidacionVisita
)


class ConfiguradorAplicacion:
    """Configurador de la aplicación - inyecta dependencias."""
    
    def __init__(self):
        """Inicializar configuración desde variables de entorno."""
        # Base de datos
        self.db_user = os.getenv("DB_USER", "admin")
        self.db_password = os.getenv("DB_PASSWORD", "password123")
        self.db_host = os.getenv("DB_HOST", "localhost")
        self.db_port = os.getenv("DB_PORT", "5432")
        self.db_name = os.getenv("DB_NAME", "urbanizacion_db")
        self.db_url = f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
        
        # Verificación
        self.umbral_verificacion = float(os.getenv("VERIFICATION_THRESHOLD", "0.6"))
        
        # Archivos
        self.directorio_uploads = os.getenv("UPLOADS_DIR", "uploads")
    
    def crear_analizador_rostros(self) -> PuertoAnalizadorRostros:
        """Crear adaptador de análisis de rostros."""
        return AdaptadorInsightFaceAnalyzer(nombre_modelo="buffalo_s")
    
    def crear_almacen_embeddings(self) -> PuertoAlmacenamientoEmbeddings:
        """Crear adaptador de almacenamiento de embeddings."""
        return AdaptadorPostgresEmbeddings(self.db_url)
    
    def crear_almacen_fotos(self) -> PuertoAlmacenamientoFotos:
        """Crear adaptador de almacenamiento de fotos."""
        return AdaptadorPostgresFotos(self.db_url)
    
    def crear_sistema_archivos(self) -> PuertoSistemaArchivos:
        """Crear adaptador de sistema de archivos."""
        return AdaptadorSistemaArchivosLocal(self.directorio_uploads)
    
    def crear_caso_enrollamiento(self) -> CasoDeUsoEnrollamiento:
        """Crear caso de uso de enrollamiento."""
        return CasoDeUsoEnrollamiento(
            analizador_rostros=self.crear_analizador_rostros(),
            almacen_fotos=self.crear_almacen_fotos(),
            almacen_embeddings=self.crear_almacen_embeddings(),
            sistema_archivos=self.crear_sistema_archivos()
        )
    
    def crear_caso_verificacion(self) -> CasoDeUsoVerificacion:
        """Crear caso de uso de verificación."""
        return CasoDeUsoVerificacion(
            analizador_rostros=self.crear_analizador_rostros(),
            almacen_embeddings=self.crear_almacen_embeddings(),
            umbral_verificacion=self.umbral_verificacion
        )
    
    def crear_caso_validacion_visita(self) -> CasoDeUsoValidacionVisita:
        """Crear caso de uso de validación de visita."""
        return CasoDeUsoValidacionVisita(
            analizador_rostros=self.crear_analizador_rostros(),
            umbral_validacion=self.umbral_verificacion
        )

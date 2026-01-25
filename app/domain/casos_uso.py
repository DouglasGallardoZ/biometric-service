"""Casos de uso - Lógica de negocio de la aplicación."""

from typing import Optional

from app.domain.models import (
    Embedding, PersonaFoto, PersonaEmbedding, VerificacionFacial,
    ErrorSinRostroDetectado, ErrorVerificacion
)
from app.domain.puertos import (
    PuertoAnalizadorRostros, PuertoAlmacenamientoFotos,
    PuertoAlmacenamientoEmbeddings, PuertoSistemaArchivos
)


class CasoDeUsoEnrollamiento:
    """Caso de uso para registrar una nueva persona."""
    
    def __init__(
        self,
        analizador_rostros: PuertoAnalizadorRostros,
        almacen_fotos: PuertoAlmacenamientoFotos,
        almacen_embeddings: PuertoAlmacenamientoEmbeddings,
        sistema_archivos: PuertoSistemaArchivos
    ):
        self.analizador = analizador_rostros
        self.almacen_fotos = almacen_fotos
        self.almacen_embeddings = almacen_embeddings
        self.sistema_archivos = sistema_archivos
    
    def ejecutar(
        self,
        persona_titular_fk: int,
        usuario_creado: str,
        imagenes_bytes: list[bytes]
    ) -> dict:
        """Enrollar una persona con múltiples fotos.
        
        Args:
            persona_titular_fk: ID de la persona
            usuario_creado: Usuario que realiza la acción
            imagenes_bytes: Lista de bytes de imágenes
            
        Returns:
            Diccionario con información del enrollamiento
            
        Raises:
            ErrorSinRostroDetectado: Si no se detecta rostro
            ValueError: Si hay menos de 3 imágenes
        """
        if len(imagenes_bytes) < 3:
            raise ValueError("Se requieren al menos 3 imágenes para enrollar")
        
        embeddings = []
        fotos_guardadas = []
        
        # Procesar cada imagen
        for idx, contenido in enumerate(imagenes_bytes):
            # Obtener embedding
            embedding = self.analizador.obtener_embedding_desde_bytes(contenido)
            embeddings.append(embedding)
            
            # Generar ruta y guardar imagen
            ruta = self.sistema_archivos.obtener_ruta_imagen(persona_titular_fk, idx)
            self.sistema_archivos.guardar_imagen(contenido, ruta)
            
            # Crear modelo de foto
            foto = PersonaFoto(
                persona_titular_fk=persona_titular_fk,
                ruta_imagen=ruta,
                formato=ruta.split('.')[-1],
                embedding=embedding,
                usuario_creado=usuario_creado
            )
            
            # Guardar foto
            foto.foto_pk = self.almacen_fotos.guardar_foto(foto)
            fotos_guardadas.append(foto)
        
        # Calcular embedding promedio
        embedding_promedio = self.analizador.calcular_embedding_promedio(embeddings)
        
        # Guardar embedding promedio
        persona_embedding = PersonaEmbedding(
            persona_titular_fk=persona_titular_fk,
            embedding=embedding_promedio
        )
        persona_embedding.embedding_pk = self.almacen_embeddings.guardar_embedding(persona_embedding)
        
        return {
            "persona_titular_fk": persona_titular_fk,
            "embedding_pk": persona_embedding.embedding_pk,
            "fotos_guardadas": len(fotos_guardadas)
        }


class CasoDeUsoVerificacion:
    """Caso de uso para verificar a una persona."""
    
    def __init__(
        self,
        analizador_rostros: PuertoAnalizadorRostros,
        almacen_embeddings: PuertoAlmacenamientoEmbeddings,
        umbral_verificacion: float = 0.6
    ):
        self.analizador = analizador_rostros
        self.almacen_embeddings = almacen_embeddings
        self.umbral = umbral_verificacion
    
    def ejecutar(
        self,
        persona_titular_fk: int,
        imagen_bytes: bytes
    ) -> VerificacionFacial:
        """Verificar identidad de una persona.
        
        Args:
            persona_titular_fk: ID de la persona a verificar
            imagen_bytes: Bytes de la imagen a verificar
            
        Returns:
            Resultado de verificación
            
        Raises:
            ErrorSinRostroDetectado: Si no se detecta rostro
            ErrorVerificacion: Si no hay embedding de referencia
        """
        # Obtener embedding de la imagen
        embedding_verificacion = self.analizador.obtener_embedding_desde_bytes(imagen_bytes)
        
        # Obtener embedding de referencia
        persona_embedding = self.almacen_embeddings.obtener_embedding(persona_titular_fk)
        if not persona_embedding:
            raise ErrorVerificacion(f"No hay embedding de referencia para persona {persona_titular_fk}")
        
        # Calcular distancia
        distancia = self.analizador.calcular_distancia_coseno(
            embedding_verificacion,
            persona_embedding.embedding
        )
        
        # Determinar coincidencia
        coincide = distancia <= self.umbral
        
        return VerificacionFacial(
            coincide=coincide,
            distancia=distancia
        )


class CasoDeUsoValidacionVisita:
    """Caso de uso para validar una visita comparando dos fotos."""
    
    def __init__(
        self,
        analizador_rostros: PuertoAnalizadorRostros,
        umbral_validacion: float = 0.6
    ):
        self.analizador = analizador_rostros
        self.umbral = umbral_validacion
    
    def ejecutar(
        self,
        foto_cedula_bytes: bytes,
        foto_rostro_vivo_bytes: bytes
    ) -> VerificacionFacial:
        """Validar que el rostro vivo coincide con la cédula.
        
        Args:
            foto_cedula_bytes: Bytes de la foto de cédula
            foto_rostro_vivo_bytes: Bytes de la foto de rostro vivo
            
        Returns:
            Resultado de validación
            
        Raises:
            ErrorSinRostroDetectado: Si no se detecta rostro
        """
        # Obtener embeddings
        embedding1 = self.analizador.obtener_embedding_desde_bytes(foto_cedula_bytes)
        embedding2 = self.analizador.obtener_embedding_desde_bytes(foto_rostro_vivo_bytes)
        
        # Calcular distancia
        distancia = self.analizador.calcular_distancia_coseno(embedding1, embedding2)
        
        # Determinar coincidencia
        coincide = distancia <= self.umbral
        
        return VerificacionFacial(
            coincide=coincide,
            distancia=distancia
        )

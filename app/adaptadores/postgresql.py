"""Adaptador para almacenamiento usando SQLAlchemy."""

from typing import Optional
import numpy as np
from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.exc import SQLAlchemyError
from pgvector.sqlalchemy import Vector

from app.domain.models import Embedding, PersonaFoto, PersonaEmbedding
from app.domain.puertos import PuertoAlmacenamientoFotos, PuertoAlmacenamientoEmbeddings


class AdaptadorPostgresEmbeddings(PuertoAlmacenamientoEmbeddings):
    """Implementación de almacenamiento de embeddings en PostgreSQL."""
    
    def __init__(self, url_base_datos: str):
        """Inicializar conexión a PostgreSQL."""
        self.motor = create_engine(url_base_datos, future=True)
        self.metadatos = MetaData()
        
        # Tabla persona_embedding
        self.tabla_persona_embedding = Table(
            "persona_embedding",
            self.metadatos,
            Column("embedding_pk", Integer, primary_key=True, autoincrement=True),
            Column("persona_titular_fk", Integer, nullable=False),
            Column("rostro_embedding", Vector(512), nullable=True),
        )
        
        self._inicializar_bd()
    
    def _inicializar_bd(self):
        """Crear tablas y extensiones si no existen."""
        with self.motor.begin() as conexion:
            try:
                conexion.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            except SQLAlchemyError:
                pass
            self.metadatos.create_all(bind=conexion)
    
    def guardar_embedding(self, persona_embedding: PersonaEmbedding) -> int:
        """Guardar embedding promedio y retornar el ID."""
        with self.motor.begin() as conexion:
            sql = text(
                "INSERT INTO persona_embedding (persona_titular_fk, rostro_embedding) "
                "VALUES (:persona_fk, :vec) RETURNING embedding_pk"
            )
            resultado = conexion.execute(sql, {
                "persona_fk": persona_embedding.persona_titular_fk,
                "vec": persona_embedding.embedding.to_list()
            }).fetchone()
            return resultado[0] if resultado else None
    
    def obtener_embedding(self, persona_titular_fk: int) -> Optional[PersonaEmbedding]:
        """Obtener embedding promedio de una persona."""
        with self.motor.connect() as conexion:
            sql = text(
                "SELECT embedding_pk, persona_titular_fk, rostro_embedding "
                "FROM persona_embedding WHERE persona_titular_fk = :persona_fk "
                "ORDER BY embedding_pk DESC LIMIT 1"
            )
            resultado = conexion.execute(sql, {"persona_fk": persona_titular_fk}).fetchone()
            
            if not resultado:
                return None
            
            embedding_pk, persona_fk, vec = resultado
            return PersonaEmbedding(
                embedding_pk=embedding_pk,
                persona_titular_fk=persona_fk,
                embedding=Embedding(vector=np.array(vec, dtype=np.float32))
            )


class AdaptadorPostgresFotos(PuertoAlmacenamientoFotos):
    """Implementación de almacenamiento de fotos en PostgreSQL."""
    
    def __init__(self, url_base_datos: str):
        """Inicializar conexión a PostgreSQL."""
        self.motor = create_engine(url_base_datos, future=True)
        self.metadatos = MetaData()
        
        # Tabla persona_foto
        self.tabla_persona_foto = Table(
            "persona_foto",
            self.metadatos,
            Column("foto_pk", Integer, primary_key=True, autoincrement=True),
            Column("persona_titular_fk", Integer, nullable=False),
            Column("ruta_imagen", Text, nullable=False),
            Column("formato", String(10), nullable=False),
            Column("eliminado", Boolean, nullable=False, default=False),
            Column("motivo_eliminado", Text, nullable=True),
            Column("fecha_creado", DateTime, nullable=True),
            Column("usuario_creado", String(20), nullable=False),
            Column("fecha_actualizado", DateTime, nullable=True),
            Column("usuario_actualizado", String(20), nullable=True),
            Column("rostro_embedding", Vector(512), nullable=True),
        )
        
        self._inicializar_bd()
    
    def _inicializar_bd(self):
        """Crear tablas y extensiones si no existen."""
        with self.motor.begin() as conexion:
            self.metadatos.create_all(bind=conexion)
    
    def guardar_foto(self, foto: PersonaFoto) -> int:
        """Guardar foto y retornar el ID."""
        with self.motor.begin() as conexion:
            sql = text(
                "INSERT INTO persona_foto "
                "(persona_titular_fk, ruta_imagen, formato, rostro_embedding, usuario_creado, eliminado) "
                "VALUES (:persona_fk, :ruta, :fmt, :vec, :usuario, :eliminado) "
                "RETURNING foto_pk"
            )
            resultado = conexion.execute(sql, {
                "persona_fk": foto.persona_titular_fk,
                "ruta": foto.ruta_imagen,
                "fmt": foto.formato,
                "vec": foto.embedding.to_list(),
                "usuario": foto.usuario_creado,
                "eliminado": foto.eliminado
            }).fetchone()
            return resultado[0] if resultado else None
    
    def obtener_foto(self, foto_pk: int) -> Optional[PersonaFoto]:
        """Obtener foto por ID."""
        with self.motor.connect() as conexion:
            sql = text(
                "SELECT foto_pk, persona_titular_fk, ruta_imagen, formato, "
                "eliminado, motivo_eliminado, fecha_creado, usuario_creado, "
                "fecha_actualizado, usuario_actualizado, rostro_embedding "
                "FROM persona_foto WHERE foto_pk = :foto_pk"
            )
            resultado = conexion.execute(sql, {"foto_pk": foto_pk}).fetchone()
            
            if not resultado:
                return None
            
            (foto_pk, persona_fk, ruta, fmt, eliminado, motivo, fecha_creado,
             usuario_creado, fecha_act, usuario_act, vec) = resultado
            
            return PersonaFoto(
                foto_pk=foto_pk,
                persona_titular_fk=persona_fk,
                ruta_imagen=ruta,
                formato=fmt,
                eliminado=eliminado,
                motivo_eliminado=motivo,
                fecha_creado=fecha_creado,
                usuario_creado=usuario_creado,
                fecha_actualizado=fecha_act,
                usuario_actualizado=usuario_act,
                embedding=Embedding(vector=np.array(vec, dtype=np.float32))
            )
    
    def obtener_fotos_persona(self, persona_titular_fk: int) -> list[PersonaFoto]:
        """Obtener todas las fotos no eliminadas de una persona."""
        with self.motor.connect() as conexion:
            sql = text(
                "SELECT foto_pk, persona_titular_fk, ruta_imagen, formato, "
                "eliminado, motivo_eliminado, fecha_creado, usuario_creado, "
                "fecha_actualizado, usuario_actualizado, rostro_embedding "
                "FROM persona_foto WHERE persona_titular_fk = :persona_fk AND eliminado = false "
                "ORDER BY fecha_creado DESC"
            )
            resultados = conexion.execute(sql, {"persona_fk": persona_titular_fk}).fetchall()
            
            fotos = []
            for (foto_pk, persona_fk, ruta, fmt, eliminado, motivo, fecha_creado,
                 usuario_creado, fecha_act, usuario_act, vec) in resultados:
                foto = PersonaFoto(
                    foto_pk=foto_pk,
                    persona_titular_fk=persona_fk,
                    ruta_imagen=ruta,
                    formato=fmt,
                    eliminado=eliminado,
                    motivo_eliminado=motivo,
                    fecha_creado=fecha_creado,
                    usuario_creado=usuario_creado,
                    fecha_actualizado=fecha_act,
                    usuario_actualizado=usuario_act,
                    embedding=Embedding(vector=np.array(vec, dtype=np.float32))
                )
                fotos.append(foto)
            
            return fotos

import os
from typing import Optional, Tuple
from datetime import datetime

import numpy as np
from sqlalchemy import (Column, Integer, MetaData, String, Table, create_engine, text, Boolean, DateTime, Text)
from sqlalchemy.exc import SQLAlchemyError
from pgvector.sqlalchemy import Vector


class DataBase:
    def __init__(self, url_base_datos: str):
        self.url_base_datos = url_base_datos
        self.motor = create_engine(self.url_base_datos, future=True)
        self.metadatos = MetaData()

        # Tabla: persona_embedding(embedding_pk, persona_titular_fk, rostro_embedding)
        self.persona_embedding = Table(
            "persona_embedding",
            self.metadatos,
            Column("embedding_pk", Integer, primary_key=True, autoincrement=True),
            Column("persona_titular_fk", Integer, nullable=False),
            Column("rostro_embedding", Vector(512), nullable=True),
        )

        # Tabla: persona_foto(foto_pk, persona_titular_fk, ruta_imagen, formato, eliminado, etc)
        self.persona_foto = Table(
            "persona_foto",
            self.metadatos,
            Column("foto_pk", Integer, primary_key=True, autoincrement=True),
            Column("persona_titular_fk", Integer, nullable=False),
            Column("ruta_imagen", Text, nullable=False),
            Column("formato", String(10), nullable=False),
            Column("eliminado", Boolean, nullable=False, default=False),
            Column("motivo_eliminado", Text, nullable=True),
            Column("fecha_creado", DateTime, nullable=True, default=datetime.utcnow),
            Column("usuario_creado", String(20), nullable=False),
            Column("fecha_actualizado", DateTime, nullable=True),
            Column("usuario_actualizado", String(20), nullable=True),
        )

    def inicializar_bd(self):
        # Crear extensión si no existe y crear tablas
        with self.motor.begin() as conexion:
            try:
                # Extensión pgvector para vectores
                conexion.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            except SQLAlchemyError:
                # Si el usuario de BD carece de privilegios, aún así intentar crear tablas
                pass

            self.metadatos.create_all(bind=conexion)

    def insertar_o_actualizar_residente(self, persona_titular_fk: int, rostro_embedding: list):
        # Insertar nuevo embedding o actualizar si existe
        with self.motor.begin() as conexion:
            sql = text(
                "INSERT INTO persona_embedding (persona_titular_fk, rostro_embedding) VALUES (:persona_fk, :vec)"
            )
            conexion.execute(sql, {"persona_fk": persona_titular_fk, "vec": rostro_embedding})

    def obtener_incrustacion_residente(self, persona_titular_fk: int) -> Optional[np.ndarray]:
        with self.motor.connect() as conexion:
            sql = text("SELECT rostro_embedding FROM persona_embedding WHERE persona_titular_fk = :persona_fk ORDER BY embedding_pk DESC LIMIT 1")
            resultado = conexion.execute(sql, {"persona_fk": persona_titular_fk}).fetchone()
            if resultado is None:
                return None
            # SQLAlchemy retorna una lista/tupla conteniendo una lista de Python para rostro_embedding
            vec = resultado[0]
            return vec
            # return np.asarray(vec, dtype=np.float32)

    def insertar_foto_residente(self, persona_titular_fk: int, ruta_imagen: str, formato: str, usuario_creado: str):
        # Insertar foto en persona_foto
        with self.motor.begin() as conexion:
            sql = text(
                "INSERT INTO persona_foto (persona_titular_fk, ruta_imagen, formato, usuario_creado, eliminado) "
                "VALUES (:persona_fk, :ruta, :fmt, :usuario, :eliminado)"
            )
            conexion.execute(sql, {
                "persona_fk": persona_titular_fk,
                "ruta": ruta_imagen,
                "fmt": formato,
                "usuario": usuario_creado,
                "eliminado": False
            })

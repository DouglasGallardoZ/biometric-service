import os
from typing import Optional, Tuple

import numpy as np
from sqlalchemy import (Column, Integer, MetaData, String, Table, create_engine, text)
from sqlalchemy.exc import SQLAlchemyError
from pgvector.sqlalchemy import Vector


class DataBase:
    def __init__(self, url_base_datos: str):
        self.url_base_datos = url_base_datos
        self.motor = create_engine(self.url_base_datos, future=True)
        self.metadatos = MetaData()

        # Tabla: residentes(id unique, rostro_embedding vector(512))
        self.residentes = Table(
            "residentes",
            self.metadatos,
            Column("id", Integer, primary_key=True, autoincrement=True),
            # Column("id", String, unique=True, nullable=False),
            Column("rostro_embedding", Vector(512), nullable=False),
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

    def insertar_o_actualizar_residente(self, id: str, rostro_embedding: list):
        # Insertar o actualizar
        with self.motor.begin() as conexion:
            sql = text(
                "INSERT INTO residentes (id, rostro_embedding) VALUES (:id, :vec)"
                " ON CONFLICT (id) DO UPDATE SET rostro_embedding = EXCLUDED.rostro_embedding"
            )
            conexion.execute(sql, {"id": id, "vec": rostro_embedding})

    def obtener_incrustacion_residente(self, id: str) -> Optional[np.ndarray]:
        with self.motor.connect() as conexion:
            sql = text("SELECT rostro_embedding FROM residentes WHERE id = :id")
            resultado = conexion.execute(sql, {"id": id}).fetchone()
            if resultado is None:
                return None
            # SQLAlchemy retorna una lista/tupla conteniendo una lista de Python para rostro_embedding
            vec = resultado[0]
            return vec
            # return np.asarray(vec, dtype=np.float32)

    

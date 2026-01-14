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

        # table: residentes(id unique, rostro_embedding rostro_embedding(512))
        self.residentes = Table(
            "residentes",
            self.metadatos,
            Column("id", Integer, primary_key=True, autoincrement=True),
            # Column("id", String, unique=True, nullable=False),
            Column("rostro_embedding", Vector(512), nullable=False),
        )

    def inicializar_bd(self):
        # Create extension if not exists and create tables
        with self.motor.begin() as conexion:
            try:
                # pgvector extension is named 'rostro_embedding'
                conexion.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            except SQLAlchemyError:
                # If the database user lacks privileges, still try to create tables.
                pass

            self.metadatos.create_all(bind=conexion)

    def insertar_o_actualizar_residente(self, id: str, rostro_embedding: list):
        # insert or update
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
            # SQLAlchemy returns a list/tuple containing a Python list for the rostro_embedding
            vec = resultado[0]
            return vec
            # return np.asarray(vec, dtype=np.float32)

    def verificar_usuario(self, id: str, rostro_embedding: list, umbral: float) -> Optional[Tuple[float, bool]]:
        """Compare candidate rostro_embedding against stored rostro_embedding for user using cosine distance in DB.

        This uses pgvector's cosine distance operator `<#>` which returns a float where 0 means identical.
        """
        with self.motor.connect() as conexion:
            sql = text("SELECT (rostro_embedding <#> :vec) AS distance FROM residentes WHERE id = :id LIMIT 1")
            resultado = conexion.execute(sql, {"vec": str(rostro_embedding), "id": id}).fetchone()
            if resultado is None:
                return None
            distancia = float(resultado[0])
            coincide = distancia <= umbral
            return distancia, coincide

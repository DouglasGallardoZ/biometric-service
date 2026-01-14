import os
from typing import Optional, Tuple

import numpy as np
from sqlalchemy import (Column, Integer, MetaData, String, Table, create_engine, text)
from sqlalchemy.exc import SQLAlchemyError
from pgvector.sqlalchemy import Vector


class Database:
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.engine = create_engine(self.database_url, future=True)
        self.metadata = MetaData()

        # table: residentes(id unique, rostro_embedding rostro_embedding(512))
        self.residentes = Table(
            "residentes",
            self.metadata,
            Column("id", Integer, primary_key=True, autoincrement=True),
            # Column("id", String, unique=True, nullable=False),
            Column("rostro_embedding", Vector(512), nullable=False),
        )

    def init_db(self):
        # Create extension if not exists and create tables
        with self.engine.begin() as conn:
            try:
                # pgvector extension is named 'rostro_embedding'
                conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            except SQLAlchemyError:
                # If the database user lacks privileges, still try to create tables.
                pass

            self.metadata.create_all(bind=conn)

    def upsert_resident(self, id: str, rostro_embedding: list):
        # insert or update
        with self.engine.begin() as conn:
            sql = text(
                "INSERT INTO residentes (id, rostro_embedding) VALUES (:id, :vec)"
                " ON CONFLICT (id) DO UPDATE SET rostro_embedding = EXCLUDED.rostro_embedding"
            )
            conn.execute(sql, {"id": id, "vec": rostro_embedding})

    def get_resident_embedding(self, id: str) -> Optional[np.ndarray]:
        with self.engine.connect() as conn:
            sql = text("SELECT rostro_embedding FROM residentes WHERE id = :id")
            res = conn.execute(sql, {"id": id}).fetchone()
            if res is None:
                return None
            # SQLAlchemy returns a list/tuple containing a Python list for the rostro_embedding
            vec = res[0]
            return vec
            # return np.asarray(vec, dtype=np.float32)

    def verify_user(self, id: str, rostro_embedding: list, threshold: float) -> Optional[Tuple[float, bool]]:
        """Compare candidate rostro_embedding against stored rostro_embedding for user using cosine distance in DB.

        This uses pgvector's cosine distance operator `<#>` which returns a float where 0 means identical.
        """
        with self.engine.connect() as conn:
            sql = text("SELECT (rostro_embedding <#> :vec) AS distance FROM residentes WHERE id = :id LIMIT 1")
            res = conn.execute(sql, {"vec": str(rostro_embedding), "id": id}).fetchone()
            if res is None:
                return None
            distance = float(res[0])
            match = distance <= threshold
            return distance, match

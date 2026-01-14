-- Habilitar la extensión de vectores
-- CREATE EXTENSION IF NOT EXISTS vector;

-- Tabla para residentes
-- CREATE TABLE residentes (
--     id VARCHAR(50) PRIMARY KEY,
--     nombre TEXT,
--     rostro_embedding vector(512), -- 512 es la dimensión de InsightFace Buffalo_L/S
--     fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );
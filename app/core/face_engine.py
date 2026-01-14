from typing import List

import numpy as np

from insightface.app import FaceAnalysis


class NoFaceDetectedError(Exception):
    pass


class FaceEngine:
    def __init__(self, model_name: str = "buffalo_s"):
        """Initialize FaceAnalysis using ONNX CPUExecutionProvider.

        Note: Ensure that `onnxruntime` is installed and that `CPUExecutionProvider` is available.
        """
        # Use CPU execution provider and CPU context id (-1)
        try:
            self.app = FaceAnalysis(name=model_name, providers=["CPUExecutionProvider"])
            # ctx_id=-1 forces CPU
            self.app.prepare(ctx_id=-1)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize FaceAnalysis: {e}")

    def get_embedding(self, img: np.ndarray) -> np.ndarray:
        """Return a normalized embedding for the largest detected face.

        Raises NoFaceDetectedError if no face is found.
        """
        faces = self.app.get(img)
        if not faces:
            raise NoFaceDetectedError("No face detected in the provided image")

        # pick largest face (usually first) and get .embedding
        face = faces[0]
        emb = np.asarray(face.embedding, dtype=np.float32)
        # normalize
        norm = np.linalg.norm(emb)
        if norm == 0:
            raise NoFaceDetectedError("Invalid embedding (zero norm)")
        return emb / norm

    def mean_embedding(self, embeddings: List[np.ndarray]) -> np.ndarray:
        """Compute mean embedding and normalize it."""
        m = np.mean(np.stack(embeddings, axis=0), axis=0)
        norm = np.linalg.norm(m)
        if norm == 0:
            raise ValueError("Mean embedding has zero norm")
        return m / norm

    def cosine_distance(self, a: np.ndarray, b: np.ndarray) -> float:
        """Return cosine distance (1 - cosine_similarity)."""
        a = np.asarray(a, dtype=np.float32)
        b = np.asarray(b, dtype=np.float32)
        dot = float(np.dot(a, b))
        na = np.linalg.norm(a)
        nb = np.linalg.norm(b)
        if na == 0 or nb == 0:
            return 1.0
        cos_sim = dot / (na * nb)
        # cosine distance
        return 1.0 - cos_sim

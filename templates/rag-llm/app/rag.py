import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class LocalVectorStore:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.encoder = SentenceTransformer(model_name)
        self.dimension = self.encoder.get_sentence_embedding_dimension()
        self.index = faiss.IndexFlatIP(self.dimension)
        self.chunks = []

    def add_texts(self, texts: list[str]):
        embeddings = self.encoder.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
        self.index.add(embeddings.astype(np.float32))
        self.chunks.extend(texts)

    def search(self, query: str, top_k=3) -> list[str]:
        q_vec = self.encoder.encode([query], convert_to_numpy=True, normalize_embeddings=True)
        _, indices = self.index.search(q_vec.astype(np.float32), top_k)
        return [self.chunks[i] for i in indices[0] if i < len(self.chunks)]

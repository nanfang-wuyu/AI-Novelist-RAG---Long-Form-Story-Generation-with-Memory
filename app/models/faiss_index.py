import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# FAISS索引初始化
class FaissIndex:
    def __init__(self, encoder, index_path: str = 'data/memory_store.faiss'):
        self.encoder = encoder
        if not encoder:
            self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        self.dimension = self.encoder.get_sentence_embedding_dimension()
        print(f"FAISS dimension: {self.dimension}")
        self.index_path = index_path

        try:
            self.index = faiss.read_index(self.index_path) 
            print("Reading dindex with dimension", self.index.d)
        except:
            self.index = faiss.IndexFlatL2(self.dimension)
            print("Creating dindex with dimension", self.index.d)
        
    def add(self, embeddings: np.ndarray, metainfo: list):
        """Add embeddings to the index"""
        faiss.normalize_L2(embeddings)  
        print(self.index.d, embeddings.shape[1]) 
        self.index.add(embeddings)  
        self.metainfo = metainfo
        self.store()
        
    def search(self, query_embedding: np.ndarray, top_k: int = 3):
        """Search for the top_k nearest neighbors"""
        faiss.normalize_L2(query_embedding)
        distances, indices = self.index.search(query_embedding, top_k)
        return distances, indices
    
    def store(self):
        """Store the index to disk"""
        faiss.write_index(self.index, self.index_path)

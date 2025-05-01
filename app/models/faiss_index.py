import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import os
from typing import Optional


class FaissIndex:
        
    def __init__(self, 
                 encoder=None, 
                 index_path: str = 'data/memory_store.faiss', 
                 metainfo_path: str = 'data/metainfo.npy'):
        self.encoder = encoder or SentenceTransformer('all-MiniLM-L6-v2')
        self.dimension = self.encoder.get_sentence_embedding_dimension()
        print(f"FAISS dimension: {self.dimension}")
        
        self.index_path = index_path
        self.metainfo_path = metainfo_path
        self.index = None
        self.metainfo = None

        if os.path.exists(self.index_path):
            self.load_vectorstore()
        else:
            self.new_vectorstore()
        
        if os.path.exists(self.metainfo_path):
            self.load_metainfo()
        else:
            self.new_metainfo()

    def add(self, texts: list, extract_info_list: Optional[list] = None):
        """Add texts to the index"""
        embeddings = self.encoder.encode(texts, normalize_embeddings=True)
        embeddings = np.array(embeddings).astype('float32')

        start_id = len(self.metainfo)
        ids = list(range(start_id, start_id + len(texts)))

        faiss.normalize_L2(embeddings)  

        self.index.add(embeddings)

        if extract_info_list:
            for i, text, extract_info in zip(ids, texts, extract_info_list):
                self.metainfo[i] = (text, extract_info)
        else:
            for i, text in zip(ids, texts):
                self.metainfo[i] = text

        self.store()

    
    def search(self, query: str, top_k: int = 5):
        """Search for the top_k nearest neighbors"""
        query_embedding = self.encoder.encode([query], normalize_embeddings=True)
        query_embedding = np.array(query_embedding).astype('float32')
        faiss.normalize_L2(query_embedding)

        distances, indices = self.index.search(query_embedding, top_k)

        results = []
        for idx in indices[0]:
            if idx in self.metainfo:
                results.append(self.metainfo[idx])
        return results

    def new_vectorstore(self):
        self.index = faiss.IndexFlatL2(self.dimension)
        print("Creating new FAISS index with dimension", self.index.d)
    
    def store_vectorstore(self):
        faiss.write_index(self.index, self.index_path)
        print("Storing FAISS index to disk.")

    def load_vectorstore(self):
        self.index = faiss.read_index(self.index_path)
        print("Loaded existing FAISS index.")

    def new_metainfo(self):
        self.metainfo = {}
        print("Creating new metainfo. ")

    def store_metainfo(self):
        np.save(self.metainfo_path, self.metainfo)
        print("Storing metainfo to disk.")

    def load_metainfo(self):
        self.metainfo = np.load(self.metainfo_path, allow_pickle=True).item()
        print("Loaded existing metainfo.")

    def reset(self):
        """Clear the index and metainfo"""
        if os.path.exists(self.index_path):
            os.remove(self.index_path)
        if os.path.exists(self.metainfo_path):
            os.remove(self.metainfo_path)
        self.new()
        self.store()
        print("Reset FAISS index and metainfo.")

    def new(self):
        self.new_vectorstore()
        self.new_metainfo()

    def store(self):
        self.store_vectorstore()
        self.store_metainfo()
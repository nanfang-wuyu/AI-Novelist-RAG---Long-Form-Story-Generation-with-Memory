import numpy as np
from app.models.faiss_index import FaissIndex
from sentence_transformers import SentenceTransformer
from app.apis.extractor import extract_info
import atexit
import faiss

def save_index_on_exit(faiss_index: FaissIndex):
    faiss.write_index(faiss_index.index, faiss_index.index_path)

faiss_index = FaissIndex(SentenceTransformer('all-MiniLM-L6-v2'), index_path='data/memory_store.faiss')
atexit.register(save_index_on_exit, faiss_index)



def insert_to_memory(text: str):

    """Insert a new memory into the FAISS index"""

    extracted_information = extract_info(text)
    embedding = faiss_index.encoder.encode([extracted_information]) 
    faiss_index.add(np.array(embedding), [text]) 

    return "Memory Inserted!"

def search_memory(query: str, top_k: int = 3):

    """Search for the most relevant memory based on the query"""

    query_embedding = faiss_index.encoder.encode([query])
    distances, indices = faiss_index.search(np.array(query_embedding), top_k)
    results = [faiss_index.metainfo[idx] for idx in indices[0]]
    
    return results

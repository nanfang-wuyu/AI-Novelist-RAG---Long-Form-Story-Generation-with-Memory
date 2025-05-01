import numpy as np
from app.models.faiss_index import FaissIndex
from sentence_transformers import SentenceTransformer
from app.apis.extractor import extract_info
import atexit
import faiss

def save_index_on_exit(faiss_index: FaissIndex):
    faiss_index.store()

faiss_index = FaissIndex()
atexit.register(save_index_on_exit, faiss_index)

def split_into_paragraphs(doc):
    return doc.split("\n\n")

def insert_chapter_to_memory(texts: str, split: bool = True):

    # extracted_information = extract_info(text)

    if split:
        texts = split_into_paragraphs(texts)
    
    
    faiss_index.add(texts=texts, extract_info_list=None) 
    faiss_index

    return "Memory Inserted!"

def search_memory(query: str, top_k: int = 3):

    return faiss_index.search(query, top_k=top_k)

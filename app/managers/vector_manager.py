import os
import faiss
from typing import List, Optional
from langchain_community.vectorstores import FAISS
# from langchain.docstore import InMemoryDocstore
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain.schema import Document
from app.models.model import Embedding_model

BASE_PATH = "data/vectorstore"

VECTORSTORE_TYPES = {
    "chapter": "chapter_index",
    "summary": "summary_index"
}


def create_new_vectorstore(embedding_model):
    dim = len(embedding_model.embed_query("hello world"))
    index = faiss.IndexFlatL2(dim)
    return FAISS(
        embedding_function=embedding_model,
        index=index,
        docstore=InMemoryDocstore(),
        index_to_docstore_id={}
    )


def load_vectorstore(store_type: str) -> FAISS:
    assert store_type in VECTORSTORE_TYPES, "Invalid vectorstore type."
    path = os.path.join(BASE_PATH, VECTORSTORE_TYPES[store_type])

    if os.path.exists(os.path.join(path, 'index.faiss')):
        print("Reload existing faiss")
        return FAISS.load_local(path, Embedding_model, allow_dangerous_deserialization=True)
    else:
        print("Create new faiss")
        vs = create_new_vectorstore(Embedding_model)
        save_vectorstore(vs, store_type)
        return vs


def save_vectorstore(vectorstore: FAISS, store_type: str):
    path = os.path.join(BASE_PATH, VECTORSTORE_TYPES[store_type])
    vectorstore.save_local(path)


def add_document(store_type: str, content: str, metadata: dict):
    assert store_type == metadata.get("type")
    vs = load_vectorstore(store_type)
    doc = Document(page_content=content, metadata=metadata)
    vs.add_documents([doc])
    save_vectorstore(vs, store_type)


def update_document(store_type: str, chapter_num: str, new_content: str):
    print(f"Updating chapter {chapter_num} in store: {store_type}")
    
    vs = load_vectorstore(store_type)

    target_doc_ids = [
        doc_id for doc_id, doc in vs.docstore._dict.items()
        if doc.metadata.get("chapter") == chapter_num
    ]
    
    if not target_doc_ids:
        raise ValueError(f"No document found for chapter: {chapter_num}")

    for doc_id in target_doc_ids:
        vs.delete([doc_id])

    new_doc = Document(
        page_content=new_content,
        metadata={"type": store_type, "chapter": chapter_num}
    )
    vs.add_documents([new_doc])

    save_vectorstore(vs, store_type)

    print(f"Chapter {chapter_num} successfully updated.")



def get_relevant_documents(store_type: str, query: str, top_k: int = 10) -> List[Document]:
    vs = load_vectorstore(store_type)
    return vs.similarity_search(query, k=top_k)

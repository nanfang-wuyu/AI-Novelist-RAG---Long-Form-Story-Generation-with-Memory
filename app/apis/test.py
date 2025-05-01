from fastapi import APIRouter
from app.utils.memory import insert_chapter_to_memory, search_memory, faiss_index
import os

router = APIRouter()

@router.post("/test_memory")
def test_memory_endpoint():

    with open("data/samples/raws/generated_20250427_023257.txt", "r", encoding="utf-8") as f:
        chapter_demo = f.read()
    example_generated_text = chapter_demo

    insert_chapter_to_memory(example_generated_text)

    query = "Kevin is a magician"
    results = search_memory(query)

    return {"query": query, "results": results}

@router.post("/clear_memory")
def clear_memory():
    faiss_index.reset()
    return {"message": "FAISS memory cleared."}
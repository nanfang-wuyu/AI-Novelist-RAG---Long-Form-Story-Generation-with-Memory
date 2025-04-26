from fastapi import APIRouter
from app.apis.memory import insert_to_memory, search_memory

router = APIRouter()

@router.post("/test_memory")
def test_memory_endpoint():

    example_generated_text = "The hero, John, walked into the dark cave. He was frightened, but determined."

    insert_to_memory(example_generated_text)

    query = "hero in cave"
    results = search_memory(query)

    return {"query": query, "results": results}

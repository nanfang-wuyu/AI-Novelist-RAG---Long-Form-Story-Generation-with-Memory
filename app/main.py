from fastapi import FastAPI
from app.apis import generator, test

app = FastAPI(title="AI Novelist RAG")

app.include_router(generator.router)
app.include_router(test.router)


@app.get("/")
def read_root():
    return {"message": "AI Novelist RAG service is running."}
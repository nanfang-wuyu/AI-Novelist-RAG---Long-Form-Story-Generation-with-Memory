from fastapi import FastAPI
from app.apis import generator, test, extractor

app = FastAPI(title="AI Novelist RAG")

app.include_router(generator.router)
app.include_router(test.router)
app.include_router(extractor.router)


@app.get("/")
def read_root():
    return {"message": "AI Novelist RAG service is running."}
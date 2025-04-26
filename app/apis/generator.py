from fastapi import APIRouter
from pydantic import BaseModel
from app.models.qwenint4 import LocalQwenModel
from app.models.tinyllama import TinyLlamaModel
import subprocess
import json
from ollama import generate

router = APIRouter()

# model = LocalQwenModel("Qwen/Qwen1.5-7B-Chat-GPTQ-Int4")  
model = TinyLlamaModel()


class GenerateRequest(BaseModel):
    prompt: str
    max_new_tokens: int = 2048
    temperature: float = 0.7
    top_k: int = 50
    top_p: float = 0.95


@router.post("/generate")
def generate_text(request: GenerateRequest):
    try:
        result = model.generate(request.prompt, request.max_new_tokens, request.temperature, request.top_k, request.top_p)
        return {"output": result}
    except Exception as e:
        print(f"Error during generation: {e}")
        return {"error": str(e)}
    

@router.post("/generate_ollama")
def generate_text_by_ollama(request: GenerateRequest):
    result = subprocess.run(
        ["ollama", "run", "--model", "llama3.2:1b-instruct-fp16", request.prompt],
        capture_output=True, text=True
    )
    output = result.stdout
    return {"output": output}


# def generate_with_memory(prompt):
#     generated = model.generate(prompt)
#     extracted = extract_keywords(generated)
#     insert_to_memory(extracted, source=generated)
#     return generated

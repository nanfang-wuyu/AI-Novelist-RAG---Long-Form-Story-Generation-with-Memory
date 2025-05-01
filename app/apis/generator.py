from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
from app.models.model import model
import subprocess
import json
from ollama import generate
import os

router = APIRouter()


class GenerateRequest(BaseModel):
    prompt: str
    role: str = None
    max_new_tokens: int = 2048
    temperature: float = 0.7
    top_k: int = 50
    top_p: float = 0.95


@router.post("/generate")
def generate_text(request: GenerateRequest):
    try:
        result = model.generate(request.prompt, request.role, request.max_new_tokens, request.temperature, request.top_k, request.top_p)
        return {"output": result}
    except Exception as e:
        print(f"Error during generation: {e}")
        return {"error": str(e)}
    

# @router.post("/generate_ollama")
# def generate_text_by_ollama(request: GenerateRequest):
#     result = subprocess.run(
#         ["ollama", "run", "--model", "llama3.2:1b-instruct-fp16", request.prompt],
#         capture_output=True, text=True
#     )
#     output = result.stdout
#     return {"output": output}

@router.post("/generate_and_save")
def generate_and_save(request: GenerateRequest):
    # try:
        
        
        result = model.generate(request.prompt, request.role, request.max_new_tokens, request.temperature, request.top_k, request.top_p)
        # result = "Prompt: \n" + request.prompt + "\nResponse: \n" + result
        save_dir = "data/samples/raws"
        os.makedirs(save_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"generated_{timestamp}"
        filepath = os.path.join(save_dir, filename) + ".txt"

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(result)

        summary = model.summarize(result, filename=filename)

        return {"output": result, "saved_path": filepath, "summary": summary}
    # except Exception as e:
    #     print(f"Error during generation: {e}")
    #     return {"error": str(e)}

# def generate_with_memory(prompt):
#     generated = model.generate(prompt)
#     extracted = extract_keywords(generated)
#     insert_to_memory(extracted, source=generated)
#     return generated

from fastapi import APIRouter
from pydantic import BaseModel
import os
from app.managers.chapter_manager import chapter_chain, update_chapter
from app.managers.summary_manager import summary_chain


router = APIRouter()




class ChapterInput(BaseModel):
    query: str

@router.post("/generate")
def generate_chapter(input: ChapterInput):
    result = chapter_chain(query=input.query)
    print("chapter generated")
    summary = summary_chain(result) # auto-call summary_chain
    print("summary generated")
    return {"chapter": result, "summary": summary}

class ChapterOutput(BaseModel):
    chapter: str
    chapter_num: int

@router.post("/change")
def change_chapter(input: ChapterOutput):
    update_chapter(input.chapter, chapter_num=input.chapter_num)
    summary_chain(input.chapter, chapter_num=input.chapter_num)
    return {"message": "Success"}
    
@router.post("/get_all")
def get_all_chapters():
    all_chapters = []
    for filename in os.listdir("data/samples/raws"):
        if filename.endswith(".txt"):
            with open(os.path.join("data/samples/raws", filename), "r", encoding="utf-8") as f:
                content = f.read()
                all_chapters.append({"filename": filename, "content": content})
    all_chapters.sort(key=lambda x: int(x["filename"].split("_")[1].split(".")[0]))
    return {"all_chapters": all_chapters}

class ChapterNumber(BaseModel):
    chapter_num: int
    
@router.post("/get_one")
def get_one_chapter(input: ChapterNumber):
    filename = f"chapter_{input.chapter_num:03}.txt"
    filepath = os.path.join("data/samples/raws", filename)
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        return {"filename": filename, "content": content}
    else:
        return {"error": "Chapter not found."}


# @router.post("/generate")
# def generate_text(request: GenerateRequest):
#     try:
#         result = model.generate(request.prompt, request.role, request.max_new_tokens, request.temperature, request.top_k, request.top_p)
#         return {"output": result}
#     except Exception as e:
#         print(f"Error during generation: {e}")
#         return {"error": str(e)}
    

# @router.post("/generate_ollama")
# def generate_text_by_ollama(request: GenerateRequest):
#     result = subprocess.run(
#         ["ollama", "run", "--model", "llama3.2:1b-instruct-fp16", request.prompt],
#         capture_output=True, text=True
#     )
#     output = result.stdout
#     return {"output": output}

# class GenerateRequest(BaseModel):
#     prompt: str
#     role: str = None
#     max_new_tokens: int = 2048
#     temperature: float = 0.7
#     top_k: int = 50
#     top_p: float = 0.95

# @router.post("/generate_and_save")
# def generate_and_save(request: GenerateRequest):
#     # try:
        
        
#         result = LLM.generate(request.prompt, request.role, request.max_new_tokens, request.temperature, request.top_k, request.top_p)
#         # result = "Prompt: \n" + request.prompt + "\nResponse: \n" + result
#         save_dir = "data/samples/raws"
#         os.makedirs(save_dir, exist_ok=True)

#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#         filename = f"generated_{timestamp}"
#         filepath = os.path.join(save_dir, filename) + ".txt"

#         with open(filepath, "w", encoding="utf-8") as f:
#             f.write(result)

#         summary = LLM.summarize(result, filename=filename)

#         return {"output": result, "saved_path": filepath, "summary": summary}
    # except Exception as e:
    #     print(f"Error during generation: {e}")
    #     return {"error": str(e)}

# def generate_with_memory(prompt):
#     generated = model.generate(prompt)
#     extracted = extract_keywords(generated)
#     insert_to_memory(extracted, source=generated)
#     return generated


    
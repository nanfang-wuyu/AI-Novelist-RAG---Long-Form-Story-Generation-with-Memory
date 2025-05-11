from app.models.model import LLM
from app.utils.prompts import get_chapter_generation_prompt
from app.managers import vector_manager as vm
import os

SAVE_DIR = "data/samples/raws"
os.makedirs(SAVE_DIR, exist_ok=True)



def get_latest_chapter_num(store_type="summary"):
    vectorstore = vm.load_vectorstore(store_type)
    all_docs = vectorstore.docstore._dict.values()
    chapter_numbers = [doc.metadata.get("chapter", 0) for doc in all_docs if isinstance(doc.metadata.get("chapter", 0), int)]
    latest_chapter_num = max(chapter_numbers) if chapter_numbers else 0
    return latest_chapter_num

def get_latest_and_relevant_chapter_summaries(user_query: str, k = 10):
    
    summary_vs = vm.load_vectorstore("summary")
    latest_chapter_num = get_latest_chapter_num()
    
    all_docs = summary_vs.docstore._dict.values()
    latest_summary_docs = [doc for doc in all_docs if doc.metadata.get("chapter") == latest_chapter_num]
    latest_summary_doc = latest_summary_docs[0] if latest_summary_docs else ""

    related_docs = vm.get_relevant_documents("summary", user_query, k)
    if latest_summary_doc in related_docs:
        related_docs.remove(latest_summary_doc)
    related_summaries = "\n\n".join(["Summary of Chapter {}:\n\n".format(doc.metadata.get("chapter")) + doc.page_content for doc in related_docs])
    return latest_chapter_num, latest_summary_doc, related_summaries

def setup_prompt(query: str, context_info):
    prompt = get_chapter_generation_prompt(query, *context_info)
    return prompt



def generate_chapter(prompt):
    generated_chapter = LLM.generate(prompt, max_tokens=2048)
    return generated_chapter

def save_chapter_to_file(chapter: str, chapter_num: int):
    filename = f"chapter_{chapter_num:03}.txt"
    filepath = os.path.join(SAVE_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(chapter)

def add_chapter(chapter: str, chapter_num: int):
    vm.add_document(
        store_type="chapter",
        content=chapter,
        metadata={"type": "chapter", "chapter": chapter_num}
    )
    save_chapter_to_file(chapter, chapter_num)

def update_chapter(chapter: str, chapter_num: int):
    vm.update_document(
        store_type="chapter",
        chapter_num=chapter_num,
        new_content=chapter
    )
    save_chapter_to_file(chapter, chapter_num)


    

def chapter_chain(query):
    context_info = get_latest_and_relevant_chapter_summaries(query)
    prompt = setup_prompt(query, context_info)
    chapter = generate_chapter(prompt)
    new_chapter_num = context_info[0] + 1
    add_chapter(chapter, new_chapter_num)
    return chapter


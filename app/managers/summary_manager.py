import os
from langchain.schema import Document
from app.models.model import Summary_Model
from app.managers import vector_manager as vm
from app.managers.chapter_manager import get_latest_chapter_num, chapter_chain


SAVE_DIR = "data/samples/summarized"
os.makedirs(SAVE_DIR, exist_ok=True)


def generate_summary(chapter: str, max_length: int = 100) -> str:
    return Summary_Model.summarize(chapter, max_length=max_length)


def save_summary_to_file(summary: str, chapter_num: int):
    filename = f"chapter_{chapter_num:03}_summary.txt"
    filepath = os.path.join(SAVE_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(summary)


def add_summary(summary: str, chapter_num: int):
    vm.add_document(
        store_type="summary",
        content=summary,
        metadata={"type": "summary", "chapter": chapter_num}
    )


def update_summary(summary: str, chapter_num: int):
    
    vm.update_document(
        store_type="summary",
        chapter_id=chapter_num,
        new_content=summary
    )


def get_relevant_summaries(query: str, top_k: int = 10):
    return vm.get_relevant_documents(
        store_type="summary",
        query=query,
        top_k=top_k
    )


def summary_chain(text: str, chapter_num: int = None) -> str:
    new_chapter_num = get_latest_chapter_num() + 1
    if chapter_num is None or chapter_num >= new_chapter_num:
        chapter_num = new_chapter_num
        summary = generate_summary(text)
        save_summary_to_file(summary, chapter_num)
        add_summary(summary, chapter_num)
    else:
        summary = generate_summary(text)
        save_summary_to_file(summary, chapter_num) # cover old file
        update_summary(summary, chapter_num)
    return summary

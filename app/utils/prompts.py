def get_chapter_generation_prompt(user_query, latest_chapter, latest_summary_doc, related_summaries):
    if latest_chapter > 1:

        prompt = f"""You are a novelist working on a long novel.

Here is a summary of the previously on few related chapters:

"{related_summaries}"

And here is a summary of the previously on the last chapter (Chapter {latest_summary_doc.metadata.get("chapter")}): 

"{latest_summary_doc.page_content}"

Please continue to WRITE the CONTENT of the NEXT CHAPTER - chapter {latest_chapter + 1}, keeping it logically coherent, within about 300 words. 

Here is what the user expects to see in the next chapter: "{user_query}"

    """
    elif latest_chapter == 1:
        prompt = f"""You are a novelist working on a long novel.

Here is a summary of the previously on the first chapter (Chapter {latest_summary_doc.metadata.get("chapter")}): 

"{latest_summary_doc.page_content}"

Please continue to WRITE the CONTENT of the NEXT CHAPTER - chapter {latest_chapter + 1}, keeping it logically coherent, within about 300 words. 

Here is what the user expects to see in the next chapter: "{user_query}"
"""
    else:
        prompt = f"""You are a novelist working on a long novel.

Please WRITE the content of the chapter 1 within about 300 words. 

Here is what the user expects to see in the chapter 1: "{user_query}"

    """


    return prompt
import re

def extract_info(text: str) -> str:

    keywords = re.findall(r'\b[A-Z][a-z]+\b', text)  
    return ' '.join(keywords)

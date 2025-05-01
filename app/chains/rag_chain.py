from langchain.chains import RetrievalQA
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from app.utils.memory import faiss_index
from langchain.vectorstores import FAISS
import numpy as np
from app.models.model import model



def create_retriever():
    return faiss_index.as_retriever(search_kwargs={"k": 3})

def setup_llm():
    llm = model
    return llm

def setup_rag_chain(retriever, llm):
    prompt_template = """
    You are writing a new chapter of a story. Use the following context from previous chapters and information to ensure logical consistency in the new content:

    Context: {context}
    Prompt: {query}

    Generate a continuation of the story while keeping it logically consistent with the provided context.
    """

    prompt = PromptTemplate(input_variables=["context", "query"], template=prompt_template)
    
    llm = setup_llm()
    
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain

def generate_response(query, rag_chain):
    result = rag_chain.run(query=query)
    return result

def rag_generate(query):
    retriever = create_retriever()
    llm = setup_llm()
    rag_chain = setup_rag_chain(retriever, llm)
    response = generate_response(query, rag_chain)
    return response

# 示例调用
query = "What did Kevin do at the magic show?"
response = rag_generate(query)
print(response)

# from app.models.tinyllama import TinyLlamaModel
from app.models.gpt4omini import GPT4OMini
from app.models.bart_large_cnn import BartSummaryModel
from langchain_huggingface import HuggingFaceEmbeddings

# model = TinyLlamaModel()
LLM = GPT4OMini()
Summary_Model = BartSummaryModel()
Embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
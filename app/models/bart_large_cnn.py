from transformers import pipeline
import os

class BartSummaryModel:
    def __init__(self):
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    def summarize(self, text: str, max_length = 100) -> str:
        summary = self.summarizer(text, max_length=max_length, min_length=50, do_sample=False)[0]['summary_text']
        return summary

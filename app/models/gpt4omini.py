import os
from openai import OpenAI
import getpass

class GPT4OMini:
    def __init__(self, model_name="gpt-4o-mini", api_key=None):
        self.model_name = model_name
        self.api_key = api_key 
        if self.api_key == None:
            self.api_key = os.getenv("OPENAI_API_KEY")
        if self.api_key == None:
            self.api_key = getpass.getpass("Enter API key for OpenAI: ")
        if self.api_key == None:
            raise ValueError("API key is required. Please set it in the environment variable OPENAI_API_KEY or provide it directly.")
        self.client = OpenAI(
            # This is the default and can be omitted
            api_key=self.api_key,
        )

    def generate(self, prompt: str, role: str = None, max_tokens: int = 512, temperature=0.7, top_p=0.95):
        role = role or "You are a friendly chatbot who always responds in the style of a novelist."
        messages = [
            {"role": "system", "content": role},
            {"role": "user", "content": prompt}
        ]
        response = self.client.chat.completions.create(
            messages=messages,
            model=self.model_name,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p
        )
        return response.choices[0].message.content

    def summarize(self, text: str, prompt: str = None, role: str = None, filename: str = '', max_tokens=256) -> str:
        prompt = prompt or f"Write a SHORT summary recording the main plot and setting for the following content WITHIN 100 words:\n\n{text}\n\nSummary:"
        role = role or "You are a friendly chatbot who is a novelist and summarizes text concisely."

        messages = [
            {"role": "system", "content": role},
            {"role": "user", "content": prompt}
        ]

        response = self.client.chat.completions.create(
            messages=messages,
            model=self.model_name,
            max_tokens=max_tokens,
            temperature=0.5,
            top_p=1.0
        )

        summary = response.choices[0].message.content

        
        return summary

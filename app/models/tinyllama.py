import torch
from transformers import pipeline
import os

class TinyLlamaModel:
    def __init__(self, model_name="TinyLlama/TinyLlama-1.1B-Chat-v1.0"):

        self.pipe = pipeline(
            "text-generation",
            model=model_name,
            torch_dtype=torch.bfloat16,  
            device_map="auto"  
        )

    def generate(self, prompt: str, role: str = None, max_new_tokens: int = 256, temperature=0.7, top_k=50, top_p=0.95):
        
        role = role if role else "You are a friendly chatbot who always responds in the style of a novelist"
        messages = [
            {"role": "system", "content": role},
            {"role": "user", "content": prompt}
        ]
        prompt = self.pipe.tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=False
        )
        outputs = self.pipe(prompt, max_new_tokens=max_new_tokens, do_sample=True, temperature=temperature, top_k=top_k, top_p=top_p)
        return outputs[0]["generated_text"].split("<|assistant|>")[-1].strip()

    def summarize(self, text: str, prompt: str = None, role: str = None, filename: str = '', max_new_tokens=200) -> str:
        
        prompt = prompt if prompt else f"Write a SHORT summary recording the main plot and setting for the following content WITHIN 100 words:\n\n{text}\n\nSummary:"

        role = role if role else "You are a friendly chatbot who are a novelist and summarize the text in a concise manner"
        messages = [
            {"role": "system", "content": role},
            {"role": "user", "content": prompt}
        ]
        prompt = self.pipe.tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=False
        )

        summary = self.pipe(prompt, max_new_tokens=200, do_sample=False)[0]['generated_text'].split("<|assistant|>")[-1].strip()
        save_dir = "data/samples/summarized"
        filepath = os.path.join(save_dir, filename) + "_summary.txt"
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(summary)
        return summary

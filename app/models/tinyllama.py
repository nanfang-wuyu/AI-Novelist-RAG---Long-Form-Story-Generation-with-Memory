import torch
from transformers import pipeline

class TinyLlamaModel:
    def __init__(self, model_name="TinyLlama/TinyLlama-1.1B-Chat-v1.0"):

        self.pipe = pipeline(
            "text-generation",
            model=model_name,
            torch_dtype=torch.bfloat16,  
            device_map="auto"  
        )

    def generate(self, prompt: str, max_new_tokens: int = 256, temperature=0.7, top_k=50, top_p=0.95):
        
        messages = [
            {"role": "system", "content": "You are a friendly chatbot who always responds in the style of a novelist"},
            {"role": "user", "content": prompt}
        ]
        prompt = self.pipe.tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        outputs = self.pipe(prompt, max_new_tokens=max_new_tokens, do_sample=True, temperature=temperature, top_k=top_k, top_p=top_p)
        return outputs[0]["generated_text"]

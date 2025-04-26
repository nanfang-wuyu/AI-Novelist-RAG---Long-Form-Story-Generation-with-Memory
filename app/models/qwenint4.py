import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, TextStreamer, BitsAndBytesConfig


class LocalQwenModel:
    

    def __init__(self, model_path: str = "Qwen/Qwen2.5-7B-Instruct-GPTQ-Int4"):
        self.model_path = model_path
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
        
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            device_map="auto",
            trust_remote_code=True,
            torch_dtype="auto",
            # quantization_config=self.quantization_config,
            low_cpu_mem_usage=True,
        )

        self.streamer = TextStreamer(self.tokenizer, skip_prompt=True, skip_special_tokens=True)


    def generate(self, prompt: str, max_new_tokens: int = 256) -> str:
        
        messages = [
            {"role": "system", "content": "You are a helpful novelist."},
            {"role": "user", "content": prompt}
        ]
        
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

        inputs = self.tokenizer([text], return_tensors="pt").to(self.device)
        
        with torch.no_grad():
            output = self.model.generate(
                **inputs,
                # streamer=self.streamer,
                max_new_tokens=max_new_tokens,
                # do_sample=True,
                temperature=0.8,
                top_p=0.9
            )
        return self.tokenizer.decode(output[0], skip_special_tokens=True)

import transformers
import torch
import os
import sys

class Model:
    def __init__(self):
        self.name: str = None
        self.tokenizer = None
        self.model = None

    def set_model(self, name: str, torch_dtype: str = "auto", device_map: str = "auto"):
        if not self.name or self.name != name:
            print(f"[*] Task: Preparing to load '{name}'")
            self.name = name
            
            # Optimization for Colab Free Tier (CPU/T4)
            dtype = torch.float16 if torch.cuda.is_available() else torch.float32
            device = "cuda" if torch.cuda.is_available() else "cpu"

            print(f"[*] Step 1/3: Loading Tokenizer...")
            self.tokenizer = transformers.AutoTokenizer.from_pretrained(self.name)
            
            print(f"[*] Step 2/3: Loading Model weights on {device} (Dtype: {dtype})...")
            self.model = transformers.AutoModelForCausalLM.from_pretrained(
                self.name,
                torch_dtype=dtype,
                device_map=device_map,
                trust_remote_code=True
            )

            if self.tokenizer.pad_token_id is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
                
            print(f"[!] SUCCESS: {self.name} is ready.")
        return self

    def query(self, task=None, instruction=None, rules=None, inp=None, context=None, code=None, output=None, max_new_tokens=256):
        if not self.model:
            return "Error: Model not loaded."

        print("[*] Constructing structured prompt...")
        segments = []
        if task: segments.append(f"# TASK\n{task}")
        if instruction: segments.append(f"## INSTRUCTIONS\n{instruction}")
        if rules: segments.append(f"## RULES\n{rules}")
        if context: segments.append(f"## CONTEXT\n{context}")
        if code: segments.append(f"## CODE REFERENCE\n```python\n{code}\n```")
        if inp: segments.append(f"## INPUT\n{inp}")
        if output: segments.append(f"## EXPECTED OUTPUT\n{output}")

        prompt_content = "\n\n".join(segments)
        messages = [
            {"role": "system", "content": "You are a professional Python developer."},
            {"role": "user", "content": prompt_content}
        ]

        text = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)

        print(f"[*] Tokenization complete. Generating response (max_new_tokens={max_new_tokens})...")
        
        with torch.no_grad():
            generated_ids = self.model.generate(
                **model_inputs,
                max_new_tokens=max_new_tokens,
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                pad_token_id=self.tokenizer.pad_token_id
            )

        print("[*] Decoding output...")
        generated_ids = [output_ids[len(model_inputs.input_ids[0]):] for output_ids in generated_ids]
        return self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

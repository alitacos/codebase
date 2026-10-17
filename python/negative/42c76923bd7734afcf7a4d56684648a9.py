import transformers
import torch
import os

class Model:
    def __init__(self):
        self.name: str = None
        self.tokenizer = None
        self.model = None

    def set_model(self, name: str, torch_dtype: str = "auto", device_map: str = "auto"):
        """
        Downloads and loads the model and tokenizer with progress updates.
        """
        if not self.name or self.name != name:
            print(f"[1/3] Initializing download/load for: {name}")
            self.name = name
            
            print(f"[2/3] Loading Tokenizer...")
            self.tokenizer = transformers.AutoTokenizer.from_pretrained(self.name)
            
            print(f"[3/3] Loading Model (this may take a minute based on connection/size)...")
            self.model = transformers.AutoModelForCausalLM.from_pretrained(
                self.name,
                torch_dtype=torch_dtype,
                device_map=device_map,
                trust_remote_code=True
            )
            
            # Ensure pad_token is set to avoid warnings
            if self.tokenizer.pad_token_id is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
                
            print(f"SUCCESS: Model '{self.name}' is loaded on {self.model.device}.")
        else:
            print(f"Model '{self.name}' is already loaded.")
        return self

    def query(self, task=None, instruction=None, rules=None, inp=None, context=None, code=None, output=None, max_new_tokens=512):
        if not self.model:
            return "Error: Model not loaded. Run set_model() first."
            
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
            {"role": "system", "content": "You are a world-class Python developer and code assistant."},
            {"role": "user", "content": prompt_content}
        ]

        text = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)

        generated_ids = self.model.generate(
            **model_inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            pad_token_id=self.tokenizer.pad_token_id
        )

        generated_ids = [output_ids[len(model_inputs.input_ids[0]):] for output_ids in generated_ids]
        return self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

# --- Initialization ---
coder_model = Model().set_model(name="Qwen/Qwen2.5-Coder-1.5B")
#NEGATIVE
from typing import Any, Tuple

import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel


class GPTGenerator:
    def __init__(self, model_path: str, seq_len=60):
        self.seq_len = seq_len
        self.device = torch.device("cpu")
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_path)
        self.model = GPT2LMHeadModel.from_pretrained(model_path).to(self.device)
        self.model.eval()

    def encode_text(self, text):
        text_tokens = self.tokenizer.encode(text, add_special_tokens=False,
                                            add_prefix_space=True)
        return text_tokens

    def get_context_tokens(self, input_text_for_tokens, max_context_len=1024):
        tokens = self.tokenizer.encode(input_text_for_tokens, add_special_tokens=False)
        return tokens

    def generate_text(self, input_text: str, context: Any) -> Tuple[str, Any]:
        if not isinstance(context, str):
            raise NotImplementedError("Only strings plz")
        input_text_for_tokens = input_text + context
        context_tokens = self.get_context_tokens(input_text_for_tokens)
        context_tensor = torch.tensor(context_tokens, dtype=torch.long)
        generated = context_tensor
        pasts = None
        with torch.no_grad():
            for j in range(self.seq_len):
                output = self.model(input_ids=generated, past_key_values=None)
                logits = output['logits'][-1, :]
                pasts = output['past_key_values']
                next_token = torch.argmax(logits, dim=-1).unsqueeze(-1)
                generated = torch.cat((generated, next_token))
        generated_tokens = generated[len(context_tokens):].tolist()
        generated_text = self.tokenizer.decode(generated_tokens,
                                               clean_up_tokenization_spaces=False,
                                               skip_special_tokens=True)
        return generated_text, context + input_text + generated_text
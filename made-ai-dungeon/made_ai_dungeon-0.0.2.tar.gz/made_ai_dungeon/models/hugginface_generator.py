from typing import Optional, Union, List, Dict

import requests
from loguru import logger


class HugginfaceGenerator:
    def __init__(self, api_url: str, headers: str, context_length: int = 300) -> None:
        self.api_url = api_url
        self.headers = headers
        self.context_length = context_length

    def generate_text(self, input_text: str, context: Optional[str]) -> tuple[str, str]:
        if context is None:
            context = ""
        elif len(context) > self.context_length:
            context = context[-self.context_length:]
        query_text = context + input_text
        query_output = self.query_hugginface(query_text)
        if query_output is None:
            new_context = context
            generated_text = "Проблемы с сервером попробуйте позже"
        else:
            text = query_output[0].get('generated_text')
            new_context = text
            generated_text = text[len(query_text):]

        logger.info("Generated text: {gt}, Context: {ct}", gt=generated_text, ct=new_context)
        return generated_text, new_context

    def query_hugginface(self, text: str) -> Union[List[Dict[str, str]], None]:
        response = requests.post(self.api_url, headers=self.headers, json=text).json()
        if isinstance(response, list):
            return response
        return None

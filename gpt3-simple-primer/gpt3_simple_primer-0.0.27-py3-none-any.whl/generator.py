from typing import Dict
import logging

import openai


level = logging.INFO
logging.basicConfig(level=level)
logger = logging.getLogger(__name__)


class GPT3Generator:
    # TODO: add parametrization around more flexible priming (instead of always using input-output)
    def __init__(self,
                 engine: str,
                 max_tokens: int,
                 temperature: float = 1,
                 top_p: int = 1) -> None:
        '''Wrapper for simplifying priming
        see https://beta.openai.com/docs/api-reference for documentation
        '''
        self.engine = engine
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.instructions: str = ''
        self.examples: Dict[str, str] = {}

    def set_key(self, key: str) -> None:
        '''set OpenAI API key'''
        openai.api_key = key

    def set_instructions(self, instructions: str) -> None:
        '''Set instructions for language generation (followed by examples)

        Parameters:
        -----------
        instructions (str): priming instructions
        '''
        if self.instructions != '':
            logger.warning('Previous instructions overwritten.')
        self.instructions = instructions + '\n\n'

    def add_example(self, input: str, output: str) -> None:
        '''Add an example to the primed prompt

        Parameters:
        -----------
        input (str): input text in example

        output (str): output text in example
        '''
        if input in self.examples:
            logger.warning(f'Example already exists. This will cause duplicate examples in the prompt.')
        else:
            self.examples[input] = output

    def remove_example(self, input: str) -> None:
        '''Removes an example'''
        try:
            del self.examples[input]
        except KeyError:
            logger.warning(f'Example {input} not found in existing examples.')

    def get_prompt(self) -> str:
        '''Returns the prompt used for language generation'''
        if self.instructions == '' and not self.examples:
            raise ValueError('No prompt has been provided. Please use at least one of set_instructions(), add_examples().')

        expanded_examples = '\n\n'.join([f'Input: {k}\nOutput: {v}' for k, v in self.examples.items()])
        
        return f'{self.instructions}{expanded_examples}'

    def get_gpt3_response(self, starting_text: str) -> openai.openai_response:
        '''Call OpenAI API to get the prompt'''
        prompt = self.get_prompt() + f'\n\nInput: {starting_text}'
        try:
            return openai.Completion.create(engine=self.engine,
                                            prompt=prompt,
                                            max_tokens=self.max_tokens,
                                            temperature=self.temperature,
                                            top_p=self.top_p)
        except openai.error.AuthenticationError:
            raise Exception('Use set_key to set OpenAI key. If already set, check if it is correct.')

    def generate(self, starting_text: str) -> None:
        '''Get generated text'''
        gpt3_response = self.get_gpt3_response(starting_text)
        generated_text = gpt3_response['choices'][0]['text'].strip()
        return generated_text.split('\n\nInput')[0].replace('Output: ', '')

import re

#TODO: Eliminar Corpus_Transformer
class Corpus_Transformer:

    def __init__(self, thought_tuples: [], filters: []):
        self.tuples = thought_tuples
        self.filters = filters

    def execute(self, has_tokenized_tokens=False):

        for thought in self.tuples:
            for filter in self.filters:
                if not has_tokenized_tokens:
                    new_offers = filter.transform(thought.offers)
                    thought.offers = new_offers
                    print('len de ofers',len(thought.offers))
                else:
                    new_tokenized_offers = filter.transform(thought.tokenized_offers, has_tokenized_tokens)
                    thought.tokenized_offers = new_tokenized_offers
                    print('len de tokenized ofers',len(thought.tokenized_offers))

        return self.tuples

class Base_Corpus_Filter:
    TOKENIZED_SEPARATOR = 'toksep'

    def transform (self, messages:[], has_tokenized_tokens=False):

        if not has_tokenized_tokens:
            result = []
            for message in messages:
                result.extend(self.execute(message))
        else:
            result = []
            print('messages', messages)
            for message in messages:
                print('message individual', message)
                full_message = self.TOKENIZED_SEPARATOR.join(message)
                print('full message', full_message)
                result.extend(self.execute(full_message, has_tokenized_tokens))
                print('result', result)
                for i, val in enumerate(result):
                    if isinstance(val, str):
                        result[i] = val.split(self.TOKENIZED_SEPARATOR)
                print('final result', result)
                print('#####\n')
        return result

class Ignore_Accents_Filter (Base_Corpus_Filter):

    def __init__(self):
        self.accent_regex = r"[áéíóú]"
        self.accent_mapping = {'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u'}

    def execute (self, orig_message:str, has_tokenized_tokens=None):

        result = []
        result.append(orig_message)

        punctuation_indices = [m.start(0) for m in re.finditer(self.accent_regex, orig_message)]

        for index in punctuation_indices:
            new_messages = []

            for message in result:
                #creates a new message changing the accent
                new_messages.append(message[:index] + self.accent_mapping[message[index]] + message[index + 1:])

            result.extend(new_messages)

        return result

class Ignore_Punctuation_Filter (Base_Corpus_Filter):

        def __init__(self):
            self.punctuation_regex = r"[!#$%&\'()*+,-./:;<=>?@^_`~¿¡]"

        def execute(self, orig_message: str, has_tokenized_tokens=None):

            result = []
            result.append(orig_message)

            punctuation_indices = [m.start(0) for m in re.finditer(self.punctuation_regex, orig_message)]
            orig_length = len(orig_message)

            for index in punctuation_indices:
                new_messages = []

                for message in result:
                    len_diff = orig_length - len(message)
                    # creates a new message without the given punctuation
                    new_messages.append(message[:index - len_diff] + message[index + 1 - len_diff:])

                result.extend(new_messages)

            return result

class Ignore_Casing_Filter (Base_Corpus_Filter):

    def execute(self, orig_message: str, has_tokenized_tokens=None):

        result = []
        result.append(orig_message)

        for index, char in enumerate(orig_message):

            if char.isalpha() is False:
                continue

            new_messages = []

            for message in result:
                # creates a new message swapping that character casing
                new_messages.append(message[:index] + char.swapcase() + message[index + 1:])

            result.extend(new_messages)

        return result

class Ignore_First_Letter_Casing_Filter (Base_Corpus_Filter):

    def execute(self, orig_message: str, has_tokenized_tokens=None):

        result = []
        result.append(orig_message)

        letter_index = 0

        if has_tokenized_tokens is None:
            #splits by whitespace
            splited_message = orig_message.split()
        else:
            splited_message = orig_message.split(self.TOKENIZED_SEPARATOR)

        for word in splited_message:

            new_messages = []

            for message in result:
                # creates a new message swapping the first character casing
                if word != '':
                    new_messages.append(message[:letter_index] + word[0].swapcase() + message[letter_index + 1:])
                else:
                    new_messages.append(message[:letter_index])

            if has_tokenized_tokens is None:
                letter_index += len(word) + 1
            else:
                letter_index += len(word) + len(self.TOKENIZED_SEPARATOR)
            result.extend(new_messages)

        return result


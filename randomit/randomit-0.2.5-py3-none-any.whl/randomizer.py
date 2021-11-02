import random, re
from pathlib import Path
from randomit.parsers.random_images import ImageScraper

# TODO: add  sentence generator
# TODO: add email generator

RANDOM_WORDS_FILE = Path(__file__).parent / 'words_storage' / 'random_words.txt'
NAMES_FILE = Path(__file__).parent.resolve() / 'words_storage' / 'names_list.txt'
SURNAMES_FILE = Path(__file__).parent.resolve() / 'words_storage' / 'surnames_list.txt'
COUNTRIES_FILE = Path(__file__).parent.resolve() / 'words_storage' / 'countries_list.txt'
CITIES_FILE = Path(__file__).parent.resolve() / 'words_storage' / 'cities_list.txt'
ADDRESS_LIST = Path(__file__).parent.resolve() / 'words_storage' / 'addresses_list.txt'


class Words:

    def __init__(self,
                 file=None,
                 theme: str = 'random words' or 'names' or 'surnames' or 'cities' or 'countries' or 'address'
                 ):
        self.theme = theme.lower().strip()
        self.file = file

    def available_themes(self):
        return ['random words', 'names', 'surnames', 'cities', 'countries', 'address']

    def load_words(self):

        if self.theme == '':
            raise ValueError("Apparently, no theme specified. Please add theme='THEME' argument.")

        if self.file == '':
            raise ValueError("Apparently, no file specified. Please add file='FILE' argument.")

        if self.file:
            with open(self.file, 'r', encoding='utf-8') as file:
                return [word.replace('\n', '') for word in file]

        if self.theme == 'random':
            with open(RANDOM_WORDS_FILE, 'r', encoding='utf-8') as all_words:
                return [word.replace('\n', '') for word in all_words]

        elif self.theme == 'random words':
            with open(RANDOM_WORDS_FILE, 'r', encoding='utf-8') as all_words:
                return [word.replace('\n', '') for word in all_words]

        elif self.theme == 'names':
            with open(NAMES_FILE, 'r', encoding='utf-8') as all_words:
                return [word.replace('\n', '') for word in all_words]

        elif self.theme == 'surnames':
            with open(SURNAMES_FILE, 'r', encoding='utf-8') as all_words:
                return [word.replace('\n', '') for word in all_words]

        elif self.theme == 'cities':
            with open(CITIES_FILE, 'r', encoding='utf-8') as all_words:
                return [word.replace('\n', '') for word in all_words]

        elif self.theme == 'countries':
            with open(COUNTRIES_FILE, 'r', encoding='utf-8') as all_words:
                return [word.replace('\n', '') for word in all_words]

        elif self.theme == 'address':
            with open(ADDRESS_LIST, 'r', encoding='utf-8') as all_words:
                return [word.replace('\n', '') for word in all_words]

        else:
            raise ValueError(
                "No such build-in theme. Hover over a Words() object to see available themes. Or call available_themes() function.")

    def randomize(self,
                  letter_starts_with: str = '',
                  amount_to_return: int = 0,
                  capitalize: bool = False,
                  return_one_word: bool = False,
                  return_dict: bool = False,
                  ) -> list[str] or str:

        words = Words(file=self.file, theme=self.theme).load_words()

        words_list = []

        if return_dict and amount_to_return and self.theme == 'address':
            for word in words:
                address = ''.join(re.findall(r'(.*),', word))
                city = ''.join(re.findall(r',\s?(\w+\s?\w{3,})', word))
                state = ''.join(re.findall(r'(\w{2})\s?\d+$', word))
                zip_code = ''.join(re.findall(r'\d+$', word))

                words_list.append({
                    "address": address,
                    "city": city,
                    "state": state,
                    "zip": zip_code
                })

            return [words_list[random.randrange(0, len(words_list))] for _ in range(amount_to_return)]

        if self.theme == 'address' and return_dict:
            for word in words:
                address = ''.join(re.findall(r'(.*),', word))
                city = ''.join(re.findall(r',\s?(\w+\s?\w{3,})', word))
                state = ''.join(re.findall(r'(\w{2})\s?\d+$', word))
                zip_code = ''.join(re.findall(r'\d+$', word))

                words_list.append({
                    "address": address,
                    "city": city,
                    "state": state,
                    "zip": zip_code
                })

            return [words_list[random.randrange(0, len(words_list))] for _ in
                    range(1, 702)]  # 1-702 number of total addresses in .txt file

        if return_one_word and capitalize:
            for word in words:
                words_list.append(word.title())

            return ''.join([words_list[random.randrange(0, len(words_list))] for _ in range(1)])

        if capitalize and amount_to_return and letter_starts_with:
            for word in words:
                if word.startswith(letter_starts_with.lower()):
                    words_list.append(word.title())

            return [words_list[random.randrange(0, len(words_list))] for _ in range(amount_to_return)]

        if capitalize and amount_to_return:
            for word in words:
                words_list.append(word.title())

            return [words_list[random.randrange(0, len(words_list))] for _ in range(amount_to_return)]

        if capitalize and letter_starts_with:
            for word in words:
                if word.startswith(letter_starts_with.lower()):
                    words_list.append(word.title())

            return words_list

        if amount_to_return and letter_starts_with:
            for word in words:
                if word.startswith(letter_starts_with.lower()):
                    words_list.append(word)

            return [words_list[random.randrange(0, len(words_list))] for _ in range(amount_to_return)]

        if capitalize:
            for word in words:
                words_list.append(word.title())

            return words_list

        elif amount_to_return:
            for word in words:
                words_list.append(word)

            return [words_list[random.randrange(0, len(words_list))] for _ in range(amount_to_return)]

        elif letter_starts_with:
            for word in words:
                if word.startswith(letter_starts_with.lower()):
                    words_list.append(word)

            return words_list

        elif return_one_word:
            return random.choice(words)

        else:
            for word in words:
                words_list.append(word)

            return words_list


class PhoneNumbers:
    '''
    Generate 10 random phone numbers:

    for _ in range(10):
        print(PhoneNumbers().randomize())

    +887 978-8625
    +562 633-8341
    +568 435-4740
    +2 295-5912
    +159 720-930
    ...
    '''

    def randomize(self):
        return f"+{random.randint(0, 999)} {random.randint(100, 9999)}-{random.randint(100, 9999)}"


class Images:

    def __init__(self, query: str = '', amount_to_return: int = 100):
        self.query = query
        self.amount_to_return = amount_to_return

    def get_randomized(self):
        images = ImageScraper(query=self.query, amount_to_return=self.amount_to_return).get_images()

        image_list = []

        if self.query and self.amount_to_return:
            for image in images:
                image_list.append(image)

            return [image_list[random.randrange(0, len(image_list))] for _ in range(self.amount_to_return)]

        if self.query == '':
            raise ValueError("It seems like you enter an empty query. Make sure you typed something.")

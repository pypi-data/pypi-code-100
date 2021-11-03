import string
import numpy as np

from typing import Union, List, Optional

from instancelib.instances.text import TextInstanceProvider

from text_explainability.default import Readable


class RandomData(Readable):
    def __init__(self,
                 seed: int = 0,
                 options: Union[str, List[str]] = string.printable):
        """Base class for random data (string) generation.

        Args:
            seed (int, optional): Seed for reproducibility. Defaults to 0.
            options (Union[str, List[str]], optional): Characters or strings to generate data from. 
                Defaults to string.printable.
        """
        self._seed = seed
        self.options = options

    def generate(self,
                 n: int,
                 min_length: int = 0,
                 max_length: int = 100) -> TextInstanceProvider:
        """Generate n instances of random data. 

        Args:
            n (int): Number of instances to generate.
            min_length (int, optional): Minimum length of random instance. Defaults to 0.
            max_length (int, optional): Maximum length of random instance. Defaults to 100.

        Raises:
            AssertionError: `min_length` should be smaller than `max_length`.

        Returns:
            TextInstanceProvider: Provider containing generated instances.
        """
        assert min_length < max_length, 'min_length should be smaller than max_length'
        min_length = max(min_length, 0)

        np.random.seed(self._seed)
        data = [''.join(np.random.choice(list(self.options))
                        for _ in range(np.random.randint(min_length, max_length)))
                for _ in range(n)]
        return TextInstanceProvider.from_data(data)       

    def __call__(self, *args, **kwargs):
        """Alias for `RandomData.generate()`."""
        return self.generate(*args, **kwargs)


class RandomSpaces(RandomData):
    def __init__(self,
                 seed: int = 0):
        """Generate strings with a random number of spaces."""
        super().__init__(seed=seed, options=' ')


class RandomWhitespace(RandomData):
    def __init__(self,
                 seed: int = 0):
        """Generate strings with a random number whitespace characters."""
        super().__init__(seed=seed, options=string.whitespace)


class RandomAscii(RandomData):
    def __init__(self,
                 seed: int = 0):
        """Generate random ASCII characters."""
        super().__init__(seed=seed, options=string.ascii_letters)


class RandomUpper(RandomData):
    def __init__(self,
                 seed: int = 0):
        """Generate random ASCII uppercase characters."""
        super().__init__(seed=seed, options=string.ascii_uppercase)


class RandomLower(RandomData):
    def __init__(self,
                 seed: int = 0):
        """Generate random ASCII lowercase characters."""
        super().__init__(seed=seed, options=string.ascii_lowercase)


class RandomDigits(RandomData):
    def __init__(self,
                 seed: int = 0):
        """Generate strings containing random digits."""
        super().__init__(seed=seed, options=string.digits)


class RandomPunctuation(RandomData):
    def __init__(self,
                 seed: int = 0):
        """Generate strings containing random punctuation characters."""
        super().__init__(seed=seed, options=string.punctuation)


class RandomEmojis(RandomData):
    def __init__(self,
                 seed: int = 0,
                 base: bool = True,
                 dingbats: bool = True,
                 flags: bool = True,
                 components: bool = False):
        """Generate strings containing a subset of random unicode emojis.

        Args:
            seed (int, optional): Seed for reproducibility. Defaults to 0.
            base (bool, optional): Include base emojis (e.g. smiley face).
                Defaults to True.
            dingbats (bool, optional): Include dingbat emojis. Defaults to True.
            flags (bool, optional): Include flag emojis. Defaults to True.
            components (bool, optional): Include emoji components (e.g. skin color 
                modifier or country flags). Defaults to False.

        Raises:
            AssertionError: At least one of `base`, `dingbats`, `flags` should be True.
        """
        assert base or dingbats or flags, \
            'At least one of `base`, `dingbats`, `flags` should be True.'
        emojis = []
        if base:
            emojis.extend(['\U0001F600', '\U0001F601', '\U0001F602', '\U0001F603',
                           '\U0001F604', '\U0001F605', '\U0001F606', '\U0001F607',
                           '\U0001F608', '\U0001F609', '\U0001F60A', '\U0001F60B',
                           '\U0001F60C', '\U0001F60D', '\U0001F60E', '\U0001F60F',
                           '\U0001F610', '\U0001F611', '\U0001F612', '\U0001F613',
                           '\U0001F910', '\U0001F911', '\U0001F912', '\U0001F913'])
        if dingbats:  # 2700-27BF
            emojis.extend(['\U00002704', '\U00002705', '\U00002706', '\U00002707',
                           '\U00002708', '\U00002709', '\U0000270A', '\U0000270B',
                           '\U0000270C', '\U0000270D', '\U0000270E', '\U0000270F',
                           '\U0000274C', '\U0000274D', '\U0000274E', '\U0000274F'])
        if flags:
            emojis.extend(['\U00002690', '\U00002691', '\U0001F3F3', '\U0001F3F4',
                           '\U0001F6A9'])
            if components:  # e.g. country flags
                emojis.extend(['\U0001F1E6\U0001F1E8', '\U0001F1E6\U0001F1E9',
                               '\U0001F1E6\U0001F1EA', '\U0001F1E6\U0001F1EB'])
        if components:
            emojis.extend(['\U0001F9D1\U0001F3FB', '\U0001F9D1\U0001F3FC',
                           '\U0001F9D1\U0001F3FD', '\U0001F9D1\U0001F3FE'])
        super().__init__(seed=seed, options=emojis)


class RandomCyrillic(RandomData):
    def __init__(self,
                 languages: Union[List[str], str] = 'ru',
                 upper: bool = True,
                 lower: bool = True,
                 seed: int = 0):
        """Generate containing random Cyrillic characters.

        Can generate text in Bulgarian ('bg'), Macedonian ('mk'), Russian ('ru'), Serbian ('sr'), Ukrainian ('uk'), 
        and all combinations thereof.

        Args:
            languages (Union[List[str], str], optional): Cyrillic languages to select. Defaults to 'ru'.
            upper (bool, optional): Whether to include 
            seed (int, optional): Seed for reproducibility. Defaults to 0.

        Raises:
            Exception: Either upper or lower should be True.
            AssertionError: One of the selected languages is unknown.
        """
        if not upper and not lower:
            raise Exception('At least one of upper and lower should be True. Cannot generate text.')

        if isinstance(languages, str):
            languages = [languages]
        languages = [str.lower(lang) for lang in languages]

        lowercase = {'bg': u'абвгдежзийклмнопрстуфхцчшщьъюя',
                     'mk': u'абвгдезијклмнопрстуфхцѓжѕљњќчџш',
                     'ru': u'абвгдеёжзийклмнопрстуфхцчшщъыьэюя',
                     'sr': u'абвгдђежзијклљмнњопрстћуфхцчџш',
                     'uk': u'абвгґдезиійклмнопрстуфьєжїхцчшщюя'}
        uppercase = {'bg': u'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЮЯЪ',
                     'mk': u'АБВГДЕЗИЈКЛМНОПРСТУФХЦЃЖЅЉЊЌЧЏШ',
                     'ru': u'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ',
                     'sr': u'АБВГДЂЕЖЗИЈКЛЉМНЊОПРСТЋУФХЦЧЏШ',
                     'uk': u'АБВГҐДЕЗИІЙКЛМНОПРСТУФЬЄЖЇХЦЧШЩЮЯ'}

        options = ''

        for lang in languages:
            assert lang in lowercase.keys(), f'Unknown language code "{lang}". Choose from {list(lowercase.keys())}.'
            if lower:
                options += lowercase[lang]
            if upper:
                options += uppercase[lang]

        super().__init__(seed=seed, options=options)


def combine_generators(*generators, seed: Optional[int] = None) -> RandomData:
    """Combine muliple random data generators into one.

    Args:
        *generators: Generators to combine.
        seed (Optional[int]): Seed value for new generator. 
            If None picks a random seed from the generators. Defaults to None.

    Example:
        Make a generator that generates random punctuation, emojis and ASCII characters:

        >>> new_generator = combine_generators(RandomPunctuation(), RandomEmojis(), RandomAscii())

    Returns:
        RandomData: Generator with all generator options combined.
    """
    all_options = [list(generator.options) for generator in generators]
    if seed is None:
        seed = np.random.choice([generator._seed for generator in generators])
    return RandomData(seed=seed,
                      options=[item for sublist in all_options for item in sublist])

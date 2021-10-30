import re
import fasttext
import swifter
import wget
import numpy as np
import pandas as pd

from pathlib import Path
from textblob_de import TextBlobDE
from sklearn.base import BaseEstimator, TransformerMixin


class Preprocessor(BaseEstimator, TransformerMixin):

    def __init__(self,
                 fasttext_model_path='models/',
                 merge_cols=True,
                 remove_hashtags=True,
                 log=False):
        # FastText model configs
        fasttext.FastText.eprint = lambda x: None
        fasttext_model_name = 'lid.176.ftz'
        fasttext_model_url = f'https://dl.fbaipublicfiles.com/fasttext/supervised-models/{fasttext_model_name}'
        fasttext_model_path = Path(fasttext_model_path)

        # check if model exists
        if not Path(fasttext_model_path / fasttext_model_name).is_file():
            wget.download(fasttext_model_url, out=str(fasttext_model_path))

        # load the fasttext model
        self.fasttext_model = fasttext.load_model(str(fasttext_model_path / fasttext_model_name))

        # configs
        self.merge_cols = merge_cols
        self.rm_hashtags = remove_hashtags
        self.log = log

    def fit(self, X, y=None):
        return self

    def transform(self, df: pd.DataFrame, **_) -> pd.DataFrame:
        # make a copy of the dataframe
        df_cleaned = df.copy(deep=True)

        if self.merge_cols:
            # merge all columns with prefix `text`
            cols = [x for x in df_cleaned.columns if x.startswith('text')]
            df_cleaned['text'] = df_cleaned[cols].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)
            df_cleaned = df_cleaned[[x for x in df_cleaned.columns if x not in cols]]

        # clean up the text
        df_cleaned = Preprocessor.standard_replacements(df_cleaned)
        df_cleaned = Preprocessor.remove_hashtags(df_cleaned,
                                                  remove=self.rm_hashtags,
                                                  log=self.log)
        df_cleaned = Preprocessor.remove_emails(df_cleaned, log=self.log)
        df_cleaned = Preprocessor.remove_mentions(df_cleaned)
        df_cleaned = Preprocessor.remove_emojis(df_cleaned)

        # remove multiple spaces
        df_cleaned.text = df_cleaned.text.swifter.progress_bar(False).apply(lambda x: re.sub(r' +', ' ', str(x)).strip()
                                                        if x is not np.nan else x)
        df_cleaned = df_cleaned.replace('', np.nan, regex=True)

        # drop all `np.nan` values in the `text` column, ie. entries without a review
        df_cleaned.dropna(subset=['text'], inplace=True)

        # remove all duplicates
        df_cleaned = df_cleaned.drop_duplicates(subset=['text'])

        # remove all non-german reviews
        df_cleaned = Preprocessor.remove_non_german_lang(df_cleaned,
                                                         self.fasttext_model,
                                                         log=self.log)

        # remove auxiliary columns
        df_cleaned = df_cleaned.drop(columns=['text_lang', 'text_lang_conf'])

        return df_cleaned

    @staticmethod
    def remove_umlaut(string: str):
        """
        Removes umlauts from strings and replaces them with the letter+e convention
        :param string: string to remove umlauts from
        :return: unumlauted string
        """

        u = 'ü'.encode()
        U = 'Ü'.encode()
        a = 'ä'.encode()
        A = 'Ä'.encode()
        o = 'ö'.encode()
        O = 'Ö'.encode()
        ss = 'ß'.encode()

        string = string.encode()
        string = string.replace(u, b'ue')
        string = string.replace(U, b'Ue')
        string = string.replace(a, b'ae')
        string = string.replace(A, b'Ae')
        string = string.replace(o, b'oe')
        string = string.replace(O, b'Oe')
        string = string.replace(ss, b'ss')
        string = string.decode('utf-8')

        return string

    @staticmethod
    def apply_umlaut(string: str):
        """
        Converts non-umlauts to umlauts from strings
        :param string: string to apply umlauts from
        :return: umlauted string
        """

        u = 'ü'.encode()
        U = 'Ü'.encode()
        a = 'ä'.encode()
        A = 'Ä'.encode()
        o = 'ö'.encode()
        O = 'Ö'.encode()

        string = string.encode()
        string = string.replace(b'ue', u)
        string = string.replace(b'Ue', U)
        string = string.replace(b'ae', a)
        string = string.replace(b'Ae', A)
        string = string.replace(b'oe', o)
        string = string.replace(b'Oe', O)
        string = string.decode('utf-8')

        return string

    @staticmethod
    def pluralize(word: str) -> str:
        """
        Pluralizes a given word.

        Using TextBlobDE the word gets pluralized.

        Parameters
        ----------
        word : str
            Word to pluralize.
        """
        result = TextBlobDE(word).words.pluralize()

        return ' '.join(result) if len(result) > 0 else ''

    @staticmethod
    def standard_replacements(df: pd.DataFrame, remove_umlauts=False, remove_numbers=False) -> pd.DataFrame:
        # strip the text
        df.text = df.text.swifter.progress_bar(False).apply(lambda x: x.strip() if x is not np.nan else x)
        # remove linebreaks
        df.text = df.text.swifter.progress_bar(False).apply(lambda x: re.sub(r'[\r\n]+', '', str(x)) if x is not np.nan else x)
        # remove all non-ascii signs
        df.text = df.text.swifter.progress_bar(False).apply(lambda x: re.sub(r'\&\#.+\;', '', str(x)) if x is not np.nan else x)
        # remove all html tags
        df.text = df.text.swifter.progress_bar(False).apply(lambda x: re.sub(r'<[^<]+?>', ' ', str(x)) if x is not np.nan else x)
        # remove all URLs
        df.text = df.text.swifter.progress_bar(False).apply(lambda x: re.sub(r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))", '', str(x)) if x is not np.nan else x)
        # remove multiple spaces
        df.text = df.text.swifter.progress_bar(False).apply(lambda x: re.sub(r' +', ' ', str(x)) if x is not np.nan else x)
        # replace all the repeated chars (e.g. if a char is repeated more than 3 times replace with a single char)
        # this includes everything except digits (e.g. also punctuation)
        df.text = df.text.swifter.progress_bar(False).apply(lambda x: re.sub(r'(\D)\1{3,}', r'\1', str(x)) if x is not np.nan else x)
        # replace all repeated punctuation (e.g. if a punctuation is repeated more than 1 time it gets replaced with a single)
        df.text = df.text.swifter.progress_bar(False).apply(lambda x: re.sub(r'([!#$%&*+,-.:;?])\1{1,}', r'\1', str(x)) if x is not np.nan else x)
        # remove all quotation marks
        df.text = df.text.swifter.progress_bar(False).apply(lambda x: re.sub(r"['\"<>«»“”‘’]", '', str(x)) if x is not np.nan else x)
        # remove all brackets that contain non-word characters, e.g. "(!), [...]"
        df.text = df.text.swifter.progress_bar(False).apply(lambda x: re.sub(r"\(\s*\W*?\s*\)", '', str(x)) if x is not np.nan else x)
        df.text = df.text.swifter.progress_bar(False).apply(lambda x: re.sub(r"\[\s*\W*?\s*\]", '', str(x)) if x is not np.nan else x)
        # remove all the other brackets without its content, e.g. (test) -> test
        df.text = df.text.swifter.progress_bar(False).apply(lambda x: re.sub(r"[()\[\]]", '', str(x)) if x is not np.nan else x)
        # remove all lists, e.g. numbered or not numbered ones
        df.text = df.text.swifter.progress_bar(False).apply(lambda x: re.sub(r'\d+.\s', ' ', str(x)) if x is not np.nan else x)
        df.text = df.text.swifter.progress_bar(False).apply(lambda x: re.sub(r'-\s', ' ', str(x)) if x is not np.nan else x)
        # remove various other characters which are not informative
        df.text = df.text.swifter.progress_bar(False).apply(lambda x: re.sub(r"[\$\%\&\€\*\°]", '', str(x)) if x is not np.nan else x)
        # remove more strange things
        df.text = df.text.swifter.progress_bar(False).apply(lambda x: re.sub(r"\|\w+\|", '', str(x)) if x is not np.nan else x)
        # remove all punctuation that is right at the start of a string
        df.text = df.text.swifter.progress_bar(False).apply(lambda x: re.sub(r'^[!#$%&*+\,\-\.\/:;]+', '', str(x)) if x is not np.nan else x)

        # replace non-breaking space with correct space
        df.text = df.text.str.replace(u'\xa0', u' ')

        if remove_numbers:
            # remove all digits from the text since they do not provide any additional information
            df.text = df.text.swifter.progress_bar(False).apply(lambda x: re.sub(r'[.,%]*\d+[.,%]*', '', str(x)) if x is not np.nan else x)
        else:
            df.text = Preprocessor.replace_numbers(df.text)

        # replace umlauts
        if remove_umlauts:
            df.text = df.text.swifter.progress_bar(False).apply(lambda x: Preprocessor.remove_umlaut(x) if x is not np.nan else x)

        return df

    @staticmethod
    def replace_numbers(series: pd.Series) -> pd.Series:
        """
        Replace all numbers with the text of the numbers.

        Numbers in a pandas series get replaced with the string representation of that number in German.
        E.g. 2 -> zwei.

        Parameters
        ----------
        series : pd.Series
            Series to replace the numbers in.

        Returns
        -------
        pd.Series:
            Series in which the numbers were replaced.
        """
        series = series.swifter.progress_bar(False).apply(
            lambda x: re.sub(r"0", ' null', str(x)) if x is not np.nan else x)
        series = series.swifter.progress_bar(False).apply(
            lambda x: re.sub(r"1", ' eins', str(x)) if x is not np.nan else x)
        series = series.swifter.progress_bar(False).apply(
            lambda x: re.sub(r"2", ' zwei', str(x)) if x is not np.nan else x)
        series = series.swifter.progress_bar(False).apply(
            lambda x: re.sub(r"3", ' drei', str(x)) if x is not np.nan else x)
        series = series.swifter.progress_bar(False).apply(
            lambda x: re.sub(r"4", ' vier', str(x)) if x is not np.nan else x)
        series = series.swifter.progress_bar(False).apply(
            lambda x: re.sub(r"5", ' fünf', str(x)) if x is not np.nan else x)
        series = series.swifter.progress_bar(False).apply(
            lambda x: re.sub(r"6", ' sechs', str(x)) if x is not np.nan else x)
        series = series.swifter.progress_bar(False).apply(lambda x: re.sub(
            r"7", ' sieben', str(x)) if x is not np.nan else x)
        series = series.swifter.progress_bar(False).apply(
            lambda x: re.sub(r"8", ' acht', str(x)) if x is not np.nan else x)
        series = series.swifter.progress_bar(False).apply(
            lambda x: re.sub(r"9", ' neun', str(x)) if x is not np.nan else x)

        return series

    @staticmethod
    def remove_hashtags(df: pd.DataFrame,
                        remove=True,
                        log=False) -> pd.DataFrame:
        """
        Removes all hashtags from the dataframe.

        Uses a regular expression to first find all the possible hashtags and then replaces them with an empty string.

        Parameters
        ----------
        df : pd.DataFrame
            Dataframe to replace the hashtags in.
        remove : bool,
            If the hashtags should be removed or if the hashtag should be replaced.
            Depends if the hashtags may contain some additional useful information.
        log : bool,
            If the function outputs removement.

        Returns
        -------
        pd.DataFrame:
            Returns the dataframe in which all hashtags were removed.
        """

        if log:
            hashtags = re.findall(r'\#\w+', ' '.join(
                    list(df[(df.text.str.contains(r'\#\w+'))
                            & (df.text != np.nan)].text)))
            print(f'Number of possible hastags: {len(hashtags)}')
        if remove:
            # remove the possible hashtags
            df.text = df.text.str.replace(r'\#\w+', '')
        else:
            # replace hashtag
            df.text = df.text.str.replace(r'\#', '')

        return df

    @staticmethod
    def remove_mentions(df: pd.DataFrame) -> pd.DataFrame:
        df.text = df.text.str.replace(r'(?:\@|https?\://)\S+', '')

        return df

    @staticmethod
    def remove_emojis(df: pd.DataFrame) -> pd.DataFrame:

        def remove_emoji(string):
            emoji_pattern = re.compile(
                "["
                u"\U0001F600-\U0001F64F"  # emoticons
                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                u"\U0001F680-\U0001F6FF"  # transport & map symbols
                u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                u"\U00002500-\U00002BEF"  # chinese char
                u"\U00002702-\U000027B0"
                u"\U00002702-\U000027B0"
                u"\U000024C2-\U0001F251"
                u"\U0001f926-\U0001f937"
                u"\U00010000-\U0010ffff"
                u"\u2640-\u2642"
                u"\u2600-\u2B55"
                u"\u200d"
                u"\u23cf"
                u"\u23e9"
                u"\u231a"
                u"\ufe0f"  # dingbats
                u"\u3030"
                "]+",
                flags=re.UNICODE)
            return emoji_pattern.sub(r'', string)

        df.text = df.text.apply(lambda x: remove_emoji(x))

        return df

    @staticmethod
    def remove_emails(df: pd.DataFrame, log=False) -> pd.DataFrame:
        """
        Removes all email addresses from the dataframe.

        Uses a regular expression to find all the possible email addresses in the dataframe and replaces them with an empty string.

        Parameters
        ----------
        df : pd.DataFrame
            Dataframe to remove the emails in.

        Returns
        -------
        pd.DataFrame:
            Dataframe in free of emails.
        """

        emails = re.findall(r'[\w.+]+@[\w\-]+\.[a-z]+', ' '.join(list(df[(df.text.str.contains(r'\@'))
                                                                         & (df.text != np.nan)].text)))
        if log:
            print(f'Number of possible emails: {len(emails)}')
        # remove the emails
        df.text = df.text.swifter.progress_bar(False).apply(lambda x: re.sub(r'[\w.+]+@[\w\-]+\.[a-z]+', '', str(x)) if '@' in str(x) else x)

        return df

    @staticmethod
    def remove_non_german_lang(df: pd.DataFrame,
                               fasttext_model: fasttext.FastText._FastText,
                               log=False) -> pd.DataFrame:
        """
        Removes all non-german reviews.

        Uses a trained fasttext model that was trained on detecting 176 different languages, to detect the language.
        Then the non-german reviews get removed.

        Parameters
        ----------
        df : pd.DataFrame
            Dataframe to remove the non-german reviews.

        Returns
        -------
        pd.DataFrame:
            Dataframe that only contains german reviews.
        """
        df['text_lang'] = df.text.swifter.progress_bar(False).apply(lambda text: (fasttext_model.predict(text, k=1)[0][0],
                                                              fasttext_model.predict(text, k=1)[1][0]))
        df[['text_lang', 'text_lang_conf']] = pd.DataFrame(df.text_lang.tolist(), index=df.index)
        df.text_lang = df.text_lang.replace('__label__', '', regex=True)

        df_filtered = df[df.text_lang == 'de']
        if log:
            not_german = len(df) - len(df_filtered)
            print(f'Number of rows dropped due to review not in german: {not_german}')
            print(f'Percentage of not german reviews: {round(not_german/len(df), 5)}%')
        df = df_filtered

        return df

import json
from os import listdir
from os.path import isfile, join
from typing import Dict, List, TextIO


class TranslationService:
    def __init__(self, translation_files_path: str, locale: str):
        self.locale = locale
        self.translation_files_path = translation_files_path
        self.messages = self._load_messages()

    def get(self, translation_key: str, translation_params: Dict[str, str] = None, **kwargs):
        try:
            locales = self.messages[self.locale]
            try:
                translation = locales[translation_key]
                if "{" in translation:
                    params_dict = translation_params if translation_params is not None else kwargs
                    translation = self._replace_params(translation, params_dict)
                return translation
            except KeyError:
                return translation_key
        except KeyError:
            raise Exception(f"Locale '{self.locale}' not defined")

    def change_locale(self, locale: str):
        self.locale = locale

    def _load_messages(self):
        messages_files = self._get_translation_files(self.translation_files_path)
        return {self._get_messages_filename(messages_file): self._get_messages(messages_file) for messages_file in
                messages_files}

    @classmethod
    def _get_translation_files(cls, messages_path: str) -> List[TextIO]:
        return [open(join(messages_path, f), 'r', encoding='utf-8') for f in listdir(messages_path) if
                isfile(join(messages_path, f))]

    @classmethod
    def _get_messages_filename(cls, messages_file):
        return messages_file.name.split('\\')[-1].split('.')[0]

    @classmethod
    def _get_messages(cls, messages_file: TextIO) -> Dict[str, str]:
        return json.load(messages_file)

    @classmethod
    def _replace_params(cls, translation, kwargs: Dict[str, str]) -> str:
        for param_name, params_value in kwargs.items():
            translation = translation.replace(f"{{{param_name}}}", f"{params_value}", 1)
        return translation

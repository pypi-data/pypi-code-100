from collections import namedtuple
import parsec as pc
from typing import List


class InflectionRule:
    """
    Supported commands:
        <E>: Empty string. DOes not modify the word
        <L>: keyboard Left arrow
        <R>: keyboard Right arrow
        <A>: remove accute accent from last letter aeiou
        <B>: keyboard Backspace
        <Á>: add acute accent to last letter aeiou
        <Ä>: add dieresis/trema/umlaut to last letter aeiou
    """

    VOWEL_REMOVE_ACUTE_ACCENT_REPLACEMENTS = {
        "á": "a",
        "é": "e",
        "í": "i",
        "ó": "o",
        "ú": "u",
    }
    VOWEL_ADD_ACUTE_ACCENT_REPLACEMENTS = {
        "a": "á",
        "e": "é",
        "i": "í",
        "o": "ó",
        "u": "ú",
    }
    VOWEL_ADD_DIERESIS_REPLACEMENTS = {
        "a": "ä",
        "e": "ë",
        "i": "ï",
        "o": "ö",
        "u": "ü",
    }
    PARADIGM_NAME_REGEX_STR = r"[A-ZÑÁÉÍÓÚÜÇa-zñáéíóúüç\-_0-9]+"

    Morpheme = namedtuple(
        "Morpheme",
        ["text", "features", "regional_settings", "deleted", "added"],
    )

    class PartialMorpheme:
        def __init__(self, current, cursor):
            self.current = current
            self.cursor = cursor
            self.deleted = []
            self.added = []

    def __init__(self, raw_rule: str, paradigm_producer):
        self.raw_rule = raw_rule
        self.paradigm_producer = paradigm_producer
        if "/" in raw_rule:
            rr_parts = raw_rule.split("/")
            self.commands = self.commands_parser().parse(rr_parts[0])
            self.features = []
            for f in rr_parts[1].split("+"):
                if (
                    f
                    in self.paradigm_producer.group.standard.feature_descriptor_list
                ):
                    self.features.append(
                        self.paradigm_producer.group.standard.feature_descriptor_list[
                            f
                        ]
                    )
                else:
                    raise Exception(
                        f"Regla de inflexion invalida. Id de feature invalido: \n{f} - {self.paradigm_producer.group.sheet_title} - {self.paradigm_producer.word_model} - {raw_rule}"
                    )
        else:
            raise Exception(
                f'Regla de inflexion invalida. El identificador es invalido o se omitio el separador "/". \n{self.paradigm_producer.group.sheet_title} - {self.paradigm_producer.word_model} - {raw_rule}'
            )

    def get_empty_command_parser(self):
        res = pc.string("<E>").result(self.empty_command)
        return res

    def empty_command(self, partial_morpheme: PartialMorpheme):
        return partial_morpheme

    def get_left_cursor_command_parser(self):
        res = pc.regex(r"<L[0-9]*>").parsecmap(
            lambda chars: self.create_left_cursor_command(chars)
        )
        return res

    def create_left_cursor_command(self, chars: str):
        chars = chars.strip("<L>")
        count = 1
        if chars:
            count = int(chars)

        def left_cursor_command(
            partial_morpheme: InflectionRule.PartialMorpheme,
        ):
            partial_morpheme.cursor -= count
            return partial_morpheme

        return left_cursor_command

    def get_right_cursor_command_parser(self):
        res = pc.regex(r"<R[0-9]*>").parsecmap(
            lambda chars: self.create_right_cursor_command(chars)
        )
        return res

    def create_right_cursor_command(self, chars: str):
        chars = chars.strip("<R>")
        count = 1
        if chars:
            count = int(chars)

        def right_cursor_command(
            partial_morpheme: InflectionRule.PartialMorpheme,
        ):
            partial_morpheme.cursor += count
            return partial_morpheme

        return right_cursor_command

    def get_remove_acute_accent_command_parser(self):
        res = pc.string("<A>").result(self.remove_acute_accent_command)
        return res

    def remove_acute_accent_command(self, partial_morpheme: PartialMorpheme):
        vowel_accent = partial_morpheme.current[partial_morpheme.cursor]
        temp_list = list(partial_morpheme.current)
        if (
            vowel_accent
            in InflectionRule.VOWEL_REMOVE_ACUTE_ACCENT_REPLACEMENTS
        ):
            temp_list[
                partial_morpheme.cursor
            ] = InflectionRule.VOWEL_REMOVE_ACUTE_ACCENT_REPLACEMENTS[
                vowel_accent
            ]
        else:
            raise Exception("El caracter no es una vocal acentuada.")
        partial_morpheme.current = "".join(temp_list)
        return partial_morpheme

    def get_add_acute_accent_command_parser(self):
        res = pc.string("<Á>").result(self.add_acute_accent_command)
        return res

    def add_acute_accent_command(self, partial_morpheme: PartialMorpheme):
        vowel_accent = partial_morpheme.current[partial_morpheme.cursor]
        temp_list = list(partial_morpheme.current)
        if vowel_accent in InflectionRule.VOWEL_ADD_ACUTE_ACCENT_REPLACEMENTS:
            temp_list[
                partial_morpheme.cursor
            ] = InflectionRule.VOWEL_ADD_ACUTE_ACCENT_REPLACEMENTS[
                vowel_accent
            ]
        else:
            raise Exception("El caracter no es una vocal sin acento.")
        partial_morpheme.current = "".join(temp_list)
        return partial_morpheme

    def get_add_dieresis_command_parser(self):
        res = pc.string("<Ä>").result(self.add_dieresis_command)
        return res

    def add_dieresis_command(self, partial_morpheme: PartialMorpheme):
        vowel_dieresis = partial_morpheme.current[partial_morpheme.cursor]
        temp_list = list(partial_morpheme.current)
        if vowel_dieresis in InflectionRule.VOWEL_ADD_DIERESIS_REPLACEMENTS:
            temp_list[
                partial_morpheme.cursor
            ] = InflectionRule.VOWEL_ADD_DIERESIS_REPLACEMENTS[vowel_dieresis]
        else:
            raise Exception("El caracter no es una vocal sin dieresis.")
        partial_morpheme.current = "".join(temp_list)
        return partial_morpheme

    def get_delete_current_char_command_parser(self):
        res = pc.regex(r"<B[0-9]*>").parsecmap(
            lambda chars: self.create_delete_current_char_command(chars)
        )
        return res

    def create_delete_current_char_command(self, chars: str):
        chars = chars.strip("<B>")
        count = 1
        if chars:
            count = int(chars)

        def delete_current_char_command(
            partial_morpheme: InflectionRule.PartialMorpheme,
        ):
            temp_list = list(partial_morpheme.current)
            for i in range(0, count):
                removed_char = temp_list.pop(partial_morpheme.cursor)
                partial_morpheme.cursor -= 1
                partial_morpheme.deleted.append(removed_char)
            partial_morpheme.current = "".join(temp_list)
            return partial_morpheme

        return delete_current_char_command

    def get_insert_in_current_position_command_parser(self):
        res = pc.regex(InflectionRule.PARADIGM_NAME_REGEX_STR).parsecmap(
            lambda chars: self.create_insert_in_current_position_command(chars)
        )
        return res

    def create_insert_in_current_position_command(self, chars: str):
        chars = chars.lower()

        def insert_in_current_position_command(
            partial_morpheme: InflectionRule.PartialMorpheme,
        ):
            temp_list = list(partial_morpheme.current)
            for c in chars:
                partial_morpheme.cursor += 1
                temp_list.insert(partial_morpheme.cursor, c)
                partial_morpheme.added.append(c)
            partial_morpheme.current = "".join(temp_list)
            return partial_morpheme

        return insert_in_current_position_command

    def commands_parser(self):
        options = (
            self.get_left_cursor_command_parser()
            ^ self.get_right_cursor_command_parser()
            ^ self.get_add_acute_accent_command_parser()
            ^ self.get_add_dieresis_command_parser()
        )
        options = (
            options
            ^ self.get_remove_acute_accent_command_parser()
            ^ self.get_delete_current_char_command_parser()
        )
        options = (
            options
            ^ self.get_empty_command_parser()
            ^ self.get_insert_in_current_position_command_parser()
        )
        return pc.many(options)

    def apply(self, lemma: str) -> Morpheme:
        partialMorpheme = InflectionRule.PartialMorpheme(lemma, len(lemma) - 1)
        for c in self.commands:
            partialMorpheme = c(partialMorpheme)
        return InflectionRule.Morpheme(
            partialMorpheme.current,
            self.features,
            self.paradigm_producer.group.regional_setting,
            partialMorpheme.deleted,
            partialMorpheme.added,
        )

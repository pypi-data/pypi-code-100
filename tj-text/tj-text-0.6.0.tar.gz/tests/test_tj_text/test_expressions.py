import pytest

from tj_text.typograph import en_typus, ru_typus
from tj_text.typograph.chars import HYPHEN, HYPHEN_MINUS, NBHYPHEN, NBSP
from tj_text.typograph.core import TypusCore
from tj_text.typograph.mixins import RuExpressions
from tj_text.typograph.processors import EscapeHtml, EscapePhrases, Expressions


@pytest.fixture()
def typus_factory():
    def factory(expression_mixin_cls, *, include=None, exclude=None):
        class Typus(expression_mixin_cls, TypusCore):
            processors = (EscapePhrases, EscapeHtml, Expressions)
            expressions = filter(
                lambda expr: (
                    (expr in include if include else True)
                    and (expr not in exclude if exclude else True)
                ),
                expression_mixin_cls.expressions,
            )

        return Typus()

    return factory


class TestEnRuExpressions:
    """Tests for typograph.mixins.EnRuExpressions class."""

    @pytest.mark.parametrize(
        'word_parts',
        [
            ('из', 'под'),
            ('когда', 'либо'),
            ('сим', 'карта'),
            ('QR', 'код'),
            ('где', 'нибудь'),
        ],
    )
    @pytest.mark.parametrize('hyphen', [HYPHEN, HYPHEN_MINUS])
    def test_expr_rep_hyphen_between_short_words(self, word_parts, hyphen):
        word = hyphen.join(word_parts)
        expected_word = NBHYPHEN.join(word_parts)
        text = (
            f'{word} проверим{word}дефис неразрывный {word} подставляется '
            f'корректно{word}между словами {word}.'
        )
        expected_text = (
            f'{expected_word} проверим{word}дефис неразрывный {expected_word} '
            f'подставляется корректно{word}между словами {expected_word}.'
        )

        result = en_typus(text)

        assert result == expected_text


class TestRuExpressions:
    """Tests for typograph.mixins.RuExpressions class."""

    def test_expressions_from_parent_class_are_in_child(self):
        for expression in ru_typus.expressions:
            assert expression in RuExpressions.expressions

    @pytest.mark.parametrize(
        'word',
        [
            'без',
            'перед',
            'при',
            'через',
            'над',
            'под',
            'про',
            'для',
            'около',
            'среди',
            'из-под',
            'из-за',
            'по-над',
        ],
    )
    def test_expr_rep_positional_spaces_after_long_prepositions(
        self, word, typus_factory
    ):
        typus = typus_factory(RuExpressions, exclude={'rep_hyphen_between_short_words'})
        text = (
            f'{word.capitalize()} проверяем{word} предлог {word} неразрывным '
            f'{word}пробелом {word}. {word.capitalize()} тоже.'
        )
        expected_result = (
            f'{word.capitalize()}{NBSP}проверяем{word} предлог {word}{NBSP}неразрывным '
            f'{word}пробелом {word}. {word.capitalize()}{NBSP}тоже.'
        )

        result = typus(text)

        assert result == expected_result

    @pytest.mark.parametrize('word', ['же', 'ли', 'бы', 'б', 'уж'])
    def test_expr_rep_positional_spaces_before_particles(self, word):
        text = f'Проверяем{word} частицу {word} неразрывным {word}пробелом {word}.'
        expected_result = (
            f'Проверяем{word} частицу{NBSP}{word} '
            f'неразрывным {word}пробелом{NBSP}{word}.'
        )

        result = ru_typus(text)

        assert result == expected_result

    @pytest.mark.parametrize(
        'original,expected',
        [
            ('несмотря на', f'несмотря{NBSP}на'),
            ('в отличие от', f'в{NBSP}отличие{NBSP}от'),
            ('в связи с', f'в{NBSP}связи{NBSP}с'),
        ],
    )
    def test_rep_positional_spaces_for_verbose_prepositions(self, original, expected):
        original_text = (
            f'{original.capitalize()} проверяем {original} неразрывным пробелом. '
            f'{original.capitalize()} даже в начале второго предложения.'
        )
        expected_result = (
            f'{expected.capitalize()}{NBSP}проверяем {expected}{NBSP}неразрывным '
            f'пробелом. '
            f'{expected.capitalize()}{NBSP}даже в{NBSP}начале второго предложения.'
        )

        result = ru_typus(original_text)

        assert result == expected_result

    @pytest.mark.parametrize(
        'original,expected', [('когда-нибудь', f'когда{NBHYPHEN}нибудь')]
    )
    def test_rep_custom_replacements(self, original, expected):
        original_text = (
            f'{original} проверим {original} слово-исключение '
            f'{original} будет сразу{original} заменено{original}.'
        )
        expected_result = (
            f'{expected} проверим {expected} слово-исключение '
            f'{expected} будет сразу{original} заменено{original}.'
        )

        result = ru_typus(original_text)

        assert result == expected_result

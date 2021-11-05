from django.db.models import CharField
from django.db.models.functions import Cast, Trim, Concat, Substr
from pyparsing import *
from .consts import Functions
from .core.utils import functions_attrs, functions_attrs_map

# Описание функций
Keywords = Functions.Keywords
String = Functions.String
Arithmetic = Functions.Arithmetic
Date = Functions.Date


class ExpressionTemplate:
    """
    Шаблоны выражений
    """

    @property
    def any(self):
        """
        Шаблон любого значения
        """
        return Regex(r'[\w.,-|]+')

    @property
    def key(self):
        """
        Получение ключа из начала запроса для определения фнукции обработки выражения:
        """
        return stringStart + Or([Keyword(key) for key in Functions.all_keys()])('key')

    # def _keyword(self, keyword, alias):
    #     """
    #     Единственное значение
    #     """
    #     return Group(Keyword(keyword) + '(' + self.any(alias) + ')')
    #
    # @property
    # def field(self):
    #     """
    #     Шаблон поля
    #     """
    #     return self._keyword(self.keywords.FIELD, 'field')
    #
    # @property
    # def value(self):
    #     """
    #     Шаблон значения
    #     """
    #     return self._keyword(self.keywords.VALUE, 'value')
    #
    # @property
    # def const(self):
    #     """
    #     Шаблон константы
    #     """
    #     return self._keyword(self.keywords.CONST, 'const')

    def _keywords(self, *items):
        """
        Группа ключевых слов
        """
        return Group(Or([Keyword(key) for key in items])('keyword') + '(' + self.any('value') + ')')

    @property
    def keywords(self):
        """
        Шаблон ключевых слов
        """
        return self._keywords(*Keywords.ITEMS)

    @property
    def dates(self):
        """
        Шаблон дат
        """
        return self._keywords(*Date.ITEMS)

    @property
    def substring(self):
        """
        Шаблон подстроки
        """
        return (
            Keyword(String.SUBSTRING)
            + '('
            + self.keywords("field")
            + ','
            + Word(nums)('position')
            + Optional(',' + Word(nums)('length'))
        )

    @property
    def concatenation(self):
        """
        Шаблон конкантенации строк
        """
        keywords = self._keywords(*Keywords.ITEMS, *Date.ITEMS)
        return Keyword(String.CONCAT) + '(' + OneOrMore(keywords)('fields') + ')'


@functions_attrs_map('syntax_key')
class SyntaxAnalyzer:
    """
    Синтаксический анализатор конструкций запросов
    """

    def __init__(self):
        self.template = ExpressionTemplate()

    def define_function(self, query):
        """
        Определение функции по ключу
        """
        conditions = self.template.key.parseString(query).asDict()
        if not conditions:
            return

        # Поиск функции по ключу
        return self.function_by_key(conditions.get('key'))

    @functions_attrs(syntax_key=String.key(String.SUBSTRING))
    def substring(self, query, **kwargs):
        """
        Подстрока
        """
        conditions = self.template.substring.parseString(query)
        if not conditions:
            return
        field, position, *length = conditions.asDict().values()
        return Substr(self._build_keyword(field), int(position), length and int(length[0]) or None)

    @functions_attrs(syntax_key=String.key(String.CONCAT))
    def concatenation(self, query, **kwargs):
        """
        Конкатенация
        """
        conditions = self.template.concatenation.parseString(query)
        if not conditions:
            return
        fields = conditions.asDict().get('fields')

        # Составление запроса из распарсенного выражения
        parts = []
        output_field = kwargs.get('output_field',  CharField())
        for index, field in enumerate(fields):
            parts.append(Cast(self._build_keyword(field), output_field=output_field))
        return Trim(Concat(*parts, output_field=output_field))

    def _build_keyword(self, keyword):
        """
        Построение ключевого слова
        """
        function = Functions.Keywords.FUNCTIONS.get(keyword.get('keyword'))
        return function(keyword.get('value'))

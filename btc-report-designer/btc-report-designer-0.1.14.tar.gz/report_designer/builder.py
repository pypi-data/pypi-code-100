import itertools
from itertools import groupby
from operator import itemgetter, eq

import pandas
from django.apps import apps
from django.contrib.postgres.aggregates import StringAgg
from django.db.models import CharField, Value, F, Case, When, Q
from django.db.models.constants import LOOKUP_SEP
from django.db.models.functions import Cast, Trim, Concat, Substr
from pyparsing import *
from .consts import Functions
from .core.joiner import CJoin
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
        output_field = kwargs.get('output_field', CharField())
        for index, field in enumerate(fields):
            parts.append(Cast(self._build_keyword(field), output_field=output_field))
        return Trim(Concat(*parts, output_field=output_field))

    def _build_keyword(self, keyword):
        """
        Построение ключевого слова
        """
        function = Functions.Keywords.FUNCTIONS.get(keyword.get('keyword'))
        return function(keyword.get('value'))


class ReportBuilder:
    """
    Конструктор отчетов
    """

    def __init__(self, queryset, fields, columns_names, group_fields=None, aggregation_fields=None, formats=None):
        # QuerySet с данными
        self.queryset = queryset
        # Поля шаблона
        self.fields = fields
        # Наименование полей
        self.columns_names = columns_names
        # Групповые поля
        self.group_fields = group_fields
        # Поля для аггрегации данных для групповых полей
        self.aggregation_fields = aggregation_fields or []
        # Форматы полей
        self.formats = formats

        # Параметры конструктора
        self.dataframe = None
        self.groups = None
        self.aggregation = None
        self.report = None
        self.levels = range(len(self.group_fields or []))

    def build(self):
        """
        Построение шаблона
        """
        # Установка dataframe
        self.set_dataframe()

        # Если есть групповые поля, установка групп и агрегированных значений
        if self.group_fields:
            self.set_groups()
            self.set_aggregation()

        # Заполнение отчета данными
        self.fill_dataframe()

        # Применение форматирование
        self.set_formats()

        # Переименование полей
        self.rename_columns()

    def set_dataframe(self):
        """
        Получение фрейма данных из набора данных
        """
        values = self.queryset.values(*self.fields)
        self.dataframe = pandas.DataFrame(values)

    def set_groups(self):
        """
        Группировка данных по заданным полям
        """
        # Установка индекса и сортировка по группируемым полям
        self.dataframe = self.dataframe.set_index(self.group_fields).sort_index(level=self.levels)
        if self.group_fields:
            self.groups = self.dataframe.groupby(self.group_fields)

    def set_aggregation(self):
        """
        Расчет агрегированных полей для группированных полей
        """
        if not self.aggregation_fields:
            return
        fields, functions = zip(*self.aggregation_fields)

        # Создание пустого фрейма с результатами
        aggregation = self._get_empty_frame(fields)

        # Связки уровней агрегирования и функций для аггрегирования
        bunches = itertools.product(self.levels, functions)
        aggregation_dataframe = self.dataframe[list(fields)]
        for level, function in bunches:
            # Получение данных для уровня и функции.
            # Т.к. агрегация по столбцам, то axis=0
            level_data = aggregation_dataframe.agg(function, level=level, axis=0)

            # Обновление индексов данных для привязки к уровню и функции
            level_data.index = level_data.index.map(lambda index: f'{level}_{function}_{index}')

            # Запись полученного фрейма во фрейм агрегации
            aggregation = aggregation.append(level_data)
        self.aggregation = aggregation

    def _build_header_group(self, index, level):
        """
        Построение шапки группы
        """
        # Пустой фрейм для создания шапки каждой группы
        empty = self._get_empty_frame(self.fields)

        header = []
        # Получение значений для каждого уровня, начиная с текущего
        for i in self.levels[level:]:
            # Текущее наименование группы
            key, value = self.group_fields[i], index[i]

            # Получение агрегируемых значений для текущего уровня
            aggregations = {
                column: self.aggregation[column][f'{i}_{function}_{value}']
                for column, function in self.aggregation_fields
            }
            header.append(empty.copy().append({key: value, **aggregations}, ignore_index=True))
        return pandas.concat(header)

    def fill_dataframe(self):
        """
        Заполнение фрейма данных данными из выборки и группированными данными
        """
        # Фрейм для заполнения шаблона
        report = self._get_empty_frame(self.fields)

        if self.groups:
            # На начальной итерации индекс пустой
            previous_index = ()
            for index, group in self.groups:
                # Если отчет имеет одиночную группировку
                if not isinstance(index, tuple):
                    index = (index,)

                # Текущий level. Получен путем нахождение первого
                # расхождения индекса группы и предыдущего текущего индекса
                level = sum(eq(*item) for item in zip(previous_index, tuple(index)))

                # Построение шапки группы, добавление группы и шапки в шаблон
                report = report.append(self._build_header_group(index, level))
                report = report.append(group)

                # Установка предыдущего индекса
                previous_index = index
        else:
            report = report.append(self.dataframe)
        self.report = report

    def set_formats(self):
        """
        Применение форматирования
        """
        if not self.formats:
            return
        self.report.reset_index(drop=True, inplace=True)
        for field, format_string in self.formats.items():
            self.report[field] = self.report[field].apply(
                lambda item: item if pandas.isnull(item) else f'{item:{format_string}}'
            )

    def rename_columns(self):
        """
        Переименование полей
        """
        self.report.reset_index(drop=True, inplace=True)
        self.report.columns = list(self.columns_names)

    @staticmethod
    def _get_empty_frame(fields):
        """
        Построение пустого фрейма на основании полей
        """
        return pandas.DataFrame(dict.fromkeys(fields, []))


class ReportDataHandler:
    """
    Обработчик данных отчета перед формированием
    """

    def __init__(self, report):
        # Шаблон
        self.report = report

        # Выборка отчета
        self.queryset = None

        # Параметры
        self.tables_relations_map = {}
        self.report_fields = None
        self.field_values = None
        self.formats = None
        self.group_fields = None
        self.aggregation_fields = None
        self.sorted_fields = None
        self.columns_names = None
        self.value = None

    def run(self):
        """
        Запуск обработки данных отчета для формирования
        """
        # Маппинг таблиц отчета
        self.set_queryset()

        # Присоединение таблиц отчета
        self.join_tables()

        # Установка полей отчета
        self.set_report_fields()

        # Установка полей для выборки
        self.set_field_values()

        # Получение форматов
        self.set_formats()

        # Групповые поля
        self.set_group_fields()

        # Аггрегированные поля
        self.set_aggregation_fields()

        # Сортировочные поля
        self.set_sorted_fields()

        # Установка
        self.set_columns_names()

        # Получение значений выборки
        self.set_report()

    def set_queryset(self):
        """
        Установка выборки
        """
        self.queryset = self.report.root.table.model_class().objects.all()

    def join_tables(self):
        """
        Присоединение таблиц отчета
        """
        # Вспомогательные параметры
        table_template = 'db_table__table__%s'
        parent_table_template = 'relations__parent__report_table__db_table__table__%s'
        rel_field_template = 'relations__from_report_table_relations__%s__db_field'

        # Аннотация параметров для группировки
        group_annotation_kwargs = {
            'app_label': F(table_template % 'app_label'),
            'model': F(table_template % 'model'),
            'relation_pk': F('relations__pk'),
        }

        # Аннотация не группируемых параметров
        annotation_kwargs = {
            'from_field': F(rel_field_template % 'from_field'),
            'to_field': F(rel_field_template % 'to_field'),
            'parent_app_label': F(parent_table_template % 'app_label'),
            'parent_model': F(parent_table_template % 'model'),
        }

        # Получение таблиц отчета
        report_tables = (
            self.report.report_tables.filter(is_root=False)
            .select_related('db_table')
            .prefetch_related('relations', 'relations__from_report_table_relations')
            .annotate(**group_annotation_kwargs, **annotation_kwargs)
        )

        # Параметры для прикрепления таблиц
        group_annotation_kwargs_keys = group_annotation_kwargs.keys()
        report_tables_attrs = report_tables.values(*group_annotation_kwargs_keys, *annotation_kwargs.keys())

        # Группировка аттрибутов по первым трем параметрам
        def key_function(attrs):
            return [attrs[key] for key in group_annotation_kwargs.keys()]

        def _values(key, array):
            return list(map(itemgetter(key), array))

        for group_key, group_value in groupby(report_tables_attrs, key=key_function):
            app_label, model, relation_pk = group_key

            # Сохранение связи для полей
            alias = f'{app_label}_{model}_{relation_pk}'
            self.tables_relations_map[relation_pk] = alias

            # Присоединение таблицы
            group_values_list = list(group_value)
            self.queryset = CJoin(
                self.queryset,
                apps.get_model(app_label, model),
                _values('from_field', group_values_list),
                _values('to_field', group_values_list),
                alias,
            ).join()

    def set_field_values(self):
        """
        Поля для отчета для выборки
        """
        self.field_values = self.report_fields.values_list('lookup', flat=True)

    def set_report_fields(self):
        """
        Поля отчета с аннотацией уникального имени
        """
        base_lookup_parts = (
            StringAgg('relations__db_field', LOOKUP_SEP),
            F('field__db_field'),
        )
        self.report_fields = (
            self.report.report_fields.annotate(
                field_name=Concat(Value('field_'), Cast('pk', output_field=CharField())),
                report_table_relation_lookup=Case(
                    *[
                        When(report_table_relation__isnull=False, report_table_relation_id=pk, then=Value(lookup))
                        for pk, lookup in self.tables_relations_map.items()
                    ],
                    default=Value(''),
                    output_field=CharField(),
                ),
            )
            .annotate(
                # todo: здесь что-то не так
                lookup=Case(
                    *[
                        # Установка виртуальных полей происходит отдельно
                        When(is_virtual=True, then=Value('')),
                        When(relations__isnull=True, report_table_relation_lookup__exact='', then=F('field__db_field')),
                        When(
                            relations__isnull=False,
                            report_table_relation_lookup__exact='',
                            then=Concat(*base_lookup_parts),
                        ),
                    ],
                    default=Concat('report_table_relation_lookup', Value(LOOKUP_SEP), *base_lookup_parts),
                    output_field=CharField(),
                ),
            )
            .prefetch_related('representation')
            .order_by('order')
        )

    def set_formats(self):
        """
        Установка форматов полей
        """
        self.formats = dict(
            self.report_fields.filter(representation__isnull=False).values_list(
                'field_name', 'representation__representation'
            )
        )

    def set_group_fields(self):
        """
        Получение групповых полей
        """
        self.group_fields = list(self.report_fields.filter(is_group=True).values_list('lookup', flat=True))

    def set_aggregation_fields(self):
        """
        Получение агрегированных полей
        """
        self.aggregation_fields = list(
            self.report_fields.filter(is_aggregate=True).values_list('field_name', 'aggregate_function')
        )

    def set_sorted_fields(self):
        """
        Получение сортировочных полей
        """
        self.sorted_fields = (
            self.report_fields.filter(is_sort=True)
            .annotate(
                sorted_field=Case(
                    When(reverse_sort=True, then=Concat(Value('-'), 'lookup')),
                    default=F('lookup'),
                    output_field=CharField(),
                )
            )
            .values_list('sorted_field', flat=True)
        )

    def set_columns_names(self):
        """
        Получение полей
        """
        self.columns_names = list(
            self.report_fields.annotate(
                title=Case(When(alias__exact='', then=F('name')), default=F('alias'))
            ).values_list('title', flat=True)
        )

    def set_report(self):
        """
        Формирование отчета
        """
        # Фильтрация по групповым полям
        # Сортировка
        queryset = self.queryset.filter(
            *(
                Q(Q(**{f'{field}__isnull': False}), Q(**{f'{field}__iexact': ''}), _connector=Q.OR)
                for field in self.group_fields
            )
        ).order_by(*self.sorted_fields)
        # Построение шаблона
        builder = ReportBuilder(
            queryset,
            self.field_values,
            self.columns_names,
            self.group_fields,
            self.aggregation_fields,
            self.formats,
        )
        builder.build()
        self.report = builder.report

from collections import namedtuple

from django.db.models.expressions import Combinable, Value, F
from django.db.models.functions import (
    ExtractYear,
    ExtractQuarter,
    ExtractMonth,
    ExtractWeek,
    ExtractWeekDay,
    ExtractDay,
    ExtractHour,
    ExtractMinute,
    ExtractSecond,
)
from django.utils.translation import ugettext_lazy as _


class InternalType:
    """
    Тип поля
    """

    AUTO_FIELD = 0
    BIG_AUTO_FIELD = 1
    BINARY_FIELD = 2
    BOOLEAN_FIELD = 3
    CHAR_FIELD = 4
    DATE_FIELD = 5
    DATE_TIME_FIELD = 6
    DECIMAL_FIELD = 7
    DURATION_FIELD = 8
    FILE_FIELD = 9
    IMAGE_FIELD = 10
    FILE_PATH_FIELD = 11
    FLOAT_FIELD = 12
    INTEGER_FIELD = 13
    BIG_INTEGER_FIELD = 14
    GENERIC_IP_ADDRESS_FIELD = 15
    NULL_BOOLEAN_FIELD = 16
    POSITIVE_INTEGER_FIELD = 17
    POSITIVE_SMALL_INTEGER_FIELD = 18
    SLUG_FIELD = 19
    SMALL_INTEGER_FIELD = 20
    TEXT_FIELD = 21
    TIME_FIELD = 22
    URL_FIELD = 23
    UUID_FIELD = 24

    # Соотношение значений с реальными полями
    INTERNAL_TYPES = (
        (AUTO_FIELD, 'AutoField'),
        (BIG_AUTO_FIELD, 'BigAutoField'),
        (BINARY_FIELD, 'BinaryField'),
        (BOOLEAN_FIELD, 'BooleanField'),
        (CHAR_FIELD, 'CharField'),
        (DATE_FIELD, 'DateField'),
        (DATE_TIME_FIELD, 'DateTimeField'),
        (DECIMAL_FIELD, 'DecimalField'),
        (DURATION_FIELD, 'DurationField'),
        (FILE_FIELD, 'FileField'),
        (IMAGE_FIELD, 'ImageField'),
        (FILE_PATH_FIELD, 'FilePathField'),
        (FLOAT_FIELD, 'FloatField'),
        (INTEGER_FIELD, 'IntegerField'),
        (BIG_INTEGER_FIELD, 'BigIntegerField'),
        (GENERIC_IP_ADDRESS_FIELD, 'GenericIPAddressField'),
        (NULL_BOOLEAN_FIELD, 'NullBooleanField'),
        (POSITIVE_INTEGER_FIELD, 'PositiveIntegerField'),
        (POSITIVE_SMALL_INTEGER_FIELD, 'PositiveSmallIntegerField'),
        (SLUG_FIELD, 'SlugField'),
        (SMALL_INTEGER_FIELD, 'SmallIntegerField'),
        (TEXT_FIELD, 'TextField'),
        (TIME_FIELD, 'TimeField'),
        (URL_FIELD, 'URLField'),
        (UUID_FIELD, 'UUIDField'),
    )

    CHOICES = (
        (AUTO_FIELD, _('Автоинкрементное')),
        (BIG_AUTO_FIELD, _('Автоинкрементное (64-битное)')),
        (BINARY_FIELD, _('Бинарное')),
        (BOOLEAN_FIELD, _('Логическое')),
        (CHAR_FIELD, _('Строковое')),
        (DATE_FIELD, _('Дата')),
        (DATE_TIME_FIELD, _('Дата и время')),
        (DECIMAL_FIELD, _('Десятичное с фиксированной точностью')),
        (DURATION_FIELD, _('Период времени (в микросекундах)')),
        (FILE_FIELD, _('Файл')),
        (IMAGE_FIELD, _('Изображение')),
        (FILE_PATH_FIELD, _('Путь до файла')),
        (FLOAT_FIELD, _('Число с плавающей точкой')),
        (INTEGER_FIELD, _('Целочисленное')),
        (BIG_INTEGER_FIELD, _('Целочисленное (64-битное)')),
        (GENERIC_IP_ADDRESS_FIELD, _('IP адрес')),
        (NULL_BOOLEAN_FIELD, _('Логическое с нулевым значением')),
        (POSITIVE_INTEGER_FIELD, _('Положительное целочисленное')),
        (POSITIVE_SMALL_INTEGER_FIELD, _('Положительное целочисленное (16-битное)')),
        (SLUG_FIELD, _('Название-метка')),
        (SMALL_INTEGER_FIELD, _('Целочисленное (16-битное)')),
        (TEXT_FIELD, _('Текстовое')),
        (TIME_FIELD, _('Время')),
        (URL_FIELD, _('URL')),
        (UUID_FIELD, _('UUID')),
    )

    @classmethod
    def get_internal_type(cls, choice_name: int):
        return dict(cls.INTERNAL_TYPES).get(choice_name, choice_name)

    @classmethod
    def get_value_by_internal_type(cls, choice_name: int):
        return dict(map(reversed, cls.INTERNAL_TYPES)).get(choice_name, choice_name)

    @classmethod
    def get_display_value(cls, choice_name: int):
        return dict(cls.CHOICES).get(choice_name, choice_name)


class AggregateFunctionChoices:
    """
    Функции агрегирования
    """

    SUM = 'sum'
    MEAN = 'mean'
    MAX = 'max'
    MIN = 'min'

    ITEMS = (
        SUM,
        MEAN,
        MAX,
        MIN,
    )

    CHOICES = (
        (SUM, _('Сумма')),
        (MEAN, _('Среднее')),
        (MAX, _('Максимальное')),
        (MIN, _('Минимальное')),
    )


class Functions:
    """
    Функции конструктора отчетов
    """

    class __KeyMaker:
        """
        Получение ключа для функций
        """

        @classmethod
        def key(cls, key: str):
            """
            Генерация ключа
            """
            return f'{cls.__name__.lower()}:{key.lower()}'

    class Keywords:
        """
        Ключевые слова, используемые в других выражениях
        """

        CONST = 'const'
        FIELD = 'field'
        VALUE = 'value'

        ITEMS = (
            CONST,
            FIELD,
            VALUE,
        )

        TITLES = {
            CONST: _('Константа'),
            FIELD: _('Поле'),
            VALUE: _('Значение'),
        }

        DISPLAY_NAMES = {
            CONST: _('КОНСТАНТА'),
            FIELD: _('ПОЛЕ'),
            VALUE: _('ЗНАЧЕНИЕ'),
        }

        FUNCTIONS = {
            CONST: Value,
            FIELD: F,
            VALUE: Value,
        }

    class String(__KeyMaker):
        """
        Функции работы со строками
        """

        title = _('Функции работы со строками')

        CONCAT = 'concat'
        SUBSTRING = 'substring'

        ITEMS = (
            CONCAT,
            SUBSTRING,
        )

        CHOICES = (
            (CONCAT, _('Конкатенация'), _('КОНКАТ'), True),
            (SUBSTRING, _('Подстрока'), _('ПОДСТРОКА'), True),
        )

    class Arithmetic(__KeyMaker):
        """
        Арифметические операторы
        """

        # Параметры
        title = _('Арифметические операторы')

        ADD = 'add'
        SUB = 'sub'
        MUL = 'mul'
        DIV = 'div'
        POW = 'pow'
        MOD = 'mod'
        BITAND = 'bitand'
        BITOR = 'bitor'
        BITLEFTSHIFT = 'bitleftshift'
        BITRIGHTSHIFT = 'bitrightshift'

        ITEMS = (
            ADD,
            SUB,
            MUL,
            DIV,
            POW,
            MOD,
            BITAND,
            BITOR,
            BITLEFTSHIFT,
            BITRIGHTSHIFT,
        )

        CHOICES = (
            (ADD, _('Сложение'), Combinable.ADD, False),
            (SUB, _('Вычитание'), Combinable.SUB, False),
            (MUL, _('Умножение'), Combinable.MUL, False),
            (DIV, _('Деление'), Combinable.DIV, False),
            (POW, _('Возведение в степень'), Combinable.POW, False),
            (MOD, _('Деление по модулю'), Combinable.MOD, False),
            (BITAND, _('Побитовое И'), Combinable.BITAND, False),
            (BITOR, _('Побитовое ИЛИ'), Combinable.BITOR, False),
            (BITLEFTSHIFT, _('Побитовый сдвиг влево'), Combinable.BITLEFTSHIFT, False),
            (BITRIGHTSHIFT, _('Побитовый сдвиг вправо'), Combinable.BITRIGHTSHIFT, False),
        )

    class Date(__KeyMaker):
        """
        Функции работы со строками
        """

        # Параметры
        title = _('Функции работы со строками')
        # Использование в конкатенации
        is_concat = True

        YEAR = 'year'
        QUARTER = 'quarter'
        MONTH = 'month'
        WEEK = 'week'
        WEEK_DAY = 'week_day'
        DAY = 'day'
        HOUR = 'hour'
        MINUTE = 'minute'
        SECOND = 'second'

        ITEMS = (
            YEAR,
            QUARTER,
            MONTH,
            WEEK,
            WEEK_DAY,
            DAY,
            HOUR,
            MINUTE,
            SECOND,
        )

        CHOICES = (
            (YEAR, _('Год'), _('ГОД'), True),
            (QUARTER, _('Квартал'), _('КВРТАЛ'), True),
            (MONTH, _('Месяц'), _('МЕСЯЦ'), True),
            (WEEK, _('Неделя'), _('НЕДЕЛЯ'), True),
            (WEEK_DAY, _('День недели'), _('ДЕНЬ_НЕДЕЛИ'), True),
            (DAY, _('День'), _('ДЕНЬ'), True),
            (HOUR, _('Час'), _('ЧАС'), True),
            (MINUTE, _('Минута'), _('МИНУТА'), True),
            (SECOND, _('Секунда'), _('СЕКУНДА'), True),
        )

        FUNCTIONS = {
            YEAR: ExtractYear,
            QUARTER: ExtractQuarter,
            MONTH: ExtractMonth,
            WEEK: ExtractWeek,
            WEEK_DAY: ExtractWeekDay,
            DAY: ExtractDay,
            HOUR: ExtractHour,
            MINUTE: ExtractMinute,
            SECOND: ExtractSecond,
        }

    ITEMS = (
        String,
        Arithmetic,
        Date,
    )

    @classmethod
    def all_keys(cls):
        """
        Генерация всех ключей
        """
        keys = []
        for cls_item in cls.ITEMS:
            for item in cls_item.ITEMS:
                keys.append(cls_item.key(item))
        return keys

    @classmethod
    def create_tree_for_template(cls):
        """
        Сбор дерева для вывода в шаблоне
        """
        tree = []

        # Класс для ветки дерева
        # Аттрибуты:
        # - name - Наименование;
        # - title - Наименование в дереве;
        # - display_name - Наименование для переноса при построении запроса;
        # - is_editable - Редактируемая ли функция (добавление области для редактирования)
        # - tree_branches - Подветки;
        tree_branch_attrs = ('name', 'title', 'display_name', 'is_editable', 'tree_branches', 'has_subtree')
        tree_branch_class = namedtuple('TreeBranch', tree_branch_attrs)

        # Сбор дерева
        for item in cls.ITEMS:
            # Префикс функций
            prefix = hasattr(item, 'prefix') and item.prefix or item.__name__.lower()

            # Функции
            tree_branches = []
            for choice in item.CHOICES:
                name, *attrs = choice
                tree_branches.append(tree_branch_class(f'{prefix}:{name}', *attrs, None, False))
            tree.append(tree_branch_class(item.__name__.lower(), item.title, False, None, tree_branches, True))
        return tree

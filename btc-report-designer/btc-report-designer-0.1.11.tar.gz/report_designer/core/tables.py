import re
from io import StringIO

from django.db.models import QuerySet
from django.http import QueryDict
from django.utils.safestring import mark_safe

from report_designer.core.utils import RenderMixin, format_date, prepare_attrs


# region Миксины таблиц


class TablePartMethodsMixin:
    """
    Миксин с методами со вспомогательными методами для частей таблиц
    """

    def data_attrs(self, attrs: dict):
        """
        Подготовка data-аттрибутов
        :param attrs: Добавляемые аттрибуты
        """
        return prepare_attrs(attrs, 'data')


# endregion Миксины таблиц


# region Шапка таблицы


class HeaderItem:
    """
    Ячейка шапки таблицы
    """

    def __init__(self, name, col_span=None, row_span=None, css_class=None, ordering=None, **kwargs):
        """
        :param name: Название ячейки шапки
        :param col_span: Количествозанимаемых колонок
        :param row_span: Количество занимаемых строк
        """
        self.name = name
        self.col_span = col_span
        self.row_span = row_span
        self.css_class = css_class
        self.ordering = ordering


# endregion Шапка таблицы


# region Вспомогательный текст


class HelpText:
    """
    Класс вспомогательного текста для вывода вместе с таблицей
    """

    def __init__(self, text: str, classes: str = None):
        self.text = text
        self.classes = classes


# endregion Вспомогательный текст


# region Строки таблицы


class TableRow(TablePartMethodsMixin):
    """
    Строка таблицы
    """

    base_classes = ''

    def __init__(self, cells, object_id=None, classes='', data=None, **kwargs):
        self.cells = cells or []
        self.object_id = object_id
        self.additional_classes = classes
        self.additional_data = data

    def get_row_classes(self):
        """
        Получение классов для строки
        """
        classes = ' '.join([self.base_classes, self.additional_classes or ''])
        return re.sub(r'\s+', ' ', classes).strip()

    def data(self):
        """
        Data-параметры
        """
        return self.data_attrs(self.additional_data or {})

    def __len__(self):
        return len(self.cells)

    def __iter__(self):
        for cell in self.cells:
            yield cell


# endregion Строки таблицы


# region Ячейки таблицы


class CellType:
    """
    Базовый класс для типов ячеек работующих на основе форматирования значений
    """

    align = 'left'

    def __init__(self, cell):
        self.cell = cell

    def render(self):
        """
        Рендер ячейки в HTML
        """
        # Аттрибуты ячейки
        _cell_attrs = (
            ('class', self.cell.td_classes),
            ('col_span', self.cell.col_span),
            ('rowspan', self.cell.row_span),
            ('style', self.cell.style),
        )
        cell_attrs = ' '.join([f'{key}="{value}"' for key, value in _cell_attrs if value])

        # Аттрибуты ссылки, если есть
        _link_attrs = (
            ('href', self.cell.url),
            ('target', self.cell.target or '_self'),
            ('class', self.cell.link_class),
            ('style', 'display: block;'),
        )
        link_attrs = ' '.join([f'{key}="{value}"' for key, value in _link_attrs if value])
        value_part = ''.join(
            [
                self.cell.url and f'<a {link_attrs} {self.cell.link_html_attrs}>' or '',
                f'<div class="{self.cell.div_classes}">{self._format_value()}</div>',
                self.cell.url and '</a>' or '',
            ]
        )

        # Шаблон ячейки
        template = f'<td {cell_attrs} {self.cell.td_data_attrs}>{value_part}</td>'
        rendered_cell = StringIO()
        rendered_cell.write(template)
        cell_html = rendered_cell.getvalue()
        rendered_cell.close()
        return cell_html

    def _format_value(self):
        """
        Общее форматирование значения ячейки
        """
        return self.cell.value


class CellTypeDefault(CellType):
    """
    Тип ячейки по умолчанию
    """

    align = 'left'
    default_value = '&ndash;'

    def _format_value(self):
        return self.cell.value or self.default_value


class CellTypeCenter(CellTypeDefault):
    """
    Тип ячейки с выравниванием по центру
    """

    align = 'center'


class CellTypeDateTime(CellType):
    """
    Тип ячейки для вывода дат и лет с временем
    """

    align = 'center'

    def _format_value(self):
        return format_date(self.cell.value, format='d.m.Y в H:i') or '&ndash;'


class CellTypeDate(CellTypeCenter):
    """
    Тип ячейки для вывода дат и лет
    """

    align = 'center'

    def _format_value(self):
        return format_date(self.cell.value) or self.default_value


class CellTypeBoolean(CellTypeCenter):
    """
    Тип ячейки для вывода значения "Да"-"Нет"
    """

    def _format_value(self):
        return 'Да' if self.cell.value else 'Нет'


class CellTypeBooleanIcon(CellTypeCenter):
    """
    Тип ячейки для вывода булевого значения в виде значка
    """

    def _format_value(self):
        return mark_safe(f'<span class="rd-boolean-{str(self.cell.value).lower()}"></span>')


class CellTypeDeleteIcon(CellTypeCenter):
    """
    Тип ячейки для вывода корзинки удаления
    """

    def _format_value(self):
        return mark_safe('<a href="#" class="js-rd-ajax-load-modal-btn"><i class="glyphicon glyphicon-trash"></i></a>')


class CellTypeSortableIcon(CellTypeCenter):
    """
    Тип ячейки для вывода иконки сортировки
    """

    def _format_value(self):
        return '&equiv;'


class BaseCell:
    """
    Базовая ячейка таблицы
    """

    def __init__(
        self,
        value,
        align=None,
        col_span=None,
        row_span=None,
        cell_type=CellTypeDefault,
        bold=False,
        background_color=None,
        text_color=None,
        **kwargs,
    ):
        self.value = value
        self.cell_type = cell_type(self)
        self.col_span = col_span
        self.row_span = row_span
        self.background_color = background_color
        self.bold = bold
        self.text_color = text_color

        if not align:
            align = self.cell_type.align
        self.align = align

    def render(self):
        return self.cell_type.render()


class Cell(TablePartMethodsMixin, BaseCell):
    """
    Ячейка таблицы
    """

    def __init__(
        self,
        value,
        url=None,
        css_class=None,
        html_width=None,
        target=None,
        td_classes=None,
        **kwargs,
    ):
        self.url = url
        self.css_class = css_class
        self.html_width = html_width
        self.target = target

        super().__init__(value, **kwargs)

        self._td_data_attrs = kwargs.get('td_data_attrs', {})
        self._div_classes = kwargs.get('div_classes', '')
        self._link_html_attrs = kwargs.get('link_html_attrs', {})
        self.td_classes = td_classes
        self.link_class = kwargs.get('link_class', '')

    def __str__(self):
        return mark_safe(self.render())

    @property
    def style(self):
        """
        Стили ячейки
        """
        style = ''
        if self.html_width:
            style += f'width:{self.html_width}px;'
        if self.background_color:
            style += f'background-color:#{self.background_color};'
        return style

    @property
    def div_style(self):
        """
        Стили тега обертки значения
        """
        style = ''
        if self.text_color:
            style += f'color:#{self.text_color}; '
        return style

    @property
    def div_classes(self):
        """
        Классы тега обертки значения
        """
        if self.align:
            self._div_classes += f' text-{self.align.lower()}'
        if self.bold:
            self._div_classes += ' font_bold'
        return self._div_classes

    @property
    def td_data_attrs(self):
        """
        Data-атрибуты ячейки
        """
        return self.data_attrs(self._td_data_attrs)

    @property
    def link_html_attrs(self):
        """
        Метод для получения html-атрибутов для ссылки <a></a>
        """
        return prepare_attrs(self._link_html_attrs)


# endregion Ячейки таблицы


class AbstractTable(RenderMixin):
    """
    Таблица вывода выборки
    """

    template_name = 'report_designer/core/tables/table.html'

    header_class = HeaderItem
    row_class = TableRow
    cell_class = Cell

    context_object_name = 'table'

    # Аттрибуты таблицы
    base_classes = 'table table-hover'
    empty_message = 'Данные отсутствуют'

    # CSS класс пустой ячейки шапки таблицы
    css_empty_header_class = 'rd-table-empty-header'

    # Строки с удалением (необходимо либо в модели указать метод get_delete_url, либо переопределить метод)
    is_deleted = True

    # JS класс для включения сортировки таблицы
    js_sortable_class = ''
    js_sortable_icon_classes = 'js-rd-table-sortable'
    css_sortable_icon_classes = 'rd-table-sortable'
    sortable_column_width = 40
    delete_column_width = 40

    # CSS класс для заблокированной ячейки
    css_disabled_td_classes = 'rd-table-td-disabled'

    def __init__(self, queryset: QuerySet, request_get: QueryDict):
        self._queryset = queryset
        self._request_get = request_get

        # Параметры таблицы
        self._header = []
        self._rows = []
        self._help_text = []

    def create_table(self):
        """
        Создание таблицы
        """
        self._create_header()
        self._create_help_text()
        self.create_body()

    def _create_header(self):
        """
        Создание шапки таблицы
        """
        header = self.create_header(self.header_class)
        level_0, *levels = header

        # Пустая ячейка шапки таблицы
        empty_header = self.header_class(
            '',
            row_span=len(levels) + 1,
            css_class=self.css_empty_header_class,
        )
        level_0 = [
            *(self.js_sortable_class and [empty_header] or []),
            *level_0,
            *(self.is_deleted and [empty_header] or [])
        ]
        header = [
            level_0,
            *levels,
        ]
        self._header = header

    def create_body(self):
        """
        Формирование тела таблицы
        """
        for obj in self.get_queryset():
            row = self.create_row(obj)
            self._add_row(row)

    def create_row(self, obj):
        """
        Формирование строки тела таблицы
        """
        cells = [
            *(self.js_sortable_class and [self.create_sortable_cell(obj)] or []),
            *self.create_cells(obj),
            *(self.is_deleted and [self.create_deleted_cell(obj)] or []),
        ]
        return self.row_class(
            cells,
            object_id=obj.pk,
            classes=self.get_row_classes(obj),
            data=self.get_row_data_attrs(obj),
        )

    def create_sortable_cell(self, obj):
        """
        Создание ячейки сортировки
        """
        div_classes = ' '.join([
            *(self.request_get_is_empty and [self.js_sortable_icon_classes] or []),
            self.css_sortable_icon_classes,
        ])
        td_classes = ' '.join(not self.request_get_is_empty and [self.css_disabled_td_classes] or [])
        return self.cell_class(
            '',
            cell_type=CellTypeSortableIcon,
            html_width=self.sortable_column_width,
            div_classes=div_classes,
            td_classes=td_classes,
        )

    def create_deleted_cell(self, obj):
        """
        Создание ячейки удаления
        """
        url = hasattr(obj, 'get_delete_url') and obj.get_delete_url() or '#'
        return self.cell_class(
            '',
            cell_type=CellTypeDeleteIcon,
            html_width=self.delete_column_width,
            url=url,
        )

    def create_header(self, header):
        """
        Создание шапки таблицы
        """
        return []

    def _add_row(self, row):
        """
        Добавление строки
        """
        self._rows.append(row)

    def create_cells(self, obj):
        """
        Создание ячеек строки
        """
        return []

    def _create_help_text(self):
        """
        Создание подсказок для таблиц
        """
        if self.js_sortable_class and not self.request_get_is_empty:
            self.add_help_text(
                HelpText(text='Для изменения поряка полей необходимо сбросить фильтры', classes='alert alert-warning')
            )
        self.create_help_text()

    def create_help_text(self):
        """
        Создание подсказок для таблиц
        """
        pass

    def add_help_text(self, help_text: HelpText):
        """
        Добавление вспомогательного текста
        """
        self._help_text.append(help_text)

    def get_help_text(self):
        """
        Подсказки для таблицы
        """
        return self._help_text

    def get_queryset(self):
        """
        Выборка таблицы
        """
        return self._queryset

    def get_table_classes(self):
        """
        Получение классов для таблицы
        """
        return self.base_classes

    def get_row_classes(self, obj):
        """
        Получение классов для таблицы
        """
        return ''

    def get_row_data_attrs(self, obj):
        """
        Получение data-аттрибутов для строки
        """
        return {}

    @property
    def is_data_exists(self):
        """
        Есть ли данные в таблице
        """
        return bool(self._rows)

    @property
    def request_get_is_empty(self):
        """
        Проверка парамтеров запроса на сущестование
        """
        return not any(self._request_get.dict().values())

    def get_table_data_attrs(self):
        """
        Data-аттрибуты таблицы
        """
        return {}

    def get_context_data(self):
        context_data = super().get_context_data()
        context_data.update(
            {
                'empty_message': self.empty_message,
                'header': self._header,
                'rows': self._rows,
                'classes': self.get_table_classes(),
                'request_get_is_empty': self.request_get_is_empty,
                'sortable_class': self.js_sortable_class,
                'help_text': self.get_help_text(),
                'table_data_attrs': prepare_attrs(self.get_table_data_attrs(), 'data'),
            }
        )
        return context_data

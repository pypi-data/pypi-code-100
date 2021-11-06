from copy import copy

from django.conf import settings
from django.forms import Select, NullBooleanSelect, ModelForm, ModelChoiceField

from report_designer.core.utils import RenderMixin


class FormFields:
    """
    Коллекция стилей/типов полей формы
    """

    TEXT_INPUT = 'TextInput'
    SELECT = 'Select'
    DATE_INPUT = 'DateInput'
    NUMBER_INPUT = 'NumberInput'
    TEXT_AREA = 'Textarea'
    CHECKBOX_INPUT = 'CheckboxInput'

    WIDGET_CLASSES = (
        TEXT_INPUT,
        SELECT,
        DATE_INPUT,
        NUMBER_INPUT,
        TEXT_AREA,
        CHECKBOX_INPUT,
    )

    DISABLE_FIELDS_CSS = (
        (TEXT_INPUT, 'disabled-input'),
        (TEXT_AREA, 'disabled-input'),
        (DATE_INPUT, 'disabled-input'),
        (NUMBER_INPUT, 'disabled-input'),
        (CHECKBOX_INPUT, 'disabled-input'),
        (SELECT, 'disabled-select'),
    )

    @classmethod
    def get_base_class(cls, field_widget):
        """
        Метод для получения базового классов виджета
        :param field_widget: Widget
        :return: str
        """
        base_class = None
        if field_widget:
            base_classes = [fidget_class.__name__ for fidget_class in field_widget.__class__.__mro__]
            classes_intersection = set(cls.WIDGET_CLASSES) & set(base_classes)
            if classes_intersection:
                base_class = classes_intersection.pop()
        return base_class

    @classmethod
    def get_css_for_disabled_field(cls, field_widget):
        """
        Метод для получения css-класс заблокированного поля по его типу
        :param field_widget: Widget
        :return: str
        """
        widget_class = cls.get_base_class(field_widget)
        return dict(cls.DISABLE_FIELDS_CSS).get(widget_class, '')


class StyledFormMixin:
    """
    Миксин стилизации форм
    """

    js_class_prefix = 'js-rd-field'
    field_css_class = 'input__input'
    empty_choice_label = 'Не выбрано'
    searching_select = ()
    select_id_prefix = None

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        # Поля формы
        self.form_fields = self.get_form_fields()

        # Установка базовых классов виджетов
        self.init_processing_fields()

    def init_processing_fields(self):
        """
        Обработка полей при инициализации
        """
        for field_name, field in self.form_fields.items():
            self.init_processing_field(field_name, field)

    def init_processing_field(self, field_name, field):
        """
        Обработка поля при инициализации
        """
        widget_type = field.widget.__class__.__name__.lower()
        field_classes = (
            f'{self.js_class_prefix}_{field_name}',
            f'{self.field_css_class} {self.field_css_class}_{widget_type}',
        )
        self.set_widget_class(field_name, field_classes)

        # Выпадающие списки
        if isinstance(field.widget, Select):
            # Установка пустого значения для Select
            if hasattr(field, 'empty_label') and field.empty_label is not None:
                field.empty_label = self.empty_choice_label
                self.add_or_update_widget_attr(field_name, 'data-empty-label', self.empty_choice_label)
            # Поиск
            if field_name in self.searching_select:
                self.set_widget_class(field_name, 'js-rd-select-search')

            # Префикс айди
            if self.select_id_prefix:
                self.add_or_update_widget_attr(field_name, 'id', f'id_{self.select_id_prefix}_{field_name}')

        # Выпадающие списки с булевыми значениями
        if isinstance(field.widget, NullBooleanSelect):
            if hasattr(settings, 'NULL_BOOLEAN_CHOICES'):
                field.widget.choices = settings.NULL_BOOLEAN_CHOICES

        # Если поле ModelChoiceField
        if isinstance(field, ModelChoiceField):
            is_default_label_instance = getattr(field, 'is_default_label_instance', True)
            # Метод должен быть @classmethod
            label_for_instance_method = getattr(field.queryset.model, 'label_for_instance', None)
            if is_default_label_instance and label_for_instance_method:
                field.label_from_instance = copy(label_for_instance_method)

    def set_widget_class(self, field, value):
        """
        Установка класса виджету поля
        """
        self.add_or_update_widget_attr(field, 'class', value)

    def disable_fields(self, *fields, by_css_class_only=False):
        """
        Метод для блокировки списка полей
        """
        for field_name in fields:
            field = self.form_fields[field_name]
            self.set_widget_class(field_name, FormFields.get_css_for_disabled_field(field.widget))
            if by_css_class_only:
                field.disabled = True

    def add_or_update_widget_attr(self, field, attr, value, joiner=' '):
        """
        Добавление или обновление аттрибута виджета поля
        """
        attrs = self.form_fields[field].widget.attrs
        value = isinstance(value, (list, tuple)) and value or [value]
        self.update_widget_attr(field, attr, f'{joiner}'.join(filter(None, [attrs.get(attr), *value])))

    def update_widget_attr(self, field, attr, value):
        """
        Обновление аттрибута виджета поля
        """
        self.form_fields[field].widget.attrs.update({attr: value})

    def update_widgets_attr(self, *fields, attr=None, value=None):
        """
        Обновление аттрибута виджета поля
        """
        if not attr:
            raise AttributeError('Необходимо наименование аттрибута')
        for field in fields:
            self.update_widget_attr(field, attr, value)

    def set_fields_attr(self, *fields, attr=None, value=None):
        """
        Установка аттрибута полям формы
        """
        if not attr:
            raise AttributeError('Необходимо наименование аттрибута')
        for field in fields:
            self.set_field_attr(field, attr, value)

    def set_field_attr(self, field, attr, value):
        """
        Установка аттрибута полю формы
        """
        setattr(self.form_fields[field], attr, value)

    def get_form_fields(self):
        """
        Получение полей формы
        """
        return self.fields.copy()


class CustomStyledModelForm(RenderMixin, StyledFormMixin, ModelForm):
    """
    Кастомный StyledModelForm
    """

    context_object_name = 'form'

    @property
    def instance_exists(self):
        """
        Проверка на существование instance
        """
        return self.instance and self.instance.id

    def get_foreign_value_from_parent(self, name, parent_field):
        """
        Получение значений из родительской формы для foreign key
        """
        if not self.data:
            if not self.instance_exists:
                return
            parent_value = getattr(self.instance, parent_field, None)
            return getattr(parent_value, name, None)

        value = self.data.get(name)
        if not value:
            return

        parent_model = self._meta.model._meta.get_field(parent_field).remote_field.model
        value_model = parent_model._meta.get_field(name).remote_field.model
        return value_model.objects.filter(pk=value).first()

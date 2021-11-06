from django.forms import ModelForm

from report_designer.core.forms import StyledFormMixin
from report_designer.models import DBTable, TableField


class DBTableBaseForm(StyledFormMixin, ModelForm):
    """
    Базовая форма: Таблица БД
    """

    class Meta:
        model = DBTable
        fields = (
            'alias',
            'is_visible',
        )


class DBTableCreateForm(DBTableBaseForm):
    """
    Форма: создание таблиц БД
    """

    searching_select = (
        'table',
    )

    class Meta(DBTableBaseForm.Meta):
        fields = (
            'table',
            *DBTableBaseForm.Meta.fields,
        )


class DBTableUpdateForm(DBTableBaseForm):
    """
    Форма: редактирование таблиц БД
    """

    pass


class TableFieldUpdateForm(StyledFormMixin, ModelForm):
    """
    Форма: редактирование поле таблицы БД
    """

    class Meta:
        model = TableField
        fields = (
            'alias',
            'representation',
            'is_visible',
        )

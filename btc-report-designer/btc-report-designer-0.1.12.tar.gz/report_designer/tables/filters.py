from report_designer.core.filters import (
    SearchBaseFilterSet,
    StyledFilterSet,
)
from report_designer.models import (
    DBTable,
    TableField,
)


class DBTableFilterSet(StyledFilterSet, SearchBaseFilterSet):
    """
    Фильтр: Таблицы БД
    """

    searching_fields = ('alias',)
    searching_select = ('table',)

    class Meta:
        model = DBTable
        fields = (
            'table',
            'is_visible',
        )


class DBTableFieldsFilterSet(StyledFilterSet, SearchBaseFilterSet):
    """
    Фильтр: Поля таблицы БД
    """

    searching_fields = (
        'alias',
        'name',
    )
    searching_select = ('representation',)

    class Meta:
        model = TableField
        fields = (
            'representation',
            'is_visible',
            'is_relation',
        )

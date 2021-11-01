from report_designer.core.filters import StyledFilterSet, SearchBaseFilterSet
from report_designer.models import Report, ReportField, ReportTableRelation


class ReportFilterSet(StyledFilterSet, SearchBaseFilterSet):
    """
    Фильтр: Отчеты
    """

    searching_fields = ('name',)
    searching_select = (
        'root',
        'author',
    )

    class Meta:
        model = Report
        fields = (
            'root',
            'author',
            'groups',
        )


class ReportFieldsFilterSet(StyledFilterSet, SearchBaseFilterSet):
    """
    Фильтр: Поля таблицы отчета
    """

    searching_fields = (
        'alias',
        'name',
    )
    searching_select = ('representation',)

    class Meta:
        model = ReportField
        fields = (
            'is_virtual',
            'is_group',
            'is_sort',
            'reverse_sort',
            'is_aggregate',
        )


class ReportTableRelationFilterSet(StyledFilterSet, SearchBaseFilterSet):
    """
    Фильтр: Связи таблиц отчета
    """

    searching_fields = (
        'name',
        'parent__name',
    )
    searching_select = ('report_table',)

    class Meta:
        model = ReportTableRelation
        fields = ('report_table',)

    def __init__(self, *args, **kwargs):
        report = kwargs.pop('report', None)
        super().__init__(*args, **kwargs)
        self.set_field_attr('report_table', 'queryset', report.report_tables.exclude(db_table=report.root))

from report_designer.core.filters import StyledFilterSet, SearchBaseFilterSet


class ReportGroupFilterSet(StyledFilterSet, SearchBaseFilterSet):
    """
    Фильтр: Группы отчетов
    """

    searching_fields = ('name',)

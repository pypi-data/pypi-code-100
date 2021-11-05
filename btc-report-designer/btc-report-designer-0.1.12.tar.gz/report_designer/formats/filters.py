from report_designer.core.filters import (StyledFilterSet, SearchBaseFilterSet,)
from report_designer.models import Format


class FormatFilterSet(StyledFilterSet, SearchBaseFilterSet):
    """
    Фильтр: Форматы
    """

    searching_fields = ('name',)
    searching_select = (
        'internal_type',
    )

    class Meta:
        model = Format
        fields = (
            'internal_type',
        )

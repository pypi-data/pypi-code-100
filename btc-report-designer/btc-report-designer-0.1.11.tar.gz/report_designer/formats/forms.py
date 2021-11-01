from django.forms import ModelForm

from report_designer.core.forms import StyledFormMixin
from report_designer.models import Format


class FormatCreateUpdateForm(StyledFormMixin, ModelForm):
    """
    Форма: создание форматов
    """

    searching_select = (
        'internal_type',
    )

    class Meta:
        model = Format
        fields = (
            'name',
            'internal_type',
            'representation',
        )

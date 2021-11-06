from django.forms import ModelForm

from report_designer.core.forms import StyledFormMixin
from report_designer.models import ReportGroup


class ReportGroupCreateUpdateForm(StyledFormMixin, ModelForm):
    """
    Форма: создание группы отчетов
    """

    class Meta:
        model = ReportGroup
        fields = (
            'name',
        )

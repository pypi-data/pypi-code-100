from report_designer.core.views import (
    DynamicContentTableBaseView,
    CreateAjaxView,
    UpdateAjaxView,
    BreadcrumbsListMixin,
)
from report_designer.formats.actions import FormatListActionGroup
from report_designer.formats.filters import FormatFilterSet
from report_designer.formats.forms import FormatCreateUpdateForm
from report_designer.formats.tables import FormatTable
from report_designer.models import Format


# endregion Базовые миксины


class FormatBreadcrumbsListMixin(BreadcrumbsListMixin):
    """
    Хлебные крошки форматов
    """

    title_breadcrumb = 'Список форматов'


# endregion Базовые миксины


class FormatListView(FormatBreadcrumbsListMixin, DynamicContentTableBaseView):
    """
    Представление: Список форматов
    """

    model = Format
    filterset_class = FormatFilterSet
    table_class = FormatTable
    title = 'Форматы'
    ajax_content_name = 'formats'
    action_group_classes = (FormatListActionGroup,)


class FormatCreateUpdateMixin:
    """
    Миксин создания / редактирования форматов
    """

    model = Format
    form_class = FormatCreateUpdateForm
    dependents = (
        ('dynamic_contents', 'formats'),
    )
    is_only_ajax = True


class FormatCreateView(FormatCreateUpdateMixin, CreateAjaxView):
    """
    Представление: Создание формата
    """

    title = 'Создание формата'


class FormatUpdateView(FormatCreateUpdateMixin, UpdateAjaxView):
    """
    Представление: Редактирование формата
    """

    title = 'Редактирование формата'

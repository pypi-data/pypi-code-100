from report_designer.core.views import (
    BreadcrumbsListMixin,
    DynamicContentTableBaseView,
    UpdateAjaxView,
    CreateAjaxView,
)
from report_designer.groups.actions import ReportGroupListActionGroup
from report_designer.groups.filters import ReportGroupFilterSet
from report_designer.groups.forms import ReportGroupCreateUpdateForm
from report_designer.groups.tables import ReportGroupTable
from report_designer.models import ReportGroup


# region Базовые миксины


class ReportGroupBreadcrumbsListMixin(BreadcrumbsListMixin):
    """
    Хлебные крошки групп отчетов
    """

    title_breadcrumb = 'Список групп отчетов'


# endregion Базовые миксины


# region Список групп отчетов


class ReportGroupListView(ReportGroupBreadcrumbsListMixin, DynamicContentTableBaseView):
    """
    Представление: Список групп отчетов
    """

    model = ReportGroup
    filterset_class = ReportGroupFilterSet
    table_class = ReportGroupTable
    title = 'Группы отчетов'
    ajax_content_name = 'report_groups'
    action_group_classes = (ReportGroupListActionGroup,)
    filters_clear = False


# endregion Список групп отчетов


# region Создание / редактирование групп отчетов


class ReportGroupCreateUpdateMixin:
    """
    Миксин создания / редактирования группы отчетов
    """

    model = ReportGroup
    form_class = ReportGroupCreateUpdateForm
    dependents = (
        ('dynamic_contents', 'report_groups'),
    )
    is_only_ajax = True


class ReportGroupCreateView(ReportGroupCreateUpdateMixin, CreateAjaxView):
    """
    Представление: Создание группы отчетов
    """

    title = 'Создание группы отчетов'


class ReportGroupUpdateView(ReportGroupCreateUpdateMixin, UpdateAjaxView):
    """
    Представление: Редактирование граппы отчетов
    """

    title = 'Редактирование группы отчетов'


# endregion Создание / редактирование групп отчетов

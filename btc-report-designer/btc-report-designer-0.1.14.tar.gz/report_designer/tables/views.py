from django.views.generic import DetailView

from report_designer.core.views import (
    DynamicContentTableBaseView,
    CreateAjaxView,
    TitleMixin,
    ParentMixin,
    UpdateAjaxView,
    ActionGroupMixin,
    BreadcrumbsListMixin,
    BreadcrumbsDetailMixin,
    BackUrlDetailMixin,
)
from report_designer.models import DBTable, TableField
from report_designer.tables.actions import (
    TablesListActionGroup,
    TableDropdownActionGroup,
)
from report_designer.tables.filters import (
    DBTableFilterSet,
    DBTableFieldsFilterSet,
)
from report_designer.tables.forms import (
    DBTableCreateForm,
    TableFieldUpdateForm,
    DBTableUpdateForm,
)
from report_designer.tables.tables import (
    DBTablesTable,
    TableFieldsTable,
)


# endregion Базовые миксины


class DBTableBreadcrumbsListMixin(BreadcrumbsListMixin):
    """
    Хлебные крошки таблиц БД
    """

    title_breadcrumb = 'Список таблиц БД'


class DBTableBreadcrumbsDetailBaseMixin(BreadcrumbsDetailMixin, DBTableBreadcrumbsListMixin):
    """
    Хлебные крошки таблицы БД
    """

    pass


# endregion Базовые миксины


class DBTableListView(DBTableBreadcrumbsListMixin, DynamicContentTableBaseView):
    """
    Представление: Список добавленных таблиц БД
    """

    title = 'Таблицы БД'
    model = DBTable
    table_class = DBTablesTable
    filterset_class = DBTableFilterSet
    ajax_content_name = 'db_tables'
    action_group_classes = (TablesListActionGroup,)


class DBTableCreateUpdateMixin:
    """
    Миксин создания / редактирования таблицы БД
    """

    model = DBTable

    def get_success_redirect_url(self):
        return self.object.get_detail_url()


class DBTableCreateView(DBTableCreateUpdateMixin, CreateAjaxView):
    """
    Представление: Создание таблицы БД
    """

    title = 'Создание таблицы БД'
    form_class = DBTableCreateForm

    def after_save(self, **kwargs):
        super().after_save(**kwargs)
        self.object.reload_fields()


class DBTableUpdateView(DBTableCreateUpdateMixin, UpdateAjaxView):
    """
    Представление: Редактирование таблицы БД
    """

    title = 'Редактирование таблицы БД'
    form_class = DBTableUpdateForm


class DBTableDetailView(
    BackUrlDetailMixin,
    DBTableBreadcrumbsDetailBaseMixin,
    ActionGroupMixin,
    TitleMixin,
    DetailView,
):
    """
    Представление: Просмотр таблицы БД
    """

    model = DBTable
    template_name = 'report_designer/tables/detail.html'
    context_object_name = 'db_table'
    action_group_classes = (TableDropdownActionGroup,)

    def get_title(self):
        return f'Таблица БД "{self.object.alias}"'


class TableFieldsListView(ParentMixin, DynamicContentTableBaseView):
    """
    Представление: Список полей таблицы БД
    """

    model = TableField
    parent_model = DBTable
    parent_field = 'db_table'
    table_class = TableFieldsTable
    filterset_class = DBTableFieldsFilterSet
    ajax_content_name = 'db_table_fields'

    def get_content_url_kwargs(self):
        content_url_kwargs = super().get_content_url_kwargs()
        content_url_kwargs.update(pk=self.parent.pk)
        return content_url_kwargs


class TableFieldUpdateView(UpdateAjaxView):
    """
    Представление: Создание таблицы БД
    """

    title = 'Редактирование поля таблицы БД'
    model = TableField
    form_class = TableFieldUpdateForm
    dependents = (
        ('dynamic_contents', 'db_table_fields'),
    )

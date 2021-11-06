from django.urls import reverse_lazy

from report_designer.core.actions import (
    ActionGroup,
    SimpleModalAction,
    DropdownActionGroup,
    UpdateDropdownModalAction,
)


class TablesListActionGroup(ActionGroup):
    """
    Группа действий в списке таблиц
    """

    create = SimpleModalAction(title='Добавить', url=reverse_lazy('report_designer:tables:create'))


class TableDropdownActionGroup(DropdownActionGroup):
    """
    Выпадающий список для претензионного дела
    """

    edit = UpdateDropdownModalAction(title='Редактировать основную информацию')

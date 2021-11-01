from report_designer.core.tables import (
    AbstractTable,
    CellTypeCenter,
    CellTypeBooleanIcon,
)


class DBTablesTable(AbstractTable):
    """
    Таблица списка таблиц базы данных
    """

    def create_header(self, header):
        level_0 = [
            header('Таблицы БД'),
            header('Псевдоним'),
            header('Отображать в конструкторе'),
        ]
        return [level_0]

    def create_cells(self, obj):
        cell = self.cell_class
        url = obj.get_detail_url()
        return [
            cell(obj.table, url=url, cell_type=CellTypeCenter),
            cell(obj.alias, url=url, cell_type=CellTypeCenter),
            cell(obj.is_visible, url=url, cell_type=CellTypeBooleanIcon),
        ]


class TableFieldsTable(AbstractTable):
    """
    Таблица списка полей таблицы
    """

    def create_header(self, header):
        level_0 = [
            header('Наименование'),
            header('Псевдоним'),
            header('Представление'),
            header('Отображение'),
            header('Связанное поле'),
        ]
        return [level_0]

    def create_cells(self, obj):
        cell = self.cell_class
        base_attrs = {'link_class': 'js-rd-ajax-load-modal-btn', 'url': obj.get_edit_url()}
        return [
            cell(obj.name, cell_type=CellTypeCenter, **base_attrs),
            cell(obj.alias, cell_type=CellTypeCenter, **base_attrs),
            cell(obj.representation and obj.representation.name or None, cell_type=CellTypeCenter, **base_attrs),
            cell(obj.is_visible, cell_type=CellTypeBooleanIcon, **base_attrs),
            cell(obj.is_relation, cell_type=CellTypeBooleanIcon, **base_attrs),
        ]

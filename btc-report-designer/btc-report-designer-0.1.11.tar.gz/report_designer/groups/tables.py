from report_designer.core.tables import AbstractTable, CellTypeCenter


class ReportGroupTable(AbstractTable):
    """
    Таблица списка групп отчетов
    """

    def create_header(self, header):
        level_0 = [
            header('Наименование'),
            header('Количество отчетов в группе'),
        ]
        return [level_0]

    def create_cells(self, obj):
        cell = self.cell_class
        base_attrs = {
            'link_class': 'js-rd-ajax-load-modal-btn',
            'url': obj.get_edit_url(),
        }
        return [
            cell(obj.name, cell_type=CellTypeCenter, **base_attrs),
            cell(obj.reports_count, cell_type=CellTypeCenter, **base_attrs),
        ]

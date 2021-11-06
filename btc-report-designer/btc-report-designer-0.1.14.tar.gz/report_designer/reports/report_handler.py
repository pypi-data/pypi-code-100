from django.db import transaction

from report_designer.models import (
    Report,
    ReportTable,
    ReportTableRelation,
    ReportTableRelationCondition,
    ReportField,
    ReportFieldRelation
)


class ReportCloneHandler:
    """
    Обработчик клонирования отчета по другому отчету
    """

    def __init__(self, report_from: Report, report_to: Report) -> None:
        super().__init__()
        self.report_from: Report = report_from
        self.report_to: Report = report_to

        self.relation_map = {}

    @transaction.atomic
    def run(self) -> None:
        self._create_tables()

    def _create_tables(self):
        """
        Клонирование таблиц
        """
        for table in self.report_from.report_tables.prefetch_related('relations').all():
            new_table = ReportTable.objects.create(
                report=self.report_to,
                db_table=table.db_table,
                is_root=table.is_root,
                order=table.order
            )
            self._create_relations(table, new_table)
        self._create_report_fields()

    def _create_relations(self, table_from: ReportTable, table_to: ReportTable):
        """
        Создание "Связь до таблицы отчета"
        """
        for relation in table_from.relations.all().order_by('-parent', 'pk'):
            new_relation = ReportTableRelation.objects.create(
                report_table=table_to,
                parent=relation.parent,  # todo: проверить!
                name=relation.name
            )
            self._create_conditions(relation, new_relation)

    def _create_conditions(self, relation_from: ReportTableRelation, relation_to: ReportTableRelation):
        """
        Создание "Условие связи таблицы отчета"
        """
        for condition in relation_from.from_report_table_relations.all():
            new_condition = ReportTableRelationCondition.objects.create(
                report_table_relation=relation_to,
                from_field=condition.from_field,
                to_field=condition.to_field,
                order=condition.order,
            )
            self.relation_map.update({condition.pk: new_condition.pk})

    def _create_report_fields(self):
        """
        Создание "Поле отчета"
        """
        report_field_relation_list = []

        for report_field in self.report_from.report_fields.all():
            report_field = ReportField.objects.create(
                report=self.report_to,
                field=report_field.field,
                report_table_relation=self.relation_map.get(getattr(report_field.report_table_relation, 'pk', None), None),
                expression_attrs=report_field.expression_attrs,
                internal_type=report_field.internal_type,
                is_virtual=report_field.is_virtual,
                is_group=report_field.is_group,
                is_sort=report_field.is_sort,
                reverse_sort=report_field.reverse_sort,
                is_aggregate=report_field.is_aggregate,
                aggregate_function=report_field.aggregate_function,
                order=report_field.order,
                name=report_field.name,
                alias=report_field.alias,
                representation=report_field.representation,
            )
            report_field.relations.add(*report_field.relations.all())

            for report_field_relation in ReportFieldRelation.objects.filter(report_field=report_field):
                report_field_relation_list.append(ReportFieldRelation(
                    report_field=report_field,
                    table_field=report_field_relation.table_field,
                    order=report_field_relation.order,
                ))
        ReportFieldRelation.objects.bulk_create(report_field_relation_list)

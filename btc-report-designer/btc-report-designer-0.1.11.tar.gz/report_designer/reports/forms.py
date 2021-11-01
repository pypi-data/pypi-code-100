from django.core.exceptions import ValidationError
from django.urls import reverse_lazy

from report_designer.core.forms import CustomStyledModelForm
from report_designer.core.formsets import FormsetManager, CustomBaseInlineFormSet
from report_designer.models import (
    Report,
    ReportTableRelation,
    ReportTableRelationCondition,
    TableField,
    ReportField,
)


# region Отчет


class ReportBaseForm(CustomStyledModelForm):
    """
    Базовая форма отчета
    """

    searching_select = (
        'root',
        'groups',
    )

    class Meta:
        model = Report
        fields = (
            'name',
            'groups',
            'is_visible_in_reports',
        )


class ReportCreateForm(ReportBaseForm):
    """
    Форма: создание отчета
    """

    class Meta(ReportBaseForm.Meta):
        fields = (
            'name',
            'root',
            'groups',
            'is_visible_in_reports',
        )


class ReportUpdateForm(ReportBaseForm):
    """
    Форма: редактирование отчета
    """

    pass


# region Отчет


# region Условия связи таблиц отчета


class ReportTableRelationCreateUpdateForm(CustomStyledModelForm):
    """
    Форма: создание связи до таблицы отчета
    """

    class Meta:
        model = ReportTableRelation
        fields = (
            'name',
            'parent',
            'report_table',
        )

    def __init__(self, *args, **kwargs):
        report = kwargs.pop('report', None)
        super().__init__(*args, **kwargs)

        # Блокировка полей родительской связи и таблицы при редактировании
        if self.instance_exists:
            self.disable_fields('parent', 'report_table')
        else:
            # Установка url для полей выбора полей
            url = reverse_lazy('report_designer:reports:select2-fields-list', kwargs={'pk': report.pk})
            self.update_widgets_attr('parent', 'report_table', attr='data-fields-url', value=url)

            # Установка зависимого поля
            self.update_widget_attr('parent', 'data-target-field', 'from_field')
            self.update_widget_attr('report_table', 'data-target-field', 'to_field')

            # Установка наименования GET параметра
            self.update_widget_attr('parent', 'data-query-name', 'relation')
            self.update_widget_attr('report_table', 'data-query-name', 'table')

            # Установка выборок
            self.set_field_attr(
                'parent',
                'queryset',
                ReportTableRelation.objects.filter(report_table__report=report).distinct(),
            )
            self.set_field_attr('report_table', 'queryset', report.report_tables.exclude(db_table_id=report.root.pk))

    @property
    def is_selected_parent(self):
        """
        Пустое поле родительской связи
        """
        if self.instance_exists:
            return bool(self.instance.parent)
        return bool(self.data.get('parent'))


class ReportTableRelationConditionForm(CustomStyledModelForm):
    """
    Форма: условие связи таблицы отчета
    """

    template_name = 'report_designer/reports/blocks/create_table_relation_condition.html'

    class Meta:
        model = ReportTableRelationCondition
        fields = (
            'from_field',
            'to_field',
        )

    def __init__(self, *args, **kwargs):
        report = kwargs.pop('report', None)
        super().__init__(*args, **kwargs)

        # Установка
        parent = self.get_foreign_value_from_parent('parent', 'report_table_relation')
        parent_tables_queryset = (
            parent and parent.report_table.db_table.fields.all() or TableField.objects.filter(db_table=report.root)
        )
        self.set_field_attr('from_field', 'queryset', parent_tables_queryset)

        report_table = self.get_foreign_value_from_parent('report_table', 'report_table_relation')
        report_table_tables_queryset = report_table and report_table.db_table.fields.all() or TableField.objects.none()
        self.set_field_attr('to_field', 'queryset', report_table_tables_queryset)

    def has_changed(self):
        return not self.instance_exists or super().has_changed()


class ReportTableRelationConditionFormSet(CustomBaseInlineFormSet):
    """
    Формсет: условия связи таблицы отчета
    """

    css_forms_container = 'block-gray conditions'
    css_header = 'conditions-header'

    def clean(self):
        super().clean()
        if self.is_empty:
            raise ValidationError('Необходимо добавить хотя бы одно условие связи')


class ReportTableRelationConditionsFormsetManager(FormsetManager):
    """
    Менеджер формсета: Условия связи таблицы отчета
    """

    min_num = 1
    title = 'Условия связи'
    name = 'relation_conditions'
    parent_model = ReportTableRelation
    model = ReportTableRelationCondition
    custom_form = ReportTableRelationConditionForm
    custom_formset = ReportTableRelationConditionFormSet


# endregion Условия связи таблиц отчета


# region Поля шаблона


class ReportFieldUpdateForm(CustomStyledModelForm):
    """
    Форма: редактирование поля
    """

    searching_select = (
        'representation',
        'report_table_relation',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not (self.data.get('is_sort') or self.instance.is_sort):
            self.disable_fields('reverse_sort')

        if not (self.data.get('is_aggregate') or self.instance.is_aggregate):
            self.disable_fields('aggregate_function')

    class Meta:
        model = ReportField
        fields = (
            'alias',
            'representation',
            'report_table_relation',
            'is_group',
            'is_sort',
            'reverse_sort',
            'is_aggregate',
            'aggregate_function',
        )

    @property
    def is_group_field(self):
        """
        Поле помечено, как групповое
        """
        return 'is_group' in self.changed_data and self.data and self.data.get('is_group', False)

    def clean(self):
        super().clean()

        # Для агрегированных полей необходимо указать функцию агрегирования
        is_aggregate = self.cleaned_data.get('is_aggregate')
        aggregate_function = self.cleaned_data.get('aggregate_function')

        if is_aggregate and not aggregate_function:
            self.add_error('aggregate_function', 'Обязательно для агрегированных полей')
        return self.cleaned_data

# endregion Поля шаблона

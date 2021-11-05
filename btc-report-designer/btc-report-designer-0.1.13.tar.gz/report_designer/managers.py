from django.core.exceptions import FieldDoesNotExist
from django.db.models import (
    QuerySet,
    Prefetch,
    BooleanField,
    Value,
    When,
    Case,
    F,
    ForeignKey,
    ManyToManyField,
    CharField,
    OuterRef,
    Subquery,
)

from report_designer.consts import InternalType


class BaseIsVisibleQuerySet(QuerySet):
    """
    QuerySet видимых в констркуторе сущностей
    """

    is_visible_field = 'is_visible'

    def is_visible(self):
        """
        Видимые сущности
        """
        return self.filter(**{self.is_visible_field: True})


class TableFieldQuerySet(BaseIsVisibleQuerySet):
    """
    QuerySet полей таблиц БД
    """

    def available_for_report(self, report):
        """
        Поля доступные для отчета
        """
        return self.is_visible().filter(db_table__report_tables__report=report).distinct()

    def is_relation(self):
        """
        Поля связи
        """
        return self.filter(is_relation=True)

    def is_not_relation(self):
        """
        Поля связи
        """
        return self.filter(is_relation=False)

    def with_title(self):
        """
        Заполнение псевдонима из названия, если не указан псевдоним
        """
        return self.annotate(title=Case(When(alias__exact='', then=F('name')), default=F('alias')))

    def with_related_tables(self, db_table):
        """
        Поля таблицы с аннотацией ID таблицы для полей со связью
        """
        from .models import DBTable

        # Поля таблицы
        fields = self.is_visible()

        # Метакласс реальной таблицы
        db_table_meta_class = db_table.table.model_class()._meta

        # Получение аттрибутов таблиц связанных полей
        app_labels, model_names = [], []
        for field_pk, field_name in fields.values_list('pk', 'db_field'):
            try:
                field = db_table_meta_class.get_field(field_name)
            except FieldDoesNotExist:
                continue

            # Если поле связанное и имеет тип ForeignKey
            if field.is_relation and isinstance(field, (ForeignKey, ManyToManyField)):
                related_model_meta = field.related_model._meta
                app_labels.append(When(pk=field_pk, then=Value(related_model_meta.app_label)))
                model_names.append(When(pk=field_pk, then=Value(related_model_meta.model_name)))

        # Аннотация параметров связанных таблиц
        fields = fields.annotate(
            app_label=Case(*app_labels, output_field=CharField(), default=Value(None)),
            model_name=Case(*model_names, output_field=CharField(), default=Value(None)),
        )
        # Аннотация флага существования таблицы в системе и фильтрация
        subquery = DBTable.objects.filter(
            table__app_label=OuterRef('app_label'), table__model=OuterRef('model_name')
        )
        fields = fields.annotate(related_table_pk=Subquery(subquery.values('pk')[:1]))
        # Удаление аннотаций (фикс бага группировки)
        fields.query.annotations.pop('app_label', None)
        fields.query.annotations.pop('model_name', None)
        return fields


class DBTableQuerySet(BaseIsVisibleQuerySet):
    """
    QuerySet таблиц БД
    """

    def available(self, is_relation=False):
        """
        Доступные для выбора таблицы

        Таблицы попадаюбт в выборку:
        - если отображаются в конструкторе
        - если имеют поля, отображаемые в конструкторе
        """
        from report_designer.models import TableField

        tables = self.is_visible().filter(fields__is_visible=True)
        prefetch = Prefetch('fields', TableField.objects.is_visible().filter(is_relation=is_relation))
        return tables.prefetch_related(prefetch).distinct()

    def for_report(self, report):
        """
        Таблицы отчета
        """
        return (
            self.filter(report_tables__report=report)
            .order_by('report_tables__order')
            .distinct()
        )


class FormatQuerySet(BaseIsVisibleQuerySet):
    """
    QuerySet форматов
    """

    def available_for_field(self, table, field):
        """
        Список допустимых форматов для поля модели
        """
        choice_name = table.model_class()._meta.get_field(field).get_internal_type()
        internal_type = InternalType.get_value_by_internal_type(choice_name)
        return self.filter(internal_type=internal_type)


class ReportFieldQuerySet(QuerySet):
    """
    QuerySet полей отчета
    """

    def with_relation(self):
        """
        Поля, имеющие связь
        """
        return self.filter(relation__isnull=False)

    def without_relation(self):
        """
        Поля, не имеющие связь
        """
        return self.filter(relation__isnull=True)

    def is_virtual(self):
        """
        Виртуальные поля
        """
        return self.filter(is_virtual=True)

    def is_group(self):
        """
        Виртуальные поля
        """
        return self.filter(is_group=True)

    def with_relation_options(self):
        """
        Поля, с аннотацией существования связи
        """
        relation_exists = Case(
            When(relation__isnull=True, then=Value(False)), default=Value(True), output_field=BooleanField()
        )
        relation_need = Case(
            When(field__db_table=F('report__root'), then=Value(False)),
            default=Value(True),
            output_field=BooleanField(),
        )
        return self.annotate(relation_exists=relation_exists, relation_need=relation_need)

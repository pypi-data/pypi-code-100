from operator import attrgetter

from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import (
    Max,
    ManyToManyField,
    ForeignKey,
    Case,
    When,
    Value,
    F,
    Q,
)
from django.db.models.functions import Coalesce
from django.urls import reverse_lazy
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from .choices import InternalType, AggregateFunctionChoices
from .managers import (
    DBTableQuerySet,
    TableFieldQuerySet,
    FormatQuerySet,
    ReportFieldQuerySet,
)


# region Абстрактные модели


class AbstractRDAuthor(models.Model):
    """
    Абстрактная модель: "Автор"
    """

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Автор'),
        related_name='rd_%(class)ss',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        abstract = True


class AbstractRDField(models.Model):
    """
    Абстрактная модель: "Поле"
    """

    name = models.CharField(verbose_name=_('Наименование'), max_length=200)
    alias = models.CharField(verbose_name=_('Псевдоним'), max_length=200, blank=True)
    representation = models.ForeignKey(
        'Format',
        verbose_name=_('Представление'),
        related_name='%(class)s_fields',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        abstract = True
        ordering = ('-pk',)

    def __str__(self):
        return self.name


class AbstracrRDOrder(models.Model):
    """
    Абстрактная модель: "Порядковый номер"
    """

    order = models.PositiveSmallIntegerField(verbose_name=_('Порядковый номер'), default=0)

    class Meta:
        abstract = True
        ordering = ('-order',)


# endregion Абстрактные модели


# region Основные модели


# region Таблицы и поля БД


class DBTable(models.Model):
    """
    Сущность: Таблица БД
    """

    table = models.ForeignKey(ContentType, verbose_name=_('Таблица'), on_delete=models.CASCADE)
    alias = models.CharField(verbose_name=_('Псевдоним'), max_length=200, unique=True)
    is_visible = models.BooleanField(verbose_name=_('Отображение'), default=True)

    objects = DBTableQuerySet.as_manager()

    class Meta:
        verbose_name = _('Таблица БД')
        verbose_name_plural = _('Таблицы БД')
        ordering = ('-pk',)

    def __str__(self):
        return f'{self.alias} ({self.table.name})'

    def get_detail_url(self):
        """
        Ссылка на просмотр таблицы
        """
        return reverse_lazy('report_designer:tables:detail', kwargs={'pk': self.pk})

    def get_edit_url(self):
        """
        Ссылка на редактирование таблицы
        """
        return reverse_lazy('report_designer:tables:update', kwargs={'pk': self.pk})

    def reload_fields(self):
        """
        Актуализация полей таблицы
        """
        # Создание полей таблицы
        fields = []
        for field in self.table.model_class()._meta.get_fields():
            if field.is_relation and not isinstance(field, (ForeignKey, ManyToManyField)):
                continue
            fields.append(
                TableField(
                    db_table=self,
                    name=field.verbose_name,
                    db_field=field.name,
                    is_relation=field.is_relation,
                ),
            )
        TableField.objects.bulk_create(fields)


class TableField(AbstractRDField):
    """
    Сущность: Поле таблицы БД
    """

    db_table = models.ForeignKey(
        DBTable,
        verbose_name=_('Таблица БД'),
        related_name='fields',
        on_delete=models.CASCADE,
    )
    db_field = models.CharField(verbose_name=_('Поле таблицы БД'), max_length=200)
    is_visible = models.BooleanField(verbose_name=_('Отображение'), default=True)
    is_relation = models.BooleanField(verbose_name=_('Связанное поле'), default=False)

    objects = TableFieldQuerySet.as_manager()

    class Meta(AbstractRDField.Meta):
        verbose_name = _('Поле таблицы БД')
        verbose_name_plural = _('Поля таблиц БД')
        unique_together = (
            'db_table',
            'name',
            'db_field',
        )

    def get_edit_url(self):
        """
        Ссылка на редактирование
        """
        return reverse_lazy('report_designer:tables:field-update', kwargs={'pk': self.pk})


# endregion Таблицы и поля БД


# region Формат


class Format(models.Model):
    """
    Сущность: Формат
    """

    name = models.CharField(verbose_name=_('Наименование в БД'), max_length=200, unique=True)
    internal_type = models.SmallIntegerField(verbose_name=_('Тип поля'), choices=InternalType.CHOICES)
    representation = models.CharField(verbose_name=_('Представление'), max_length=1000)

    objects = FormatQuerySet.as_manager()

    class Meta:
        verbose_name = _('Формат')
        verbose_name_plural = _('Форматы')
        ordering = ('-pk',)

    def __str__(self):
        return self.name

    def get_edit_url(self):
        """
        Ссылка на редактирование формата
        """
        return reverse_lazy('report_designer:formats:update', kwargs={'pk': self.pk})


# endregion Формат


# region Отчеты


class ReportGroup(models.Model):
    """
    Сущность: Группа отчета
    """

    name = models.CharField(verbose_name=_('Наименование'), max_length=200, unique=True)

    class Meta:
        verbose_name = _('Группа отчета')
        verbose_name_plural = _('Группы отчетов')
        ordering = ('-pk',)

    def __str__(self):
        return self.name

    @cached_property
    def reports_count(self):
        """
        Количество отчетов в группе
        """
        return self.reports.count()

    def get_edit_url(self):
        """
        Ссылка на редактирование группы отчетов
        """
        return reverse_lazy('report_designer:groups:update', kwargs={'pk': self.pk})


class Report(AbstractRDAuthor):
    """
    Сущность: Отчет
    """

    name = models.CharField(verbose_name=_('Наименование'), max_length=200, unique=True)
    updated = models.DateTimeField(verbose_name=_('Дата и время обновления'), auto_now=True)
    groups = models.ManyToManyField(
        'ReportGroup',
        verbose_name=_('Группы отчетов'),
        related_name='reports',
        blank=True,
    )
    root = models.ForeignKey(
        'DBTable',
        verbose_name=_('Основная таблица'),
        related_name='root_table_reports',
        on_delete=models.CASCADE,
    )
    is_visible_in_reports = models.BooleanField(
        verbose_name=_('Отображать в перечне отчетов при формировании нового отчета'),
        default=True,
    )

    class Meta:
        verbose_name = _('Отчет')
        verbose_name_plural = _('Отчеты')
        ordering = ('-pk',)

    def __str__(self):
        return self.name

    def get_detail_url(self):
        """
        Ссылка на просмотр
        """
        return reverse_lazy('report_designer:reports:detail', kwargs={'pk': self.pk})

    def get_edit_url(self):
        """
        Ссылка на редактирование
        """
        return reverse_lazy('report_designer:reports:update', kwargs={'pk': self.pk})

    @cached_property
    def get_groups_names(self):
        """
        Наименования групп
        """
        return ', '.join(self.groups.values_list('name', flat=True))

    def next_order(self, fields):
        """
        Получение следующего порядкового номера из списка
        """
        return fields.aggregate(max_order=Coalesce(Max('order'), -1)).get('max_order') + 1

    @cached_property
    def field_next_order(self):
        """
        Получение следующего порядкового номера поля в отчете
        """
        return self.next_order(self.report_fields)

    @cached_property
    def group_field_next_order(self):
        """
        Получение следующего порядкового номера группового поля в отчете
        """
        return self.next_order(self.report_fields.filter(is_group=True))

    @cached_property
    def table_next_order(self):
        """
        Получение следующего порядкового номера таблицы в отчете
        """
        return self.next_order(self.report_tables)

    @cached_property
    def field_names(self):
        """
        Поля шапки отчета
        """
        report_fields = self.report_fields.order_by('order')
        return report_fields.annotate(field_name=Coalesce('alias', 'name')).values_list('field_name', flat=True)

    @cached_property
    def field_lookups(self):
        """
        Поля отчета для выборки
        """
        report_fields = self.report_fields.order_by('order')
        return list(map(attrgetter('lookup'), report_fields))

    @cached_property
    def virtual_fields(self):
        """
        Получение виртуальных полей отчета
        """
        return self.report_fields.exclude(expression__iexact='')


class ReportTable(AbstracrRDOrder):
    """
    Сущность: Таблица отчета
    """

    report = models.ForeignKey(
        Report,
        verbose_name=_('Отчет'),
        related_name='report_tables',
        on_delete=models.CASCADE,
    )
    db_table = models.ForeignKey(
        DBTable,
        verbose_name=_('Таблица БД'),
        related_name='report_tables',
        on_delete=models.CASCADE,
    )
    is_root = models.BooleanField(verbose_name=_('Основная таблица отчета'), default=False)

    class Meta:
        verbose_name = _('Таблица отчета')
        verbose_name_plural = _('Таблицы отчета')
        ordering = (
            'order',
            '-pk',
        )

    def __str__(self):
        return f'Таблица отчета "{self.report}"'

    @classmethod
    def label_for_instance(cls, obj):
        """
        Значение для выпадающих списков
        """
        return obj.db_table.alias


class ReportTableRelation(MPTTModel):
    """
    Сущность: Связь до таблицы отчета
    """

    report_table = models.ForeignKey(
        ReportTable,
        verbose_name=_('Таблица отчета'),
        related_name='relations',
        on_delete=models.CASCADE,
    )
    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        db_index=True,
        verbose_name=_('Родительская связь'),
        on_delete=models.SET_NULL,
    )
    name = models.CharField(verbose_name=_('Наименование'), max_length=200)

    class Meta:
        verbose_name = _('Связь до таблицы отчета')
        verbose_name_plural = _('Связи до таблиц отчетов')
        ordering = ('-pk',)

    def __str__(self):
        return f'Связь до таблицы {self.report_table.db_table.alias} отчета {self.report_table.report}'

    @classmethod
    def label_for_instance(cls, obj):
        """
        Значение для выпадающих списков
        """
        return f'{obj.name} ({obj.report_table.db_table.alias})'

    def get_edit_url(self):
        """
        Ссылка на редактирование
        """
        kwargs = {'report_pk': self.report_table.report.pk, 'pk': self.pk}
        return reverse_lazy('report_designer:reports:update-report-table-relation', kwargs=kwargs)


class ReportTableRelationCondition(AbstracrRDOrder):
    """
    Сущность: Условие связи таблицы отчета
    """

    report_table_relation = models.ForeignKey(
        ReportTableRelation,
        verbose_name=_('Связь до таблицы отчета'),
        related_name='from_report_table_relations',
        on_delete=models.CASCADE,
    )
    from_field = models.ForeignKey(
        TableField,
        verbose_name=_('Начальное поле'),
        related_name='report_table_rel_from',
        on_delete=models.CASCADE,
    )
    to_field = models.ForeignKey(
        TableField,
        verbose_name=_('Конечное поле'),
        related_name='report_table_rel_to',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _('Условие связи таблицы отчета')
        verbose_name_plural = _('Условия связи таблиц отчетов')
        ordering = (
            'order',
            '-pk',
        )

    def __str__(self):
        return f'{self.report_table_relation} ({self.from_field.alias} = {self.to_field.alias})'


class ReportField(AbstracrRDOrder, AbstractRDField):
    """
    Сущность: Поле отчета
    """

    report = models.ForeignKey(
        Report,
        verbose_name=_('Отчет'),
        related_name='report_fields',
        on_delete=models.CASCADE,
    )
    field = models.ForeignKey(
        TableField,
        verbose_name=_('Поле таблицы БД'),
        related_name='report_fields',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    report_table_relation = models.ForeignKey(
        ReportTableRelation,
        verbose_name=_('Связь таблицы поля с основной таблицей отчета'),
        related_name='report_fields',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    relations = models.ManyToManyField(
        TableField,
        verbose_name=_('Связь с корневой таблицей'),
        related_name='relations_report_fields',
        through='ReportFieldRelation',
        blank=True,
    )
    expression = models.CharField(verbose_name=_('Выражение'), max_length=2000, blank=True)
    internal_type = models.SmallIntegerField(
        verbose_name=_('Тип поля'),
        choices=InternalType.CHOICES,
        blank=True,
        null=True,
    )
    is_virtual = models.BooleanField(verbose_name=_('Виртуальное поле'), default=False)
    is_group = models.BooleanField(verbose_name=_('Групповое поле'), default=False)
    is_sort = models.BooleanField(verbose_name=_('Сортировочное поле'), default=False)
    reverse_sort = models.BooleanField(verbose_name=_('Обратная сортировка'), default=False)
    is_aggregate = models.BooleanField(
        verbose_name=_('Агрегированное поле'),
        default=False,
        help_text=_('Аггрегация производится для групповых полей отчета'),
    )
    aggregate_function = models.CharField(
        verbose_name=_('Функция агрегирования'),
        blank=True,
        null=True,
        max_length=20,
        choices=AggregateFunctionChoices.CHOICES,
    )

    objects = ReportFieldQuerySet.as_manager()

    class Meta(AbstractRDField.Meta):
        verbose_name = _('Поле отчета')
        verbose_name_plural = _('Поля отчетов')
        ordering = (
            'order',
            '-pk',
        )

    def get_edit_url(self):
        """
        URL редактирования поля
        """
        return reverse_lazy('report_designer:reports:report-field-update', kwargs={'pk': self.pk})

    def get_change_order_url(self):
        """
        URL изменения порядка поля
        """
        return reverse_lazy('report_designer:reports:field-change-order', kwargs={'pk': self.pk})

    @property
    def model_field(self):
        """
        Настойщее поле модели
        """
        if self.field:
            table = self.field.db_table.table
            return table.model_class()._meta.get_field(self.field.db_field)

    def get_field_internal_type(self):
        """
        Получение типа поля для полей таблиц
        """
        field = self.model_field
        if field:
            return field.get_internal_type()

    def reorder(self, new):
        """
        Изменение порядка поля
        """
        is_downgrade = new < self.order

        # Обновление порядка у всех полей отчета
        query = Case(
            *[
                When(order=Value(self.order), then=Value(new)),
                When(
                    Q(
                        **{
                            f'order__{is_downgrade and "l" or "g"}t': Value(self.order),
                            f'order__{is_downgrade and "g" or "l"}te': Value(new),
                        }
                    ),
                    then=F('order') + (is_downgrade and 1 or -1),
                ),
            ],
            default=F('order'),
        )
        self.report.report_fields.update(order=query)

    @cached_property
    def relations_lookup(self):
        """
        Связь от корневой таблицы до поля
        """
        if self.relations.exists():
            return f'__'.join(self.relations.all().values_list('db_field', flat=True))

    @cached_property
    def lookup(self):
        """
        Связь от корневой таблицы до поля
        """
        return f'__'.join(filter(None, [self.relations_lookup, self.field.db_field]))


class ReportFieldRelation(AbstracrRDOrder):
    """
    Сущность: Связь от корневой таблицы до поля
    -------------

    Под корневой таблицей понимается корень дерева при
    переносе полей в отчет, от которого выбиралось поле
    """

    report_field = models.ForeignKey(ReportField, verbose_name=_('Поле отчета'), on_delete=models.CASCADE)
    table_field = models.ForeignKey(TableField, verbose_name='Поле таблицы', on_delete=models.CASCADE)

    class Meta(AbstracrRDOrder.Meta):
        verbose_name = _('Связь поля отчета')
        verbose_name_plural = _('Связи полей очтетов')
        unique_together = (
            'order',
            'report_field',
            'table_field',
        )

    def __str__(self):
        return f'Связь поля отчета "{self.report_field}" через поле таблицы "{self.table_field}"'


# endregion Отчеты


# endregion Основные модели

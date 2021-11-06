from copy import copy
from typing import Optional, Union

from django.db.models import Model, ForeignObject, DO_NOTHING, QuerySet
from django.db.models.options import Options
from django.db.models.sql.constants import LOUTER
from django.db.models.sql.datastructures import Join


class CJoin:
    """
    Присоединение таблиц
    -----------

    Использование
    -----------
    >>>
    >>> class FirstModel(Model):
    >>>     objects = QuerySet
    >>>
    >>> class SecondModel(Model):
    >>>     pass
    >>>
    >>> qs = CJoin(FirstModel.objects.all(), SecondModel, ['first_field'], ['second_field'], 'alias_for_filter').join()
    >>>
    >>>
    """

    _COPIED_META_ATTRS = (
        'local_fields',
        'local_many_to_many',
        'local_managers',
        'ordering',
        'db_table',
        'object_name',
        'app_label',
        'pk',
        'auto_field',
    )

    JOIN_TYPE = LOUTER

    def __init__(
        self,
        queryset: QuerySet,
        target: Model,
        from_fields: Union[list, tuple],
        to_fields: Union[list, tuple],
        alias: str = None,
    ) -> None:
        self.qs = queryset
        self.target = target
        self.from_fields = from_fields
        self.to_fields = to_fields
        # Псевдоним для фильтров
        self._alias = alias
        self._options: Optional[Options] = None

    def join(self):
        """
        Присоединение таблицы к выборке
        """
        self.prepare_joined_fields()
        foreign_object = self.create_foreign_obj()
        options = self.create_options(foreign_object)
        foreign_object.opts = options
        join = self.create_join(foreign_object)
        return self.processing_qs(options, join)

    def prepare_joined_fields(self):
        """
        Обработка полей перед объединением
        """
        def prepare_fields(model, fields):
            prepared_fields = []
            model_meta = model._meta
            for field in fields:
                model_field = model_meta.get_field(field)
                prepared_fields.append(model_field.is_relation and model_field.column or field)
            return prepared_fields

        # Проверка, является ли поле связью
        self.from_fields = prepare_fields(self.base_model, self.from_fields)
        self.to_fields = prepare_fields(self.target, self.to_fields)

    def processing_qs(self, options: Options, join: Join) -> QuerySet:
        """
        Обработка выборки
        """

        def get_meta(*args, **kwargs):
            """
            Получение метокласса в запросе
            """
            return options

        # Подмена функции получения метакласса выборки
        # для получения необходимых полей при объединении
        self.qs.query.get_meta = get_meta
        self.qs.query.join(join)
        return self.qs

    def create_foreign_obj(self) -> ForeignObject:
        """
        Создание абстрактной связи присоединяемой таблицы
        """

        def get_joining_columns(*args, **kwargs):
            """
            Поля для объединения
            """
            return list(zip(self.from_fields, self.to_fields))

        foreign_obj = ForeignObject(
            self.target,
            on_delete=DO_NOTHING,
            from_fields=self.from_fields,
            to_fields=self.to_fields,
            name=self.alias,
        )
        foreign_obj.get_joining_columns = get_joining_columns
        foreign_obj.model = self.target
        return foreign_obj

    def create_options(self, foreign_object: ForeignObject) -> Options:
        """
        Создание настроек таблицы
        """
        meta = self.base_model_meta
        options = Options(meta)
        for attr in self._COPIED_META_ATTRS:
            value = getattr(meta, attr, None)
            if not value:
                continue
            setattr(options, attr, copy(value))
        options.model = meta.model
        options._forward_fields_map.update({self.alias: foreign_object})
        return options

    def create_join(self, foreign_object: ForeignObject):
        """
        Создание объединения
        """
        return Join(
            self.target._meta.db_table,
            self.base_model_meta.db_table,
            self.alias,
            self.JOIN_TYPE,
            foreign_object,
            True,
        )

    @property
    def alias(self) -> str:
        """
        Псевдоним присоединяемой таблицы
        """
        alias = self._alias or self.target._meta.db_table
        if alias in self.base_model_meta.fields_map:
            raise AttributeError(f'Псевдоним {alias} уже существует в таблице {self.base_model.__name__}')
        return alias

    @property
    def base_model(self) -> Model:
        """
        Базовая таблица
        """
        return self.qs.model

    @property
    def base_model_meta(self) -> Options:
        """
        Базовая таблица
        """
        return self.base_model._meta

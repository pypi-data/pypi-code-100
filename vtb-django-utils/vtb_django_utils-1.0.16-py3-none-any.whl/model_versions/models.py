from __future__ import annotations

from copy import copy
from typing import Optional, List, Tuple, Type

from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.db.models import JSONField, Func, F, Value
from django_lifecycle import hook, BEFORE_SAVE

from vtb_django_utils.user_info.info import get_user_info
from vtb_django_utils.utils.class_factory import class_factory
from vtb_django_utils.utils.db import CreatedMixin, get_model_fields
from vtb_django_utils.utils.diff import get_objs_diff
from vtb_django_utils.utils.jsons import get_json_hash
from .utils.consts import START_VERSION, THERE_IS_NO_VERSION_DATA, DOES_NOT_EXIST_VERSION, REL_VERSION_FIELD_END, \
    REL_VERSION_PATTERN_FIELD_END, VERSION_DELIMITER, ERR_VERSIONED_OBJ_NOT_SELECTED, \
    ERR_VERSIONED_OBJ_DONT_MATCH_SELECTED_VERSION, ERR_SELECTED_VERSION_AND_PATTERN, ERR_WRONG_VERSION_PATTERN_FORMAT, \
    VERSION_PATTERN_REGEX
from .utils.regex import version_regex
from .utils.strings import int_arr_to_str, str_to_int_arr
from ..utils.exceptions import VersionException


class VersionModel(CreatedMixin, models.Model):
    """ Базовый класс для версий какой-либо модели """
    user = JSONField(default=dict, blank=True)
    json = JSONField(default=dict, blank=True)
    hash = models.TextField()
    version_arr = ArrayField(models.PositiveSmallIntegerField(), max_length=3, default=list, blank=True)

    class Meta:
        abstract = True

    @property
    def version(self) -> str:
        """ Возвращает версию в виде строки """
        return int_arr_to_str(self.version_arr)

    @property
    def changed_by_user(self) -> str:
        """ Имя пользователя, создавшего версию """
        # noinspection PyUnresolvedReferences
        return self.user.get('username', '')


class VersionRawJsonModel(VersionModel):
    """ Базовый класс для версий какой-либо модели с raw_json """
    raw_json = JSONField(default=dict, blank=True)
    raw_hash = models.TextField(default='', blank=True)

    class Meta:
        abstract = True
        
        
class ModelWithVersionedRelationsMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rel_versioned_fields = self._get_field_names_for_rel_versioned_obj()

    def _get_field_names_for_rel_versioned_obj(self) -> set:
        """ Возвращает имена связанных полей с версиями """
        def _get_fields(pattern):
            return set([f.replace(pattern, '') for f in fields if f.endswith(pattern)])

        fields = get_model_fields(self.__class__)
        rel_fields = set(_get_fields(REL_VERSION_FIELD_END)) & set(_get_fields(REL_VERSION_PATTERN_FIELD_END))
        return rel_fields


class ModelWithVersionedRelationsValidatorsMixin(ModelWithVersionedRelationsMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.class_name = self.__class__.__name__

    def clean(self):
        # noinspection PyUnresolvedReferences
        super().clean()
        self._validate()

    @hook(BEFORE_SAVE)
    def _validate(self):
        self.validation_versioned_instance_not_selected()
        self.validation_version_pattern_format()
        self.validation_versioned_instance_not_natch_version()
        self.validation_select_version_and_pattern()

    def validation_versioned_instance_not_selected(self):
        """ Проверка что если задана ее версия или шаблон, то модель с версией тоже выбрана """
        for rel_field in self.rel_versioned_fields:
            versioned_instance_id = getattr(self, f'{rel_field}_id')
            version = getattr(self, f'{rel_field}{REL_VERSION_FIELD_END}')
            version_pattern = getattr(self, f'{rel_field}{REL_VERSION_PATTERN_FIELD_END}')
            if not versioned_instance_id and (version or version_pattern):
                raise ValidationError(ERR_VERSIONED_OBJ_NOT_SELECTED.format(self.class_name))

    def validation_version_pattern_format(self):
        """ Проверяет формат паттерна версии """
        for rel_field in self.rel_versioned_fields:
            version_pattern = getattr(self, f'{rel_field}{REL_VERSION_PATTERN_FIELD_END}')
            if version_pattern and not VERSION_PATTERN_REGEX.match(version_pattern):
                raise ValidationError(ERR_WRONG_VERSION_PATTERN_FORMAT + f' node: ')

    def validation_versioned_instance_not_natch_version(self):
        """ Проверка что выбраная модель с версией и выбранная версия соответствуют """
        for rel_field in self.rel_versioned_fields:
            if (
                    (versioned_instance := getattr(self, f'{rel_field}')) and
                    (version := getattr(self, f'{rel_field}{REL_VERSION_FIELD_END}'))
            ):
                if not versioned_instance.versions.filter(id=version.id).exists():
                    raise ValidationError(ERR_VERSIONED_OBJ_DONT_MATCH_SELECTED_VERSION.format(
                        str(version), self.class_name, str(getattr(self, f'{rel_field}'))
                    ))

    def validation_select_version_and_pattern(self):
        """ Нельзя выбрать версию и шаблон версии одновременно """
        for rel_field in self.rel_versioned_fields:
            version = getattr(self, f'{rel_field}{REL_VERSION_FIELD_END}')
            version_pattern = getattr(self, f'{rel_field}{REL_VERSION_PATTERN_FIELD_END}')
            if version and version_pattern:
                raise ValidationError(ERR_SELECTED_VERSION_AND_PATTERN.format(self.class_name))

    
class VersionedModelMixin(ModelWithVersionedRelationsValidatorsMixin):
    """ Добавляет методы для работы с версиями модели """
    @property
    def json(self) -> dict:
        return {}

    @property
    def versions_set(self):
        """ Возвращает set связанной модели по related_name """
        return getattr(self, 'versions')

    @property
    def hash(self) -> str:
        """ Возвращает хеш json  """
        return get_json_hash(self.json)

    def get_version_by_pattern(
            self, version: Optional[VersionModel] = None, version_pattern_attr: Optional[str] = None) -> VersionModel:
        """ Возвращает инстанс версии модели по шаблону """
        if version:
            return version

        if not version_pattern_attr:
            return self.last_version

        if len([s for s in version_pattern_attr.split(VERSION_DELIMITER) if s]) < 3:
            # это паттерн
            version_instance = self.versions_set.annotate(
                exact_version=Func(F('version_arr'), Value(VERSION_DELIMITER), function='array_to_string')
            ).filter(
                exact_version__regex=version_regex(version_pattern_attr)
            ).order_by('-version_arr').first()
        else:
            # это строка
            try:
                version_instance = self.versions_set.get(version_arr=str_to_int_arr(version_pattern_attr))
            except self.versions_set.model.DoesNotExist:
                # noinspection PyUnresolvedReferences
                raise VersionException(f'Версия {version_pattern_attr} для {str(self)} id={self.pk} не существует')

        return version_instance

    @property
    def version_list(self) -> List[str]:
        """ Возвращает список версий в виде строк """
        return [v.version for v in self.versions_set.all()]

    @property
    def last_version(self) -> Optional[VersionModel]:
        """ Возвращает инстанс последней версии """
        versions = self.versions_set.all()
        return max(versions, key=lambda x: x.version_arr) if versions else None

    @property
    def is_version_changed(self) -> bool:
        """ Возвращает признак изменения json модели по сравнению с посделней сохраненной версией """
        if self.last_version and self.hash == self.last_version.hash:
            return False
        return True

    @property
    def next_version_str(self) -> str:
        """ Возвращает строку со следующей версией, инкрементированной по минору """
        last_version = self.last_version
        if last_version and last_version.version_arr:
            # noinspection PyUnresolvedReferences
            last_version.version_arr[-1] += 1
            return int_arr_to_str(last_version.version_arr)
        else:
            return START_VERSION

    def _add_version_for_rel_versioned_obj(self, model_version_json):
        """ Добавляет информацию о версиях связанных моделей """
        for rel_field in self.rel_versioned_fields:
            obj_version = getattr(self, f'{rel_field}{REL_VERSION_FIELD_END}')
            model_version_json[f'{rel_field}{REL_VERSION_FIELD_END}'] = obj_version.version if obj_version else ''

    def get_json_by_version(self, version_or_pattern: Optional[str] = None, json_field_name: str = 'json',
                            compare_with_version: str = None) -> dict:
        """ Возвращает json версии по строке версии (или паттерну) """
        if version_or_pattern:
            version_instance = self.get_version_by_pattern(version_pattern_attr=version_or_pattern)
        else:
            version_instance = self.last_version

        if version_instance:
            model_version_json = copy(getattr(version_instance, json_field_name, {}))
            if not model_version_json:
                model_version_json['error'] = THERE_IS_NO_VERSION_DATA
            model_version_json['version'] = version_instance.version
            model_version_json['version_create_dt'] = version_instance.create_dt
            model_version_json['version_changed_by_user'] = version_instance.changed_by_user
            # добавляем разницу с указанной версией (если заказано)
            if compare_with_version:
                json_diff = {'compare_with_version': compare_with_version}
                try:
                    compare_version_instance = self.versions_set.get(version_arr=str_to_int_arr(compare_with_version))
                except self.versions_set.model.DoesNotExist:
                    json_diff['err'] = DOES_NOT_EXIST_VERSION.format(compare_with_version)
                else:
                    origin_version_json = getattr(version_instance, json_field_name)
                    compare_version_json = getattr(compare_version_instance, json_field_name)
                    json_diff['diff'] = get_objs_diff(compare_version_json or {}, origin_version_json)
                    json_diff['changed_by_user'] = compare_version_instance.changed_by_user
                model_version_json['version_diff'] = json_diff
            # добавляем версии связанных моделей
            self._add_version_for_rel_versioned_obj(model_version_json)
        else:
            model_version_json = {}

        return model_version_json

    @transaction.atomic
    def create_or_update_version(self, version_str: str = None) -> Tuple[bool, VersionModel]:
        """ Создает или обновляет версию """
        model_version, is_created = self.versions_set.get_or_create(
            version_arr=str_to_int_arr(version_str or self.next_version_str),
        )
        model_version.user = get_user_info()
        model_version = self._patch_model_version(model_version)
        model_version.save()

        return is_created, model_version

    def _patch_model_version(self, model_version: VersionModel) -> VersionModel:
        """ Модификация полей версии """
        model_version.json = self.json
        model_version.hash = self.hash
        return model_version


class VersionedRawModelMixin(VersionedModelMixin):
    """ Добавляет методы для работы с версиями модели """
    versions = None

    @property
    def raw_json(self) -> dict:
        return {}

    @property
    def raw_hash(self) -> str:
        """ Возвращает хеш json отнаследованной модели """
        return get_json_hash(self.raw_json)

    def _patch_model_version(self, model_version: VersionRawJsonModel):
        """ Модификация полей версии """
        model_version = super(VersionedRawModelMixin, self)._patch_model_version(model_version)
        model_version.raw_json = self.raw_json
        model_version.raw_hash = self.raw_hash
        return model_version

    @property
    def is_raw_version_changed(self) -> bool:
        """ Возвращает признак изменения raw_json модели по сравнению с посделней сохраненной версией """
        last_version: Optional[VersionRawJsonModel] = self.last_version
        if last_version and self.raw_hash == last_version.raw_hash:
            return False
        return True


def create_version_model_class(
        module_name: str, model_name: str, version_parent_model: Type[VersionModel]) -> VersionModel:
    lower_name = model_name.lower()
    capitalize_name = model_name.capitalize()
    meta_fields = dict(
        verbose_name=f'{lower_name} version',
        verbose_name_plural=f'{lower_name} versions',
        unique_together=(f'{lower_name}_id', 'version_arr'),
        indexes=[models.Index(fields=(f'{lower_name}_id', 'version_arr'))],
        ordering=(f'{lower_name}_id', 'version_arr'),
    )

    # create class Meta
    class_meta = class_factory(module_name, 'Meta', (version_parent_model.Meta,), {})
    for k, v in meta_fields.items():
        setattr(class_meta, k, v)

    # create class VersionModel
    class_version = class_factory(module_name, f'{capitalize_name}Version', (version_parent_model,), {
        lower_name: models.ForeignKey(capitalize_name, related_name='versions', on_delete=models.CASCADE),
        'Meta': class_meta,
    })
    class_version.__str__ = lambda self: f'{getattr(self, lower_name)}:{self.version}'

    return class_version


def is_instance_versioned(instance):
    return hasattr(instance, 'versions')

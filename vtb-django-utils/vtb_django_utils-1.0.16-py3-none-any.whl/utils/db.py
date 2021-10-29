from typing import List, Optional, Union

from django.db import models
from django.utils import timezone


class CreatedMixin(models.Model):
    create_dt = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        abstract = True
        ordering = ('create_dt',)


def get_model_fields(model_class, exclude: Union[tuple, list] = None) -> List[str]:
    """ Возвращает список полей модели БД """
    exclude_set = set(exclude or [])
    # noinspection PyProtectedMember
    return [f.name for f in model_class._meta.fields if f.name not in exclude_set]


def create_model_from_dict(model, data: dict, ignore_fields: Optional[Union[list, tuple]] = None):
    """ Создает экземпляр модели в БД из словаря """
    db_fields = set(get_model_fields(model))
    ignore_fields = ignore_fields or []
    return model.objects.create(**{
        k: v for k, v in data.items()
        if k in db_fields and k not in ignore_fields}
    )

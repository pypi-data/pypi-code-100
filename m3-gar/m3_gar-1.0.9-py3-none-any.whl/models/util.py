from django.apps import (
    apps,
)
from django.db import (
    models,
)


def make_fk(model, field_name, **kwargs):
    field = model._meta.get_field(field_name)
    _, db_column = field.get_attname_column()

    unique = kwargs.pop('unique', False)
    kwargs.setdefault('on_delete', models.DO_NOTHING)
    kwargs.setdefault('related_name', '+')
    kwargs.setdefault('verbose_name', field.verbose_name)
    kwargs.setdefault('null', field.null)
    kwargs.setdefault('blank', field.blank)
    kwargs.setdefault('db_column', db_column)

    if unique:
        new_field_type = models.OneToOneField
    else:
        new_field_type = models.ForeignKey

    new_field = new_field_type(**kwargs)

    model._meta.local_fields.remove(field)
    new_field.contribute_to_class(model, field_name)


def add_params(addr_model, params_model):

    @property
    def params(self):
        Param = apps.get_model(params_model)

        class ParamManager(Param._default_manager.__class__):
            def get_queryset(manager):
                return super().get_queryset().filter(objectid=self.objectid_id)

        manager = ParamManager()
        manager.model = Param

        return manager

    addr_model.params = params


class RegionCodeModelMixin(models.Model):
    region_code = models.SmallIntegerField(verbose_name='Код региона')

    class Meta:
        abstract = True

# banjo.db.models
# Database models which wrap django
from django.db import models

class Model(models.Model):

    @classmethod
    def from_dict(cls, props):
        """Tries to create an instance of Model from props.
        """
        if 'id' in props:
            del props['id']
        return cls(**props)

    def to_dict(self):
        """Returns a json representation of the Model.
        """
        field_names = [f.name for f in self._meta.get_fields() if f.name != "model_ptr"]
        d = {}
        for name in field_names:
            value = getattr(self, name)
            if isinstance(value, Model):
                d[name] = {'id': value.id}
            elif hasattr(value, 'all'):
                d[name] = [{'id': obj.id} for obj in value.all()]
            else:
                d[name] = value
        return d

    def __str__(self):
        return "<{} {}>".format(self.__class__.__name__, self.to_dict())

    class Meta:
        abstract = True
        app_label = "app"

class BooleanField(models.BooleanField):
    """A database column which stores a boolean.
    The default value is False.
    """
    def __init__(self, *args, **kwargs):
        kwargs['default'] = False
        models.BooleanField.__init__(self, *args, **kwargs)

class IntegerField(models.IntegerField):
    """A database column which stores an integer.
    The default value is 0.
    """
    def __init__(self, *args, **kwargs):
        kwargs['default'] = 0
        models.IntegerField.__init__(self, *args, **kwargs)

class FloatField(models.FloatField):
    """A database column which stores a float.
    The default value is 0.0.
    """
    def __init__(self, *args, **kwargs):
        kwargs['default'] = 0.0
        models.FloatField.__init__(self, *args, **kwargs)

class StringField(models.TextField):
    """A database column which stores a string.
    The default value is '', the empty string.
    """
    def __init__(self, *args, **kwargs):
        kwargs['default'] = ''
        models.TextField.__init__(self, *args, **kwargs)

class ForeignKey(models.ForeignKey):
    """A database column which links a model to another model.
    """
    def __init__(self, *args, **kwargs):
        kwargs['on_delete'] = models.CASCADE
        models.ForeignKey.__init__(self, *args, **kwargs)

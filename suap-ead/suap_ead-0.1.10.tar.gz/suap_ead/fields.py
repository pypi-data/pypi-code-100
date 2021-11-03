from django.db.models import CharField
from django.db.models import ForeignKey, CASCADE


nullable = {'null': True, 'blank': True}
nullable_phone = {'null': True, 'blank': True, 'help_text': '(00) 00000-0000', 'max_length': 15}


class StringField(CharField):
    def __init__(self, verbose_name, max_length=250, *args, **kwargs):
        super().__init__(verbose_name=verbose_name, max_length=max_length, *args, **kwargs)


class NullStringField(StringField):
    def __init__(self, verbose_name, max_length=250, null=True, blank=True, *args, **kwargs):
        super().__init__(verbose_name=verbose_name, max_length=max_length, null=True, blank=True, *args, **kwargs)


class FK(ForeignKey):
    def __init__(self, verbose_name, to, on_delete=CASCADE,
                 related_name=None, related_query_name=None, limit_choices_to=None,
                 parent_link=False, to_field=None, db_constraint=True, **kwargs):
        super().__init__(to, on_delete, related_name, related_query_name,
                         limit_choices_to, parent_link, to_field, db_constraint, verbose_name=verbose_name, **kwargs)


class NullFK(ForeignKey):
    def __init__(self, verbose_name, to, on_delete=CASCADE,
                 related_name=None, related_query_name=None, limit_choices_to=None,
                 parent_link=False, to_field=None, db_constraint=True, null=True, blank=True, **kwargs):
        super().__init__(to, on_delete, related_name, related_query_name,
                         limit_choices_to, parent_link, to_field, db_constraint,
                         verbose_name=verbose_name, null=null, blank=blank, **kwargs)

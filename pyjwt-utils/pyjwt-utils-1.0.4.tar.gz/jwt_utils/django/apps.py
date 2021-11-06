# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class DjangoJwtUtilsConfig(AppConfig):  # Our app config class
    name = 'jwt_utils.django'
    verbose_name = _('Django JWT Utils')

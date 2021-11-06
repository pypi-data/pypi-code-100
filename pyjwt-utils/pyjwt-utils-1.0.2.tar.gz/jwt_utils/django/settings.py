from django.conf import settings
from django.test.signals import setting_changed
from django.utils.translation import gettext_lazy as _

from rest_framework.settings import APISettings as _APISettings


USER_SETTINGS = getattr(settings, 'JWT_UTILS', None)

DEFAULTS = {
    # all settings with None or False are ignored by default.

    # Generating Jwt
    'SIGNING_KEY': settings.SECRET_KEY,
    'ALGORITHM': 'HS256',
    'ISSUER': None,  # None -> ignore (https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.1)
    'SUBJECT': None,  # None -> ignore (https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.2)
    'AUDIENCE': None,  # None -> ignore (https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.3)
    'EXPIRATION': None,  # None -> ignore, ex: timedelta(minutes=5) (https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.4)
    'NOT_BEFORE': None,  # None -> ignore, ex: timedelta(seconds=1) (https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.5)
    'IAT': None,  # None -> ignore (https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.6)
    'AUTO_IAT': False,  # Default False (generate iat with current time) - (used only if IAT is None)
    'JTI': None,  # None -> ignore (https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.7)
    'AUTO_JTI': False,  # Default False (generate jti with random hex) - (used only if JTI is None)

    # Checking Jwt
    'VERIFY_ISSUER': False,  # False -> ignore
    'VERIFY_AUDIENCE': False,  # False -> ignore
    'VERIFY_EXPIRATION': False,  # False -> ignore
    'VERIFY_NOT_BEFORE': False,  # False -> ignore
    'VERIFY_IAT': False,  # False -> ignore
    'VERIFY_MAX_LEEWAY': 0,
}

DEFAULTS = {
    **DEFAULTS,
    'VERIFY_ISSUER': DEFAULTS['ISSUER'] is not None,
    'VERIFY_AUDIENCE': DEFAULTS['AUDIENCE'] is not None,
    'VERIFY_EXPIRATION': DEFAULTS['EXPIRATION'] is not None,
    'VERIFY_NOT_BEFORE': DEFAULTS['NOT_BEFORE'] is not None,
    'VERIFY_IAT': DEFAULTS['IAT'] is not None or DEFAULTS['AUTO_IAT'],
    'VERIFY_MAX_LEEWAY': 0,
}

IMPORT_STRINGS = ()

REMOVED_SETTINGS = ()


class APISettings(_APISettings):  # pragma: no cover
    pass


api_settings = APISettings(USER_SETTINGS, DEFAULTS, IMPORT_STRINGS)


def reload_api_settings(*args, **kwargs):  # pragma: no cover
    global api_settings

    setting, value = kwargs['setting'], kwargs['value']

    if setting == 'JWT_UTILS':
        api_settings = APISettings(value, DEFAULTS, IMPORT_STRINGS)


setting_changed.connect(reload_api_settings)

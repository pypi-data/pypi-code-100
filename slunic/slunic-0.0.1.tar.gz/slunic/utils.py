import re
import uuid
import json
import hashlib
import logging
from urllib import request
from datetime import datetime
from calendar import timegm
from django.db import models
from django.apps import apps
from django.core.cache import cache
from django.core.exceptions import ImproperlyConfigured
from django.core.cache.utils import make_template_fragment_key
from django.urls import reverse, NoReverseMatch
from django.utils.http import urlencode
from django.template.defaultfilters import slugify


from .configs import app_configs

logger = logging.getLogger(app_configs.LOGGER_NAME)


def get_model_slug(model):
    opts = model._meta
    return "%s.%s" % (opts.app_label, opts.model_name)


def get_profile_model():
    """
    Return the User Profile model that is active in this project.
    """
    try:
        return apps.get_model(app_configs.USER_PROFILE_MODEL, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured("PROFILE_MODEL must be of the form 'app_label.model_name'")
    except LookupError:
        raise ImproperlyConfigured(
            "SLUNIC_PROFILE_MODEL refers to model '%s' that has not been installed"
            % app_configs.USER_PROFILE_MODEL
        )


def get_login_url():
    try:
        return reverse(app_configs.USER_LOGIN_URL)
    except NoReverseMatch as err:
        logger.info(err)
        return app_configs.USER_LOGIN_URL


def get_logout_url():
    try:
        return reverse(app_configs.USER_LOGOUT_URL)
    except NoReverseMatch as err:
        logger.info(err)
        return app_configs.USER_LOGOUT_URL


def get_signup_url():
    try:
        return reverse(app_configs.USER_SIGNUP_URL)
    except NoReverseMatch as err:
        logger.info(err)
        return app_configs.USER_SIGNUP_URL


def get_uid(limit=8):
    if limit == 0:
        return str(uuid.uuid4())
    return str(uuid.uuid4())[:limit]


def get_ip(request):
    """
    Attempts to extract the IP number from the HTTP request headers.
    """
    key = "REMOTE_ADDR"
    meta = request.META

    # Lowercase keys
    simple_meta = {k.lower(): v for k, v in request.META.items()}
    ip = meta.get(key, simple_meta.get(key, "0.0.0.0"))
    return ip


def get_location(ip):
    try:
        url = f"http://ip-api.com/json/{ip}"
        logger.info(f"{ip}, {url}")
        req = request.Request(url=url, headers={"User-Agent": "Mozilla/5.0"})
        res = request.urlopen(req, timeout=3).read()
        data = json.loads(res)

        # Log the return data.
        logger.info(data)
        return data
    except Exception as exc:
        logger.error(exc, exc_info=1)


def get_gravatar_url(email, size=50):
    default = "mm"
    size = int(size) * 2  # requested at retina size by default and scaled down at point of use with css
    gravatar_provider_url = app_configs.USER_GRAVATAR_PROVIDER_URL

    if (not email) or (gravatar_provider_url is None):
        return None

    gravatar_url = "{gravatar_provider_url}/{hash}?{params}".format(
        gravatar_provider_url=gravatar_provider_url.rstrip("/"),
        hash=hashlib.md5(email.lower().encode("utf-8")).hexdigest(),
        params=urlencode({"s": size, "d": default}),
    )

    return gravatar_url


def delete_cache(prefix, user):
    """
    Create key from prefix-user.pk and delete from cache.
    """
    key = f"{prefix}:{user.pk}"

    # Check if it exists and delete object from cache.
    if cache.get(key):
        cache.delete(key)
        logger.debug(f"deleted {key} from cache")
    return


def make_fragment_key(model, request=None, **kwarg):
    if isinstance(model, str):
        fragment_name = model
    elif issubclass(model, models.Model):
        opts = model._meta
        fragment_name = f"{opts.app_label}.{opts.model_name}"
    vary_on = ["%s:%s" % (key, val) for key, val in kwarg.items()]
    if request is not None:
        vary_on.extend(["%s:%s" % (key, val) for key, val in request.GET.items()])

    cache_key = make_template_fragment_key(fragment_name, vary_on)
    return cache_key


def delete_fragment_cache(model, request=None, **kwargs):
    """
    Drops a fragment cache.
    """
    key = make_fragment_key(model, request=None, **kwargs)
    cache.delete(key)


def delete_page_cache(page):
    """
    Drops both page specific api and  template fragment caches.
    """
    model = page.get_real_model_class()
    delete_fragment_cache(model, mode="api", page_id=page.id)
    delete_fragment_cache(model, mode="view", page_id=page.id)
    if page.parent:
        delete_fragment_cache(model, mode="api", page_id=page.parent.id)
        delete_fragment_cache(model, mode="view", page_id=page.parent.id)


def datetime_to_iso(date):
    """
    Converts a datetime to the ISO8601 format, like: 2014-05-20T06:11:41.733900.

    Parameters:
    date -- a `datetime` instance.
    """
    if not isinstance(date, datetime):
        date = datetime.combine(date, datetime.min.time())
    return date.isoformat()


def datetime_to_unix(date):
    """
    Converts a datetime to a Unix timestamp , like: 1400566301.

    Parameters:
    date -- a `datetime` instance.
    """
    return timegm(date.timetuple())


def pluralize(value, word):
    if value > 1:
        return "%d %ss" % (value, word)
    else:
        return "%d %s" % (value, word)


def unique_slugify(instance, value, slug_field_name="slug", queryset=None, slug_separator="-"):
    """
    Calculates and stores a unique slug of ``value`` for an instance.

    ``slug_field_name`` should be a string matching the name of the field to
    store the slug in (and the field to check against for uniqueness).

    ``queryset`` usually doesn't need to be explicitly provided - it'll default
    to using the ``.all()`` queryset from the model's default manager.
    """
    slug_field = instance._meta.get_field(slug_field_name)

    slug = getattr(instance, slug_field.attname)
    slug_len = slug_field.max_length

    # Sort out the initial slug, limiting its length if necessary.
    slug = slugify(value)
    if slug_len:
        slug = slug[:slug_len]
    slug = _slug_strip(slug, slug_separator)
    original_slug = slug

    # Create the queryset if one wasn't explicitly provided and exclude the
    # current instance from the queryset.
    if queryset is None:
        queryset = instance.__class__._default_manager.all()
    if instance.pk:
        queryset = queryset.exclude(pk=instance.pk)

    # Find a unique slug. If one matches, at '-2' to the end and try again
    # (then '-3', etc).
    next = 2
    while not slug or queryset.filter(**{slug_field_name: slug}):
        slug = original_slug
        end = "%s%s" % (slug_separator, next)
        if slug_len and len(slug) + len(end) > slug_len:
            slug = slug[: slug_len - len(end)]
            slug = _slug_strip(slug, slug_separator)
        slug = "%s%s" % (slug, end)
        next += 1

    setattr(instance, slug_field.attname, slug)


def _slug_strip(value, separator="-"):
    """
    Cleans up a slug by removing slug separator characters that occur at the
    beginning or end of a slug.

    If an alternate separator is used, it will also replace any instances of
    the default '-' separator with the new separator.
    """
    separator = separator or ""
    if separator == "-" or not separator:
        re_sep = "-"
    else:
        re_sep = "(?:-|%s)" % re.escape(separator)
    # Remove multiple instances and if an alternate separator is provided,
    # replace the default '-' separator.
    if separator != re_sep:
        value = re.sub("%s+" % re_sep, separator, value)
    # Remove separator from the beginning and end of the slug.
    if separator:
        if separator != "-":
            re_sep = re.escape(separator)
        value = re.sub(r"^%s+|%s+$" % (re_sep, re_sep), "", value)
    return value

import builtins
from urllib.parse import (
    ParseResult,
    parse_qs,
    quote,
    unquote,
    urlencode,
    urlparse,
    urlunparse,
)


def _set_typed_attr(config, name, value):
    attr_type = getattr(builtins, config.__class__.__dataclass_fields__[name].type)
    setattr(config, name, attr_type(value))


def _init_config_from_url(config, url, auth_key_attr="auth_key", auth_secret_attr="auth_secret"):
    if not url:
        return config
    parsed_url = urlparse(url)
    params = None
    if parsed_url.query:
        params = parse_qs(parsed_url.query)
    extra_params = {}
    if params:
        for k, v in params.items():
            attr = k.decode("utf-8") if isinstance(k, bytes) else str(k)
            if hasattr(config, attr):
                _set_typed_attr(config, attr, v)
            else:
                extra_params[k] = v

    if parsed_url.username and auth_key_attr:
        setattr(config, auth_key_attr, unquote(parsed_url.username))
    if parsed_url.password and auth_secret_attr:
        setattr(config, auth_secret_attr, unquote(parsed_url.password))

    new_query = urlencode(extra_params, quote_via=quote)
    new_netloc = "{}:{}".format(parsed_url.hostname, parsed_url.port) if parsed_url.port else parsed_url.hostname
    new_url = ParseResult(
        scheme=parsed_url.scheme,
        netloc=new_netloc,
        path=parsed_url.path,
        params=parsed_url.params,
        query=new_query,
        fragment=parsed_url.fragment,
    )
    config.url = urlunparse(new_url)
    return config


def _str2bool(value):
    return value.lower() in ["true", "1", "t", "y", "yes"]

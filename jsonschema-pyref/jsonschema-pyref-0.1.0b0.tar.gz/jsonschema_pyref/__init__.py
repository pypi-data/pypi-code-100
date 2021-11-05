import json
import os.path as pth
import pkgutil
from functools import lru_cache
from importlib import import_module
from typing import Any, Callable, List, Optional, Type, Union
from urllib.parse import (ParseResult, urljoin as _urllib_urljoin,
                          urlparse as _urllib_urlparse)

from jsonschema import RefResolver as _RefResolver  # type: ignore

try:
    import yaml  # type: ignore
except ImportError:
    yaml = None


__all__ = ['URL_SCHEME_RESOLVERS', 'RefResolver', 'urljoin', 'urlparse',
           'validate']


_JSONTypes = Union[dict, list, str, int, float, bool, None]
_SchemaTypes = Union[dict, bool]


def validate(document: _JSONTypes, schema: _SchemaTypes,
             cls: Optional[Type] = None, *args: Any, **kwargs: Any):
    """
    Drop-in replacement for `jsonschema.validate` which uses the customized
    `jsonschema_pyref.RefResolver` by default.

    >>> from jsonschema_pyref import validate
    >>> schema = {
    ...     'properties': {
    ...         'a': {'$ref': 'py-obj:jsonschema_pyref.examples.schema1'}
    ...     }
    ... }
    ...
    >>> validate({'a': 'hello'}, schema) is None
    True
    """


class RefResolver(_RefResolver):
    """
    Drop-in replacement for `jsonschema.RefResolver` that can resolve
    ``py-obj`` and ``py-pkgdata URLs.

    The easiest way to use it is to initialize it using the
    `~jsonschema.RefResolver.from_schema` method and pass it as a keyword
    argument to `jsonschema.validate`:

    >>> import jsonschema
    >>> from jsonschema_pyref import RefResolver
    >>> schema = {
    ...     'properties': {
    ...         'a': {'$ref': 'py-obj:jsonschema_pyref.examples.schema1'}
    ...     }
    ... }
    ...
    >>> resolver = RefResolver.from_schema(schema)
    >>> jsonschema.validate({'a': 'hello'}, schema, resolver=resolver) is None
    True
    """

    def __init__(self, base_uri: str, referrer: _JSONTypes,
                 store: Union[dict, tuple] = (),
                 cache_remote: bool = True,
                 handlers: Union[dict, tuple] = (),
                 urljoin_cache: Optional[Callable[[str, str], str]] = None,
                 remote_cache: Optional[Callable[[str], dict]] = None) -> None:
        base_handlers = dict(URL_SCHEME_RESOLVERS)
        # Users may still override the builtin handlers for py-obj and
        # py-pkgdata as well as any others
        base_handlers.update(handlers)
        handlers = base_handlers

        # Same for urljoin_cache
        if urljoin_cache is None:
            urljoin_cache = lru_cache(1024)(urljoin)

        super().__init__(base_uri, referrer, store=store,
                         cache_remote=cache_remote,
                         handlers=handlers, urljoin_cache=urljoin_cache,
                         remote_cache=remote_cache)


def urljoin(base: str, url: str, allow_fragments: bool = True) -> str:
    """
    Extends the stdlib's `urllib.parse.urljoin` to support the custom URL
    schemes implemented by this package.

    The join semantics for ``py-obj`` and ``py-pkgdata`` URLs differ from
    those of typical http-like URLs, as well as from each other.

    The rules for ``py-obj`` are as follows:

    * If joined with a "relative" URL, if the URL starts with a Python
      identifier, it is simply appended to the current object path:

      >>> from jsonschema_pyref import urljoin
      >>> urljoin('py-obj:a.b.c', 'd.e')
      'py-obj:a.b.c.d.e'

    * However, if the "relative" URL starts with one or more ``.``, it
      is processed relative to the base path using similar semantics to
      Python relative imports.  That is, one dot means a different attribute
      of the same object, and so on:

      >>> urljoin('py-obj:a.b.c', '.d')
      'py-obj:a.b.d'
      >>> urljoin('py-obj:a.b.c', '..d')
      'py-obj:a.d'
      >>> urljoin('py-obj:a.b.c', '..d.e')
      'py-obj:a.d.e'

    * When joining an absolute URL with the ``py-obj`` scheme, the new URL
      replaces the base:

      >>> urljoin('py-obj:a.b.c', 'py-obj:d.e.f')
      'py-obj:d.e.f'

    * And likewise when joining an absolute URL with an entirely different
      scheme:

      >>> urljoin('py-obj:a.b.c', 'https://example.com')
      'https://example.com'

    * Fragments are dropped from the base URL, and retained from the joined
      URL:

      >>> urljoin('py-obj:a.b.c#replaced', '.d#fragment')
      'py-obj:a.b.d#fragment'
      >>> urljoin('py-obj:a.b.c#replaced', '#fragment')
      'py-obj:a.b.c#fragment'

    The rules for ``py-pkgdata`` are as follows:

    * If joined to a relative URL, it is treated as a different file relative
      to the same package/directory as the base URL, very similarly to how
      `urllib.parse.urljoin` works for relative paths joined to http(s) URLs:

      >>> urljoin('py-pkgdata:a.b.c/schema1.json', 'schema2.json')
      'py-pkgdata:a.b.c/schema2.json'
      >>> urljoin('py-pkgdata:a.b.c/schemas/schema1.json', 'schema2.json')
      'py-pkgdata:a.b.c/schemas/schema2.json'
      >>> urljoin('py-pkgdata:a.b.c/schemas/schema1.json', '../more_schemas/schema2.json')
      'py-pkgdata:a.b.c/more_schemas/schema2.json'

      .. note::

          This does not support relative URLs with a package-relative
          component, only different paths within the same package.  Maybe
          support for this could be added in the future, but under the current
          format it's too ambiguous.

    * When joining an absolute URL, if the joined URL is in the same package
      it works the same as the relative case (effectivly the joined URL
      replaces the base):

      >>> urljoin('py-pkgdata:a.b.c/schema1.json', 'py-pkgdata:a.b.c/schema2.json')
      'py-pkgdata:a.b.c/schema2.json'

    * Likewise when they are different packages:

      >>> urljoin('py-pkgdata:a.b.c/schema1.json', 'py-pkgdata:d.e.f/schema2.json')
      'py-pkgdata:d.e.f/schema2.json'

    * And likewise if they are not the same scheme at all:

      >>> urljoin('py-pkgdata:a.b.c/schema1.json', 'http://example.com/schema2.json')
      'http://example.com/schema2.json'

    * The same rules apply for fragments as with ``py-obj``:

      >>> urljoin('py-pkgdata:a.b.c/schema1.json#replaced', 'schema2.json#fragment')
      'py-pkgdata:a.b.c/schema2.json#fragment'
      >>> urljoin('py-pkgdata:a.b.c/schema1.json#replaced', '#fragment')
      'py-pkgdata:a.b.c/schema1.json#fragment'

    """
    parsedb = urlparse(base)
    if parsedb.scheme in _URL_SCHEME_JOINERS:
        return _URL_SCHEME_JOINERS[parsedb.scheme](base, url)

    return _urllib_urljoin(base, url, allow_fragments=allow_fragments)


def urlparse(url: str) -> ParseResult:
    """
    Extends the stdlib's `urllib.parse.urlparse` to support the custom URL
    schemes implemented by this package.
    """

    if ':' in url:
        scheme, _ = url.split(':', 1)
        if scheme in _URL_SCHEME_PARSERS:
            return _URL_SCHEME_PARSERS[scheme](url)

    return _urllib_urlparse(url)


def _is_dotted_identifier(s: str) -> bool:
    """
    Return True if string is one or more valid Python identifiers separated
    by ``.``.
    """

    s = s.strip()
    if not s:
        return False

    for ident in s.split('.'):
        if not ident.isidentifier():
            return False

    return True


def _resolve_url_py_obj(url: str) -> dict:
    parsed = _urlparse_py_obj(url)
    path = parsed.path
    modname = path
    objpath: List[str] = []
    module = None

    while module is None:
        try:
            module = import_module(modname)
        except ImportError:
            if '.' in path:
                # At least part of the dotted name is the name of the object
                # in the module, and not the module itself.
                modname, objname = modname.rsplit('.', 1)
                objpath.insert(0, objname)
            else:
                raise

    obj = module
    for idx, attr in enumerate(objpath):
        try:
            obj = getattr(obj, attr)
        except Exception:
            raise AttributeError(
                f"no attribute '{attr}' on "
                f"{'.'.join([modname] + objpath[:idx])}")

    if not isinstance(obj, dict):
        raise ValueError(
            f'path {path} does not resolve to a dict, which it must be in '
            f'order to be a JSON Schema')

    return obj


def _resolve_url_py_pkgdata(url: str) -> dict:
    parsed = _urlparse_py_pkgdata(url)
    path = parsed.path
    pkgname, filename = path.split('/', 1)

    _, ext = pth.splitext(filename)

    # TODO: Support more file types and a pluggable registry of loaders for
    # different types--as long as it can be loaded into a dict it can be
    # supported
    yaml_exts = {'.yaml', '.yml'}
    json_exts = {'.json'}
    supported_exts = yaml_exts | json_exts
    data = pkgutil.get_data(pkgname, filename)

    if data is None:
        raise RuntimeError(
            f'no resource named {filename} could be loaded from package '
            f'{pkgname}; see https://docs.python.org/3/library/pkgutil.html#pkgutil.get_data')

    if ext in yaml_exts:
        if yaml is None:
            raise RuntimeError(
                'reading schemas from YAML files requires PyYAML to be '
                'installed: https://pypi.org/project/PyYAML/')

        return yaml.safe_load(data)
    elif ext in json_exts:
        return json.loads(data)
    else:
        supported_exts = yaml_exts | json_exts
        raise ValueError(
            f'schemas are currently only loadable from files with the '
            f'following filename extensions: {sorted(supported_exts)}')


def _urljoin_py_obj(base: str, url: str) -> str:
    parsedb = _urlparse_py_obj(base)
    parsedu = urlparse(url)

    if parsedu.scheme:
        return url

    rel_depth = 0
    pathu = parsedu.path

    while pathu and pathu[0] == '.':
        rel_depth += 1
        pathu = pathu[1:]

    pathb = parsedb.path
    pathb_parts = pathb.split('.')

    if rel_depth > len(pathb_parts):
        raise ValueError(
            f'relative object path {url} outside the original path {base}')

    if rel_depth > 0:
        pathb = '.'.join(pathb_parts[:-rel_depth])

    new_url = 'py-obj:' + pathb

    if pathu:
        new_url += '.' + pathu

    if parsedu.fragment:
        new_url += '#' + parsedu.fragment

    return new_url


def _urljoin_py_pkgdata(base: str, url: str) -> str:
    # This follows similar semantics to normal URL joins w.r.t. the filename
    # path, so we actually pass this to urljoin but without the scheme (which
    # it doesn't recognize)
    parsedb = _urlparse_py_pkgdata(base)
    parsedu = urlparse(url)

    # If url is an absolute url with a scheme, what we do depends on the
    # scheme:
    # * If also py-pkgdata, check if the package names match; if so join just
    #   the filename, if not replace both the package name and the filename.
    #   This is a bit similar to stdlib urljoin() semantics for http URLs
    #
    # * If different scheme, also replace the base URL enirely.
    if parsedu.scheme == parsedb.scheme:
        pkgb, filenameb = parsedb.path.split('/', 1)
        pkgu, filenameu = parsedu.path.split('/', 1)
        if pkgb == pkgu:
            new_path = _urllib_urljoin(parsedb.path, filenameu)
        else:
            return url
    elif parsedu.scheme:
        # Some other scheme
        return url
    else:
        # A relative URL relative to the base py-pkgdata URL
        new_path = _urllib_urljoin(parsedb.path, parsedu.path)

    if parsedu.fragment:
        new_path += '#' + parsedu.fragment

    return 'py-pkgdata:' + new_path


def _urlparse_py_obj(url: str) -> ParseResult:
    """Parse URLs with the ``py-obj:`` scheme."""

    if not url.startswith('py-obj:'):
        raise ValueError(f'not a py-obj URL: {url}')

    _, rest = url.split(':', 1)
    if '#' in rest:
        path, fragment = rest.split('#', 1)
    else:
        path, fragment = rest, ''

    if not _is_dotted_identifier(path):
        fmt = 'py-obj:<identifier>[.<identifier>...][#<fragment>]'

        raise ValueError(
            f'py-obj URL path component {path} contains an invalid Python '
            f'indentifier; the correct format for a py-obj URL is: {fmt}')

    return ParseResult(scheme='py-obj', netloc='', path=path, params='',
                       query='', fragment=fragment)


def _urlparse_py_pkgdata(url: str) -> ParseResult:
    """Parse URLs with the ``py-pkgdata:`` scheme."""

    if not url.startswith('py-pkgdata:'):
        raise ValueError(f'not a py-pkgdata URL: {url}')

    _, rest = url.split(':', 1)
    if '#' in rest:
        path, fragment = rest.split('#', 1)
    else:
        path, fragment = rest, ''

    path = path.strip()
    fmt = 'py-pkgdata:<module>[.<module>...]/<path>[#<fragment>]'

    if '/' in path:
        module, filename = path.split('/', 1)
    else:
        module, filename = path, ''

    filename = filename.strip()

    if not filename:
        raise ValueError(
            f'py-pkgdata URL must contain a package-relative path to a file '
            f'contained in the package, starting with a "/"; the correct '
            f'format for a py-pkgdata URL is: {fmt}')

    if not _is_dotted_identifier(module):
        raise ValueError(
            f'py-obj URL module component {module} is not a valid Python '
            f'indentifier; the correct format for a py-obj URL is: {fmt}')

    return ParseResult(scheme='py-pkgdata', netloc='',
                       path=f'{module}/{filename}', params='', query='',
                       fragment=fragment)


URL_SCHEME_RESOLVERS = {
    'py-obj': _resolve_url_py_obj,
    'py-pkgdata': _resolve_url_py_pkgdata
}
"""
Additional URL handlers for the custom URL schemes supported by this package.

This can be passed to the ``handlers`` argument of `jsonschema.RefResolver`,
but take note: It is also necessary to override the ``urljoin_cache`` argument
to use `jsonschema_pyref.urljoin` as follows::

    >>> import jonschema
    >>> from jsonschema_pyref import URL_SCHEME_RESOLVERS, urljoin
    >>> from functools import lru_cache
    >>> resolver = RefResolver({}, {}, handlers=URL_SCHEME_RESOLVERS,
    ...                        urljoin_cache=lru_cache(1024)(urljoin))

This boilerplate can be avoided entirely by using the supplied
`jsonschema_pyref.RefResolver` which has these enhancements by default (and
is otherwise identical to `jsonschema.RefResolver`).
"""


_URL_SCHEME_JOINERS = {
    'py-obj': _urljoin_py_obj,
    'py-pkgdata': _urljoin_py_pkgdata
}


_URL_SCHEME_PARSERS = {
    'py-obj': _urlparse_py_obj,
    'py-pkgdata': _urlparse_py_pkgdata
}

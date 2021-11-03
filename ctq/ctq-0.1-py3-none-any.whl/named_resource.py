from .acquisition import acquire
from .traversal import resource_path_names
from functools import partial
from typing import Any
from typing import Callable
from typing import Iterable
from typing import Optional


class Resourceful(object):
    """Add a get item behavior to an object in order for that object to expose
    subobjects through self[name] that are defined with the ``@resource``
    decorator.
    """

    _ctq_named_resource_cache: Optional[
        dict
    ] = None  # Used by NamedResourceFactoryProperty

    def _ctq_get_named_resource(self, name: str) -> Any:
        """Return a named resource

        named resources are traversable by self[name], this function when called
        by __getitem__ searches the class object for wrapped methods that inherit
        NamedResrouceFactoryDecorator with the matching ``name`` property. After
        a match is found the attribute of the same name on the instance is called
        and the result returned.

        Arguments:
            name: The name of the tinterface. This must be a string.

        Returns:

            The object being request. None otherwise.
        """
        cls = type(self)
        for attribute_name in dir(cls):
            cls_attribute = getattr(cls, attribute_name, None)
            if (
                isinstance(cls_attribute, NamedResourceFactoryProperty)
                and cls_attribute.name == name
            ):
                factory = getattr(self, attribute_name)
                return factory()
        return None

    def __getitem__(self, key: str) -> Any:
        """Returns: the result of of calling ``_ctq_get_named_resource``. If the result is
        None, either because there is no named resource or because the recource factory
        also returned ``None``, then super's __getitem__ is consulted.
        """
        item = self._ctq_get_named_resource(key)
        if item is not None:
            return item
        else:
            try:
                super_getitem = super().__getitem__
            except AttributeError as e:
                raise KeyError(key) from e
            return super_getitem()


def resource(name: str, no_cache: bool = False, no_parent: bool = False) -> Callable:
    """Decorator which wraps an item factory to create a resource for the item
    ``name`` for a class that inherts from ``Resourceful``. This should allow
    retreival of an item using ``self[name]``

    Unless ``no_parent`` is set, the wrapper will set ``__name__`` and
    ``__parent__`` if the resource producted by the factory doens't already
    have those attributes.

    Args:

        name: The name that should be used to access the resource using the
        ``self[name]`` syntax

        no_cache: Don't cache the resource for subsiquent ``self[name]``
        expressions

        no_parent: Don't set ``__parent__`` and ``__name__`` on newly generated
        resoures.

    Returns:

        A callable which wrapps a factory and returns an instance of
        ``NamedResourceFactoryProperty``

    """
    return partial(NamedResourceFactoryProperty, name, no_cache, no_parent)


def iter_named_resources(obj: Any) -> Iterable[Any]:
    """Returns: an iterable of each named resource in the object"""
    cls = type(obj)
    for attribute_name in dir(cls):
        cls_attribute = getattr(cls, attribute_name, None)
        if isinstance(cls_attribute, NamedResourceFactoryProperty):
            factory = getattr(obj, attribute_name)
            item = factory()
            if item is not None:
                yield factory()


class NamedResourceFactoryProperty(object):
    """Property-ish object which annotates a factory and processes factory
    items for caching binding into a resource tree with ``__name__`` and
    ``__parent__`` attributes
    """

    def __init__(self, name: str, no_cache: bool, no_parent: bool, factory: Callable):
        """Initialize a property object.

        Args:

            name: The name to be used when accessing the resource object with
            ``inst[name]``

            no_cache: Do not save a generated resource into a cache.

            no_parent: Do not bind a generated resource to the parent instance
            or set its name.
        """
        self.name = name
        self.factory = factory
        self.no_cache = no_cache
        self.no_parent = no_parent

    def __get__(self, inst: Optional[Resourceful], owner) -> Callable:
        """Returns: The ``NamedResourceFactoryProperty`` object for the class
        object and a callable wrapping ``self.instance_get_resource`` for the
        instance object.
        """
        if inst is None:
            return self
        else:
            return partial(self.instance_get_resource, inst)

    def instance_get_resource(self, inst: Resourceful) -> Any:
        """Get the resource object for a given ``self.name`` on an instance.

        Consult caches or or the resource factory in oder to obtain a resource
        object. Optionally bind the object into the resource tree and save
        back to caches.

        Returns:

            A resource object.
        """
        resource = self.cache_get(inst)
        if resource is not None:
            return resource

        resource = self.factory(inst)

        if resource is None:
            return None

        if not self.no_parent:
            self.bind_resource_to_tree(inst, resource)

        if not self.no_cache:
            self.cache_set(inst, resource)

        return resource

    def cache_get(self, inst: Resourceful) -> Optional[object]:
        """Returns: A reources object if present in a cache. ``None`` if absent
        of a cache
        """
        # Check if there is a resource_cache_get through acquire()
        resource_cache_get = getattr(acquire(inst), "resource_cache_get", None)
        
        if resource_cache_get:
            base_path_names = resource_path_names(inst)
            if base_path_names is not None:  # Can't resolve path names
                path_names = base_path_names + (self.name,)
                cached_resource = resource_cache_get(path_names)
                if cached_resource is not None:
                    return cached_resource

        # Check the _ctq_named_resource_cache on the instance
        if inst._ctq_named_resource_cache is not None:
            cached_resource = inst._ctq_named_resource_cache.get(self.name, None)
            if cached_resource is not None:
                return cached_resource

        return None

    def cache_set(self, inst: Resourceful, resource: Any):
        """Save a resource into a cache."""
        resource_cache_set = getattr(acquire(inst), "resource_cache_set", None)
        if resource_cache_set is not None:
            base_path_names = resource_path_names(inst)
            if base_path_names is not None:  # Can't resolve path names
                path_names = base_path_names + (self.name,)
                resource_cache_set(path_names, resource)
                return

        if inst._ctq_named_resource_cache is None:
            inst._ctq_named_resource_cache = {self.name: resource}
        else:
            inst._ctq_named_resource_cache[self.name] = resource

    def bind_resource_to_tree(self, inst: Resourceful, resource: Any):
        """Annotate a resource object binding it to a resource tree by setting
        ``__parent__`` and ``__name__`` if they don't already exist.

        Args:

            inst: The parent object to bind the resource to.

            resource: The object to annotate.
        """
        if not hasattr(resource, "__name__"):
            resource.__name__ = self.name

        if not hasattr(resource, "__parent__"):
            resource.__parent__ = inst

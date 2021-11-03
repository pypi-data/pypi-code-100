"""A events implementation.

cqt provides a function ``emit(target: Any, name: str, data: Optional[dict])`` which
creates an event object, searches and calls event handlers starting with the target
and bubbeling up to the root of a resource tree.

Event handlers can be declared using the ``@handle(name: str, priority: Optional[int])`` decorator on an
instance method which accepts the paramiter ``event``.

For example::

    >>> class Root(object):
    ...
    ...     @handle('after-edit')
    ...     def on_after_edit(self, event):
    ...         print("Was very edited.")

    >>> class Foo(object):
    ...
    ...     @handle('after-edit')
    ...     def on_after_edit(self, event):
    ...         print("Was edited.")

    >>> foo = Foo()
    >>> foo.__parent__ Root()
    >>> emit(foo, 'after-edit')
    Was edited.
    Was very edited.

"""
from functools import partial
from typing import Any
from typing import Optional


def handle(*event_names, target=None, priority=None):
    """Create an EventHandlerProperty from an instance method. The instance method
    is to accept two arguments - self, event.

    Args:

        *event_names: The event names that the function is to handle.

        target: The type of target to handle for.

        priority: An int priority indicating that an event handler should be
        called before others. Lower numbers are called first.
    """
    return partial(
        EventHandlerProperty,
        event_names=event_names,
        target=target,
        priority=priority,
    )


def emit(target: Any, name: str, data: Optional[dict] = None):
    """Create an event and call matching event handlers starting with the target
    bubbling up to the root of a resource tree.

    Args:

        target: The ressource objet to emit the event on.

        name: The name of the event. This will be used to match event handlers.

        data: Extra dictionary data to be available on event.data
    """
    data = data or {}
    event = Event(target, name, data)
    for decorated, bound_handler in get_event_handlers(target):
        if decorated.match(event):
            bound_handler(event)


class Event(object):
    """An event object that is passed as an argument to event handlers.

    Attributes:

        target: The resource object the event was emmited on

        name: The name of the event

        data: Abitrary data passed as the ``data`` argument in emit
    """

    def __init__(self, target: Any, name: str, data: dict = None):
        """Initializse and event

        Args:
            target: The resource object the event was emmited on

            name: The name of the event

            data: Abitrary data passed as the ``data`` argument in emit
        """
        self.target = target
        self.name = name
        self.data = data


def get_event_handlers(target: Any) -> list[tuple]:
    """Returns a list of two item tuples (EventHandlerProperty
    instance, bound_handler) from this object and its parents.
    """
    event_handlers_cache = getattr(target, "_ctq_event_handlers_cache", None)
    if event_handlers_cache is not None:
        return event_handlers_cache

    # Get event handlers for target
    ordered = []
    unordered = []
    cls = type(target)
    for attribute_name in dir(cls):
        cls_item = getattr(cls, attribute_name, None)
        if isinstance(cls_item, EventHandlerProperty):
            bound_handler = getattr(target, attribute_name)
            if cls_item.priority is not None:
                ordered.append((cls_item, bound_handler))
            else:
                unordered.append((cls_item, bound_handler))
    ordered.sort(key=lambda h: h[0].priority)

    # get parent event handlers
    parent = getattr(target, "__parent__", None)
    if parent:
        parent_handlers = get_event_handlers(parent)
    else:
        parent_handlers = []

    # Combine, cache and return
    handlers = [*ordered, *unordered, *parent_handlers]
    target._ctq_event_handlers_cache = handlers
    return handlers


class EventHandlerProperty(object):
    """Property class of an event handler.

    This wraps an event handler function. On the class it exposes event handler
    meta data and on the class instance provides the handler function itself
    """

    def __init__(self, handler, event_names=None, target=None, priority=None):
        """Initialize property

        Args:

            handler: A function able to receive event objects when called.

            event_names: A list of names that the event handler is valid for

            target: The type of target to select for event handeling

            priority: An optional numerical priority number which allows some
            event handlers to be called first
        """
        self.handler = handler
        self.event_names = event_names
        self.target = target
        self.priority = priority
        self.owner = None  # Set during __get__
        if hasattr(handler, "__doc__"):
            self.__doc__ = handler.__doc__

    def match(self, event):
        """Returns: True if the event matches this handler otherwise None"""
        return self.match_name(event) and self.match_for_target(event)

    def match_name(self, event):
        """Returns: True if the event matches the event name"""
        if self.event_names is None:
            return True
        else:
            return event.name in self.event_names

    def match_for_target(self, event):
        """Returns: True if the event target matches the event target_for"""
        if self.target is None:
            return True
        if self.target == "self":
            assert self.owner
            return isinstance(event.target, self.owner)
        else:
            return isinstance(event.target, self.target)

    def __get__(self, inst, owner):
        """Some serious depp python stuff going on here....

        The get magic method allows an object to behave as a class property such as @property.
        It returns the attribute of the owner instance or owner class depending on if the
        attribute that is accessed is on the instance or the class object. E.g. A.foo and A().foo
        both call the __get__ method for a propertyish object "foo". In our case we want
        self to be returned on the class object so the named resource is discoverable by
        iterating the class objects contents and testing isinstance, yet the instance of the
        class needs the function to be working too. See also the named resource decorator.
        """
        self.owner = owner

        if inst is None:
            # the attribute access is on the class object
            return self

        # return a wrapped handler method for an attribute on an instance object
        return partial(self.handler, inst)

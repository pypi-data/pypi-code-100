# MIT License

# Copyright (c) 2021 AIOCord

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Dyspatch
~~~~~~~~

A simple package for dispatching and managing events asynchronously.
"""
from __future__ import annotations
from typing import List, Callable, Any

from inspect import iscoroutinefunction
import asyncio

__author__  = 'nerdguyahmad <nerdguyahmad.contact@gmail.com>'
__version__ = '0.0.1'


EventListener = Callable[..., Any]

class Events:
    """
    Represents the core class where all the events and listeners for them are stored
    and handled.

    Parameters
    ----------
    loop: :class:`asyncio.AbstractEventLoop`
        The event loop, if not provided, it is obtained by :meth:`asyncio.get_event_loop`
    """
    _listeners: Dict[str, List[EventListener]]

    def __init__(self, *, loop: asyncio.AbstractEventLoop = None):
        self._listeners = {}

    @property
    def listeners(self) -> Dict[str, List[EventListener]]:
        """Returns a mapping of event name to list of listeners attached to the event."""
        return self._listeners

    def get_listeners(self, event: str, *, fail_if_not_exist: bool = False):
        """
        Gets all the listeners for the provided event.

        Parameters
        ----------
        event: :class:`str`
            The name of event to get listeners of.
        """
        return self._listeners.get(event, [])

    def clear_listeners(self, event: str, *, fail_if_not_exist: bool = False) -> None:
        """
        Removes the listeners for provided event.

        This method by default, doesn't raise any error if the ``event``
        is not in :attr:`~.listeners` but ``fail_if_not_exist`` can be set
        to ``True`` to raise error.

        Parameters
        ----------
        event: :class:`str`
            The name of event to clear listeners of.
        fail_if_not_exist: :class:`bool`
            Whether to raise error if no listeners exist for the provided
            event. Defaults to ``False``
        """
        try:
            del self._listeners[event]
        except KeyError:
            if fail_if_not_exist:
                raise RuntimeError(f'No listeners exist for event {event!r}')

    def add_listener(self,
        event: str,
        callback: EventListener,
        *,
        once: bool = False,
        ):
        """
        Adds a listener.

        Parameters
        ----------
        event: :class:`str`
            The name of event to create listener for.
        callback:
            The async-function aka coroutine that represents the callback
            of the event.
        once: :class:`bool`
            Whether the listener is one-time call only which means
            the listener will be removed after it has been dispatched once.
        """
        if not event in self._listeners:
            self._listeners[event] = []

        if once:
            callback.__dyspatch_call_once__ = True

        self._listeners[event].append(callback)

    def _schedule(self, listener: EventListener, args: Sequence[str], kwargs: Mapping[str, Any]):
        return asyncio.ensure_future(listener(*args, **kwargs))

    def dispatch(self,
        event: str,
        args: Sequence[str] = None,
        kwargs: Mapping[str, Any] = None,
        *,
        fail_if_not_exist: bool = False,
        ):
        """
        Dispatches the event as such, calls all the listeners for the provided
        event with provided data.

        Parameters
        ----------
        event: :class:`str`
            The name of event to dispatch.
        args:
            The sequence of positional arguments to pass to the listeners.
        kwargs:
            The mapping of keyword arguments to pass to the listeners.
        fail_if_not_exist: :class:`bool`
            Whether to raise error if no event listener is found for event or not.
            Defaults to False.
        """
        try:
            listeners = self._listeners[event]
        except KeyError:
            if fail_if_not_exist:
                raise RuntimeError(f'no event listeners found for event {event!r}')
            return

        if args is None:
            args = ()
        if kwargs is None:
            kwargs = {}

        to_remove: List[EventListener] = []

        for listener in listeners:
            try:
                once = listener.__dyspatch_call_once__
            except AttributeError:
                once = False

            if iscoroutinefunction(listener):
                self._schedule(listener, args, kwargs)
            else:
                listener(*args, **kwargs)

            if once:
                to_remove.append(listener)

        for listener in to_remove:
            try:
                self._listeners[event].remove(listener)
            except Exception:
                continue
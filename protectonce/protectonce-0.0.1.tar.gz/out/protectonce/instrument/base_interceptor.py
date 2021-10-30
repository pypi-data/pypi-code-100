import importlib
from abc import ABC, abstractmethod

from .po_exceptions import SecurityException

from wrapt import FunctionWrapper


class BaseInterceptor(ABC):
    def __init__(self, mod, cls, methods, handlers) -> None:
        self._module = mod
        self._class = cls
        self._handlers = handlers
        self._save_methods(methods)

    def pre_callbacks(self, method_name, *args, **kwargs):
        self.__handle_callbacks('before', self._handlers.before,
                                method_name, args, kwargs, None)

    def post_callbacks(self, method_name, result, *args, **kwargs):
        self.__handle_callbacks('after', self._handlers.after,
                                method_name, args, kwargs, result)

    def __handle_callbacks(self, type, handlers, method_name, args, kwargs, result):
        for handler in handlers:
            method_data = self._methods.get(method_name, {})

            if type == 'before':
                result = handler.handle_before(method_data, args, kwargs)
            elif type == 'after':
                result = handler.handle_after(
                    method_data, args, kwargs, result)
            else:
                print(f'Invalid handler type: {type}') # TODO: Logging

            if result == False:
                raise SecurityException("Malicious input blocked")

    @abstractmethod
    def intercept(self):
        raise NotImplementedError

    def _wrap_method(self, method, wrapper) -> None:
        mod = self._module
        if isinstance(self._module, str):
            mod = importlib.import_module(self._module)
            mod = getattr(mod, self._class, mod)

        fn = getattr(mod, method)

        fw = FunctionWrapper(fn, wrapper)
        setattr(mod, method, fw)

    def _save_methods(self, methods):
        self._methods = {}
        for method in methods:
            _method = {}
            _method['args'] = method.get('args', [])
            _method['kwargs'] = method.get('kwargs', [])

            method_name = method.get('method', None)
            _method['method'] = method_name
            if method_name:
                self._methods[method_name] = _method

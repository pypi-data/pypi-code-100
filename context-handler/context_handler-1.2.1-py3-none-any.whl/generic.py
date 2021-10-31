import typing

from context_handler import _datastructures, ensure_context, getters

GenericContextFactoryT = typing.TypeVar(
    "GenericContextFactoryT", bound="_GenericContextFactory"
)
AsyncGenericContextFactoryT = typing.TypeVar(
    "AsyncGenericContextFactoryT", bound="_GenericAsyncContextFactory"
)
ClientT = typing.TypeVar("ClientT")
ProviderT = typing.TypeVar("ProviderT", bound=_datastructures.Provider)
AsyncProviderT = typing.TypeVar(
    "AsyncProviderT", bound=_datastructures.AsyncProvider
)


class _GenericContextFactory:
    _factory: _datastructures.AbstractSyncContextFactory

    def __class_getitem__(
        cls: typing.Type[GenericContextFactoryT],
        params: typing.Tuple[
            typing.Type[_datastructures.Provider], typing.Type
        ],
    ) -> GenericContextFactoryT:
        if len(params) != 2:
            raise NotImplementedError
        provider_class = params[0]
        context_class = ensure_context._guess_context_class(provider_class)
        new_t = type("{}[{}]".format(cls.__name__, ",".join(param.__name__ for param in params)), (cls,), {"_factory": getters.context_factory(provider_class, context_class)})  # type: ignore
        return new_t  # type: ignore

    def __init__(self, has_state: _datastructures.HasState):
        self._context = self._factory(has_state)

    def get(self):
        return self._context


class _GenericAsyncContextFactory:
    _factory: _datastructures.AbstractAsyncContextFactory

    def __class_getitem__(
        cls: typing.Type[AsyncGenericContextFactoryT],
        params: typing.Tuple[typing.Type[_datastructures.Provider], ...],
    ) -> AsyncGenericContextFactoryT:
        if len(params) != 2:
            raise NotImplementedError
        provider_class = params[0]
        context_class = ensure_context._guess_context_class(provider_class)
        new_t = type("{}[{}]".format(cls.__name__, ",".join(param.__name__ for param in params)), (cls,), {"_factory": getters.context_factory(provider_class, context_class)})  # type: ignore
        return new_t  # type: ignore

    def __init__(self, has_state: _datastructures.HasState):
        self._context = self._factory(has_state)

    def get(self):
        return self._context


class GenericFactory(
    _GenericContextFactory, typing.Generic[ProviderT, ClientT]
):
    def get(self) -> _datastructures.AbstractSyncContext[ClientT]:
        return super().get()


class AsyncGenericFactory(
    _GenericAsyncContextFactory,
    typing.Generic[AsyncProviderT, ClientT],
):
    def get(self) -> _datastructures.AbstractAsyncContext[ClientT]:
        return super().get()

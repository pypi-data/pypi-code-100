from typing import Callable, List, Dict, Any

from sqlalchemy.exc import UnboundExecutionError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.horizontal_shard import ShardedSession
from sqlalchemy.orm import Session

from constellate.database.sqlalchemy.sqlalchemydbconfigmanager import SQLAlchemyDbConfigManager


class _GetBindResolver:
    def _get_bind_resolve(self, mapper=None, clause=None, resolvers: List[Callable] = None):
        try:
            return resolvers[0](mapper=mapper, clause=clause)
        except UnboundExecutionError:
            return resolvers[1](mapper=mapper, clause=clause)

    def _get_bind_build_resolvers_order(
        self, bind_priority: str = None, resolvers: List[Callable] = None
    ):
        return list(resolvers if bind_priority == "sqlalchemy" else reversed(resolvers))


class _ConfigManager:
    @property
    def config_manager(self):
        return self._config_manager


class _InjectDefaultExecutionOptions:
    def _inject_default_execution_options(self, kw: Dict = {}):
        default_execution_options = self._default_execution_options or {}
        execution_options = kw.get("execution_options", default_execution_options)

        no_value = object()
        for key, value in default_execution_options.items():
            current_value = execution_options.get(key, no_value)
            if current_value == no_value:
                # Set default execution option value
                execution_options.update({key: value})
            else:
                # Do not use default execution option value
                pass
        kw.update({"execution_options": execution_options})


def extract_param_when_available(kwargs: Dict = {}, key: Any = None, default_value: Any = None):
    return kwargs.pop(key) if key in kwargs else default_value


class MultiEngineSession(
    AsyncSession, _GetBindResolver, _InjectDefaultExecutionOptions, _ConfigManager
):
    def __init__(
        self,
        owner=None,
        config_manager: SQLAlchemyDbConfigManager = None,
        bind_priority: str = "sqlalchemy",
        **kwargs
    ):
        has_custom_sync_session_class = "sync_session_class" in kwargs

        if has_custom_sync_session_class:
            execution_options = kwargs.get("execution_options", {})
            kwargs.update({"owner": owner, "config_manager": config_manager})
        else:
            # Extracting execution_options from kwargs because super.init is not
            # supporting said param
            execution_options = extract_param_when_available(
                kwargs=kwargs, key="execution_options", default_value={}
            )

        super().__init__(**kwargs)
        self._owner = owner
        self._config_manager = config_manager
        self._default_execution_options = execution_options
        self._get_bind_resolvers = self._get_bind_build_resolvers_order(
            bind_priority=bind_priority, resolvers=[super().get_bind, self._get_bind]
        )

    def get_bind(self, mapper=None, clause=None):
        return self._get_bind_resolve(
            mapper=mapper, clause=clause, resolvers=self._get_bind_resolvers
        )

    def _get_bind(self, mapper=None, clause=None):
        # clause = SELECT * FROM ....
        # mapper = Class being used to access a table. Eg: TradeR
        raise UnboundExecutionError()

    async def execute(self, statement, **kw):
        self._inject_default_execution_options(kw=kw)
        return await super().execute(statement, **kw)

    async def connection(self, **kw):
        self._inject_default_execution_options(kw=kw)
        return await super().connection(**kw)


class SyncMultiEngineSession(
    Session, _GetBindResolver, _InjectDefaultExecutionOptions, _ConfigManager
):
    def __init__(
        self,
        owner=None,
        config_manager: SQLAlchemyDbConfigManager = None,
        bind_priority: str = "sqlalchemy",
        **kwargs
    ):
        # Extracting execution_options from kwargs because super.init is not supporting said param
        execution_options = extract_param_when_available(
            kwargs=kwargs, key="execution_options", default_value={}
        )
        super().__init__(**kwargs)
        self._owner = owner
        self._config_manager = config_manager
        self._default_execution_options = execution_options
        self._get_bind_resolvers = self._get_bind_build_resolvers_order(
            bind_priority=bind_priority, resolvers=[super().get_bind, self._get_bind]
        )

    def get_bind(self, mapper=None, clause=None):
        return self._get_bind_resolve(
            mapper=mapper, clause=clause, resolvers=self._get_bind_resolvers
        )

    def _get_bind(self, mapper=None, clause=None):
        raise UnboundExecutionError()

    def execute(self, statement, **kw):
        self._inject_default_execution_options(kw=kw)
        return super().execute(statement, **kw)

    def connection(self, **kw):
        self._inject_default_execution_options(kw=kw)
        return super().connection(**kw)


class SyncMultiEngineShardSession(
    ShardedSession, _GetBindResolver, _InjectDefaultExecutionOptions, _ConfigManager
):
    def __init__(
        self,
        owner=None,
        config_manager: SQLAlchemyDbConfigManager = None,
        bind_priority: str = "sqlalchemy",
        **kwargs
    ):
        # Unsupported params in parent class
        execution_options = extract_param_when_available(
            kwargs=kwargs, key="execution_options", default_value={}
        )
        super().__init__(**kwargs)
        self._owner = owner
        self._config_manager = config_manager
        self._default_execution_options = execution_options
        self._get_bind_resolvers = self._get_bind_build_resolvers_order(
            bind_priority=bind_priority, resolvers=[super().get_bind, self._get_bind]
        )

    def get_bind(self, mapper=None, clause=None):
        return self._get_bind_resolve(
            mapper=mapper, clause=clause, resolvers=self._get_bind_resolvers
        )

    def _get_bind(self, mapper=None, clause=None):
        raise UnboundExecutionError()

    def execute(self, statement, **kw):
        self._inject_default_execution_options(kw=kw)
        return super().execute(statement, **kw)

    def connection(self, **kw):
        self._inject_default_execution_options(kw=kw)
        return super().connection(**kw)

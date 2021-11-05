from typing import Callable, List

from sqlalchemy.exc import UnboundExecutionError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.horizontal_shard import ShardedSession
from sqlalchemy.orm import Session

from constellate.database.sqlalchemy.sqlalchemydbconfigmanager import SQLAlchemyDbConfigManager


class _GetBindResolver:
    def _get_bind_resolver(self, mapper=None, clause=None, get_bind_fns: List[Callable] = None):
        try:
            return get_bind_fns[0](mapper=mapper, clause=clause)
        except UnboundExecutionError:
            return get_bind_fns[1](mapper=mapper, clause=clause)


class _ConfigManager:
    @property
    def config_manager(self):
        return self._config_manager


class MultiEngineSession(AsyncSession, _GetBindResolver, _ConfigManager):
    def __init__(
        self,
        owner=None,
        config_manager: SQLAlchemyDbConfigManager = None,
        bind_priority: str = "sqlalchemy",
        **kwargs
    ):
        has_custom_sync_session_class = "sync_session_class" in kwargs
        execution_options = kwargs.get("execution_options", None)
        if has_custom_sync_session_class:
            kwargs.update({"owner": owner, "config_manager": config_manager})
        else:
            kwargs.pop("execution_options", None)

        super().__init__(**kwargs)
        self._owner = owner
        self._config_manager = config_manager
        self._execution_options = execution_options
        self._bind_priority = bind_priority

        get_bind_fns = [super().get_bind, self._get_bind]
        self._get_bind_fns = list(
            get_bind_fns if bind_priority == "sqlalchemy" else reversed(get_bind_fns)
        )

    def get_bind(self, mapper=None, clause=None):
        return self._get_bind_resolver(
            mapper=mapper, clause=clause, get_bind_fns=self._get_bind_fns
        )

    def _get_bind(self, mapper=None, clause=None):
        # clause = SELECT * FROM ....
        # mapper = Class being used to access a table. Eg: TradeR
        raise UnboundExecutionError()


class SyncMultiEngineSession(Session, _GetBindResolver, _ConfigManager):
    def __init__(
        self,
        owner=None,
        config_manager: SQLAlchemyDbConfigManager = None,
        bind_priority: str = "sqlalchemy",
        **kwargs
    ):
        # Extracting execution_options from kwargs because super.init is not supporting said param
        execution_options = (
            kwargs.pop("execution_options") if "execution_options" in kwargs else None
        )
        super().__init__(**kwargs)
        self._owner = owner
        self._config_manager = config_manager
        self._execution_options = execution_options
        self._bind_priority = bind_priority

        get_bind_fns = [super().get_bind, self._get_bind]
        self._get_bind_fns = list(
            get_bind_fns if bind_priority == "sqlalchemy" else reversed(get_bind_fns)
        )

    def get_bind(self, mapper=None, clause=None):
        return self._get_bind_resolver(
            mapper=mapper, clause=clause, get_bind_fns=self._get_bind_fns
        )

    def _get_bind(self, mapper=None, clause=None):
        raise UnboundExecutionError()


class SyncMultiEngineShardSession(ShardedSession, _GetBindResolver, _ConfigManager):
    def __init__(
        self,
        owner=None,
        config_manager: SQLAlchemyDbConfigManager = None,
        bind_priority: str = "sqlalchemy",
        **kwargs
    ):
        # Extracting execution_options from kwargs because super.init is not supporting said param
        execution_options = (
            kwargs.pop("execution_options") if "execution_options" in kwargs else None
        )
        super().__init__(**kwargs)
        self._owner = owner
        self._config_manager = config_manager
        self._execution_options = execution_options
        self._bind_priority = bind_priority

        get_bind_fns = [super().get_bind, self._get_bind]
        self._get_bind_fns = list(
            get_bind_fns if bind_priority == "sqlalchemy" else reversed(get_bind_fns)
        )

    def get_bind(self, mapper=None, clause=None):
        return self._get_bind_resolver(
            mapper=mapper, clause=clause, get_bind_fns=self._get_bind_fns
        )

    def _get_bind(self, mapper=None, clause=None):
        raise UnboundExecutionError()

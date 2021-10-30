from sqlalchemy.exc import UnboundExecutionError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from constellate.database.sqlalchemy.sqlalchemydbconfigmanager import SQLAlchemyDbConfigManager


class MultiEngineSession(AsyncSession):
    def __init__(self, owner=None, config_manager: SQLAlchemyDbConfigManager = None, **kwargs):
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

    @property
    def config_manager(self):
        return self._config_manager

    def get_bind(self, mapper=None, clause=None):
        try:
            return super().get_bind(mapper=mapper, clause=clause)
        except UnboundExecutionError:
            return self._get_bind(mapper=mapper, clause=clause)

    def _get_bind(self, mapper=None, clause=None):
        # clause = SELECT * FROM ....
        # mapper = Class being used to access a table. Eg: TradeR
        raise NotImplementedError()


class SyncMultiEngineSession(Session):
    def __init__(self, owner=None, config_manager: SQLAlchemyDbConfigManager = None, **kwargs):
        # Extracting execution_options from kwargs because super.init is not supporting said param
        execution_options = (
            kwargs.pop("execution_options") if "execution_options" in kwargs else None
        )
        super().__init__(**kwargs)
        self._owner = owner
        self._config_manager = config_manager
        self._execution_options = execution_options

    @property
    def config_manager(self):
        return self._config_manager

    def get_bind(self, mapper=None, clause=None):
        try:
            return super().get_bind(mapper=mapper, clause=clause)
        except UnboundExecutionError:
            return self._get_bind(mapper=mapper, clause=clause)

    def _get_bind(self, mapper=None, clause=None):
        raise NotImplementedError()

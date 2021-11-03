"""handler for settings"""
from datetime import datetime
from uuid import UUID

from peewee import DoesNotExist
from requests.exceptions import ConnectionError as RequestConnectionError

from timeslime.handler import DatabaseHandler, TimeslimeServerHandler
from timeslime.handler.state_handler import StateHandler
from timeslime.models import Setting


class SettingsHandler:
    """ "class for setting handler"""

    def __init__(
        self,
        database_handler: DatabaseHandler,
        state_handler: StateHandler = None,
        timeslime_server_handler: TimeslimeServerHandler = None,
    ):
        self.database_handler = database_handler
        self.state_handler = state_handler
        self.timeslime_server_handler = timeslime_server_handler
        self._set_timeslime_server_handler()

    def _set_timeslime_server_handler(self):
        if self.timeslime_server_handler is not None:
            return

        if self.contains("timeslime_server"):
            setting = self.get("timeslime_server")
            self.timeslime_server_handler = TimeslimeServerHandler(setting.value)
        else:
            self.timeslime_server_handler = None

    def set(self, key: str, value: str, setting_id: UUID = None):
        """set a setting
        :param key: defines settings key
        :param value: defines settings value (could be None)
        :param id: defines settings key (default: set automatically)"""
        setting = Setting()
        if setting_id:
            setting.id = setting_id
        setting.key = key
        setting.value = value
        self.database_handler.save_setting(setting)
        if self.timeslime_server_handler is not None:
            try:
                self.timeslime_server_handler.send_setting(setting)
            except RequestConnectionError:
                pass

    def get(self, key: str) -> Setting:
        return self.database_handler.read_setting(key)

    def get_all(self, date: datetime = None) -> list:
        """get all settings"""
        return self.database_handler.read_settings(date)

    def delete(self, key: str):
        return self.database_handler.delete_setting(key)

    def contains(self, key: str) -> bool:
        try:
            self.database_handler.read_setting(key)
            return True
        except DoesNotExist:
            return False

    def sync(self):
        """sync settings with a timeslime server"""
        if self.timeslime_server_handler is not None:
            last_setting_sync = None
            if self.state_handler:
                last_setting_sync = self.state_handler.get_state().last_setting_sync
            settings_response = self.timeslime_server_handler.get_settings(
                last_setting_sync
            )

            for setting in settings_response.settings:
                if not self.contains(setting.key):
                    self.set(setting.key, setting.value, setting.id)
                else:
                    local_setting = self.get(setting.key)
                    if local_setting.updated_at < setting.updated_at:
                        self.set(setting.key, setting.value, setting.id)

            self.timeslime_server_handler.send_setting_list(
                self.get_all(last_setting_sync)
            )

            if self.state_handler:
                self.state_handler.set_last_setting_sync(settings_response.request_time)

import logging
import time
from datetime import datetime, timedelta
from logging import LogRecord, StreamHandler
from typing import List

import httpx

from pytest_zebrunner.api.client import ZebrunnerAPI
from pytest_zebrunner.api.models import LogRecordModel
from pytest_zebrunner.context import zebrunner_context


class ZebrunnerHandler(StreamHandler):
    """
    A class that inherit from StreamHandler useful for recording logs.

    Attributes:
        logs (List[LorRecordModel]): List of logs to be handled.
    """
    logs: List[LogRecordModel] = []

    def __init__(self) -> None:
        super().__init__()
        self.api = ZebrunnerAPI()
        self.last_push = datetime.utcnow()

    def emit(self, record: LogRecord) -> None:
        """
        Try to send logs to test_run_id if the last attempt was more than a second ago. If not, and test is active,
        adds a new log to the list.

        Args:
            record (LogRecord): The log to be recorded.
        """
        if datetime.utcnow() - self.last_push >= timedelta(seconds=1):
            self.push_logs()

        if zebrunner_context.test_is_active:
            self.logs.append(
                LogRecordModel(
                    test_id=str(zebrunner_context.test_id),
                    timestamp=str(round(time.time() * 1000)),
                    level=record.levelname,
                    message=str(record.msg),
                )
            )

    def push_logs(self) -> None:
        """
        Updates last_push datetime, resets logs list and send the to Zebrunner API
        for reporting if test_run_id is active.

        """
        try:    
            if zebrunner_context.test_run_id and zebrunner_context.settings.send_logs:
                self.api.send_logs(zebrunner_context.test_run_id, self.logs)
        except httpx.HTTPError as e:
            logging.error("Failed to send logs to zebrunner", exc_info=e)
        finally:
            self.logs = []
            self.last_push = datetime.utcnow()

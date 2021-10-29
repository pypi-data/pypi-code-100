from typing import Iterable, Optional

from eventy.messaging.errors import MessagingError
from eventy.messaging.store import Store
from eventy.record import Record

__all__ = [
    'MemoryStore',
]


class MemoryStore(Store):
    """
    In-memory record store, essentially for testing and debug purposes
    """

    def __init__(self) -> None:
        super().__init__()
        self.read_list: list[Record] = []
        self.write_list: list[Record] = []
        self.uncommitted_read_list: list[Record] = []
        self.uncommitted_write_list: list[Record] = []
        self.in_transaction = False

    def add_record_to_read(self, records: list[Record]) -> None:
        """
        Make records available to be read
        """
        self.read_list += records

    def get_written_records(self) -> list[Record]:
        """
        Get all written records
        """
        return self.write_list

    def clear_written_records(self) -> None:
        """
        Clear previously written records

        After calling this method, `get_written_records()` will always return an empty list.
        """
        self.write_list = []

    def reset(self) -> None:
        """
        Reset to the committed state (as if the service restarted)
        """
        # Uncommitted read records will be read again
        self.read_list = self.uncommitted_read_list + self.read_list
        # Uncommitted write records are not written yet
        self.uncommitted_write_list = []
        self.in_transaction = False

    def read(
        self,
        max_count: int = 1,
        timeout_ms: Optional[int] = None,
        auto_ack: bool = False
    ) -> Iterable[Record]:
        count = min(max_count, len(self.read_list))
        records = self.read_list[0:count]
        self.read_list = self.read_list[count:]
        self.uncommitted_read_list += records
        return records

    def ack(self, timeout_ms=None) -> None:
        self.uncommitted_read_list = []

    def write(self, record: Record, topic: str, timeout_ms=None) -> None:
        if self.in_transaction:
            self.uncommitted_write_list.append(record)
        else:
            self.write_list.append(record)

    def write_now(self, record: Record, topic: str, timeout_ms=None) -> None:
        self.write_list.append(record)

    def start_transaction(self) -> None:
        if self.in_transaction:
            raise MessagingError(f"Already in a transaction.")
        self.in_transaction = True

    def commit(self, timeout_ms: Optional[int] = None) -> None:
        if not self.in_transaction:
            raise MessagingError(f"Not in a transaction.")
        self.write_list += self.uncommitted_write_list
        self.uncommitted_write_list = []

        self.uncommitted_read_list = []

    def abort(self, timeout_ms: Optional[int] = None) -> None:
        if not self.in_transaction:
            raise MessagingError(f"Not in a transaction.")
        self.reset()

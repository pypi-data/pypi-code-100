from datetime import datetime
from uuid import getnode as get_mac


def _dump(value):
    return "%s(%s) -> 0x%s" % (value, type(value), "{0:b}".format(value))


def _epoch(dt: datetime):
    return dt.timestamp()


def _get_current_node():
    return hash(get_mac())


class UUID(object):
    _sequence_number = 0

    _time_mask = (2 ** 42 - 1) << 22
    _sequence_mask = (2 ** 16 - 1) << 6
    _node_mask = (2 ** 5 - 1) << 1
    _cheat_bit_mask = 1
    max_id = 9999999999999999999999

    @staticmethod
    def build_one(time_ms, seq_number, node_id, cheat_bit=1):
        return time_ms << 22 | seq_number << 6 | node_id << 1 | cheat_bit

    @staticmethod
    def fetch_one():
        time_ms = int(_epoch(datetime.utcnow()) * 1000)
        UUID._sequence_number += 1
        if UUID._sequence_number > 65536:
            UUID._sequence_number = 0

        return UUID.build_one(time_ms, UUID._sequence_number, _get_current_node(), 0)

    @staticmethod
    def describe(uuid):
        return {
            "time_ms": (uuid & UUID._time_mask) >> 22,
            "seq_number": (uuid & UUID._sequence_mask) >> 6,
            "node_id": (uuid & UUID._node_mask) >> 1,
            "cheat_bit": uuid & UUID._cheat_bit_mask,
        }

    @staticmethod
    def build_cheated_uuid_based_on_another_uuid(uuid, seq_number=None):
        describe = UUID.describe(uuid)
        if seq_number is None:
            seq_number = describe["seq_number"]

        return UUID.build_one(describe["time_ms"], seq_number, describe["node_id"], 1)

    def __str__(self):
        describe = UUID.describe(self)
        return "time_ms: %s\nseq_num: %s\nnode_id: %s\ncheat_bit: %s\nuuid: %s" % (
            _dump(describe["time_ms"]),
            _dump(describe["seq_number"]),
            _dump(describe["node_id"]),
            _dump(describe["cheat_bit"]),
            _dump(self),
        )

    def __repr__(self):
        return self.__str__

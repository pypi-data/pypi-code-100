from abc import ABC, abstractmethod
from math import nan
import can
import datetime
import re
import struct
import base64
from .can_message import CanMessage


class CanBusReaderBase(ABC):

    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def __next__(self):
        pass

    @abstractmethod
    def __len__(self):
        pass

    def stop(self):
        pass


class PCANTraceFileReader(CanBusReaderBase):
    # Matches the following:
    # 21889      6254.519 DT     0301 Rx 8  46 FF AF FD FF FF 7F 00
    # 16)         3.0  Rx         0094  8  51 E9 CF 74 B1 E9 F4 0F
    REGEX = re.compile(r'\s*(\d+)\)?\s+(\d+\.\d+)\s+([A-Za-z]+)\s+([A-F0-9]{4})\s+(Rx)?\s+(\d)\s+([A-F0-9\s]+)$')

    def __init__(self, trace_file):
        self.n = 0
        with open(trace_file) as f:
            self.msgs = [self._parse_line(line) for line in f]
            self.msgs = list(filter(lambda x: x is not None, self.msgs))

    def _parse_line(self, line):
        if line.startswith(';'):  # comment
            return
        m = PCANTraceFileReader.REGEX.match(line)
        if m:
            # seq = m.group(1)
            time_ms = float(m.group(2)) / 1000
            # direction = m.group(3)
            canid = int(m.group(4), base=16)
            # length = m.group(6)
            data = bytes.fromhex(m.group(7))
            return CanMessage(time_ms, canid, data, False)
        else:
            print("no find", line)

    def __iter__(self):
        return self

    def __next__(self):
        if self.n < len(self.msgs):
            msg = self.msgs[self.n]
            self.n += 1
            return msg
        else:
            raise StopIteration

    def __len__(self):
        return len(self.msgs)


class PiLoggerBinaryReader(CanBusReaderBase):

    def __init__(self, file):
        self.f = open(file, mode='br')
        self.f.seek(0, 2)
        self.len = self.f.tell()
        self.f.seek(0)
        self.prev_timestamp = (-1, -1)

    def __timestamp_bug_workaround(self, ms, us):
        ret = (ms, us)
        if self.prev_timestamp[0] > 0 and self.prev_timestamp[0] < ms and self.prev_timestamp[1] < us:
            ret = (self.prev_timestamp[0], us)
        self.prev_timestamp = (ms, us)
        return ret

    def _parse_line(self, data):
        # 86 00      7A C5    00 00 0F 12 08 4E 01 80 00 00 00 00 00
        # -----      -----    ----------- -- -----------------------
        # 1=655.36ms 1=10us   id          len        data
        timestamp_ms, timestamp_us, canid = struct.unpack('HHI', data[0:8])
        timestamp_ms, timestamp_us = self.__timestamp_bug_workaround(timestamp_ms, timestamp_us)
        timestamp = (2**16 / 1e5) * timestamp_ms + 1e-5 * timestamp_us
        extended = canid & 0x40000000 != 0
        canid &= 0x1fffffff
        canid = canid if extended else (canid >> 18)
        payload = data[9:9 + data[8]]
        return CanMessage(timestamp, canid, payload, extended)

    def __iter__(self):
        return self

    def __next__(self):
        data = self.f.read(17)
        if len(data) == 17:
            return self._parse_line(data)
        else:
            self.f.close()
            raise StopIteration

    def __len__(self):
        return self.len // 17


class PiLoggerTextReader(CanBusReaderBase):

    def __init__(self, file):
        self.f = open(file)
        self.f.seek(0, 2)
        self.len = self.f.tell()
        self.f.seek(0)

    def _parse_line(self, line):
        items = [item.strip('"\n') for item in line.split(';')]
        timestamp, canid, extended, _, data = items
        canid = int(canid, base=16)
        data = bytes.fromhex(data)
        timestamp = (datetime.datetime.strptime(timestamp, '%H:%M:%S.%f') - datetime.datetime(1900, 1, 1)).total_seconds()
        return CanMessage(timestamp, canid, data, extended == 'Ext')

    def __iter__(self):
        return self

    def __next__(self):
        for line in self.f:
            msg = self._parse_line(line)
            return msg
        self.f.close()
        raise StopIteration

    def __len__(self):
        return self.len


class PythonCANCSVReader(CanBusReaderBase):

    def __init__(self, csv_file):
        self.n = 0
        with open(csv_file) as f:
            next(f)  # skip header
            self.msgs = [self._parse_line(line) for line in f]

    def _parse_line(self, line):
        timestamp, arbitration_id, extended, remote, error, dlc, data = line.split(',')
        arbitration_id = int(arbitration_id, base=16)
        data = base64.b64decode(data)
        return CanMessage(float(timestamp), arbitration_id, data, extended == '1')

    def __iter__(self):
        return self

    def __next__(self):
        if self.n < len(self.msgs):
            msg = self.msgs[self.n]
            self.n += 1
            return msg
        else:
            raise StopIteration

    def __len__(self):
        return len(self.msgs)


class CanBusReader(CanBusReaderBase):

    def __init__(self, bus: can.interface.Bus):
        self.bus = bus

    def __iter__(self):
        return self

    def __next__(self):
        for msg in self.bus:
            return CanMessage(msg.timestamp, int(msg.arbitration_id), msg.data, msg.is_extended_id)

    def stop(self):
        self.bus.shutdown()

    def __len__(self):
        return nan

#  Copyright (c) 2021 ETH Zurich, SIS ID and HVL D-ITET
#
"""
Device classes for "RS 232" and "Ethernet" Interfaces which are used to control power
supplies from Technix.
Manufacturer homepage:
https://www.technix-hv.com

The Regulated power Supplies Series and Capacitor Chargers Series from Technix are
series of low and high voltage direct current power supplies as well as capacitor
chargers.
The class `Technix` is tested with a CCR10KV-7,5KJ via an ethernet connection as well
as a CCR15-P-2500-OP via a serial connection.
Check the code carefully before using it with other devices or device series

This Python package may support the following interfaces from Technix:
    - `Remote Interface RS232
      <https://www.technix-hv.com/remote-interface-rs232.php>`_
    - `Ethernet Remote Interface
      <https://www.technix-hv.com/remote-interface-ethernet.php>`_
    - `Optic Fiber Remote Interface
      <https://www.technix-hv.com/remote-interface-optic-fiber.php>`_

"""
import logging
from abc import ABC
from time import sleep
from typing import Type, Union, Optional

import aenum

from . import SingleCommDevice
from .utils import Poller
from ..comm.base import SyncCommunicationProtocol, SyncCommunicationProtocolConfig

from ..configuration import configdataclass
from hvl_ccb.comm import (
    SerialCommunicationConfig,
    SerialCommunication,
    TelnetCommunicationConfig,
    TelnetCommunication,
)
from ..utils.typing import Number

logger = logging.getLogger(__name__)


class TechnixError(Exception):
    """
    Technix related errors.
    """


@configdataclass
class TechnixCommunicationConfig(SyncCommunicationProtocolConfig):
    #: The terminator is CR
    terminator: bytes = b"\r"


class TechnixCommunication(SyncCommunicationProtocol, ABC):
    """
    Generic communication class for Technix, which can be implemented via
    `TechnixSerialCommunication` or `TechnixTelnetCommunication`
    """

    def query(self, command: str) -> str:
        """
        Send a command to the interface and handle the status message.
        Eventually raises an exception.

        :param command: Command to send
        :raises TechnixError: if the connection is broken
        :return: Answer from the interface
        """

        with self.access_lock:
            logger.debug(f"TechnixCommunication, send: '{command}'")
            answer: Optional[str] = super().query(command)  # string or None
            logger.debug(f"TechnixCommunication, receive: '{answer}'")
            if answer is None:
                raise TechnixError(
                    f"TechnixCommunication did get no answer on "
                    f"command: '{command}'"
                )
            return answer


@configdataclass
class TechnixSerialCommunicationConfig(
    TechnixCommunicationConfig, SerialCommunicationConfig
):
    pass


class TechnixSerialCommunication(TechnixCommunication, SerialCommunication):
    @staticmethod
    def config_cls():
        return TechnixSerialCommunicationConfig


@configdataclass
class TechnixTelnetCommunicationConfig(
    TelnetCommunicationConfig, TechnixCommunicationConfig
):
    #: Port at which Technix is listening
    port: int = 4660


class TechnixTelnetCommunication(TelnetCommunication, TechnixCommunication):
    @staticmethod
    def config_cls():
        return TechnixTelnetCommunicationConfig


TechnixCommunicationClasses = Union[
    Type[TechnixSerialCommunication], Type[TechnixTelnetCommunication]
]


@configdataclass
class TechnixConfig:
    #: communication channel between computer and Technix
    communication_channel: TechnixCommunicationClasses

    #: Maximal Output voltage
    max_voltage: Number

    #: Maximal Output current
    max_current: Number

    #: Polling interval in s to maintain to watchdog of the device
    polling_interval_sec: Number = 4

    #: Time to wait after stopping the device
    post_stop_pause_sec: Number = 1

    #: Time for pulsing a register
    register_pulse_time: Number = 0.1


class _TechnixSetRegisters(aenum.Enum):
    _init_ = "value description"
    VOLTAGE = "d1", "Output Voltage programming"
    CURRENT = "d2", "Output Current programming"
    HVON = "P5", "HV on"
    HVOFF = "P6", "HV off"
    LOCAL = "P7", "Local/remote mode"
    INHIBIT = "P8", "Inhibit"


class _TechnixGetRegisters(aenum.Enum):
    _init_ = "value description"
    VOLTAGE = "a1", "Output Voltage Monitor"
    CURRENT = "a2", "Output Current Monitor"
    STATUS = "E", "Image of the power supply logical status"


class TechnixStatusByte:
    def __init__(self, value: int):
        if value < 0 or value > 255:
            raise TechnixError(f"Cannot convert '{value}' into StatusByte")
        self._status: list = [bool(value & 1 << 7 - ii) for ii in range(8)]

    def __str__(self):
        return "".join(str(int(ii)) for ii in self._status)

    def __repr__(self):
        return f"StatusByte: {self}"

    def msb_first(self, idx: int) -> Optional[bool]:
        """
        Give the Bit at position idx with MSB first

        :param idx: Position of Bit as 1...8
        :return:
        """
        if idx < 1 or idx > 8:
            return None

        return self._status[8 - idx]


class Technix(SingleCommDevice):
    def __init__(self, com, dev_config):
        # Call superclass constructor
        super().__init__(com, dev_config)
        logger.debug("Technix Power Supply initialised.")

        # maximum output current of the hardware
        self._max_current_hardware = self.config.max_current
        # maximum output voltage of the hardware
        self._max_voltage_hardware = self.config.max_voltage

        #: status of Technix
        self._voltage_regulation: Optional[bool] = None
        self._fault: Optional[bool] = None
        self._open_interlock: Optional[bool] = None
        self._hv: Optional[bool] = None
        self._local: Optional[bool] = None
        self._inhibit: Optional[bool] = None
        self._real_status = False

        #: Status Poller to maintain the watchdog of the device
        self._status_poller: Poller = Poller(
            spoll_handler=self._spoll_handler,
            polling_interval_sec=self.config.polling_interval_sec,
        )

    @staticmethod
    def config_cls():
        return TechnixConfig

    def default_com_cls(self) -> TechnixCommunicationClasses:  # type: ignore
        return self.config.communication_channel

    @property
    def voltage_regulation(self) -> Optional[bool]:
        if self._real_status:
            return self._voltage_regulation
        return None

    @property
    def max_current(self) -> Number:
        return self._max_current_hardware

    @property
    def max_voltage(self) -> Number:
        return self._max_voltage_hardware

    def start(self):
        super().start()

        with self.com.access_lock:
            logger.debug("Technix: Set remote = True")
            self.remote = True
            self.hv = False
            self._status_poller.start_polling()

        logger.debug("Technix: Started communication")

    def stop(self):
        with self.com.access_lock:
            self._status_poller.stop_polling()
            self.hv = False
            self.remote = False
            self._real_status = False
            sleep(self.config.post_stop_pause_sec)

        super().stop()

        logger.debug("Technix: Stopped communication")

    def _spoll_handler(self):
        try:
            self.get_status_byte()
        except TechnixError as exception:
            self._status_poller.stop_polling()
            raise TechnixError("Connection is broken") from exception

    def _set_register(self, register: _TechnixSetRegisters, value: Union[bool, int]):
        command = register.value + "," + str(int(value))
        answer = self.com.query(command)
        if not answer == command:
            raise TechnixError(f"Expected '{command}', but answer was '{answer}'")

    def _get_register(self, register: _TechnixGetRegisters) -> int:
        answer = self.com.query(register.value)
        if not answer[: register.value.__len__()] == register.value:
            raise TechnixError(
                f"Expected '{register.value}', but answer was '{answer}'")
        return int(answer[register.value.__len__():])  # noqa: E203

    @property
    def voltage(self) -> Number:
        return self._get_register(
            _TechnixGetRegisters.VOLTAGE  # type: ignore
        ) / 4095 * self.max_voltage

    @voltage.setter
    def voltage(self, value: Number):
        _voltage = int(4095 * value / self.max_voltage)
        if _voltage < 0 or _voltage > 4095:
            raise TechnixError(f"Voltage '{value}' is out of range")
        self._set_register(
            _TechnixSetRegisters.VOLTAGE,  # type: ignore
            _voltage)

    @property
    def current(self) -> Number:
        return self._get_register(
            _TechnixGetRegisters.CURRENT  # type: ignore
        ) / 4095 * self.max_current

    @current.setter
    def current(self, value: Number):
        _current = int(4095 * value / self.max_current)
        if _current < 0 or _current > 4095:
            raise TechnixError(f"Current '{value}' is out of range")
        self._set_register(
            _TechnixSetRegisters.CURRENT,  # type: ignore
            _current)

    @property
    def hv(self) -> Optional[bool]:
        if self._real_status:
            return self._hv
        return None

    @hv.setter
    def hv(self, value: Union[bool, Number]):
        if int(value) < 0 or int(value) > 1:
            raise TechnixError(f"HV '{value}' is out of range")
        if value:
            self._set_register(
                _TechnixSetRegisters.HVON,  # type: ignore
                True)
            sleep(self.config.register_pulse_time)
            self._set_register(
                _TechnixSetRegisters.HVON,  # type: ignore
                False)
        else:
            self._set_register(
                _TechnixSetRegisters.HVOFF,  # type: ignore
                True)
            sleep(self.config.register_pulse_time)
            self._set_register(
                _TechnixSetRegisters.HVOFF,  # type: ignore
                False)
        logger.debug(f"Technix: HV-Output is {'' if value else 'de'}activated")

    @property
    def remote(self) -> Optional[bool]:
        if self._real_status:
            return not self._local
        return None

    @remote.setter
    def remote(self, value: Union[bool, Number]):
        if int(value) < 0 or int(value) > 1:
            raise TechnixError(f"Remote '{value}' is out of range")
        self._set_register(
            _TechnixSetRegisters.LOCAL,  # type: ignore
            not value)
        logger.debug(f"Technix: Remote control is {'' if value else 'de'}activated")

    @property
    def inhibit(self) -> Optional[bool]:
        if self._real_status:
            return not self._inhibit
        return None

    @inhibit.setter
    def inhibit(self, value: Union[bool, Number]):
        if int(value) < 0 or int(value) > 1:
            raise TechnixError(f"Inhibit '{value}' is out of range")
        self._set_register(
            _TechnixSetRegisters.INHIBIT,  # type: ignore
            not value)
        logger.debug(f"Technix: Inhibit is {'' if value else 'de'}activated")

    def get_status_byte(self) -> TechnixStatusByte:
        with self.com.access_lock:
            """This method can be called manually and by the poller. In case of a
            fault the communication is stopped and subsequent calls of this function
            are  skipped. Only one unique call of this function is allowed to be
            performed at the same time. cf. issue 161 on gitlab.com/ethz_hvl/hvl_ccb"""

            if not self.com.is_open:
                """If the communication was closed in the meantime"""
                raise TechnixError("Technix communication is not open.")

            answer = TechnixStatusByte(self._get_register(
                _TechnixGetRegisters.STATUS  # type: ignore
            ))
            self._inhibit = answer.msb_first(8)
            self._local = answer.msb_first(7)
            # HV-Off (1 << (6 - 1))
            # HV-On (1 << (5 - 1))
            self._hv = answer.msb_first(4)
            self._open_interlock = answer.msb_first(3)
            self._fault = answer.msb_first(2)
            self._voltage_regulation = answer.msb_first(1)
            self._real_status = True
            if self._fault:
                self.stop()
                raise TechnixError(
                    "Technix returned the status code with the fault flag set"
                )
            logger.debug(f"Technix: Received status code: {answer}")
            return answer

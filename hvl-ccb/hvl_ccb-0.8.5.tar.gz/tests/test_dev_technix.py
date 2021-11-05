#  Copyright (c) 2021 ETH Zurich, SIS ID and HVL D-ITET
#
"""
Tests for .dev sub-package technix
"""
import logging
from time import sleep

import pytest

from hvl_ccb.dev import (
    TechnixTelnetCommunication,
    Technix,
    TechnixError,
    TechnixSerialCommunication,
)
from hvl_ccb.dev.technix import TechnixSerialCommunicationConfig
from masked_comm import LocalTechnixServer
from masked_comm.serial import TechnixLoopSerialCommunication
from masked_comm.uitls import get_free_tcp_port

logging.basicConfig(level=logging.DEBUG)


@pytest.fixture(scope="function")
def com_telnet():
    host = "127.0.0.1"
    return {
        "host": host,
        "port": get_free_tcp_port(host),
        "timeout": 0.01,
        "wait_sec_read_text_nonempty": 0.01,
        "default_n_attempts_read_text_nonempty": 2,
    }


@pytest.fixture(scope="module")
def com_serial():
    return {
        "port": "loop://?logging=debug",
        "baudrate": 9600,
        "parity": TechnixSerialCommunicationConfig.Parity.NONE,
        "stopbits": TechnixSerialCommunicationConfig.Stopbits.ONE,
        "bytesize": TechnixSerialCommunicationConfig.Bytesize.EIGHTBITS,
        "timeout": 0.01,
        "wait_sec_read_text_nonempty": 0.01,
        "default_n_attempts_read_text_nonempty": 2,
    }


@pytest.fixture(scope="module")
def dev_config_telnet():
    return {
        "max_voltage": 10000,
        "max_current": 1.5,
        "communication_channel": TechnixTelnetCommunication,
        "post_stop_pause_sec": 0.01,
        "register_pulse_time": 0.01,
    }


@pytest.fixture(scope="module")
def dev_config_serial():
    return {
        "max_voltage": 10000,
        "max_current": 1.5,
        "communication_channel": TechnixSerialCommunication,
        "post_stop_pause_sec": 0.01,
        "register_pulse_time": 0.01,
    }


def start_technix_telnet(com, dev_config):
    # Start server and listen
    ts = LocalTechnixServer(port=com["port"], timeout=com["timeout"])
    # Connect with the client to the server
    tex = Technix(com, dev_config)
    # Open/accept the connection from the client to the server
    ts.open()

    return ts, tex


def full_start_devices(com, dev_config):
    ts, tex = start_technix_telnet(com, dev_config)
    tex.start()
    return ts, tex


def test_devices(com_telnet, dev_config_telnet):
    ts, tex = start_technix_telnet(com_telnet, dev_config_telnet)
    assert ts is not None
    assert tex.__class__ is Technix
    tex.stop()
    ts.close()


def test_watchdog(com_telnet, dev_config_telnet):
    ts, tex = full_start_devices(com_telnet, dev_config_telnet)
    sleep(5)

    tex.stop()
    ts.close()


def test_status_byte(com_telnet, dev_config_telnet):
    ts, tex = full_start_devices(com_telnet, dev_config_telnet)

    # Wrong status byte
    with pytest.raises(TechnixError):
        ts.status = 1000
        tex.get_status_byte()

    ts.status = 1
    assert tex.get_status_byte().__repr__() == "StatusByte: 00000001"
    assert tex.get_status_byte().msb_first(0) is None

    tex.stop()
    ts.close()


def test_no_properties(com_telnet, dev_config_telnet):
    ts, tex = start_technix_telnet(com_telnet, dev_config_telnet)

    assert tex.voltage_regulation is None
    assert tex.hv is None
    assert tex.remote is None
    assert tex.inhibit is None

    tex.stop()
    ts.close()


def test_properties(com_telnet, dev_config_telnet):
    ts, tex = full_start_devices(com_telnet, dev_config_telnet)

    ts.status = 0
    tex.get_status_byte()
    assert not tex.voltage_regulation
    assert not tex.hv
    assert tex.remote
    assert tex.inhibit

    ts.status = (1 << 0) + (1 << 3) + (1 << 6) + (1 << 7)
    tex.get_status_byte()
    assert tex.voltage_regulation
    assert tex.hv
    assert not tex.remote
    assert not tex.inhibit

    tex.stop()
    ts.close()


def test_voltage_current(com_telnet, dev_config_telnet):
    ts, tex = full_start_devices(com_telnet, dev_config_telnet)

    assert tex.max_voltage == 10000
    assert tex.max_current == 1.5

    ts.custom_answer = "d1,102"
    tex.voltage = 250
    assert ts.last_request == "d1,102"

    ts.custom_answer = "d2,2730"
    tex.current = 1
    assert ts.last_request == "d2,2730"

    ts.custom_answer = "a12048"
    assert int(tex.voltage) == 5001
    assert ts.last_request == "a1"

    ts.custom_answer = "a23000"
    assert int(tex.current * 1000) == 1098
    assert ts.last_request == "a2"

    with pytest.raises(TechnixError):
        tex.voltage = 1e6
    with pytest.raises(TechnixError):
        tex.current = 1e6

    tex.stop()
    ts.close()


def test_hv_remote(com_telnet, dev_config_telnet):
    ts, tex = full_start_devices(com_telnet, dev_config_telnet)

    with pytest.raises(TechnixError):
        tex.hv = 100
    tex.hv = 1
    tex.hv = True
    tex.hv = 0
    tex.hv = False

    with pytest.raises(TechnixError):
        tex.remote = 100

    with pytest.raises(TechnixError):
        tex.inhibit = 100
    tex.inhibit = True

    tex.stop()
    ts.close()


def test_fault_detection(com_telnet, dev_config_telnet):
    ts, tex = full_start_devices(com_telnet, dev_config_telnet)

    tex.get_status_byte()
    assert tex._real_status
    with pytest.raises(TechnixError):
        ts.status = 127
        tex.get_status_byte()

    ts.close()


def test_no_or_wrong_reply(com_telnet, dev_config_telnet):
    ts, tex = full_start_devices(com_telnet, dev_config_telnet)

    with pytest.raises(TechnixError):
        ts.listen_and_repeat = []
        tex.inhibit = 0

    with pytest.raises(TechnixError):
        ts.custom_answer = "P7,1"
        ts.listen_and_repeat = []
        tex.inhibit = 0

    with pytest.raises(TechnixError):
        ts.custom_answer = "d1,1234"
        assert tex.current == 666

    ts.close()


def start_serial_devices(com_serial, dev_config_serial):
    com = TechnixLoopSerialCommunication(com_serial)
    com.open()

    tex = Technix(com, dev_config_serial)

    com.put_text("P7,0")
    com.put_text("P6,1")
    com.put_text("P6,0")
    com.put_text("E0")  # status byte for the polling thread
    tex.start()
    assert com.get_written() == "P7,0"
    assert com.get_written() == "P6,1"
    assert com.get_written() == "P6,0"
    sleep(0.1)  # time for the polling thread to start
    assert com.get_written() == "E"
    return com, tex


def test_serial(com_serial, dev_config_serial):
    com, tex = start_serial_devices(com_serial, dev_config_serial)

    com.put_text("E0")
    assert tex.get_status_byte().__repr__() == "StatusByte: 00000000"
    assert tex._real_status
    assert com.get_written() == "E"

    com.put_text("P6,1")
    com.put_text("P6,0")
    com.put_text("P7,1")
    tex.stop()
    assert com.get_written() == "P6,1"
    assert com.get_written() == "P6,0"
    assert com.get_written() == "P7,1"

    com.close()


def test_serial_no_answer(com_serial, dev_config_serial):
    com, tex = start_serial_devices(com_serial, dev_config_serial)

    with pytest.raises(TechnixError):
        assert tex.get_status_byte().__repr__() == "StatusByte: 00000000"

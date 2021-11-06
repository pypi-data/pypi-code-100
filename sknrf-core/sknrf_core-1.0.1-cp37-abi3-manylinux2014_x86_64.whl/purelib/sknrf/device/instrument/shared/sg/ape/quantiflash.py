# -*- coding: utf-8 -*-
#!/usr/bin/env python

# #############################################################################
#  ATTENTION
# #############################################################################
#
#  This software is for guidance only. It is provided "as is".
#  It only aims at providing coding information to the customer in order for
#  them to save time. As a result no warranties, whether express, implied or
#  statutory, including, but not limited to implied warranties of
#  merchantability and fitness for a particular purpose apply to this software.
#  A·P·E Angewandte Physik und Elektronik GmbH shall not be held liable for any
#  direct, indirect or consequential damages with respect to any claims arising
#  from the content of such sourcecode and/or the use made by customers of the
#  coding information contained herein in connection with their products.
#
#  File Version: 1.0
#
#  Changelog:
#    1.0 - Initial Version
#
# #############################################################################

import time

from sknrf.device.instrument.shared.sg.ape.device import Device
from sknrf.device.instrument.shared.sg.ape.gui import Control


class QuantiFlash(Device):
    def __init__(self, host="127.0.0.1", port=51019, name="quantiFlash"):
        super(self.__class__, self).__init__(host=host, port=port, name=name)
        self.id = "{:s}:{:d}".format(host, port)

    def __del__(self):
        self.disconnect_target()

    def send(self, command):
        super(self.__class__, self).send(command)
        time.sleep(0.1)

    def getDevice(self):
        return self.query(":sys:device?")

    def getSerial(self):
        return self.query(":sys:snumber?")

    def getSoftware(self):
        return self.query(":sys:software?")

    def getLEDControl(self):
        return self.query(":led:control?")

    def setLEDControl(self, control):
        self.send(":led:control=" + control)

    def getLEDMode(self):
        return self.query(":led:mode?")

    def setLEDMode(self, mode):
        self.send(":led:mode=" + mode)

    def getPulseIntensity(self):
        return self.query(":pulse:intensity?")

    def setPulseIntensity(self, intensity):
        self.send(":pulse:intensity=" + str(intensity))

    def getPulseDuration(self):
        return self.query(":pulse:duration?")

    def setPulseDuration(self, duration):
        self.send(":pulse:duration=" + str(duration))

    def getPulseRate(self):
        return self.query(":pulse:rate?")

    def setPulseRate(self, rate):
        self.send(":pulse:rate="+str(rate))

    def getTriggerIntensity(self):
        return self.query(":trigger:intensity?")

    def setTriggerIntensity(self, intensity):
        self.send(":trigger:intensity=" + str(intensity))

    def getPulseShapeNumber(self):
        return self.query(":pulse:shape?")

    def getPulseShapeName(self):
        return self.query(":pulse:shape:name?")

    def selectPulseShape(self, shape):
        self.send(":pulse:shape=" + str(shape))

    def selectPulseShapeByName(self, shape):
        self.send(":pulse:shape:name=" + shape)

    def getLedIntensity(self):
        return self.query(":led:intensity?")

    def setLedIntensity(self, intensity):
        self.send(":led:intensity=" + str(intensity))

    def getChannel(self):
        return self.query(":channel:enable?")

    def setChannel(self, channel):
        self.send(":channel:enable=" + str(channel))

    def getChannelActive(self):
        return self.query(":channel:active?")

    def setChannelActive(self, channel):
        self.send(":channel:active=" + str(channel))



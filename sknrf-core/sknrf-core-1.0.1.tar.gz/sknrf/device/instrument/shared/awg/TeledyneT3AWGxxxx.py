
import pyvisa as visa

from sknrf.settings import Settings


def download_waveform_bug(self, command):
    self.handles["awg"].write("SYSTem:BEEPer:STATe OFF")
    self.handles["awg"].query("*OPC?")
    self.handles["awg"].write_raw(command)
    try:
        self.handles["awg"].query("*OPC?")  # this command fails when the waveform is long
    except visa.VisaIOError:
        pass  # this command fails when the waveform is long
    finally:
        self.handles["awg"].write("SYSTem:BEEPer:STATe ON")


def preset(self):
    t_points = int(self._a_p_.shape[-2] * self._config["resample"])
    end = t_points + 16 - t_points % 16
    self.handles["awg"].write("*CLS")
    self.handles["awg"].write("*RST")
    self.handles["awg"].query("*OPC?")

    # Coax Switch
    self.channel = 1

    # AWG Control
    self.handles["awg"].write("AWGControl:STOP")
    self.handles["awg"].write("AWGControl:RMODe BURSt")
    self.handles["awg"].write("AWGControl:BURST 1")
    self.handles["awg"].write("AWGControl:SRATe %f" % (1/Settings().t_step*self._config["resample"]))
    self.handles["awg"].write("AWGControl:WAITstate LASTsample")
    self.handles["awg"].query("*OPC?")

    # Sequence
    self.handles["awg"].write("SEQuence:LENGth 1")
    self.handles["awg"].write("SEQuence:ELEM1:LOOP:COUNt 1")
    self.handles["awg"].query("*OPC?")

    # Sequence
    self.handles["awg"].write('SEQuence:ELEM1:LENGth %d' % (end,))
    self.handles["awg"].write('SEQuence:ELEM1:LOOP:COUNt 1')
    self.handles["awg"].query("*OPC?")

    # Waveform List
    self.handles["awg"].write('WLISt:WAVeform:DELete ALL')
    self.handles["awg"].query("*OPC?")

    # Trigger
    is_master = (Settings().trigger_device & self.device_id).value and Settings().trigger_port == self.port
    self.handles["awg"].write("TRIGger:SOURce %s" % ("MAN" if is_master else "EXT",))
    self.handles["awg"].write("TRIGger:LEVel %f" % (self._config["marker_level"],))
    self.handles["awg"].write("TRIGger:SLOPe %s" % ("NEGative",))
    self.handles["awg"].write("TRIGger:IMPedance %s " % ("50Ohm",))

    # Marker
    self.handles["awg"].write("MARKer:MODE1 %s" % ("AUTOmatic",))
    self.handles["awg"].write("MARKer:LEVel1 %e" % (self._config["trigger_level"],))
    if self._config["trigger_delay"] > 0.0:
        self.handles["awg"].write("MARKer:SKEW1 %e" % (self._config["trigger_delay"],))
    else:
        self.handles["awg"].write("OUTPut1:DELay %e" % (-self._config["trigger_delay"]))
        self.handles["awg"].write("OUTPut2:DELay %e" % (-self._config["trigger_delay"]))

    # Waveform
    bytes = ('0\r\n' * end).encode()  # todo: correct this
    n_bytes = str(len(bytes)).encode()
    prefix = str(len(n_bytes)).encode()

    waveform = "_".join((self.__class__.__name__, "p"))
    self.handles["awg"].write(r'MMEM:DOWN:FNAM "%s.txt"' % (waveform,))
    download_waveform_bug(self, b'MMEM:DOWN:DATA #' + prefix + n_bytes + bytes)
    self.handles["awg"].query("*OPC?")
    self.handles["awg"].write('WLISt:WAVeform:IMPort "%s", "%s.txt", ANAlog' % (waveform, waveform))
    self.handles["awg"].query("*OPC?")

    waveform = "_".join((self.__class__.__name__, "n"))
    self.handles["awg"].write(r'MMEM:DOWN:FNAM "%s.txt"' % (waveform,))
    download_waveform_bug(self, b'MMEM:DOWN:DATA #' + prefix + n_bytes + bytes)
    self.handles["awg"].query("*OPC?")
    self.handles["awg"].write('WLISt:WAVeform:IMPort "%s", "%s.txt", ANAlog' % (waveform, waveform))
    self.handles["awg"].query("*OPC?")


def arm(self):
    self.handles["awg"].write("AWGControl:RUN")
    self.handles["awg"].query("*OPC?")


def trigger(self):
    is_master = (Settings().trigger_device & self.device_id).value and Settings().trigger_port == self.port
    if is_master:
        self.handles["awg"].write("*TRG")

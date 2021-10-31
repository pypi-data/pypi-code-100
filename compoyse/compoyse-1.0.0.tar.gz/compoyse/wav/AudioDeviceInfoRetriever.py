import pyaudio

class AudioDeviceInfoRetriever():
    def __init__(self):
        self.pya = pyaudio.PyAudio()
        return
    
    def get_device_count(self):
        return self.pya.get_device_count()
    
    def get_device_info_by_index(self, index):
        return self.pya.get_device_info_by_index(index)
    
    def get_default_output_device_info(self):
        return self.pya.get_default_output_device_info()
    
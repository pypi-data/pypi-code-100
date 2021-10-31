class AudioClip:
    def __init__(self):
        self.audio_file = None
        self.start = 0
        self.duration_of_playtime = 0
        self.output_device_index = None
        return
    
    def get_audio_file(self):
        return self.audio_file
    
    def get_start(self):
        return self.start
    
    def get_duration_of_playtime(self):
        return self.duration_of_playtime
    
    def _get_file_real_path(self):
        return self.audio_file._get_file_real_path()
    
    def get_output_device_index(self):
        return self.output_device_index
    
    def set_audio_file(self, audio_file):
        self.audio_file = audio_file
        return
        
    def set_start(self, start):
        self.start = start
        return
    
    def set_duration_of_playtime(self, duration):
        self.duration_of_playtime = duration
        return
    
    def set_output_device_index(self, index):
        self.output_device_index = index
        return
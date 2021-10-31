from compoyse.midi.Meter import _Meter

class Section:
    def __init__(self):
        self.voices = []
        self.identifier = ''
        return
    
    def get_voice_at_index(self, index):
        return self.voices[index]
    
    def get_number_of_voices(self):
        return len(self.voices)
    
    def get_identifier(self):
        return self.identifier
    
    def add_voice(self, voice):
        self.voices.append(voice)
        return
    
    def set_identifier(self, identifier):
        self.identifier = identifier
        return
    
    def set_quarter_note_bpm(self, quarter_note_bpm):
        self.meter =  _Meter()
        self.meter._set_length_of_quarter_in_seconds(quarter_note_bpm)
        return
    
    def _get_meter(self):
        return self.meter
    
    def _get_length(self):
        length_of_each_voice = []
        for i in range(0, len(self.voices)):
            length_of_each_voice.append(self.voices[i]._get_length(self.meter))
        return max(length_of_each_voice)
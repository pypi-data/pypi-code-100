from compoyse.midi.Beat_dependencies.Time import _Time

class _Beat:
    def __init__(self, rhythmic_value=['quarter']):
        self.time = _Time(rhythmic_value)
        return
    
    def get_rhythmic_value(self):
        return self.time._get_rhythmic_value()
    
    def _set_start_and_end(self, start, meter):
        self.time._set_start_and_end(start, meter)
        return
    
    def _get_length_in_seconds(self):
        return self.time._get_length_in_seconds()
    
    def set_rhythmic_value(self, rhythmic_value):
        self.time._set_rhythmic_value(rhythmic_value)
        return
    
    def _is_note(self):
        return
    
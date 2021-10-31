class Measure:
    def __init__(self):
        self.beats = []
        return
    
    def get_beat_at_index(self, index):
        return self.beats[index]
    
    def get_number_of_beats(self):
        return len(self.beats)

    def add_beat(self, note):
        self.beats.append(note)
        return
    
    def _get_length(self, meter):
        current_length = 0
        for i in range(0, len(self.beats)):
            current_beat = self.beats[i]
            current_beat._set_start_and_end(0, meter)
            current_length = current_length + self.beats[i]._get_length_in_seconds()
        return current_length
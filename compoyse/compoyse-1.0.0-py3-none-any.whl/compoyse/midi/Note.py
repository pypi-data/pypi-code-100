import pretty_midi
from compoyse.midi.Beat import _Beat
from compoyse.midi.Beat_dependencies.Velocity import _Velocity
from compoyse.midi.Beat_dependencies.NoteLetter import _NoteLetter

class Note(_Beat):
    def __init__(self,
                 velocity=0,
                 letter='C',
                 octave=0,
                 rhythmic_value=['quarter']):
        self.velocity = _Velocity(velocity)
        self.note_letter = _NoteLetter(letter, octave)
        super().__init__(rhythmic_value)
        return
    
    def get_note_data(self):
        return [self.velocity._get_velocity(), 
                self.note_letter._get_letter(), 
                self.note_letter._get_octave(), 
                self.time._get_rhythmic_value()]
    
    def get_velocity(self):
        return self.velocity._get_velocity()
    
    def get_letter(self):
        return self.note_letter._get_letter()
    
    def get_octave(self):
        return self.note_letter._get_octave()
    
    def get_midi_value(self):
        return self.note_letter._get_midi_value()
    
    def _get_midi_data(self):
        return pretty_midi.Note(velocity=self.velocity._get_velocity(),
                                pitch=self.note_letter._get_midi_value(),
                                start=self.time._get_start(),
                                end=self.time._get_end())
    
    def set_velocity(self, velocity):
        self.velocity._set_velocity(velocity)
        return
    
    def set_letter(self, letter):
        self.note_letter._set_letter(letter)
        return
    
    def set_octave(self, octave):
        self.note_letter._set_octave(octave)
        return
    
    def set_midi_value(self, midi_value):
        self.note_letter._set_midi_value(midi_value)
        return
    
    def alter_velocity(self, amount_to_alter_by):
        self.velocity._alter_velocity(amount_to_alter_by)
        return
    
    def alter_octave(self, amount_to_alter_by):
        self.note_letter._alter_octave(amount_to_alter_by)
        return
    
    def _is_note(self):
        return True
    
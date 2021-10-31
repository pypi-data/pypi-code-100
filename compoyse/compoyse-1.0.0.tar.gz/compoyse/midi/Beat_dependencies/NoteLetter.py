import pretty_midi
from compoyse.midi.MIDIExceptions import ValueNotValidMIDIValue

class _NoteLetter:
    def __init__(self, letter, octave):
        if(self._new_midi_value_is_in_midi_value_range(letter, octave)):
            self.letter = letter
            self.octave = octave
        return
    
    def _get_letter(self):
        return self.letter
    
    def _get_octave(self):
        return self.octave
            
    def _get_midi_value(self):
        return self.midi_value
    
    def _set_letter(self, letter):
        if(self._new_midi_value_is_in_midi_value_range(letter, self.octave)):
            self.letter = letter
        return
    
    def _set_octave(self, octave):
        if(self._new_midi_value_is_in_midi_value_range(self.letter, octave)):
            self.octave = octave
        return
        
    def _alter_octave(self, amount_to_alter_by):
        new_octave = self.octave + amount_to_alter_by
        if(self._new_midi_value_is_in_midi_value_range(self.letter, new_octave)):
            self.octave = new_octave
        return
        
    def _set_midi_value(self, midi_value):
        self.midi_value = midi_value
        return
    
    def _new_midi_value_is_in_midi_value_range(self, letter, octave):
        new_value = self._find_midi_value(letter, octave)
        if(new_value >= 0 and new_value <= 127):
            self._set_midi_value(new_value)
            return True
        else:
            raise ValueNotValidMIDIValue(str(new_value) +
                                         " is not a valid value for a note (must be greater than or equal to 0 or lesser than or equal to 127).")
            
    def _find_midi_value(self, letter, octave):
        return pretty_midi.note_name_to_number(letter + str(octave))
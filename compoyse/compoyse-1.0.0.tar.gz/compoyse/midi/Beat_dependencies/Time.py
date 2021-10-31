from compoyse.midi.MIDIExceptions import ValueNotValidRhythmicValue

class _Time:
    def __init__(self, rhythmic_value):
        self.start = 0
        self._set_rhythmic_value(rhythmic_value)
        self.length_in_seconds = 0
        return
    
    def _get_start(self):
        return self.start
    
    def _get_rhythmic_value(self):
        return self.rhythmic_value
    
    def _get_length_in_seconds(self):
        return self.length_in_seconds

    def _get_end(self):
        end = self.start + self.length_in_seconds
        return end
    
    def _set_rhythmic_value(self, value):
        if(self._rhythmic_value_is_valid(value)):
            self.rhythmic_value = value
        return
    
    def _rhythmic_value_is_valid(self, value):
        if((not isinstance(value[0], int)) and (not isinstance(value[0], str))):
            raise ValueNotValidRhythmicValue(str(value[0]) + ' is not a valid value for a tuplet designation or rhythm.')
        for i in range(1, len(value)):
            if(not isinstance(value[i], str)):
                raise ValueNotValidRhythmicValue(str(value[i]) + ' is not a valid value rhythmic value.')
        return True
    
    def _set_start_and_end(self, start, meter):
        self.start = start
        self.length_in_seconds = meter._compute_rhythmic_value_length_in_seconds(self._get_rhythmic_value())
        return
    
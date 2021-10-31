from compoyse.midi.MIDIExceptions import ValueNotValidRhythmicValue

class _Meter:
    def __init__(self):
        return
    
    def _set_length_of_quarter_in_seconds(self, bpm_length_of_quarter):
        NUMBER_OF_SECONDS_IN_A_MINUTE = 60
        self.length_of_quarter_in_seconds = (NUMBER_OF_SECONDS_IN_A_MINUTE / bpm_length_of_quarter)
        return
    
    def _compute_rhythmic_value_length_in_seconds(self, rhythmic_value):
        length = 0
        
        if(not isinstance(rhythmic_value[0], int)):
            for i in range(0, len(rhythmic_value)):
                length = length + self._compute_rhythmic_value_length_in_seconds_given_single_rhythmic_value(rhythmic_value[i])
        else: 
            # this is single note in a tuplet - 
            # [number_of_divisions_in_tuplet, 'part_of_rhythmic_value_tuplet_is_occuring_on_one', 'part_of_rhythmic_value_tuplet_is_occuring_on_two'...]
            number_of_divisions_in_tuplet = rhythmic_value[0]
            for i in range(1, len(rhythmic_value)):
                length = length + self._compute_rhythmic_value_length_in_seconds_given_single_rhythmic_value(rhythmic_value[i])
            length = length / number_of_divisions_in_tuplet
            
        return length
    
    def _compute_rhythmic_value_length_in_seconds_given_single_rhythmic_value(self, rhythmic_value):
        if(rhythmic_value == 'two_hundred_fifty_sixth'):
            return (self.length_of_quarter_in_seconds / 64)
        elif(rhythmic_value == 'one_hundred_twenty_eighth'):
            return (self.length_of_quarter_in_seconds / 32)
        elif(rhythmic_value == 'sixty_fourth'):
            return (self.length_of_quarter_in_seconds / 16)
        elif(rhythmic_value == 'thirty_secondth'):
            return (self.length_of_quarter_in_seconds / 8)
        elif(rhythmic_value == 'sixteenth'):
            return (self.length_of_quarter_in_seconds / 4)
        elif(rhythmic_value == 'eighth'):
            return (self.length_of_quarter_in_seconds / 2)
        elif(rhythmic_value == 'quarter'):
            return (self.length_of_quarter_in_seconds * 1)
        elif(rhythmic_value == 'half'):
            return (self.length_of_quarter_in_seconds * 2)
        elif(rhythmic_value == 'whole'):
            return (self.length_of_quarter_in_seconds * 4)
        raise ValueNotValidRhythmicValue(str(rhythmic_value) + ' is not a valid rhythmic value.')
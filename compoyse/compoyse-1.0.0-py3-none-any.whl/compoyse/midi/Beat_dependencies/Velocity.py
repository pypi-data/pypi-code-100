from compoyse.midi.MIDIExceptions import ValueNotValidMIDIValue

class _Velocity:
    def __init__(self, velocity):
        self._set_velocity(velocity)
        return
    
    def _get_velocity(self):
        return self.velocity
    
    def _set_velocity(self, velocity):
        if(self._new_velocity_is_in_midi_value_range(velocity)):
            self.velocity = velocity
        return
    
    def _alter_velocity(self, amount_to_alter_by):
        new_velocity = self.velocity + amount_to_alter_by
        if(self._new_velocity_is_in_midi_value_range(new_velocity)):
            self.velocity = new_velocity
        return
    
    def _new_velocity_is_in_midi_value_range(self, new_velocity):
        if(new_velocity >= 0 and new_velocity <= 127):
            return True
        else:
            raise ValueNotValidMIDIValue(str(new_velocity) + 
                                         " is not a valid value for velocity (must be greater than or equal to 0 or lesser than or equal to 127).")
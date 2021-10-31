class Velocity:
    def __init__(self, velocity):
        self.set_velocity(velocity)
        return
    
    def get_velocity(self):
        return self.velocity
    
    def set_velocity(self, velocity):
        if(self.new_velocity_is_in_midi_value_range(velocity)):
            self.velocity = velocity
        return
    
    def alter_velocity(self, amount_to_alter_buy):
        new_velocity = self.velocity + amount_to_alter_buy
        if(self.new_velocity_is_in_midi_value_range(new_velocity)):
            self.velocity = new_velocity
        return
    
    def new_velocity_is_in_midi_value_range(self, new_velocity):
        if(newVelocity >= 0 and newVelocity <= 127):
            return True
        else:
            return False
import pretty_midi
from Velocity import Velocity
from NoteLetter import NoteLetter
from Time import Time

class Note:
    def __init__(self,
                 velocity=0,
                 letter='C#',
                 octave=-2,
                 start=0,
                 length=0):
        self.set_note(velocity, letter, octave, start, length)
        return
    
    def get_note_data(self):
        return [self.velocity.get_velocity(), 
                self.note_letter.get_letter(), 
                self.note_letter.get_octave(), 
                self.start, 
                self.length, 
                self.end]
    
    def get_velocity(self):
        return self.velocity.get_velocity()
    
    def get_letter(self):
        return self.note_letter.get_letter()
    
    def get_octave(self):
        return self.note_letter.get_octave()
    
    def get_midi_value(self):
        return self.note_letter.get_midi_value()
    
    def get_start(self):
        return self.time.get_start()
    
    def get_length(self):
        return self.time.get_length()
    
    def get_midi_data(self):
        note = pretty_midi.Note(velocity=self.velocity.get_velocity(),
                                pitch=self.note_letter.get_midi_value(),
                                start=self.time.get_start(),
                                end=self.time.get_end())
        return note
    
    def set_note(self, velocity, letter, octave, start, length):
        self.velocity = Velocity(velocity)
        self.note_letter = NoteLetter(letter, octave)
        self.time = Time(start, length)
        return
    
    def set_velocity(self, velocity):
        self.velocity.set_velocity(velocity)
        return
    
    def set_letter(self, letter):
        self.note_letter.set_letter(letter)
        return
    
    def set_octave(self, octave):
        self.note_letter.set_octave(octave)
        return
    
    def set_midi_value(self, midi_value):
        self.note_letter.set_midi_value(midi_value)
        return
    
    def set_start(self, start):
        self.time.set_start(start)
        return
    
    def set_length(self, length):
        self.time.set_length(length)
        return
    
    def alter_velocity(self, amount_to_alter_buy):
        self.velocity.alter_velocity(amount_to_alter_buy)
        return
    
    def alter_octave(self, amount_to_alter_buy):
        self.note_letter.alter_octave(amount_to_alter_buy)
        return
    
    def alter_start(self, amount_to_alter_buy):
        self.time.alter_start(amount_to_alter_buy)
        return
    
    def alter_length(self, amount_to_alter_buy):
        self.time.alter_length(amount_to_alter_buy)
        return
    
    def augment_length(self, factor_to_augment_by):
        self.time.augment_length(factor_to_augment_by)
        return
    
    def diminish_length(self, factor_to_diminish_by):
        self.time.diminish_length(factor_to_diminish_by)
        return
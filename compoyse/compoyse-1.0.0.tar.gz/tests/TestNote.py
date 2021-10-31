from compoyse.midi.MIDIExceptions import ValueNotValidRhythmicValue
from tests.TestMIDI import TestMIDI
from compoyse.midi.Note import Note

class TestNote(TestMIDI):
    def test__init__whenCalled_shouldSetDefaultValues(self):
        test_note = Note()
        self.assertEqual(test_note.get_note_data(), [0,'C', 0, ['quarter']], "Notes values are the default parameters.")
        return
    
    def test_setVelocity_givenVelocity_shouldSetVelocity(self):
        self.test_note.set_velocity(100)
        self.assertEqual(self.test_note.get_velocity(), 100, "Velocity is 100.")
        return
    
    def test_setLetter_givenLetter_shouldSetLetter(self):
        self.test_note.set_letter('C')
        self.assertEqual(self.test_note.get_letter(), 'C', "Note is D.")
        return
    
    def test_setOctave_givenOctave_shouldSetOctave(self):
        self.test_note.set_octave(5)
        self.assertEqual(self.test_note.get_octave(), 5, "Octave is 5.")
        return
    
    def test_setMIDIValue_givenMIDIValue_shouldSetMIDIValue(self):
        self.test_note.set_midi_value(100)
        self.assertEqual(self.test_note.get_midi_value(), 100, "Midi value is 100.")
        return
    
    def test_setRhythmicValue_givenRhythmicValue_shouldSetRhythmicValue(self):
        self.test_note.set_rhythmic_value(['quarter'])
        self.assertEqual(self.test_note.get_rhythmic_value(), ['quarter'], "Note is a quarter note.")
        return
    
    def test_setRhythmicValue_givenInvalidRhythmicValue_shouldRaiseValueNotValidRhythmicValueException(self):
        self.assertRaises(ValueNotValidRhythmicValue, self.test_note.set_rhythmic_value, ['quarter', 0])
        return
    
    def test_getMIDIData_whenCalled_shouldReturnMIDIData(self):
        self.test_note._set_start_and_end(0, self.test_meter)
        
        test_note_midi_data = self.test_note._get_midi_data()
        
        self.assertEqual(test_note_midi_data.get_duration(), 1, "MIDI note calls pretty_midi function and is 1 second long.")
        return
    
    def test_alterVeloicty_givenAmountToAlterBy_shouldAlterVelocity(self):
        self.test_note.alter_velocity(10)
        self.assertEqual(self.test_note.get_velocity(), 110, 'Notes veloicty is now 110.')
        return 
    
    def test_alterOctave_givenAmountToAlterBy_shouldAlterOctave(self):
        self.test_note.alter_octave(1)
        self.assertEqual(self.test_note.get_octave(), 5, 'Notes octave is now 5.')
        return
    
    def test_isNote_whenCalled_shouldReturnTrue(self):
        self.assertEqual(self.test_note._is_note(), True, "This is a note.")
        return
    
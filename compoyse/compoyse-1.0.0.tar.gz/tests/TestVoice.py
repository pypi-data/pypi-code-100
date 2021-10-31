from tests.TestMIDI import TestMIDI

class TestVoice(TestMIDI):
    def test_getMeasureAtIndex_givenIndex_shouldReturnMeasure(self):
        self.assertEqual(self.test_voice.get_measure_at_index(1).get_number_of_beats(), 3, 'Number of beats is 3.')
        return
    
    def test_getNumberOfMeasures_whenCalled_shouldReturnNumberOfMeasures(self):
        self.assertEqual(self.test_voice.get_number_of_measures(), 3, 'There are 3 measures.')
        return
    
    def test_addMeasure_givenMeasure_shouldAddMeasure(self):
        self.test_voice.add_measure(self.measure_to_add)
        self.assertEqual(self.test_voice.get_measure_at_index(3).get_number_of_beats(), 1, 'Number of beats is 1.')
        return
    
    def test_setName_givenName_shouldSetName(self):
        self.test_voice.set_name('Trombone')
        self.assertEqual(self.test_voice.get_name(), 'Trombone', 'Name is trombone.')
        return
    
    def test_getLength_whenCalled_shouldReturnLength(self):
        self.assertEqual(self.test_voice._get_length(self.test_meter), 9, 'Voices length is 9.')
        return
    
from tests.TestMIDI import TestMIDI
import os.path

class TestComposition(TestMIDI):
    def test_getSectionAtIndex_givenIndex_shouldReturnSection(self):
        self.assertEqual(self.test_composition.get_section_at_index(1).get_number_of_voices(), 3, 'Number of voices is 3.')
        return
    
    def test_getNumberOfSections_whenCalled_shouldReturnNumberOfSections(self):
        self.assertEqual(self.test_composition.get_number_of_sections(), 3, 'There are 3 sections.')
        return
        
    def test_addSection_givenSection_shouldAddSection(self):
        self.test_composition.add_section(self.section_to_add)
        self.assertEqual(self.test_composition.get_section_at_index(3)._get_length(), 1, 'Added sections length is 1.')
        return
    
    def test_getLength_givenCompositionHasSections_shouldReturnLength(self):
        self.assertEqual(self.test_composition.get_length(), 27, 'Compositions length is 27.')
        
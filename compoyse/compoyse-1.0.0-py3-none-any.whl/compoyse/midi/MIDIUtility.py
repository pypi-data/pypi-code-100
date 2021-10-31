from compoyse.midi.Composition import Composition
from datetime import datetime

class MIDIUtility:
    def get_current_date_and_time_formatted(self):
        current_time = datetime.now()
        current_time_formatted =  current_time.strftime("%Y.%m.%d %H.%M.%S")
        return current_time_formatted
    
    def get_all_12tet_pitches_as_array(self):
        return ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    
    def arrange_sections_in_given_order_in_composition(self, order, composition):
        new_composition = Composition()
        for i in range(0, len(order)):
            for j in range(0, composition.get_number_of_sections()):
                current_section = composition.get_section_at_index(j)
                if order[i] == current_section.get_identifier():
                    new_composition.add_section(current_section)
        return new_composition
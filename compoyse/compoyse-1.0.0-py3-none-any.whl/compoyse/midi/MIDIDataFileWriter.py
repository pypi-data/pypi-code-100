import pretty_midi

class MIDIDataFileWriter:
    def __init__(self, 
                 composition, 
                 put_voices_in_same_track=True, 
                 fileName='compoyse_composition'):
        composition_midi_data = self._get_composition_midi_data(composition, 
                                                                put_voices_in_same_track)
        self._write_midi_data(composition_midi_data, 
                              fileName)
        return
    
    def _get_composition_midi_data(self, 
                                   composition, 
                                   put_voices_in_same_track):
        midi_instruments = self._create_midi_instruments(put_voices_in_same_track, 
                                                         composition)
        section_start = 0
        for i in range(0, composition.get_number_of_sections()):
            current_section = composition.get_section_at_index(i)
            section_start = self._get_section_midi_data(current_section, 
                                                        section_start, midi_instruments, 
                                                        put_voices_in_same_track, 
                                                        self._get_number_of_voices_up_until_now(composition, i))
        return midi_instruments
    
    def _create_midi_instruments(self, 
                                 put_voices_in_same_track, 
                                 composition):
        midi_instruments = []
        if(put_voices_in_same_track is True):
            first_section = composition.get_section_at_index(0)
            for i in range(0, first_section.get_number_of_voices()):
                midi_instruments.append(self._create_midi_instrument(first_section.get_voice_at_index(i).get_name()))
        else:
            for i in range(0, composition.get_number_of_sections()):
                current_section = composition.get_section_at_index(i)
                for j in range(0, current_section.get_number_of_voices()):
                    midi_instruments.append(self._create_midi_instrument(current_section.get_voice_at_index(j).get_name()))
        return midi_instruments
    
    def _create_midi_instrument(self, 
                                instrument_name):
        return pretty_midi.Instrument(program=pretty_midi.instrument_name_to_program('Cello'), 
                                      name=instrument_name)
    
    def _get_number_of_voices_up_until_now(self, 
                                           composition, 
                                           current_section_index):
        number_of_voices_up_until_now = 0
        for i in range(0, current_section_index):
            number_of_voices_up_until_now = number_of_voices_up_until_now + composition.get_section_at_index(i).get_number_of_voices()
        return number_of_voices_up_until_now
            
    def _get_section_midi_data(self, 
                               current_section, 
                               section_start, 
                               midi_instruments, 
                               put_voices_in_same_track, 
                               number_of_voices_up_until_now):
        length_of_each_voice_in_section = []
        for i in range(0, current_section.get_number_of_voices()):
            current_voice = current_section.get_voice_at_index(i)
            current_place_in_time = section_start
            
            if(put_voices_in_same_track is True):
                length_of_each_voice_in_section.append(self._get_voice_midi_data(current_voice, 
                                                                                current_place_in_time, 
                                                                                current_section._get_meter(), 
                                                                                midi_instruments[i]))
            else:
                length_of_each_voice_in_section.append(self._get_voice_midi_data(current_voice, 
                                                                                current_place_in_time, 
                                                                                current_section._get_meter(), 
                                                                                midi_instruments[number_of_voices_up_until_now + i]))
        return max(length_of_each_voice_in_section)
    
    def _get_voice_midi_data(self, 
                             current_voice, 
                             current_place_in_time, 
                             current_meter, 
                             midi_instrument):
        for i in range(0, current_voice.get_number_of_measures()):
            current_measure = current_voice.get_measure_at_index(i)
            current_place_in_time = self._get_measure_midi_data(current_measure, 
                                                                current_place_in_time, 
                                                                current_meter, 
                                                                midi_instrument)
        return current_place_in_time
    
    def _get_measure_midi_data(self, 
                               current_measure, 
                               current_place_in_time, 
                               current_meter, 
                               midi_instrument):
        for i in range(0, current_measure.get_number_of_beats()):
            current_beat = current_measure.get_beat_at_index(i)
            current_beat._set_start_and_end(current_place_in_time, current_meter)
            if current_beat._is_note():
                midi_instrument.notes.append(self._get_note_midi_data(current_beat))
            current_place_in_time = current_place_in_time + current_beat._get_length_in_seconds()
        return current_place_in_time
    
    def _get_note_midi_data(self, 
                            current_beat):
        return current_beat._get_midi_data()
    
    def _write_midi_data(self, 
                         composition_midi_data, 
                         fileName):
        midi_file = self._create_midi_file(composition_midi_data)
        midi_file.write(fileName + '.mid')
        return
    
    def _create_midi_file(self, 
                          composition_midi_data):
        midi_file = pretty_midi.PrettyMIDI()
        for i in range(0, len(composition_midi_data)):
            midi_file.instruments.append(composition_midi_data[i])
        return midi_file
        
from Note import Note
import pretty_midi

# note = Note()
# note.set_note('C', 4, 0, 10, 100)

note = Note(velocity=100,
            letter='D',
            octave=4,
            end=10)
print(note.get_note_data())

pm = pretty_midi.PrettyMIDI()
instrument_program=pretty_midi.instrument_name_to_program('Cello')
instrument = pretty_midi.Instrument(program=instrument_program)
instrument.notes.append(note.get_midi_data())
pm.instruments.append(instrument)
pm.write('demo' + '.mid')
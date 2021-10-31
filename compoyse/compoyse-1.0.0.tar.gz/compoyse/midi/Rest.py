from compoyse.midi.Beat import _Beat

class Rest(_Beat):
    def __init__(self):
        super().__init__()
        return
    
    def _is_note(self):
        return False
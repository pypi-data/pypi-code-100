""" Auto-Generated Code for sknrf Sequencer"""

from sknrf.model.sequencer.base import AbstractSequencerRuntimeModel

#  Module Import List


class SequencerRuntimeModel(AbstractSequencerRuntimeModel):
    
    def measure(self):
        #  Variable Declaration Section
        
        # Load Sequencer Namespace
        self.connect_signals()
        globals().update(self._locals)
        try:
            
            #  Action Sequence Section
            pass
        finally:
            #  Unload Sequencer Namespace
            for k in self._locals.keys():
                globals().pop(k)
            self.disconnect_signals()
class Voice:
    def __init__(self):
        self.measures = []
        self.name = 'voice'
        return
    
    def get_name(self):
        return self.name

    def get_measure_at_index(self, index):
        return self.measures[index]
    
    def get_number_of_measures(self):
        return len(self.measures)
    
    def set_name(self, name):
        self.name = name
        return

    def add_measure(self, measure):
        self.measures.append(measure)
        return
    
    def _get_length(self, meter):
        current_length = 0
        for i in range(0, len(self.measures)):
            current_length = current_length + self.measures[i]._get_length(meter)
        return current_length
class Composition:
    def __init__(self):
        self.sections = []
        return
    
    def get_section_at_index(self, index):
        return self.sections[index]
    
    def get_number_of_sections(self):
        return len(self.sections)
    
    def add_section(self, section):
        self.sections.append(section)
        return
    
    def get_length(self):
        current_length = 0
        for i in range(0, len(self.sections)):
            current_length = current_length + self.get_section_at_index(i)._get_length()
        return current_length
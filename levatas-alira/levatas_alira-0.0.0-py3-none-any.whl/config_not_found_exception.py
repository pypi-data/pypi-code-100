class ConfigNotFoundException(Exception):
    def __init__(self, not_found_key):
        self.not_found_key = not_found_key
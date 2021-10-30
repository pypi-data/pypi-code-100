################################################################################
# MMI v2.0
# Codename: Fir
# Copyright 2021 Fe-Ti
################################################################################
# Directory handler
#
from pathlib import Path

class PathHandler:
    def __init__(self, some_path, target_file=''):
        self.path = Path(str(some_path))
        if not self.path.is_absolute():
            self.path = self.path.cwd() / Path(str(target_file)).parent / self.path
    def __str__(self):
        return str(self.path)
    def str(self):
        return str(self.path)


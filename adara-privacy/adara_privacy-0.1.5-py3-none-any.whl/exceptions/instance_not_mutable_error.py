class InstanceNotMutableError(Exception):
    def __init__(self, class_name: str, *args, **kwargs):
        super().__init__(f'This instance of "{class_name}" is locked and cannot be mutated.')

class MissingRequiredSettingError(Exception):
    def __init__(self, setting_name: str, *args, **kwargs):
        super().__init__(f'Missing required setting "{setting_name}".  Please check the configuration file to ensure this value has been added.', *args, **kwargs)

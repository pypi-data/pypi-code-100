from configparser import ConfigParser

prefs = None

defaults = {
        'Main': {
            'logging': 'info',
            'cache': r'''C:\Windows\Temp\ppt-cache''',
            'cache_format': 'JPG',
            'cache_timeout': 5*60,
            'cache_init': True,
            'blackwhite': 'both',
            'refresh': 2,
            'disable_protected': True
        },
        'HTTP': {
            'interface': '',
            'port': 80
        },
        'WebSocket': {
            'interface': '0.0.0.0',
            'port': 5678
        }
}


def loadconf(configpaths):
    """
    Initial setup for a ConfigParser object. `configpaths` should be a list of
    configuration files to load (typically only one). To use the generated
    ConfigParser, use `import logparse.config` and then `config.prefs.get(..)`.
    The prefs object is returned after creation as a convenience but this method
    should only be called once per runtime.
    """
    prefs = ConfigParser()
    prefs.read_dict(defaults)
    try:
        success = prefs.read(configpaths)
        print("Loaded {0} config file(s): {1}".format(
                str(len(success)), str(success)))
    except Exception as e:
        print("Error processing config: " + str(e))
    return prefs

def export_defaults(file):
    """
    Write the default settings to a file object, including comments and with spaces around 
    delimeters. This function is intended to be used to populate the config file with defaults
    after installation.
    """
    prefs = loadconf([])
    prefs.write(file, space_around_delimiters=True)

from pathlib import Path
import os
import platform


OS_DIC = {
    'Windows': {
        'Global': ['C:\\', 'ProgramData', 'pip'],
        'User': [ os.environ.get('HOMEPATH'), 'pip'],
        'File': 'pip.ini'
    },
    'Linux': {
        # TODO
    }
}


class Configurator:

    OS = OS_DIC.get(platform.system())

    def __init__(self, level = '', configuration = ''):
        self.level = level
        self.configuration = configuration 
        if(level != ''):
            try:
                self.PATH = Path(*self.OS.get(level)).absolute()            
                os.makedirs(self.PATH)
            except OSError:
                pass

        # print(self.PATH)

    def config(self):
        try:
            with open(self.PATH.joinpath(self.OS.get('File')), 'w') as f:
                if(f.writable()):
                    f.writelines(self.configuration)
                    return True
                return False
        except:
            return False


    def searchConfigs(self):
        configs = []
        for l, p in self.OS.items():
            path = Path(*p)
            if( path.joinpath(self.OS.get('File')).exists() and os.path.getsize(path.joinpath(self.OS.get('File'))) != 0 ):
                configs.append((l, path.__str__()))
        return configs
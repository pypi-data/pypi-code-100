from . import SIMPLE_PATH
import os

class Package:

    def __init__( self, name, versions = []):
        self.name = name
        self.versions: Version = versions

    def __str__(self):
        return f'{self.name} - {self.versions}'


class Version():

    def __init__(self, fullname, v, size):
        self.fullname = fullname
        self.v = v
        self.size = size


class Repo(object):

    __instance = None
    packages: {str: Package} = {}
    size: int = 0
    total_versions: int = 0

    def __init__(self):
        self.loadPackages()
    
    def __new__(cls):
        if Repo.__instance is None:
            Repo.__instance = object.__new__(cls)
        return Repo.__instance

    def getName(self, pkg):
        return pkg.name.split('-')[0].lower().replace('.', '-')

    def toVersion(self, pkg):
        version = pkg.name.split('-')[1].replace('.tar.gz', '').replace('.whel', '')
        return Version(pkg.name, version, os.path.getsize(pkg))

    def loadPackages(self):
        self.packages = {}
        self.size = 0
        self.total_versions = 0

        for pkg in SIMPLE_PATH.iterdir():
            name = self.getName(pkg) #Nombre de la clave del diccionario
            version = self.toVersion(pkg)
            if ( name not in self.packages.keys() ):
                self.size += version.size
                self.total_versions += 1
                self.packages[name] = Package(name, [version, ])
            else: 
                # if( version.v not in [v.v for v in self.packages[name].versions] ):
                self.size += version.size
                self.total_versions += 1
                self.packages[name].versions.append(version)

    def getPackage(self, name):
        try:
            if ( name not in self.packages.keys() ):
                name = name.replace(".","-")
                if ( name not in self.packages.keys() ):
                    name = name.replace("-","_")

            return self.packages[name].versions
        except:
            return []
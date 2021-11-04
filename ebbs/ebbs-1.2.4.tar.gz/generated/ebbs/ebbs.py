import os
import logging
from abc import abstractmethod
from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT
from distutils.dir_util import mkpath
import eons as e
import argparse
import requests
from zipfile import ZipFile

######## START CONTENT ########
# All builder errors
class BuildError(Exception): pass


# Exception used for miscillaneous build errors.
class OtherBuildError(BuildError): pass


# Project types can be things like "lib" for library, "bin" for binary, etc. Generally, they are any string that evaluates to a different means of building code.
class ProjectTypeNotSupported(BuildError): pass


class Builder(e.UserFunctor):
    def __init__(self, name=e.INVALID_NAME()):
        super().__init__(name)
        
        self.requiredKWArgs.append("dir")

        self.supportedProjectTypes = []

        #TODO: project is looking an awful lot like a Datum.. Would making it one add functionality?
        self.projectType = "bin"
        self.projectName = e.INVALID_NAME()

    #Build things!
    #Override this or die.
    @abstractmethod
    def Build(self):
        raise NotImplementedError

    #Projects should have a name of {project-type}_{project-name}.
    #For information on how projects should be labelled see: https://eons.dev/convention/naming/
    #For information on how projects should be organized, see: https://eons.dev/convention/uri-names/
    def PopulateProjectDetails(self):
        details = os.path.basename(os.path.abspath(os.path.join(self.buildPath,"../"))).split("_")
        self.projectType = details[0]
        if (len(details) > 1):
            self.projectName = '_'.join(details[1:])
        
    #Sets the build path that should be used by children of *this.
    #Also sets src, inc, lib, and dep paths, if they are present.
    def SetBuildPath(self, path):
        self.buildPath = path

        #TODO: Consolidate this code with more attribute hacks?
        rootPath = os.path.abspath(os.path.join(self.buildPath, "../"))
        if (os.path.isdir(rootPath)):
            self.rootPath = rootPath
        else:
            self.rootPath = None
        srcPath = os.path.abspath(os.path.join(self.buildPath, "../src"))
        if (os.path.isdir(srcPath)):
            self.srcPath = srcPath
        else:
            self.srcPath = None
        incPath = os.path.abspath(os.path.join(self.buildPath, "../inc"))
        if (os.path.isdir(incPath)):
            self.incPath = incPath
        else:
            self.incPath = None
        depPath = os.path.abspath(os.path.join(self.buildPath, "../dep"))
        if (os.path.isdir(depPath)):
            self.depPath = depPath
        else:
            self.depPath = None
        libPath = os.path.abspath(os.path.join(self.buildPath, "../lib"))
        if (os.path.isdir(srcPath)):
            self.libPath = libPath
        else:
            self.libPath = None

    #Hook for any pre-build configuration
    def PreBuild(self, **kwargs):
        pass

    #Hook for any post-build configuration
    def PostBuild(self, **kwargs):
        # TODO: Do we need to clear self.buildPath here?
        pass

    def UserFunction(self, **kwargs):
        self.SetBuildPath(kwargs.get("dir"))
        self.PopulateProjectDetails()
        self.PreBuild(**kwargs)
        if (len(self.supportedProjectTypes) and self.projectType not in self.supportedProjectTypes):
            raise ProjectTypeNotSupported(f"{self.projectType} is not supported. Supported project types for {self.name} are {self.supportedProjectTypes}")
        logging.info(f"Using {self.name} to build {self.projectName}, a {self.projectType}")
        self.Build()
        self.PostBuild(**kwargs)

    #RETURNS: an opened file object for writing.
    #Creates the path if it does not exist.
    def CreateFile(self, file, mode="w+"):
        mkpath(os.path.dirname(os.path.abspath(file)))
        return open(file, mode)

    #Run whatever.
    #DANGEROUS!!!!!
    #TODO: check return value and raise exceptions?
    #per https://stackoverflow.com/questions/803265/getting-realtime-output-using-subprocess
    def RunCommand(self, command):
        p = Popen(command, stdout = PIPE, stderr = STDOUT, shell = True)
        while True:
          line = p.stdout.readline()
          if (not line):
            break
          print(line.decode('ascii')[:-1]) #[:-1] to strip excessive new lines.


class EBBS(e.Executor):

    def __init__(self):
        super().__init__(name="eons Basic Build System", descriptionStr="A hackable build system for all languages!")

        self.RegisterDirectory("language")
        self.RegisterDirectory("inc/language")
        self.RegisterDirectory("ebbs/inc/language")

    #Override of eons.Executor method. See that class for details
    def RegisterAllClasses(self):
        super().RegisterAllClasses()
        self.RegisterAllClassesInDirectory(os.path.join(os.path.dirname(os.path.abspath(__file__)), "language"))

    #Override of eons.Executor method. See that class for details
    def AddArgs(self):
        super().AddArgs()
        self.argparser.add_argument('dir', type = str, metavar = '/project/build', help = 'path to build folder', default = '.')
        self.argparser.add_argument('-l','--language', type = str, metavar = 'cpp', help = 'language of files to build', dest = 'lang')
        self.argparser.add_argument('--repo-store', type=str, default='./ebbs/inc/language', help='file path for storing downloaded packages', dest = 'store')
        self.argparser.add_argument('--repo-url', type = str, default='https://api.infrastructure.tech/v1/package', help = 'package repository for additional languages', dest = 'url')
        self.argparser.add_argument('--repo-username', type = str, help = 'username for http basic auth', dest = 'username')
        self.argparser.add_argument('--repo-password', type = str, help = 'password for http basic auth', dest = 'password')

    #Override of eons.Executor method. See that class for details
    def ParseArgs(self):
        super().ParseArgs()

        if (not self.args.lang):
            self.ExitDueToErr("You must specify a language.")

    #Override of eons.Executor method. See that class for details
    def UserFunction(self, **kwargs):
        super().UserFunction(**kwargs)
        self.Build()

    #Build things!
    def Build(self):
        try:
            builder = self.GetRegistered(self.args.lang)
        except:
            logging.debug(f'Builder for {self.args.lang} not found. Trying to download from repository.')
            try: #again
                self.DownloadPackage(f'build_{self.args.lang}')
                builder = self.GetRegistered(self.args.lang)
            except Exception as e:
                logging.error(f'Could not find builder for {self.args.lang}: {e}')
                raise OtherBuildError(f'Could not get builder for {self.args.lang}')
                return #just for extra safety.

        repoData = {}
        if (self.args.store and self.args.url and self.args.username and self.args.password):
            repoData = {
                'store': self.args.store,
                'url': self.args.url,
                'username': self.args.username,
                'password': self.args.password
            }

        builder(dir = self.args.dir, repo = repoData, **self.extraArgs)

    #Attempts to download the given package from the repo url specified in calling args.
    #Will refresh registered builders upon success
    #RETURNS void
    #Does not guarantee new builders are made available; errors need to be handled by the caller.
    def DownloadPackage(self, packageName):

        url = f'{self.args.url}/download?package_name={packageName}'

        auth = None
        if self.args.username and self.args.password:
            auth = requests.auth.HTTPBasicAuth(self.args.username, self.args.password)

        packageQuery = requests.get(url, auth=auth)

        if (packageQuery.status_code != 200 or not len(packageQuery.content)):
            logging.error(f'Unable to download {packageName}')
            #TODO: raise error?
            return #let caller decide what to do next.

        if (not os.path.exists(self.args.store)):
            logging.debug(f'Creating directory {self.args.store}')
            mkpath(self.args.store)

        packageZip = os.path.join(self.args.store, f'{packageName}.zip')

        logging.debug(f'Writing {packageZip}')
        open(packageZip, 'wb+').write(packageQuery.content) #TODO: close?
        if (not os.path.exists(packageZip)):
            logging.error(f'Failed to create {packageZip}')
            return

        logging.debug(f'Extracting {packageZip}')
        ZipFile(packageZip, 'r').extractall(f'{self.args.store}') #TODO: close?

        logging.debug(f'Registering classes in {self.args.store}')
        self.RegisterAllClassesInDirectory(self.args.store)

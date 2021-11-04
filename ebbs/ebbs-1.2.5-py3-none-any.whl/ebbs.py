import os
import logging
from abc import abstractmethod
from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT
from distutils.dir_util import mkpath
import eons as e

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
        builder = self.GetRegistered(self.args.lang, "build")

        repoData = {}
        if (self.args.repo_store and self.args.repo_url and self.args.repo_username and self.args.repo_password):
            repoData = {
                'store': self.args.repo_store,
                'url': self.args.repo_url,
                'username': self.args.repo_username,
                'password': self.args.repo_password
            }

        builder(dir=self.args.dir, repo=repoData, **self.extraArgs)



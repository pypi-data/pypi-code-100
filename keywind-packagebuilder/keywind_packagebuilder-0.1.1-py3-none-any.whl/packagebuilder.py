import os, logging
logging.basicConfig(level = logging.DEBUG, format = "%(message)s")
class BuilderData:
    def __init__(self):
        self.setup = "import setuptools\nwith open(\"README.md\", \"r\", encoding=\"utf-8\") as fh:\n\tlong_description = fh.read()\nsetuptools.setup(\n\tname=\"\",\n\tversion=\"0.0.0\",\n\tauthor=\"\",\n\tauthor_email=\"\",\n\tdescription=\"\",\n\tlong_description=long_description,\n\tlong_description_content_type=\"text/markdown\",\n\turl=\"\",\n\tproject_urls={\n\t\t\"Bug Tracker\": \"\",\n\t},\n\tclassifiers=[\n\t\t\"Programming Language :: Python :: 3\",\n\t\t\"License :: OSI Approved :: MIT License\",\n\t\t\"Operating System :: OS Independent\",\n\t],\n\tpackage_dir={\"\": \"src\"},\n\tpackages=setuptools.find_packages(where=\"src\"),\n\tpython_requires=\">=3.6\",\n\t\n\tinstall_requires=[\n\t\t'markdown'\n\t]\n\t\n)"
        self.pyproject = "[build-system]\nrequires = [\n\t\"setuptools>=42\",\n\t\"wheel\"\n]\nbuild-backend = \"setuptools.build_meta\""
        self.license = ("Copyright (c) <year> <copyright holders>\n\
Permission is hereby granted, free of charge, to any person obtaining a copy\n\
of this software and associated documentation files (the \"Software\"), to deal\n\
in the Software without restriction, including without limitation the rights\n\
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n\
copies of the Software, and to permit persons to whom the Software is\n\
furnished to do so, subject to the following conditions:\n\
\n\
The above copyright notice and this permission notice shall be included in all\n\
copies or substantial portions of the Software.\n\
\n\
THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n\
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n\
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n\
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n\
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n\
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n\
SOFTWARE.")
class Builder:
    def help():
        logging.debug("Builder(): __init__(self, packagename, folderpath = './', openwith = None)\n")
    def __init__(self, packagename, folderpath = './', openwith = None):
        self.packagename, self.folderpath = packagename, folderpath
        self.openwith = openwith
        self.rootpath = self.__mod_path(self.__mod_path(self.folderpath) + self.packagename)
        self.builderData = BuilderData()
        self.__change_dir()
        self.__build_root()
        self.__build_path()
        self.__create_file()
        self.__create_rootfile()
    def __change_dir(self):
        os.chdir(self.folderpath)
    def __check_create(self, path):
        if not (os.path.exists(path)):
            os.mkdir(path)
    def __build_root(self):
        self.__check_create(self.packagename)
    def __mod_path(self, path):
        return (path if (path[-1] == '/') else (path + '/'))
    def __build_path(self):
        self.path = self.rootpath + 'src/'
        self.__check_create(self.path)
        self.path += (self.__mod_path(self.packagename))
        self.__check_create(self.path)
    def __open_with(self, filename):
        if (os.path.isfile(filename) and (self.openwith != None)):
            try:
                os.system(f"{self.openwith} {filename}")
            except:
                logging.debug(f"Could not open {filename} with {self.openwith}.")
    def __create_file(self):
        with open(self.path + '__init__.py', 'w') as FILE:
            FILE.write(f"from {self.packagename} import {self.packagename}")
        self.__open_with(self.path + '__init__.py')
        with open(self.path + self.packagename + '.py', 'w') as FILE:
            FILE.write('')
        self.__open_with(self.path + self.packagename + '.py')
    def __create_rootfile(self):
        with open(self.rootpath + 'README.md', 'w') as FILE:
            FILE.write('')
        self.__open_with(self.rootpath + 'README.md')
        with open(self.rootpath + 'setup.py', 'w') as FILE:
            FILE.write(self.builderData.setup)
        self.__open_with(self.rootpath + 'setup.py')
        with open(self.rootpath + 'pyproject.toml', 'w') as FILE:
            FILE.write(self.builderData.pyproject)
        self.__open_with(self.rootpath + 'pyproject.toml')
        with open(self.rootpath + 'LICENSE', 'w') as FILE:
            FILE.write(self.builderData.license)
        self.__open_with(self.rootpath + 'LICENSE')
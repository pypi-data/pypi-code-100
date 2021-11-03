import os, logging
logging.basicConfig(level = logging.DEBUG, format = "%(message)s")
class ExceptionPackages:
    def __init__(self):
        self.exceptionList = {
            "keywind-albumplayer" : [ "pip install pipwin", "pipwin install pyaudio", "pip3 install keywind-albumplayer" ]
        }
    def __format_name(self, name):
        return name.split("==")[0]
    def __get_instruction(self, name):
        return [ f"pip3 install {name}" ]
    def get_command(self, name):
        name = self.__format_name(name)
        if (name in self.exceptionList):
            return self.exceptionList[name]
        else:
            return self.__get_instruction(name)
class Installer:
    exceptionList = ExceptionPackages()
    def help():
        logging.debug("Installer(): self.__init__(self, name)\n")
    def __init__(self, name):
        self.__execute_commands(self.exceptionList.get_command(name))
    def __execute_commands(self, commands):
        for command in commands:
            os.system(command)
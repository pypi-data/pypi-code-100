import warnings
from time import sleep
from utils.system import paths, command
from utils.thread_helpers import thread
from playerFramework.exceptions import *
import subprocess


class player:
    """
    This will be the API to interact with the player, the player class can not be initialised without
    a valid path to the player if the player file does not exist an exception will be raised
    """
    def __init__(self, executable: str, info: dict, warning=True):
        """
        :param warning:
        boolean to spit out warnings
        default set to True

        :param executable:
        path to the executable file

        :param info:
        a dictionary containing the IO file path and commands to pause or play the player
        i.e.
        {
            'io file': '/Users/*/.ioFile',
            'play' : ['player', '**path**'],
            'pause': 'pause',
            'resume': 'resume',
            'exit': 'stop',
            'exit_codes': [4, 5, 6]
            'Volume': 'volume:{}'
        }

        if the player does not conform to the standard arg[0] == executable_path and arg[1] == track_path
        the 'play' value must be a list which defines how the player will ba called via subprocesses/utils
        with the keyword '**path**' which defines where the framework will replace it with the path to the track
        otherwise leave 'play' to the value of None

        exit_codes value is optional although if the player exits with the codes [15, 9, 2, 4] an exception will be
        raised playerFramework.exceptions.ProcessTerminatedExternally
        """
        self.internalKill = False
        self.warning = warning
        self.exec = paths.Path(executable)
        self.info = info
        self.thread = None

        self.exitCodes = [15, 9, 2]

        if info.__contains__('exit_codes'):
            for code in info['exit_codes']:
                self.exitCodes.append(int(abs(code)))


        if not self.exec.isPath():
            raise PlayerPathNotValid('Player not found')

    def changeValue(self, key_name, Format=False):
        """
        :param key_name:
        Will be used to find the value against info dictionary
        :param Format:
        Value to format the string via {}
        :return:
        """
        try:
            if Format is False:
                with open(self.info['io file'], 'w+') as file:
                    file.write(self.info[key_name])
            else:
                writeINFO = self.info[key_name].format(Format)
                with open(self.info['io file'], 'w+') as file:
                    file.write(writeINFO)

        except FileNotFoundError or PermissionError as exception:
            raise UnableToWriteToIOFile(exception)

        except KeyError as exception:
            raise UndefinedKeyName(exception)

    def play_track(self, track_path, main_thread=False):
        """
        The player will not be run on the main thread
        to wait till the player is completed on the main thread use .wait_for_player()

        :param main_thread:
        by default set to false, if true the player will be on the main thread
        :param track_path:
        path to the file that will be played
        :return:
        """

        def internal_player(playerClass, track):
            arguments = [playerClass.exec.path]
            playINFO = playerClass.info['play']
            if playINFO is None:
                arguments.append(track_path)
            else:
                for a in playINFO:
                    if a == '**path**':
                        a = track

                    arguments.append(a)

            try:
                process = subprocess.Popen(args=arguments, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                                           stderr=subprocess.STDOUT)

                # any code executed after this point means the player is not alive
                self.thread = None

                process.communicate()[0].decode('utf8')
                process.wait()
                process.poll()
                return_code = int(abs(process.returncode))

                if self.internalKill is not True:
                    for code in self.exitCodes:
                        if return_code == code:
                            raise ProcessTerminatedExternally(code)

                # print('Return Code: ' + return_code.__str__())


                # print('exit code', return_code)

            except KeyboardInterrupt:
                warning = 'Player was stopped by KeyBoardInterrupt'
                if playerClass.warning:
                    # Not raising an exception just letting the user know
                    warnings.warn(warning)

            self.thread = None
            self.process = None

        self._kill_player()
        if main_thread:
            internal_player(playerClass=self, track=track_path)
        else:
            self.thread = thread(func=internal_player, args=[self, track_path])

    def wait_for_player(self):
        if self.thread is not None:
            self.thread.join()

    def is_playing(self):
        if self.thread is None:
            return False
        elif self.thread is not None:
            return True

    def _kill_player(self):
        # We are making an assumption here for the name that will be shown when the player is running
        # so far works fine (tests with pod2 & player)
        self.internalKill = True
        command(['killall', self.exec.last_component()], quite=True)
        sleep(0.1)
        self.internalKill = False

    def exit(self):
        self._kill_player()

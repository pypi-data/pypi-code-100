"""
GNU-Screen session module handler for Python
============================================

Dependencies
----------
gnu-screen : apt-get install screen

Description
----------
Screen is a Vanilla Python module create to manage easyly command process,
with an undeterminate ending like a minecraft server.
It was actually build only on linux, so you should rewrite this for windows.

Repository
----------
Github : https://github.com/LoucasMaillet/Lib-GNU-Screen

Author
----------
Lucas Maillet : loucas.maillet.pro@gmail.com

License
----------
GPL-3.0 License
"""

__version__ = "0.0.1"
__author__ = 'Lucas Maillet'
__credits__ = 'None'

import os
from time import sleep
import re
from threading import Thread
from typing import List


MARK = "@&$£"
ROOT = (os.getenv("TEMP") if os.name == "nt" else "/tmp") + os.path.sep


class Screen:
    """

    Description
    ----------
    A representation of a gnu-screen session.

    """

    def __init__(self, id: any, mode: str):
        """

        Description
        ----------
        Create/connect to a screen session.

        Parameters
        ----------
        id : ANY
            Id of your screen's session.
        mode : STRING <optional>
            "s" if you want to save logs, required if you use "stdout" event.
            Defaults to None.

        """

        self.logFilePath = self.pid = self.date = self.state = None
        if mode == "s":
            self.logFilePath = f"{ROOT}{id}"
        self.id: str = f"{MARK}{id}{MARK}{mode}{MARK}"
        self.events = {"stdout": lambda: None, "close": lambda: None}

    def __repr__(self) -> str:
        """

        Returns
        ----------
        selfItem : STRING
            A correct representation of Screen.

        """
        return f"{object.__repr__(self)}\n" + "\n".join("\t%s: %s" % item for item in self.__dict__.items())

    def on(self, call: callable):
        """

        Description
        ----------
        Add an event.

        Parameters
        ----------
        call : CALLABLE
            Event to add.

        """
        if not call.__name__ in self.events:
            raise TypeError(f"Event '{call.__name__}' isn't available.")
        self.events[call.__name__] = call

    def exist(self) -> bool:
        """

        Description
        ----------
        Check if screen session already exist.

        Returns
        ----------
        res : BOOLEAN
            Screen session status.

        """

        res = self.id in os.popen(f"screen -ls").read()
        if not res:
            self.pid = self.date = self.state = None
        return res

    def setup(self):
        """

        Description
        ----------
        Set some Screen variable if screen session exist.

        """
        res = os.popen(f"screen -ls").read()
        if self.id in res:
            for line in res.split("\n"):
                if self.id in line:
                    self.pid = int(re.findall(r"(?<=\t)(.*?)(?=\.)", line)[0])
                    self.date, self.state = re.findall(
                        "(?<=\()(.*?)(?=\))", line)
        else:
            self.pid = self.date = self.state = None

    def setStdout(self):
        """

        Description
        ----------
        Require logs to be saved and screen session to run.
        Call "stdout" event for every latest log from screen session's logFilePath.
        Infinite loop until his pid is None.

        Event
        ----------
        stdout (line : STRING)
            Called when a new line is writted in the logFilePath.

        """

        if not self.logFilePath:
            raise FileNotFoundError("LogFile not found.")

        def _stdWatcher():
            file = open(self.logFilePath, "r")
            file.read()
            file.seek(0, 1)
            while self.pid:
                line = file.readline()
                if not line or not "\n" in line:
                    sleep(0.1)
                    continue
                Thread(target=self.events["stdout"], args=(
                    line,)).start()

        Thread(target=_stdWatcher, args=()).start()

    def setRule(self, *rules: str):
        """

        Description
        ----------
        Change screen session's rules by command,
        see: https://www.gnu.org/software/screen/manual/.

        Parameters
        ----------
        *rules : STRING
            Rules to setup on screen session.

        """
        for rule in rules:
            os.popen(f"screen -r '{self.id}' -p0 -X {rule}")

    def write(self, *stdins: str):
        """

        Description
        ----------
        Write in screen session.

        Parameters
        ----------
        *stdins : STRING
            Text to write.

        """
        for stdin in stdins:
            os.popen(f"screen -S '{self.id}' -X stuff '{stdin}\n'")

    def logFile(self) -> str:
        """

        Description
        ----------
        Get screen session's logs.

        Returns
        ----------
        logFilePathText : STRING
            Screen session's logs.

        """
        return open(self.logFilePath, "r")

    def run(self, stdin: str = None):
        """

        Description
        ----------
        Create and run screen session with stdin,
        and save log if logFilePath was defined.

        Parameters
        ----------
        stdin : STRING <optional>
            Command to execute when running screen session.

        """
        if not self.exist():

            os.popen(f"screen -dmS '{self.id}'")
            if self.logFilePath:
                if not os.path.exists(self.logFilePath):
                    open(self.logFilePath, "a").close()
                self.setRule(f"logfile '{self.logFilePath}'",
                             "logfile flush 0", "log")
            if stdin:
                self.write(stdin)
        self.setup()

    def close(self):
        """

        Description
        ----------(?<=\£)(.*?)(?=\@)
        Remove screen session.

        """
        if self.exist():
            os.popen(f"screen -XS '{self.id}' quit")
            self.setup()
            if not self.pid:
                self.events["close"]()

    def kill(self, signal: int = 15):
        """

        Description
        ----------
        Default kill screen session's processing with his pid.

        Parameters
        ----------
        signal : INT <optional>
            signalnal code to apply on process.
            Default to 15 (kill).

        """
        os.kill(self.pid, signal)


def getAll() -> List[Screen]:
    """

    Description
    ----------
    Get all available Screen.

    Returns
    ----------
    screens : LIST [Screen]
        All Screen available.

    """
    screens = []
    for line in os.popen("screen -ls").readlines()[1:-1]:
        if "£" in line:
            [pid, id, saveLog, date, state] = re.findall(
                r"(?<=\t).*?(?=\.)|(?<=\@\&\$\£).*?(?=\@\&\$\£)|(?<=\().*?(?=\))", line)
            screen = Screen(id, saveLog)
            screen.pid = int(pid)
            screen.date = date
            screen.state = state
            screens.append(screen)
    return screens

import datetime
import threading

import flask
import my_pickledb
from .formating import default


class Logging:
    def __init__(self, location: str = "plsl.log"):
        """
        Creates a logging object containing Flask Class and PickleDB Class
        It modifies PickleDB save method to custom one

        It will start Flask Server automatically on daemon mode, so if program stops, it will stop after it

        :param location:
        """

        self.__location = location
        self.database = my_pickledb.PickleDB(location)
        [self.database.set(key, []) for key in ["info", "debug", "warning", "error"]]

    """
    All methods below works in the same way
    It will add a message to specified logging type:
        - info
        - debug
        - warning
        - error
        
    How to use datetime_format?
    Check datetime format codes here: https://www.w3schools.com/python/gloss_python_date_format_codes.asp
    
    How to use str_format?
    Parameters:
        0 -> message
        1 -> datetime
    Add as many args as you want, indexing is important, 0 and 1 are reserved to message and datetime
    You can also use kwargs as parameters, it uses .format()    
    """

    def save_log(self):
        with open(self.__location, "w") as f: [f.write(f"{type_.upper()} : {value} \n") for type_, values in self.database.json.items() for value in values]

    def info(self, message: str, *args, datetime_format: str = "%d-%b-%Y %H:%M:%S", str_format: str = default, **kwargs): self.database.append("info", str_format.format(message, datetime.datetime.now().strftime(datetime_format), *args, **kwargs)); self.save_log()

    def debug(self, message: str, *args, datetime_format: str = "%d-%b-%Y %H:%M:%S", str_format: str = default, **kwargs): self.database.append("debug", str_format.format(message, datetime.datetime.now().strftime(datetime_format), *args, **kwargs)); self.save_log()

    def warning(self, message: str, *args, datetime_format: str = "%d-%b-%Y %H:%M:%S", str_format: str = default, **kwargs): self.database.append("warning", str_format.format(message, datetime.datetime.now().strftime(datetime_format), *args, **kwargs)); self.save_log()

    def error(self, message: str, *args, datetime_format: str = "%d-%b-%Y %H:%M:%S", str_format: str = default, **kwargs): self.database.append("error", str_format.format(message, datetime.datetime.now().strftime(datetime_format), *args, **kwargs)); self.save_log()


class WebLogging(Logging):
    def __init__(self, location: str = "plsl.log", **kwargs):
        super().__init__(location)

        self.server = flask.Flask(__name__, **kwargs)

        @self.server.route("/")
        def logging( ): return flask.render_template("index.html", database=self.database.database.items())

        threading.Thread(target=self.server.run, args=("0.0.0.0", 9999,), daemon=True).start()

import logging
import logging.handlers
import os
import socket
import sys


def mb_namer(default_name: str) -> str:
    # change "mbServer.log.2020-12-39" to "mbServer-2020-12-39.log"
    names = default_name.split(".log.")
    if len(names) > 1:
        return "{}-{}.log".format(names[0], names[-1])
    else:
        return default_name


class Logger:
    def __init__(self, cfg):
        self.normal_log = None
        self.biz_log = None
        self.error_log = None
        self.json_log = None
        self.cfg = cfg

    def initialize(self, server_name='mbServer', debug=False, level=logging.DEBUG, root='admin'):
        formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(name)s - %(message)s")
        console_handler = logging.StreamHandler(stream=sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        host = socket.getfqdn(socket.gethostname())
        backup_count = self.cfg["aliyunSLS"].get("limitCount", "1")
        backup_count = int(backup_count)

        json_handler = logging.handlers.TimedRotatingFileHandler(
            self.mkdir('/{0}/logs/{1}/json4biz_{2}.log'.format(root, server_name, host)), 'D', 1, backup_count, 'UTF-8')
        json_handler.namer = mb_namer
        json_handler.setLevel(level)
        json_handler.setFormatter(formatter)

        log_handler = logging.handlers.TimedRotatingFileHandler(
            self.mkdir('/{0}/logs/{1}/{1}_{2}.log'.format(root, server_name, host)), 'D', 1, backup_count, 'UTF-8')
        log_handler.namer = mb_namer
        log_handler.setLevel(level)
        log_handler.setFormatter(formatter)

        error_handler = logging.handlers.TimedRotatingFileHandler(
            self.mkdir('/{0}/logs/{1}/error_{2}.log'.format(root, server_name, host)), 'M', 1, 3, 'UTF-8')
        error_handler.namer = mb_namer
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)

        biz_handler = logging.handlers.TimedRotatingFileHandler(
            self.mkdir('/{0}/logs/{1}/biz_{2}.log'.format(root, server_name, host)), 'D', 1, backup_count, 'UTF-8')
        biz_handler.namer = mb_namer
        biz_handler.setLevel(logging.INFO)
        biz_handler.setFormatter(formatter)

        self.json_log = logging.getLogger("[{}][JSON]".format(server_name))
        self.json_log.setLevel(logging.DEBUG)
        self.json_log.propagate = False
        self.json_log.addHandler(json_handler)

        self.normal_log = logging.getLogger("[{}][INFO]".format(server_name))
        self.normal_log.setLevel(logging.DEBUG)
        self.normal_log.propagate = False
        self.normal_log.addHandler(log_handler)

        self.error_log = logging.getLogger("[{}][ERROR]".format(server_name))
        self.error_log.setLevel(logging.ERROR)
        self.error_log.propagate = False
        self.error_log.addHandler(log_handler)
        self.error_log.addHandler(error_handler)

        self.biz_log = logging.getLogger("[{}][BIZ]".format(server_name))
        self.biz_log.setLevel(logging.INFO)
        self.biz_log.propagate = False
        self.biz_log.addHandler(biz_handler)

        if debug:
            self.normal_log.addHandler(console_handler)
            self.error_log.addHandler(console_handler)
            self.biz_log.addHandler(console_handler)

    def warning(self, *args):
        self.normal_log.warning(*self.strengthen(*args))

    def debug(self, *args):
        self.normal_log.debug(*self.strengthen(*args))

    def info(self, *args):
        self.normal_log.info(*self.strengthen(*args))

    def error(self, *args):
        self.error_log.error(*self.strengthen(*args))

    def fatal(self, *args):
        self.error_log.fatal(*self.strengthen(*args))

    def biz(self, *args):
        # api访问日志
        self.biz_log.info(*self.strengthen(*args))

    def exception(self, *args):
        self.error_log.exception(*args)

    def json(self, d: dict):
        """打印到json4biz里面"""
        self.json_log.info(d)

    @staticmethod
    def strengthen(*args):
        if isinstance(args[0], str) and args[0].find('%s') < 0:
            return (' '.join([str(arg) for arg in args]),)
        elif not isinstance(args[0], str):
            return (' '.join([str(arg) for arg in args]),)
        else:
            return args

    @staticmethod
    def mkdir(path):
        try:
            os.makedirs(os.path.dirname(path))
        except OSError:
            pass
        return path

    @staticmethod
    def format_equal(d: dict):
        """
        :param d: {"serviceId":1,"recordId":6}
        :return: [serviceId=1][recordId=6]
        """
        return "".join(["[{}={}]".format(key, value) for key, value in d.items()])

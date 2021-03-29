import logging
import sys

LOGGER_NAME = "SimpleAppLog"


class Logger(object):
    # __created_std_out = False
    log_file = bytes
    EXCEPTION = 100
    CRITICAL = 50
    ERROR = 40
    WARNING = 30
    INFO = 20
    DEBUG = 10
    NOTSET = 0

    def __init__(self):
        self.__log = logging.getLogger(LOGGER_NAME)
        # create formatter
        formatter = logging.Formatter("%(asctime)-15s [%(levelname)-8s] %(message)s")
        ch = logging.StreamHandler(sys.stderr)
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)
        self.__log.addHandler(ch)

        self.__log.setLevel(self.INFO)
        self.__methods_map = {
            self.DEBUG: self.__log.debug,
            self.INFO: self.__log.info,
            self.WARNING: self.__log.warning,
            self.ERROR: self.__log.error,
            self.CRITICAL: self.__log.critical,
            self.EXCEPTION: self.__log.exception,
        }

    def __call__(self, lvl, msg, *args, **kwargs):
        if lvl in self.__methods_map:
            self.__methods_map[lvl](msg, *args, **kwargs)
        else:
            self.__log.log(lvl, msg, *args, **kwargs)

    def set_level(self, level=None):
        if level is None:
            level = self.INFO
        self.__log.setLevel(level)


log = Logger()

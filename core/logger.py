import sys
import logging
import traceback

default_logger = logging.getLogger(__name__)


class Logger:
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        stream_handler = logging.StreamHandler(sys.stdout)
        log_formatter = logging.Formatter(
            "%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] - %(message)s"
        )
        stream_handler.setFormatter(log_formatter)
        self.logger.addHandler(stream_handler)

    def log(self, *args, log_level="debug"):
        data = self._arg_to_string(args)
        if log_level == self.INFO:
            default_logger.info(data)
        elif log_level == self.WARNING:
            default_logger.warning(data)
        elif log_level == self.ERROR:
            default_logger.error(data)
        else:
            default_logger.debug(data)

    def log_exc(self, exc):
        self.log("Error Exc ->> ", traceback.format_exc())

    def _arg_to_string(self, *args):
        arg_strs = []
        for arg in args:
            try:
                arg_strs.append(str(arg))
            except Exception:
                pass
        return ", ".join(arg_strs)


logger = Logger()

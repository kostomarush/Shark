import logging
import sys


class LogFilter(logging.Filter):
    """
    Simplify pathname
    """
    def filter(self, record):
        s_path = record.pathname.replace(sys.path[0], '').split('/')[1:-1]
        if s_path:
            record.pathname = f"{'.'.join([(x or ' ')[0] for x in s_path])}.{record.module}"[-20:]
        else:
            record.pathname = record.module
        return True


class Logger:

    def __init__(self):
        logger = logging.getLogger('console')
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        handler.addFilter(LogFilter())
        log_format = '%(asctime)s %(levelname)s %(process)d --- [%(threadName)+15s] %(pathname)-20s : %(message)s'
        formatter = logging.Formatter(log_format, datefmt='%Y-%m-%d %H:%M:%S.000')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        self.logger = logger


logs = Logger().logger

import logging
import queue

class GUILogHandler(logging.Handler):
    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        log_entry = self.format(record)
        self.log_queue.put(log_entry)

def setup_logger(log_queue=None):
    logger = logging.getLogger("CapCutAuto")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s', datefmt='%H:%M:%S')

    # Console handler
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # GUI handler if queue is provided
    if log_queue:
        gh = GUILogHandler(log_queue)
        gh.setFormatter(formatter)
        logger.addHandler(gh)

    return logger

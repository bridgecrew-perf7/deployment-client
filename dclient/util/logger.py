import logging


def get_logger():
    logger = logging.getLogger("dclient")
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler("/var/log/deployment/dclient.log")
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger

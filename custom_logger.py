#!/usr/bin/python3

import logging


def create_logger(name=None, logfile=None, level=logging.INFO, propagate=False):
    logger = logging.getLogger(name)
    formatter = logging.Formatter(
        fmt="[{asctime}] {levelname:<8} | {filename}:{lineno} -> {message}",
        datefmt="%Y-%m-%d %H:%M:%S",
        style="{",
    )
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    if logfile:
        file_handler = logging.FileHandler(logfile, mode="w", encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    logger.setLevel(level)
    logger.propagate = propagate
    return logger


logger = create_logger("xyz", logfile="xyz.log")

logger.info("bla")

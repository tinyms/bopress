# -*- coding: utf-8 -*-

import logging
import os
from logging.handlers import RotatingFileHandler

from tornado.log import enable_pretty_logging
from tornado.escape import json_encode

from BoPress import settings

C_LOG_SIZE = 1048576
C_LOG_NAME = os.path.join(settings.BASE_DIR, "BoPress.log")
C_LOG_FILES = 3

TAG = "BoPress"
__author__ = 'yezang'


class Logger(object):
    is_inited = False

    @staticmethod
    def init():
        if not settings.LOGGER_LEVEL:
            settings.LOGGER_LEVEL = logging.NOTSET
        rt = RotatingFileHandler(filename=C_LOG_NAME, maxBytes=C_LOG_SIZE, backupCount=C_LOG_FILES)
        rt.setLevel(settings.LOGGER_LEVEL)
        rt.setFormatter(logging.Formatter('[%(asctime)s] %(message)s'))
        log = logging.getLogger()
        enable_pretty_logging()
        log.addHandler(rt)
        Logger.is_inited = True

    @staticmethod
    def error(obj, tag=TAG):
        logging.error("[ERROR] %s: %s" % (tag, json_encode(obj)))

    @staticmethod
    def exception(e, tag=TAG):
        logging.error("[EXCEPTION] %s " % tag, exc_info=e)

    @staticmethod
    def info(obj, tag=TAG):
        logging.info("[INFO] %s: %s" % (tag, json_encode(obj)))

    @staticmethod
    def debug(obj, tag=TAG):
        logging.debug("[DEBUG] %s: %s" % (tag, json_encode(obj)))

    @staticmethod
    def warning(obj, tag=TAG):
        logging.warning("[WARNING] %s: %s" % (tag, json_encode(obj)))

    @staticmethod
    def critical(obj, tag=TAG):
        logging.critical("[CRITICAL] %s: %s" % (tag, json_encode(obj)))

    @staticmethod
    def nothing(e):
        pass

"""Container for the most basic platform layout"""

__author__ = "Felix Simkovic"
__date__ = "03 Jun 2017"
__version__ = "0.1"

import logging

logger = logging.getLogger(__name__)


class Platform(object):

    @staticmethod
    def alt(*args, **kwargs):
        logger.debug("Function unavailable for specified queue type")
        return None

    @staticmethod
    def hold(*args, **kwargs):
        logger.debug("Function unavailable for specified queue type")
        return None

    @staticmethod
    def kill(*args, **kwargs):
        logger.debug("Function unavailable for specified queue type")
        return None

    @staticmethod
    def rls(*args, **kwargs):
        logger.debug("Function unavailable for specified queue type")
        return None

    @staticmethod
    def sub(*args, **kwargs):
        logger.debug("Function unavailable for specified queue type")
        return None

    @staticmethod
    def stat(*args, **kwargs):
        logger.debug("Function unavailable for specified queue type")
        return None

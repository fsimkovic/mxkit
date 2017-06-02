"""Module to store a stopwatch class"""

from __future__ import print_function

__author__ = "Felix Simkovic"
__date__ = "02 Jun 2017"
__version__ = "1.0"

import datetime
import logging
import time

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)


class StopWatch(object):
    """This class provides simple stopwatch functionality.

    You can :func:`lap <StopWatch.lap>` times, i.e. see
    individual subroutines and measure their time.

    Examples
    --------
    >>> import time
    >>> from mbkit.misc.stopwatch import StopWatch
    >>> watch = StopWatch()
    >>> watch.start()
    >>> time.sleep(5)       # Some processing here
    >>> watch.stop()
    >>> StopWatch.convert(watch.runtime())
    (0, 0, 0, 5)

    """

    def __init__(self):
        """Instantiate a new :obj:`StopWatch`"""
        self.reset()

    @property
    def running(self):
        """Status"""
        return self._running

    @property
    def lap(self):
        """Lap time"""
        self._laps += [time.time() - self._start_time - sum(self._laps)]
        return int(round(self._laps[-1]))

    @property
    def runtime(self):
        """Total runtime in seconds"""
        if self._running:
            return int(round(time.time() - self._start_time))
        else:
            return int(round(self._stop_time - self._start_time))

    def reset(self):
        """Reset the timer"""
        self._locked = False
        self._running = False
        self._laps = []
        self._start_time = 0.0
        self._stop_time = 0.0

    def start(self):
        """Start the timer"""
        if self._running:
            logger.warning("Timer already running!")
        else:
            logger.info("Starting timer ...")
            self._start_time = time.time()
            self._locked = False
            self._running = True

    def stop(self):
        """Stop the timer"""
        if self._running:
            logger.info("Stopping timer ...")
            self._stop_time = time.time()
            self._locked = True
            self._running = False
        else:
            logger.warning("Timer not running!")

    @staticmethod
    def convert(runtime):
        """Convert (seconds) to (days, hours, minutes, seconds)"""
        d = datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=runtime)
        # Leave -1 in day as we start on the first day of the year
        return d.day - 1, d.hour, d.minute, d.second

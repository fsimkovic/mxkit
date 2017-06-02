"""Testing facility for mbkit.misc.stopwatch"""

__author__ = "Felix Simkovic"
__date__ = "02 Jun 2017"

import time
import unittest

from mbkit.misc.stopwatch import StopWatch


class TestTimer(unittest.TestCase):

    def test_start_1(self):
        t = StopWatch()
        t.start()
        self.assertTrue(t.running)
        self.assertGreater(t._start_time, 0.0)

    def test_stop_1(self):
        t = StopWatch()
        t.start()
        self.assertTrue(t.running)
        t.stop()
        self.assertFalse(t.running)
        self.assertGreater(t._start_time, 0.0)

    def test_stop_2(self):
        t = StopWatch()
        t.start()
        t.stop()
        self.assertTrue(t._locked)

    def test_reset_1(self):
        t = StopWatch()
        t.start()
        time.sleep(2)
        t.stop()
        self.assertAlmostEqual(t.runtime, 2)
        t.reset()
        self.assertAlmostEqual(t.runtime, 0)

    def test_lap_1(self):
        t = StopWatch()
        t.start()
        time.sleep(2)
        self.assertAlmostEqual(t.lap, 2)

    def test_lap_2(self):
        t = StopWatch()
        t.start()
        time.sleep(2)
        self.assertAlmostEqual(t.lap, 2)
        time.sleep(1)
        self.assertAlmostEqual(t.lap, 1)

    def test_lap_3(self):
        t = StopWatch()
        t.start()
        time.sleep(2)
        self.assertAlmostEqual(t.lap, 2)
        time.sleep(1)
        self.assertAlmostEqual(t.lap, 1)
        time.sleep(1)
        self.assertAlmostEqual(t.lap, 1)

    def test_runtime_1(self):
        t = StopWatch()
        t.start()
        time.sleep(2)
        t.stop()
        self.assertAlmostEqual(t.runtime, 2)

    def test_runtime_2(self):
        t = StopWatch()
        t.start()
        time.sleep(2)
        self.assertAlmostEqual(t.runtime, 2)

    def test_runtime_3(self):
        t = StopWatch()
        t.start()
        time.sleep(2)
        self.assertAlmostEqual(t.runtime, 2)
        time.sleep(2)
        self.assertAlmostEqual(t.runtime, 4)

    def test_runtime_4(self):
        t = StopWatch()
        t.start()
        time.sleep(2)
        self.assertAlmostEqual(t.runtime, 2)
        time.sleep(1)
        self.assertAlmostEqual(t.runtime, 3)
        time.sleep(1)
        self.assertAlmostEqual(t.runtime, 4)

    def test_convert_1(self):
        self.assertEqual((0, 0, 1, 40), StopWatch.convert(100))

    def test_convert_2(self):
        self.assertEqual((5, 3, 7, 21), StopWatch.convert(443241))


if __name__ == "__main__":
    unittest.main(verbosity=2)

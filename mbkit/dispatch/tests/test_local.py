"""Testing facility for mbkit.dispatch.local"""

__author__ = "Felix Simkovic"
__date__ = "10 May 2017"

import os
import time
import unittest

import mbkit.apps
import mbkit.dispatch.cexectools
import mbkit.dispatch.local
import mbkit.util


class TestLocalJobServer(unittest.TestCase):

    def test_jsub_1(self):
        j = mbkit.apps.make_python_script([
            ["import sys, time"], 
            ["print(\"I am job: 1\")"],
            ["sys.exit(0)"],
        ], prefix="unittest")
        l = j.rsplit('.', 1)[0] + '.log'
        mbkit.dispatch.local.LocalJobServer.jsub([j], nproc=1)
        time.sleep(0.5)
        self.assertTrue(os.path.isfile(l))
        for f in [j, l]: os.unlink(f)

    def test_jsub_2(self):
        jobs = [
            mbkit.apps.make_python_script([
                ["import sys, time"], 
                ["print(\"I am job: {0}\")".format(i)],
                ["sys.exit(0)"],
            ], prefix="unittest") for i in range(6)
        ]
        logs = [j.rsplit('.', 1)[0] + '.log' for j in jobs]
        mbkit.dispatch.local.LocalJobServer.jsub(jobs, nproc=2)
        time.sleep(0.5)
        self.assertTrue(os.path.isfile(logs[-1]))
        for f in jobs + logs: os.unlink(f)
     

if __name__ == "__main__":
    unittest.main(verbosity=2)


"""Testing facility for mbkit.dispatch.local"""

__author__ = "Felix Simkovic"
__date__ = "10 May 2017"

import os
import unittest

import mbkit.apps
import mbkit.dispatch.cexectools
import mbkit.dispatch.local
import mbkit.util


class TestLocalJobServer(unittest.TestCase):

    def test_sub_1(self):
        j = mbkit.apps.make_python_script([
            ["import sys, time"], 
            ["print(\"I am job: 1\")"], 
            ["time.sleep(3)"], 
            ["sys.exit(0)"],
        ], prefix="unittest")
        l = j.rsplit('.', 1)[0] + '.log'
        mbkit.dispatch.local.LocalJobServer.sub([j], nproc=1)
        self.assertTrue(os.path.isfile(l))
        for f in [j, l]: os.unlink(f)

    def test_sub_2(self):
        jobs = [
            mbkit.apps.make_python_script([
                ["import sys, time"], 
                ["print(\"I am job: {0}\")".format(i)], 
                ["time.sleep(3)"], 
                ["sys.exit(0)"],
            ], prefix="unittest") for i in range(6)
        ]
        logs = [j.rsplit('.', 1)[0] + '.log' for j in jobs]
        mbkit.dispatch.local.LocalJobServer.sub(jobs, nproc=2)
        self.assertTrue(os.path.isfile(logs[-1]))
        for f in jobs + logs: os.unlink(f)
     
    def test_sub_3(self):
        def _checker(log):
            with open(log, 'r') as f_in:
                lines = f_in.readlines()
            return any("the special one" in l for l in lines)

        jobs = [
            mbkit.apps.make_python_script([
                ["import sys, time"], 
                ["print(\"I am job: {0}\")".format(i)], 
                ["time.sleep(3)"], 
                ["sys.exit(0)"],
            ], prefix="unittest") for i in range(6)
        ]
        os.unlink(jobs[3])
        # Special one to terminate early
        jobs[3] = mbkit.apps.make_python_script([
            ["import sys, time"],
            ["print(\"I am job: 3 - the special one\")"],
            ["time.sleep(3)"],
            ["sys.exit(0)"]
        ], prefix="unittest")
        logs = [j.rsplit('.', 1)[0] + '.log' for j in jobs]
        mbkit.dispatch.local.LocalJobServer.sub(jobs, nproc=2, check_success=_checker)
        self.assertTrue(os.path.isfile(logs[0]))
        self.assertTrue(os.path.isfile(logs[1]))
        self.assertTrue(os.path.isfile(logs[2]))
        self.assertTrue(os.path.isfile(logs[3]))
        # Testing for 4th file is unreliable on 2 cores
        self.assertFalse(os.path.isfile(logs[5]))
        for f in jobs + logs: 
            if os.path.isfile(f): 
                os.unlink(f)
     

if __name__ == "__main__":
        unittest.main(verbosity=2)


"""Testing facility for mbkit.dispatch.sge"""

__author__ = "Felix Simkovic"
__date__ = "10 May 2017"

import glob
import inspect
import os
import sys
import time

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

from mbkit.apps import make_script
from mbkit.dispatch.sge import SunGridEngine


@unittest.skipUnless("SGE_ROOT" in os.environ, "not on SunGridEngine platform")
class TestSunGridEngine(unittest.TestCase):

    def test_alt_1(self):
        jobs = [make_script(["sleep 100"])]
        jobid = SunGridEngine.sub(jobs, hold=True, name=inspect.stack()[0][3])
        time.sleep(5)
        SunGridEngine.alt(jobid, priority=-1)
        data = SunGridEngine.stat(jobid)
        self.assertTrue(data)
        self.assertEqual(jobid, int(data['job_number']))
        self.assertEqual(-1, int(data['priority']))
        SunGridEngine.kill(jobid)
        map(os.unlink, jobs)

    def test_kill_1(self):
        jobs = [make_script(["sleep 100"])]
        jobid = SunGridEngine.sub(jobs, hold=True, name=inspect.stack()[0][3])
        time.sleep(5)
        self.assertTrue(SunGridEngine.stat(jobid))
        SunGridEngine.kill(jobid)
        map(os.unlink, jobs)
 
    def test_kill_2(self):
        jobs = [make_script(["sleep 100"]) for _ in range(5)]
        jobid = SunGridEngine.sub(jobs, hold=True, name=inspect.stack()[0][3])
        time.sleep(5)
        self.assertTrue(SunGridEngine.stat(jobid))
        SunGridEngine.kill(jobid)
        map(os.unlink, jobs)
        map(os.unlink, glob.glob(u'*.jobs'))
        map(os.unlink, glob.glob(u'*.script'))

    def test_hold_1(self):
        jobs = [make_script(["sleep 100"])]
        jobid = SunGridEngine.sub(jobs, hold=False, name=inspect.stack()[0][3], log=os.devnull)
        time.sleep(5)
        SunGridEngine.hold(jobid)
        SunGridEngine.kill(jobid)
        map(os.unlink, jobs)

    def test_rls_1(self):
        jobs = [make_script(["touch", "mbkit_rls_test_1"])]
        jobid = SunGridEngine.sub(jobs, hold=True, name=inspect.stack()[0][3], log=os.devnull)
        time.sleep(5)
        SunGridEngine.rls(jobid)
        start, timeout = time.time(), False
        while SunGridEngine.stat(jobid):
            # Don't wait too long, one minute, then fail
            if ((time.time() - start) // 60) >= 1:
                SunGridEngine.kill(jobid)
                timeout = True
            time.sleep(10)
        if timeout:
            map(os.unlink, jobs)
            self.assertEqual(1, 0, "Timeout")
        else:
            self.assertTrue(os.path.isfile('mbkit_rls_test_1'))
            os.unlink('mbkit_rls_test_1')
        map(os.unlink, jobs)

    def test_stat_1(self):
        jobs = [make_script(["sleep 100"])]
        jobid = SunGridEngine.sub(jobs, hold=True, name=inspect.stack()[0][3])
        time.sleep(5)
        data = SunGridEngine.stat(jobid)
        self.assertTrue(data)
        self.assertEqual(jobid, int(data['job_number']))
        self.assertTrue('sge_o_shell' in data)
        self.assertTrue('sge_o_workdir' in data)
        self.assertTrue('sge_o_host' in data)
        SunGridEngine.kill(jobid)
        map(os.unlink, jobs)

    def test_stat_2(self):
        jobs = [make_script(["sleep 100"]) for _ in range(5)]
        jobid = SunGridEngine.sub(jobs, hold=True, name=inspect.stack()[0][3])
        time.sleep(5)
        data = SunGridEngine.stat(jobid)
        SunGridEngine.kill(jobid)
        self.assertTrue(data)
        self.assertEqual(jobid, int(data['job_number']))
        self.assertTrue('sge_o_shell' in data)
        self.assertTrue('sge_o_workdir' in data)
        self.assertTrue('sge_o_host' in data)
        self.assertTrue('job-array tasks' in data)
        self.assertEqual("1-5:1", data['job-array tasks'].strip())
        map(os.unlink, jobs)
        map(os.unlink, glob.glob(u'*.jobs'))
        map(os.unlink, glob.glob(u'*.script'))

    def test_sub_1(self):
        jobs = [make_script(["sleep 1"])]
        jobid = SunGridEngine.sub(jobs, hold=True, name=inspect.stack()[0][3])
        time.sleep(5)
        self.assertTrue(SunGridEngine.stat(jobid))
        SunGridEngine.kill(jobid)
        map(os.unlink, jobs)

    def test_sub_2(self):
        jobs = [make_script(["sleep 1"]) for _ in range(5)]
        jobid = SunGridEngine.sub(jobs, hold=True, name=inspect.stack()[0][3])
        time.sleep(5)
        self.assertTrue(SunGridEngine.stat(jobid))
        SunGridEngine.kill(jobid)
        map(os.unlink, jobs)
        map(os.unlink, glob.glob(u'*.jobs'))
        map(os.unlink, glob.glob(u'*.script'))
    
    def test_sub_3(self):
        directory = os.getcwd()
        jobs = [make_script([["sleep 5"], ['echo "file {0}"'.format(i)]], directory=directory) 
                for i in range(5)]
        jobid = SunGridEngine.sub(jobs, name=inspect.stack()[0][3])
        start, timeout = time.time(), False
        while SunGridEngine.stat(jobid):
            # Don't wait too long, one minute, then fail
            if ((time.time() - start) // 60) >= 1:
                SunGridEngine.kill(jobid)
                timeout = True
            time.sleep(10)
        if timeout:
            map(os.unlink, jobs)
            map(os.unlink, glob.glob(u'*.jobs'))
            map(os.unlink, glob.glob(u'*.script'))
            self.assertEqual(1, 0, "Timeout")
        else:
            for i, j in enumerate(jobs):
                f = j.replace(".sh", ".log")
                self.assertTrue(os.path.isfile(f))
                content = open(f).read().strip()
                self.assertEqual("file {0}".format(i), content)
                os.unlink(f)
        map(os.unlink, jobs)
        map(os.unlink, glob.glob(u'*.jobs'))
        map(os.unlink, glob.glob(u'*.script'))

    def test_sub_4(self):
        directory = os.getcwd()
        jobs = [make_script(['echo "file {0}"'.format(i)], directory=directory) 
                for i in range(100)]
        jobid = SunGridEngine.sub(jobs, name=inspect.stack()[0][3])
        start, timeout = time.time(), False
        while SunGridEngine.stat(jobid):
            # Don't wait too long, one minute, then fail
            if ((time.time() - start) // 60) >= 1:
                SunGridEngine.kill(jobid)
                timeout = True
            time.sleep(10)
        if timeout:
            map(os.unlink, jobs)
            map(os.unlink, glob.glob(u'*.jobs'))
            map(os.unlink, glob.glob(u'*.script'))
            self.assertEqual(1, 0, "Timeout")
        else:
            for i, j in enumerate(jobs):
                f = j.replace(".sh", ".log")
                self.assertTrue(os.path.isfile(f))
                content = open(f).read().strip()
                self.assertEqual("file {0}".format(i), content)
                os.unlink(f)
        map(os.unlink, jobs)
        map(os.unlink, glob.glob(u'*.jobs'))
        map(os.unlink, glob.glob(u'*.script'))

    def test_sub_5(self):
        jobs = [make_script(["echo $SGE_ROOT"], directory=os.getcwd()) for _ in range(2)]
        jobid = SunGridEngine.sub(jobs, name=inspect.stack()[0][3])
        start, timeout = time.time(), False
        while SunGridEngine.stat(jobid):
            # Don't wait too long, one minute, then fail
            if ((time.time() - start) // 60) >= 1:
                SunGridEngine.kill(jobid)
                timeout = True
            time.sleep(10)
        if timeout:
            map(os.unlink, jobs)
            map(os.unlink, glob.glob(u'*.jobs'))
            map(os.unlink, glob.glob(u'*.script'))
            self.assertEqual(1, 0, "Timeout")
        else:
            for i, j in enumerate(jobs):
                f = j.replace(".sh", ".log")
                self.assertTrue(os.path.isfile(f))
                content = open(f).read().strip()
                self.assertEqual(os.environ["SGE_ROOT"], content)
                os.unlink(f)
        map(os.unlink, jobs)
        map(os.unlink, glob.glob(u'*.jobs'))
        map(os.unlink, glob.glob(u'*.script'))



if __name__ == "__main__":
    unittest.main(verbosity=2)


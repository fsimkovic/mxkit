"""Testing facility for mbkit.dispatch.lsf"""

__author__ = "Felix Simkovic"
__date__ = "30 May 2017"

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
from mbkit.dispatch.lsf import LoadSharingFacility


@unittest.skipUnless("LSF_BINDIR" in os.environ, "not on LoadSharingFacility platform")
class TestLoadSharingFacility(unittest.TestCase):

    def test_bjobs_1(self):
        jobs = [make_script(["sleep 100"])]
        jobid = LoadSharingFacility.bsub(jobs, hold=True, name=inspect.stack()[0][3])
        time.sleep(5)
        data = LoadSharingFacility.bjobs(jobid)
        self.assertTrue(data)
        self.assertEqual(jobid, int(data['job_number']))
        LoadSharingFacility.bkill(jobid)
        map(os.unlink, jobs)

    def test_bjobs_2(self):
        jobs = [make_script(["sleep 100"]) for _ in range(5)]
        jobid = LoadSharingFacility.bsub(jobs, hold=True, name=inspect.stack()[0][3])
        time.sleep(5)
        data = LoadSharingFacility.bjobs(jobid)
        LoadSharingFacility.bkill(jobid)
        self.assertTrue(data)
        self.assertEqual(jobid, int(data['job_number']))
        map(os.unlink, jobs)
        map(os.unlink, glob.glob(u'*.jobs'))
        map(os.unlink, glob.glob(u'*.script'))

    def test_bkill_1(self):
        jobs = [make_script(["sleep 100"])]
        jobid = LoadSharingFacility.bsub(jobs, hold=True, name=inspect.stack()[0][3])
        time.sleep(5)
        self.assertTrue(LoadSharingFacility.bjobs(jobid))
        LoadSharingFacility.bkill(jobid)
        map(os.unlink, jobs)

    def test_bkill_2(self):
        jobs = [make_script(["sleep 100"]) for _ in range(5)]
        jobid = LoadSharingFacility.bsub(jobs, hold=True, name=inspect.stack()[0][3])
        time.sleep(5)
        self.assertTrue(LoadSharingFacility.bjobs(jobid))
        LoadSharingFacility.bkill(jobid)
        map(os.unlink, jobs)
        map(os.unlink, glob.glob(u'*.jobs'))
        map(os.unlink, glob.glob(u'*.script'))

    def test_bresume_1(self):
        jobs = [make_script(["touch", "mbkit_bresume_test_1"])]
        jobid = LoadSharingFacility.bsub(jobs, hold=True, name=inspect.stack()[0][3])
        time.sleep(5)
        LoadSharingFacility.bresume(jobid)
        start, timeout = time.time(), False
        while LoadSharingFacility.bjobs(jobid):
            # Don't wait too long, one minute, then fail
            if ((time.time() - start) // 60) >= 1:
                LoadSharingFacility.bkill(jobid)
                timeout = True
            time.sleep(10)
        if timeout:
            map(os.unlink, jobs)
            self.assertEqual(1, 0, "Timeout")
        else:
            self.assertTrue(os.path.isfile('mbkit_bresume_test_1'))
            os.unlink('mbkit_bresume_test_1')
        map(os.unlink, jobs)

    def test_bstop_1(self):
        jobs = [make_script(["sleep 100"])]
        jobid = LoadSharingFacility.bsub(jobs, hold=False, name=inspect.stack()[0][3])
        time.sleep(5)
        LoadSharingFacility.bstop(jobid)
        LoadSharingFacility.bkill(jobid)
        map(os.unlink, jobs)

    def test_bsub_1(self):
        jobs = [make_script(["sleep 1"])]
        jobid = LoadSharingFacility.bsub(jobs, hold=True, name=inspect.stack()[0][3])
        time.sleep(5)
        self.assertTrue(LoadSharingFacility.bjobs(jobid))
        LoadSharingFacility.bkill(jobid)
        map(os.unlink, jobs)

    def test_bsub_2(self):
        jobs = [make_script(["sleep 1"]) for _ in range(5)]
        jobid = LoadSharingFacility.bsub(jobs, hold=True, name=inspect.stack()[0][3])
        time.sleep(5)
        self.assertTrue(LoadSharingFacility.bjobs(jobid))
        LoadSharingFacility.bkill(jobid)
        map(os.unlink, jobs)
        map(os.unlink, glob.glob(u'*.jobs'))
        map(os.unlink, glob.glob(u'*.script'))

    def test_bsub_3(self):
        directory = os.getcwd()
        jobs = [make_script([["sleep 5"], ['echo "file {0}"'.format(i)]], directory=directory)
                for i in range(5)]
        jobid = LoadSharingFacility.bsub(jobs, name=inspect.stack()[0][3])
        start, timeout = time.time(), False
        while LoadSharingFacility.bjobs(jobid):
            # Don't wait too long, one minute, then fail
            if ((time.time() - start) // 60) >= 1:
                LoadSharingFacility.bkill(jobid)
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

    def test_bsub_4(self):
        directory = os.getcwd()
        jobs = [make_script(['echo "file {0}"'.format(i)], directory=directory)
                for i in range(100)]
        jobid = LoadSharingFacility.bsub(jobs, name=inspect.stack()[0][3])
        start, timeout = time.time(), False
        while LoadSharingFacility.bjobs(jobid):
            # Don't wait too long, one minute, then fail
            if ((time.time() - start) // 60) >= 1:
                LoadSharingFacility.bkill(jobid)
                timeout = True
            time.sleep(10)
        time.sleep(20)
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

    def test_bsub_5(self):
        jobs = [make_script(["echo $LSF_BINDIR"], directory=os.getcwd()) for _ in range(2)]
        jobid = LoadSharingFacility.bsub(jobs, name=inspect.stack()[0][3])
        start, timeout = time.time(), False
        while LoadSharingFacility.bjobs(jobid):
            # Don't wait too long, one minute, then fail
            if ((time.time() - start) // 60) >= 1:
                LoadSharingFacility.bkill(jobid)
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
                self.assertEqual(os.environ["LSF_BINDIR"], content)
                os.unlink(f)
        map(os.unlink, jobs)
        map(os.unlink, glob.glob(u'*.jobs'))
        map(os.unlink, glob.glob(u'*.script'))


if __name__ == "__main__":
    unittest.main(verbosity=2)

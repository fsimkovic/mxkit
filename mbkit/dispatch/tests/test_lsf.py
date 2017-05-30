"""Testing facility for mbkit.dispatch.lsf"""

__author__ = "Felix Simkovic"
__date__ = "30 May 2017"

import glob
import inspect
import os
import time
import unittest

from mbkit.apps import make_script
from mbkit.dispatch.cexectools import cexec
from mbkit.dispatch.lsf import LoadSharingFacility


def on_cluster(cmd):
    """Little wrapper function to test whether we are on a specified cluster

    Parameters
    ----------
    cmd : list
       A command (with options) to run. This should normally be something
       simple, such as ``bjobs`` on the LoadSharingFacility platform

    Returns
    -------
    bool
       A boolean to indicate if we are on that particular cluster

    """
    try:
        cexec(cmd)
    # Command/file not found
    except OSError:
        return False
    # Non-zero return code
    except RuntimeError:
        return False
    return True


@unittest.skipUnless(on_cluster(["bjobs"]), "not on LoadSharingFacility platform")
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

    def test_bmod_1(self):
        jobs = [make_script(["sleep 100"])]
        jobid = LoadSharingFacility.bsub(jobs, hold=True, name=inspect.stack()[0][3])
        time.sleep(5)
        LoadSharingFacility.bmod(jobid, priority=-1)
        data = LoadSharingFacility.bjobs(jobid)
        self.assertTrue(data)
        self.assertEqual(jobid, int(data['job_number']))
        self.assertEqual(-1, int(data['priority']))
        LoadSharingFacility.bkill(jobid)
        map(os.unlink, jobs)

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
        jobs = [make_script(["sleep 5"], directory=directory) for _ in range(5)]
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
            for j in jobs:
                l = os.path.isfile(j.replace(".sh", ".log"))
                self.assertTrue(l)
                os.unlink(l)
        map(os.unlink, jobs)
        map(os.unlink, glob.glob(u'*.jobs'))
        map(os.unlink, glob.glob(u'*.script'))


if __name__ == "__main__":
    unittest.main(verbosity=2)


"""Testing facility for mbkit.dispatch.sge"""

__author__ = "Felix Simkovic"
__date__ = "10 May 2017"

import glob
import inspect
import os
import time
import unittest

from mbkit.apps import make_script
from mbkit.dispatch.cexectools import cexec
from mbkit.dispatch.sge import SunGridEngine


def on_cluster(cmd):
    """Little wrapper function to test whether we are on a specified cluster

    Parameters
    ----------
    cmd : list
       A command (with options) to run. This should normally be something
       simple, such as ``qstat`` on the SunGridEngine platform

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


@unittest.skipUnless(on_cluster(["qstat"]), "not on SunGridEngine platform")
class TestSunGridEngine(unittest.TestCase):

    def test_qalter_1(self):
        jobs = [make_script(["sleep 100"])]
        jobid = SunGridEngine.qsub(jobs, hold=True, name=inspect.stack()[0][3])
        time.sleep(5)
        SunGridEngine.qalter(jobid, priority=-1)
        data = SunGridEngine.qstat(jobid)
        self.assertTrue(data)
        self.assertEqual(jobid, int(data['job_number']))
        self.assertEqual(-1, int(data['priority']))
        SunGridEngine.qdel(jobid)
        map(os.unlink, jobs)

    def test_qdel_1(self):
        jobs = [make_script(["sleep 100"])]
        jobid = SunGridEngine.qsub(jobs, hold=True, name=inspect.stack()[0][3]) 
        time.sleep(5)
        self.assertTrue(SunGridEngine.qstat(jobid))
        SunGridEngine.qdel(jobid)
        map(os.unlink, jobs)
 
    def test_qdel_2(self):
        jobs = [make_script(["sleep 100"]) for _ in range(5)]
        jobid = SunGridEngine.qsub(jobs, hold=True, name=inspect.stack()[0][3])
        time.sleep(5)
        self.assertTrue(SunGridEngine.qstat(jobid))
        SunGridEngine.qdel(jobid)
        map(os.unlink, jobs)
        map(os.unlink, glob.glob(u'*.jobs'))
        map(os.unlink, glob.glob(u'*.script'))

    def test_qhold_1(self):
        jobs = [make_script(["sleep 100"])]
        jobid = SunGridEngine.qsub(jobs, hold=False, name=inspect.stack()[0][3])
        time.sleep(5)
        SunGridEngine.qhold(jobid)
        SunGridEngine.qdel(jobid)
        map(os.unlink, jobs)

    def test_qrls_1(self):
        jobs = [make_script(["touch", "mbkit_qrls_test_1"])]
        jobid = SunGridEngine.qsub(jobs, hold=True, name=inspect.stack()[0][3])
        time.sleep(5)
        SunGridEngine.qrls(jobid)
        start, timeout = time.time(), False
        while SunGridEngine.qstat(jobid):
            # Don't wait too long, one minute, then fail
            if ((time.time() - start) // 60) >= 1:
                SunGridEngine.qdel(jobid)
                timeout = True
            time.sleep(10)
        if timeout:
            map(os.unlink, jobs)
            self.assertEqual(1, 0, "Timeout")
        else:
            self.assertTrue(os.path.isfile('mbkit_qrls_test_1'))
            os.unlink('mbkit_qrls_test_1')
        map(os.unlink, jobs)

    def test_qstat_1(self):
        jobs = [make_script(["sleep 100"])]
        jobid = SunGridEngine.qsub(jobs, hold=True, name=inspect.stack()[0][3])
        time.sleep(5)
        data = SunGridEngine.qstat(jobid)
        self.assertTrue(data)
        self.assertEqual(jobid, int(data['job_number']))
        self.assertTrue('sge_o_shell' in data)
        self.assertTrue('sge_o_workdir' in data)
        self.assertTrue('sge_o_host' in data)
        SunGridEngine.qdel(jobid)
        map(os.unlink, jobs)

    def test_qstat_2(self):
        jobs = [make_script(["sleep 100"]) for _ in range(5)]
        jobid = SunGridEngine.qsub(jobs, hold=True, name=inspect.stack()[0][3])
        time.sleep(5)
        data = SunGridEngine.qstat(jobid)
        SunGridEngine.qdel(jobid)
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

    def test_qsub_1(self):
        jobs = [make_script(["sleep 1"])]
        jobid = SunGridEngine.qsub(jobs, hold=True, name=inspect.stack()[0][3])
        time.sleep(5)
        self.assertTrue(SunGridEngine.qstat(jobid))
        SunGridEngine.qdel(jobid)
        map(os.unlink, jobs)

    def test_qsub_2(self):
        jobs = [make_script(["sleep 1"]) for _ in range(5)]
        jobid = SunGridEngine.qsub(jobs, hold=True, name=inspect.stack()[0][3])
        time.sleep(5)
        self.assertTrue(SunGridEngine.qstat(jobid))
        SunGridEngine.qdel(jobid)
        map(os.unlink, jobs)
        map(os.unlink, glob.glob(u'*.jobs'))
        map(os.unlink, glob.glob(u'*.script'))
    
    def test_qsub_3(self):
        directory = os.getcwd()
        jobs = [make_script(["sleep 5"], directory=directory) for _ in range(5)]
        jobid = SunGridEngine.qsub(jobs, name=inspect.stack()[0][3])
        start, timeout = time.time(), False
        while SunGridEngine.qstat(jobid):
            # Don't wait too long, one minute, then fail
            if ((time.time() - start) // 60) >= 1:
                SunGridEngine.qdel(jobid)
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


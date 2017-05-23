"""Testing facility for mbkit.dispatch.cluster"""

__author__ = "Felix Simkovic"
__date__ = "10 May 2017"

import inspect
import os
import time
import unittest

import mbkit.apps
import mbkit.dispatch.cexectools
import mbkit.dispatch.cluster
import mbkit.util


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
        mbkit.dispatch.cexectools.cexec(cmd)
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
        f = mbkit.apps.make_script(["sleep 100"])
        jobid = mbkit.dispatch.cluster.SunGridEngine.qsub([f], hold=True, name=inspect.stack()[0][3])
        time.sleep(5)
        mbkit.dispatch.cluster.SunGridEngine.qalter(jobid, priority=-1)
        data = mbkit.dispatch.cluster.SunGridEngine.qstat(jobid)
        self.assertTrue(data)
        self.assertEqual(jobid, int(data['job_number']))
        self.assertEqual(-1, int(data['priority']))
        mbkit.dispatch.cluster.SunGridEngine.qdel(jobid)
        os.unlink(f)

    def test_qdel_1(self):
        f = mbkit.apps.make_script(["sleep 100"])
        jobid = mbkit.dispatch.cluster.SunGridEngine.qsub([f], hold=True, name=inspect.stack()[0][3]) 
        time.sleep(5)
        self.assertTrue(mbkit.dispatch.cluster.SunGridEngine.qstat(jobid))
        mbkit.dispatch.cluster.SunGridEngine.qdel(jobid)
        os.unlink(f)
 
    def test_qdel_2(self):
        jobs = [mbkit.apps.make_script(["sleep 100"]) for _ in range(5)]
        g = mbkit.util.tmp_fname(prefix='array_jobs')
        with open(g, 'w') as f_out: 
            f_out.write(os.linesep.join(jobs))
        h = mbkit.apps.make_script(["script=`sed -n \"${{SGE_TASK_ID}}p\" {0}`".format(g), "$script"])
        jobid = mbkit.dispatch.cluster.SunGridEngine.qsub([h], array=(1, 5, 5), hold=True, name=inspect.stack()[0][3])
        time.sleep(5)
        self.assertTrue(mbkit.dispatch.cluster.SunGridEngine.qstat(jobid))
        mbkit.dispatch.cluster.SunGridEngine.qdel(jobid)
        for f in jobs + [g, h]: os.unlink(f)

    def test_qhold_1(self):
        f = mbkit.apps.make_script(["sleep 100"])
        jobid = mbkit.dispatch.cluster.SunGridEngine.qsub([f], hold=False, name=inspect.stack()[0][3])
        time.sleep(5)
        mbkit.dispatch.cluster.SunGridEngine.qhold(jobid)
        mbkit.dispatch.cluster.SunGridEngine.qdel(jobid)
        os.unlink(f)

    def test_qrls_1(self):
        f = mbkit.apps.make_script(["touch mbkit_qrls_test_1"])
        jobid = mbkit.dispatch.cluster.SunGridEngine.qsub([f], hold=True, name=inspect.stack()[0][3])
        time.sleep(5)
        mbkit.dispatch.cluster.SunGridEngine.qrls(jobid)
        while mbkit.dispatch.cluster.SunGridEngine.qstat(jobid):
            time.sleep(2)
        self.assertTrue(os.path.isfile('mbkit_qrls_test_1'))
        os.unlink(f)

    def test_qstat_1(self):
        f = mbkit.apps.make_script(["sleep 100"])
        jobid = mbkit.dispatch.cluster.SunGridEngine.qsub([f], hold=True, name=inspect.stack()[0][3])
        time.sleep(5)
        data = mbkit.dispatch.cluster.SunGridEngine.qstat(jobid)
        self.assertTrue(data)
        self.assertEqual(jobid, int(data['job_number']))
        self.assertTrue('sge_o_shell' in data)
        self.assertTrue('sge_o_workdir' in data)
        self.assertTrue('sge_o_host' in data)
        mbkit.dispatch.cluster.SunGridEngine.qdel(jobid)
        os.unlink(f)

    def test_qstat_2(self):
        jobs = [mbkit.apps.make_script(["sleep 100"]) for _ in range(5)]
        g = mbkit.util.tmp_fname(prefix='array_jobs')
        with open(g, 'w') as f_out:
            f_out.write(os.linesep.join(jobs))
        h = mbkit.apps.make_script(["script=`sed -n \"${{SGE_TASK_ID}}p\" {0}`".format(g), "$script"])
        jobid = mbkit.dispatch.cluster.SunGridEngine.qsub([h], array=(1, 5, 5), hold=True, name=inspect.stack()[0][3])
        time.sleep(5)
        data = mbkit.dispatch.cluster.SunGridEngine.qstat(jobid)
        mbkit.dispatch.cluster.SunGridEngine.qdel(jobid)
        self.assertTrue(data)
        self.assertEqual(jobid, int(data['job_number']))
        self.assertTrue('sge_o_shell' in data)
        self.assertTrue('sge_o_workdir' in data)
        self.assertTrue('sge_o_host' in data)
        self.assertTrue('job-array tasks' in data)
        self.assertEqual("1-5:1", data['job-array tasks'].strip())
        for f in jobs + [g, h]: os.unlink(f)

    def test_qsub_1(self):
        f = mbkit.apps.make_script(["sleep 1"])
        jobid = mbkit.dispatch.cluster.SunGridEngine.qsub([f], hold=True, name=inspect.stack()[0][3])
        time.sleep(5)
        self.assertTrue(mbkit.dispatch.cluster.SunGridEngine.qstat(jobid))
        mbkit.dispatch.cluster.SunGridEngine.qdel(jobid)
        os.unlink(f)

    def test_qsub_2(self):
        jobs = [mbkit.apps.make_script(["sleep 1"]) for _ in range(5)]
        g = mbkit.util.tmp_fname(prefix='array_jobs')
        with open(g, 'w') as f_out:
            f_out.write(os.linesep.join(jobs))
        h = mbkit.apps.make_script(["script=`sed -n \"${{SGE_TASK_ID}}p\" {0}`".format(g), "$script"])
        jobid = mbkit.dispatch.cluster.SunGridEngine.qsub([h], array=(1, 5, 5), hold=True, name=inspect.stack()[0][3])
        time.sleep(5)
        self.assertTrue(mbkit.dispatch.cluster.SunGridEngine.qstat(jobid))
        mbkit.dispatch.cluster.SunGridEngine.qdel(jobid)
        for f in jobs + [g, h]: os.unlink(f)

    def test_rename_array_logs_1(self):
        directory = os.getcwd()
        jobs = [mbkit.apps.make_script(["sleep 100"], directory=directory) for _ in range(5)]
        g = mbkit.util.tmp_fname(prefix='array_jobs', directory=directory)
        with open(g, 'w') as f_out: 
            f_out.write(os.linesep.join(jobs))
        h = mbkit.apps.make_script(["script=`sed -n \"${{SGE_TASK_ID}}p\" {0}`".format(g), "$script"])
        l = "arrayJob_$TASK_ID.log"
        jobid = mbkit.dispatch.cluster.SunGridEngine.qsub([h], array=(1, 5, 5), log=l, name=inspect.stack()[0][3])
        start, timeout = time.time(), False
        while mbkit.dispatch.cluster.SunGridEngine.qstat(jobid):
            time.sleep(5)
            # Don't wait too long, one minute, then fail
            if int((time.time() - start) / 60) > 1:
                mbkit.dispatch.cluster.SunGridEngine.qdel(jobid)
                timeout = True
                break
        if not timeout:
            mbkit.dispatch.cluster.SunGridEngine.rename_array_logs(g, directory=directory)
            for j in jobs:
                l = os.path.isfile(j.rsplit('.') + '.log')
                self.assertTrue(l)
                os.unlink(l)
        for f in jobs + [g, h]: os.unlink(f)
        if timeout:
            self.assertTrue(False)


if __name__ == "__main__":
        unittest.main(verbosity=2)


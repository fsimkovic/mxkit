"""Testing facility for mbkit.dispatch.cluster"""

__author__ = "Felix Simkovic"
__date__ = "10 May 2017"

import time
import unittest

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

    def test_qstat_1(self):
        content = """#!/bin/bash
        sleep(100)
        """
        f = mbkit.util.tmp_fname()
        with open(f, 'w') as f_out:
            f_out.write(content)
        l = mbkit.util.tmp_fname()
        jobid = mbkit.dispatch.cluster.SunGridEngine.qsub([script], log=l)
        while True:
            data = mbkit.dispatch.cluster.SunGridEngine.qstat(jobid)
            if data:
                self.assertEqual(jobid, int(data['job_number']))
                self.assertTrue('sge_o_shell' in data)
                self.assertTrue('sge_o_workdir' in data)
                self.assertTrue('sge_o_host' in data)
                break
            time.sleep(10)
        for f in [f, l]: os.unlink(f)

    def test_qstat_2(self):
        jobs = []
        for _ in range(5):
            content = """#!/bin/bash
            sleep(100)
            """
            f = mbkit.util.tmp_fname()
            with open(f, 'w') as f_out:
                f_out.write(content)
            jobs.append(f)
        g = mbkit.util.tmp_fname(prefix='array_jobs')
        with open(g, 'w') as f_out: 
            f_out.write(os.linesep.join(jobs))
        h = mbkit.util.tmp_fname(prefix='array_master')
        with open(h, 'w') as f_out:
            f_out.write(os.linesep.join([
                "#!/bin/sh", 
                "script=`sed -n \"${{SGE_TASK_ID}}p\" {0}`".format(g),
                "$script",
            ]))
        l = os.path.join(os.path.basename(g), "arrayJob_$TASK_ID.log")
        jobid = mbkit.dispatch.cluster.SunGridEngine.qsub([h], log=l)
        while True:
            data = mbkit.dispatch.cluster.SunGridEngine.qstat(jobid)
            if data:
                self.assertEqual(jobid, int(data['job_number']))
                self.assertTrue('sge_o_shell' in data)
                self.assertTrue('sge_o_workdir' in data)
                self.assertTrue('sge_o_host' in data)
                break
            time.sleep(20)
        for f in jobs + [g, h]: os.unlink(f)
        for i in range(5): 
            os.unlink(os.path.join(os.path.basename(g), "arrayJob_{0}.log".format(i)))
    
    def test_qsub_1(self):
        content = """#!/bin/bash
        sleep(1)
        """
        f = mbkit.util.tmp_fname()
        with open(f, 'w') as f_out:
            f_out.write(content)
        l = mbkit.util.tmp_fname()
        jobid = mbkit.dispatch.cluster.SunGridEngine.qsub([script], log=l)
        self.assertIsInstance(jobid, int)
        for f in [f, l]: os.unlink(f)

    def test_qsub_2(self):
        jobs = []
        for _ in range(5):
            content = """#!/bin/bash
            sleep(1)
            """
            f = mbkit.util.tmp_fname()
            with open(f, 'w') as f_out:
                f_out.write(content)
            jobs.append(f)
        g = mbkit.util.tmp_fname(prefix='array_jobs')
        with open(g, 'w') as f_out: 
            f_out.write(os.linesep.join(jobs))
        h = mbkit.util.tmp_fname(prefix='array_master')
        with open(h, 'w') as f_out:
            f_out.write(os.linesep.join([
                "#!/bin/sh", 
                "script=`sed -n \"${{SGE_TASK_ID}}p\" {0}`".format(g),
                "$script",
            ]))
        l = os.path.join(os.path.basename(g), "arrayJob_$TASK_ID.log")
        jobid = mbkit.dispatch.cluster.SunGridEngine.qsub([h], log=l)
        self.assertIsInstance(jobid, int)
        for f in jobs + [g, h]: os.unlink(f)
        for i in range(5):
            os.unlink(os.path.join(os.path.basename(g), "arrayJob_{0}.log".format(i)))
 
    def test_qdel_1(self):
        content = """#!/bin/bash
        sleep(100)
        """
        f = mbkit.util.tmp_fname()
        with open(f, 'w') as f_out:
            f_out.write(content)
        l = mbkit.util.tmp_fname()
        jobid = mbkit.dispatch.cluster.SunGridEngine.qsub([script], log=l) 
        for f in [f, l]: os.unlink(f)
 
    def test_qdel_2(self):
        jobs = []
        for _ in range(5):
            content = """#!/bin/bash
            sleep(100)
            """
            f = mbkit.util.tmp_fname()
            with open(f, 'w') as f_out:
                f_out.write(content)
            jobs.append(f)
        g = mbkit.util.tmp_fname(prefix='array_jobs')
        with open(g, 'w') as f_out: 
            f_out.write(os.linesep.join(jobs))
        h = mbkit.util.tmp_fname(prefix='array_master')
        with open(h, 'w') as f_out:
            f_out.write(os.linesep.join([
                "#!/bin/sh", 
                "script=`sed -n \"${{SGE_TASK_ID}}p\" {0}`".format(g),
                "$script",
            ]))
        l = os.path.join(os.path.basename(g), "arrayJob_$TASK_ID.log")
        jobid = mbkit.dispatch.cluster.SunGridEngine.qsub([h], log=log)
        mbkit.dispatch.cluster.SunGridEngine.qdel(jobid)
        for f in jobs + [g, h]: os.unlink(f)
        for i in range(5):
            os.unlink(os.path.join(os.path.basename(g), "arrayJob_{0}.log".format(i)))
    
    def test_rename_array_logs_1(self):
        jobs = []
        for _ in range(5):
            content = """#!/bin/bash
            sleep(1)
            """
            f = mbkit.util.tmp_fname()
            with open(f, 'w') as f_out:
                f_out.write(content)
            jobs.append(f)
        g = mbkit.util.tmp_fname(prefix='array_jobs')
        with open(g, 'w') as f_out: 
            f_out.write(os.linesep.join(jobs))
        h = mbkit.util.tmp_fname(prefix='array_master')
        with open(h, 'w') as f_out:
            f_out.write(os.linesep.join([
                "#!/bin/sh", 
                "script=`sed -n \"${{SGE_TASK_ID}}p\" {0}`".format(g),
                "$script",
            ]))
        l = os.path.join(os.path.basename(g), "arrayJob_$TASK_ID.log")
        jobid = mbkit.dispatch.cluster.SunGridEngine.qsub([h], log=log)
        while mbkit.dispatch.cluster.SunGridEngine.qstat(jobid):
            time.sleep(10)
        mbkit.dispatch.cluster.SunGridEngine.rename_array_logs(g, os.path.basename(g))
        for f in [g, h]: os.unlink(f)
        for j in jobs:
            l = os.path.isfile(j.rsplit('.') + '.log')
            self.assertTrue(l)
            for f in [j, l]: os.unlink(f)


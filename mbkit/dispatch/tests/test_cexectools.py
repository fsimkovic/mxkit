"""Testing facility for mbkit.dispatch.cexectools"""

__author__ = "Felix Simkovic"
__date__ = "10 May 2017"

import os
import sys
import unittest

import mbkit.dispatch.cexectools
import mbkit.util


class Test(unittest.TestCase):

    def test_cexec_1(self):
        cmd = [sys.executable, "-c", "import sys; print(\"hello\"); sys.exit(0)"]
        stdout = mbkit.dispatch.cexectools.cexec(cmd)
        self.assertEqual("hello", stdout)
    
    def test_cexec_2(self):
        cmd = [sys.executable, "-c", "import sys; sys.exit(1)"]
        self.assertRaises(RuntimeError, mbkit.dispatch.cexectools.cexec, cmd)

    def test_cexec_3(self):
        cmd = [sys.executable, "-c", "import sys; print(\"hello\"); sys.exit(0)"]
        stdout = mbkit.dispatch.cexectools.cexec(cmd, permit_nonzero=True)
        self.assertEqual("hello", stdout)
    
    def test_cexec_4(self):
        if sys.version_info < (3, 0):
            cmd = [sys.executable, "-c", "import sys; print(raw_input()); sys.exit(0)"]
        else:
            cmd = [sys.executable, "-c", "import sys; print(input()); sys.exit(0)"]
        stdout = mbkit.dispatch.cexectools.cexec(cmd, stdin="hello")
        self.assertEqual("hello", stdout)

    def test_cexec_5(self):
        cmd = [sys.executable, "-c", "import os, sys; print(os.getcwd()); sys.exit(0)"]
        directory = os.path.join(os.getcwd(), 'mbkit', 'dispatch')
        stdout = mbkit.dispatch.cexectools.cexec(cmd, directory=directory)
        self.assertEqual(directory, stdout)

    def test_prep_array_scripts_1(self):
        scripts = ["/path/to/script1.sh", "/path/to/script2.sh"]
        array_script, array_jobs = mbkit.dispatch.cexectools.prep_array_scripts(scripts, os.getcwd(), "SGE_TASK_ID")
        array_jobs_content = [l.strip() for l in open(array_jobs).readlines()]
        self.assertEqual(scripts, array_jobs_content)
        array_script_content = [l.strip() for l in open(array_script).readlines()]
        self.assertEqual(["#!/bin/sh", "script=`sed -n \"${{SGE_TASK_ID}}p\" {0}`".format(array_jobs), "$script"],
                         array_script_content)
        map(os.remove, [array_script, array_jobs])

    def test_prep_array_scripts_2(self):
        scripts = ["/path/to/script1.sh", "/path/to/script2.sh"]
        array_script, array_jobs = mbkit.dispatch.cexectools.prep_array_scripts(scripts, os.getcwd(), "LSB_JOBINDEX")
        array_jobs_content = [l.strip() for l in open(array_jobs).readlines()]
        self.assertEqual(scripts, array_jobs_content)
        array_script_content = [l.strip() for l in open(array_script).readlines()]
        self.assertEqual(["#!/bin/sh", "script=`sed -n \"${{LSB_JOBINDEX}}p\" {0}`".format(array_jobs), "$script"],
                         array_script_content)
        map(os.remove, [array_script, array_jobs])

    def test_prep_array_scripts_3(self):
        scripts = ["/path/to/script1.sh", "/path/to/script2.sh"]
        array_script, array_jobs = mbkit.dispatch.cexectools.prep_array_scripts(scripts, os.getcwd(), "RANDOM_TEXT")
        array_jobs_content = [l.strip() for l in open(array_jobs).readlines()]
        self.assertEqual(scripts, array_jobs_content)
        array_script_content = [l.strip() for l in open(array_script).readlines()]
        self.assertEqual(["#!/bin/sh", "script=`sed -n \"${{RANDOM_TEXT}}p\" {0}`".format(array_jobs), "$script"],
                         array_script_content)
        map(os.remove, [array_script, array_jobs])

    def test_prep_array_scripts_4(self):
        scripts = ["/path/to/script1.sh", "/path/to/script2.sh"]
        array_script, array_jobs = mbkit.dispatch.cexectools.prep_array_scripts(scripts, "mbkit", "RANDOM_TEXT")
        self.assertEqual(os.path.abspath("mbkit"), os.path.dirname(array_script))
        self.assertEqual(os.path.abspath("mbkit"), os.path.dirname(array_jobs))
        array_jobs_content = [l.strip() for l in open(array_jobs).readlines()]
        self.assertEqual(scripts, array_jobs_content)
        array_script_content = [l.strip() for l in open(array_script).readlines()]
        self.assertEqual(["#!/bin/sh", "script=`sed -n \"${{RANDOM_TEXT}}p\" {0}`".format(array_jobs), "$script"],
                         array_script_content)
        map(os.remove, [array_script, array_jobs])


if __name__ == "__main__":
    unittest.main(verbosity=2)

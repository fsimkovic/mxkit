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
        if (sys.version_info < (3, 0)):
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


if __name__ == "__main__":
    unittest.main(verbosity=2)

# -*- coding: utf-8 -*-

import sys
import mock
import unittest
from pingpong.transport import system
from tests import helper as h

class test_sys_transport(unittest.TestCase):

    def test_write_uses_sys_stdout(self):
        with h.mock_value(sys, "stdout") as mymock:
            t = system.sys_transport()
            t.write("foobar")
            mymock[0].write.assert_called_with("foobar")

    def test_terminate_raise_EOFError(self):
        t = system.sys_transport()
        self.assertRaises(EOFError, t.terminate)

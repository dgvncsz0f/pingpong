# -*- coding: utf-8 -*-

import sys
import termios
import tty
import mock
import unittest
from pingpong.engine import term
from pingpong.transport import system
from tests import helper as h

class test_tty_engine(unittest.TestCase):

    def test_run_invokes_the_proper_methods(self):
        with h.mock_value(term.tty_engine, "_loop") as mymock:
            session = mock.Mock()
            term.tty_engine().run(lambda _: session)
            session.on_begin.assert_called()
            mymock[0].assert_called()
            session.on_end.assert_called()

    def test__loop_turns_raw_mode_on(self):
        values = ["f"]
        def read_f(l):
            self.assertEqual(1, l)
            if (len(values) == 0):
                raise(EOFError())
            return(values.pop())
        with h.mock_value( sys,     "stdin",
                           termios, "tcgetattr",
                           tty,     "setraw",
                           termios, "tcsetattr"
                         ) as mymock:
            mymock[0].read.side_effect = read_f
            session = mock.Mock()
            term.tty_engine().run(lambda _: session)

            mymock[1].assert_called()
            mymock[2].assert_called()
            mymock[3].assert_called()
            session.on_data.assert_called_with("f")

    def test_run_uses_sys_transport(self):
        with h.mock_value(term.tty_engine, "_loop") as mymock:
            factory = mock.Mock()
            term.tty_engine().run(factory)
            self.assertTrue(isinstance(factory.call_args[0][0], system.sys_transport))

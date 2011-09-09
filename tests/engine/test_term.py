# -*- coding: utf-8 -*-

# Copyright (c) 2011, Diego Souza
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
#   * Neither the name of the <ORGANIZATION> nor the names of its contributors
#     may be used to endorse or promote products derived from this software
#     without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

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
            self.assertEqual(1, session.on_begin.call_count)
            self.assertEqual(1, mymock[0].call_count)
            self.assertEqual(1, session.on_end.call_count)

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

            self.assertEqual(1, mymock[1].call_count)
            self.assertEqual(1, mymock[2].call_count)
            self.assertEqual(1, mymock[3].call_count)
            session.on_data.assert_called_with("f")

    def test_run_uses_sys_transport(self):
        with h.mock_value(term.tty_engine, "_loop") as mymock:
            factory = mock.Mock()
            term.tty_engine().run(factory)
            self.assertTrue(isinstance(factory.call_args[0][0], system.sys_transport))

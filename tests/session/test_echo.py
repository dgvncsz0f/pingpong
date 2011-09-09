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


import unittest
import mock
from pingpong.session import echo

class test_echo(unittest.TestCase):

    def test_do_cancel(self):
        t = mock.Mock()
        h = echo.echo(t)
        h.do_cancel()
        self.assertEqual([(("^C",),{}), (("\r\n",),{})], t.write.call_args_list)

    def test_do_unhandle(self):
        t = mock.Mock()
        h = echo.echo(t)
        h.do_unhandle()
        t.write.assert_called_with("\b \b")

    def test_do_handle_echoes_char_back(self):
        t = mock.Mock()
        h = echo.echo(t)
        h.do_handle("a")
        t.write.assert_called_with("a")

    def test_do_handle_echoes_newline_properly0(self):
        t = mock.Mock()
        h = echo.echo(t)
        self.assertFalse(h.stop)
        h.do_handle("\r")
        t.write.assert_called_with("\r\n")
        self.assertTrue(h.stop)

    def test_do_handle_echoes_newline_properly1(self):
        t = mock.Mock()
        h = echo.echo(t)
        self.assertFalse(h.stop)
        h.do_handle("\n")
        t.write.assert_called_with("\r\n")
        self.assertTrue(h.stop)

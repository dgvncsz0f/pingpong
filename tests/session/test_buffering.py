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
from pingpong.session import buffering

class test_buffering(unittest.TestCase):

    def test_do_cancel(self):
        h = buffering.buffering(mock.Mock(), mock.Mock())
        h.do_cancel()
        h.c_cc.assert_called_with()

    def test_do_unhandle(self):
        h = buffering.buffering(mock.Mock())
        h.buffer = mock.Mock()
        h.do_unhandle()
        h.buffer.pop.assert_called_with()

    def test_do_handle_buffers_character(self):
        h = buffering.buffering(mock.Mock())
        h.do_handle("a")
        self.assertEqual(["a"], h.buffer)

    def test_do_handle_flushes_buffer_on_newline0(self):
        h = buffering.buffering(mock.Mock())
        h.do_handle("a")
        h.do_handle("\n")
        self.assertEqual([], h.buffer)
        h.cc.assert_called_with("a")

    def test_do_handle_flushes_buffer_on_newline1(self):
        h = buffering.buffering(mock.Mock())
        h.do_handle("a")
        h.do_handle("\r")
        self.assertEqual([], h.buffer)
        h.cc.assert_called_with("a")


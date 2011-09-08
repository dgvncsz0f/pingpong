# -*- coding: utf-8 -*-

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


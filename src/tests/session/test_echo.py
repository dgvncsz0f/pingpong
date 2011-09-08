# -*- coding: utf-8 -*-

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

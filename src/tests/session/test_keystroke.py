# -*- coding: utf-8 -*-

import unittest
import mock
from pingpong.session import keystroke
from tests import helper as h

class test_keystroke(unittest.TestCase):

    def test_init(self):
        k = keystroke.keystroke(1500)
        self.assertEqual({}, k.mapping)
        self.assertEqual([], k.kbuffer)
        self.assertEqual(1500, k.timeout)

    def test_bind_updates_kbuffer(self):
        k = keystroke.keystroke()
        k.bind("fo", "bar")
        self.assertEqual([(None,0),(None, 0)], k.kbuffer)

    def test_bind_defines_key_on_mapping(self):
        k = keystroke.keystroke()
        k.bind("foo", "bar")
        self.assertEqual("bar", k.mapping["foo"])

    def test_simpleterm_bindings_defines_Cd(self):
        m = mock.Mock()
        k = keystroke.keystroke()
        k.simpleterm_bindings(m)
        k.do_handle("")
        self.assertEqual(1, m.terminate.call_count)

    def test_simpleterm_bindings_defines_Cc(self):
        with h.mock_value(keystroke.keystroke, "cancel") as mymock:
            k = keystroke.keystroke()
            k.simpleterm_bindings(mock.Mock())
            k.do_handle("")
            self.assertEqual(1, mymock[0].call_count)

    def test_simpleterm_bindings_defines_BACKSPACE(self):
        with h.mock_value(keystroke.keystroke, "unhandle") as mymock:
            k = keystroke.keystroke()
            k.simpleterm_bindings(mock.Mock())
            k.do_handle("")
            self.assertEqual(1, mymock[0].call_count)

    def test_do_handle_invokes_stop_propagation_when_there_is_a_binding_defined(self):
        m = mock.Mock()
        k = keystroke.keystroke()
        k.bind(("a",), m)
        k.do_handle("a")
        self.assertEqual(1, m.call_count)
        self.assertTrue(k.stop)

    def test_do_handle_does_nothing_when_keystroke_is_not_defined(self):
        m = mock.Mock()
        k = keystroke.keystroke()
        k.bind(("a",), m)
        k.do_handle("x")
        self.assertEqual(0, m.call_count)
        self.assertFalse(k.stop)

    def test_cleanup_removes_expired_items(self):
        k = keystroke.keystroke(timeout=-1)
        k.bind(("a",), mock.Mock())
        k.do_handle("x")
        k._cleanup()
        self.assertEqual([(None, 0)], k.kbuffer)

    def test_cleanup_keeps_non_expired_items(self):
        k = keystroke.keystroke(timeout=1000)
        k.bind(("a","b"), mock.Mock())
        k.do_handle("x")
        k._cleanup()
        self.assertEqual("x", k.kbuffer[0][0])

    def test_stamp_uses_current_timestap(self):
        with h.mock_value(keystroke, "now") as mymock:
            mymock[0].return_value = "now"
            k = keystroke.keystroke()
            self.assertEqual(("x","now"), k._stamp("x"))

    # TODO:test_keystroke
    # TODO:test_expire

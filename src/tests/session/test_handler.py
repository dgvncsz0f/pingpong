# -*- coding: utf-8 -*-

import unittest
import mock
from pingpong.session import handler
from tests import helper as h

class test_handler(unittest.TestCase):

    def test_init(self):
        h = handler.handler()
        self.assertEqual([], h.handlers)
        self.assertFalse(h.stop)

    def test_chain_returns_self(self):
        h = handler.handler()
        self.assertEqual(h, h.chain("foo", "bar"))

    def test_chain_extends_handlers(self):
        h = handler.handler()
        h.chain("foo", "bar")
        self.assertEqual(["foo","bar"], h.handlers)

    def test_chain_other_returns_param(self):
        h = handler.handler()
        self.assertEqual("foo", h.chain_other("foo"))

    def test_chain_other_appends_to_handlers(self):
        h = handler.handler()
        h.chain_other("foo")
        self.assertEqual(["foo"], h.handlers)

    def test_stop_propagation_updates_stop_variable(self):
        h = handler.handler()
        h.stop_propagation()
        self.assertTrue(h.stop)

    def test_cancel_call_all_handlers(self):
        m = mock.Mock()
        h = handler.handler()
        h.chain(m)
        h.cancel()
        m.cancel.assert_called_with()

    def test_cancel_invokes_do_cancel(self):
        with h.mock_value(handler.handler, "do_cancel") as mymock:
            hl = handler.handler()
            hl.do_cancel()
            mymock[0].assert_called_with()
    
    def test_cancel_does_not_invoke_handlers_if_stop_is_set(self):
        m = mock.Mock()
        h = handler.handler()
        h.chain(m)
        h.stop_propagation()
        h.cancel()
        self.assertEqual(0, m.cancel.call_count)

    def test_cancel_resets_stop_variable(self):
        m = mock.Mock()
        h = handler.handler()
        h.chain(m)
        h.stop_propagation()
        h.cancel()
        self.assertFalse(h.stop)

    def test_unhandle_call_all_handlers(self):
        m = mock.Mock()
        h = handler.handler()
        h.chain(m)
        h.unhandle()
        m.unhandle.assert_called_with()

    def test_unhandle_invokes_do_cancel(self):
        with h.mock_value(handler.handler, "do_unhandle") as mymock:
            hl = handler.handler()
            hl.do_unhandle()
            mymock[0].assert_called_with()
    
    def test_unhandle_does_not_invoke_handlers_if_stop_is_set(self):
        m = mock.Mock()
        h = handler.handler()
        h.chain(m)
        h.stop_propagation()
        h.unhandle()
        self.assertEqual(0, m.cancel.call_count)

    def test_unhandle_resets_stop_variable(self):
        m = mock.Mock()
        h = handler.handler()
        h.chain(m)
        h.stop_propagation()
        h.unhandle()
        self.assertFalse(h.stop)

    def test_handle_call_all_handlers(self):
        m = mock.Mock()
        h = handler.handler()
        h.chain(m)
        h.handle("a")
        m.handle.assert_called_with("a")

    def test_handle_invokes_do_cancel(self):
        with h.mock_value(handler.handler, "do_handle") as mymock:
            hl = handler.handler()
            hl.do_handle("a")
            mymock[0].assert_called_with("a")
    
    def test_handle_does_not_invoke_handlers_if_stop_is_set(self):
        m = mock.Mock()
        h = handler.handler()
        h.chain(m)
        h.stop_propagation()
        h.handle("a")
        self.assertEqual(0, m.handle.call_count)

    def test_handle_resets_stop_variable(self):
        m = mock.Mock()
        h = handler.handler()
        h.chain(m)
        h.stop_propagation()
        h.handle("a")
        self.assertFalse(h.stop)


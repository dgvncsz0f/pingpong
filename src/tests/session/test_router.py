# -*- coding: utf-8 -*-

import unittest
import mock
from pingpong.session import router

class test_router(unittest.TestCase):

    def test_init(self):
        r = router.router("router", "default")
        self.assertEqual("router", r.routes)
        self.assertEqual("default", r.default)

    def test_find_action_uses_routes_as_regexp(self):
        r = router.router(((r"^foobar$", "success"),), "default")
        self.assertEqual(("success",()), r.find_action("foobar"))

    def test_find_action_uses_default_route(self):
        r = router.router((), "default")
        self.assertEqual(("default",()), r.find_action("foobar"))

    def test_find_action_returns_matching_groups(self):
        r = router.router(((r"^foo(bar)$", "success"),), "default")
        self.assertEqual(("success", ("bar",)), r.find_action("foobar"))

    def test_dispatch_gives_the_line_that_originated_the_event(self):
        m = mock.Mock()
        r = router.router((), m)
        r.dispatch("foobar")
        m.assert_called_with("foobar")

    def test_dispatch_gives_the_line_that_originated_the_event_plus_the_matching_groups(self):
        m = mock.Mock()
        r = router.router(((r"^foo(bar)$", m),), "default")
        r.dispatch("foobar")
        m.assert_called_with("foobar", "bar")

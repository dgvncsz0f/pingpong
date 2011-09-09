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

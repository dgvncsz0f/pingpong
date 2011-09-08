# -*- coding: utf-8 -*-

import sys
import mock
import unittest
from pingpong.transport import twisted
from tests import helper as h

class test_twisted_transport(unittest.TestCase):

    def test_write_uses_protocol_transport(self):
        protocol = mock.Mock()
        t = twisted.twisted_transport(protocol)
        t.write("foobar")
        protocol.transport.write.assert_called_with("foobar")

    def test_terminate_invokes_loseConnection(self):
        protocol = mock.Mock()
        t = twisted.twisted_transport(protocol)
        t.terminate()
        protocol.transport.loseConnection.assert_called()

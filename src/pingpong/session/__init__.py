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

from pingpong.session import handler
from pingpong.session import buffering
from pingpong.session import keystroke
from pingpong.session import echo
from pingpong.session import router

class session(object):
    """
      Represents a session that may be used to interact with the
      user.
    """

    def __init__(self, transport):
        """
          Initializes this session with a given transport. Transport
          is the object that allows send information to the peer.
        """
        self.transport = transport
    
    def on_begin(self):
        """
          Called once when application starts.
        """

    def on_end(self):
        """
          Called once when application finishes.
        """

    def on_data(self, c):
        """
          Called everytime user sends a character user enters.
        """

class interactive_session(session):

    def __init__(self, transport):
        super(interactive_session, self).__init__(transport)
        
        lhandler = buffering.buffering(self.on_line, self.on_abort)
        ehandler = echo.echo(transport)
        khandler = keystroke.keystroke()
        khandler.simpleterm_bindings(transport)

        self.handler = handler.handler()
        self.handler.chain_next(khandler).chain_self(ehandler, lhandler)
        self.networks = []

    def on_data(self, c):
        self.handler.handle(c)


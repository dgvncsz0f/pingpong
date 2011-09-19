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

import time
from pingpong.engine import term
from pingpong.engine import ssh
from pingpong import session
from pingpong.session import handler
from pingpong.session import buffering
from pingpong.session import keystroke
from pingpong.session import echo
from pingpong.session import router

class ping_session(session.simple_session):

    def on_begin(self, interactive):
        self.interactive = interactive
        self._prompt()
        self.noecho = not interactive
            
    def on_end(self):
        pass

    def on_abort(self):
        self._endl()
        self._prompt()

    def on_line(self, line):
        r = router.router(( (r"^ping$", self._pong),
                          ), self._missing)
        r.dispatch(line)
        self._endl()
        self._prompt()

    def _missing(self, raw, *args):
        self.transport.write(">> %s" % raw)

    def _pong(self, raw, *args):
        self.transport.write("pong")

    def _prompt(self):
        if (self.interactive):
            self.transport.write("$ ")

    def _endl(self):
        self.transport.write("\r\n")

if (__name__ == "__main__"):
    # e = term.tty_engine()
    e = ssh.ssh_engine()
    e.run(ping_session)


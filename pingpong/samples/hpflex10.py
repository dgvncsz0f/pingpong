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
import random
from pingpong.engine import ssh
from pingpong import session
from pingpong.session import handler
from pingpong.session import buffering
from pingpong.session import keystroke
from pingpong.session import echo
from pingpong.session import router

class hpflex10_session(session.interactive_session):

    def __init__(self, transport, logger=[]):
        super(hpflex10_session, self).__init__(transport)
        self.logger = logger

    def on_begin(self):
        self._greeting()
        self._endl()
        self._prompt()

    def on_end(self):
        pass

    def on_abort(self):
        self._endl()
        self._prompt()

    def on_line(self, line):
        r = router.router(( (r"^add network\s+(.*?)\s+(.*?)$",         self._add_network),
                            (r"^set network\s+(.*?)\s+(.*?)$",         self._set_network),
                            (r"^show enclosure\s*$",                   self._show_enclosure),
                            (r"^set enet-connection\s+(.*?)\s+(.*?)$", self._set_enetconnection)
                          ), self._missing)
        r.dispatch(line)
        self._endl()
        self._prompt()

    def _add_network(self, raw, name, *args):
        name = name.strip()
        self.networks.append(name)
        if (random.random() > 0.5):
            self.transport.write("SUCCESS: Network added : %s" % name)
        else:
            self.transport.write("ERROR: Duplicated name")
        self._endl()

    def _set_network(self, raw, name, *args):
        name = name.strip()
        self.transport.write("SUCCESS: Network modified : %s" % name)
        self._endl()

    def _show_enclosure(self, raw, *args):
        self.transport.write("\r\n".join([ "=====================================================================",
                                           "ID    Name      Import Status  Serial Number  Part        Asset Tag  ",
                                           "                                              Number                 ",
                                           "=====================================================================",
                                           "enc0  BLHP0042  Imported       XXXXXXXXXX     XXXXXX-XXX             ",
                                           "                                                                     ",
                                         ]))

    def _missing(self, raw, *args):
        self.transport.write("ERROR: UNKNOWN COMMAND : %s" % raw)
        self._endl()

    def _set_enetconnection(self, raw, name, *args):
        time.sleep(2)
        name = name.strip()
        self.transport.write("SUCCESS: Connection modified : %s" % name)
        self._endl()

    def _greeting(self):
        self.transport.write("\r\n".join([ "Last login: Thu Jan  1 00:00:00 1970 from 127.0.0.1                            ",
                                           "-------------------------------------------------------------------------------",
                                           "HP Virtual Connect Management CLI v0.00                                        ",
                                           "Build: 0.00-0 (r00000) Jan  1 1970 00:00:00                                    ",
                                           "(C) Copyright 2006-2011 Hewlett-Packard Development Company, L.P.              ",
                                           "All Rights Reserved                                                            ",
                                           "-------------------------------------------------------------------------------",
                                           "                                                                               ",
                                           "                                                                               ",
                                           "GETTING STARTED:                                                               ",
                                           "                                                                               ",
                                           "help           : displays a list of available subcommands                      ",
                                           "exit           : quits the command shell                                       ",
                                           "<subcommand> ? : displays a list of managed elements for a subcommand          ",
                                           "<subcommand> <managed element> ? : displays detailed help for a command        ",
                                           "                                                                               ",
                                         ]))

    def _prompt(self):
        self.transport.write("->")

    def _endl(self):
        self.transport.write("\r\n")

if (__name__ == "__main__"):
    e = ssh.ssh_engine()
    e.run(hpflex10_session)


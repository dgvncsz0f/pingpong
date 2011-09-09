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

import os
import time
from pingpong.session import handler

def now():
    return(1000 * time.time())

class keystroke(handler.handler):

    def __init__(self, timeout=200):
        super(keystroke, self).__init__()
        self.mapping = {}
        self.kbuffer = []
        self.timeout = timeout

    def bind(self, key, f):
        self.mapping[key] = f
        bufsz = max(map(len, self.mapping.keys()))
        self.kbuffer = bufsz * [(None,0)]
        return(self)

    def simpleterm_bindings(self, transport):
        self.bind(("",), lambda : transport.terminate())
        self.bind(("",), lambda : self.unhandle())
        self.bind(("",), lambda : self.cancel())

    def do_handle(self, c):
        key = self._keystroke(c)
        f = self.mapping.get(key, None)
        if (f is None):
            pass
        else:
            f()
            self.stop_propagation()

    def _keystroke(self, c):
        self._cleanup()
        self.kbuffer.append(self._stamp(c))
        self.kbuffer = self.kbuffer[1:]
        event = filter(lambda x: x is not None, map(lambda e: e[0], self.kbuffer))
        return(tuple(event))

    def _cleanup(self):
        self.kbuffer = map(self._expire, self.kbuffer)

    def _expire(self, item):
        current = now()
        event = item[1]
        if ((current - event) > self.timeout):
            return(None, 0)
        else:
            return(item)

    def _stamp(self, c):
        return(c, now())

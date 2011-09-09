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


import mock

def mock_value(*args):
    ms = list(args)
    lim = len(args)
    for k in reversed(range(2, lim+1, 2)):
        ms.insert(k, mock.Mock())
    return(mock_value_with(*ms))

def mock_value_with(*args):
    ms = []
    lim = len(args)
    for k in xrange(0, lim, 3):
        ms.append(MockContext(args[k], args[k+1], args[k+2]))
    return(ContextList(*ms))

class ANY(object):

    def __eq__(self, x):
        return(True)

class ContextList(object):

    def __init__(self, *args):
        self.contexts = args

    def __enter__(self):
        for ctx in self.contexts:
            ctx.__enter__()
        return(self)

    def __exit__(self, type, value, tb):
        for ctx in self.contexts:
            ctx.__exit__(type, value, tb)

    def __call__(self, *args, **kwargs):
        return(self.at(0).__call__(*args, **kwargs))

    def at(self, index):
        return(self.contexts[index].value)

    def __getitem__(self, k):
        return(self.at(k))

class TrackAssignments(object):

    def __init__(self):
        self.assignment_args = []
        self.attrcache = {}

    def __setattr__(self, key, value):
        if (key in ["assignment_args", "attrcache"]):
            super(TrackAssignments, self).__setattr__(key, value)
        else:
            self.assignment_args.append((key, value))

    def __getattr__(self, key):
        if (key not in self.attrcache):
            self.attrcache[key] = mock.Mock()
        return(self.attrcache[key])

class MockContext(object):

    def __init__(self, base, attr, value):
        self.base = base
        self.attr = attr
        self.value = value

    def __enter__(self):
        self.has_attr = hasattr(self.base, self.attr)
        if (self.has_attr):
            self.ovalue = getattr(self.base, self.attr)
        setattr(self.base, self.attr, self.value)

    def __exit__(self, type, value, tb):
        delattr(self.base, self.attr)
        if (self.has_attr):
            setattr(self.base, self.attr, self.ovalue)


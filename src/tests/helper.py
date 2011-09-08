# -*- coding: utf-8 -*-

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


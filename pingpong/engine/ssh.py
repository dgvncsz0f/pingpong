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
import subprocess
import tempfile
from Crypto.PublicKey import RSA
from twisted.internet import reactor
from twisted.internet import protocol
from twisted.cred import portal
from twisted.cred import checkers
from twisted.cred import credentials
from twisted.conch import error
from twisted.conch import avatar
from twisted.conch import recvline
from twisted.conch import interfaces as conchinterfaces
from twisted.conch.ssh import factory as ssh_factory
from twisted.conch.ssh import userauth
from twisted.conch.ssh import connection
from twisted.conch.ssh import keys
from twisted.conch.ssh import session
from twisted.conch.ssh import common
from twisted.conch.insults import insults
from twisted.application import service
from twisted.application import internet
from twisted.python import components
from zope.interface import implements
from pingpong import engine
from pingpong.transport import twisted as ttransport
from pingpong.transport import pipe as ptransport

def rsa_keygen():
    def ssh_keygen(key):
        fd, tmpf = tempfile.mkstemp()
        try:
            os.write(fd, key.exportKey())
            os.fsync(fd)
            # TODO:figure_a_better_implementation
            args = ["/usr/bin/ssh-keygen", "-y", "-f", tmpf]
            p = subprocess.Popen(args, stdout=subprocess.PIPE)
            rc = p.wait()
            if (rc != 0):
                raise(RuntimeError("error creating ssh-pubkey"))
            result = p.stdout.read().strip()
            return(result)
        finally:
            os.unlink(tmpf)
            os.close(fd)
    privkey = RSA.generate(1024)
    return(ssh_keygen(privkey), privkey.exportKey())

class session_wrapper_protocol(protocol.Protocol):

    def __init__(self, avatar, interactive):
        self.stransport = ttransport.twisted_transport(self)
        self.interactive = interactive
        self.avatar = avatar
        self.session = self.avatar.sfactory(self.stransport)

    def connectionMade(self):
        self.session.on_begin(self.interactive)

    def connectionLost(self, reason):
        self.session.on_end()

    def dataReceived(self, data):
        map(self.session.on_data, data)

class pp_avatar(avatar.ConchUser):
    implements(conchinterfaces.ISession)

    def __init__(self, username, sfactory):
        avatar.ConchUser.__init__(self)
        self.username = username
        self.sfactory = sfactory
        self.channelLookup.update({'session':session.SSHSession})

    def openShell(self, proto):
        p = session_wrapper_protocol(self, True)
        p.makeConnection(proto)
        proto.makeConnection(session.wrapProtocol(p))

    def getPty(self, terminal, windowSize, attrs):
        pass

    def execCommand(self, proto, cmd):
        p = session_wrapper_protocol(self, False)
        p.makeConnection(proto)
        proto.makeConnection(session.wrapProtocol(p))
        p.dataReceived(cmd)
        p.stransport.terminate()

    def eofReceived(self):
        pass

    def closed(self):
        pass

class pp_ssh_factory(ssh_factory.SSHFactory):

    def __init__(self, myportal):
        pubkey, privkey = rsa_keygen()

        self.portal = myportal
        self.publicKeys  = { "ssh-rsa": keys.Key.fromString(data=pubkey)
                           }
        self.privateKeys = { "ssh-rsa": keys.Key.fromString(data=privkey)
                           }
        self.services    = { "ssh-userauth": userauth.SSHUserAuthServer,
                             "ssh-connection": connection.SSHConnection
                           }

class pp_realm:
    implements(portal.IRealm)

    def __init__(self, factory):
        self.sfactory = factory

    def requestAvatar(self, avatarId, mind, *interfaces):
        if conchinterfaces.IConchUser in interfaces:
            return(interfaces[0], pp_avatar(avatarId, self.sfactory), lambda: None)
        else:
            raise(RuntimeError("No supported interfaces found."))

class ssh_engine(engine.engine):

    def _factory(self, factory, usersdb, port):
        passwd = checkers.InMemoryUsernamePasswordDatabaseDontUse(**usersdb)
        myrealm = pp_realm(factory)
        myportal = portal.Portal(myrealm)
        myportal.registerChecker(passwd)
        return(pp_ssh_factory(myportal))
    
    def application(self, factory, usersdb={"root": "password"}, port=2222):
        app = service.Application("PINGPONG SSH")
        myfactory = self._factory(factory, usersdb, port)
        myservice = internet.TCPServer(port, myfactory)
        myservice.setServiceParent(app)
        return(app)

    def run(self, factory, usersdb={"root": "password"}, port=2222):
        myfactory = self._factory(factory, usersdb, port)
        reactor.listenTCP(port, myfactory)
        reactor.run()

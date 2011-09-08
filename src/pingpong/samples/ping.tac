# -*- coding: utf-8 -*-

from pingpong.engine import ssh
from pingpong.samples import ping

engine = ssh.ssh_engine()
application = engine.application(ping.ping_session, usersdb={"root":"root"}, port=2222)

# -*- coding: utf-8 -*-

from pingpong.engine import ssh
from pingpong.samples import hpflex10

engine = ssh.ssh_engine()
application = engine.application(hpflex10.hpflex10_session)

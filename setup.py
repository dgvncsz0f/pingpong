import os
from setuptools import setup
from setuptools import find_packages

VERSION = "0.0.1"

setup( name             = "pingpong",
       version          = VERSION,
       packages         = find_packages(exclude=["tests", "tests.*"]),
       author           = "Diego Souza",
       author_email     = "dsouza+pingpong@bitforest.org",
       description      = "A library for quickly creating line-based interactive programs",
       keywords         = "interactive line-based protocols",
       data_files       = ( ("/etc/pingpong", [ "pingpong/samples/ping.tac",
                                                "pingpong/samples/hpflex10.tac"
                                              ]
                            ),
                          ),
       install_requires = [ "twisted >= 11.0.0",
                            "twisted-conch >= 11.0.0"
                          ]
     )

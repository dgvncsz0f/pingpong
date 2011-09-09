import os
from setuptools import setup
from setuptools import find_packages

setup( name         = "pingpong",
       version      = "0.0.1",
       packages     = find_packages(exclude=["tests", "tests.*"]),
       author       = "Diego Souza",
       author_email = "dsouza at bitforest.org",
       description  = "A library for quickly creating line-based interactive programs",
       keywords     = "interactive line-based protocols"
     )

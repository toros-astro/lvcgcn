[![Build Status](https://travis-ci.org/toros-astro/lvcgcn.svg?branch=master)](https://travis-ci.org/toros-astro/lvcgcn)
[![Coverage](https://codecov.io/gh/toros-astro/lvcgcn/branch/master/graphs/badge.svg?branch=master)](https://codecov.io/gh/toros-astro/lvcgcn)
[![Documentation Status](https://readthedocs.org/projects/lvcgcn/badge/?version=latest)](https://lvcgcn.readthedocs.io/en/latest/?badge=latest)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

# The LVC GCN Daemon Service

This is intended to perform various tasks

* A daemon to establish a connection with LVC GCN notices to receive alerts and notify the collaborators.
* Once the alert VOEvent is received, generate possible targets of observation.
* Send out emails with alert information to collaborators and upload observation targets to broker website.

-------

(c) TOROS Dev Team

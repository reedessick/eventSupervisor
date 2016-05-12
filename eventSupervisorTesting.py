#!/usr/bin/python
usage = "eventSupervisorTesting.py [--options]"
description = "a module containing testing routines for the event supervisor toolkits"
author = "reed.essick@ligo.org"

#-------------------------------------------------

import eventSupervisor as es
import eventSupervisorUtils as esUtils

from notify import notify

from basic import basic
from basic import approvalProcessor

from skymaps import skymaps
from skymaps import skymapSummary

from pe import bayestar
from pe import bayeswavePE
from pe import cwbPE
from pe import libPE
from pe import lalinf

from dq import dq
from dq import idq
from dq import omegaScan
from dq import segDB2grcDB

#------------------------

from optparse import OptionParser

#-------------------------------------------------

parser = OptionParser(usage=usage, description=description)

parser.add_option("-v", "--verbose", default=False, action="store_true")

# notify
parser.add_option("", "--notify", default=False, action="store_true")

# basic
parser.add_option("", "--basic", default=False, action="strore_true")
parser.add_option("", "--approvalProcessor", default=False, action="strore_true")

# skymaps
parser.add_option("", "--skymaps", default=False, action="strore_true")
parser.add_option("", "--skymapSummary", default=False, action="strore_true")

# pe
parser.add_option("", "--bayestar", default=False, action="strore_true")
parser.add_option("", "--bayeswavePE", default=False, action="strore_true")
parser.add_option("", "--cwbPE", default=False, action="strore_true")
parser.add_option("", "--libPE", default=False, action="strore_true")
parser.add_option("", "--lalinf", default=False, action="strore_true")

# dq
parser.add_option("", "--dq", default=False, action="strore_true")
parser.add_option("", "--idq", default=False, action="strore_true")
parser.add_option("", "--omegaScan", default=False, action="strore_true")
parser.add_option("", "--segDB2grcDB", default=False, action="strore_true")

opts, args = parser.parse_args()

#-------------------------------------------------

### want to test the instantiation of all QueueItems and their associated Tasks
### we should be able to get away with this simply by instantiating the QueueItems and then asserting that their attributes are as expected
###   -> some of those attributes are Tasks, which we can then check iteratively



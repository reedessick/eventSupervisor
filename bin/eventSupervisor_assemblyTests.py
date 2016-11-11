#!/usr/bin/python
usage       = "eventSupervisor_assemblyTests.py [--options]"
description = "a script testing how event supervisor assembles and manages a SortedQueue through parseAlert"
author      = "reed.essick@ligo.org"

#-------------------------------------------------

import eventSupervisor.eventSupervisor as es
import eventSupervisor.eventSupervisorUtils as esUtils

from eventSupervisor.notify import notify

from eventSupervisor.basic import basic
from eventSupervisor.basic import approvalProcessor

from eventSupervisor.skymaps import skymaps
from eventSupervisor.skymaps import skymapSummary

from eventSupervisor.pe import bayestar
from eventSupervisor.pe import bayeswavePE
from eventSupervisor.pe import cwbPE
from eventSupervisor.pe import libPE
from eventSupervisor.pe import lalinf

from eventSupervisor.dq import dq
from eventSupervisor.dq import idq
from eventSupervisor.dq import omegaScan
from eventSupervisor.dq import segDB2grcDB

#------------------------

from ligo.gracedb.rest import GraceDb

#------------------------

import time

from optparse import OptionParser

#-------------------------------------------------

parser = OptionParser(usage=usage, description=description)

### check everything
parser.add_option('', '--everything', default=False, action="store_true", help="run tests for everything")

# notify
parser.add_option("", "--notify", default=False, action="store_true")

# basic
parser.add_option("", "--basic", default=False, action="store_true")
parser.add_option("", "--approvalProcessor", default=False, action="store_true")

# skymaps
parser.add_option("", "--skymaps", default=False, action="store_true")
parser.add_option("", "--skymapSummary", default=False, action="store_true")

# pe
parser.add_option("", "--bayestar", default=False, action="store_true")
parser.add_option("", "--bayeswavePE", default=False, action="store_true")
parser.add_option("", "--cwbPE", default=False, action="store_true")
parser.add_option("", "--libPE", default=False, action="store_true")
parser.add_option("", "--lalinf", default=False, action="store_true")

# dq
parser.add_option("", "--dq", default=False, action="store_true")
parser.add_option("", "--idq", default=False, action="store_true")
parser.add_option("", "--omegaScan", default=False, action="store_true")
parser.add_option("", "--segDB2grcDB", default=False, action="store_true")

### misc
#parser.add_option("", "--gracedb-url", default="https://gracedb.ligo.org/api", type="string")

opts, args = parser.parse_args()

opts.notify            = opts.notify            or opts.everything
opts.basic             = opts.basic             or opts.everything
opts.approvalProcessor = opts.approvalProcessor or opts.everything
opts.skymaps           = opts.skymaps           or opts.everything
opts.skymapSummary     = opts.skymapSummary     or opts.everything
opts.bayestar          = opts.bayestar          or opts.everything
opts.bayeswavePE       = opts.bayeswavePE       or opts.everything
opts.cwbPE             = opts.cwbPE             or opts.everything
opts.libPE             = opts.libPE             or opts.everything
opts.lalinf            = opts.lalinf            or opts.everything
opts.dq                = opts.dq                or opts.everything
opts.idq               = opts.idq               or opts.everything
opts.omegaScan         = opts.omegaScan         or opts.everything
opts.segDB2grcDB       = opts.segDB2grcDB       or opts.everything

#-------------------------------------------------

raise NotImplementedError('WRITE ASSERTION STATEMENTS HERE! probably need to rely on lvalertTest to generate lvalert messages for me')

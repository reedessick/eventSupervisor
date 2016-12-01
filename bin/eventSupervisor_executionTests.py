#!/usr/bin/python
usage       = "eventSupervisor_executionTests.py [--options] graceid config"
description = "a script testing event supervisor toolkits' execution"
author      = "reed.essick@ligo.org"

#-------------------------------------------------

import eventSupervisor.eventSupervisor as es           ### import individual QueueItems from es.qid
import eventSupervisor.eventSupervisorUtils as esUtils
import lvalertMP.lvalert.lvalertMPutils as utils

#------------------------

from ligo.gracedb.rest import GraceDb
from ligoTest.gracedb.rest import FakeDb

#------------------------

import os

import logging

import time

from ConfigParser import SafeConfigParser

from optparse import OptionParser

#-------------------------------------------------

def execute( item, cadence=0.1, verbose=False, Verbose=False ):
    """
    executes everything in the item
    """
    while not item.complete: ### until it's done
        while not item.hasExpired(): ### wait until this has expired
            if Verbose:
                print "sleeping for : %.3f sec"%cadence
            time.sleep( cadence )
        item.execute( verbose=verbose ) ### do it

#-------------------------------------------------

parser = OptionParser(usage=usage, description=description)

parser.add_option('-G', '--gracedb_url', default='https://gracedb-test.ligo.org/api/', type='string', help='default=https://gracedb-test.ligo.org/api/')

### how the results are reported
parser.add_option('-w', '--warnings', default=False, action='store_true', help='send email alerts')
parser.add_option('-a', '--annotate', default=False, action='store_true', help='annotate graceDb')

parser.add_option('-v', '--verbose', default=False, action='store_true', help='passed to QueueItem.execute')
parser.add_option('-V', '--Verbose', default=False, action='store_true', help='print out sleep statements while waiting to execute QueueItems. If supplied, also sets --verbose=True')

parser.add_option('-l', '--logDir', default='.', type='string', help='the directory into which log files will be written')
parser.add_option('-L', '--logLevel', default=10, type='int', help='the verbosity level of the logger. Lower numbers mean more output')
parser.add_option('', '--logTag', default='exeTest', type='string')

### options about testing proceedure
parser.add_option('', '--cadence', default=0.1, type='float', help='how long we sleep between checking that QueueItems have expired')

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

### ensure we have the correct arguments
if len(args)!=2:
    raise ValueError('please supply exactly two input arguments\n%s'%usage)
graceid, configname = args

### finish setting up options
opts.verbose = opts.verbose or opts.Verbose

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

### set up logger
### essentially copied from lvalertMP.lvalert.interactiveQueue
if not os.path.exists(opts.logDir):
    os.makedirs( opts.logDir )
logger = logging.getLogger(opts.logTag)
logger.setLevel(opts.logLevel)

logname = utils.genLogname(opts.logDir, 'event_supervisor')

for handler in [logging.FileHandler(logname), logging.StreamHandler()]:
    handler.setFormatter( utils.genFormatter() )
    logger.addHandler( handler )

logger.debug( "writing log into : %s"%logname )

#-------------------------------------------------

### set up standard options for QueueItems
if opts.gracedb_url[:5] == "https": ### assume this is a remote server
    gdb = GraceDb( opts.gracedb_url )
    logger.info( "GraceDb : %s"%opts.gracedb_url )

else:                               ### assume this is a FakeDb directory
    gdb = FakeDb( opts.gracedb_url )
    logger.info( "FakeDb : %s"%opts.gracedb_url )

#-------------------------------------------------

logger.info( "graceid : %s"%graceid )

#-------------------------------------------------

### set up what we feed into the tests

tests = []

if opts.notify:

    ### set up inputs
    alert = {
             'alert_type' : 'new',
             'uid'        : graceid, ### generate an alert from graceid? Should already be a dicitonary by this point...
            }

    #------- Notify
    name = 'notify'
    tests.append( (name, alert) )

#------------------------

if opts.basic:

    ### set up inputs
    event = gdb.event(graceid).json()
    alert = {
             'alert_type' : 'new',
             'uid'        : graceid, ### generate an alert from graceid? Should already be a dicitonary by this point...
             'group'      : event['group'],
             'pipeline'   : event['pipeline'],
            }

    #------- EventCreation
    name = 'event creation'
#    raise NotImplementedError('need to test event creation for each possible pipeline separately')
    """
    EventCreationItem
        cWBTriggerCheck
        oLIBTriggerCheck
        cbcCoincCheck
        cbcPSDCheck
    """
    tests.append( (name, alert) )

    #------- FAR
    name = 'far'
    tests.append( (name, alert) )

    #------- LocalRate
    name = 'local rate'
    tests.append( (name, alert) )

    #------- CreateRate
    name = 'creation rate'
    tests.append( (name, alert) )

    #------- ExternalTriggers
    name = 'external triggers'
    tests.append( (name, alert) )

    #------- UnblindInjections
    name = 'unblind injections'
    tests.append( (name, alert) )

#------------------------

if opts.dq:
    raise NotImplementedError('dq.DQSummaryItem')

    ### set up inputs
    alert = {
             'alert_type' : 'new',
             'uid'        : graceid, ### generate an alert from graceid? Should already be a dicitonary by this point...
            }

    #------- DQSummary
    name = 'lldqReport'
    tests.append( (name, alert) )

#------------------------

if opts.idq:

    ### set up inputs
    alert = {
             'alert_type' : 'new',
             'uid'        : graceid, ### generate an alert from graceid? Should already be a dicitonary by this point...
            }

    #------- IDQStart
    name = 'idq start'
    tests.append( (name, alert) )
    
    ### set up inputs
    ### assume that if this works for H1 it will work for L1
    alert = {
             'alert_type'  : 'update',
             'uid'         : graceid, ### generate an alert from graceid? Should already be a dicitonary by this point...
             'description' : 'Started searching for iDQ information within [xxx, xxx] at H1'
            }

    #------- IDQ
    name = 'idq'
    tests.append( (name, alert) )

#------------------------

if opts.segDB2grcDB:

    ### set up inputs
    alert = {
             'alert_type' : 'new',
             'uid'        : graceid, ### generate an alert from graceid? Should already be a dicitonary by this point...
            }

    #------- SegDB2GrcDBStart
    name = 'segdb2grcdb start'
    tests.append( (name, alert) )

    ### set up inputs
    alert = {
             'alert_type' : 'update',
             'uid'        : graceid, ### generate an alert from graceid? Should already be a dicitonary by this point...
            }

    #------- SegDB2GrcDB
    name = 'segdb2grcdb'
    tests.append( (name, alert) )

#------------------------

if opts.omegaScan: 

#   assume that if H1 works, so will L1?

    ### set up inputs
    alert = {
             'alert_type' : 'new',
             'uid'        : graceid, ### generate an alert from graceid? Should already be a dicitonary by this point...
            }

    #------- OmegaScanStart
    name = 'h1 omega scan start'
    tests.append( (name, alert) )

    ### set up inputs
    alert = {
             'alert_type' : 'update',
             'uid'        : graceid, ### generate an alert from graceid? Should already be a dicitonary by this point...
            }

    #------- OmegaScan
    name = 'h1 omega scan'
    tests.append( (name, alert) )

#------------------------

if opts.skymaps:

    ### set up inputs
    fitsname = [fitsname for fitsname in gdb.files( graceid ).json().keys() if fitsname.endswith('.fits') or fitsname.endswith('.fits.gz')][0]
    alert = {
             'alert_type' : 'update',
             'uid'        : graceid, ### generate an alert from graceid? Should already be a dicitonary by this point...
             'file'       : fitsname,
             'object'     : {'tag_names' : ['sky_loc']}
            }

    #------- SkymapSanity
    name = 'skymap sanity'
    tests.append( (name, alert) )

    #------- PlotSkymap
    name = 'plot skymap'
    tests.append( (name, alert) )

    #------- Skyviewer
    name = 'skyviewer'
    tests.append( (name, alert) )

#------------------------

if opts.skymapSummary:
    raise NotImplementedError('skymapSummary.SkymapSummaryStartItem')

    ### set up inputs
    alert = {
             'alert_type' : 'update',
             'uid'        : graceid, ### generate an alert from graceid? Should already be a dicitonary by this point...
            }

    #------- SkymapSummaryStart
    name = 'skymap summary start'
    tests.append( (name, alert) )

    raise NotImplementedError('skymapSummary.SkymapSummaryItem')

    ### set up inputs
    alert = {
             'alert_type' : 'update',
             'uid'        : graceid, ### generate an alert from graceid? Should already be a dicitonary by this point...
            }

    #------- SkymapSummary
    name = 'skymap summary'
    tests.append( (name, alert) )

#------------------------

if opts.bayestar:

    ### set up inputs
    alert = {
             'alert_type' : 'new',
             'uid':graceid, ### generate an alert from graceid? Should already be a dicitonary by this point...
            }

    #------- BayestarStart
    name = 'bayestar start'
    tests.append( (name, alert) )

    ### set up inputs
    alert = {
             'alert_type' : 'update',
             'uid':graceid, ### generate an alert from graceid? Should already be a dicitonary by this point...
            }

    #------- Bayestar
    name = 'bayestar'
    tests.append( (name, alert) )

#------------------------

if opts.bayeswavePE:

    ### set up inputs
    alert = {
             'alert_type' : 'new',
             'uid'        : graceid, ### generate an alert from graceid? Should already be a dicitonary by this point...
            }

    #------- BayesWavePEStart
    name = 'bayeswave pe start'
    tests.append( (name, alert) )

    ### set up inputs
    alert = {
             'alert_type' : 'update',
             'uid'        : graceid, ### generate an alert from graceid? Should already be a dicitonary by this point...
            }

    #------- BayesWavePE
    name = 'bayeswave pe'
    tests.append( (name, alert) )

#------------------------

if opts.cwbPE:

    ### set up inputs
    alert = {
             'alert_type' : 'new',
             'uid'        : graceid, ### generate an alert from graceid? Should already be a dicitonary by this point...
            }

    #------- CWBPEStart
    name = 'cwb pe start'
#    tests.append( (name, alert) )  ### NOTE: not implemented/does not exist in GraceDb logs

    ### set up inputs
    alert = {
             'alert_type' : 'update',
             'uid'        : graceid, ### generate an alert from graceid? Should already be a dicitonary by this point...
            }

    #------- CWBPE
    name = 'cwb pe'
    tests.append( (name, alert) )

#------------------------

if opts.lalinf:

    ### set up inputs
    alert = {
             'alert_type' : 'new',
             'uid'        : graceid, ### generate an alert from graceid? Should already be a dicitonary by this point...
            }

    #------- LALInfStart
    name = 'lalinf start'
    tests.append( (name, alert) )

    ### set up inputs
    alert = {
             'alert_type' : 'update',
             'uid'        : graceid, ### generate an alert from graceid? Should already be a dicitonary by this point...
            }

    #------- LALInf
    name = 'lalinf'
    tests.append( (name, alert) )

#------------------------

if opts.libPE:

    ### set up inputs
    alert = {
             'alert_type' : 'new',
             'uid'        : graceid, ### generate an alert from graceid? Should already be a dicitonary by this point...
            }

    #------- LIBPEStart
    name = 'lib pe start'
    tests.append( (name, alert) )

    ### set up inputs
    alert = {
             'alert_type' : 'update',
             'uid'        : graceid, ### generate an alert from graceid? Should already be a dicitonary by this point...
            }

    #------- LIBPE
    name = 'lib pe'
    tests.append( (name, alert) )

#------------------------

if opts.approvalProcessor:

    raise NotImplementedError("approvalProcessor.ApprovalProcessorPrelimDQItem")

    ### set up inputs
    alert = {
             'alert_type' : 'new',
             'uid'        : graceid, ### generate an alert from graceid? Should already be a dicitonary by this point...
            }

    #------- ApprovalProcessorPrelimDQ
    name = "approval processor prelim dq"
    tests.append( (name, alert) )

    raise NotImplementedError('approvalProcessor.ApprovalProcessorSegDBItem')

    ### set up inputs
    alert = {
             'alert_type' : 'new',
             'uid'        : graceid, ### generate an alert from graceid? Should already be a dicitonary by this point...
            }

    #------- ApprovalProcessorSegDB
    name = 'approval processor segdb'
    tests.append( (name, alert) )

    raise NotImplementedError('approvalProcessor.ApprovalProcessoriDQItem')

    ### set up inputs
    alert = {
             'alert_type' : 'new',
             'uid'        : graceid, ### generate an alert from graceid? Should already be a dicitonary by this point...
            }

    #------- ApprovalProcessoriDQ
    name = 'approval processor idq'
    tests.append( (name, alert) )

    raise NotImplementedError('approvalProcessor.ApprovalProcessorVOEventItem')

    ### set up inputs
    alert = {
             'alert_type' : 'new',
             'uid'        : graceid, ### generate an alert from graceid? Should already be a dicitonary by this point...
            }

    #------- ApprovalProcessorVOEvent
    name = 'approval processor voevent'
    tasks.append( (name, alert) )

    raise NotImplementedError('approvalProcessor.ApprovalProcessorGCNItem')

    ### set up inputs
    alert = {
             'alert_type' : 'new',
             'uid'        : graceid, ### generate an alert from graceid? Should already be a dicitonary by this point...
            }

    #------- ApprovalProcessorGCN
    name = 'approval processor gcn'
    tests.append( (name, alert) )

#-------------------------------------------------

### load config file
logger.info( "loading config from : %s"%configname )
config = SafeConfigParser()
config.read( configname )

#-------------------

### actually test the items
for name, alert in tests:
    logger.info( "TESTING: %s"%name )

    ### instantiate the item
    item = es.qid[name]( alert, time.time(), dict(config.items(name)), gdb, annotate=opts.annotate, warnings=opts.warnings, logDir=opts.logDir, logTag=opts.logTag )
#    raise NotImplementedError('check object internals')

    execute( item, verbose=opts.verbose, Verbose=opts.Verbose, cadence=opts.cadence )
#    raise NotImplementedError('check object internals')

    logger.info( "TESTING: %s complete"%name )

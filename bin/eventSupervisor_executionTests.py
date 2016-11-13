#!/usr/bin/python
usage       = "eventSupervisor_executionTests.py [--options] graceid"
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

from optparse import OptionParser

#-------------------------------------------------

parser = OptionParser(usage=usage, description=description)

parser.add_option('-G', '--gracedb_url', default='https://gracedb-test.ligo.org/api/', type='string', help='default=https://gracedb-test.ligo.org/api/')

### how the results are reported
parser.add_option('-w', '--warnings', default=False, action='store_true', help='send email alerts')
parser.add_option('-a', '--annotate', default=False, action='store_true', help='annotate graceDb')

parser.add_option('-v', '--verbose', default=False, action='store_true', help='passed to QueueItem.execute')
parser.add_option('-l', '--logDir', default='.', type='string', help='the directory into which log files will be written')
parser.add_option('-L', '--logLevel', default=10, type='int', help='the verbosity level of the logger. Lower numbers mean more output')
parser.add_option('', '--logTag', default='exeTest', type='string')

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
if len(args)!=1:
    raise ValueError('please supply exactly one input argument\n%s'%usage)
graceid = args[0]

### finish setting up options
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

if opts.notify:

    ### set up inputs
    name = 'notify'
    options = {'dt'        : '1.0',
               'ignoreInj' : 'True',
               'by email'  : 'ressick@mit.edu',
               'by sms'    : '',                ### not implemented yet...
               'by phone'  : '',                ### not implemented yet...
               'email'  : 'ressick@mit.edu',
              }
    alert = {'uid':graceid, ### generate an alert from graceid? Should already be a dicitonary by this point...
            }
    t0 = time.time()

    ### instantiate the item
    logger.info( "TESTING: %s"%name )

    item = es.qid['notify']( alert, t0, options, gdb, annotate=opts.annotate, warnings=opts.warnings, logDir=opts.logDir, logTag=opts.logTag )
#    raise NotImplementedError('check internals of object')

    ### execute the item
    while not item.complete: ### iterate until item is complete
        while not item.hasExpired(): ### wait until item has expired
            time.sleep(0.1) ### sleep for 0.1 seconds just to avoid burning out the cpu...

        item.execute( verbose=opts.verbose )
#        raise NotImplementedError('check internals of object')

    logger.info( "TESTING: %s complete"%name )

#------------------------

if opts.basic:
    raise NotImplementedError
    """
    EventCreationItem
        cWBTriggerCheck
        oLIBTriggerCheck
        cbcCoincCheck
        cbcPSDCheck

    FARItem
        FARCheck

    LocalRateItem
        localRateCheck

    CreateRateItem
        createRateCheck

    ExternalTriggersItem
        externalTriggersCheck				*** don't know what it looks like when we do find one...

    UnblindInjectionsItem
        unblindInjectionsCheck				*** unkown statement when there is something there
   							    also, we don't know if this will continue to be done
    """

#------------------------

if opts.approvalProcessor:
    raise NotImplementedError
    """
    ApprovalProcessorPrelimDQItem
        approvalProcessorFARCheck
        approvalProcessorSegDBStartCheck		*** leave unimplemented for the time being
    ApprovalProcessorSegDBItem
        approvalProcessorSegDBFlagsCheck		*** leave unimplemented for the time being
        approvalProcessorSegDBFinishCheck		*** leave unimplemented for the time being
    ApprovalProcessoriDQItem
        approvalProcessoriDQglitchFAPCheck		*** leave unimplemented for the time being
    ApprovalProcessorVOEventItem
        approvalProcessorVOEventCreationCheck		*** leave unimplemented for the time being
        approvalProcessorVOEventDistributionCheck	*** leave unimplemented for the time being
    ApprovalProcessorGCNItem
        approvalProcessorGCNCreationCheck		*** leave unimplemented for the time being
        approvalProcessorGCNDistributionCheck		*** leave unimplemented for the time being

    labeling?						*** leave unimplemented for the time being
    """

#------------------------

if opts.dq:
    raise NotImplementedError
    """
    DQSummaryItem
        dqSummaryCheck					*** don't know what this looks like...
    """

#------------------------

if opts.idq:
    raise NotImplementedError
    """
    IDQStartItem
        idqStartCheck
    IDQItem
        idqGlitchFapCheck
        idqFAPFrameCheck
        idqRankFrameCheck
        idqTimeseriesPlotcheck
        idqActiveChanCheck
        idqActiveChanPlotCheck
        idqTablesCheck
        idqCalibrationCheck
        idqCalibrationPlotCheck
        idqROCCheck
        idqROCPlotCheck
        idqCalibStatsCheck
        idqTrainStatsCheck
        idqFinishCheck
    """

#------------------------

if opts.segDB2grcDB:
    raise NotImplementedError
    """
    SegDB2GrcDBStartItem
        segDB2grcDBStartCheck
    SegDB2GrcDBItem
        segDB2grcDBFlagsCheck				
        segDB2grcDBVetoDefCheck				*** leave this unimplemented for the moment
        segDB2grcDBAnyCheck				
        segDB2grcDBFinishCheck
    """

#------------------------

if opts.omegaScan:
    raise NotImplementedError
    """
    OmegaScanStartItem
        omegaScanStartCheck				
    OmegaScanItem
        omegaScanDataCheck				
        omegaScanFinishCheck				
    """

#------------------------

if opts.skymaps:
    raise NotImplementedError
    """
    SkymapSanityItem
        skymapSanityCheck
    PlotSkymapItem
        plotSkymapCheck
    SkyviewerItem
        skyviewerCheck
    """

#------------------------

if opts.skymapSummary:
    raise NotImplementedError
    """
    SkymapSummaryStartItem
        skymapSummaryStartCheck				*** leave this unimplemented until new skymapSummaries are running
    SkymapSummaryItem
        skymapSummaryDatacheck 				*** leave this unimplemented until new skymapSummaries are running
        skymapSummaryFinishCheck			*** leave this unimplemented until new skymapSummaries are running
    """

#------------------------

if opts.bayestar:
    raise NotImplementedError
    """
    BayestarStartItem
        bayestarStartCheck
    BayestarItem
        bayestarSkymapCheck
        bayestarFinishCheck
    """

#------------------------

if opts.bayeswavePE:
    raise NotImplementedError
    """
    BayesWavePEStartItem
        bayeswavePEStartCheck
    BayesWavePEItem
        bayeswavePEPostSampCheck
        bayeswavePEEstimateCheck
        bayeswavePEBayesFactorsCheck
        bayeswavePESkymapCheck
        bayeswavePEFinishCheck				*** no known statement? May not be reported by the pipeline?
    """

#------------------------

if opts.cwbPE:
    raise NotImplementedError
    """
    CWBPEStartItem
        cWBPEStartCheck					*** no statement may exist?
    CWBPEItem
        cWBPECEDCheck
        cWBPEEstimateCheck
        cWBPESkymapCheck
        cWBPEFinishCheck				*** no statement may exist?
    """

#------------------------

if opts.lalinf:
    raise NotImplementedError
    """
    LALInfStartItem
        lalinfStartCheck
    LALInfItem
        lalinfPostSampCheck				*** no known statement?
        lalinfSkymapCheck
        lalinfFinishCheck
    """

#------------------------

if opts.libPE:
    raise NotImplementedError
    """
    LIBPEStartItem
        libPEStartCheck
    LIBPEItem
        libPEPostSampCheck
        libPEBayesFactors
        libPESkymapCheck
        libPEFinishCheck
    """

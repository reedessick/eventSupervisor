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

import time

from ligo.gracedb.rest import GraceDb

from optparse import OptionParser

#-------------------------------------------------

parser = OptionParser(usage=usage, description=description)

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

### misc
parser.add_option("", "--gracedb-url", default="https://gracedb.ligo.org/api", type="string")

opts, args = parser.parse_args()

### set up standard options for QueueItems
gdb = GraceDb( opts.gracedb_url )
annotate = False

#-------------------------------------------------

### want to test the instantiation of all QueueItems and their associated Tasks
### we should be able to get away with this simply by instantiating the QueueItems and then asserting that their attributes are as expected
###   -> some of those attributes are Tasks, which we can then check iteratively

### Item instantiation follows : (alert, t0, options, gdb, annotate=annotate)

#-------------------------------------------------

### notify
if opts.notify:
    print "testing notify/notify.py"
    raise NotImplemented

    ### set up options
    alert = {
        'uid':'FakeEvent'
        }
    t0 = time.time()
 
    options = {
        'dt'       : '10.0',
        'ignorInj' : 'True',
        'by email' : '',
        'by sms'   : '',
        'by phone' : '',
        }

    ### instantiate Item
    item = notify.NotifyItem( alert, t0, options, gdb, annotate=annotate )

    ### assert stuff about Items
    ### notify item
    ###   notifyByEmail
    ###   notifyBySMS
    ###   notifyByPhone

    ### actually run the execute() method for the Item and the Tasks and check how everything ticks through?

### basic
if opts.basic:
    print "testing basic/basic.py"
    raise NotImplemented
    ### EventCreationItem
    ###   cWBTriggerCheck
    ###   oLIBTriggercheck
    ###   cbcCoincCheck
    ###   cbcPSDCheck
    ### CreateRateItem
    ###   createRateCheck
    ### LocalRateItem
    ###   localRateCheck
    ### FARItem
    ###   FARCheck
    ### ExternalTriggersItem
    ###   externalTriggersCheck
    ###   unblindInjectionsCheck

if opts.approvalProcessor:
    print "testing basic/approvalProcessor.py"
    raise NotImplemented
    ### ApprovalProcessorPrelimDQItem
    ###   approvalProcessorFARCheck
    ###   approvalProcessorSegDBStartCheck
    ### ApprovalProcessorSegDBItem
    ###   approvalProcessorFlagsCheck
    ###   approvalProcessorFinishCheck
    ### ApprovalProcessoriDQItem
    ###   approvalProcessoriDQglitchFAPCheck
    ### ApprovalProcessorVOEventItem
    ###   approvalProcessorVOEventCreationCheck
    ###   approvalProcessorVOEventDistributionCheck
    ### ApprovalProcessorGCNCheck
    ###   approvalProcessorGCNCreationCheck
    ###   approvalProcessorGCNDistributionCheck

### skymaps
if opts.skymaps:
    print "testing skymaps/skymaps.py"
    raise NotImplemented
    ### SkumapSanityItem
    ###   skymapSanityCheck
    ### PlotSkymapItem
    ###   plotSkymapCheck
    ### SkyviewerItem
    ###   skyviewerCheck

if opts.skymapSummary:
    print "testing skymaps/skymapSummary.py"
    raise NotImplemented
    ### SkymapSummaryStartItem
    ###   skymapSummaryStartCheck
    ### SkymapSummaryItem
    ###   skymapSummaryDataCheck
    ###   skymapSummaryFinishCheck

### pe
if opts.bayestar:
    print "testing pe/bayestar.py"
    raise NotImplemented
    ### BaystarStartItem
    ###   bayestarStartCheck
    ### BayestarItem
    ###   bayestarSkymapCheck
    ###   bayestarFinishItem

if opts.bayeswavePE:
    print "testing pe/bayeswavePE.py"
    raise NotImplemented
    ### BayesWavePEStartItem
    ###   bayeswavePEStartCheck
    ### BayesWavePEItem
    ###   bayeswavePEPostSampCheck
    ###   bayeswavePEBayesFactorsCheck
    ###   bayeswavePEEstimateCheck
    ###   bayeswavePESkymapCheck
    ###   bayeswavePEFinishCheck

if opts.cwbPE:
    print "testing pe/cwbPE.py"
    raise NotImplemented
    ### note, start and finish checks don't really make sense given the way cWB uploads data
    ### CWBPEItem
    ###   cWBCEDCheck
    ###   cWBPEEstimateCheck
    ###   cWBPESkymapCheck

if opts.libPE:
    print "testing pe/libPE.py"
    raise NotImplemented
    ### LIBPEStartItem
    ###   libPEStartCheck
    ### LIBPEItem
    ###   libPEBayesFactorsCheck
    ###   libPEPostSampCheck
    ###   libPESkymapCheck
    ###   libPEFinishCheck

if opts.lalinf:
    print "testing pe/lalinf.py"
    raise NotImplemented
    ### LALInfStartItem
    ###   lalinfStartCheck
    ### LALInfItem
    ###   lalinfPostSampCheck
    ###   lalinfSkymapCheck
    ###   lalinfFinishCheck

### dq
if opts.dq:
    print "testing dq/dq.py"
    raise NotImplemented
    ### DQSummaryItem
    ###   dqSummaryCheck

if opts.idq:
    print "testing dq/idq.py"
    raise NotImplemented
    ### IDQStartItem
    ###   idqStartCheck
    ### IDQItem
    ###   idqGltichFAPCheck
    ###   idqFAPFrameCheck
    ###   idqRankFrameCheck
    ###   idqTimeseriesPlotCheck
    ###   idqActiveChanCheck
    ###   idqActiveChanPlotCheck
    ###   idqTablesCheck
    ###   idqCalibrationCheck
    ###   idqCalibrationPlotCheck
    ###   idqROCCheck
    ###   idqROCPlotCheck
    ###   idqCalibStatsCheck
    ###   idqTranStatsCheck

if opts.omegaScan:
    print "testing dq/omegaScan.py"
    raise NotImplemented
    ### HofTOmegaScanStartItem
    ###   omegaScanStartCheck
    ### AuxOmegaScanStartItem
    ###   omegaScanStartCheck
    ### IDQOmegaScanStartItem
    ###   omegaScanStartCheck
    ### HofTOmegaScanItem
    ###   omegaScanDataCheck
    ###   omegaScanFinishCheck
    ### AuxOmegaScanItem
    ###   omegaScanDataCheck
    ###   omegaScanFinishCheck
    ### IDQOmegaScanItem
    ###   omegaScanDataCheck
    ###   omegaScanFinishCheck

if opts.segDB2grcDB:
    print "testing dq/segDB2grcDB"
    raise NotImplemented
    ### SegDB2GrcDBStartItem
    ###   segDB2grcDBStartCheck
    ### SegDB2GrceDBItem
    ###   segDB2grcDBFlagsCheck
    ###   segDB2grcDBVetoDefCheck
    ###   segDB2grcDBAnyCheck
    ###   segDB2grcDBFinishCheck

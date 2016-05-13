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

from optparse import OptionParser

#-------------------------------------------------

parser = OptionParser(usage=usage, description=description)

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

### set up standard options for QueueItems

#from ligo.gracedb.rest import GraceDb
#gdb = GraceDb( opts.gracedb_url )
gdb = None

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

    #--------------------
    # NotifyItem
    #--------------------
    print "    NotifyItem"

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid
        }
    t0 = time.time()
    options = {
        'dt'       : '10.0',
        'ignoreInj' : 'True',
        'by email' : 'a',
        'by sms'   : 'b c',
        'by phone' : 'd e f',
        }

    ### instantiate Item
    item = notify.NotifyItem( alert, t0, options, gdb, annotate=annotate )

    ### assert stuff about Items
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 3 )
    assert( len(item.completedTasks) == 0 ) 
    
    tasks = dict( (task.name, task) for task in item.tasks )
    byEmail = tasks['notifyByEmail']
    bySMS   = tasks['notifyBySMS']
    byPhone = tasks['notifyByPhone']

    assert( byEmail.notificationList == ['a'] )
    assert( byEmail.expiration == t0+10.0 )

    assert( bySMS.notificationList == ['b', 'c'] )
    assert( bySMS.expiration == t0+10.0 )

    assert( byPhone.notificationList == ['d', 'e', 'f'] )
    assert( byPhone.expiration == t0+10.0 )

    ### actually run the execute() method for the Item and the Tasks and check how everything ticks through?
    print "    WARNING: notify Task.execute() not implemented and not tested"
#    raise NotImplementedError("actually test Task.execute() for this Item")
    
    print "    notify.py passed all tests sucessfully!"

#-------------------------------------------------

### basic
if opts.basic:
    print "testing basic/basic.py"
    raise NotImplementedError

    #--------------------
    # EventCreationItem
    #--------------------
    print "EventCreationItem"

    graceid = 'FakeEvent'
    pipeline = 'cwb'
    alert = {
        'uid' : graceid,
        'pipeline' : 'pipeline',
        }
    t0 = time.time()
    options = {
        'dt' : '10.0',
        'email' : 'a',
        }

    item = basic.EventCreationItem( alert, t0, options, gdb, annotate=annotate )

    ### EventCreationItem
    ###   cWBTriggerCheck
    ###   oLIBTriggercheck
    ###   cbcCoincCheck
    ###   cbcPSDCheck

    #--------------------
    # NotifyItem
    #--------------------
    print "CreateRateItem"

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid
        }
    t0 = time.time()
    options = {
        'dt'   : '10.0',
        'win+' : '5.0',
        'win-' : '5.0',
        'mas rate' : 2.0,
        'email' : 'a',
        }

    item = basic.CreateRateItem( alert, t0, options, gdb, annotate=annotate )
    ### CreateRateItem
    ###   createRateCheck

    #--------------------
    # NotifyItem
    #--------------------
    print "LocalRateItem"

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid
        }
    t0 = time.time()
    options = {
        'dt'   : '10.0',
        'win+' : '5.0',
        'win-' : '5.0',
        'mas rate' : 2.0,
        'email' : 'a',
        }

    item = basic.LocalRateItem( alert, t0, options, gdb, annotate=annotate )
    ### LocalRateItem
    ###   localRateCheck

    #--------------------
    # NotifyItem
    #--------------------
    print "FARItem"

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid
        }
    t0 = time.time()
    options = {
        'dt'   : '10.0',
        'min far' : '5.0',
        'max far' : '5.0',
        'email' : 'a',
        }

    item = basic.FARItem( alert, t0, options, gdb, annotate=annotate )
    ### FARItem
    ###   FARCheck

    #--------------------
    # NotifyItem
    #--------------------
    print "ExternalTriggersItem"

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid
        }
    t0 = time.time()
    options = {
        'dt'   : '10.0',
        'email' : 'a',
        }

    item = basic.ExternalTriggersItem( alert, t0, options, gdb, annotate=annotate )
    ### ExternalTriggersItem
    ###   externalTriggersCheck

    #--------------------
    # UnblindInjectionsItem
    #--------------------
    print "UnblindInjectionsItem"

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid
        }
    t0 = time.time()
    options = {
        'dt'   : '10.0',
        'email' : 'a',
        }

    item = basic.UnblindInjectionsItem( alert, t0, options, gdb, annotate=annotate )
    ### UnblindInjectionsItem
    ###   unblindInjectionsCheck

#-------------------------------------------------

if opts.approvalProcessor:
    print "testing basic/approvalProcessor.py"
    raise NotImplemented

    #--------------------
    # ApprovalProcessroPrelimDQItem
    #--------------------
    print "ApprovalProcessorPrelimDQItem"

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid
        }
    t0 = time.time()
    options = {
        'far dt'   : '10.0',
        'seg start dt'   : '10.0',
        'email' : 'a',
        }

    item = approvalProcessor.ApprovalProcessorPrelimDQItem( alert, t0, options, gdb, annotate=annotate )
    ### ApprovalProcessorPrelimDQItem
    ###   approvalProcessorFARCheck
    ###   approvalProcessorSegDBStartCheck

    #--------------------
    # ApprovalProcessorSegDBItem
    #--------------------
    print "ApprovalProcessorSegDBItem"

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid
        }
    t0 = time.time()
    options = {
        'flags dt' : '10.0',
        'flags' : 'H1:DMT-ANALYSIS_READY:1',
        'finish dt' : '10.0',
        'email' : 'a',
        }

    item = approvalProcessor.ApprovalProcessorSegDBItem( alert, t0, options, gdb, annotate=annotate )
    ### ApprovalProcessorSegDBItem
    ###   approvalProcessorFlagsCheck
    ###   approvalProcessorFinishCheck

    #--------------------
    # ApprovalProcessoriDQItem
    #--------------------
    print "ApprovalProcessoriDQItem"

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid
        }
    t0 = time.time()
    options = {
        'dt'   : '10.0',
        'ifos' : 'H L',
        'email' : 'a',
        }

    item = approvalProcessor.ApprovalProcessoriDQItem( alert, t0, options, gdb, annotate=annotate )
    ### ApprovalProcessoriDQItem
    ###   approvalProcessoriDQglitchFAPCheck

    #--------------------
    # ApprovalProcessroVOEventItem
    #--------------------
    print "ApprovalProcessorVOEventItem"

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid
        }
    t0 = time.time()
    options = {
        'dt'   : '10.0',
        'email' : 'a',
        }

    item = approvalProcessor.ApprovalProcessorVOEventItem( alert, t0, options, gdb, annotate=annotate )
    ### ApprovalProcessorVOEventItem
    ###   approvalProcessorVOEventCreationCheck
    ###   approvalProcessorVOEventDistributionCheck

    #--------------------
    # ApprovalProcessorGCNItem
    #--------------------
    print "ApprovalProcessorGCNItem"

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid
        }
    t0 = time.time()
    options = {
        'dt'   : '10.0',
        'email' : 'a',
        }

    item = approvalProcessor.ApprovalProcessorGCNItem( alert, t0, options, gdb, annotate=annotate )
    ### ApprovalProcessorGCNCheck
    ###   approvalProcessorGCNCreationCheck
    ###   approvalProcessorGCNDistributionCheck

#-------------------------------------------------

### skymaps
if opts.skymaps:
    print "testing skymaps/skymaps.py"
    raise NotImplemented

    #--------------------
    # SkymapSanityItem
    #--------------------
    print "SkymapSanityItem"

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid
        }
    t0 = time.time()
    options = {
        'dt'   : '10.0',
        'email' : 'a',
        }

    item = skymaps.SkymapSanityItem( alert, t0, options, gdb, annotate=annotate )
    ### SkumapSanityItem
    ###   skymapSanityCheck

    #--------------------
    # PlotSkymapItem
    #--------------------
    print "PlotSkymapItem"

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid
        }
    t0 = time.time()
    options = {
        'dt'   : '10.0',
        'email' : 'a',
        }

    item = skymaps.PlotSkymapItem( alert, t0, options, gdb, annotate=annotate )
    ### PlotSkymapItem
    ###   plotSkymapCheck

    #--------------------
    # SkyviewerItem
    #--------------------
    print "SkyviewerItem"

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid
        }
    t0 = time.time()
    options = {
        'dt'   : '10.0',
        'email' : 'a',
        }

    item = skymaps.SkyviewerItem( alert, t0, options, gdb, annotate=annotate )
    ### SkyviewerItem
    ###   skyviewerCheck

#-------------------------------------------------

if opts.skymapSummary:
    print "testing skymaps/skymapSummary.py"
    raise NotImplemented

    #--------------------
    # SkymapSummaryStartItem
    #--------------------
    print "SkymapSummaryStartItem"

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid
        }
    t0 = time.time()
    options = {
        'dt'   : '10.0',
        'email' : 'a',
        }

    item = skymapsSummary.SkymapSummaryStartItem( alert, t0, options, gdb, annotate=annotate )
    ### SkymapSummaryStartItem
    ###   skymapSummaryStartCheck

    #--------------------
    # SkymapSummaryItem
    #--------------------
    print "SkymapSummaryItem"

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid
        }
    t0 = time.time()
    options = {
        'dt'   : '10.0',
        'email' : 'a',
        }

    item = skymapsSummary.SkymapSummaryItem( alert, t0, options, gdb, annotate=annotate )
    ### SkymapSummaryItem
    ###   skymapSummaryDataCheck
    ###   skymapSummaryFinishCheck

#-------------------------------------------------

### pe
if opts.bayestar:
    print "testing pe/bayestar.py"
    raise NotImplemented

    #--------------------
    # BayestarStartItem
    #--------------------
    print "BayestarStartItem"

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid
        }
    t0 = time.time()
    options = {
        'dt'   : '10.0',
        'email' : 'a',
        }

    item = bayestar.BayestarStartItem( alert, t0, options, gdb, annotate=annotate )
    ### BaystarStartItem
    ###   bayestarStartCheck

    #--------------------
    # BayestarItem
    #--------------------
    print "BayestarItem"

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid
        }
    t0 = time.time()
    options = {
        'skymap dt'   : '10.0',
        'skymap tagnames'   : 'sky_loc lvem',
        'email' : 'a',
        }

    item = bayestar.BayestarItem( alert, t0, options, gdb, annotate=annotate )
    ### BayestarItem
    ###   bayestarSkymapCheck
    ###   bayestarFinishItem

#-------------------------------------------------

if opts.bayeswavePE:
    print "testing pe/bayeswavePE.py"
    raise NotImplemented

    #--------------------
    # BayesWavePEStartItem
    #--------------------
    print "BayesWavePEStartItem"

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid
        }
    t0 = time.time()
    options = {
        'dt'   : '10.0',
        'email' : 'a',
        }

    item = bayeswavePE.BayesWavePEStartItem( alert, t0, options, gdb, annotate=annotate )
    ### BayesWavePEStartItem
    ###   bayeswavePEStartCheck

    #--------------------
    # BayesWavePEItem
    #--------------------
    print "BayesWavePEItem"

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid
        }
    t0 = time.time()
    options = {
        'post samp dt'   : '10.0',
        'estimate dt' : '10.0',
        'bayes factor dt' : '10.0',
        'skymap dt' : '10.0',
        'skymap tagnames' : 'sky_loc',
        'email' : 'a',
        }

    item = bayeswavePE.BayesWavePEItem( alert, t0, options, gdb, annotate=annotate )
    ### BayesWavePEItem
    ###   bayeswavePEPostSampCheck
    ###   bayeswavePEBayesFactorsCheck
    ###   bayeswavePEEstimateCheck
    ###   bayeswavePESkymapCheck
    ###   bayeswavePEFinishCheck

#-------------------------------------------------

if opts.cwbPE:
    print "testing pe/cwbPE.py"
    raise NotImplemented
    ### note, start and finish checks don't really make sense given the way cWB uploads data

    #--------------------
    # CWBPEItem
    #--------------------
    print "CWBPEItem"

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid
        }
    t0 = time.time()
    options = {
        'ced dt'   : '10.0',
        'estimate dt' : '10.0',
        'skymap dt' : '10.0',
        'skymap tagnames' : 'sky_loc lvem',
        'email' : 'a',
        }

    item = cwbPE.CWBPEItem( alert, t0, options, gdb, annotate=annotate )
    ### CWBPEItem
    ###   cWBCEDCheck
    ###   cWBPEEstimateCheck
    ###   cWBPESkymapCheck

#-------------------------------------------------

if opts.libPE:
    print "testing pe/libPE.py"
    raise NotImplemented

    #--------------------
    # LIBPEStartItem
    #--------------------
    print "LIBPEStartItem"

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid
        }
    t0 = time.time()
    options = {
        'dt'   : '10.0',
        'email' : 'a',
        }

    item = libPE.LIBPEStartItem( alert, t0, options, gdb, annotate=annotate )
    ### LIBPEStartItem
    ###   libPEStartCheck

    #--------------------
    # LIBPEItem
    #--------------------
    print "LIBPEItem"

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid
        }
    t0 = time.time()
    options = {
        'post samp dt'   : '10.0',
        'bayesFct dt' : '10.0',
        'skymap dt' : '10.0',
        'skymap tagnames' : 'sky_loc lvem',
        'finish dt' : '10.0',
        'email' : 'a',
        }

    item = libPE.LIBPEItem( alert, t0, options, gdb, annotate=annotate )
    ### LIBPEItem
    ###   libPEBayesFactorsCheck
    ###   libPEPostSampCheck
    ###   libPESkymapCheck
    ###   libPEFinishCheck

#-------------------------------------------------

if opts.lalinf:
    print "testing pe/lalinf.py"
    raise NotImplemented

    #--------------------
    # LALInfStartItem
    #--------------------
    print "LALInfStartItem"

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid
        }
    t0 = time.time()
    options = {
        'dt'   : '10.0',
        'email' : 'a',
        }

    item = lalinf.LALInfStartItem( alert, t0, options, gdb, annotate=annotate )
    ### LALInfStartItem
    ###   lalinfStartCheck

    #--------------------
    # LALInfItem
    #--------------------
    print "LALInfItem"

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid
        }
    t0 = time.time()
    options = {
        'post samp dt'   : '10.0',
        'skymap dt' : '10.0',
        'skymap tagnames' : 'sky_loc lvem',
        'finish dt' : '10.0',
        'email' : 'a',
        }

    item = lalinf.LALInfItem( alert, t0, options, gdb, annotate=annotate )
    ### LALInfItem
    ###   lalinfPostSampCheck
    ###   lalinfSkymapCheck
    ###   lalinfFinishCheck

#-------------------------------------------------

### dq
if opts.dq:
    print "testing dq/dq.py"
    raise NotImplemented

    #--------------------
    # DQSummaryItem
    #--------------------
    print "DQSummaryItem"

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid
        }
    t0 = time.time()
    options = {
        'dt'   : '10.0',
        'email' : 'a',
        }

    item = dq.DQSummaryItem( alert, t0, options, gdb, annotate=annotate )
    ### DQSummaryItem
    ###   dqSummaryCheck

#-------------------------------------------------

if opts.idq:
    print "testing dq/idq.py"
    raise NotImplemented

    #--------------------
    # IDQStartItem
    #--------------------
    print "IDQStartItem"

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid
        }
    t0 = time.time()
    options = {
        'dt'   : '10.0',
        'ifos' : 'H L',
        'email' : 'a',
        }

    item = idq.IDQStartItem( alert, t0, options, gdb, annotate=annotate )
    ### IDQStartItem
    ###   idqStartCheck

    #--------------------
    # IDQItem
    #--------------------
    print "IDQItem"

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid
        }
    t0 = time.time()
    options = {
        'tables dt' : '10.0',
        'glitch fap dt' : '10.0',
        'fap frame dt' : '30.0',
        'rank frame dt' : '50.0',
        'timeseries plot dt' : '60.0',
        'active chan dt' : '70.0',
        'active chan plot dt' : '80.0',
        'calib dt' : '90.0',
        'calib plot dt' : '100.0',
        'roc dt' : '110.0',
        'roc plot dt' : '120.0',
        'calib stats dt' : '140.0',
        'train stats dt' : '150.0',
        'finish dt' : '160.0',
        'classifiers' : 'ovl B',
        'email' : 'a',
        }

    item = idq.IDQItem( alert, t0, options, gdb, annotate=annotate )
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

#-------------------------------------------------

if opts.omegaScan:
    print "testing dq/omegaScan.py"
    raise NotImplemented

    #--------------------
    # HofTOmegaScanStartItem
    #--------------------
    print "HofTOmegaScanStartItem"

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid
        }
    t0 = time.time()
    options = {
        'dt'   : '10.0',
        'ifos' : 'H L',
        'email' : 'a',
        }

    item = omegaScan.HofTOmegaScanStartItem( alert, t0, options, gdb, annotate=annotate )
    ### HofTOmegaScanStartItem
    ###   omegaScanStartCheck

    #--------------------
    # HofTOmegaScanItem
    #--------------------
    print "HofTOmegaScanItem"

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid
        }
    t0 = time.time()
    options = {
        'data dt'   : '10.0',
        'finish dt' : '10.0',
        'email' : 'a',
        }

    item = omegaScan.HofTOmegaScanItem( alert, t0, options, gdb, annotate=annotate )
    ### HofTOmegaScanItem
    ###   omegaScanDataCheck
    ###   omegaScanFinishCheck

    #--------------------
    # AuxOmegaScanStartItem
    #--------------------
    print "AuxOmegaScanStartItem"

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid
        }
    t0 = time.time()
    options = {
        'data dt'   : '10.0',
        'finish dt' : '10.0',
        'email' : 'a',
        }

    item = omegaScan.AuxOmegaScanStartItem( alert, t0, options, gdb, annotate=annotate )
    ### AuxOmegaScanStartItem
    ###   omegaScanStartCheck

    #--------------------
    # AuxOmegaScanItem
    #--------------------
    print "AuxOmegaScanItem"

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid
        }
    t0 = time.time()
    options = {
        'dt'   : '10.0',
        'ifos' : 'H L',
        'email' : 'a',
        }

    item = omegaScan.AuxOmegaScanItem( alert, t0, options, gdb, annotate=annotate )
    ### AuxOmegaScanItem
    ###   omegaScanDataCheck
    ###   omegaScanFinishCheck

    #--------------------
    # IDQOmegaScanStartItem
    #--------------------
    print "IDQOmegaScanStartItem"

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid
        }
    t0 = time.time()
    options = {
        'dt'   : '10.0',
        'email' : 'a',
        }

    item = omegaScan.IDQOmegaScanStartItem( alert, t0, options, gdb, annotate=annotate )
    ### IDQOmegaScanStartItem
    ###   omegaScanStartCheck

    #--------------------
    # IDQOmegaScanItem
    #--------------------
    print "IDQOmegaScanItem"

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid
        }
    t0 = time.time()
    options = {
        'data dt'   : '10.0',
        'finish dt' : '10.0',
        'email' : 'a',
        }

    item = omegaScan.IDQOmegaScanItem( alert, t0, options, gdb, annotate=annotate )
    ### IDQOmegaScanItem
    ###   omegaScanDataCheck
    ###   omegaScanFinishCheck

#-------------------------------------------------

if opts.segDB2grcDB:
    print "testing dq/segDB2grcDB"
    raise NotImplemented

    #--------------------
    # SegDB2GrcDBStartItem
    #--------------------
    print "SegDB2GrcDBStartItem"

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid
        }
    t0 = time.time()
    options = {
        'dt'   : '10.0',
        'email' : 'a',
        }

    item = segDB2grcDB.SegDB2GrcDBStartItem( alert, t0, options, gdb, annotate=annotate )
    ### SegDB2GrcDBStartItem
    ###   segDB2grcDBStartCheck

    #--------------------
    # SegDB2GrcDBItem
    #--------------------
    print "SegDB2GrcDBItem"

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid
        }
    t0 = time.time()
    options = {
        'flags dt'   : '10.0',
        'flags' : 'H1:DMT-ANALYSIS_READY:1',
        'vetoDef dt'   : '10.0',
        'vet def' : '',
        'any dt'   : '10.0',
        'finish dt' : '10.0',
        'email' : 'a',
        }

    item = segDB2grcDBItem( alert, t0, options, gdb, annotate=annotate )
    ### SegDB2GrceDBItem
    ###   segDB2grcDBFlagsCheck
    ###   segDB2grcDBVetoDefCheck
    ###   segDB2grcDBAnyCheck
    ###   segDB2grcDBFinishCheck

#!/usr/bin/python
usage       = "eventSupervisorTesting.py [--options]"
description = "a script testing whether event supervisor objects are instantiated as expected"
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
from eventSupervisor.pe import embright
from eventSupervisor.pe import bayeswavePE
from eventSupervisor.pe import cwbPE
from eventSupervisor.pe import libPE
from eventSupervisor.pe import lalinf

from eventSupervisor.dq import dq
from eventSupervisor.dq import idq
from eventSupervisor.dq import omegaScan
from eventSupervisor.dq import segDB2grcDB

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
parser.add_option("", "--embright", default=False, action="store_true")
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
opts.embright          = opts.embright          or opts.everything
opts.bayeswavePE       = opts.bayeswavePE       or opts.everything
opts.cwbPE             = opts.cwbPE             or opts.everything
opts.libPE             = opts.libPE             or opts.everything
opts.lalinf            = opts.lalinf            or opts.everything
opts.dq                = opts.dq                or opts.everything
opts.idq               = opts.idq               or opts.everything
opts.omegaScan         = opts.omegaScan         or opts.everything
opts.segDB2grcDB       = opts.segDB2grcDB       or opts.everything

### set up standard options for QueueItems
#from ligo.gracedb.rest import GraceDb
#gdb = GraceDb( opts.gracedb_url )
gdb = None

annotate = False

#-------------------------------------------------

if opts.notify:
    print "testing notify/notify.py"

    #--------------------
    # NotifyItem
    #--------------------
    print "    NotifyItem"

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid,
        'object' : {'group'    : 'a',
                    'pipeline' : 'b',
                   },
        }
    t0 = time.time()
    options = {
        'dt'       : '10.0',
        'ignore inj' : 'True',
        'by email' : 'a',
#        'by sms'   : 'b c',    ### NOTE: not currently implemented
#        'by phone' : 'd e f',  ### NOTE: not currently implemented
        'email' : 'g',
        }

    ### instantiate Item
    item = notify.NotifyItem( alert, t0, options, gdb, annotate=annotate )

    ### assert stuff about Items
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 1 ) ### NOTE: only using 'by email' right now...
    assert( len(item.completedTasks) == 0 ) 
    assert( item.expiration == t0+10.0 )

    ### asser stuff about Tasks    
    tasks = dict( (task.name, task) for task in item.tasks )

    byEmail = tasks['notifyByEmail']
    assert( byEmail.notificationList == ['a'] )
    assert( byEmail.expiration == t0+10.0 )

#    bySMS   = tasks['notifyBySMS']
#    assert( bySMS.notificationList == ['b', 'c'] )
#    assert( bySMS.expiration == t0+10.0 )

#    byPhone = tasks['notifyByPhone']
#    assert( byPhone.notificationList == ['d', 'e', 'f'] )
#    assert( byPhone.expiration == t0+10.0 )

    ### actually run the execute() method for the Item and the Tasks and check how everything ticks through?
    print "        WARNING: notifyCheck Task.execute() not implemented and not tested"
#    raise NotImplementedError("actually test Task.execute() for this Item")
    
    print "    notify.py passed all tests sucessfully!"

#-------------------------------------------------

if opts.basic:
    print "testing basic/basic.py"

    #--------------------
    # EventCreationItem
    #--------------------
    print "    EventCreationItem"

    ### cwb
    graceid = 'FakeEvent'
    pipeline = 'cwb'
    alert = {
        'uid' : graceid,
        'pipeline' : pipeline,
        }
    t0 = time.time()
    options = {
        'dt' : '10.0',
        'email' : 'a',
        }

    item = basic.EventCreationItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 1 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+10.0 )

    ###   cWBTriggerCheck
    task = item.tasks[0]
    assert( task.expiration == t0+10.0 )
    assert( task.email == ['a'] )

    print "        WARNING: cWBTriggerCheck Task.execute() not implemented and not tested"
#    raise NotImplementedError("actually test Task.execute() for this Item")

    ### olib
    graceid = 'FakeEvent'
    pipeline = 'lib'
    alert = {
        'uid' : graceid,
        'pipeline' : pipeline,
        }
    t0 = time.time()
    options = {
        'dt' : '10.0',
        'email' : 'a',
        }

    item = basic.EventCreationItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 1 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+10.0 )

    ###   oLIBTriggercheck
    task = item.tasks[0]
    assert( task.expiration == t0+10.0 )
    assert( task.email == ['a'] )

    print "        WARNING: oLIBTriggerCheck Task.execute() not implemented and not tested"
#    raise NotImplementedError("actually test Task.execute() for this Item")

    ### gstlal
    for pipeline in ['gstlal', 'mbtaonline', 'pycbc']:
        graceid = 'FakeEvent'
        alert = {
            'uid' : graceid,
            'pipeline' : pipeline,
            }
        t0 = time.time()
        options = {
            'dt' : '10.0',
            'email' : 'a',
            }

        item = basic.EventCreationItem( alert, t0, options, gdb, annotate=annotate )
        assert( item.graceid == graceid )
        assert( item.annotate == annotate )
        assert( item.complete == False )
        assert( len(item.tasks) == 2 )
        assert( len(item.completedTasks) == 0 )
        assert( item.expiration == t0+10.0 )

        tasks = dict( (task.name, task) for task in item.tasks )
        coinc = tasks['cbcCoinc']
        psd   = tasks['cbcPSD']
        ###   cbcCoincCheck
        assert( coinc.expiration == t0+10.0 )
        assert( coinc.email == ['a'] )
        print "        WARNING: cbcCoincCheck Task.execute() not implemented and not tested"

        ###   cbcPSDCheck
        assert( psd.expiration == t0+10.0 )
        assert( psd.email == ['a'] )
        print "        WARNING: cbcPSDCheck Task.execute() not implemented and not tested"

    #--------------------
    # CreateRateItem
    #--------------------
    print "    CreateRateItem"

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid,
        'pipeline': 'pipeline',
        'group' : 'group',
        'search' : 'search',
        }
    t0 = time.time()
    options = {
        'dt'   : '10.0',
        'win+' : '5.0',
        'win-' : '5.0',
        'max rate' : 2.0,
        'email' : 'a',
        }

    item = basic.CreateRateItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 1 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+10.0 )

    ### createRateCheck
    task = item.tasks[0]
    assert( task.pipeline == "pipeline" )
    assert( task.group == "group" )
    assert( task.search == "search" )
    assert( task.expiration == t0+10.0 )
    assert( task.email == ["a"] )

    ### check again when search is not specified
    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid,
        'pipeline': 'pipeline',
        'group' : 'group',
        }
    t0 = time.time()
    options = {
        'dt'   : '10.0',
        'win+' : '5.0',
        'win-' : '5.0',
        'max rate' : 2.0,
        'email' : 'a',
        }

    item = basic.CreateRateItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 1 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+10.0 )

    ###   createRateCheck
    task = item.tasks[0]
    assert( task.pipeline == "pipeline" )
    assert( task.group == "group" )
    assert( task.search == None )
    assert( task.expiration == t0+10.0 )
    assert( task.email == ["a"] )
    print "        WARNING: CreateRateCheck Task.execute() not implemented and not tested"
#    raise NotImplementedError("actually test Task.execute() for this Item")

    #--------------------
    # LocalRateItem
    #--------------------
    print "    LocalRateItem"

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid,
        'pipeline' : 'pipeline',
        'group' : 'group',
        'search' : 'search',
        }
    t0 = time.time()
    options = {
        'dt'   : '10.0',
        'win+' : '5.0',
        'win-' : '5.0',
        'max rate' : 2.0,
        'email' : 'a',
        }

    item = basic.LocalRateItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 1 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+10.0 )

    ### localRateCheck
    task = item.tasks[0]
    assert( task.pipeline == "pipeline" )
    assert( task.group == "group" )
    assert( task.search == "search" )
    assert( task.expiration == t0+10.0 )
    assert( task.email == ["a"] )

    ### check again when search is not specified
    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid,
        'pipeline': 'pipeline',
        'group' : 'group',
        }
    t0 = time.time()
    options = {
        'dt'   : '10.0',
        'win+' : '5.0',
        'win-' : '5.0',
        'max rate' : 2.0,
        'email' : 'a',
        }

    item = basic.LocalRateItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 1 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+10.0 )

    ###   localRateCheck
    task = item.tasks[0]
    assert( task.pipeline == "pipeline" )
    assert( task.group == "group" )
    assert( task.search == None )
    assert( task.expiration == t0+10.0 )
    assert( task.email == ["a"] )
    print "        WARNING: LocalRateCheck Task.execute() not implemented and not tested"
#    raise NotImplementedError("actually test Task.execute() for this Item")

    #--------------------
    # FARItem
    #--------------------
    print "    FARItem"

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid
        }
    t0 = time.time()
    options = {
        'dt'   : '10.0',
        'min far' : '0.0',
        'max far' : '5.0',
        'email' : 'a',
        }

    item = basic.FARItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 1 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+10.0 )

    ###   FARCheck
    task = item.tasks[0]
    assert( task.minFAR == 0.0 )
    assert( task.maxFAR == 5.0 )
    assert( task.expiration == t0+10.0 )
    assert( task.email == ['a'] )

    print "        WARNING: FARCheck Task.execute() not implemented and not tested"
#    raise NotImplementedError("actually test Task.execute() for this Item")

    #--------------------
    # ExternalTriggersItem
    #--------------------
    print "    ExternalTriggersItem"

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
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 1 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+10.0 )

    ###   externalTriggersCheck
    task = item.tasks[0]
    assert( task.expiration == t0+10.0 )
    assert( task.email == ['a'] )
    print "        WARNING: ExternalTriggersCheck Task.execute() not implemented and not tested"
#    raise NotImplementedError("actually test Task.execute() for this Item")

    #--------------------
    # UnblindInjectionsItem
    #--------------------
    print "    UnblindInjectionsItem"

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
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 1 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+10.0 )

    ###   unblindInjectionsCheck
    task = item.tasks[0]
    assert( task.expiration == t0+10.0 )
    assert( task.email == ['a'] )
    print "        WARNING: unblindInjectionsCheck Task.execute() not implemented and not tested"
#    raise NotImplementedError("actually test Task.execute() for this Item")

    print "    basic.py passed all tests sucessfully!"

#-------------------------------------------------

if opts.approvalProcessor:
    print "testing basic/approvalProcessor.py"

    #--------------------
    # ApprovalProcessroPrelimDQItem
    #--------------------
    print "    ApprovalProcessorPrelimDQItem"

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid
        }
    t0 = time.time()
    options = {
        'far dt'   : '10.0',
#        'seg start dt'   : '20.0',
        'email' : 'a',
        }

    item = approvalProcessor.ApprovalProcessorPrelimDQItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 1 ) ### NOTE: only using "far dt" right now
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+10.0 )

    ### check tasks
    tasks = dict( (task.name, task) for task in item.tasks )

    ###   approvalProcessorFARCheck
    far = tasks['approvalProcessorFAR']
    assert( far.expiration == t0+10.0 )
    assert( far.email == ['a'] )
    print "        WARNING: approvalProcessorFARCheck Task.execute() not implemented and not tested"

    ###   approvalProcessorSegDBStartCheck
#    segStart = tasks['approvalProcessorSegDBStart']
#    assert( segStart.expiration == t0+20.0 )
#    assert( segStart.email == ['a'] )
#    print "        WARNING: approvalProcessorSegDBStartCheck Task.execute() not implemented and not tested"

    #--------------------
    # ApprovalProcessorSegDBItem
    #--------------------
    print "    ApprovalProcessorSegDBItem"

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid
        }
    t0 = time.time()
    options = {
        'flags dt' : '10.0',
        'flags' : 'H1:DMT-ANALYSIS_READY:1',
        'finish dt' : '20.0',
        'email' : 'a',
        }

    item = approvalProcessor.ApprovalProcessorSegDBItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 2 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+10.0 )

    ### check tasks
    tasks = dict( (task.name, task) for task in item.tasks )
    flags = tasks['approvalProcessorSegDBFlags']
    finish = tasks['approvalProcessorSegDBFinish']
    ###   approvalProcessorSegDBFlagsCheck
    assert( flags.expiration == t0+10.0 )
    assert( flags.email == ['a'] )
    assert( flags.flags == ['H1:DMT-ANALYSIS_READY:1'] )
    print "        WARNING: approvalProcessorFARCheck Task.execute() not implemented and not tested"

    ###   approvalProcessorSegDBFinishCheck
    assert( finish.expiration == t0+20.0 )
    assert( finish.email == ['a'] )
    print "        WARNING: approvalProcessorFARCheck Task.execute() not implemented and not tested"

    #--------------------
    # ApprovalProcessoriDQItem
    #--------------------
    print "    ApprovalProcessoriDQItem"

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid,
        'description' : 'blah blah blah H1',
        }
    t0 = time.time()
    options = {
        'dt'   : '10.0',
        'email' : 'a',
        }

    item = approvalProcessor.ApprovalProcessoriDQItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 1 )
    assert( len(item.completedTasks) == 0 )
    assert( item.ifo == "H1" )
    assert( item.expiration == t0+10.0 )

    ###   approvalProcessoriDQglitchFAPCheck
    task = item.tasks[0]
    assert( task.expiration == t0+10.0 )
    assert( task.email == ['a'] )
    assert( task.ifo == "H1" )
    print "        WARNING: approvalProcessoriDQglitchFAPCheck Task.execute() not implemented and not tested"

    #--------------------
    # ApprovalProcessroVOEventItem
    #--------------------
    print "    ApprovalProcessorVOEventItem"

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
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 2 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+10.0 )

    ### check tasks
    tasks = dict( (task.name, task) for task in item.tasks )
    create = tasks['approvalProcessorVOEventCreation']
    distrb = tasks['approvalProcessorVOEventDistribution']
    ###   approvalProcessorVOEventCreationCheck
    assert( create.expiration == t0+10.0 )
    assert( create.email == ["a"] )
    print "        WARNING: approvalProcessorVOEventCreationCheck Task.execute() not implemented and not tested"

    ###   approvalProcessorVOEventDistributionCheck
    assert( distrb.expiration == t0+10.0 )
    assert( distrb.email == ["a"] )
    print "        WARNING: approvalProcessorVOEventDistributionCheck Task.execute() not implemented and not tested"

    #--------------------
    # ApprovalProcessorGCNItem
    #--------------------
    print "    ApprovalProcessorGCNItem"

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
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 2 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+10.0 )

    ### check tasks
    tasks = dict( (task.name, task) for task in item.tasks )
    create = tasks['approvalProcessorGCNCreation']
    distrb = tasks['approvalProcessorGCNDistribution']
    ###   approvalProcessorGCNCreationCheck
    assert( create.expiration == t0+10.0 )
    assert( create.email == ["a"] )
    print "        WARNING: approvalProcessorGCNCreationCheck Task.execute() not implemented and not tested"

    ###   approvalProcessorGCNDistributionCheck
    assert( create.expiration == t0+10.0 )
    assert( create.email == ["a"] )
    print "        WARNING: approvalProcessorGCNdistributionCheck Task.execute() not implemented and not tested"

    print "    approvalProcessor.py passed all tests sucessfully!"

#-------------------------------------------------

### skymaps
if opts.skymaps:
    print "testing skymaps/skymaps.py"

    #--------------------
    # SkymapSanityItem
    #--------------------
    print "    SkymapSanityItem"

    graceid = 'FakeEvent'
    fitsname = "fake.fits.gz"
    alert = {
        'uid' : graceid,
        'file' : fitsname,
        'object' : {'tagnames':[]},
        }
    t0 = time.time()
    options = {
        'dt'   : '10.0',
        'email' : 'a',
        }

    item = skymaps.SkymapSanityItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.fitsname == fitsname )
    assert( item.complete == False )
    assert( len(item.tasks) == 1 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+10.0 )

    ###   skymapSanityCheck
    task = item.tasks[0]
    assert( task.fitsname == fitsname )
    assert( task.expiration == t0+10.0 ) 
    assert( task.email == ['a'] )

    print "        WARNING: skymapSanityCheck Task.execute() not implemented and not tested"
#    raise NotImplementedError("actually test Task.execute() for this Item")

    #--------------------
    # PlotSkymapItem
    #--------------------
    print "    PlotSkymapItem"

    graceid = 'FakeEvent'
    fitsname = 'fake.fits.gz'
    alert = {
        'uid' : graceid,
        'file' : fitsname,
        'object' : {'tagnames':[]},
        }
    t0 = time.time()
    options = {
        'dt'   : '10.0',
        'email' : 'a',
        }

    item = skymaps.PlotSkymapItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.fitsname == fitsname )
    assert( item.tagnames == [] )
    assert( item.complete == False )
    assert( len(item.tasks) == 1 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+10.0 )

    ###   plotSkymapCheck
    task = item.tasks[0]
    assert( task.fitsname == fitsname )
    assert( task.expiration == t0+10.0 )
    assert( task.email == ['a'] )

    print "        WARNING: plotSkymapCheck Task.execute() not implemented and not tested"
#    raise NotImplementedError("actually test Task.execute() for this Item")

    #--------------------
    # SkyviewerItem
    #--------------------
    print "    SkyviewerItem"

    graceid = 'FakeEvent'
    fitsname = 'fake.fits.gz'
    alert = {
        'uid' : graceid,
        'file' : fitsname,
        'object' : {'tagnames':[]},
        }
    t0 = time.time()
    options = {
        'dt'   : '10.0',
        'email' : 'a',
        }

    item = skymaps.SkyviewerItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.fitsname == fitsname )
    assert( item.tagnames == [] )
    assert( item.complete == False )
    assert( len(item.tasks) == 1 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+10.0 )

    ###   skyviewerCheck
    task = item.tasks[0]
    assert( task.fitsname == fitsname )
    assert( task.expiration == t0+10.0 )
    assert( task.email == ['a'] )

    print "        WARNING: skyviewerCheck Task.execute() not implemented and not tested"
#    raise NotImplementedError("actually test Task.execute() for this Item")

    print "    skymaps.py passed all tests sucessfully!"

#-------------------------------------------------

if opts.skymapSummary:
    print "testing skymaps/skymapSummary.py"

    #--------------------
    # SnglFITSStartItem
    #--------------------
    print "    SnglFITSStartItem"

    graceid = 'FakeEvent'
    filename = 'fake.fits.gz',
    alert = {
        'uid' : graceid,
        'file' : filename,
        'object' : {'tagnames':['sky_loc']},
        }
    t0 = time.time()
    options = {
        'dt'   : '10.0',
        'email' : 'a',
        }

    item = skymapSummary.SnglFITSStartItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.fitsname == filename )
#    assert( item.tagnames == ['sky_loc'] ) ### FIXME: this should fail...
    assert( item.complete == False )
    assert( len(item.tasks) == 1 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+10.0 )

    ###   skymapSummaryStartCheck
    task = item.tasks[0]
    assert( task.fitsname == filename )
#    assert( task.tagnames == ['sky_loc'] )
    assert( task.expiration == t0+10.0 )
    assert( task.email == ['a'] )

    print "        WARNING: skymapSummaryStartCheck Task.execute() not implemented and not tested"

    #--------------------
    # SnglFITSItem
    #--------------------
    print "    SnglFITSItem"

    graceid = 'FakeEvent'
    filename = 'fake.fits.gz'
    alert = {
        'uid' : graceid,
        'description' : 'started skymap summary for <a href="not real">%s</a>'%filename,
        }
    t0 = time.time()
    options = {
        'html dt'   : '10.0',
        'finish dt' : '20.0',
        'email' : 'a',
        }

    item = skymapSummary.SnglFITSItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.fitsname == filename )
#    assert( item.tagnames == ['sky_loc'] ) ### FIXME: this should fail...
    assert( item.complete == False )
    assert( len(item.tasks) == 2 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+10.0 )

    ### check tasks
    tasks = dict( (task.name, task) for task in item.tasks )
    data = tasks['snglFITShtml']
    finish = tasks['snglFITSFinish']
    ###   skymapSummaryDataCheck
    assert( data.fitsname == filename )
#    assert( data.tagnames == ['sky_loc'] ) ### this should fail...
    assert( data.expiration == t0+10.0 )
    assert( data.email == ['a'] )
    print "        WARNING: skymapSummaryDataCheck Task.execute() not implemented and not tested"

    ###   skymapSummaryFinishCheck
    assert( finish.fitsname == filename )
#    assert( finish.tagnames == ['sky_loc'] ) ### this should fail...
    assert( finish.expiration == t0+20.0 )
    assert( finish.email == ['a'] )
    print "        WARNING: skymapSummaryFinishCheck Task.execute() not implemented and not tested"

    #--------------------
    # MultFITSStartItem
    #--------------------
    print "    MultFITSStartItem"

    graceid = 'G263969' ### extracted this by hand from GraceDb -> FRAGILE!

    from ligo.gracedb.rest import GraceDb
    gdb = GraceDb()
    filenames = [fits for fits in gdb.files( graceid ).json().keys() if fits.endswith('.fits') or fits.endswith('.fits.gz')]

    alert = {
        'uid' : graceid,
        'description' : 'finished skymap summary for DOES NOT MATTER',
        }
    t0 = time.time()
    options = {
        'dt'   : '10.0',
        'email' : 'a',
        }

    item = skymapSummary.MultFITSStartItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.fitsnames == filenames )
#    assert( item.tagnames == ['sky_loc'] ) ### FIXME: this should fail...
    assert( item.complete == False )
    assert( len(item.tasks) == 1 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+10.0 )

    ###   skymapSummaryStartCheck
    task = item.tasks[0]
    assert( task.fitsnames == filenames )
#    assert( task.tagnames == ['sky_loc'] ) ### FIXME: this should break...
    assert( task.expiration == t0+10.0 )
    assert( task.email == ['a'] )

    print "        WARNING: skymapSummaryStartCheck Task.execute() not implemented and not tested"

    #--------------------
    # MultFITSItem
    #--------------------
    print "    MultFITSItem"

    filenames = ['fake1.fits', 'fake2.fits.gz']

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid,
        'description' : 'started skymap comparison for <a href="not real">%s</a>, <a href="not real either">%s</a>'%tuple(filenames),
        }
    t0 = time.time()
    options = {
        'html dt'   : '10.0',
        'finish dt' : '20.0',
        'email' : 'a',
        }

    item = skymapSummary.MultFITSItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.fitsnames == filenames )
#    assert( item.tagnames == ['sky_loc'] ) ### FIXME: this should fail...
    assert( item.complete == False )
    assert( len(item.tasks) == 2 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+10.0 )

    ### check tasks
    tasks = dict( (task.name, task) for task in item.tasks )
    data = tasks['multFITShtml']
    finish = tasks['multFITSFinish']
    ###   skymapSummaryDataCheck
#    assert( data.tagnames == ['sky_loc'] ) ### this should fail...
    assert( data.expiration == t0+10.0 )
    assert( data.email == ['a'] )
    print "        WARNING: skymapSummaryDataCheck Task.execute() not implemented and not tested"

    ###   skymapSummaryFinishCheck
    assert( finish.fitsnames == filenames )
#    assert( finish.tagnames == ['sky_loc'] ) ### this should fail...
    assert( finish.expiration == t0+20.0 )
    assert( finish.email == ['a'] )
    print "        WARNING: skymapSummaryFinishCheck Task.execute() not implemented and not tested"

    print "    skymapSummary.py passed all tests sucessfully!"

#-------------------------------------------------

### pe
if opts.bayestar:
    print "testing pe/bayestar.py"

    #--------------------
    # BayestarStartItem
    #--------------------
    print "    BayestarStartItem"

    graceid = 'FakeEvent'
    filename = "bayestar.fits.gz",
    alert = {
        'uid' : graceid,
        }
    t0 = time.time()
    options = {
        'dt'   : '10.0',
        'email' : 'a',
        }

    item = bayestar.BayestarStartItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 1 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+10.0 )

    ###   bayestarStartCheck
    task = item.tasks[0]
    assert( task.expiration == t0+10.0 )
    assert( task.email == ['a'] )

    print "        WARNING: bayestarStartCheck Task.execute() not implemented and not tested"

    #--------------------
    # BayestarItem
    #--------------------
    print "    BayestarItem"

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid
        }
    t0 = time.time()
    options = {
        'skymap dt'   : '10.0',
        'skymap tagnames'   : 'sky_loc lvem',
        'finish dt' : '20.0',
        'email' : 'a',
        }

    item = bayestar.BayestarItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 2 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+10.0 )

    ### check tasks
    tasks = dict( (task.name, task) for task in item.tasks )
    skymap = tasks['bayestarSkymap']
    finish = tasks['bayestarFinish']
    ###   bayestarSkymapCheck
    assert( skymap.expiration == t0+10.0 )
    assert( skymap.email == ['a'] )
    assert( skymap.tagnames == ['sky_loc', 'lvem'] )
    print "        WARNING: bayestarSkymapCheck Task.execute() not implemented and not tested"

    ###   bayestarFinishItem
    assert( finish.expiration == t0+20.0 )
    assert( finish.email == ['a'] )
    print "        WARNING: bayestarFinishCheck Task.execute() not implemented and not tested"

    print "    bayestar.py passed all tests sucessfully!"

#-------------------------------------------------

if opts.embright:
    print "testing pe/embright.py"

    #--------------------
    # EMBrightItem
    #--------------------
    print "    EMBrightItem"

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid,
        }
    t0 = time.time()
    options = {
        'dt'   : '10.0',
        'email' : 'a',
        }

    item = embright.EMBrightItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 1 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+10.0 )

    ###   emBrightCheck
    task = item.tasks[0]
    assert( task.expiration == t0+10.0 )
    assert( task.email == ['a'] )

    print "        WARNING: emBrigthCheck Task.execute() not implemented and not tested"

    print "    embright.py passed all tests sucessfully!"

#-------------------------------------------------

if opts.bayeswavePE:
    print "testing pe/bayeswavePE.py"

    #--------------------
    # BayesWavePEStartItem
    #--------------------
    print "    BayesWavePEStartItem"

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
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 1 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+10.0 )

    ###   bayeswavePEStartCheck
    task = item.tasks[0]
    assert( task.expiration == t0+10.0 )
    assert( task.email == ['a'] )

    print "        WARNING: bayeswavePEStartCheck Task.execute() not implemented and not tested"

    #--------------------
    # BayesWavePEItem
    #--------------------
    print "    BayesWavePEItem"

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid
        }
    t0 = time.time()
    options = {
        'post samp dt'   : '10.0',
        'estimate dt' : '20.0',
        'bayes factor dt' : '30.0',
        'skymap dt' : '40.0',
        'skymap tagnames' : 'sky_loc',
        'email' : 'a',
        }

    item = bayeswavePE.BayesWavePEItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 4 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+10.0 )

    ### check tasks
    tasks = dict( (task.name, task) for task in item.tasks )
    postSamp = tasks['bayeswavePEPostSamp']
    baysFact = tasks['bayeswavePEBayesFactors']
    estimate = tasks['bayeswavePEEstimate']
    skymap = tasks['bayeswavePESkymap']

    ###   bayeswavePEPostSampCheck
    assert( postSamp.expiration == t0+10.0 )
    assert( postSamp.email == ['a'] )
    print "        WARNING: bayeswavePEPostSampCheck Task.execute() not implemented and not tested"

    ###   bayeswavePEBayesFactorsCheck
    assert( baysFact.expiration == t0+30.0 )
    assert( baysFact.email == ['a'] )
    print "        WARNING: bayeswavePEBayesFactorCheck Task.execute() not implemented and not tested"

    ###   bayeswavePEEstimateCheck
    assert( estimate.expiration == t0+20.0 )
    assert( estimate.email == ['a'] )
    print "        WARNING: bayeswavePEEstimateCheck Task.execute() not implemented and not tested"

    ###   bayeswavePESkymapCheck
    assert( skymap.expiration == t0+40.0 )
    assert( skymap.email == ['a'] )
    assert( skymap.tagnames == ['sky_loc'] )
    print "        WARNING: bayeswavePESkymapCheck Task.execute() not implemented and not tested"

    print "    bayeswavePE.py passed all tests sucessfully!"

#-------------------------------------------------

if opts.cwbPE:
    print "testing pe/cwbPE.py"
    
    ### note, start and finish checks don't really make sense given the way cWB uploads data

    #--------------------
    # CWBPEItem
    #--------------------
    print "    CWBPEItem"

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid
        }
    t0 = time.time()
    options = {
        'ced dt'   : '10.0',
        'estimate dt' : '20.0',
        'skymap dt' : '30.0',
        'skymap tagnames' : 'sky_loc lvem',
        'email' : 'a',
        }

    item = cwbPE.CWBPEItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 3 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+10.0 )

    ### check tasks
    tasks = dict( (task.name, task) for task in item.tasks )
    ced = tasks['cWBPECED']
    est = tasks['cWBPEEstimate']
    sky = tasks['cWBPESkymap']

    ###   cWBPECEDCheck
    assert( ced.expiration == t0+10.0 )
    assert( ced.email == ['a'] )
    print "        WARNING: cWBCEDCheck Task.execute() not implemented and not tested"

    ###   cWBPEEstimateCheck
    assert( est.expiration == t0+20.0 )
    assert( est.email == ['a'] )
    print "        WARNING: cWBPEEstimateCheck Task.execute() not implemented and not tested"

    ###   cWBPESkymapCheck
    assert( sky.expiration == t0+30.0 )
    assert( sky.email == ['a'] )
    assert( sky.tagnames == ['sky_loc', 'lvem'] )
    print "        WARNING: cWBPESkymapCheck Task.execute() not implemented and not tested"

    print "    cwbPE.py passed all tests sucessfully!"

#-------------------------------------------------

if opts.libPE:
    print "testing pe/libPE.py"

    #--------------------
    # LIBPEStartItem
    #--------------------
    print "    LIBPEStartItem"

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
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 1 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+10.0 )

    ###   libPEStartCheck
    task = item.tasks[0]
    assert( task.expiration == t0+10.0 )
    assert( task.email == ['a'] )
    print "        WARNING: libPEStartCheck Task.execute() not implemented and not tested"

    #--------------------
    # LIBPEItem
    #--------------------
    print "    LIBPEItem"

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid
        }
    t0 = time.time()
    options = {
        'post samp dt'   : '20.0',
        'bayes factor dt' : '10.0',
        'skymap dt' : '30.0',
        'skymap tagnames' : 'sky_loc lvem',
        'finish dt' : '40.0',
        'email' : 'a',
        }

    item = libPE.LIBPEItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 4 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+10.0 )

    ### check tasks
    tasks = dict( (task.name, task) for task in item.tasks )
    bysFct = tasks['libPEBayesFactors']
    pstSmp = tasks['libPEPostSamp']
    skymap = tasks['libPESkymap']
    finish = tasks['libPEFinish']

    ###   libPEBayesFactorsCheck
    assert( bysFct.expiration == t0+10.0 )
    assert( bysFct.email == ['a'] )
    print "        WARNING: libPEBayesFactorsCheck Task.execute() not implemented and not tested"

    ###   libPEPostSampCheck
    assert( pstSmp.expiration == t0+20.0 )
    assert( pstSmp.email == ['a'] )
    print "        WARNING: libPEPostSampCheck Task.execute() not implemented and not tested"

    ###   libPESkymapCheck
    assert( skymap.expiration == t0+30.0 )
    assert( skymap.email == ['a'] )
    assert( skymap.tagnames == ['sky_loc', 'lvem'] )
    print "        WARNING: libPESkymapCheck Task.execute() not implemented and not tested"

    ###   libPEFinishCheck
    assert( finish.expiration == t0+40.0 )
    assert( finish.email == ['a'] )
    print "        WARNING: libPEFinishCheck Task.execute() not implemented and not tested"

    print "    libPE.py passed all tests sucessfully!"

#-------------------------------------------------

if opts.lalinf:
    print "testing pe/lalinf.py"

    #--------------------
    # LALInfStartItem
    #--------------------
    print "    LALInfStartItem"

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
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 1 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+10.0 )

    ###   lalinfStartCheck
    task = item.tasks[0]
    assert( task.expiration == t0+10.0 )
    assert( task.email == ['a'] )
    print "        WARNING: lalinfStartCheck Task.execute() not implemented and not tested"

    #--------------------
    # LALInfItem
    #--------------------
    print "    LALInfItem"

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid
        }
    t0 = time.time()
    options = {
        'post samp dt'   : '10.0',
        'skymap dt' : '20.0',
        'skymap tagnames' : 'sky_loc lvem',
        'finish dt' : '30.0',
        'email' : 'a',
        }

    item = lalinf.LALInfItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 3 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+10.0 )

    ### check tasks
    tasks = dict( (task.name, task) for task in item.tasks )
    pstSmp = tasks['lalinfPostSamp']
    skymap = tasks['lalinfSkymap']
    finish = tasks['lalinfFinish']

    ###   lalinfPostSampCheck
    assert( pstSmp.expiration == t0+10.0 )
    assert( pstSmp.email == ['a'] )
    print "        WARNING: lalinfPostSampCheck Task.execute() not implemented and not tested"

    ###   lalinfSkymapCheck
    assert( skymap.expiration == t0+20.0 )
    assert( skymap.email == ['a'] )
    assert( skymap.tagnames == ['sky_loc', 'lvem'] )
    print "        WARNING: lalinfSkymapCheck Task.execute() not implemented and not tested"

    ###   lalinfFinishCheck
    assert( finish.expiration == t0+30.0 )
    assert( finish.email == ['a'] )
    print "        WARNING: lalinfFinishCheck Task.execute() not implemented and not tested"

    print "    lalinf.py passed all tests sucessfully!"

#-------------------------------------------------

### dq
if opts.dq:
    print "testing dq/dq.py"

    #--------------------
    # DQSummaryItem
    #--------------------
    print "    DQSummaryItem"

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid
        }
    t0 = time.time()
    options = {
        'dt'   : '10.0',
        'email' : 'a',
        }

    item = dq.LLDQReportItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 1 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+10.0 )

    ###   dqSummaryCheck
    task = item.tasks[0]
    assert( task.expiration == t0+10.0 )
    assert( task.email == ['a'] )
    print "        WARNING: dqSummaryCheck Task.execute() not implemented and not tested"

    print "    dq.py passed all tests sucessfully!"

#-------------------------------------------------

if opts.idq:
    print "testing dq/idq.py"

    #--------------------
    # IDQStartItem
    #--------------------
    print "    IDQStartItem"

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
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 2 ) ### there are 2 ifos
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+10.0 )
    assert( item.ifos == ['H', 'L'] )

    ###   idqStartCheck
    tasks = dict( (task.ifo, task) for task in item.tasks )
    H = tasks['H']
    L = tasks['L']

    assert( H.expiration == t0+10.0 )
    assert( H.email == ['a'] )
    
    assert( L.expiration == t0+10.0 )
    assert( L.email == ['a'] )

    print "        WARNING: idqStartCheck Task.execute() not implemented and not tested"

    #--------------------
    # IDQItem
    #--------------------
    print "    IDQItem"

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid,
        'description' : 'blah blah blah H1',
        }
    t0 = time.time()
    options = {
        'classifiers' : 'ovl B',
        'tables dt' : '5.0',
        'glitch fap dt' : '10.0',
        'fap frame dt' : '20.0',
        'rank frame dt' : '30.0',
        'timeseries plot dt' : '40.0',
        'active chan dt' : '50.0',
        'active chan plot dt' : '60.0',
        'calib dt' : '70.0',
        'calib plot dt' : '80.0',
        'roc dt' : '90.0',
        'roc plot dt' : '100.0',
        'calib stats dt' : '110.0',
        'train stats dt' : '120.0',
        'finish dt' : '130.0',
        'email' : 'a',
        }

    item = idq.IDQItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 13*2+1 ) ### (13 checks per classifier and 2 classifiers) + (1 finish check)
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+5.0 )
    assert( item.ifo == 'H1' )
    assert( item.classifiers == ['ovl', 'B'] )

    ### check tasks
    for classifier in item.classifiers:
        tasks = dict( (task.name, task) for task in item.tasks if (task.name!='idqFinish') and (task.classifier==classifier) )

        tables = tasks['idqTables']
        glchFAP = tasks['idqGlitchFAP']
        fapFram = tasks['idqFAPFrame']
        rnkFram = tasks['idqRankFrame']
        timesrs = tasks['idqTimeseriesPlot']
        actvChn = tasks['idqActiveChan']
        actvChnPlt = tasks['idqActiveChanPlot']
        calibration = tasks['idqCalibration']
        calibrationPlt = tasks['idqCalibrationPlot']
        roc = tasks['idqROC']
        rocPlt = tasks['idqROCPlot']
        calibStats = tasks['idqCalibStats']
        trainStats = tasks['idqTrainStats']

        ###   idqTablesCheck
        assert( tables.expiration == t0+5.0 )
        assert( tables.email == ['a'] )
        assert( tables.ifo == 'H1' )
        print "        WARNING: idqTablesCheck Task.execute() not implemented and not tested"

        ###   idqGltichFAPCheck
        assert( glchFAP.expiration == t0+10.0 )
        assert( glchFAP.email == ['a'] )
        assert( glchFAP.ifo == 'H1' )
        print "        WARNING: idqGlitchFAPCheck Task.execute() not implemented and not tested"

        ###   idqFAPFrameCheck
        assert( fapFram.expiration == t0+20.0 )
        assert( fapFram.email == ['a'] )
        assert( fapFram.ifo == 'H1' )
        print "        WARNING: idqFAPFrameCheck Task.execute() not implemented and not tested"
 
        ###   idqRankFrameCheck
        assert( rnkFram.expiration == t0+30.0 )
        assert( rnkFram.email == ['a'] )
        assert( rnkFram.ifo == 'H1' )
        print "        WARNING: idqRankFrameCheck Task.execute() not implemented and not tested"

        ###   idqTimeseriesPlotCheck
        assert( timesrs.expiration == t0+40.0 )
        assert( timesrs.email == ['a'] )
        assert( timesrs.ifo == 'H1' )
        print "        WARNING: idqTimeseriesPlotCheck Task.execute() not implemented and not tested"

        ###   idqActiveChanCheck
        assert( actvChn.expiration == t0+50.0 )
        assert( actvChn.email == ['a'] )
        assert( actvChn.ifo == 'H1' )
        print "        WARNING: idqActiveChanCheck Task.execute() not implemented and not tested"

        ###   idqActiveChanPlotCheck
        assert( actvChnPlt.expiration == t0+60.0 )
        assert( actvChnPlt.email == ['a'] )
        assert( actvChnPlt.ifo == 'H1' )
        print "        WARNING: idqActiveChanPlotCheck Task.execute() not implemented and not tested"

        ###   idqCalibrationCheck
        assert( calibration.expiration == t0+70.0 )
        assert( calibration.email == ['a'] )
        assert( calibration.ifo == 'H1' )
        print "        WARNING: idqCalibrationCheck Task.execute() not implemented and not tested"

        ###   idqCalibrationPlotCheck
        assert( calibrationPlt.expiration == t0+80.0 )
        assert( calibrationPlt.email == ['a'] )
        assert( calibrationPlt.ifo == 'H1' )
        print "        WARNING: idqCalibrationPlotCheck Task.execute() not implemented and not tested"

        ###   idqROCCheck
        assert( roc.expiration == t0+90.0 )
        assert( roc.email == ['a'] )
        assert( roc.ifo == 'H1' )
        print "        WARNING: idqROCCheck Task.execute() not implemented and not tested"

        ###   idqROCPlotCheck
        assert( rocPlt.expiration == t0+100.0 )
        assert( rocPlt.email == ['a'] )
        assert( rocPlt.ifo == 'H1' )
        print "        WARNING: idqROCPlotCheck Task.execute() not implemented and not tested"

        ###   idqCalibStatsCheck
        assert( calibStats.expiration == t0+110.0 )
        assert( calibStats.email == ['a'] )
        assert( calibStats.ifo == 'H1' )
        print "        WARNING: idqCalibStatsCheck Task.execute() not implemented and not tested"

        ###   idqTrainStatsCheck
        assert( trainStats.expiration == t0+120.0 )
        assert( trainStats.email == ['a'] )
        assert( trainStats.ifo == 'H1' )
        print "        WARNING: idqTrainStatsCheck Task.execute() not implemented and not tested"

    task = [task for task in item.tasks if task.name=='idqFinish'][0]
    assert( task.expiration == t0+130.0 )
    assert( task.email == ['a'] )
    assert( task.ifo == 'H1' )

    print "    idq.py passed all tests sucessfully!"

#-------------------------------------------------

if opts.omegaScan:
    print "testing dq/omegaScan.py"

    #--------------------
    # L1OmegaScanStartItem
    #--------------------
    print "    L1OmegaScanStartItem"

    chansets = 'l1_llhoft l1_r-reduced l1_r-standard'.split()

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid,
        }
    t0 = time.time()
    options = {
        'dt'   : '10.0',
        'chansets' : ' '.join(chansets ),
        'email' : 'a',
        }

    item = omegaScan.L1OmegaScanStartItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 1 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+10.0 )
    assert( item.chansets == chansets )

    ###   omegaScanStartCheck
    task = item.tasks[0] ### only one task

    assert( task.expiration == t0+10.0 )
    assert( task.email == ['a'] )
    assert( task.chansets == options['chansets'].split() )
    print "        WARNING: omegaScanStartCheck Task.execute() not implemented and not tested"

    #--------------------
    # L1OmegaScanItem
    #--------------------
    print "    L1OmegaScanItem"

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid,
        'object' : {'comment':'automatic OmegaScans begun for: %s. WARNING: we will not track the individual OmegaScan processes to ensure completion'%(', '.join(chansets))},
        }
    t0 = time.time()
    options = {
        'data dt'   : '10.0',
        'finish dt' : '20.0',
        'email' : 'a',
        }

    item = omegaScan.L1OmegaScanItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == len(chansets)+1 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+10.0 )
    assert( item.chansets == chansets )

    alert = {
        'uid' : graceid,
        'object' : {'comment':'automatic OmegaScans begun for: %s.'%(', '.join(chansets))},
        }

    item = omegaScan.L1OmegaScanItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.chansets == chansets )

    ### check tasks
    dataTasks = [ task for task in item.tasks if task.name=='omegaScanData' ]
    assert( len(dataTasks)==len(chansets) )

    finishTask = [task for task in item.tasks if task.name=='omegaScanFinish']
    assert( len(finishTask)==1 )
    finishTask = finishTask[0]

    ###   omegaScanDataCheck
    for chanset, task in zip(chansets, dataTasks):
        assert( task.expiration == t0+10.0 )
        assert( task.email == ['a'] )
        assert( task.chanset == chanset )
    print "        WARNING: omegaScanDataCheck Task.execute() not implemented and not tested"

    ###   omegaScanFinishCheck
    assert( finishTask.expiration == t0+20.0 )
    assert( finishTask.email == ['a'] )
    assert( finishTask.chansets == chansets )
    print "        WARNING: omegaScanFinishCheck Task.execute() not implemented and not tested"

    #--------------------
    # H1OmegaScanStartItem
    #--------------------
    print "    H1OmegaScanStartItem"

    chansets = 'h1_llhoft h1_r-selected'.split()

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid,
        }
    t0 = time.time()
    options = {
        'dt'   : '10.0',
        'chansets' : ' '.join(chansets),
        'email' : 'a',
        }

    item = omegaScan.H1OmegaScanStartItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 1 ) ### 2 ifos
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+10.0 )
    assert( item.chansets == chansets )

    ###   omegaScanStartCheck
    task = item.tasks[0]

    assert( task.expiration == t0+10.0 )
    assert( task.email == ['a'] )
    assert( task.chansets == chansets )

    print "        WARNING: omegaScanStartCheck Task.execute() not implemented and not tested"

    #--------------------
    # H1OmegaScanItem
    #--------------------
    print "    H1OmegaScanItem"

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid,
        'object': {'comment':'automatic OmegaScans begun for: %s. WARNING: we will not track the individual OmegaScan processes to ensure completion'%(', '.join(chansets))},
        }
    t0 = time.time()
    options = {
        'data dt'   : '10.0',
        'finish dt' : '20.0',
        'email' : 'a',
        }

    item = omegaScan.H1OmegaScanItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == len(chansets)+1 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+10.0 )
    assert( item.chansets == chansets )

    ### check tasks
    dataTasks = [ task for task in item.tasks if task.name=='omegaScanData' ]
    assert( len(dataTasks)==len(chansets) )

    finishTask = [task for task in item.tasks if task.name=='omegaScanFinish']
    assert( len(finishTask)==1 )
    finishTask = finishTask[0]

    ###   omegaScanDataCheck
    for chanset, task in zip(chansets, dataTasks):
        assert( task.expiration == t0+10.0 )
        assert( task.email == ['a'] )
        assert( task.chanset == chanset )
    print "        WARNING: omegaScanDataCheck Task.execute() not implemented and not tested"

    ###   omegaScanFinishCheck
    assert( finishTask.expiration == t0+20.0 )
    assert( finishTask.email == ['a'] )
    assert( finishTask.chansets ==chansets )
    print "        WARNING: omegaScanFinishCheck Task.execute() not implemented and not tested"

    '''
    #--------------------
    # IDQOmegaScanStartItem
    #--------------------
    print "    IDQOmegaScanStartItem"

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid,
        'description' : 'blah blah blah H1',
        }
    t0 = time.time()
    options = {
        'dt'   : '10.0',
        'email' : 'a',
        }

    item = omegaScan.IDQOmegaScanStartItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 1 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+10.0 )
    assert( item.ifos == ['H1'] )
    
    ###   omegaScanStartCheck
    task = item.tasks[0]
    assert( task.expiration == t0+10.0 )
    assert( task.email == ['a'] )
    assert( task.ifo == 'H1' )
    assert( task.chanset == 'idq' )
    print "        WARNING: omegaScanStartCheck Task.execute() not implemented and not tested"

    #--------------------
    # IDQOmegaScanItem
    #--------------------
    print "    IDQOmegaScanItem"

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid,
        'description' : 'blah de dah H1',
        }
    t0 = time.time()
    options = {
        'data dt'   : '10.0',
        'finish dt' : '20.0',
        'email' : 'a',
        }

    item = omegaScan.IDQOmegaScanItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 2 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+10.0 )
    assert( item.ifo == "H1" )

    tasks = dict( (task.name, task) for task in item.tasks )
    data = tasks['omegaScanData']
    finish = tasks['omegaScanFinish']
    ###   omegaScanDataCheck
    assert( data.expiration == t0+10.0 )
    assert( data.email == ['a'] )
    assert( data.ifo == 'H1' )
    assert( data.chanset == 'idq' )
    print "        WARNING: omegaScanDataCheck Task.execute() not implemented and not tested"

    ###   omegaScanFinishCheck
    assert( finish.expiration == t0+20.0 )
    assert( finish.email == ['a'] )
    assert( finish.ifo == "H1" )
    assert( finish.chanset == "idq" )
    print "        WARNING: omegaScanFinishCheck Task.execute() not implemented and not tested"

    print "    omegaScan.py passed all tests sucessfully!"
    '''

#-------------------------------------------------

if opts.segDB2grcDB:
    print "testing dq/segDB2grcDB"

    #--------------------
    # SegDB2GrcDBStartItem
    #--------------------
    print "    SegDB2GrcDBStartItem"

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
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 1 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+10.0 )

    ###   segDB2grcDBStartCheck
    task = item.tasks[0]
    assert( task.expiration == t0+10.0 )
    assert( task.email == ['a'] )
    print "        WARNING: segDB2grcDBStartCheck Task.execute() not implemented and not tested"

    #--------------------
    # SegDB2GrcDBItem
    #--------------------
    print "    SegDB2GrcDBItem"

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid
        }
    t0 = time.time()
    options = {
        'flags dt'   : '10.0',
        'flags' : 'H1:DMT-ANALYSIS_READY:1 L1:DMT-ANALYSIS_READY:1',
        'veto def dt'   : '20.0',
        'veto defs' : '', ### not implemented...
        'any dt'   : '30.0',
        'finish dt' : '40.0',
        'email' : 'a',
        }

    item = segDB2grcDB.SegDB2GrcDBItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 4 ) ### no veto defs ...
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+10.0 )

    ###   segDB2grcDBFlagsCheck
    for flag, task in zip(options['flags'].split(), [task for task in item.tasks if task.name=='segDb2grcDBFlag']):
        assert( task.expiration == t0+10.0 )
        assert( task.email == ['a'] )
        assert( task.flag == flag )
    print "        WARNING: segDB2grcDBFlagsCheck Task.execute() not implemented and not tested"

    ###   segDB2grcDBVetoDefCheck
    for vetoDef, task in zip(options['veto defs'].split(), [task for task in item.tasks if task.name=='segDb2grcDBVetoDef']):
        assert( vetoDef.expiration == t0+20.0 )
        assert( vetoDef.email == ['a'] )
        assert( vetoDef.vetoDefs == vetoDef )
    print "        WARNING: segDB2grcDBVetoDefCheck Task.execute() not implemented and not tested"

    ###   segDB2grcDBAnyCheck
    anyseg = [task for task in item.tasks if task.name=='segDB2grcDBAny']
    assert( len(anyseg) == 1 )
    anySeg = anyseg[0]
    assert( anySeg.expiration == t0+30.0 )
    assert( anySeg.email == ['a'] )
    print "        WARNING: segDB2grcDBAnyFinishCheck Task.execute() not implemented and not tested"

    ###   segDB2grcDBFinishCheck
    finish = [task for task in item.tasks if task.name=='segDB2grcDBFinish']
    assert( len(finish) == 1 )
    finish = finish[0]
    assert( finish.expiration == t0+40.0 )
    assert( finish.email == ['a'] )
    print "        WARNING: segDB2grcDBFinishCheck Task.execute() not implemented and not tested"

    print "    segDB2grcDB.py passed all tests sucessfully!"

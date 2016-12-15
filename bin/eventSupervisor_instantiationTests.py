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

from ligo.gracedb.rest import GraceDb

from ConfigParser import SafeConfigParser

from optparse import OptionParser

#-------------------------------------------------

parser = OptionParser(usage=usage, description=description)

### check everything
parser.add_option('', '--everything', default=False, action="store_true", help="run tests for everything")

parser.add_option('-c', '--config', default=None, type='string')

# notify
parser.add_option("", "--notify", default=False, action="store_true")

# basic
parser.add_option("", "--basic", default=False, action="store_true")
#parser.add_option("", "--approvalProcessor", default=False, action="store_true")

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

if not opts.config:
    opts.config = raw_input('--config=')

opts.notify            = opts.notify            or opts.everything
opts.basic             = opts.basic             or opts.everything
#opts.approvalProcessor = opts.approvalProcessor or opts.everything
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
gdb = GraceDb()
annotate = False

#-------------------------------------------------

print "reaing config from : %s"%opts.config
config = SafeConfigParser()
config.read(opts.config)

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
    options = dict( config.items('notify') )

    ### instantiate Item
    item = notify.NotifyItem( alert, t0, options, gdb, annotate=annotate )

    ### assert stuff about Items
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 1 ) ### NOTE: only using 'by email' right now...
    assert( len(item.completedTasks) == 0 ) 
    assert( item.expiration == t0+float(options['dt']) )

    ### asser stuff about Tasks    
    tasks = dict( (task.name, task) for task in item.tasks )

    byEmail = tasks['notifyByEmail']
    assert( byEmail.notificationList == options['by email'].split() )
    assert( byEmail.expiration == t0+float(options['dt']) )
    assert( byEmail.emailOnSuccess == options['email on success'].split() )
    assert( byEmail.emailOnFailure == options['email on failure'].split() )
    assert( byEmail.emailOnException == options['email on exception'].split() )

#    bySMS   = tasks['notifyBySMS']
#    assert( bySMS.notificationList == options['by sms'].split() )
#    assert( bySMS.expiration == t0+float(options['dt']))
#    assert( byEmail.emailOnSuccess == options['email on success'].split() )
#    assert( byEmail.emailOnFailure == options['email on failure'].split() )
#    assert( byEmail.emailOnException == options['email on exception'].split() )

#    byPhone = tasks['notifyByPhone']
#    assert( byPhone.notificationList == options['by phone'].split() )
#    assert( byPhone.expiration == t0+float(options['dt']) )
#    assert( byEmail.emailOnSuccess == options['email on success'].split() )
#    assert( byEmail.emailOnFailure == options['email on failure'].split() )
#    assert( byEmail.emailOnException == options['email on exception'].split() )

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
    pipeline = 'CWB'
    alert = {
        'uid' : graceid,
        'object' : {'pipeline' : pipeline,},
        }
    t0 = time.time()
    options = dict(config.items('event creation'))

    item = basic.EventCreationItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 1 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+float(options['dt']) )

    ###   cWBTriggerCheck
    task = item.tasks[0]
    assert( task.expiration == t0+float(options['dt']) )
    assert( task.emailOnSuccess == options['email on success'].split() )
    assert( task.emailOnFailure == options['email on failure'].split() )
    assert( task.emailOnException == options['email on exception'].split() )

    print "        WARNING: cWBTriggerCheck Task.execute() not implemented and not tested"
#    raise NotImplementedError("actually test Task.execute() for this Item")

    ### olib
    graceid = 'FakeEvent'
    pipeline = 'LIB'
    alert = {
        'uid' : graceid,
        'object' : {'pipeline' : pipeline,}
        }
    t0 = time.time()
    options = dict(config.items('event creation'))

    item = basic.EventCreationItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 1 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+float(options['dt']) )

    ###   oLIBTriggercheck
    task = item.tasks[0]
    assert( task.expiration == t0+float(options['dt']) )
    assert( task.emailOnSuccess == options['email on success'].split() )
    assert( task.emailOnFailure == options['email on failure'].split() )
    assert( task.emailOnException == options['email on exception'].split() )

    print "        WARNING: oLIBTriggerCheck Task.execute() not implemented and not tested"
#    raise NotImplementedError("actually test Task.execute() for this Item")

    ### gstlal
    for pipeline in ['gstlal', 'gstlal-spiir', 'MBTAOnline', 'pycbc']:
        graceid = 'FakeEvent'
        alert = {
            'uid' : graceid,
            'object' : {'pipeline' : pipeline,},
            }
        t0 = time.time()
        options = dict(config.items('event creation'))

        item = basic.EventCreationItem( alert, t0, options, gdb, annotate=annotate )
        assert( item.graceid == graceid )
        assert( item.annotate == annotate )
        assert( item.complete == False )
        assert( len(item.tasks) == 2 )
        assert( len(item.completedTasks) == 0 )
        assert( item.expiration == t0+float(options['dt']) )

        tasks = dict( (task.name, task) for task in item.tasks )
        coinc = tasks['cbcCoinc']
        psd   = tasks['cbcPSD']
        ###   cbcCoincCheck
        assert( coinc.expiration == t0+float(options['dt']) )
        assert( coinc.emailOnSuccess == options['email on success'].split() )
        assert( coinc.emailOnFailure == options['email on failure'].split() )
        assert( coinc.emailOnException == options['email on exception'].split() )
        print "        WARNING: cbcCoincCheck Task.execute() not implemented and not tested"

        ###   cbcPSDCheck
        assert( psd.expiration == t0+float(options['dt']) )
        assert( psd.emailOnSuccess == options['email on success'].split() )
        assert( psd.emailOnFailure == options['email on failure'].split() )
        assert( psd.emailOnException == options['email on exception'].split() )
        print "        WARNING: cbcPSDCheck Task.execute() not implemented and not tested"

    #--------------------
    # CreateRateItem
    #--------------------
    print "    CreateRateItem"

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid,
        'object' : {'pipeline': 'pipeline',
                    'group' : 'group',
                    'search' : 'search',
                   },
        }
    t0 = time.time()
    options = dict(config.items('creation rate'))

    item = basic.CreateRateItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 1 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+float(options['dt']) )

    ### createRateCheck
    task = item.tasks[0]
    assert( task.pipeline == "pipeline" )
    assert( task.group == "group" )
    assert( task.search == "search" )
    assert( task.expiration == t0+float(options['dt']) )
    assert( task.pWin == float(options['win+']) )
    assert( task.mWin == float(options['win-']) )
    assert( task.emailOnSuccess == options['email on success'].split() )
    assert( task.emailOnFailure == options['email on failure'].split() )
    assert( task.emailOnException == options['email on exception'].split() )

    ### check again when search is not specified
    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid,
        'object': {'pipeline': 'pipeline',
                   'group' : 'group',
                  },
        }
    t0 = time.time()
    options = dict(config.items('creation rate'))

    item = basic.CreateRateItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 1 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+float(options['dt']) )

    ###   createRateCheck
    task = item.tasks[0]
    assert( task.pipeline == "pipeline" )
    assert( task.group == "group" )
    assert( task.search == None )
    assert( task.expiration == t0+float(options['dt']) )
    assert( task.emailOnSuccess == options['email on success'].split() )
    assert( task.emailOnFailure == options['email on failure'].split() )
    assert( task.emailOnException == options['email on exception'].split() )
    print "        WARNING: CreateRateCheck Task.execute() not implemented and not tested"
#    raise NotImplementedError("actually test Task.execute() for this Item")

    #--------------------
    # LocalRateItem
    #--------------------
    print "    LocalRateItem"

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid,
        'object' : {'pipeline' : 'pipeline',
                    'group' : 'group',
                    'search' : 'search',
                   },
        }
    t0 = time.time()
    options = dict(config.items('local rate'))

    item = basic.LocalRateItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 1 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+float(options['dt']) )

    ### localRateCheck
    task = item.tasks[0]
    assert( task.pipeline == "pipeline" )
    assert( task.group == "group" )
    assert( task.search == "search" )
    assert( task.expiration == t0+float(options['dt']) )
    assert( task.pWin == float(options['win+']) )
    assert( task.mWin == float(options['win-']) )
    assert( task.emailOnSuccess == options['email on success'].split() )
    assert( task.emailOnFailure == options['email on failure'].split() )
    assert( task.emailOnException == options['email on exception'].split() )

    ### check again when search is not specified
    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid,
        'object' : {'pipeline': 'pipeline',
                    'group' : 'group',
                   },
        }
    t0 = time.time()
    options = dict(config.items('local rate'))

    item = basic.LocalRateItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 1 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+float(options['dt']) )

    ###   localRateCheck
    task = item.tasks[0]
    assert( task.pipeline == "pipeline" )
    assert( task.group == "group" )
    assert( task.search == None )
    assert( task.expiration == t0+float(options['dt']) )
    assert( task.emailOnSuccess == options['email on success'].split() )
    assert( task.emailOnFailure == options['email on failure'].split() )
    assert( task.emailOnException == options['email on exception'].split() )
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
    options = dict(config.items('far'))

    item = basic.FARItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 1 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+float(options['dt']) )

    ###   FARCheck
    task = item.tasks[0]
    assert( task.minFAR == float(options['min far']) )
    assert( task.maxFAR == float(options['max far']) )
    assert( task.expiration == t0+float(options['dt']) )
    assert( task.emailOnSuccess == options['email on success'].split() )
    assert( task.emailOnFailure == options['email on failure'].split() )
    assert( task.emailOnException == options['email on exception'].split() )

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
    options = dict(config.items('external triggers'))

    item = basic.ExternalTriggersItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 1 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+float(options['dt']) )

    ###   externalTriggersCheck
    task = item.tasks[0]
    assert( task.expiration == t0+float(options['dt']) )
    assert( task.emailOnSuccess == options['email on success'].split() )
    assert( task.emailOnFailure == options['email on failure'].split() )
    assert( task.emailOnException == options['email on exception'].split() )
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
    options = dict(config.items('unblind injections'))

    item = basic.UnblindInjectionsItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 1 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+float(options['dt']) )

    ###   unblindInjectionsCheck
    task = item.tasks[0]
    assert( task.expiration == t0+float(options['dt']) )
    assert( task.emailOnSuccess == options['email on success'].split() )
    assert( task.emailOnFailure == options['email on failure'].split() )
    assert( task.emailOnException == options['email on exception'].split() )
    print "        WARNING: unblindInjectionsCheck Task.execute() not implemented and not tested"
#    raise NotImplementedError("actually test Task.execute() for this Item")

    print "    basic.py passed all tests sucessfully!"

#-------------------------------------------------

'''
if opts.approvalProcessor:
    print "testing basic/approvalProcessor.py"

    raise NotImplementedError

    #--------------------
    # ApprovalProcessroPrelimDQItem
    #--------------------
    print "    ApprovalProcessorPrelimDQItem"

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid
        }
    t0 = time.time()
    options = dict(config.items('approval processor prelim dq'))

    item = approvalProcessor.ApprovalProcessorPrelimDQItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 1 ) ### NOTE: only using "far dt" right now
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+float(options['dt']) )

    ### check tasks
    tasks = dict( (task.name, task) for task in item.tasks )

    ###   approvalProcessorFARCheck
    far = tasks['approvalProcessorFAR']
    assert( far.expiration == t0+float(options['dt']) )
    assert( far.emailOnSuccess == options['email on success'].split() )
    assert( far.emailOnFailure == options['email on failure'].split() )
    assert( far.emailOnException == options['email on exception'].split() )
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
    options = dict(config.items('approval processor segdb'))

    item = approvalProcessor.ApprovalProcessorSegDBItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 2 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+float(options['dt']) )

    ### check tasks
    tasks = dict( (task.name, task) for task in item.tasks )
    flags = tasks['approvalProcessorSegDBFlags']
    finish = tasks['approvalProcessorSegDBFinish']
    ###   approvalProcessorSegDBFlagsCheck
    assert( flags.expiration == t0+float(options['flags dt']) )
    assert( flags.emailOnSuccess == options['email on success'].split() )
    assert( flags.emailOnFailure == options['email on failure'].split() )
    assert( flags.emailOnException == options['email on exception'].split() )
    assert( flags.flags == ['H1:DMT-ANALYSIS_READY:1'] )
    print "        WARNING: approvalProcessorFARCheck Task.execute() not implemented and not tested"

    ###   approvalProcessorSegDBFinishCheck
    assert( finish.expiration == t0+float(options['finish dt']) )
    assert( finish.emailOnSuccess == options['email on success'].split() )
    assert( finish.emailOnFailure == options['email on failure'].split() )
    assert( finish.emailOnException == options['email on exception'].split() )
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
    options = dict(config.items('approval processor idq'))

    item = approvalProcessor.ApprovalProcessoriDQItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 1 )
    assert( len(item.completedTasks) == 0 )
    assert( item.ifo == "H1" )
    assert( item.expiration == t0+float(options['dt']) )

    ###   approvalProcessoriDQglitchFAPCheck
    task = item.tasks[0]
    assert( task.expiration == t0+float(options['dt']) )
    assert( task.emailOnSuccess == options['email on success'].split() )
    assert( task.emailOnFailure == options['email on failure'].split() )
    assert( task.emailOnException == options['email on exception'].split() )
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
    options = dict(config.items('approval processor voevent'))

    item = approvalProcessor.ApprovalProcessorVOEventItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 2 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+float(options['dt']) )

    ### check tasks
    tasks = dict( (task.name, task) for task in item.tasks )
    create = tasks['approvalProcessorVOEventCreation']
    distrb = tasks['approvalProcessorVOEventDistribution']
    ###   approvalProcessorVOEventCreationCheck
    assert( create.expiration == t0+float(options['dt']) )
    assert( create.emailOnSuccess == options['email on success'].split() )
    assert( create.emailOnFailure == options['email on failure'].split() )
    assert( create.emailOnException == options['email on exception'].split() )
    print "        WARNING: approvalProcessorVOEventCreationCheck Task.execute() not implemented and not tested"

    ###   approvalProcessorVOEventDistributionCheck
    assert( distrb.expiration == t0+float(options['dt']) )
    assert( distrib.emailOnSuccess == options['email on success'].split() )
    assert( distrib.emailOnFailure == options['email on failure'].split() )
    assert( distrib.emailOnException == options['email on exception'].split() )
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
    options = dict(config.items('approval processor gcn'))

    item = approvalProcessor.ApprovalProcessorGCNItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 2 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+float(options['dt']) )

    ### check tasks
    tasks = dict( (task.name, task) for task in item.tasks )
    create = tasks['approvalProcessorGCNCreation']
    distrb = tasks['approvalProcessorGCNDistribution']
    ###   approvalProcessorGCNCreationCheck
    assert( create.expiration == t0+float(options['dt']) )
    assert( create.emailOnSuccess == options['email on success'].split() )
    assert( create.emailOnFailure == options['email on failure'].split() )
    assert( create.emailOnException == options['email on exception'].split() )
    print "        WARNING: approvalProcessorGCNCreationCheck Task.execute() not implemented and not tested"

    ###   approvalProcessorGCNDistributionCheck
    assert( distrib.expiration == t0+float(options['dt']) )
    assert( distrib.emailOnSuccess == options['email on success'].split() )
    assert( distrib.emailOnFailure == options['email on failure'].split() )
    assert( distrib.emailOnException == options['email on exception'].split() )
    print "        WARNING: approvalProcessorGCNdistributionCheck Task.execute() not implemented and not tested"

    print "    approvalProcessor.py passed all tests sucessfully!"
'''

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
    options = dict(config.items('skymap sanity'))

    item = skymaps.SkymapSanityItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.fitsname == fitsname )
    assert( item.complete == False )
    assert( len(item.tasks) == 1 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+float(options['dt']) )

    ###   skymapSanityCheck
    task = item.tasks[0]
    assert( task.fitsname == fitsname )
    assert( task.expiration == t0+float(options['dt']) ) 
    assert( task.emailOnSuccess == options['email on success'].split() )
    assert( task.emailOnFailure == options['email on failure'].split() )
    assert( task.emailOnException == options['email on exception'].split() )

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
        'object' : {'tag_names':[]},
        }
    t0 = time.time()
    options = dict(config.items('plot skymap'))

    item = skymaps.PlotSkymapItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.fitsname == fitsname )
    assert( item.tagnames == [] )
    assert( item.complete == False )
    assert( len(item.tasks) == 1 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+float(options['dt']) )

    ###   plotSkymapCheck
    task = item.tasks[0]
    assert( task.fitsname == fitsname )
    assert( task.expiration == t0+float(options['dt']) )
    assert( task.emailOnSuccess == options['email on success'].split() )
    assert( task.emailOnFailure == options['email on failure'].split() )
    assert( task.emailOnException == options['email on exception'].split() )

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
        'object' : {'tag_names':[]},
        }
    t0 = time.time()
    options = dict(config.items('skyviewer'))

    item = skymaps.SkyviewerItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.fitsname == fitsname )
    assert( item.tagnames == [] )
    assert( item.complete == False )
    assert( len(item.tasks) == 1 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+float(options['dt']) )

    ###   skyviewerCheck
    task = item.tasks[0]
    assert( task.fitsname == fitsname )
    assert( task.expiration == t0+float(options['dt']) )
    assert( task.emailOnSuccess == options['email on success'].split() )
    assert( task.emailOnFailure == options['email on failure'].split() )
    assert( task.emailOnException == options['email on exception'].split() )

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
        'object' : {'tag_names':['sky_loc']},
        }
    t0 = time.time()
    options = dict(config.items('snglFITS start'))

    item = skymapSummary.SnglFITSStartItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.fitsname == filename )
#    assert( item.tagnames == alert['object']['tag_names'] ) ### FIXME: this should fail...
    assert( item.complete == False )
    assert( len(item.tasks) == 1 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+float(options['dt']) )

    ###   skymapSummaryStartCheck
    task = item.tasks[0]
    assert( task.fitsname == filename )
#    assert( task.tagnames == alert['object']['tag_names'] )
    assert( task.expiration == t0+float(options['dt']) )
    assert( task.emailOnSuccess == options['email on success'].split() )
    assert( task.emailOnFailure == options['email on failure'].split() )
    assert( task.emailOnException == options['email on exception'].split() )

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
        'object' : {'tag_names' : []},
        }
    t0 = time.time()
    options = dict(config.items('snglFITS'))

    item = skymapSummary.SnglFITSItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.fitsname == filename )
#    assert( item.tagnames == alert['object']['tag_names'] ) ### FIXME: this should fail...
    assert( item.complete == False )
    assert( len(item.tasks) == 2 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+min(float(options['html dt']), float(options['finish dt'])) )

    ### check tasks
    tasks = dict( (task.name, task) for task in item.tasks )
    data = tasks['snglFITShtml']
    finish = tasks['snglFITSFinish']
    ###   skymapSummaryDataCheck
    assert( data.fitsname == filename )
#    assert( data.tagnames == alert['object']['tag_names'] ) ### this should fail...
    assert( data.expiration == t0+float(options['html dt']) )
    assert( data.emailOnSuccess == options['email on success'].split() )
    assert( data.emailOnFailure == options['email on failure'].split() )
    assert( data.emailOnException == options['email on exception'].split() )
    print "        WARNING: skymapSummaryDataCheck Task.execute() not implemented and not tested"

    ###   skymapSummaryFinishCheck
    assert( finish.fitsname == filename )
#    assert( finish.tagnames == alert['object']['tag_names'] ) ### this should fail...
    assert( finish.expiration == t0+float(options['finish dt']) )
    assert( finish.emailOnSuccess == options['email on success'].split() )
    assert( finish.emailOnFailure == options['email on failure'].split() )
    assert( finish.emailOnException == options['email on exception'].split() )
    print "        WARNING: skymapSummaryFinishCheck Task.execute() not implemented and not tested"

    #--------------------
    # MultFITSStartItem
    #--------------------
    print "    MultFITSStartItem"

    graceid = 'G263969' ### extracted this by hand from GraceDb -> FRAGILE!
    filenames = [fits for fits in gdb.files( graceid ).json().keys() if fits.endswith('.fits') or fits.endswith('.fits.gz')]

    alert = {
        'uid' : graceid,
        'description' : 'finished skymap summary for DOES NOT MATTER',
        'object' : {'tag_names' : []},
        }
    t0 = time.time()
    options = dict(config.items('multFITS start'))

    item = skymapSummary.MultFITSStartItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.fitsnames == filenames )
#    assert( item.tagnames == alert-'object']['tag_names'] ) ### FIXME: this should fail...
    assert( item.complete == False )
    assert( len(item.tasks) == 1 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+float(options['dt']) )

    ###   skymapSummaryStartCheck
    task = item.tasks[0]
    assert( task.fitsnames == filenames )
#    assert( task.tagnames == alert['object']['tag_names'] ) ### FIXME: this should break...
    assert( task.expiration == t0+float(options['dt']) )
    assert( task.emailOnSuccess == options['email on success'].split() )
    assert( task.emailOnFailure == options['email on failure'].split() )
    assert( task.emailOnException == options['email on exception'].split() )

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
        'object' : {'tag_names':[]},
        }
    t0 = time.time()
    options = dict(config.items('multFITS'))

    item = skymapSummary.MultFITSItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.fitsnames == filenames )
#    assert( item.tagnames == alert['object']['tag_names'] ) ### FIXME: this should fail...
    assert( item.complete == False )
    assert( len(item.tasks) == 2 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+min(float(options['html dt']), float(options['finish dt'])) )

    ### check tasks
    tasks = dict( (task.name, task) for task in item.tasks )
    data = tasks['multFITShtml']
    finish = tasks['multFITSFinish']
    ###   skymapSummaryDataCheck
#    assert( data.tagnames == alert['object']['tag_names'] ) ### this should fail...
    assert( data.expiration == t0+float(options['html dt']) )
    assert( data.emailOnSuccess == options['email on success'].split() )
    assert( data.emailOnFailure == options['email on failure'].split() )
    assert( data.emailOnException == options['email on exception'].split() )
    print "        WARNING: skymapSummaryDataCheck Task.execute() not implemented and not tested"

    ###   skymapSummaryFinishCheck
    assert( finish.fitsnames == filenames )
#    assert( finish.tagnames == alert['object']['tag_names'] ) ### this should fail...
    assert( finish.expiration == t0+float(options['finish dt']) )
    assert( finish.emailOnSuccess == options['email on success'].split() )
    assert( finish.emailOnFailure == options['email on failure'].split() )
    assert( finish.emailOnException == options['email on exception'].split() )
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
    options = dict(config.items('bayestar start'))

    item = bayestar.BayestarStartItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 1 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+float(options['dt']) )

    ###   bayestarStartCheck
    task = item.tasks[0]
    assert( task.expiration == t0+float(options['dt']) )
    assert( task.emailOnSuccess == options['email on success'].split() )
    assert( task.emailOnFailure == options['email on failure'].split() )
    assert( task.emailOnException == options['email on exception'].split() )

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
    options = dict(config.items('bayestar'))

    item = bayestar.BayestarItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 2 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+min(float(options['skymap dt']), float(options['finish dt'])) )

    ### check tasks
    tasks = dict( (task.name, task) for task in item.tasks )
    skymap = tasks['bayestarSkymap']
    finish = tasks['bayestarFinish']
    ###   bayestarSkymapCheck
    assert( skymap.expiration == t0+float(options['skymap dt']) )
    assert( skymap.emailOnSuccess == options['email on success'].split() )
    assert( skymap.emailOnFailure == options['email on failure'].split() )
    assert( skymap.emailOnException == options['email on exception'].split() )
    assert( skymap.tagnames == (options['skymap tagnames'].split() if options.has_key('skymap tagnames') else None) )
    print "        WARNING: bayestarSkymapCheck Task.execute() not implemented and not tested"

    ###   bayestarFinishItem
    assert( finish.expiration == t0+float(options['finish dt']) )
    assert( finish.emailOnSuccess == options['email on success'].split() )
    assert( finish.emailOnFailure == options['email on failure'].split() )
    assert( finish.emailOnException == options['email on exception'].split() )
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
    options = dict(config.items('em bright'))

    item = embright.EMBrightItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 1 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+float(options['dt']) )

    ###   emBrightCheck
    task = item.tasks[0]
    assert( task.expiration == t0+float(options['dt']) )
    assert( task.emailOnSuccess == options['email on success'].split() )
    assert( task.emailOnFailure == options['email on failure'].split() )
    assert( task.emailOnException == options['email on exception'].split() )

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
    options = dict(config.items('bayeswave pe start'))

    item = bayeswavePE.BayesWavePEStartItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 1 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+float(options['dt']) )

    ###   bayeswavePEStartCheck
    task = item.tasks[0]
    assert( task.expiration == t0+float(options['dt']) )
    assert( task.emailOnSuccess == options['email on success'].split() )
    assert( task.emailOnFailure == options['email on failure'].split() )
    assert( task.emailOnException == options['email on exception'].split() )

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
    options = dict(config.items('bayeswave pe'))

    item = bayeswavePE.BayesWavePEItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 4 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+min(float(options['post samp dt']), float(options['estimate dt']), float(options['bayes factor dt']), float(options['skymap dt'])) )

    ### check tasks
    tasks = dict( (task.name, task) for task in item.tasks )
    postSamp = tasks['bayeswavePEPostSamp']
    baysFact = tasks['bayeswavePEBayesFactors']
    estimate = tasks['bayeswavePEEstimate']
    skymap = tasks['bayeswavePESkymap']

    ###   bayeswavePEPostSampCheck
    assert( postSamp.expiration == t0+float(options['post samp dt']) )
    assert( postSamp.emailOnSuccess == options['email on success'].split() )
    assert( postSamp.emailOnFailure == options['email on failure'].split() )
    assert( postSamp.emailOnException == options['email on exception'].split() )
    print "        WARNING: bayeswavePEPostSampCheck Task.execute() not implemented and not tested"

    ###   bayeswavePEBayesFactorsCheck
    assert( baysFact.expiration == t0+float(options['bayes factor dt']) )
    assert( baysFact.emailOnSuccess == options['email on success'].split() )
    assert( baysFact.emailOnFailure == options['email on failure'].split() )
    assert( baysFact.emailOnException == options['email on exception'].split() )
    print "        WARNING: bayeswavePEBayesFactorCheck Task.execute() not implemented and not tested"

    ###   bayeswavePEEstimateCheck
    assert( estimate.expiration == t0+float(options['estimate dt']) )
    assert( estimate.emailOnSuccess == options['email on success'].split() )
    assert( estimate.emailOnFailure == options['email on failure'].split() )
    assert( estimate.emailOnException == options['email on exception'].split() )
    print "        WARNING: bayeswavePEEstimateCheck Task.execute() not implemented and not tested"

    ###   bayeswavePESkymapCheck
    assert( skymap.expiration == t0+float(options['skymap dt']) )
    assert( skymap.emailOnSuccess == options['email on success'].split() )
    assert( skymap.emailOnFailure == options['email on failure'].split() )
    assert( skymap.emailOnException == options['email on exception'].split() )
    assert( skymap.tagnames == (options['skymap tagnames'].split() if options.has_key('skymap tagnames') else None) )
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
    options = dict(config.items('cwb pe'))

    item = cwbPE.CWBPEItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 3 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+min(float(options['ced dt']), float(options['estimate dt']), float(options['skymap dt'])) )

    ### check tasks
    tasks = dict( (task.name, task) for task in item.tasks )
    ced = tasks['cWBPECED']
    est = tasks['cWBPEEstimate']
    sky = tasks['cWBPESkymap']

    ###   cWBPECEDCheck
    assert( ced.expiration == t0+float(options['ced dt']) )
    assert( ced.emailOnSuccess == options['email on success'].split() )
    assert( ced.emailOnFailure == options['email on failure'].split() )
    assert( ced.emailOnException == options['email on exception'].split() )
    print "        WARNING: cWBCEDCheck Task.execute() not implemented and not tested"

    ###   cWBPEEstimateCheck
    assert( est.expiration == t0+float(options['estimate dt']) )
    assert( est.emailOnSuccess == options['email on success'].split() )
    assert( est.emailOnFailure == options['email on failure'].split() )
    assert( est.emailOnException == options['email on exception'].split() )
    print "        WARNING: cWBPEEstimateCheck Task.execute() not implemented and not tested"

    ###   cWBPESkymapCheck
    assert( sky.expiration == t0+float(options['skymap dt']) )
    assert( sky.emailOnSuccess == options['email on success'].split() )
    assert( sky.emailOnFailure == options['email on failure'].split() )
    assert( sky.emailOnException == options['email on exception'].split() )
    assert( sky.tagnames == (options['skymap tagnames'].split() if options.has_key('skymap tagnames') else None) )
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
    options = dict(config.items('lib pe start'))

    item = libPE.LIBPEStartItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 1 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+float(options['dt']) )

    ###   libPEStartCheck
    task = item.tasks[0]
    assert( task.expiration == t0+float(options['dt']) )
    assert( task.emailOnSuccess == options['email on success'].split() )
    assert( task.emailOnFailure == options['email on failure'].split() )
    assert( task.emailOnException == options['email on exception'].split() )
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
    options = dict(config.items('lib pe'))

    item = libPE.LIBPEItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 4 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+min(float(options['bayes factor dt']), float(options['post samp dt']), float(options['skymap dt']), float(options['finish dt'])) )

    ### check tasks
    tasks = dict( (task.name, task) for task in item.tasks )
    bysFct = tasks['libPEBayesFactors']
    pstSmp = tasks['libPEPostSamp']
    skymap = tasks['libPESkymap']
    finish = tasks['libPEFinish']

    ###   libPEBayesFactorsCheck
    assert( bysFct.expiration == t0+float(options['bayes factor dt']) )
    assert( bysFct.emailOnSuccess == options['email on success'].split() )
    assert( bysFct.emailOnFailure == options['email on failure'].split() )
    assert( bysFct.emailOnException == options['email on exception'].split() )
    print "        WARNING: libPEBayesFactorsCheck Task.execute() not implemented and not tested"

    ###   libPEPostSampCheck
    assert( pstSmp.expiration == t0+float(options['post samp dt']) )
    assert( pstSmp.emailOnSuccess == options['email on success'].split() )
    assert( pstSmp.emailOnFailure == options['email on failure'].split() )
    assert( pstSmp.emailOnException == options['email on exception'].split() )
    print "        WARNING: libPEPostSampCheck Task.execute() not implemented and not tested"

    ###   libPESkymapCheck
    assert( skymap.expiration == t0+float(options['skymap dt']) )
    assert( skymap.emailOnSuccess == options['email on success'].split() )
    assert( skymap.emailOnFailure == options['email on failure'].split() )
    assert( skymap.emailOnException == options['email on exception'].split() )
    assert( skymap.tagnames == (options['skymap tagnames'].split() if options.has_key('skymap tagnames') else None) )
    print "        WARNING: libPESkymapCheck Task.execute() not implemented and not tested"

    ###   libPEFinishCheck
    assert( finish.expiration == t0+float(options['finish dt']) )
    assert( finish.emailOnSuccess == options['email on success'].split() )
    assert( finish.emailOnFailure == options['email on failure'].split() )
    assert( finish.emailOnException == options['email on exception'].split() )
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
    options = dict(config.items('lalinf start'))

    item = lalinf.LALInfStartItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 1 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+float(options['dt']) )

    ###   lalinfStartCheck
    task = item.tasks[0]
    assert( task.expiration == t0+float(options['dt']) )
    assert( task.emailOnSuccess == options['email on success'].split() )
    assert( task.emailOnFailure == options['email on failure'].split() )
    assert( task.emailOnException == options['email on exception'].split() )
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
    options = dict(config.items('lalinf'))

    item = lalinf.LALInfItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.completedTasks) == 0 )
#    assert( len(item.tasks) == 3 )
#    assert( item.expiration == t0+min(float(options['post samp dt']), float(options['skymap dt']), float(options['finish dt'])) )
    assert( len(item.tasks) == 2 ) ### post samp is commented out...
    assert( item.expiration == t0+min(float(options['skymap dt']), float(options['finish dt'])) )

    ### check tasks
    tasks = dict( (task.name, task) for task in item.tasks )
#    pstSmp = tasks['lalinfPostSamp']
    skymap = tasks['lalinfSkymap']
    finish = tasks['lalinfFinish']

    ###   lalinfPostSampCheck
#    assert( pstSmp.expiration == t0+float(options['post samp dt']) )
#    assert( pstSmp.emailOnSuccess == options['email on success'].split() )
#    assert( pstSmp.emailOnFailure == options['email on failure'].split() )
#    assert( pstSmp.emailOnException == options['email on exception'].split() )
#    print "        WARNING: lalinfPostSampCheck Task.execute() not implemented and not tested"

    ###   lalinfSkymapCheck
    assert( skymap.expiration == t0+float(options['skymap dt']) )
    assert( skymap.emailOnSuccess == options['email on success'].split() )
    assert( skymap.emailOnFailure == options['email on failure'].split() )
    assert( skymap.emailOnException == options['email on exception'].split() )
    assert( skymap.tagnames == (options['skymap tagnames'].split() if options.has_key('skymap tagnames') else None) )
    print "        WARNING: lalinfSkymapCheck Task.execute() not implemented and not tested"

    ###   lalinfFinishCheck
    assert( finish.expiration == t0+float(options['finish dt']) )
    assert( finish.emailOnSuccess == options['email on success'].split() )
    assert( finish.emailOnFailure == options['email on failure'].split() )
    assert( finish.emailOnException == options['email on exception'].split() )
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
    options = dict(config.items('lldqReport'))

    item = dq.LLDQReportItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 1 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+float(options['dt']) )

    ###   dqSummaryCheck
    task = item.tasks[0]
    assert( task.expiration == t0+float(options['dt']) )
    assert( task.emailOnSuccess == options['email on success'].split() )
    assert( task.emailOnFailure == options['email on failure'].split() )
    assert( task.emailOnException == options['email on exception'].split() )
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
    options = dict(config.items('idq start'))

    item = idq.IDQStartItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 2 ) ### there are 2 ifos
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+float(options['dt']) )
    assert( item.ifos == options['ifos'].split() )

    ###   idqStartCheck
    for task in item.tasks:
        assert( task.expiration == t0++float(options['dt']) )
        assert( task.emailOnSuccess == options['email on success'].split() )
        assert( task.emailOnFailure == options['email on failure'].split() )
        assert( task.emailOnException == options['email on exception'].split() )
    
    print "        WARNING: idqStartCheck Task.execute() not implemented and not tested"

    #--------------------
    # IDQItem
    #--------------------
    print "    IDQItem"

    ifo = 'H1'

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid,
        'description' : 'blah blah blah %s'%ifo,
        }
    t0 = time.time()
    options = dict(config.items('idq'))

    item = idq.IDQItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 14*len(options['classifiers'].split())+1 ) ### (13 checks per classifier and 2 classifiers) + (1 finish check)
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+min([float(options[key]) for key in options.keys() if "dt" in key]) )
    assert( item.ifo == ifo ) ### set by alert!
    assert( item.classifiers == options['classifiers'].split() )

    ### check tasks
    for classifier in item.classifiers:
        tasks = dict( (task.name, task) for task in item.tasks if (task.name!='idqFinish') and (task.classifier==classifier) )

        tables = tasks['idqTables']
        glchFAP = tasks['idqGlitchFAP']
        rank = tasks['idqRank']
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
        assert( tables.expiration == t0++float(options['tables dt']) )
        assert( tables.emailOnSuccess == options['email on success'].split() )
        assert( tables.emailOnFailure == options['email on failure'].split() )
        assert( tables.emailOnException == options['email on exception'].split() )
        assert( tables.ifo == ifo )
        print "        WARNING: idqTablesCheck Task.execute() not implemented and not tested"

        ###   idqGltichFAPCheck
        assert( glchFAP.expiration == t0++float(options['glitch fap dt']) )
        assert( glchFAP.emailOnSuccess == options['email on success'].split() )
        assert( glchFAP.emailOnFailure == options['email on failure'].split() )
        assert( glchFAP.emailOnException == options['email on exception'].split() )
        assert( glchFAP.ifo == ifo )
        print "        WARNING: idqGlitchFAPCheck Task.execute() not implemented and not tested"

        ###   idqRankCheck
        assert( rank.expiration == t0++float(options['glitch fap dt']) )
        assert( rank.emailOnSuccess == options['email on success'].split() )
        assert( rank.emailOnFailure == options['email on failure'].split() )
        assert( rank.emailOnException == options['email on exception'].split() )
        assert( rank.ifo == ifo )
        print "        WARNING: idqGlitchFAPCheck Task.execute() not implemented and not tested"

        ###   idqFAPFrameCheck
        assert( fapFram.expiration == t0++float(options['fap frame dt']) )
        assert( fapFram.emailOnSuccess == options['email on success'].split() )
        assert( fapFram.emailOnFailure == options['email on failure'].split() )
        assert( fapFram.emailOnException == options['email on exception'].split() )
        assert( fapFram.ifo == ifo )
        print "        WARNING: idqFAPFrameCheck Task.execute() not implemented and not tested"
 
        ###   idqRankFrameCheck
        assert( rnkFram.expiration == t0++float(options['rank frame dt']) )
        assert( rnkFram.emailOnSuccess == options['email on success'].split() )
        assert( rnkFram.emailOnFailure == options['email on failure'].split() )
        assert( rnkFram.emailOnException == options['email on exception'].split() )
        assert( rnkFram.ifo == ifo )
        print "        WARNING: idqRankFrameCheck Task.execute() not implemented and not tested"

        ###   idqTimeseriesPlotCheck
        assert( timesrs.expiration == t0++float(options['timeseries plot dt']) )
        assert( timesrs.emailOnSuccess == options['email on success'].split() )
        assert( timesrs.emailOnFailure == options['email on failure'].split() )
        assert( timesrs.emailOnException == options['email on exception'].split() )
        assert( timesrs.ifo == ifo )
        print "        WARNING: idqTimeseriesPlotCheck Task.execute() not implemented and not tested"

        ###   idqActiveChanCheck
        assert( actvChn.expiration == t0++float(options['active chan dt']) )
        assert( actvChn.emailOnSuccess == options['email on success'].split() )
        assert( actvChn.emailOnFailure == options['email on failure'].split() )
        assert( actvChn.emailOnException == options['email on exception'].split() )
        assert( actvChn.ifo == ifo )
        print "        WARNING: idqActiveChanCheck Task.execute() not implemented and not tested"

        ###   idqActiveChanPlotCheck
        assert( actvChnPlt.expiration == t0++float(options['active chan plot dt']) )
        assert( actvChnPlt.emailOnSuccess == options['email on success'].split() )
        assert( actvChnPlt.emailOnFailure == options['email on failure'].split() )
        assert( actvChnPlt.emailOnException == options['email on exception'].split() )
        assert( actvChnPlt.ifo == ifo )
        print "        WARNING: idqActiveChanPlotCheck Task.execute() not implemented and not tested"

        ###   idqCalibrationCheck
        assert( calibration.expiration == t0++float(options['calib dt']) )
        assert( calibration.emailOnSuccess == options['email on success'].split() )
        assert( calibration.emailOnFailure == options['email on failure'].split() )
        assert( calibration.emailOnException == options['email on exception'].split() )
        assert( calibration.ifo == ifo )
        print "        WARNING: idqCalibrationCheck Task.execute() not implemented and not tested"

        ###   idqCalibrationPlotCheck
        assert( calibrationPlt.expiration == t0++float(options['calib plot dt']) )
        assert( calibrationPlt.emailOnSuccess == options['email on success'].split() )
        assert( calibrationPlt.emailOnFailure == options['email on failure'].split() )
        assert( calibrationPlt.emailOnException == options['email on exception'].split() )
        assert( calibrationPlt.ifo == ifo )
        print "        WARNING: idqCalibrationPlotCheck Task.execute() not implemented and not tested"

        ###   idqROCCheck
        assert( roc.expiration == t0++float(options['roc dt']) )
        assert( roc.emailOnSuccess == options['email on success'].split() )
        assert( roc.emailOnFailure == options['email on failure'].split() )
        assert( roc.emailOnException == options['email on exception'].split() )
        assert( roc.ifo == ifo )
        print "        WARNING: idqROCCheck Task.execute() not implemented and not tested"

        ###   idqROCPlotCheck
        assert( rocPlt.expiration == t0++float(options['roc plot dt']) )
        assert( rocPlt.emailOnSuccess == options['email on success'].split() )
        assert( rocPlt.emailOnFailure == options['email on failure'].split() )
        assert( rocPlt.emailOnException == options['email on exception'].split() )
        assert( rocPlt.ifo == ifo )
        print "        WARNING: idqROCPlotCheck Task.execute() not implemented and not tested"

        ###   idqCalibStatsCheck
        assert( calibStats.expiration == t0++float(options['calib stats dt']) )
        assert( calibStats.emailOnSuccess == options['email on success'].split() )
        assert( calibStats.emailOnFailure == options['email on failure'].split() )
        assert( calibStats.emailOnException == options['email on exception'].split() )
        assert( calibStats.ifo == ifo )
        print "        WARNING: idqCalibStatsCheck Task.execute() not implemented and not tested"

        ###   idqTrainStatsCheck
        assert( trainStats.expiration == t0++float(options['train stats dt']) )
        assert( trainStats.emailOnSuccess == options['email on success'].split() )
        assert( trainStats.emailOnFailure == options['email on failure'].split() )
        assert( trainStats.emailOnException == options['email on exception'].split() )
        assert( trainStats.ifo == ifo )
        print "        WARNING: idqTrainStatsCheck Task.execute() not implemented and not tested"

    task = [task for task in item.tasks if task.name=='idqFinish'][0]
    assert( task.expiration == t0+float(options['finish dt']) )
    assert( task.emailOnSuccess == options['email on success'].split() )
    assert( task.emailOnFailure == options['email on failure'].split() )
    assert( task.emailOnException == options['email on exception'].split() )
    assert( task.ifo == ifo )

    print "    idq.py passed all tests sucessfully!"

#-------------------------------------------------

if opts.omegaScan:
    print "testing dq/omegaScan.py"

    #--------------------
    # L1OmegaScanStartItem
    #--------------------
    print "    L1OmegaScanStartItem"

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid,
        }
    t0 = time.time()
    options = dict(config.items('l1 omega scan start'))
    chansets = options['chansets'].split()

    item = omegaScan.L1OmegaScanStartItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 1 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+float(options['dt']) )
    assert( item.chansets == chansets )

    ###   omegaScanStartCheck
    task = item.tasks[0] ### only one task

    assert( task.expiration == t0+float(options['dt']) )
    assert( task.emailOnSuccess == options['email on success'].split() )
    assert( task.emailOnFailure == options['email on failure'].split() )
    assert( task.emailOnException == options['email on exception'].split() )
    assert( task.chansets == chansets )
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
    options = dict(config.items('l1 omega scan'))

    item = omegaScan.L1OmegaScanItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == len(chansets)+1 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+min(float(options['data dt']), float(options['finish dt'])) )
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
        assert( task.expiration == t0+float(options['data dt']) )
        assert( task.emailOnSuccess == options['email on success'].split() )
        assert( task.emailOnFailure == options['email on failure'].split() )
        assert( task.emailOnException == options['email on exception'].split() )
        assert( task.chanset == chanset )
    print "        WARNING: omegaScanDataCheck Task.execute() not implemented and not tested"

    ###   omegaScanFinishCheck
    assert( finishTask.expiration == t0+float(options['finish dt']) )
    assert( finishTask.emailOnSuccess == options['email on success'].split() )
    assert( finishTask.emailOnFailure == options['email on failure'].split() )
    assert( finishTask.emailOnException == options['email on exception'].split() )
    assert( finishTask.chansets == chansets )
    print "        WARNING: omegaScanFinishCheck Task.execute() not implemented and not tested"

    #--------------------
    # H1OmegaScanStartItem
    #--------------------
    print "    H1OmegaScanStartItem"

    graceid = 'FakeEvent'
    alert = {
        'uid' : graceid,
        }
    t0 = time.time()
    options = dict(config.items('h1 omega scan start'))
    chansets = options['chansets'].split()

    item = omegaScan.H1OmegaScanStartItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 1 ) ### 2 ifos
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+float(options['dt']) )
    assert( item.chansets == chansets )

    ###   omegaScanStartCheck
    task = item.tasks[0]

    assert( task.expiration == t0+float(options['dt']) )
    assert( task.emailOnSuccess == options['email on success'].split() )
    assert( task.emailOnFailure == options['email on failure'].split() )
    assert( task.emailOnException == options['email on exception'].split() )
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
    options = dict(config.items('h1 omega scan'))

    item = omegaScan.H1OmegaScanItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == len(chansets)+1 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+min(float(options['data dt']), float(options['finish dt'])) )
    assert( item.chansets == chansets )

    ### check tasks
    dataTasks = [ task for task in item.tasks if task.name=='omegaScanData' ]
    assert( len(dataTasks)==len(chansets) )

    finishTask = [task for task in item.tasks if task.name=='omegaScanFinish']
    assert( len(finishTask)==1 )
    finishTask = finishTask[0]

    ###   omegaScanDataCheck
    for chanset, task in zip(chansets, dataTasks):
        assert( task.expiration == t0+float(options['data dt']) )
        assert( task.emailOnSuccess == options['email on success'].split() )
        assert( task.emailOnFailure == options['email on failure'].split() )
        assert( task.emailOnException == options['email on exception'].split() )
        assert( task.chanset == chanset )
    print "        WARNING: omegaScanDataCheck Task.execute() not implemented and not tested"

    ###   omegaScanFinishCheck
    assert( finishTask.expiration == t0+float(options['finish dt']) )
    assert( task.emailOnSuccess == options['email on success'].split() )
    assert( task.emailOnFailure == options['email on failure'].split() )
    assert( task.emailOnException == options['email on exception'].split() )
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
    options = dict(config.items('segdb2grcdb start'))

    item = segDB2grcDB.SegDB2GrcDBStartItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 1 )
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+float(options['dt']) )

    ###   segDB2grcDBStartCheck
    task = item.tasks[0]
    assert( task.expiration == t0+float(options['dt']) )
    assert( task.emailOnSuccess == options['email on success'].split() )
    assert( task.emailOnFailure == options['email on failure'].split() )
    assert( task.emailOnException == options['email on exception'].split() )
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
    options = dict(config.items('segdb2grcdb'))

    item = segDB2grcDB.SegDB2GrcDBItem( alert, t0, options, gdb, annotate=annotate )
    assert( item.graceid == graceid )
    assert( item.annotate == annotate )
    assert( item.complete == False )
    assert( len(item.tasks) == 4 ) ### no veto defs ...
    assert( len(item.completedTasks) == 0 )
    assert( item.expiration == t0+min(float(options['flags dt']), float(options['veto def dt']), float(options['any dt']), float(options['finish dt'])) )

    ###   segDB2grcDBFlagsCheck
    for flag, task in zip(options['flags'].split(), [task for task in item.tasks if task.name=='segDb2grcDBFlag']):
        assert( task.expiration == t0+float(options['flags dt']) )
        assert( task.emailOnSuccess == options['email on success'].split() )
        assert( task.emailOnFailure == options['email on failure'].split() )
        assert( task.emailOnException == options['email on exception'].split() )
        assert( task.flag == flag )
    print "        WARNING: segDB2grcDBFlagsCheck Task.execute() not implemented and not tested"

    ###   segDB2grcDBVetoDefCheck
    for vetoDef, task in zip(options['veto defs'].split(), [task for task in item.tasks if task.name=='segDb2grcDBVetoDef']):
        assert( task.expiration == t0+float(options['veto def dt']) )
        assert( task.emailOnSuccess == options['email on success'].split() )
        assert( task.emailOnFailure == options['email on failure'].split() )
        assert( task.emailOnException == options['email on exception'].split() )
        assert( task.vetoDefs == vetoDef )
    print "        WARNING: segDB2grcDBVetoDefCheck Task.execute() not implemented and not tested"

    ###   segDB2grcDBAnyCheck
    anyseg = [task for task in item.tasks if task.name=='segDB2grcDBAny']
    assert( len(anyseg) == 1 )
    anySeg = anyseg[0]
    assert( anySeg.expiration == t0+float(options['any dt']) )
    assert( anySeg.emailOnSuccess == options['email on success'].split() )
    assert( anySeg.emailOnFailure == options['email on failure'].split() )
    assert( anySeg.emailOnException == options['email on exception'].split() )
    print "        WARNING: segDB2grcDBAnyFinishCheck Task.execute() not implemented and not tested"

    ###   segDB2grcDBFinishCheck
    finish = [task for task in item.tasks if task.name=='segDB2grcDBFinish']
    assert( len(finish) == 1 )
    finish = finish[0]
    assert( finish.expiration == t0+float(options['finish dt']) )
    assert( finish.emailOnSuccess == options['email on success'].split() )
    assert( finish.emailOnFailure == options['email on failure'].split() )
    assert( finish.emailOnException == options['email on exception'].split() )
    print "        WARNING: segDB2grcDBFinishCheck Task.execute() not implemented and not tested"

    print "    segDB2grcDB.py passed all tests sucessfully!"

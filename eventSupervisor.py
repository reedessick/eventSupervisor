description = "a module containing checks and parsing logic used within event_supervisor"
author = "reed.essick@ligo.org"

#-------------------------------------------------

def extractChildren( mod, klass ):
    """ extracts the sublcasses of klass from module """
    d = {}
    for x in dir(mod):
        attr = getattr(mod, x)
        if isinstance(attr, type) and issubclass(attr, klass):
            d[attr.name] = attr
    return d

#-------------------------------------------------

qid = {} ### queueItemDict
         ### contains mapping of names -> QueueItem objects

#-------------------------------------------------

from ligo.lvalert import lvalertMPutils as utils
import eventSupervisorUtils as esUtils

### notification and alerts
from notify import notify
qid.update( extractChildren( notify, esUtils.EventSupervisorQueueItem ) )
 
### basics
from basic import basic
qid.update( extractChildren( basic, esUtils.EventSupervisorQueueItem ) )

### vetting and alerts
from basic import approvalProcessor
qid.update( extractChildren( approvalProcessor, esUtils.EventSupervisorQueueItem ) )

### localization
from skymaps import skymaps
qid.update( extractChildren( skymaps, esUtils.EventSupervisorQueueItem ) )

from skymaps import skymapSummary
qid.update( extractChildren( skymapSummary, esUtils.EventSupervisorQueueItem ) )

### PE follow-up
from pe import bayestar
qid.update( extractChildren( bayestar, esUtils.EventSupervisorQueueItem ) )

from pe import bayeswavePE
qid.update( extractChildren( bayeswavePE, esUtils.EventSupervisorQueueItem ) )

from pe import cwbPE
qid.update( extractChildren( cwbPE, esUtils.EventSupervisorQueueItem ) )

from pe import libPE
qid.update( extractChildren( libPE, esUtils.EventSupervisorQueueItem ) )

from pe import lalinf
qid.update( extractChildren( lalinf, esUtils.EventSupervisorQueueItem ) )

### DQ follow-up
from dq import dq
qid.update( extractChildren( dq, esUtils.EventSupervisorQueueItem ) )

from dq import idq
qid.update( extractChildren( idq, esUtils.EventSupervisorQueueItem ) )

from dq import omegaScan
qid.update( extractChildren( omegaScan, esUtils.EventSupervisorQueueItem ) )

from dq import segDB2grcDB
qid.update( extractChildren( segDB2grcDB, esUtils.EventSupervisorQueueItem ) )

#-------------------------------------------------

### behvior when new alerts are witnessed
new = [
  'approval processor prelim dq',
  'event creation',
  'far',
  'local rate',
  'creation rate',
  'external triggers',
  'unblind injections',
  'dq summary',
  'idq start',
  'omega scan start',
  'segdb2grcdb start',
  'notify',
  'bayestar start',
  'bayeswave pe start',
  'cwb pe',
  'lalinf start',
  'lib pe start',
  ]

### behavior if certian checks are satisfied/alerts are received
parent_child = {
### parent name : [child name]
  'idq start'            : ['idq item'],
  'idqGlitchFAP'         : ['approval processor idq'], ### involves a Task
  'idqActiveChan'        : ['omega scan idq start'], ### involves a Task
  'omega scan start'     : ['omega scan'],
  'omega scan idq start' : ['omega scan idq'],
  'segdb2grcdb start'    : ['segdb2grcdb'],
  'bayestar start'       : ['bayestar'],
  'bayeswave pe start'   : ['bayeswave pe'],
  'lalinf start'         : ['lalinf'],
  'lib pe start'         : ['lib pe'],
  'skymap summary start' : ['skymap summary'],
  }

### special behavior if certain file types are seen
fits = [
  'skymap sanity',
  'plot skymap',
  'skyviewer',
  'skymap summary start',
  ]

#-------------------------------------------------

def parseAlert( queue, queueByGraceID, alert, t0, config ):
    """
    the main parsing function that interprets lvalert messages and modifies the dynamic queue appropriately

    queue is an instance of lvalertMPutils.interactiveQueue
    queueByGraceID is a dictionary with key=graceID, value=lvalertMPutils.interactiveQueue
    alert is the json dictionary to be parsed
    t0 is the time at which the message was received
    config is the ConfigParser.SaveConfigParser object representing which checks are to be performed

    this returns the change in the number of completed tasks that are in the queue. 
    This is used by interactiveQueue.interactiveQueue to manage a garbage collector for completed tasks

    NOTE: if we mark something as complete within this method, we must remove it from queueByGraceID as well 
        but do not have to remove it from queue

    Importantly, this function will ignore anything with "event_supervisor" in the tagnames
    """
    ### grab alert type
    alert_type = alert['alert_type']

    ### general options
    annotate = config.has_option('general', 'annotate') and config.getbool('general', 'annotate')
    
    if config.has_option('general', 'gracedb'):
        gdb = GraceDb( config.get('general', 'gracedb') )
    else:
        gdb = GraceDb()

    items = [] ### list of new items to add to queue

    ### filter based on alert type
    if alert_type=="new": ### we don't need to parse this any further
        for name in new: ### iterate through names that neeed to be added
            if config.has_section( name ):
                items.append( qid[name]( alert, t0, dict( config.options( name ) ), gdb, annotate=annotate ) )

        completed = 0

    else: ### need to parse this further
        if alert_type=="update":
            completed = 0 ### counter for the number of Items marked complete

            if alert['file']: ### look for special actions based on the presence of a file
                filename = alert['file']
                if filename.strip('.gz').endswidth('.fits'): ### new FITS file
                    for name in fits:
                        if config.has_section( name ):
                            items.append( qid[name]( alert, t0, dict( config.options( name ) ), gdb, annotate=annotate ) )
                else:
                    pass ### not sure what to do here... are there other file types that require special action?

            else:
                pass ### need a good way of identifying which check a log message satisfies...

        elif alert_type=="label":
            completed = 0

        else:
            raise ValueError("do not understand alert_type=%s"%alert_type)

    if items and (not queueByGraceID.has_key(graceid)): ### ensure queues are set up
        queueByGraceID[graceid] = utils.SortedQueue()

    for item in items: ### add items to queues
        queue.insert( item )
        queueByGraceID[graceid].insert( item )
    
    return completed

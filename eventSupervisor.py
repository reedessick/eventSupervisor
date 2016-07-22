description = "a module containing checks and parsing logic used within event_supervisor"
author = "reed.essick@ligo.org"

#-------------------------------------------------

def extractChildren( mod, klass ):
    """
    extracts the sublcasses of klass from module.
    """
    d = {}
    for x in dir(mod):
        attr = getattr(mod, x)
        if isinstance(attr, type) and issubclass(attr, klass):
            d[attr.name] = attr
    return d

#-------------------------------------------------

qid = {} ### queueItemDict
         ### contains mapping of names -> QueueItem objects
         ### used to standardize instantiation of QueueItems

#-------------------------------------------------

from ligoMP.lvalert import lvalertMPutils as utils
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

#------------------------
# currently, hard code relations here (although we may want to move this into a separate module?)
#------------------------

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
  'hoft omega scan start',
  'aux omega scan start',
  'segdb2grcdb start',
  'notify',
  'bayestar start',
  'bayeswave pe start',
  'cwb pe',
  'lalinf start',
  'lib pe start',
  ]

### behavior if certian checks are satisfied/alerts are received
### NOTE: keys can be Task names but values can ONLY contain Item names
parent_child = {
  None                    : [], ### helps with parsing. parseUpdate will return None if we don't do anything special for that alert
### parent name : [child name]
  'idq start'             : ['idq item'],
  'idqGlitchFAP'          : ['approval processor idq'], 
  'idqActiveChan'         : ['idq omega scan start'], 
  'hoft omega scan start' : ['hoft omega scan'],
  'aux omega scan start'  : ['aux omega scan'],
  'idq omega scan start'  : ['idq omega scan'], 
  'segdb2grcdb start'     : ['segdb2grcdb'],
  'bayestar start'        : ['bayestar'],
  'bayeswave pe start'    : ['bayeswave pe'],
  'lalinf start'          : ['lalinf'],
  'lib pe start'          : ['lib pe'],
  'skymap summary start'  : ['skymap summary'],
  'approvalProcessorSegDBStartCheck' : ['approval processor segdb']
  }

### special behavior if certain file types are seen
fits = [
  'skymap sanity',
  'plot skymap',
  'skyviewer',
  'skymap summary start',
  ]

#-------------------------------------------------

#------------------------
# main parsing function
#------------------------

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
    #--------------------
    # new alerts -> we don't need to parse this any further
    #--------------------
    if alert_type=="new":
        for name in new: ### iterate through names that neeed to be added
            if config.has_section( name ):
                items.append( qid[name]( alert, t0, dict( config.options( name ) ), gdb, annotate=annotate ) )
        completed = 0

    else: ### need to parse this further

        #----------------
        # update alerts -> we react to each update differently
        #----------------
        ### parse updates
        if alert_type=="update": 
            completed = 0 ### counter for the number of Items marked complete

            #------------
            # react to common file types in a systematic way
            #------------
            if alert['file']: ### look for special actions based on the presence of a file
                filename = alert['file']

                ### new FITS file
                if filename.strip('.gz').endswidth('.fits'):
                    for name in fits:
                        if config.has_section( name ):
                            items.append( qid[name]( alert, t0, dict( config.options( name ) ), gdb, annotate=annotate ) )

                else:
                    pass ### not sure what to do here... are there other file types that require special action?

            #------------
            # react to alert description
            #------------
            update_name = parseUpdate( alert ) ### determine the type of update

            ### determine new QueueItems that need to be added based on this update
            for name in parent_child[update_name]:
                if config.has_section( name ):
                    items.append( qid[name]( alert, t0, dict( config.options( name ) ), gdb, annotate=annotate ) )

            ### determine which QueueItems/Tasks need to be marked complete based on this update
            ###  >>>>>>>>>>>>>>>>>> HOW DO WE DO THIS CLEANLY? <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

        #----------------
        # label alert 
        #----------------
        elif alert_type=="label":
            completed = 0 ### currently we don't do anything...

        #----------------
        # alert type is not understood
        #----------------
        else:
            raise ValueError("do not understand alert_type=%s"%alert_type)

    #--------------------
    # actually add items to the queue
    #--------------------
    if items and (not queueByGraceID.has_key(graceid)): ### ensure queues are set up
        queueByGraceID[graceid] = utils.SortedQueue()

    for item in items: ### add items to queues
        queue.insert( item )
        queueByGraceID[graceid].insert( item )
    
    ### update queue.complete
    ### we don't need to update queueByGraceID[graceid].complete because it should *always* be zero
    ### managing that is the responsibility of parseAlert, not interactiveQueue!
    queue.complete += completed

    return completed

#------------------------
# parser for update alerts based on description
#------------------------

def parseUpdate( alert ):
    """
    determines the "name" of the update, which we use to determine what actions we need to take
    new QueueItems are defined through parent_child (dict)
    and Items/Tasks that need to be marked complete are defined through ??????

    need to key off these types of messages
        idq start
        idqGlitchFAP
        idqActiveChan
        hoft omega scan start
        aux omega scan start
        idq omega scan start
        segdb2grcdb start
        bayestar start
        bayeswave pe start
        lalinf start
        lib pe start
        skymap summary start

    if update is not recognized or we do not need to do anything based on it:
        return None
    """
    description = alert['description']

    ### idq start
    if idq.is_idqStart( description ):
        return 'idq start'

    ### idqGlitchFAP
    elif idq.is_idqGlitchFap( description ):
        return 'idqGlitchFAP'

    ### idqActiveChan
    elif idq.is_idqActiveChan( description ):
        return 'idqActiveChan'

    ### hoft omega scan start
    elif omegaScan.is_hoftOmegaScanStart( description ):
        return 'hoft omega scan start'

    ### aux omega scan start
    elif omegaScan.is_auxOmegaScanStart( description ):
        return 'aux omega scan start'

    ### idq omega scan start
    elif omegaScan.is_idqOmegaScanStart( description ):
        return 'idq omega scan start'
    
    ### segdb2grcdb start
    elif segdb2grcdb.is_segdb2grcdbStart( description ):
        return 'segdb2grcdb start'

    ### bayestar start
    elif bayestar.is_bayestarStart( description ):
        return 'bayestar start'

    ### bayeswave pe start
    elif bayeswavePE.is_bayeswavePEStart( description ):
        return 'bayeswave pe start'

    ### lalinf start
    elif lalinf.is_lalinfStart( description ):
        return 'lalinf start'

    ### lib pe start
    elif libPE.is_libPEStart( description ):
        return 'lib pe start'

    ### skymap summary start
    elif skymapSummary.is_skymapSummaryStart( description ):
        return 'skymap summary start'

    ### approval processor segdb start
    elif approvalProcessor.is_approvalProcessorSegDBStart( description ):
        return 'approvalProcessorSegDBStartCheck'

    ### message not recognized or we don't care about it
    else: 
        return None

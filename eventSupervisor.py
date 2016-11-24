description = "a module containing checks and parsing logic used within event_supervisor"
author      = "reed.essick@ligo.org"

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

import logging

from ligo.gracedb.rest import GraceDb

from lvalertMP.lvalert import lvalertMPutils as utils
from lvalertMP.lvalert.commands import parseCommand

import eventSupervisorUtils as esUtils

#------------------------

### notification and alerts
from notify import notify

### basics
from basic import basic

### vetting and alerts
from basic import approvalProcessor

### localization
from skymaps import skymaps
from skymaps import skymapSummary

### PE follow-up
from pe import bayestar
from pe import bayeswavePE
from pe import cwbPE
from pe import libPE
from pe import lalinf

### DQ follow-up
from dq import dq
from dq import idq
from dq import omegaScan
from dq import segDB2grcDB

#-------------------------------------------------

qid = {} ### queueItemDict
         ### contains mapping of names -> QueueItem objects
         ### used to standardize instantiation of QueueItems
for mod in [notify, basic, approvalProcessor, skymaps, skymapSummary, bayestar, bayeswavePE, cwbPE, libPE, lalinf, dq, idq, omegaScan, segDB2grcDB]:
    qid.update( extractChildren( mod, esUtils.EventSupervisorQueueItem ) )

#-------------------------------------------------

#------------------------
# currently, hard code relations here (although we may want to move this into a separate module?)
#------------------------

### behvior when new alerts are witnessed
new = [
#  'approval processor prelim dq',
  'event creation',
  'far',
  'local rate',
  'creation rate',
  'external triggers',
  'unblind injections',
  'dq summary',
  'idq start',
  'h1 omega scan start',
  'l1 omega scan start',
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
### parent name : [child name]
  'idq start'             : ['idq'],
  'idqGlitchFAP'          : [], # ['approval processor idq'], ### FIXME: not implemented...
  'idqActiveChan'         : ['idq omega scan start'], 
  'h1 omega scan start'   : ['h1 omega scan'],
  'l1 omega scan start'   : ['l1 omega scan'], 
  'segdb2grcdb start'     : ['segdb2grcdb'],
  'bayestar start'        : ['bayestar'],
  'bayeswave pe start'    : ['bayeswave pe'],
  'lalinf start'          : ['lalinf'],
  'lib pe start'          : ['lib pe'],
  'skymap summary start'  : ['skymap summary'],
#  'approvalProcessorSegDBStartCheck' : ['approval processor segdb'], ### FIXME: not implemented...
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

def parseAlert( queue, queueByGraceID, alert, t0, config, logTag='iQ' ):
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
    ### determine if this is a command and delegate accordingly
    graceid = alert['uid']
    if graceid == 'command':
        return parseCommand( queue, queuebyGraceID, alert, t0, logTag=logTag )

    ### set up logger
    logger = logging.getLogger('%s.parseAlert'%logTag) ### propagate to iQ's logger

    ### grab alert type
    alert_type = alert['alert_type']

    ### general options
    annotate = config.getboolean('general', 'annotate')
    warnings = config.getboolean('general', 'warnings')

    logDir = config.get('general', 'log_directory') if config.has_option('general','log_directory') else '.'
    
    if config.has_option('general', 'gracedb'):
        gdb = GraceDb( config.get('general', 'gracedb') ) ### FIXME: enable this to work with lvalertTest's FakeDb!
    else:
        gdb = GraceDb()

    items = [] ### list of new items to add to queue

    ### filter based on alert type
    #--------------------
    # new alerts -> we don't need to parse this any further
    #--------------------
    if alert_type=="new":
        far = alert['object']['far'] ### extract from alert only once
        for name in new: ### iterate through names that neeed to be added
            if config.has_section( name ):
                ### check if there's a FAR threshold
                ###    we don't have a far Threshold        or        the event has a FAR           the threshold is above the event's value
                if (not config.has_option(name, 'far thr')) or ((far!=None) and (config.getfloat(name, 'far thr') >= far)):
                    items.append( qid[name]( alert, t0, dict( config.items( name ) ), gdb, annotate=annotate, warnings=warnings, logDir=logDir, logTag=logTag ) )
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
                if filename.endswith('.fits.gz') or filename.endswith('.fits'):
                    for name in fits: ### iterate over names that are needed for new FITS files
                        if config.has_section( name ):
                            items.append( qid[name]( alert, t0, dict( config.items( name ) ), gdb, annotate=annotate, warnings=warnings, logDir=logDir, logTag=logTag ) )

                else:
                    pass ### not sure what to do here... are there other file types that require special action?

            #------------
            # react to alert description
            #------------
            update_name = parseUpdate( alert, config ) ### determine the type of update

            ### determine new QueueItems that need to be added based on this update
            if parent_child.has_key(update_name): ### ensure we know what to do with this...
                for name in parent_child[update_name]:
                    if config.has_section( name ):
                        items.append( qid[name]( alert, t0, dict( config.items( name ) ), gdb, annotate=annotate, warnings=warnings, logDir=logDir, logTag=logTag ) )

            ### FIXME: determine which QueueItems/Tasks need to be marked complete based on this update
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
        logger.debug( 'added QueueItem=%s'%item.name ) ### print to logger

    ### update queue.complete
    ### we don't need to update queueByGraceID[graceid].complete because it should *always* be zero
    ### managing that is the responsibility of parseAlert, not interactiveQueue!
    queue.complete += completed

    return completed ### not strictly necessary because it's never captured...

#------------------------
# parser for update alerts based on description
#------------------------

def parseUpdate( alert, config ):
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
    elif idq.is_idqGlitchFAP( description ):
        return 'idqGlitchFAP'

    ### idqActiveChan
    elif idq.is_idqActiveChan( description ):
        return 'idqActiveChan'

    ### l1 omega scan start
    ### ensure we actually care about this
    elif config.has_section('l1 omega scan start') and omegaScan.is_OmegaScanStart( description, chansets=config.get('l1 omega scan start', 'chansets').split() ):
        return 'l1 omega scan start'

    ### h1 omega scan start
    ### ensure that we actually care about this
    elif config.has_section('h1 omega scan start') and omegaScan.is_OmegaScanStart( description, chansets=config.get('h1 omega scan start', 'chansets').split() ):
        return 'h1 omega scan start'

    ### idq omega scan start
    ### NOTE: not implemented
#    elif omegaScan.is_idqOmegaScanStart( description ):
#        return 'idq omega scan start'
    
    ### segdb2grcdb start
    elif segDB2grcDB.is_segDB2grcDBStart( description ):
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
    ### NOTE: Not implemented...
#    elif skymapSummary.is_skymapSummaryStart( description ):
#        return 'skymap summary start'

    ### approval processor segdb start
    ### NOTE: Not implemented...
#    elif approvalProcessor.is_approvalProcessorSegDBStart( description ):
#        return 'approvalProcessorSegDBStartCheck'

    ### message not recognized or we don't care about it
    else: 
        return None

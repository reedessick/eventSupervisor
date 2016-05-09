description = "a module containing checks and parsing logic used within event_supervisor"
author = "reed.essick@ligo.org"

#-------------------------------------------------

from ligo.lvalert import lvalertMPutils as utils
import eventSupervisorUtils as esUtils

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

### load "DAG" for event_supervisor follow-up
import json
fileObj = open("eventSupervisor.json", "r")
directedGraph = json.loads(fileObj.read())
fileObj.close()

#-------------------------------------------------

def getDT( string ):
    return [float(_) for _ in string.strip().split()]

def addToQueue( alert, listOfItems, queue, queueByGraceID, t0, config ):
    """
    add a list of items to the associated queues
    """
    if config.has_option('general', 'graceDB_url'):
        gdb = GraceDb(config.get('general', 'graceDB_url'))
    else:
        gdb = GraceDb()
    graceid = alert['uid']
    group = alert['group']
    pipeline = alert['pipeline']
    if alert.has_key('search'):
        search = alert['search']
    else:
        search = None

    annotate = config('general', 'annotate')

    items = []
    for name in listOfItems:
        ### event creation
        if (name=="event creation") and config.has_section( "event creation" ):
            email = config.get("event creation", "email").split()
            for timeout in getDT( config.get("event creation", "dt") ):
                items.append( basic.EventCretaionItem( graceid, gdb, pipeline, t0, timeout, annotate=annotate, email=email ) )

        ### far
        if (name=="far") and config.has_section( "far" ):
            maxFAR = config.getfloat("far", "maxFAR")
            minFAR = config.getfloat("far", "minFAR")
            email = config.get("far", "email").split()
            for timeout in getDT( config.get("far", "dt") ):
                items.append( basic.FARItem( graceid, gdb, t0, timeout, annotate=annotate, email=email ) )

        ### local rate
        if (name=="local rate") and config.has_section("local rate"):
            maxRate = config.getfloat("local rate", "maxRate")
            email = config.get("local rate", "email").split()
            for timeout in getDT( config.get("local rate", "dt") ):
                items.append( basic.LocalRateItem( graceid, gdb, t0, timeout, group, pipeline, search=search, annotate=annotate, email=email )  )

        ### external triggers
        if (name=="external triggers") and config.has_section("external triggers"):
            email = config.get("external triggers", "email").split()
            for timeout in getDT( config.get("external triggers", "dt") ):
                items.append( basic.ExternalTriggersItem( graceid, gdb, t0, timeout, annotate=annotate, email=email ) )

        ### unblind injections
        if (name=="unblind injections") and config.has_section("unblind injections"):
            email = config.get("unblind injections", "email").split()
            for timeout in getDT( config.get("unblind injections", "dt") ):
                items.append( basic.UnblindInjectionsItem( graceid, gdb, t0, timeout, annotate=annotate, email=email ) )

        ### approval processor prelim
        if (name=="approval processor prelimDQ"):
            raise NotImplementedError

        ### dq summary pages
        if (name=="dq summary start"):
            raise NotImplementedError

        ### idq start
        if (name=="idq start"):
            raise NotImplementedError

        ### segDB start

        ### HofTOmegaScan start

        ### allAuxOmegaScan start

        ### cWBPE start

        ### libPE start

        ### lalinfPE start

        ### bayestar start

        ### bayeswavePE start

    ### if we've created an item, add it to the queues
    if items and (not queueByGraceID[graceid]):
        queueByGraceID[graceid] = utils.SortedQueue()
    for item in items:
        queue.insert( item )
        queueByGraceID[graceid].insert( item )
    

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
    """
    alert_type = alert['alert_type']

    if alert_type=="new": ### we don't need to parse this any further
        addToQueue( graceid, directedGraph['new'], queue, queueByGraceID, t0, config )
        return 0 ### we've only added things and not marked anything as complted

    else: ### need to parse this further
        if alert_type=="update":
            pass
        elif alert_type=="label":
            pass
        else:
            raise ValueError("do not understand alert_type=%s"%alert_type)

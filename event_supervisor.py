description = "a module containing checks and parsing logic used within event_supervisor"
author = "reed.essick@ligo.org"

#-------------------------------------------------

from ligo.lvalert import lvalertMPutils as utils

### basics
import basic
import skymaps

### vetting and alerts
import approvalProcessor

### PE follow-up
import bayestar
import bayeswavePE
import cwbPE
import libPE
import lalinfPE

### DQ follow-up
import dq
import idq
import omegaScans
import segDB2grcDB

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
    """

    graceid = alert['uid']

    item = utils.QueueItem( graceid, t0, 5.0, printAlert, description="print the alert message", alert=alert )
    queue.insert( item )
    if not queueByGraceId.has_key(graceid):
        queueByGraceID[graceid] = utils.SortedQueue()
    queueByGraceID[graceid].insert( item )

    return 0

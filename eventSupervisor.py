description = "a module containing checks and parsing logic used within event_supervisor"
author = "reed.essick@ligo.org"

#-------------------------------------------------

from ligo.lvalert import lvalertMPutils as utils

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
from pe import lalinfPE

### DQ follow-up
from dq import dq
from dq import idq
from dq import omegaScans
from dq import segDB2grcDB

#-------------------------------------------------

### load "DAG" for event_supervisor follow-up
import json
file_obj = open("event_supervisor.json","r")
dag = json.loads(file.read())
file_obj.close()

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

    ### new event
    if alert['alert_type'] == 'new':
        ### add Items for a new event

        ### basics and vetting
        if config.has_section('event_creation'): 
            pass ### basic.EventCreationItem

        if config.has_section("far"):
            pass ### basic.FARItem

        if config.has_section("localRate"):
            pass ### basic.LocalRateItem

        if config.has_section("externaltriggers"):
            pass ### basic.ExternalTriggersItem

        if config.has_section("unblindinjections"):
            pass ### basic.UnblindInjectionsItem

        if config.has_section("approvalProcessor_far"):
            pass ### approvalProcessor.FARItem

        ### dq
        if config.has_section('idq_start'):
            pass ### idq.idq_start

        if config.has_section('dqSummary'):
            pass ### dq.DQSummaryItem

        if config.has_section('segDB_start'):
            pass ### segDB2grcDB.segDB_start

        if config.has_section('HofTOmegaScan_start'):
            pass

        if config.has_section('allAuxOmegaScan_start'):
            pass
       
        ### pe

 
    ### update
    elif alert['alert_type'] == 'update':
        if idq.is_idqAlert( alert ):
            idq.parseAlert( queue, queueByGraceID, alert, t0, config )

        else: ### default behavior... will want to change this
            item = utils.QueueItem( graceid, t0, 5.0, printAlert, description="print the alert message", alert=alert )
            queue.insert( item )
            if not queueByGraceId.has_key(graceid):
                queueByGraceID[graceid] = utils.SortedQueue()
            queueByGraceID[graceid].insert( item )

    ### label
    elif alert['alert_type'] == 'label':
        return 0

    ### else?
    else:
        return 0

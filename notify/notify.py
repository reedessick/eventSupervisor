description = "a module housing notification and alerting checks for event_supervisor"
author = "reed.essick@ligo.org"

#---------------------------------------------------------------------------------------------------

import sys
sys.path.append("../")
import eventSupervisorUtils as esUtils

#---------------------------------------------------------------------------------------------------

class NotifyItem(esUtils.EventSupervisorQueueItem):
    """
    notify folks that a new event was created
    """
    description = "notify people by email, sms or phone"

    def __init__(self, graceid, gdb, t0, timeout, ignoreInj=False, email=[], sms=[], phone=[], annotate=False):
        tasks = []
        if email:
            tasks.append( notifyByEmail(timeout, email=email, ignoreInj=ignoreInj) )
        if sms:
            tasks.append( notifyBySMS(timeout, sms=sms, ignoreInj=ignoreInj) )
        if phone:
            tasks.append( notifyByPhone(timeout, phone=phone, ignoreInj=ignoreInj) )
        super(NotifyItem, self).__init__( graceid,
                                          gdb,
                                          t0,
                                          tasks,
                                          description=self.description,
                                          annotate=annotate
                                        )

class notifyByEmail(esUtils.EventSupervisorTask):
    """
    notify folks by email that a new event was created
    """
    description = "notify folks by email that a new event was created"
    name = "notifyByEmail"

    def __init__(self, timeout, email=[], ignoreInj=False):
        self.ignoreInj = ignoreInj
        super(notifyByEmail, self).__init__( timeout, 
                                             self.notifyByEmail,
                                             name=self.name,
                                             description=self.description,
                                             email=email
                                           )

    def notifyByEmail(self, graceid, gdb, verbose=False, annotate=False ):
        """
        notify folks by email
        NOT IMPLEMENTED
        """
        raise NotImplementedError

class notifyBySMS(esUtils.EventSupervisorTask):
    """
    notify folks by SMS that new event was created
    """
    description = "notify folks by SMS that a new event was created"
    name = "notifyBySMS"

    def __init__(self, timeout, sms=[], ignoreInj=False):
        self.sms = sms
        self.ignoreInj = ignoreInj
        super(notifyBySMS, self).__init__( timeout,
                                           self.notifyBySMS,
                                           name=self.name,
                                           description=self.description,
                                           email=[]
                                         )

    def notifyBySMS(self, graceid, gdb, verbose=False, annotate=False ):
        """
        notify folks by SMS
        NOT IMPLEMENTED
        """
        raise NotImplementedError

class notifyByPhone(esUtils.EventSupervisorTask):
    """
    notify folks by phone that a new event was created
    """
    description = "notify folks by phone that a new event was created"
    name = "notifyByPhone"

    def __init__(self, timeout, phone=[], ignoreInj=False):
        self.phone = []
        self.ignoreInj = ignoreInj
        super(notifyByPhone, self).__init__( timeout,
                                             self.notifyByPhone,
                                             name=self.name,
                                             description=self.description,
                                             email=[]
                                           )

    def notifyByPhone(self, graceid, gdb, verbose=False, annotate=False ):
        """
        notify folks by phone
        NOT IMPLEMENTED
        """
        raise NotImplementedError

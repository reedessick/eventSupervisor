description = "a module housing notification and alerting checks for event_supervisor"
author = "reed.essick@ligo.org"

#---------------------------------------------------------------------------------------------------

import sys
sys.path.append("../")
import eventSupervisorUtils as esUtils

#---------------------------------------------------------------------------------------------------

### methods to identify updates by description

#---------------------------------------------------------------------------------------------------

class NotifyItem(esUtils.EventSupervisorQueueItem):
    """
    notify folks that a new event was created

    alert:
        graceid
    options:
        dt
        ignoreInj
        by email
        by sms
        by phone
    """
    name = "notify"
    description = "notify people by email, sms or phone"

    def __init__(self, alert, t0, options, gdb, annotate=False):
        graceid = alert['uid']

        email = options['by email'].split()
        sms   = options['by sms'].split()
        phone = options['by phone'].split()

        ignoreInj = bool(options['ignoreInj'])

        timeout = float(options['dt'])

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
                                          annotate=annotate
                                        )

class notifyByEmail(esUtils.EventSupervisorTask):
    """
    notify folks by email that a new event was created
    """
    description = "notify folks by email that a new event was created"
    name = "notifyByEmail"

    def __init__(self, timeout, email=[], ignoreInj=False):
        self.notificationList = email
        self.ignoreInj = ignoreInj
        super(notifyByEmail, self).__init__( timeout, 
                                             email=[]
                                           )

    def notifyByEmail(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        notify folks by email
        """
        if verbose:
            print( "%s : %s"%(graceid, self.description) )
        if self.ignoreInj:
            if esUtils.isINJ( graceid, gdb, verbose=verbose ):
                if verbose:
                    print( "    labeled INJ -> ignoring" )
            else:
                if verbose:
                    print( "    not labeled INJ -> sending emails" )
                raise NotImplementedError
        else:
            raise NotImplementedError

        return False ### action_required = False
                     ### all message are sent from within this function, so nothing else is necessary

class notifyBySMS(esUtils.EventSupervisorTask):
    """
    notify folks by SMS that new event was created
    """
    description = "notify folks by SMS that a new event was created"
    name = "notifyBySMS"

    def __init__(self, timeout, sms=[], ignoreInj=False):
        self.notificationList = sms
        self.ignoreInj = ignoreInj
        super(notifyBySMS, self).__init__( timeout,
                                           email=[]
                                         )

    def notifyBySMS(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        notify folks by SMS
        """
        if verbose:
            print( "%s : %s"%(graceid, self.description) )
        if self.ignoreInj:
            if esUtils.isINJ( graceid, gdb, verbose=verbose ):
                if verbose:
                    print( "    labeled INJ -> ignoring" )
            else:
                if verbose:
                    print( "    not labeled INJ -> sending emails" )
                raise NotImplementedError
        else:
            raise NotImplementedError

        return False ### action_required = False
                     ### all message are sent from within this function, so nothing else is necessary

class notifyByPhone(esUtils.EventSupervisorTask):
    """
    notify folks by phone that a new event was created
    """
    description = "notify folks by phone that a new event was created"
    name = "notifyByPhone"

    def __init__(self, timeout, phone=[], ignoreInj=False):
        self.notificationList = phone
        self.ignoreInj = ignoreInj
        super(notifyByPhone, self).__init__( timeout,
                                             email=[]
                                           )

    def notifyByPhone(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        notify folks by phone
        """
        if verbose:
            print( "%s : %s"%(graceid, self.description) )
        if self.ignoreInj:
            if esUtils.isINJ( graceid, gdb, verbose=verbose ):
                if verbose:
                    print( "    labeled INJ -> ignoring" )
            else:
                if verbose:
                    print( "    not labeled INJ -> sending emails" )
                raise NotImplementedError
        else:
            raise NotImplementedError

        return False ### action_required = False
                     ### all message are sent from within this function, so nothing else is necessary

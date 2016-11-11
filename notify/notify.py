description = "a module housing notification and alerting checks for event_supervisor"
author      = "reed.essick@ligo.org"

#---------------------------------------------------------------------------------------------------

from lvalertMP.lvalert.lvalertMPutils import sendEmail
import eventSupervisor.eventSupervisorUtils as esUtils

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
    description = "notify people by email, sms or phone"
    name        = "notify"

    def __init__(self, alert, t0, options, gdb, annotate=False, warnings=False, logDir='.'):
        graceid = alert['uid']

        ### extract parameters from config file
        email = options['by email'].split() if options.has_key('by email') else [] ### addresses to ping
        sms   = options['by sms'].split()   if options.has_key('by sms')   else [] ### phone numbers to ping (really, via email)
        phone = options['by phone'].split() if options.has_key('by phone') else [] ### phone numbers to ping with voice?

        ignoreInj = bool(options['ignoreInj']) ### whether we ignore things labeled as injections

        timeout = float(options['dt']) ### how long we wait before we ping people

        ### generate tasks
        tasks = []
        if email: ### only add if the list is not empty
            tasks.append( notifyByEmail(timeout, email=email, ignoreInj=ignoreInj, logDir=logDir) )
        if sms:
            raise NotImplementedError('currently do not support sms specifically, try using email')
            tasks.append( notifyBySMS(timeout, sms=sms, ignoreInj=ignoreInj, logDir=logDir) )
        if phone:
            raise NotImplementedError('currently do not suport phone')
            tasks.append( notifyByPhone(timeout, phone=phone, ignoreInj=ignoreInj, logDir=logDir) )

        ### wrap up instantiation
        super(NotifyItem, self).__init__( graceid,
                                          gdb,
                                          t0,
                                          tasks,
                                          annotate=annotate,
                                          warnings=warnings,
                                        )

class notifyByEmail(esUtils.EventSupervisorTask):
    """
    notify folks by email that a new event was created
    """
    description = "notify folks by email that a new event was created"
    name        = "notifyByEmail"

    def __init__(self, timeout, email=[], ignoreInj=False, logDir='.'):
        self.notificationList = email
        self.ignoreInj        = ignoreInj
        super(notifyByEmail, self).__init__( timeout, 
                                             email=[],
                                             logDir=logDir,
                                           )

    def notifyByEmail(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        notify folks by email
        """
        if verbose:
            ### set up logger
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag='iQ', graceid=graceid )
            logger.info( "%s : %s"%(graceid, self.description) )

        if self.notificationList:
            body    = "%s/events/view/%s"%(gdb.service_url, graceid)
            subject = "new GraceDb Event: %s"%graceid
            if self.ignoreInj:
                if esUtils.isINJ( graceid, gdb, verbose=verbose, logTag=self.logTag ):
                    if verbose:
                        logger.debug( "labeled INJ -> ignoring" )

                else:
                    if verbose:
                        logger.debug( "not labeled INJ -> sending emails" )
                    sendEmail( self.notificationList, body, subject )

            else:
                sendEmail( self.notificationList, body, subject )

        return False ### action_required = False
                     ### all message are sent from within this function, so nothing else is necessary

class notifyBySMS(esUtils.EventSupervisorTask):
    """
    notify folks by SMS that new event was created
    """
    description = "notify folks by SMS that a new event was created"
    name        = "notifyBySMS"

    def __init__(self, timeout, sms=[], ignoreInj=False, logDir='.'):
        self.notificationList = sms
        self.ignoreInj        = ignoreInj
        super(notifyBySMS, self).__init__( timeout,
                                           email=[],
                                           logDir=logDir,
                                         )

    def notifyBySMS(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        notify folks by SMS
        """
        if verbose:
            ### set up logger
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag='iQ', graceid=graceid )
            logger.info( "%s : %s"%(graceid, self.description) )

        if self.notificationList:
            if self.ignoreInj:
                if esUtils.isINJ( graceid, gdb, verbose=verbose, logTag=self.logTag ):

                    if verbose:
                        logger.debug( "labeled INJ -> ignoring" )

                else:
                    if verbose:
                        logger.debug( "not labeled INJ -> sending emails" )
                    raise NotImplementedError(self.name)

            else:
                raise NotImplementedError(self.name)

        return False ### action_required = False
                     ### all message are sent from within this function, so nothing else is necessary

class notifyByPhone(esUtils.EventSupervisorTask):
    """
    notify folks by phone that a new event was created
    """
    description = "notify folks by phone that a new event was created"
    name        = "notifyByPhone"

    def __init__(self, timeout, phone=[], ignoreInj=False, logDir='.'):
        self.notificationList = phone
        self.ignoreInj        = ignoreInj
        super(notifyByPhone, self).__init__( timeout,
                                             email=[],
                                             logDir=logDir,
                                           )

    def notifyByPhone(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        notify folks by phone
        """
        if verbose:
            ### set up logger
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag='iQ', graceid=graceid )
            logger.info( "%s : %s"%(graceid, self.description) )

        if self.ignoreInj:
            if esUtils.isINJ( graceid, gdb, verbose=verbose, logTag=self.logTag ):

                if verbose:
                    logger.debug( "labeled INJ -> ignoring" )
            else:
                if verbose:
                    logger.debug( "not labeled INJ -> sending emails" )
                raise NotImplementedError(self.name)

        else:
            raise NotImplementedError(self.name) ### send phone notification

        return False ### action_required = False
                     ### all message are sent from within this function, so nothing else is necessary

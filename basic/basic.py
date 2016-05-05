description = "a module housing checks of basic event_supervisor functionality"
author = "reed.essick@ligo.org"

#---------------------------------------------------------------------------------------------------

import sys
sys.path.append("../")
import eventSupervisorUtils as esUtils

#---------------------------------------------------------------------------------------------------

#-------------------------------------------------
# EventCreation
#-------------------------------------------------

class EventCreationItem(esUtils.EventSupervisorQueueItem):
    """
    a check for propper event creation and readability of associated trigger files
    """

    def __init__(self, graceid, gdb, pipeline, t0, timeout, annotate=False, email=[]):
        self.email = email
        if pipeline=="cwb":
            tasks = [cWBTriggerCheck(timeout, email=email)]
        elif pipeline=="lib":
            tasks = [oLIBTriggerCheck(timeout, email=email)]
        elif pipeline in ["gstlal", "mbtaonline", "gstlal-spiir", "pycbc"]:
            tasks = [cbcCoincCheck(timeout, email=email), 
                     cbcPSDCheck(timeout, email=email)
                    ]
        else:
            raise ValueError("pipeline=%s not understood"%pipeline)

        super(EventCreationItem, self).__init__( graceid, 
                                                 gdb,
                                                 t0, 
                                                 tasks, 
                                                 description="check %s event creation and trigger files"%(pipeline),
                                                 annotate=annotate 
                                                )

class cWBTriggerCheck(esUtils.EventSupervisorTask):
    """
    check for cWB event creation, checking the trigger.txt file
    """
    description = "a check of the trigger.txt file for cWB events"
    name = "cWBTriggerCheck"

    def __init__(self, timeout, email=[]):
        super(cwbTriggerCheck, self).__init__( timeout, 
                                               self.cWBTriggerCheck, 
                                               name=self.name, 
                                               description=self.description, 
                                               email=email
                                             )

    def cWBTriggerCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        query GraceDB to check for proper event creation
        we check:
            trigger.txt
        NOT IMPLEMENTED
        """
        raise NotImplementedError
        
class oLIBTriggerCheck(esUtils.EventSupervisorTask):
    """
    check for oLIB event creation
    """
    description="a check of the trigger.json file for oLIB events"
    name = "oLIBTriggerCheck"

    def __init__(self, timeout, email=[]):
        super(oLIBTriggerCheck, self).__init__( timeout, 
                                                self.oLIBTriggerCheck, 
                                                name=self.name, 
                                                description=self.description, 
                                                email=email
                                              )

    def oLIBTriggerCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        event creation sanity check for oLIB
        we check:
            trigger.json
        NOT IMPLEMENTED
        """
        raise NotImplementedError

class cbcCoincCheck(esUtils.EventSupervisorTask):
    """
    check for CBC event creation, checking coinc.xml file
    """
    description = "check coinc.xml file for CBC events"
    name = "cbcCoincCheck"

    def __init__(self, timeout, email=[]):
        super(cbcCoincCheck, self).__init__( timeout, 
                                             self.cbcCoincCheck, 
                                             name=self.name, 
                                             description=self.description, 
                                             email=email
                                           )

    def cbcTriggerCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        check for coinc.xml file
        NOT IMPLEMENTED
        """
        raise NotImplementedError("cbcCoincCheck")

class cbcPSDCheck(esUtils.EventSupervisorTask):
    """
    check for CBC event creation, checking PSD.xml file
    """
    description = "check psd.xml file for CBC events"
    name = "cbcPSDCheck"

    def __init__(self, timeout, email=[]):
        super(cbcPSDCheck, self).__init__( timeout, 
                                           self.cbcPSDCheck, 
                                           name=self.name, 
                                           description=self.description, 
                                           email=email
                                         )

    def cbcPSDCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        check for psd.xml file
        NOT IMPLEMENTED
        """
        raise NotImplementedError("cbcPSDCheck")

#-------------------------------------------------
# FAR
#-------------------------------------------------

class FARItem(esUtils.EventSupervisorQueueItem):
    """
    a check for propper FAR
    """
    description = "check sanity of reported FAR"

    def __init__(self, graceid, gdb, t0, timeout, annotate=False, email=[]):
        tasks = [farChec(timeout, email=email)]
        super(FARItem, self).__init__( graceid, 
                                       gdb, 
                                       t0, 
                                       tasks, 
                                       description=self.description,
                                       annotate=annotate
                                     )

class FARCheck(esUtils.EventSupervisorTask):
    """
    a check for propper FAR
    """
    description = "a check for propper FAR"
    name = "FARCheck"

    def __init__(self, timeout, maxFAR=1.0, minFAR=0.0, annotate=False, email=[]):
        self.maxFAR = maxFAR
        self.minFAR = minFAR
        
        super(farCheck, self).__init__( timeout, 
                                        self.FARCheck, 
                                        name=self.name, 
                                        description=self.description, 
                                        email=email
                                      )

    def FARCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        check the sanity of the reported FAR
        NOT IMPLEMENTD
        """
        raise NotImplementedError("FARCheck")

        if verbose:
            print( "%s : %s"%(graceid, self.description) )
            print( "    retrieving event details" )
        event = gdb.event( gdb_id ).json()

        if event.has_key("far"): ### check bounds
            far = event['far']
            big = far > maxFAR
            sml = far < minFAR
            action_required = big or sml

            if verbose or annotate:
                if big:
                    message = "action required : FAR=%.3e > %.3e"%(far, maxFAR)
                    if verbose:
                        print( message )
                    if annotate:
                        message = "event_supervisor : "+message
                        gdb.writeLog( graceid, message=message, tagnames=['event_supervisor'] )
                
                elif sml:
                    message = "action required : FAR=%.3e < %.3e"%(far, minFAR)
                    if verbose:
                        print( message )
                    if annotate:
                        message = "event_supervisor :"+message
                        gdb.writeLog( graceid, message=message, tagnames=['event_supervisor'] )
                else:
                    message = "no action required : %.3e <= FAR=%.3e <= %.3e"%(minFAR, far, maxFAR)
                    if verbose:
                        print( message )
                    if annotate:
                        message = "event_supervisor : "+message
                        gdb.writeLog( graceid, message=message, tagnames=['event_supervisor'] )

        else: ### something is very wrong...
            action_required = True

            if verbose or annotate:
                message = "action required : FAR is not defined!"
                if verbose:
                    print( message )
                if annotate:
                    message = "event_supervisor : "+message
                    gdb.writeLog( graceid, message=message, tagnames=['event_supervisor'] )

        return action_required

#-------------------------------------------------
# localRate
#-------------------------------------------------

class LocalRateItem(esUtils.EventSupervisorQueueItem):
    """
    a check for local rate of events submitted to GraceDb
    """
    description = "check local rates of events"

    def __init__(self, graceid, gdb, t0, timeout, group, pipeline, search=None, annotate=False, email=[]):
        tasks = [ localRateCheck(timeout, group, pipeline, search=search, email=email) ] 
        super(LocalRateItem, self).__init__( graceid, 
                                             gdb,
                                             t0, 
                                             tasks,
                                             description=self.description,
                                             annotate=annotate
                                           )

class localRateCheck(esUtils.EventSupervisorTask):
    """
    a check for local rate of events submitted to GraceDB
    """
    name = "localRateCheck"

    def __init__(self, timeout, group, pipeline, search=None, email=[]):
        description = "a check of local rates for %s_%s"%(group, pipline)
        if search:
            description = "%s_%s"%(description, search)
        self.group = group
        self.pipeline = pipeline
        self.search = search
        super(localRateCheck, self).__init__( timeout, 
                                              self.localRateCheck, 
                                              name=self.name, 
                                              description=self.description, 
                                              email=email
                                            )

    def localRateCheck(self, graceid, gdb, verbose=None, annotate=False):
        """
        check the local rate of triggers submitted to GraceDB
        NOT IMPLEMENTED
        """
        raise NotImplementedError("localRateCheck")

#-------------------------------------------------
# external triggers
#-------------------------------------------------

class ExternalTriggersItem(esUtils.EventSupervisorQueueItem):
    """
    a check that the external triggers search was completed
    """
    description = "check that the unblind injection search completed"

    def __init__(self, graceid, gdb, t0, timeout, annotate=False, email=[]):
        tasks = [externalTriggersCheck(timeout, email=email)]
        super(ExternalTriggersItem, self).__init__( graceid, 
                                                    gdb,
                                                    t0, 
                                                    tasks, 
                                                    description=self.description,
                                                    annotate=annotate
                                                  )

class externalTriggersCheck(esUtils.EventSupervisorTask):
    """
    a check that the external triggers seach was completed
    """
    description = "a check that the external triggers search was completed"
    name = "ExternalTriggersCheck"

    def __init__(self, timeout, email=[]):
        """
        a check that the external triggers search was completed
        """
        super(externalTriggersCheck, self).__init__( timeout, 
                                                     self.externalTriggersCheck, 
                                                     name=self.name, 
                                                     description=self.description, 
                                                     email=email
                                                   )
    
    def externalTriggersCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that the external triggers search was completed
        NOT IMPLEMENTED
        """
        raise NotImplementedError("externalTriggersCheck")

#-------------------------------------------------
# unblind injections
#-------------------------------------------------

class UnlindInjectionsItem(esUtils.EventSupervisorQueueItem):
    """
    a check that the unblind Injections search was completed
    """
    description = "check that the unblind injection search completed"

    def __init__(self, graceid, gdb, t0, timeout, annotate=False, email=[]):
        tasks = [unblindInjectionsCheck(timeout, email=email)]
        super(UnblindInjectionsItem, self).__init__( graceid, 
                                                     gdb,
                                                     t0, 
                                                     tasks, 
                                                     description=self.description,
                                                     annotate=annotate
                                                   )

class unblindInjectionsCheck(esUtils.EventSupervisorTask):
    """
    a check that the unblind injections search was completed
    """
    description = "a check that the unblind injections search was completed"
    name = "unblindInjectionsCheck"

    def __init__(self, timeout, email=[]):
        """
        a check that the unblind injections search was completed
        """
        super(unblindInjectionsCheck, self).__init__( timeout, 
                                                      self.unblindInjectionsCheck, 
                                                      name=self.name, 
                                                      description=self.description, 
                                                      email=email
                                                    )

    def unblindInjectionsCheck(self, graceid, gid, verbose=False, annotate=False):
        """
        a check that the unblind injections search was completed
        NOT IMPLEMENTED
        """
        raise NotImplementedError("unblindInjectionsCheck")

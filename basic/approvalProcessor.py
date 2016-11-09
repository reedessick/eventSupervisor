description = "a module housing checks of approval_processor functionality"
author      = "reed.essick@ligo.org"

#---------------------------------------------------------------------------------------------------

import eventSupervisor.eventSupervisorUtils as esUtils

#---------------------------------------------------------------------------------------------------

### methods to identify updates by description

def is_approvalProcessorSegDBStart( description ):
    ''' NOT IMPLEMENTED -> return False '''
    return False

#---------------------------------------------------------------------------------------------------

#-------------------------------------------------
# approval_processor preliminary DQ checks
#-------------------------------------------------

class ApprovalProcessorPrelimDQItem(esUtils.EventSupervisorQueueItem):
    """
    a set of checks for approval_processor's preliminary DQ and vetting

    alert:
        graceid
    options:
        far dt
        seg start dt
        email
    """
    name = "approval processor prelim dq"
    description = "a set of checks for approval_processor's preliminary DQ and vetting"

    def __init__(self, alert, t0, options, gdb, annotate=False):
        graceid = alert['uid']

        farTimeout = float(options['far dt'])
        segStartTimeout = float(options['seg start dt'])
        email = options['email'].split()

        tasks = [approvalProcessorFARCheck(farTimeout, email=email),
                 approvalProcessorSegDBStartCheck(segStartTimeout, email=email)
                ]
        super(ApprovalProcessorPrelimDQItem, self).__init__( graceid,
                                                             gdb,
                                                             t0,
                                                             tasks,
                                                             annotate=annotate
                                                           )

class approvalProcessorFARCheck(esUtils.EventSupervisorTask):
    """
    a check that approvalProcessor analyzed the FAR as expected
    """
    description = ""
    name = "approvalProcessorFAR"

    def __init__(self, timeout, email=[]):
        super(approvalProcessorFARCheck, self).__init__( timeout, 
                                                         email=email
                                                       )

    def approvalProcessorFAR(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that approvalProcessor analyzed the FAR as expected
        """
        ### note, we do not delegate to esUtils.check4log because there are multiple possible messages
        if verbose:
            print( "%s : %s"%(graceid, self.description) )
            print( "    retrieving log messages" )
        logs = gdb.logs( graceid ).json()['log']

        if verbose:
            print( "    parsing log" )
        for log in logs:
            comment = log['comment']
            if ("Candidate event has low enough FAR" in comment) \
              or ("Candidate event rejected due to large FAR" in comment) \
              or ("Ignoring new event because we found a hardware injection" in comment):
                self.warning = "found ApprovalProcessor FAR check message"
                if verbose or annotate:
                    message = "no action required : "+self.warning
                    if verbose:
                        print( "    "+message )
                    if annotate:
                        esUtils.writeGDBLog( gdb, graceid, message )
                return False ### action_required = False

        self.warning = "could not find ApprovalProcessor FAR check message"
        if verbose or annotate:
            message = "action required : "+self.warning
            if verbose:
                print( "    "+message )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )
        return True ### action_required = True

class approvalProcessorSegDBStartCheck(esUtils.EventSupervisorTask):
    """
    a check that approvalProcessor started checking segments as expected
    """
    description = "a check that approvalProcessor started checking segments as expected"
    name = "approvalProcessorSegDBStart"

    def __init__(self, timeout, email=[]):
        super(approvalProcessorSegDBStartCheck, self).__init__( timeout, 
                                                                email=email
                                                              )

    def approvalProcessorSegDBStart(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that approvalProcessor started checking segments as expected
        NOT IMPLEMENTED
        """
        raise NotImplementedError(self.name)

class ApprovalProcessorSegDBItem(esUtils.EventSupervisorQueueItem):
    """
    check that approval processor completed segment checks

    alert:
        graceid
    options:
        flags dt
        flags
        finish dt
        email
    """
    name = "approval processor segdb"
    description = "a set of checks for approval_processor's segment vetting"

    def __init__(self, alert, t0, options, gdb, annotate=False):
        graceid = alert['uid']

        flags_dt = float(options['flags dt'])
        finish_dt = float(options['finish dt'])

        flags = options['flags'].split()

        email = options['email'].split()

        tasks = [approvalProcessorSegDBFlagsCheck(flags_dt, flags=flags, email=email),
                 approvalProcessorSegDBFinishCheck(finish_dt, email=email)
                ]
        super(ApprovalProcessorSegDBItem, self).__init__( graceid,
                                                             gdb,
                                                             t0,
                                                             tasks,
                                                             annotate=annotate
                                                           )

class approvalProcessorSegDBFlagsCheck(esUtils.EventSupervisorTask):
    """
    a check that approvalProcessor checked all the segment/flags as expected
    """
    description = "a check that approvalProcessor checked all the segment/flags as expected"
    name = "approvalProcessorSegDBFlags"

    def __init__(self, timeout, flags=[], email=[]):
        self.flags = flags 
        super(approvalProcessorSegDBFlagsCheck, self).__init__( timeout,
                                                                email=email
                                                              )

    def approvalProcessorSegDBFlags(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that approvalProcessor checked all the segment/flags as expected
        NOT IMPLEMENTED
        """
        raise NotImplementedError(self.name)

class approvalProcessorSegDBFinishCheck(esUtils.EventSupervisorTask):
    """
    a check that approvalProcessor finished checking segments as expected
    """
    description = "a check that approvalProcessor finished checking segments as expected"
    name = "approvalProcessorSegDBFinish"

    def __init__(self, timeout, email=[]):
        super(approvalProcessorSegDBFinishCheck, self).__init__( timeout,
                                                                 email=email
                                                               )

    def approvalProcessorSegDBFinish(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that approvalProcessor finished checking all segments as expected
        NOT IMPLEMENTED
        """
        raise NotImplementedError(self.name)


#-------------------------------------------------
#  approvalProcessor_idq
#-------------------------------------------------

class ApprovalProcessoriDQItem(esUtils.EventSupervisorQueueItem):
    """
    an item for monitoring approval processor's response to iDQ information

    alert:
        graceid
        ifo
    options:
        dt
        email
    """
    name = "approval processor idq"
    description = "an item for montitoring approval_processor's response to iDQ information"

    def __init__(self, alert, t0, options, gdb, annotate=False):
        graceid = alert['uid']

        self.ifo = alert['description'].split()[-1]

        timeout = float(options['dt'])
        email = options['email'].split()

        tasks = [approvalProcessoriDQglitchFAPCheck(timeout, self.ifo, email=email)]
        super(ApprovalProcessoriDQItem, self).__init__( graceid,
                                                        gdb,
                                                        t0,
                                                        tasks,
                                                        annotate=annotate
                                                       )

class approvalProcessoriDQglitchFAPCheck(esUtils.EventSupervisorTask):
    """
    a check that approvalProcessor responded to iDQ FAP reports as expected
    """
    description = ""
    name = "approvalProcessoriDQglitchFAP"

    def __init__(self, timeout, ifo, email=[]):
        self.ifo = ifo
        super(approvalProcessoriDQglitchFAPCheck, self).__init__( timeout,
                                                             email=email
                                                           )

    def approvalProcessoriDQglitchFAP(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that approvalProcessor responded to iDQ FAP reports as expected
        NOT IMPLEMENTED
        """
        raise NotImplementedError(self.name)

#-------------------------------------------------
# approvalProcessor VOEvent and GCN
#-------------------------------------------------

class ApprovalProcessorVOEventItem(esUtils.EventSupervisorQueueItem):
    """
    an item for monitoring VOEvent generation and distribution

    alert:
        graceid
    options:
        dt
        email
    """
    name="approval processor voevent"
    description = "check that approval processor generated and distributed VOEvents"

    def __init__(self, alert, t0, options, gdb, annotate=False):
        graceid = alert['uid']

        timeout = float(options['dt'])
        email = options['email'].split()

        tasks = [approvalProcessorVOEventCreationCheck(timeout, email=email),
                 approvalProcessorVOEventDistributionCheck(timeout, email=email)
                ]
        super(ApprovalProcessorVOEventItem, self).__init__( graceid,
                                                            gdb,
                                                            t0,
                                                            tasks,
                                                            annotate=annotate
                                                          )

class approvalProcessorVOEventCreationCheck(esUtils.EventSupervisorTask):
    """
    a check that approval processor created the expected VOEvent
    """
    description = "a check that approval processor created the expected VOEvent"
    name = "approvalProcessorVOEventCreation"

    def __init__(self, timeout, email=[]):
        super(approvalProcessorVOEventCreationCheck, self).__init__( timeout,
                                                                     email=email
                                                                   )

    def approvalProcessorVOEventCreation(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        check that approval processor created the expected VOEvent
        NOT IMPLEMENTED
        """
        raise NotImplementedError(self.name)

class approvalProcessorVOEventDistributionCheck(esUtils.EventSupervisorTask):
    """
    a check that approval processor distributed the VOEvent as expected
    """
    description = "a check that approval processor distributed the VOEvent"
    name = "approvalProcessorVOEventDistribution"

    def __init__(self, timeout, email=[]):
        super(approvalProcessorVOEventDistributionCheck, self).__init__( timeout,
                                                                     email=email
                                                                   )

    def approvalProcessorVOEventDistribution(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        check that approval processor distributed the VOEvent
        NOT IMPLEMENTED
        """
        raise NotImplementedError(self.name)

class ApprovalProcessorGCNItem(esUtils.EventSupervisorQueueItem):
    """
    an item for monitoring GCN generation and distribution

    alert:
        graceid
    options:
        dt
        email
    """
    name = "approval processor gcn"
    description = "check that approval processor generated and distributed GCNs"

    def __init__(self, alert, t0, options, gdb, annotate=False):
        graceid = alert['uid']

        timeout = float(options['dt'])
        email = options['email'].split()

        tasks = [approvalProcessorGCNCreationCheck(timeout, email=email),
                 approvalProcessorGCNDistributionCheck(timeout, email=email)
                ]
        super(ApprovalProcessorGCNItem, self).__init__( graceid,
                                                        gdb,
                                                        t0,
                                                        tasks,
                                                        annotate=annotate
                                                      )

class approvalProcessorGCNCreationCheck(esUtils.EventSupervisorTask):
    """
    a check that approval processor created the GCN as expected
    """
    description = "a check that approval processor created the expected GCN"
    name = "approvalProcessorGCNCreation"

    def __init__(self, timeout, email=[]):
        super(approvalProcessorGCNCreationCheck, self).__init__( timeout,
                                                                 email=email
                                                               )

    def approvalProcessorGCNCreation(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        check that approval processor created the expected GCN
        NOT IMPLEMENTED
        """
        raise NotImplementedError(self.name)


class approvalProcessorGCNDistributionCheck(esUtils.EventSupervisorTask):
    """
    a check that approval processor distributed the GCN as expected
    """
    description = "a check that approval processor distributed the GCN"
    name = "approvalProcessorGCNDistribution"

    def __init__(self, timeout, email=[]):
        super(approvalProcessorGCNDistributionCheck, self).__init__( timeout,
                                                                     email=email
                                                                   )

    def approvalProcessorGCNDistribution(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        check that approval processor distributed the GCN
        NOT IMPLEMENTED
        """
        raise NotImplementedError(self.name)

#-------------------------------------------------
# labeling?
#-------------------------------------------------
"""
need to monitor the appropriate use of
  INJ
  DQV
  EM_READY
  PE_READY
  else? -> ADVREQ, H1REQ, L1REQ, ADVOK, H1OK, L1OK, ADVNO, H1NO, L1NO, 
"""

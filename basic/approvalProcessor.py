description = "a module housing checks of approval_processor functionality"
author = "reed.essick@ligo.org"

#---------------------------------------------------------------------------------------------------

import sys
sys.path.append("../")
import eventSupervisorUtils as esUtils

#---------------------------------------------------------------------------------------------------

#-------------------------------------------------
# approval_processor preliminary DQ checks
#-------------------------------------------------

class ApprovalProcessorPrelimDQItem(esUtils.EventSupervisorQueueItem):
    """
    a set of checks for approval_processor's preliminary DQ and vetting
    """
    description = "a set of checks for approval_processor's preliminary DQ and vetting"

    def __init__(self, graceid, gdb, farTimeout, segStartTimeout, t0, annotate=False, email=[]):
        tasks = [approvalProcessorFARCheck(farTimeout, email=email),
                 approvalProcessorSegDBStartCheck(segStartTimeout, email=email)
                ]
        super(ApprovalProcessorPrelimDQItem, self).__init__( graceid,
                                                             gdb,
                                                             t0,
                                                             tasks,
                                                             description=self.description,
                                                             annotate=annotate
                                                           )

class approvalProcessorFARCheck(esUtils.EventSupervisorTask):
    """
    a check that approvalProcessor analyzed the FAR as expected
    """
    description = ""
    name = "approvalProcessorFARCheck"

    def __init__(self, timeout, email=[]):
        super(approvalProcessorFARCheck, self).__init__( timeout, 
                                                         self.approvalProcessorFARCheck, 
                                                         name=self.name,
                                                         description=self.description, 
                                                         email=email
                                                       )

    def approvalProcessorFARCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that approvalProcessor analyzed the FAR as expected
        NOT IMPLEMENTED
        """
        raise NotImplementedError("approvalProcessorFARCheck")

class approvalProcessorSegDBStartCheck(esUtils.EventSupervisorTask):
    """
    a check that approvalProcessor started checking segments as expected
    """
    description = ""
    name = "approvalProcessorSegDBStartCheck"

    def __init__(self, timeout, email=[]):
        super(approvalProcessorSegDBStartCheck, self).__init__( timeout, 
                                                                self.approvalProcessorSegDBStartCheck, 
                                                                name=self.name,
                                                                description=self.description, 
                                                                email=email
                                                              )

    def approvalProcessorSegDBStartCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that approvalProcessor started checking segments as expected
        NOT IMPLEMENTED
        """
        raise NotImplementedError("approvalProcessorSegDBStartCheck")


class approvalProcessorSegDBFlagsCheck(esUtils.EventSupervisorTask):
    """
    a check that approvalProcessor checked all the segment/flags as expected
    """
    description = ""
    name = "approvalProcessorSegDBFlagsCheck"

    def __init__(self, timeout, flags=[], email=[]):
        self.flags = []
        super(approvalProcessorSegDBFlagsCheck, self).__init__( timeout,
                                                                self.approvalProcessorSegDBFlagsCheck,
                                                                name=self.name,
                                                                description=self.description,
                                                                email=email
                                                              )

    def approvalProcessorSegDBFlagsCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that approvalProcessor checked all the segment/flags as expected
        NOT IMPLEMENTED
        """
        raise NotImplementedError("approvalProcessorSegDBFlagsCheck")

class approvalProcessorSegDBFinishCheck(esUtils.EventSupervisorTask):
    """
    a check that approvalProcessor finished checking segments as expected
    """
    description = ""
    name = "approvalProcessorSegDBFinishCheck"

    def __init__(self, timeout, email=[]):
        super(approvalProcessorSegDBFinishCheck, self).__init__( timeout,
                                                                 self.approvalProcessorSegDBFinishCheck,
                                                                 name=self.name,
                                                                 description=self.description,
                                                                 email=email
                                                               )

    def approvalProcessorSegDBFlagsCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that approvalProcessor finished checking all segments as expected
        NOT IMPLEMENTED
        """
        raise NotImplementedError("approvalProcessorSegDBFinishCheck")


#-------------------------------------------------
#  approvalProcessor_idq
#-------------------------------------------------

class ApprovalProcessoriDQItem(esUtils.EventSupervisorQueueItem):
    """
    an item for monitoring approval processor's response to iDQ information
    """
    description = "an item for montitoring approval_processor's response to iDQ information"

    def __init__(self, graceid, gdb, timeout, ifos, t0, annotate=False, email=[]):
        tasks = [ approvalProcessoriDQglitchFAPCheck(timeout, ifo, email=email) for ifo in ifos ]
        super(ApprovalProcessoriDQItem, self).__init__( graceid,
                                                        gdb,
                                                        t0,
                                                        tasks,
                                                        description=self.description,
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
                                                             self.approvalProcessoriDQglitchFAPCheck,
                                                             name=self.name,
                                                             description=self.description,
                                                             email=email
                                                           )

    def approvalProcessoriDQglitchFAPCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that approvalProcessor responded to iDQ FAP reports as expected
        NOT IMPLEMENTED
        """
        raise NotImplementedError("approvalProcessoriDQgltichFAPCheck")

#-------------------------------------------------
# approvalProcessor VOEvent and GCN
#-------------------------------------------------

class ApprovalProcessorVOEventItem(esUtils.EventSupervisorQueueItem):
    """
    an item for monitoring VOEvent generation and distribution
    """
    description = "check that approval processor generated and distributed VOEvents"

    def __init__(self, graceid, gdb, t0, timeout, annotate=False, email=[]):
        tasks = [approvalProcessorVOEventCreationCheck(timeout, email=email),
                 approvalProcessorVOEventDistributionCheck(timeout, email=email)
                ]
        super(ApprovalProcessorVOEventItem, self).__init__( graceid,
                                                            gdb,
                                                            t0,
                                                            tasks,
                                                            description=self.description,
                                                            annotate=annotate
                                                          )

class approvalProcessorVOEventCreationCheck(esUtils.EventSupervisorTask):
    """
    a check that approval processor created the expected VOEvent
    """
    description = "a check that approval processor created the expected VOEvent"
    name = "approvalProcessorVOEventCreationCheck"

    def __init__(self, timeout, email=[]):
        super(approvalProcessorVOEventCreationCheck, self).__init__( timeout,
                                                                     self.voeventCreationCheck,
                                                                     name=self.name,
                                                                     description=self.description,
                                                                     email=email
                                                                   )

    def voeventCreationCheck(self, graceid, gdb, verbose=False, annotate=False ):
        """
        check that approval processor created the expected VOEvent
        NOT IMPLEMENTED
        """
        raise NotImplementedError

class approvalProcessorVOEventDistributionCheck(esUtils.EventSupervisorTask):
    """
    a check that approval processor distributed the VOEvent as expected
    """
    description = "a check that approval processor distributed the VOEvent"
    name = "approvalProcessorVOEventDistributionCheck"

    def __init__(self, timeout, email=[]):
        super(approvalProcessorVOEventDistributionCheck, self).__init__( timeout,
                                                                     self.voeventDistribCheck,
                                                                     name=self.name,
                                                                     description=self.description,
                                                                     email=email
                                                                   )

    def voeventDistribCheck(self, graceid, gdb, verbose=False, annotate=False ):
        """
        check that approval processor distributed the VOEvent
        NOT IMPLEMENTED
        """
        raise NotImplementedError

class ApprovalProcessorGCNItem(esUtils.EventSupervisorQueueItem):
    """
    an item for monitoring GCN generation and distribution
    """
    description = "check that approval processor generated and distributed GCNs"

    def __init__(self, graceid, gdb, t0, timeout, annotate=False, email=[]):
        tasks = [approvalProcessorGCNCreationCheck(timeout, email=email),
                 approvalProcessorGCNDistributionCheck(timeout, email=email)
                ]
        super(ApprovalProcessorVOEventItem, self).__init__( graceid,
                                                            gdb,
                                                            t0,
                                                            tasks,
                                                            description=self.description,
                                                            annotate=annotate
                                                          )

class approvalProcessorGCNCreationCheck(esUtils.EventSupervisorTask):
    """
    a check that approval processor created the GCN as expected
    """
    description = "a check that approval processor created the expected GCN"
    name = "approvalProcessorGCNCreationCheck"

    def __init__(self, timeout, email=[]):
        super(approvalProcessorGCNCreationCheck, self).__init__( timeout,
                                                                     self.gcnCreationCheck,
                                                                     name=self.name,
                                                                     description=self.description,
                                                                     email=email
                                                                   )

    def gcnCreationCheck(self, graceid, gdb, verbose=False, annotate=False ):
        """
        check that approval processor created the expected GCN
        NOT IMPLEMENTED
        """
        raise NotImplementedError


class approvalProcessorGCNDistributionCheck(esUtils.EventSupervisorTask):
    """
    a check that approval processor distributed the GCN as expected
    """
    description = "a check that approval processor distributed the GCN"
    name = "approvalProcessorGCNDistributionCheck"

    def __init__(self, timeout, email=[]):
        super(approvalProcessorVOEventDistributionCheck, self).__init__( timeout,
                                                                     self.gcnDistribCheck,
                                                                     name=self.name,
                                                                     description=self.description,
                                                                     email=email
                                                                   )

    def gcnDistribCheck(self, graceid, gdb, verbose=False, annotate=False ):
        """
        check that approval processor distributed the GCN
        NOT IMPLEMENTED
        """
        raise NotImplementedError

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

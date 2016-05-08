description = "a module housing checks of DQ summary page functionality"
author = "reed.essick@ligo.org"

#---------------------------------------------------------------------------------------------------

import sys
sys.path.append("../")
import eventSupervisorUtils as esUtils

#---------------------------------------------------------------------------------------------------

class DQSummaryItem(esUtils.EventSupervisorQueueItem):
    """
    a check that a link to the DQ Summary page was posted
    """
    description = "a check that the DQ summary page was posted"

    def __init__(self, graceid, gdb, t0, timeout, annotate=False, email=[]):
        tasks = [dqSummaryCheck(timeout, email=email)]
        super(DQSummaryItem, self).__init__( graceid,
                                             gdb,
                                             t0,
                                             tasks,
                                             description=self.description,
                                             annotate=annotate
                                           )

class dqSummaryCheck(esUtils.EventSupervisorTask):
    """
    a check that a link to the DQ Summary page was posted
    """
    description = "a check that the DQ summary page was posted"
    name = "dqSummaryCheck"

    def __init__(self, timeout, email=[]):
        super(dqSummaryCheck, self).__init__( timeout,
                                              self.dqSummaryCheck,
                                              name=self.name,
                                              description=self.description,
                                              email=email
                                            )

    def dqSummaryCheck(self, graceid, gdb, verbose=False, annotate=False ):
        """
        a check that a link to the DQ Summary page was posted
        NOT IMPLEMENTED
        """
        raise NotImplementedError

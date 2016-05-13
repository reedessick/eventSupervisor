description = "a module housing checks of DQ summary page functionality"
author = "reed.essick@ligo.org"

#---------------------------------------------------------------------------------------------------

import sys
sys.path.append("../")
import eventSupervisorUtils as esUtils

#---------------------------------------------------------------------------------------------------

### methods to identify updates by description

#---------------------------------------------------------------------------------------------------

class DQSummaryItem(esUtils.EventSupervisorQueueItem):
    """
    a check that a link to the DQ Summary page was posted

    alert:
        graceid
    options:
        dt
        email
    """
    name = "dq summary"
    description = "a check that the DQ summary page was posted"

    def __init__(self, alert, t0, options, gdb, annotate=False):
        graceid = alert['uid']

        timeout = float(options['dt'])
        email = options['email'].split()

        tasks = [dqSummaryCheck(timeout, email=email)]
        super(DQSummaryItem, self).__init__( graceid,
                                             gdb,
                                             t0,
                                             tasks,
                                             annotate=annotate
                                           )

class dqSummaryCheck(esUtils.EventSupervisorTask):
    """
    a check that a link to the DQ Summary page was posted
    """
    description = "a check that the DQ summary page was posted"
    name = "dqSummary"

    def __init__(self, timeout, email=[]):
        super(dqSummaryCheck, self).__init__( timeout,
                                              self.dqSummaryCheck,
                                              email=email
                                            )

    def dqSummaryCheck(self, graceid, gdb, verbose=False, annotate=False ):
        """
        a check that a link to the DQ Summary page was posted
        NOT IMPLEMENTED
        """
        raise NotImplementedError(self.name)

description = "a module housing checks of DQ summary page functionality"
author      = "reed.essick@ligo.org"

#---------------------------------------------------------------------------------------------------

import eventSupervisor.eventSupervisorUtils as esUtils

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
    description = "a check that the DQ summary page was posted"
    name        = "dq summary"

    def __init__(self, alert, t0, options, gdb, annotate=False, warnings=False):
        graceid = alert['uid']

        ### extract params
        timeout = float(options['dt'])
        email = options['email'].split()

        ### generate tasks
        tasks = [dqSummaryCheck(timeout, email=email)]

        ### wrap up instantiation
        super(DQSummaryItem, self).__init__( graceid,
                                             gdb,
                                             t0,
                                             tasks,
                                             annotate=annotate,
                                             warnings=warnings,
                                           )

class dqSummaryCheck(esUtils.EventSupervisorTask):
    """
    a check that a link to the DQ Summary page was posted
    """
    description = "a check that the DQ summary page was posted"
    name        = "dqSummary"

    def __init__(self, timeout, email=[]):
        super(dqSummaryCheck, self).__init__( timeout,
                                              email=email
                                            )

    def dqSummary(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that a link to the DQ Summary page was posted
        NOT IMPLEMENTED
        """
        raise NotImplementedError(self.name)

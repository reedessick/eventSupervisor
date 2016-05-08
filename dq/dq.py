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

class dqSummaryCheck(esUtils.EventSupervisorTask):
    """
    a check that a link to the DQ Summary page was posted
    """

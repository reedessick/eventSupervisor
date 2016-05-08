description = "a module housing checks of segDB2GraceDB functionality"
author = "reed.essick@ligo.org"

#---------------------------------------------------------------------------------------------------

import sys
sys.path.append("../")
import eventSupervisorUtils as esUtils

#---------------------------------------------------------------------------------------------------

class SegDB2GrcDBStartItem(esUtils.EventSupervisorQueueItem):
    """
    a check that segDB2grcDB started
    """

class segDB2grcDBStartCheck(esUtils.EventSupervisorTask):
    """
    a check that segDB2grcDB started
    """

class SegDB2GrcDBItem(esUtils.EventSupervisorQueueItem):
    """
    a check that segDB2grcDB uploaded the expected queries and finished
    """

class segDB2grcDBFlagsCheck(esUtils.EventSupervisorTask):
    """
    a check that segDB2grcDB uploaded the expected individual flags
    """

class segDB2grcDBVetoDefCheck(esUtils.EventSupervisorTask):
    """
    a check that segDB2grcDB uploaded the expected summary of VetoDefiner queries
    """

class segDB2grcDBAnyCheck(esUtils.EventSupervisorTask):
    """
    a check that segDB2grcDB uploaded the expected query of any active segments
    """

class segDB2grcDBFinishCheck(esUtils.EventSupervisorTask):
    """
    a check that segDB2grcDB finished as expected
    """

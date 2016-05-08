description = "a module housing checks of OmegaScans functionality"
author = "reed.essick@ligo.org"

#---------------------------------------------------------------------------------------------------

import sys
sys.path.append("../")
import eventSupervisorUtils as esUtils

#---------------------------------------------------------------------------------------------------

class OmegaScanStartItem(esUtils.EventSupervisorQueueItem):
    """
    a check that OmegaScans were started
    """

class omegaScanStartCheck(esUtils.EventSupervisorTask):
    """
    a check that OmegaScans were started
    """

class OmegaScanItem(esUtils.EventSupervisorQueueItem):
    """
    a check that OmegaScans uploaded data and finished as expected
    """

class omegaScanDataCheck(esUtils.EventSupervisorTask):
    """
    a check that OmegaScans uploaded data
    """

class omegaScansFinishCheck(esUtils.EventSupervisorTask):
    """
    a check that OmegaScans finished as expected
    """



"""
need to set this up so these classes can be used for
  h(t)
  all aux chans
  iDQ specific chans

we may do this with further inheritence... or just passing some keyword argument?
"""

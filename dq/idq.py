description = "a module housing checks of iDQ functionality"
author = "reed.essick@ligo.org"

#---------------------------------------------------------------------------------------------------

import sys
sys.path.append("../")
import eventSupervisorUtils as esUtils

#---------------------------------------------------------------------------------------------------

class IDQStartItem(esUtils.EventSupervisorQueueItem):
    """
    a check that iDQ started as expected
    """

class idqStartCheck(esUtils.EventSupervisorTask):
    """
    a check that iDQ started as expected
    """

class IDQItem(esUtils.EventSupervisorQueueItem):
    """
    a check that iDQ reported the timeseries information as expected
    """

class idqGlichFAPCheck(esUtils.EventSupervisorTask):
    """
    a check that iDQ reported the glitch-FAP as expected
    """

class idqTimeseriesCheck(esUtils.EventSupervisorTask):
    """
    a check that iDQ reported timeseries information as expected
    """

class idqTablesCheck(esUtils.EventSupervisorTask):
    """
    a check that iDQ reported the xml tables as expected
    """

class idqPerformanceCheck(esUtils.EventSupervisorTask):
    """
    a check that iDQ reported historical performance as expected
    """

class idqFinishCheck(esUtils.EventSupervisorTask):
    """
    a check that iDQ finished as expected
    """

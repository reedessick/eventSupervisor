description = "a module housing checks of iDQ functionality"
author = "reed.essick@ligo.org"

#---------------------------------------------------------------------------------------------------

import sys
sys.path.append("../")
import eventSupervisorUtils as esUtils

#---------------------------------------------------------------------------------------------------

def is_idqAlert( alert ):
    """
    determine if this is an iDQ messages
    """
    return 'idq' in alert['tagname']

#---------------------------------------------------------------------------------------------------

"""
define queueItems for the following:
  idq_start
  idq_glitchFAP
  idq_timeseries
  idq_tables
  idq_performance
  idq_finish
"""

description = "a module housing checks of LALInference-PE functionality"
author = "reed.essick@ligo.org"

#---------------------------------------------------------------------------------------------------

import sys
sys.path.append("../")
import eventSupervisorUtils as esUtils

#---------------------------------------------------------------------------------------------------

"""
define queueItems for the following:
  lalinfPE_start
  lalinfPE_postSamp
  lalinfPE_skymap
  lalinfPE_finish
"""

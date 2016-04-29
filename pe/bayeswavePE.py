description = "a module housing checks of BayesWave-PE functionality"
author = "reed.essick@ligo.org"

#---------------------------------------------------------------------------------------------------

import sys
sys.path.append("../")
import eventSupervisorUtils as esUtils

#---------------------------------------------------------------------------------------------------

"""
define queueItems for the following:
  bayeswavePE_start
  bayeswavePE_postSamp
  bayeswavePE_skymap
  bayeswavePE_finish
"""

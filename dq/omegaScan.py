description = "a module housing checks of OmegaScans functionality"
author = "reed.essick@ligo.org"

#---------------------------------------------------------------------------------------------------

from ligo.lvalert import lvalertMPutils as utils

#---------------------------------------------------------------------------------------------------

"""
define queueItems for the following:
  HofTOmegaScan_start
  HofTOmegaScan_data
  HofTOmegaScan_finish
  allAuxOmegaScan_start
  allAuxOmegaScan_data
  allAuxOmegaScan_finish
  idqOmegaScan_start
  idqOmegaScan_data
  idqOmegaScan_finish

NOTE: we may be able to get away with only defining 3 classes and re-using them as needed
"""

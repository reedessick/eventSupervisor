description = "a module housing checks of skymaps functionality"
author = "reed.essick@ligo.org"

#---------------------------------------------------------------------------------------------------

import sys
sys.path.append("../")
import eventSupervisorUtils as esUtils

#---------------------------------------------------------------------------------------------------

#-------------------------------------------------
# sanity and formatting
#-------------------------------------------------

class SkymapSanityItem(esUtils.EventSupervisorQueueItem):
    """
    a check for sane and properly formatted skymaps
    """

    def __init__(self, graceid, gdb, fitsname, t0, timeout, annotate=False, email=[]):
        self.description = "check sanity and formatting of %s"%fitsname
        tasks = [skymapSanityCheck(timeout, fitsname, email=email)]
        super(SkymapSanityItem, self).__init__( graceid,
                                                gdb,
                                                t0,
                                                tasks,
                                                description=self.description,
                                                annotate=annotate
                                              )

class skymapSanityCheck(esUtils.EventSupervisorTask):
    """
    a check for sane and properly formatted skymaps
    """
    name = "skymapSanityCheck"

    def __init__(self, timeout, fitsname, email=[]):
        self.description = "check sanity and formatting of %s"%fitsname
        self.fitsname = fitsname
        super(skymapSanityCheck, self).__init__( timeout,
                                                 self.skymapSanityCheck,
                                                 name=self.name,
                                                 description=self.description,
                                                 email=email
                                               )
    
    def skymapSanityCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        check the skymap for sane and proper formatting
        NOT IMPLEMENTED
        """
        raise NotImplementedError

#-------------------------------------------------
# plotting
#-------------------------------------------------

class PlotSkymapItem(esUtils.EventSupervisorQueueItem):
    """
    a check that plotting jobs ran and tagged figures properly
    """

    def __init__(self, graceid, gdb, fitsname, tagnames, t0, timeout, annotate=False, email=[]):
        self.description = "check plotting jobs for %s"%fitsname
        tasks = [plotSkymapCheck(timeout, fitsname, tagnames, email=email)]
        super(PlotSkymapItem, self).__init__( graceid,
                                               gdb,
                                               t0,
                                               tasks,
                                               description=description,
                                               annotate=annotate
                                             )

class plotSkymapCheck(esUtils.EventSupervisorTask):
    """
    a check that plotting jobs ran and tagged figures properly
    """
    name = "plotSkymapCheck"

    def __init__(self, timeout, fitsname, tagnames, email=[]):
        self.description = "check sanity and formatting of %s"%fitsname
        self.fitsname = fitsname
        self.tagnames = tagnames
        super(plotSkymapCheck, self).__init__( timeout,
                                               self.plotSkymapCheck,
                                               name=self.name,
                                               description=self.description,
                                               email=email
                                             )

    def plotSkymapCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that plotting jobs ran and tagged figures properly
        NOT IMPLEMENTED
        """
        raise NotImplementedError

#-------------------------------------------------
# skyviewer
#-------------------------------------------------

class SkyviewerItem(esUtils.EventSupervisorQueueItem):
    """
    a check that skyviewer ran and tagged files appropriately
    """

    def __init__(self, graceid, gdb, fitsname, tagnames, t0, timeout, annotate=False, email=[]):
        self.description = "check plotting jobs for %s"%fitsname
        tasks = [skyviewerCheck(timeout, fitsname, tagnames, email=email)]
        super(PlotSkymapItem, self).__init__( graceid,
                                               gdb,
                                               t0,
                                               tasks,
                                               description=description,
                                               annotate=annotate
                                             )

class skyviewerCheck(esUtils.EventSupervisorTask):
    """
    a check that skyviewer ran and tagged files appropriately
    """
    name = "skyviewerCheck"

    def __init__(self, timeout, fitsname, tagnames, email=[]):
        self.description = "check sanity and formatting of %s"%fitsname
        self.fitsname = fitsname
        self.tagnames = tagnames
        super(skyviewerCheck, self).__init__( timeout,
                                              self.skyviewerCheck,
                                              name=self.name,
                                              description=self.description,
                                              email=email
                                            )

    def skyviewerCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that plotting jobs ran and tagged figures properly
        NOT IMPLEMENTED
        """
        raise NotImplementedError


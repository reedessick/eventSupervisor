description = "a module housing checks of skymap summary functionality"
author = "reed.essick@ligo.org"

#---------------------------------------------------------------------------------------------------

import sys
sys.path.append("../")
import eventSupervisorUtils as esUtils

#---------------------------------------------------------------------------------------------------

#-------------------------------------------------
# skymap autosummary
#-------------------------------------------------

class SkymapSummaryStartItem(esUtils.EventSupervisorQueueItem):
    """
    a check that the autosummary of skymaps started as expected
    """

    def __init__(self, graceid, gdb, fitsname, t0, timeout, annotate=False, email=[]):
        self.description = "check that autosummary of skymaps started processing %s"%fitsname
        tasks = [skymapSummaryStartCheck(timeout, fitsname, email=email)]
        super(SkymapSummaryStartItem, self).__init__( graceid,
                                                      gdb,
                                                      t0,
                                                      tasks,
                                                      description=self.description,
                                                      annotate=annotate
                                                    )


class skymapSummaryStartCheck(esUtils.EventSupervisorTask):
    """
    a check that skymap autosummary started as expected
    """
    name = "skymapSummaryStartCheck"

    def __init__(self, timeout, fitsname, email=[]):
        self.fitsname = fitsname
        self.description = "check that autosummary of skymaps started processing %s"%fitsname
        super(skymapSummaryStartCheck, self).__init__( timeout,
                                                       self.skymapSummaryStartCheck,
                                                       name=self.name,
                                                       description=self.description,
                                                       email=email
                                                     )

    def skymapSummaryStartCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that skymap autosummary started as expected
        NOT IMPLEMENTED
        """
        raise NotImplementedError


class SkymapSummaryItem(esUtils.EventSupervisorQueueItem):
    """
    a check that autosummary of skymaps ran and reported as expected
    """

    def __init__(self, graceid, gdb, fitsname, t0, timeout, annotate=False, email=[]):
        self.description = "check that autosummary of skymaps picked up and correctly processed %s"%fitsname
        tasks = [skymapSummaryDataCheck(timeout, fitsname, email=email),
                 skymapSummaryFinishCheck(timeout, fitsname, email=email)
                ]
        super(SkymapSummaryItem, self).__init__( graceid,
                                                 gdb,
                                                 t0,
                                                 tasks,
                                                 description=self.description,
                                                 annotate=annotate
                                               )

class skymapSummaryDataCheck(esUtils.EventSupervisorTask):
    """
    a check that skymap autosummary generated the expected data
    """
    name = "skymapSummaryDataCheck"

    def __init__(self, timeout, fitsname, email=[]):
        self.fitsname = fitsname
        self.description = "check that autosummary of skymaps generated the expected data for %s"%fitsname
        super(skymapSummaryDataCheck, self).__init__( timeout,
                                                      self.skymapSummaryStartCheck,
                                                      name=self.name,
                                                      description=self.description,
                                                      email=email
                                                    )

    def skymapSummaryDataCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that skymap autosummary generated the expected data
        NOT IMPLEMENTED
        """
        raise NotImplementedError

class skymapSummaryFinishCheck(esUtils.EventSupervisorTask):
    """
    a check that skymap autosummary finished as expected
    """
    name = "skymapSummaryFinishCheck"

    def __init__(self, timeout, fitsname, email=[]):
        self.fitsname = fitsname
        self.description = "check that autosummary of skymaps finished as expected for %s"%fitsname
        super(skymapSummaryFinishCheck, self).__init__( timeout,
                                                        self.skymapSummaryStartCheck,
                                                        name=self.name,
                                                        description=self.description,
                                                        email=email
                                                      )

    def skymapSummaryFinishCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that skymap autosummary finished as expected
        NOT IMPLEMENTED
        """
        raise NotImplementedError

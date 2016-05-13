description = "a module housing checks of skymap summary functionality"
author = "reed.essick@ligo.org"

#---------------------------------------------------------------------------------------------------

import sys
sys.path.append("../")
import eventSupervisorUtils as esUtils

#---------------------------------------------------------------------------------------------------

### methods to identify updates by description

def is_skymapSummaryStart( description ):
    ''' determine whether description is for a skymap summary start alert by matching a string fragment. NOT IMPLEMENTED -> return False '''
    return False

#---------------------------------------------------------------------------------------------------

#-------------------------------------------------
# skymap autosummary
#-------------------------------------------------

class SkymapSummaryStartItem(esUtils.EventSupervisorQueueItem):
    """
    a check that the autosummary of skymaps started as expected

    alert:
        graceid
        fitsname
    options:
        dt
        email
    """
    name = "skymap summary start"

    def __init__(self, alert, t0, options, gdb, annotate=False):
        graceid = alert['uid']

        self.fitsname = alert['file']

        timeout = float(options['dt'])
        email = options['email'].split()

        self.description = "check that autosummary of skymaps started processing %s"%self.fitsname
        tasks = [skymapSummaryStartCheck(timeout, fitsname, email=email)]
        super(SkymapSummaryStartItem, self).__init__( graceid,
                                                      gdb,
                                                      t0,
                                                      tasks,
                                                      annotate=annotate
                                                    )


class skymapSummaryStartCheck(esUtils.EventSupervisorTask):
    """
    a check that skymap autosummary started as expected
    """
    name = "skymapSummaryStart"

    def __init__(self, timeout, fitsname, email=[]):
        self.fitsname = fitsname
        self.description = "check that autosummary of skymaps started processing %s"%fitsname
        super(skymapSummaryStartCheck, self).__init__( timeout,
                                                       self.skymapSummaryStartCheck,
                                                       email=email
                                                     )

    def skymapSummaryStartCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that skymap autosummary started as expected
        NOT IMPLEMENTED
        """
        raise NotImplementedError(self.name)


class SkymapSummaryItem(esUtils.EventSupervisorQueueItem):
    """
    a check that autosummary of skymaps ran and reported as expected

    alert:
        graceid
        fitsname
    options:
        data dt
        finish dt
        email
    """
    name = "skymap summary"

    def __init__(self, alert, t0, options, gdb, annotate=False):
        graceid = alert['uid']

        self.fitsname = alert['description'].split()[-1] ### likely to break because I haven't written this yet...

        data_dt = float(options['data dt'])
        finish_dt = float(options['finish dt'])
        email = options['email'].split()

        self.description = "check that autosummary of skymaps picked up and correctly processed %s"%self.fitsname
        tasks = [skymapSummaryDataCheck(data_dt, fitsname, email=email),
                 skymapSummaryFinishCheck(finish_dt, fitsname, email=email)
                ]
        super(SkymapSummaryItem, self).__init__( graceid,
                                                 gdb,
                                                 t0,
                                                 tasks,
                                                 annotate=annotate
                                               )

class skymapSummaryDataCheck(esUtils.EventSupervisorTask):
    """
    a check that skymap autosummary generated the expected data
    """
    name = "skymapSummaryData"

    def __init__(self, timeout, fitsname, email=[]):
        self.fitsname = fitsname
        self.description = "check that autosummary of skymaps generated the expected data for %s"%fitsname
        super(skymapSummaryDataCheck, self).__init__( timeout,
                                                      self.skymapSummaryStartCheck,
                                                      email=email
                                                    )

    def skymapSummaryDataCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that skymap autosummary generated the expected data
        NOT IMPLEMENTED
        """
        raise NotImplementedError(self.name)

class skymapSummaryFinishCheck(esUtils.EventSupervisorTask):
    """
    a check that skymap autosummary finished as expected
    """
    name = "skymapSummaryFinish"

    def __init__(self, timeout, fitsname, email=[]):
        self.fitsname = fitsname
        self.description = "check that autosummary of skymaps finished as expected for %s"%fitsname
        super(skymapSummaryFinishCheck, self).__init__( timeout,
                                                        self.skymapSummaryStartCheck,
                                                        email=email
                                                      )

    def skymapSummaryFinishCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that skymap autosummary finished as expected
        NOT IMPLEMENTED
        """
        raise NotImplementedError(self.name)

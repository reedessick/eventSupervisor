description = "a module housing checks of skymap summary functionality"
author      = "reed.essick@ligo.org"

#---------------------------------------------------------------------------------------------------

import eventSupervisor.eventSupervisorUtils as esUtils

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
        tagnames
    options:
        dt
        email
    """
    name = "skymap summary start"

    def __init__(self, alert, t0, options, gdb, annotate=False, warnings=False, logDir='.', logTag='iQ'):
        graceid = alert['uid']
        self.fitsname = alert['file']
        self.tagnames = alert['object']['tag_names']

        self.description = "check that autosummary of skymaps started processing %s"%self.fitsname

        ### extract params from config
        timeout = float(options['dt'])
        email = options['email'].split()

        ### generate tasks
        tasks = [skymapSummaryStartCheck(timeout, self.fitsname, tagnames=self.tagnames, email=email, logDir=logDir, logTag='%s.%s'%(logTag, self.name))]

        ### wrap up instantiation
        super(SkymapSummaryStartItem, self).__init__( graceid,
                                                      gdb,
                                                      t0,
                                                      tasks,
                                                      annotate=annotate,
                                                      warnings=warnings,
                                                      logDir=logDir,
                                                      logTag=logTag,
                                                    )


class skymapSummaryStartCheck(esUtils.EventSupervisorTask):
    """
    a check that skymap autosummary started as expected
    """
    name = "skymapSummaryStart"

    def __init__(self, timeout, fitsname, tagnames=[], email=[], logDir='.', logTag='iQ'):
        self.fitsname = fitsname
        self.tagnames = tagnames
        self.description = "check that autosummary of skymaps started processing %s"%fitsname
        super(skymapSummaryStartCheck, self).__init__( timeout,
                                                       email=email,
                                                       logDir=logDir,
                                                       logTag=logTag,
                                                     )

    def skymapSummaryStart(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
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
        tagnames
    options:
        data dt
        finish dt
        email
    """
    name = "skymap summary"

    def __init__(self, alert, t0, options, gdb, annotate=False, warnings=False, logDir='.', logTag='iQ'):
        graceid = alert['uid']
        self.fitsname = alert['description'].split()[-1] ### likely to break because I haven't written this yet...
        self.tagnames = alert['object']['tag_names']

        self.description = "check that autosummary of skymaps picked up and correctly processed %s"%self.fitsname

        ### extract params from config
        data_dt   = float(options['data dt'])
        finish_dt = float(options['finish dt'])
        email     = options['email'].split()

        ### generate tasks
        taskTag = '%s.%s'%(logTag, self.name)
        tasks = [skymapSummaryDataCheck(data_dt, self.fitsname, tagnames=self.tagnames, email=email, logDir=logDir, logTag=logTag),
                 skymapSummaryFinishCheck(finish_dt, self.fitsname, tagnames=self.tagnames, email=email, logDir=logDir, logTag=logTag)
                ]

        ### wrap up instantiation
        super(SkymapSummaryItem, self).__init__( graceid,
                                                 gdb,
                                                 t0,
                                                 tasks,
                                                 annotate=annotate,
                                                 warnings=warnings,
                                                 logDir=logDir,
                                                 logTag=logTag,
                                               )

class skymapSummaryDataCheck(esUtils.EventSupervisorTask):
    """
    a check that skymap autosummary generated the expected data
    """
    name = "skymapSummaryData"

    def __init__(self, timeout, fitsname, tagnames=[], email=[], logDir='.', logTag='iQ'):
        self.fitsname = fitsname
        self.tagnames = tagnames
        self.description = "check that autosummary of skymaps generated the expected data for %s"%fitsname
        super(skymapSummaryDataCheck, self).__init__( timeout,
                                                      email=email,
                                                      logDir=logDir,
                                                      logTag=logTag,
                                                    )

    def skymapSummaryData(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
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

    def __init__(self, timeout, fitsname, tagnames=[], email=[], logDir='.', logTag='iQ'):
        self.fitsname = fitsname
        self.tagnames = tagnames
        self.description = "check that autosummary of skymaps finished as expected for %s"%fitsname
        super(skymapSummaryFinishCheck, self).__init__( timeout,
                                                        email=email,
                                                        logDir=logDir,
                                                        logTag=logTag,
                                                      )

    def skymapSummaryFinish(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that skymap autosummary finished as expected
        NOT IMPLEMENTED
        """
        raise NotImplementedError(self.name)

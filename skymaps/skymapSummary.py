description = "a module housing checks of skymap summary functionality"
author      = "reed.essick@ligo.org"

#---------------------------------------------------------------------------------------------------

import eventSupervisor.eventSupervisorUtils as esUtils

#---------------------------------------------------------------------------------------------------

### methods to identify updates by description

def is_snglFITSStart( description ):
    ''' determine whether description is for a snglFITS start alert by matching a string fragment.'''
    raise NotImplementedError('is_SnglFITSStart')
    return False

def is_snglFITSFinish( description ):
    ''' determine whether description is for a snglFITS finish alert by matching a string fragment.'''
    raise NotImplementedError('is_SnglFITSFinish')
    return False

def is_multFITSStart( description ):
    ''' determine whether description is for multFITS start alert by matching a string fragment.'''
    raise NotImplementedError('is_MultFITSStart')
    return False

#---------------------------------------------------------------------------------------------------

#-------------------------------------------------
# skymap autosummary
#-------------------------------------------------

class SnglFITSStartItem(esUtils.EventSupervisorQueueItem):
    """
    a check that snglFITS started as expected

    alert:
        graceid
        fitsname
        tagnames
    options:
        dt
        email
    """
    name = "snglFITS start"

    def __init__(self, alert, t0, options, gdb, annotate=False, warnings=False, logDir='.', logTag='iQ'):
        graceid = alert['uid']
        self.fitsname = alert['file']
        self.tagnames = alert['object']['tag_names']

        self.description = "check that snglFITS started processing %s"%self.fitsname

        ### extract params from config
        timeout = float(options['dt'])
        email = options['email'].split()

        ### generate tasks
        tasks = [snglFITSStartCheck(timeout, self.fitsname, tagnames=self.tagnames, email=email, logDir=logDir, logTag='%s.%s'%(logTag, self.name))]

        ### wrap up instantiation
        super(SnglFITSStartItem, self).__init__( graceid,
                                                      gdb,
                                                      t0,
                                                      tasks,
                                                      annotate=annotate,
                                                      warnings=warnings,
                                                      logDir=logDir,
                                                      logTag=logTag,
                                                    )


class snglFITSStartCheck(esUtils.EventSupervisorTask):
    """
    a check that snglFITS started as expected
    """
    name = "snglFITSStart"

    def __init__(self, timeout, fitsname, tagnames=[], email=[], logDir='.', logTag='iQ'):
        self.fitsname = fitsname
        self.tagnames = tagnames
        self.description = "check that snglFITS started processing %s"%fitsname
        super(snglFITSStartCheck, self).__init__( timeout,
                                                       email=email,
                                                       logDir=logDir,
                                                       logTag=logTag,
                                                     )

    def snglFITSStart(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that snglFITS started as expected
        NOT IMPLEMENTED
        """
        raise NotImplementedError(self.name)

class SnglFITSItem(esUtils.EventSupervisorQueueItem):
    """
    a check that snglFITS ran as expected

    alert:
        graceid
        fitsname
        tagnames
    options:
        dt
        email
    """
    name = "snglFITS"

    def __init__(self, alert, t0, options, gdb, annotate=False, warnings=False, logDir='.', logTag='iQ'):
        graceid = alert['uid']

        raise NotImplementedError(self.name) ### FIXME: need to parse out filename from log comment, get tagnames from looking through log? Just ignore tagnames? Include those in the log comment from within snglFITS.py?

        self.fitsname = alert['file']
        self.tagnames = alert['object']['tag_names']

        self.description = "check that snglFITS started processing %s"%self.fitsname

        ### extract params from config
        timeout = float(options['dt'])
        email = options['email'].split()

        ### generate tasks
        tasks = [snglFITSFinishCheck(timeout, self.fitsname, tagnames=self.tagnames, email=email, logDir=logDir, logTag='%s.%s'%(logTag, self.name))]

        ### wrap up instantiation
        super(SnglFITSItem, self).__init__( graceid,
                                                      gdb,
                                                      t0,
                                                      tasks,
                                                      annotate=annotate,
                                                      warnings=warnings,
                                                      logDir=logDir,
                                                      logTag=logTag,
                                                    )


class snglFITSFinishCheck(esUtils.EventSupervisorTask):
    """
    a check that snglFITS finished as expected
    """
    name = "snglFITSFinish"

    def __init__(self, timeout, fitsname, tagnames=[], email=[], logDir='.', logTag='iQ'):
        self.fitsname = fitsname
        self.tagnames = tagnames
        self.description = "check that snglFITS finished processing %s"%fitsname
        super(snglFITSFinishCheck, self).__init__( timeout,
                                                       email=email,
                                                       logDir=logDir,
                                                       logTag=logTag,
                                                     )

    def snglFITSFinish(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that snglFITS finished as expected
        NOT IMPLEMENTED
        """
        raise NotImplementedError(self.name)

class MultFITSStartItem(esUtils.EventSupervisorQueueItem):
    """
    a check that multFITS started as expected

    alert:
        graceid
        fitsname
        tagnames
    options:
        dt
        email
    """
    name = "multFITS start"

    def __init__(self, alert, t0, options, gdb, annotate=False, warnings=False, logDir='.', logTag='iQ'):
        graceid = alert['uid']

        raise NotImplementedError(self.name) ### FIXME: need to parse out filename from log comment, get tagnames from looking through log? Just ignore tagnames? Include those in the log comment from within snglFITS.py?

        self.fitsname = alert['file']
        self.tagnames = alert['object']['tag_names']

        self.description = "check that multFITS started processing %s"%self.fitsname

        ### extract params from config
        timeout = float(options['dt'])
        email = options['email'].split()

        ### generate tasks
        tasks = [multFITSStartCheck(timeout, self.fitsname, tagnames=self.tagnames, email=email, logDir=logDir, logTag='%s.%s'%(logTag, self.name))]

        ### wrap up instantiation
        super(MultFITSStartItem, self).__init__( graceid,
                                                      gdb,
                                                      t0,
                                                      tasks,
                                                      annotate=annotate,
                                                      warnings=warnings,
                                                      logDir=logDir,
                                                      logTag=logTag,
                                                    )

class multFITSStartCheck(esUtils.EventSupervisorTask):
    """
    a check that multFITS started as expected
    """
    name = "multFITSStart"

    def __init__(self, timeout, fitsname, tagnames=[], email=[], logDir='.', logTag='iQ'):
        self.fitsname = fitsname
        self.tagnames = tagnames
        self.description = "check that multFITS started processing %s"%fitsname
        super(multFITSStartCheck, self).__init__( timeout,
                                                       email=email,
                                                       logDir=logDir,
                                                       logTag=logTag,
                                                     )

    def snglFITSStart(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that multFITS started as expected
        NOT IMPLEMENTED
        """
        raise NotImplementedError(self.name)

class MultFITSItem(esUtils.EventSupervisorQueueItem):
    """
    a check that multFITS ran as expected

    alert:
        graceid
        fitsname
        tagnames
    options:
        dt
        email
    """
    name = "multFITS"

    def __init__(self, alert, t0, options, gdb, annotate=False, warnings=False, logDir='.', logTag='iQ'):
        graceid = alert['uid']

        raise NotImplementedError(self.name) ### FIXME: need to parse out filename from log comment, get tagnames from looking through log? Just ignore tagnames? Include those in the log comment from within snglFITS.py?

        self.fitsname = alert['file']
        self.tagnames = alert['object']['tag_names']

        self.description = "check that multFITS started processing %s"%self.fitsname

        ### extract params from config
        timeout = float(options['dt'])
        email = options['email'].split()

        ### generate tasks
        tasks = [multFITSFinishCheck(timeout, self.fitsname, tagnames=self.tagnames, email=email, logDir=logDir, logTag='%s.%s'%(logTag, self.name))]

        ### wrap up instantiation
        super(multFITSItem, self).__init__( graceid,
                                                      gdb,
                                                      t0,
                                                      tasks,
                                                      annotate=annotate,
                                                      warnings=warnings,
                                                      logDir=logDir,
                                                      logTag=logTag,
                                                    )

class multFITSFinishCheck(esUtils.EventSupervisorTask):
    """
    a check that multFITS finished as expected
    """
    name = "multFITSFinish"

    def __init__(self, timeout, fitsname, tagnames=[], email=[], logDir='.', logTag='iQ'):
        self.fitsname = fitsname
        self.tagnames = tagnames
        self.description = "check that multFITS fimished processing %s"%fitsname
        super(multFITSFinishCheck, self).__init__( timeout,
                                                       email=email,
                                                       logDir=logDir,
                                                       logTag=logTag,
                                                     )

    def snglFITSFinish(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that multFITS finish as expected
        NOT IMPLEMENTED
        """
        raise NotImplementedError(self.name)

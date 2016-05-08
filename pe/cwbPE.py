description = "a module housing checks of cWB-PE functionality"
author = "reed.essick@ligo.org"

#---------------------------------------------------------------------------------------------------

import sys
sys.path.append("../")
import eventSupervisorUtils as esUtils

#---------------------------------------------------------------------------------------------------

class CWBPEStartItem(esUtils.EventSupervisorQueueItem):
    """
    a check that cWB PE started
    """
    description = "a check that cWB PE started"

    def __init__(self, graceid, gdb, t0, timeout, annotate=False, email=[]):
        tasks = [cWBPEStartCheck(timeout, email)]
        super(CWBPEStartItem, self).__init__( graceid,
                                              gdb,
                                              t0,
                                              tasks,
                                              description=self.description,
                                              annotate=annotate
                                            )

class cWBPEStartCheck(esUtils.EventSupervisorTask):
    """
    a check that cWB PE started
    """    
    name = "cWBPEStartCheck"
    description = "a check that cWB PE started"

    def __init__(self, timeout, email=[]):
        super(cWBPEStartCheck, self).__init__( timeout,
                                               self.cWBPEStartCheck,
                                               name=self.name,
                                               description=self.description,
                                               email=email
                                             )

    def cWBPEStartCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that cWB PE started
        NOT IMPLEMENTED
        """
        raise NotImplementedError

class CWBPEItem(esUtils.EventSupervisorQueueItem):
    """
    a check that cWB PE produces the expected data and finished
    """
    description = "a check that cWB PE produced the expected data and finished"

    def __init__(self, graceid, gdb, t0, timeout, annotate=False, email=[]):
        tasks = [cWBPEDataCheck(timeout, email=email),
                 cWBPESkymapCheck(timeout, email=email),
                 cWBPEFinishCheck(timeout, email=email)
                ]
        super(CWBPEItem, self).__init__( graceid, 
                                         gdb,
                                         t0,
                                         tasks,
                                         description=self.description,
                                         annotate=annotate
                                       )

class cWBPEDataCheck(esUtils.EventSupervisorTask):
    """
    a check that cWB PE posted estimates of parameters
    """
    name = "cWBPEDataCheck"
    description = "a check that cWB PE posted estimates of parameters"

    def __init__(self, timeout, email=[]):
        super(cWBPEDataCheck, self).__init__( timeout,
                                                  self.cWBPEDataCheck,
                                                  name=self.name,
                                                  descripiton=self.description,
                                                  email=email
                                                )

    def cWBPEDataCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that cWB PE posted posterior samples
        NOT IMPLEMENTED
        """
        raise NotImplementedError

class cWBPESkymapCheck(esUtils.EventSupervisorTask):
    """
    a check that cWB PE posted a skymap
    """
    name = "cWBPESkymapCheck"
    description = "a check that cWB PE posted a skymap"

    def __init__(self, timeout, email=[]):
        super(cWBPESkymapCheck, self).__init__( timeout,
                                                self.cWBPESkymapCheck,
                                                name=self.name,
                                                descripiton=self.description,
                                                email=email
                                              )

    def cWBPESkymapCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that cWB PE posted a skymap
        NOT IMPLEMENTED
        """
        raise NotImplementedError

class cWBPEFinishCheck(esUtils.EventSupervisorTask):
    """
    a check that cWB PE finished
    """
    name = "cWBPEFinishCheck"
    description = "a check that cWB PE finished"

    def __init__(self, timeout, email=[]):
        super(cWBPEFinishCheck, self).__init__( timeout,
                                                self.cWBPEFinishCheck,
                                                name=self.name,
                                                descripiton=self.description,
                                                email=email
                                              )

    def cWBPEFinishCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that cWB PE finished
        NOT IMPLEMENTED
        """
        raise NotImplementedError

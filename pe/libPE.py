description = "a module housing checks of LIB-PE functionality"
author = "reed.essick@ligo.org"

#---------------------------------------------------------------------------------------------------

import sys
sys.path.append("../")
import eventSupervisorUtils as esUtils

#---------------------------------------------------------------------------------------------------

class LIBPEStartItem(esUtils.EventSupervisorQueueItem):
    """
    a check that LIB PE started
    """
    description = "a check that LIB PE started"

    def __init__(self, graceid, gdb, t0, timeout, annotate=False, email=[]):
        tasks = [libPEStartCheck(timeout, email)]
        super(LIBPEStartItem, self).__init__( graceid,
                                              gdb,
                                              t0,
                                              tasks,
                                              description=self.description,
                                              annotate=annotate
                                            )

class libPEStartCheck(esUtils.EventSupervisorTask):
    """
    a check that LIB PE started
    """    
    name = "libPEStartCheck"
    description = "a check that LIB PE started"

    def __init__(self, timeout, email=[]):
        super(libPEStartCheck, self).__init__( timeout,
                                               self.libPEStartCheck,
                                               name=self.name,
                                               description=self.description,
                                               email=email
                                             )

    def libPEStartCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that LIB PE started
        NOT IMPLEMENTED
        """
        raise NotImplementedError

class LIBPEItem(esUtils.EventSupervisorQueueItem):
    """
    a check that LIB PE produces the expected data and finished
    """
    description = "a check that LIB PE produced the expected data and finished"

    def __init__(self, graceid, gdb, t0, timeout, annotate=False, email=[]):
        tasks = [libPEPostSampCheck(timeout, email=email),
                 libPESkymapCheck(timeout, email=email),
                 libPEFinishCheck(timeout, email=email)
                ]
        super(LIBPEItem, self).__init__( graceid, 
                                         gdb,
                                         t0,
                                         tasks,
                                         description=self.description,
                                         annotate=annotate
                                       )

class libPEPostSampCheck(esUtils.EventSupervisorTask):
    """
    a check that LIB PE posted posterior samples
    """
    name = "libPEPostSampCheck"
    description = "a check that LIB PE posted posterior samples"

    def __init__(self, timeout, email=[]):
        super(libPEPostSampCheck, self).__init__( timeout,
                                                  self.libPEPostSampCheck,
                                                  name=self.name,
                                                  descripiton=self.description,
                                                  email=email
                                                )

    def libPEPostSampCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that LIB PE posted posterior samples
        NOT IMPLEMENTED
        """
        raise NotImplementedError

class libPESkymapCheck(esUtils.EventSupervisorTask):
    """
    a check that LIB PE posted a skymap
    """
    name = "libPESkymapCheck"
    description = "a check that LIB PE posted a skymap"

    def __init__(self, timeout, email=[]):
        super(libPESkymapCheck, self).__init__( timeout,
                                                self.libPESkymapCheck,
                                                name=self.name,
                                                descripiton=self.description,
                                                email=email
                                              )

    def libPESkymapCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that LIB PE posted a skymap
        NOT IMPLEMENTED
        """
        raise NotImplementedError

class libPEFinishCheck(esUtils.EventSupervisorTask):
    """
    a check that LIB PE finished
    """
    name = "libPEFinishCheck"
    description = "a check that LIB PE finished"

    def __init__(self, timeout, email=[]):
        super(libPEFinishCheck, self).__init__( timeout,
                                                self.libPEFinishCheck,
                                                name=self.name,
                                                descripiton=self.description,
                                                email=email
                                              )

    def libPEFinishCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that LIB PE finished
        NOT IMPLEMENTED
        """
        raise NotImplementedError

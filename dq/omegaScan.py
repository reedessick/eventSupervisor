description = "a module housing checks of OmegaScans functionality"
author = "reed.essick@ligo.org"

#---------------------------------------------------------------------------------------------------

import sys
sys.path.append("../")
import eventSupervisorUtils as esUtils

#---------------------------------------------------------------------------------------------------

class OmegaScanStartItem(esUtils.EventSupervisorQueueItem):
    """
    a check that OmegaScans were started
    """

    def __init__(self, graceid, gdb, t0, timeout, ifo, chanset="h(t)", annotate=False, email=[]):
        self.ifo = ifo
        self.chanset = chanset
        self.description = "a check that OmegaScans were started for %s at %s"%(chanset, ifo)
        tasks = [omegaScanStartCheck(timeout, ifo, chanset=chanset, email=email)]
        super(OmegaScanStartItem, self).__init__( graceid,
                                                  gdb,
                                                  t0,
                                                  tasks,
                                                  description=self.description,
                                                  annotate=annotate
                                                )

class omegaScanStartCheck(esUtils.EventSupervisorTask):
    """
    a check that OmegaScans were started
    """
    name = "omegaScanStartCheck"

    def __init__(self, timeout, ifo, chanset="h(t)", email=[]): 
        self.ifo = ifo
        self.chanset = chanset
        self.description = "a check that OmegaScans were started for %s at %s"%(chanset, ifo)
        super(omegaScanStartChec, self).__init__( timeout,
                                                  self.omegaScanStartCheck,
                                                  name=self.name,
                                                  description=self.description,
                                                  email=email
                                                )

    def omegaScanStartCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that OmegaScans were started
        NOT IMPLEMENTED
        """
        raise NotImplementedError

class OmegaScanItem(esUtils.EventSupervisorQueueItem):
    """
    a check that OmegaScans uploaded data and finished as expected
    """

    def __init__(self, graceid, gdb, t0, timeout, ifo, chanset="h(t)", annotate=False, email=[]):
        self.ifo = ifo
        self.chanset = chanset
        self.description = "a check that OmegaScans ran as expected for %s at %s"%(chanset, ifo)
        tasks = [omegaScanDataCheck(timeout, ifo, chanset=chanset, email=email),
                 omegaScanFinishCheck(timeout, ifo, chanset=chanset, email=email)
                ]
        super(OmegaScanItem, self).__init__( graceid,
                                             gdb,
                                             t0,
                                             tasks,
                                             description=self.description,
                                             annotate=annotate
                                           )

class omegaScanDataCheck(esUtils.EventSupervisorTask):
    """
    a check that OmegaScans uploaded data
    """
    name = "omegaScanDataCheck"

    def __init__(self, timeout, ifo, chanset="h(t)", email=[]):
        self.ifo = ifo
        self.chanset = chanset
        self.description = "a check that OmegaScans posted data for %s at %s"%(chanset, ifo)
        super(omegaScanDataCheck, self).__init__( timeout, 
                                                  self.omegaScanDataCheck,
                                                  name=self.name,
                                                  description=self.description,
                                                  email=email
                                                )

    def omeagScanDataCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that OmegaScans uploaded data
        NOT IMPLEMENTED
        """
        raise NotImplementedError

class omegaScansFinishCheck(esUtils.EventSupervisorTask):
    """
    a check that OmegaScans finished as expected
    """
    name = "omegaScanFinishCheck"

    def __init__(self, timeout, ifo, chanset="h(t)", email=[]):
        self.ifo = ifo
        self.chanset = chanset
        self.description = "a check that OmegaScans for %s finished at %s"%(chanset, ifo)
        super(omegaScanFinishCheck, self).__init__( timeout,
                                                    self.omegaScanFinishCheck,
                                                    name=self.name,
                                                    description=self.description,
                                                    email=email
                                                  )

    def omegaScanFinishCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that OmegaScans finished
        NOT IMPLEMENTED
        """
        raise NotImplementedError                        

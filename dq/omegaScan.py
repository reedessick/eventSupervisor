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
    name = "omega scan start"

    def __init__(self, alert, t0, options, gdb, annotate=False):
        graceid = alert['uid']

        self.ifos = options['ifos'].split()
        self.chanset = options['chanset']

        timeout = float(options['dt'])
        email = options['email'].split()

        self.description = "a check that OmegaScans were started for %s at (%s)"%(self.chanset, ",".join(self.ifos))
        tasks = [omegaScanStartCheck(timeout, ifo, chanset=chanset, email=email) for ifo in self.ifos]
        super(OmegaScanStartItem, self).__init__( graceid,
                                                  gdb,
                                                  t0,
                                                  tasks,
                                                  annotate=annotate
                                                )

class omegaScanStartCheck(esUtils.EventSupervisorTask):
    """
    a check that OmegaScans were started
    """
    name = "omegaScanStart"

    def __init__(self, timeout, ifo, chanset="h(t)", email=[]): 
        self.ifo = ifo
        self.chanset = chanset
        self.description = "a check that OmegaScans were started for %s at %s"%(chanset, ifo)
        super(omegaScanStartChec, self).__init__( timeout,
                                                  self.omegaScanStartCheck,
                                                  email=email
                                                )

    def omegaScanStartCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that OmegaScans were started
        NOT IMPLEMENTED
        """
        raise NotImplementedError(self.name)

class OmegaScanItem(esUtils.EventSupervisorQueueItem):
    """
    a check that OmegaScans uploaded data and finished as expected
    """
    name = "omega scan"

    def __init__(self, alert, t0, options, gdb, annotate=False):
        graceid = alert['uid']

        self.ifo = alert['description'].split()[-1]  ### need to parse this out of the alert!
                                                        ### this is likely to break because Alex hasn't written it yet...
        self.chanset = options['chanset']

        timeout = float(options['dt'])
        email = options['email'].split()

        self.description = "a check that OmegaScans ran as expected for %s at %s"%(self.chanset, self.ifo)
        tasks = [omegaScanDataCheck(timeout, ifo, chanset=chanset, email=email),
                 omegaScanFinishCheck(timeout, ifo, chanset=chanset, email=email)
                ]
        super(OmegaScanItem, self).__init__( graceid,
                                             gdb,
                                             t0,
                                             tasks,
                                             annotate=annotate
                                           )

class omegaScanDataCheck(esUtils.EventSupervisorTask):
    """
    a check that OmegaScans uploaded data
    """
    name = "omegaScanData"

    def __init__(self, timeout, ifo, chanset="h(t)", email=[]):
        self.ifo = ifo
        self.chanset = chanset
        self.description = "a check that OmegaScans posted data for %s at %s"%(chanset, ifo)
        super(omegaScanDataCheck, self).__init__( timeout, 
                                                  self.omegaScanDataCheck,
                                                  email=email
                                                )

    def omeagScanDataCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that OmegaScans uploaded data
        NOT IMPLEMENTED
        """
        raise NotImplementedError(self.name)

class omegaScansFinishCheck(esUtils.EventSupervisorTask):
    """
    a check that OmegaScans finished as expected
    """
    name = "omegaScanFinish"

    def __init__(self, timeout, ifo, chanset="h(t)", email=[]):
        self.ifo = ifo
        self.chanset = chanset
        self.description = "a check that OmegaScans for %s finished at %s"%(chanset, ifo)
        super(omegaScanFinishCheck, self).__init__( timeout,
                                                    self.omegaScanFinishCheck,
                                                    email=email
                                                  )

    def omegaScanFinishCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that OmegaScans finished
        NOT IMPLEMENTED
        """
        raise NotImplementedError(self.name) 

#---------------------------------------------------------------------------------------------------
'''
need to define specific classes for different chansets via inheritence
  this is because the expected behavior and timeouts could be very different for different chansets
  with the standardized __init__ architecture, we need these to be separate for things to remain sane
    we need a set of classes for each of the following chansets
      -> h(t)
      -> aux
      -> idq
'''

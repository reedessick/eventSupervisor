description = "a module housing checks of OmegaScans functionality"
author = "reed.essick@ligo.org"

#---------------------------------------------------------------------------------------------------

import sys
sys.path.append("../")
import eventSupervisorUtils as esUtils

#---------------------------------------------------------------------------------------------------

### methods to identify updates by description

def is_hoftOmegaScanStart( description ):
    ''' identify whether description is for an hoft omega scan start alert by matching a fragment. NOT IMPLEMENTED -> return False '''
    return False

def is_auxOmegaScanStart( description ):
    ''' identify whether description is for an aux omega scan start alert by matching a fragment. NOT IMPLEMENTED -> return False '''
    return False

def is_idqOmegaScanStart( description ):
    ''' identify whether description is for an idq omega scan start alert by matching a fragment. NOT IMPLEMENTED -> return False '''
    return False

#---------------------------------------------------------------------------------------------------

class OmegaScanStartItem(esUtils.EventSupervisorQueueItem):
    """
    a check that OmegaScans were started
    """
    name = "omega scan start"

    def __init__(self, alert, t0, options, gdb, annotate=False, chanset='h(t'):
        graceid = alert['uid']

        self.ifos = options['ifos'].split()

        timeout = float(options['dt'])
        email = options['email'].split()

        self.chanset = chanset

        self.description = "a check that OmegaScans were started for %s at (%s)"%(",".join(self.chanset, self.ifos))
        tasks = [omegaScanStartCheck(timeout, ifo, chanset, email=email) for ifo in self.ifos]
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

    def __init__(self, timeout, ifo, chanset, email=[]): 
        self.ifo = ifo
        self.chanset = chanset
        self.description = "a check that OmegaScans were started for %s at %s"%(chanset, ifo)
        super(omegaScanStartCheck, self).__init__( timeout,
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

    def __init__(self, alert, t0, options, gdb, annotate=False, chanset='h(t)'):
        graceid = alert['uid']

        self.ifo = alert['description'].split()[-1]  ### need to parse this out of the alert!
                                                        ### this is likely to break because Alex hasn't written it yet...
        data_dt = float(options['data dt'])
        finish_dt = float(options['finish dt'])

        email = options['email'].split()

        self.chanset = chanset

        self.description = "a check that OmegaScans ran as expected for %s at %s"%(self.chanset, self.ifo)
        tasks = [omegaScanDataCheck(data_dt, ifo, chanset, email=email),
                 omegaScanFinishCheck(finish_dt, ifo, chanset, email=email)
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

    def __init__(self, timeout, ifo, chanset, email=[]):
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

    def __init__(self, timeout, ifo, chanset, email=[]):
        self.ifo = ifo
        self.chanset = chanset
        self.description = "a check that OmegaScans finished for %s at %s"%(chanset, ifo)
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

#------------------------
# h(t)
#------------------------
class HofTOmegaScanStartItem(OmegaScanStartItem):
    """
    a check that OmegaScans were started over h(t)
    """
    name = "hoft omega scan start"
    chanset = "h(t)"

    def __init__(self, alert, t0, options, gdb, annotate=False):
        super(HofTOmegaScanStartItem, self).__init__(alert, t0, options, gdb, annotate=annotate, chanset=self.chanset)

class HofTOmegaScanItem(OmegaScanItem):
    """
    a check that OmegaScans uploaded data and finished as expected
    """
    name = "omega scan"
    chanset = "h(t)"

    def __init__(self, alert, t0, options, gdb, annotate=False):
        super(HofTOmegaScanItem, self).__init__(alert, t0, options, gdb, annotate=annotate, chanset=self.chanset)        

#------------------------
# aux
#------------------------
class AuxOmegaScanStartItem(OmegaScanStartItem):
    """
    a check that OmegaScans were started
    """
    name = "aux omega scan start"
    chanset = "aux"

    def __init__(self, alert, t0, options, gdb, annotate=False):
        super(AuxOmegaScanStartItem, self).__init__(alert, t0, options, gdb, annotate=annotate, chanset=self.chanset)

class AuxOmegaScanItem(OmegaScanItem):
    """
    a check that OmegaScans uploaded data and finished as expected
    """
    name = "omega scan"
    chanset = "aux"

    def __init__(self, alert, t0, options, gdb, annotate=False):
        super(AuxOmegaScanItem, self).__init__(alert, t0, options, gdb, annotate=annotate, chanset=self.chanset)

#------------------------
# idq
#------------------------
class IDQOmegaScanStartItem(OmegaScanStartItem):
    """
    a check that OmegaScans were started
    """
    name = "idq omega scan start"
    chanset = "idq"

    def __init__(self, alert, t0, options, gdb, annotate=False):
        super(IDQOmegaScanStartItem, self).__init__(alert, t0, options, gdb, annotate=annotate, chanset=self.chanset)

class IDQOmegaScanItem(OmegaScanItem):
    """
    a check that OmegaScans uploaded data and finished as expected
    """
    name = "idq omega scan"
    chanset = "idq"

    def __init__(self, alert, t0, options, gdb, annotate=False):
        super(IDQOmegaScanItem, self).__init__(alert, t0, options, gdb, annotate=annotate, chanset=self.chanset)

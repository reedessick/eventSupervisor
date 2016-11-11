description = "a module housing checks of OmegaScans functionality"
author      = "reed.essick@ligo.org"

#---------------------------------------------------------------------------------------------------

import eventSupervisor.eventSupervisorUtils as esUtils

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

    alert:
        graceid
    options:
        dt
        email
    args:
        chanset
        ifos
    """
    name = "omega scan start"

    def __init__(self, alert, t0, options, gdb, chanset='h(t)', ifos=[], annotate=False, warnings=False, logDir='.'):
        graceid = alert['uid']

        ### extract params
        timeout = float(options['dt'])
        email = options['email'].split()

        self.chanset = chanset
        self.ifos = ifos

        self.description = "a check that OmegaScans were started for %s at (%s)"%(self.chanset, ",".join(self.ifos))

        ### generate tasks
        tasks = [omegaScanStartCheck(timeout, ifo, chanset, email=email, logDir=logDir) for ifo in self.ifos]

        ### wrap up instantiation
        super(OmegaScanStartItem, self).__init__( graceid,
                                                  gdb,
                                                  t0,
                                                  tasks,
                                                  annotate=annotate,
                                                  warnings=warnings,
                                                )

class omegaScanStartCheck(esUtils.EventSupervisorTask):
    """
    a check that OmegaScans were started
    """
    name = "omegaScanStart"

    def __init__(self, timeout, ifo, chanset, email=[], logDir='.'): 
        self.ifo = ifo
        self.chanset = chanset
        self.description = "a check that OmegaScans were started for %s at %s"%(chanset, ifo)
        super(omegaScanStartCheck, self).__init__( timeout,
                                                  email=email,
                                                  logDir=logDir,
                                                )

    def omegaScanStart(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that OmegaScans were started
        NOT IMPLEMENTED
        """
        raise NotImplementedError(self.name)

class OmegaScanItem(esUtils.EventSupervisorQueueItem):
    """
    a check that OmegaScans uploaded data and finished as expected

    alert:
        graceid
        ifo
    options:
        data dt
        finish dt
        email
    """
    name = "omega scan"

    def __init__(self, alert, t0, options, gdb, chanset='h(t)', annotate=False, warnings=False, logDir='.'):
        graceid = alert['uid']

        self.ifo = alert['description'].split()[-1]  ### need to parse this out of the alert!
                                                        ### this is likely to break because Alex hasn't written it yet...
        data_dt = float(options['data dt'])
        finish_dt = float(options['finish dt'])

        email = options['email'].split()

        self.chanset = chanset

        self.description = "a check that OmegaScans ran as expected for %s at %s"%(self.chanset, self.ifo)
        tasks = [omegaScanDataCheck(data_dt, self.ifo, chanset, email=email, logDir=logDir),
                 omegaScanFinishCheck(finish_dt, self.ifo, chanset, email=email, logDir=logDir)
                ]
        super(OmegaScanItem, self).__init__( graceid,
                                             gdb,
                                             t0,
                                             tasks,
                                             annotate=annotate,
                                             warnings=warnings,
                                           )

class omegaScanDataCheck(esUtils.EventSupervisorTask):
    """
    a check that OmegaScans uploaded data
    """
    name = "omegaScanData"

    def __init__(self, timeout, ifo, chanset, email=[], logDir='.'):
        self.ifo = ifo
        self.chanset = chanset
        self.description = "a check that OmegaScans posted data for %s at %s"%(chanset, ifo)
        super(omegaScanDataCheck, self).__init__( timeout, 
                                                  email=email,
                                                  logDir=logDir,
                                                )

    def omegaScanData(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that OmegaScans uploaded data
        NOT IMPLEMENTED
        """
        raise NotImplementedError(self.name)

class omegaScanFinishCheck(esUtils.EventSupervisorTask):
    """
    a check that OmegaScans finished as expected
    """
    name = "omegaScanFinish"

    def __init__(self, timeout, ifo, chanset, email=[], logDir='.'):
        self.ifo = ifo
        self.chanset = chanset
        self.description = "a check that OmegaScans finished for %s at %s"%(chanset, ifo)
        super(omegaScanFinishCheck, self).__init__( timeout,
                                                    email=email,
                                                    logDir=logDir,
                                                  )

    def omegaScanFinish(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that OmegaScans finished
        NOT IMPLEMENTED
        """
        raise NotImplementedError(self.name) 

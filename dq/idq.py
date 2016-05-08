description = "a module housing checks of iDQ functionality"
author = "reed.essick@ligo.org"

#---------------------------------------------------------------------------------------------------

import sys
sys.path.append("../")
import eventSupervisorUtils as esUtils

#---------------------------------------------------------------------------------------------------

class IDQStartItem(esUtils.EventSupervisorQueueItem):
    """
    a check that iDQ started as expected
    """
    
    def __init__(self, graceid, gdb, t0, timeout, ifo, annotate=False, email=[]):
        self.ifo = ifo
        self.description = "a check that iDQ GraceDB follow-up started as expected at %s"%(self.ifo)
        tasks = [idqStartCheck(timeout, ifo, email=email)]
        super(IDQStartItem, self).__init__( graceid,
                                            gdb,
                                            t0,
                                            tasks,
                                            description=self.description,
                                            annotate=annotate
                                          )     

class idqStartCheck(esUtils.EventSupervisorTask):
    """
    a check that iDQ started as expected
    """
    name = "idqStartCheck"

    def __init__(self, timeout, ifo, email=[]):
        self.ifo = ifo
        self.description = "a check that iDQ GraceDB follow-up started as expected at %s"%(self.ifo)
        super(idqStartCheck, self).__init__( timeout,
                                             self.idqStartCheck,
                                             name=self.name,
                                             description=self.description,
                                             email=email
                                           )

    def idqStartCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that iDQ started as expected
        NOT IMPLEMENTED
        """
        raise NotImplementedError

class IDQItem(esUtils.EventSupervisorQueueItem):
    """
    a check that iDQ reported information as expected
    """

    def __init__(self, graceid, gdb, t0, timeout, ifo, annotate=False, email=[]):
        self.ifo = ifo
        description = "a check that iDQ reported information as expected at %s"%(self.ifo)
        tasks = [idqGlitchFAPCheck(timeout, ifo, email=email),
                 idqTimeseriesCheck(timeout, ifo, email=email),
                 idqTablesCheck(timeout, ifo, email=email),
                 idqPerformanceCheck(timeout, ifo, email=email),
                 idqFinishCheck(timeout, ifo, email=email)
                ]
        super(IDQItem, self).__init__( graceid,
                                       gdb,
                                       t0,
                                       tasks,
                                       description=self.description,
                                       annotate=annotate
                                     )

class idqGlichFAPCheck(esUtils.EventSupervisorTask):
    """
    a check that iDQ reported the glitch-FAP as expected
    """
    name = "idqGlitchFAPCheck"

    def __init__(self, timeout, ifo, email=[]):
        self.ifo = ifo
        self.description = "a check that iDQ reported a glitch-FAP at %s"%(self.ifo)
        super(idqGlitchFAPCheck, self).__init__( timeout,
                                                 self.idqGlitchFAPCheck,
                                                 name=self.name,
                                                 description=self.description,
                                                 email=email
                                               )

    def idqGlitchFAPCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that iDQ reported the gltich-FAP as expected
        NOT IMPLEMENTED
        """
        raise NotImplementedError 

class idqTimeseriesCheck(esUtils.EventSupervisorTask):
    """
    a check that iDQ reported timeseries information as expected
    """
    name = "idqTimeseriesCheck"

    def __init__(self, timeout, ifo, email=[]):
        self.ifo = ifo
        self.description = "a check that iDQ reproted timeseries information as expected at %s"%(self.ifo)
        super(idqTimeseriesCheck, self).__init__( timeout,
                                                  self.idqTimeseriesCheck,
                                                  name=self.name,
                                                  description=self.description,
                                                  email=email
                                                )

    def idqTimeseriesCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that iDQ reported timeseries information as expected
        NOT IMPLEMENTED
        """
        raise NotImplementedError

class idqTablesCheck(esUtils.EventSupervisorTask):
    """
    a check that iDQ reported the xml tables as expected
    """
    name = "idqTablesCheck"

    def __init__(self, timeout, ifo, email=[]):
        self.ifo = ifo
        self.description = "a check that iDQ reported the xml tables as expected at %s"%(self.ifo)
        super(idqTablesCheck, self).__init__( timeout,
                                              self.idqTablesCheck,
                                              name=self.name,
                                              description=self.description,
                                              email=email
                                            ) 

    def idqTablesCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that iDQ reported the xml tables as expected
        NOT IMPLEMENTED
        """
        raise NotImplementedError

class idqPerformanceCheck(esUtils.EventSupervisorTask):
    """
    a check that iDQ reported historical performance as expected
    """
    name = "idqPerformanceCheck"

    def __init__(self, timeout, ifo, email=[]):
        self.ifo = ifo
        self.description = "a check that iDQ reported the performance metrics as expected at %s"%(self.ifo)
        super(idqPerformanceCheck, self).__init__( timeout, 
                                                   self.idqPerformanceCheck,
                                                   name=self.name,
                                                   description=self.description,
                                                   email=email
                                                 )

    def idqPerformanceCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that iDQ reported preformance metrics as expected
        NOT IMPLEMENTED
        """
        raise NotImplementedError

class idqFinishCheck(esUtils.EventSupervisorTask):
    """
    a check that iDQ finished as expected
    """
    name = "idqFinishCheck"

    def __init__(self, timeout, ifo, email=[]):
        self.ifo = ifo
        self.description = "a check that iDQ finished reporting as expected at %s"%(self.ifo)
        super(idqFinishCheck, self).__init__( timeout,
                                              self.idqFinishCheck,
                                              name=self.name,
                                              description=self.description,
                                              email=email
                                            )

    def idqFinishCheck(self, graceid, gdb, verbose=False, annoate=False):
        """
        a check that iDQ finished as expected
        NOT IMPLEMENTED
        """
        raise NotImplementedError

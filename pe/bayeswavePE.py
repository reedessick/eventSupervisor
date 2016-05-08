description = "a module housing checks of BayesWave-PE functionality"
author = "reed.essick@ligo.org"

#---------------------------------------------------------------------------------------------------

import sys
sys.path.append("../")
import eventSupervisorUtils as esUtils

#---------------------------------------------------------------------------------------------------

class BayesWavePEStartItem(esUtils.EventSupervisorQueueItem):
    """
    a check that BayesWave PE started
    """
    description = "a check that BayesWave PE started"

    def __init__(self, graceid, gdb, t0, timeout, annotate=False, email=[]):
        tasks = [bayeswavePEStartCheck(timeout, email)]
        super(BayesWavePEStartItem, self).__init__( graceid,
                                                    gdb,
                                                    t0,
                                                    tasks,
                                                    description=self.description,
                                                    annotate=annotate
                                                  )

class bayeswavePEStartCheck(esUtils.EventSupervisorTask):
    """
    a check that LIB PE started
    """    
    name = "bayeswavePEStartCheck"
    description = "a check that BayesWave PE started"

    def __init__(self, timeout, email=[]):
        super(bayeswavePEStartCheck, self).__init__( timeout,
                                                     self.libPEStartCheck,
                                                     name=self.name,
                                                     description=self.description,
                                                     email=email
                                                   )

    def bayeswavePEStartCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that BayesWave PE started
        NOT IMPLEMENTED
        """
        raise NotImplementedError

class BayesWavePEItem(esUtils.EventSupervisorQueueItem):
    """
    a check that BayesWave PE produces the expected data and finished
    """
    description = "a check that BayesWave PE produced the expected data and finished"

    def __init__(self, graceid, gdb, t0, timeout, annotate=False, email=[]):
        tasks = [bayeswavePEPostSampCheck(timeout, email=email),
                 bayeswavePESkymapCheck(timeout, email=email),
                 bayeswavePEFinishCheck(timeout, email=email)
                ]
        super(BayesWavePEItem, self).__init__( graceid, 
                                               gdb,
                                               t0,
                                               tasks,
                                               description=self.description,
                                               annotate=annotate
                                             )

class bayeswavePEPostSampCheck(esUtils.EventSupervisorTask):
    """
    a check that BayesWave PE posted posterior samples
    """
    name = "bayeswavePEPostSampCheck"
    description = "a check that BayesWave PE posted posterior samples"

    def __init__(self, timeout, email=[]):
        super(bayeswavePEPostSampCheck, self).__init__( timeout,
                                                        self.bayeswavePEPostSampCheck,
                                                        name=self.name,
                                                        descripiton=self.description,
                                                        email=email
                                                      )

    def bayeswavePEPostSampCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that BayesWave PE posted posterior samples
        NOT IMPLEMENTED
        """
        raise NotImplementedError

class bayeswavePESkymapCheck(esUtils.EventSupervisorTask):
    """
    a check that BayesWave PE posted a skymap
    """
    name = "bayeswavePESkymapCheck"
    description = "a check that BayesWave PE posted a skymap"

    def __init__(self, timeout, email=[]):
        super(bayeswavePESkymapCheck, self).__init__( timeout,
                                                      self.bayeswavePESkymapCheck,
                                                      name=self.name,
                                                      descripiton=self.description,
                                                      email=email
                                                    )

    def bayeswavePESkymapCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that BayesWave PE posted a skymap
        NOT IMPLEMENTED
        """
        raise NotImplementedError

class bayeswavePEFinishCheck(esUtils.EventSupervisorTask):
    """
    a check that BayesWave PE finished
    """
    name = "bayeswavePEFinishCheck"
    description = "a check that BayesWave PE finished"

    def __init__(self, timeout, email=[]):
        super(bayeswavePEFinishCheck, self).__init__( timeout,
                                                      self.bayeswavePEFinishCheck,
                                                      name=self.name,
                                                      descripiton=self.description,
                                                      email=email
                                                    )

    def bayeswavePEFinishCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that BayesWave PE finished
        NOT IMPLEMENTED
        """
        raise NotImplementedError

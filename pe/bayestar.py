description = "a module housing checks of bayestar functionality"
author = "reed.essick@ligo.org"

#---------------------------------------------------------------------------------------------------

import sys
sys.path.append("../")
import eventSupervisorUtils as esUtils

#---------------------------------------------------------------------------------------------------

class BayestarStartItem(esUtils.EventSupervisorQueueItem):
    """
    a check that BayesStar started as expected
    """
    description = "a check that BAYESTAR started as expected"

    def __init__(self, graceid, gdb, t0, timeout, annotate=False, email=[]):
        tasks = [bayestarStartCheck(timeout, email=email)]
        super(BayestarStartItem, self).__item__( graceid,
                                                 gdb,
                                                 t0,
                                                 tasks,
                                                 description=self.description,
                                                 annotate=annotate
                                               )

class bayestarStartCheck(esUtils.EventSupervisorTask):
    """
    a check that bayestar started as expected
    """
    name = "bayestarStartCheck"
    description = "a check that bayestar started as expected"

    def __init__(self, timeout, email=[]):
        super(bayestarStartCheck, self).__init__( timeout,
                                                  self.bayestarStartCheck,
                                                  name=self.name,
                                                  description=self.description,
                                                  email=email
                                                )

    def bayestarStartCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that bayestar started as expected
        NOT IMPLEMENTED
        """
        raise NotImplementedError


class BayestarItem(esUtils.EventSupervisorQueueItem):
    """
    a check that Bayestar produced the expected data and finished
    """
    description = "a check that BAYESTAR produced the expected data and finished"

    def __init__(self, graceid, gdb, t0, timeout, annotate=False, email=[]):
        tasks = []
        super(BayestarItem, self).__init__( graceid,
                                            gdb,
                                            t0,
                                            tasks,
                                            description=self.description,
                                            annotate=annotate
                                          )

class bayestarSkymapCheck(esUtils.EventSupervisorTask):
    """
    a check that Bayestar produced a skymap
    """
    name = "bayestarSkymapCheck"
    description = "a check that bayestar produced a skymap"

    def __init__(self, timeout, email=[]):
        super(bayestarSkymapCheck, self).__init__( timeout, 
                                                   self.bayestarSkymapCheck,
                                                   name=self.name,
                                                   description=self.description,
                                                   email=email
                                                 )

    def bayestarSkymapCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that bayestar produced a skymap
        NOT IMPLEMENTED
        """
        raise NotImplementedError

class bayestarFinishCheck(esUtils.EventSupervisorTask):
    """
    a check that bayestar finished as expected
    """
    name = "bayestarFinishCheck"
    description = "a check that bayestar finished as expected"

    def __init__(self, timeout, email=[]):
        super(bayestarFinishCheck, self).__init__( timeout,
                                                   self.bayestarFinishCheck,
                                                   name=self.name,
                                                   description=self.description,
                                                   email=email
                                                 )

    def bayestarFinishCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that bayestar finished as expected
        NOT IMPLEMENTED
        """
        raise NotImplementedError

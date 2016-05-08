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
        """
        if verbose:
            print( "%s : %s"%(graceid, self.description) )
        if not esUtils.check4log( graceid, gdb, "INFO:BAYESTAR:starting sky localization", verbose=verbose ):
            self.warning = "found BAYESTAR staring message"
            if verbose or annotate:
                message = "no action required : "+self.warning
                if verbose:
                    print( "    "+message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )
            return False ### action_required = False

        self.warning = "could not find a BAYESTAR staring message"
        if verbose or annotate:
            message = "action required : "+self.warning
            if verbose:
                print( "    "+self.warning )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )
        return True ### action_required = True


class BayestarItem(esUtils.EventSupervisorQueueItem):
    """
    a check that Bayestar produced the expected data and finished
    """
    description = "a check that BAYESTAR produced the expected data and finished"

    def __init__(self, graceid, gdb, t0, timeout, tagnames=None, annotate=False, email=[]):
        tasks = [bayestarSkymapCheck(timeout, tagnames=tagnames, email=email),
                 bayestarFinishCheck(timeout, email=email)
                ]
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

    def __init__(self, timeout, tagnames=None, email=[]):
        self.tagnames = tagnames
        super(bayestarSkymapCheck, self).__init__( timeout, 
                                                   self.bayestarSkymapCheck,
                                                   name=self.name,
                                                   description=self.description,
                                                   email=email
                                                 )

    def bayestarSkymapCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that bayestar produced a skymap
        looks for the existence of a skymap and the correct tagnames
        """
        if verbose:
            print( "%s : %s"%(graceid, self.description) )
        fitsname = "bayestar.fits.gz"
        self.warning, action_required = check4file( graceid, gdb, fitsname, tagnames=self.tagnames, verbose=verbose )
        if verbose or annotate:
            if action_required:
                message = "action required : "+self.warning
            else:
                message = "no action required : "+self.warning
            if verbose:
                print( "    "+message )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )
        return action_required

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
        """
        if verbose:
            print( "%s : %s"%(graceid, self.description) )
        if not esUtils.check4log( graceid, gdb, "INFO:BAYESTAR:sky localization complete", verbose=verbose ):
            self.warning = "found BAYESTAR completion message"
            if verbose or annotate:
                message = "no action required : "+self.warning
                if verbose:
                    print( "    "+message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )
            return False ### action_required = False

        self.warning = "could not find a BAYESTAR completion message"
        if verbose or annotate:
            message = "action required : "+self.warning
            if verbose:
                print( "    "+self.warning )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )
        return True ### action_required = True

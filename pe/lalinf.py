description = "a module housing checks of LALInference-PE functionality"
author = "reed.essick@ligo.org"

#---------------------------------------------------------------------------------------------------

import sys
sys.path.append("../")
import eventSupervisorUtils as esUtils

#---------------------------------------------------------------------------------------------------

class LALInfStartItem(esUtils.EventSupervisorQueueItem):
    """
    a check that LALInference started
    """
    description = "a check that LALInference started"

    def __init__(self, graceid, gdb, t0, timeout, annotate=False, email=[]):
        tasks = [lalinfStartCheck(timeout, email)]
        super(LALInfStartItem, self).__init__( graceid,
                                               gdb,
                                               t0,
                                               tasks,
                                               description=self.description,
                                               annotate=annotate
                                             )

class lalinfStartCheck(esUtils.EventSupervisorTask):
    """
    a check that LALInference started
    """    
    name = "lalinfStartCheck"
    description = "a check that LALInference started"

    def __init__(self, timeout, email=[]):
        super(lalinfStartCheck, self).__init__( timeout,
                                               self.lalinfStartCheck,
                                               name=self.name,
                                               description=self.description,
                                               email=email
                                             )

    def lalinfStartCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that LALInference started
        """
        if verbose:
            print( "%s : %s"%(graceid, self.description) )
        if not esUtils.check4log( graceid, gdb, "LALInference online estimation started", verbose=verbose ):
            self.warning = "found LALInference starting message"
            if verbose or annotate:
                message = "no action required : "+self.warning
                if verbose:
                    print( "    "+message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )
            return False ### action_required = False

        self.warning = "could not find LALInference staring message"
        if verbose or annotate:
            message = "action required : "+self.warning
            if verbose:
                print( "    "+self.warning )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )
        return True ### action_required = True

class LALInfItem(esUtils.EventSupervisorQueueItem):
    """
    a check that LALInference produces the expected data and finished
    """
    description = "a check that LALInference produced the expected data and finished"

    def __init__(self, graceid, gdb, t0, timeout, tagnames=None, annotate=False, email=[]):
        tasks = [lalinfPostSampCheck(timeout, email=email),
                 lalinfSkymapCheck(timeout, tagnames=tagnames, email=email),
                 lalinfFinishCheck(timeout, email=email)
                ]
        super(LALInfItem, self).__init__( graceid, 
                                          gdb,
                                          t0,
                                          tasks,
                                          description=self.description,
                                          annotate=annotate
                                       )

class lalinfPostSampCheck(esUtils.EventSupervisorTask):
    """
    a check that LALInference posted posterior samples
    """
    name = "lalinfPostSampCheck"
    description = "a check that LALInference posted posterior samples"

    def __init__(self, timeout, email=[]):
        super(lalinfPostSampCheck, self).__init__( timeout,
                                                   self.lalinfPostSampCheck,
                                                   name=self.name,
                                                   descripiton=self.description,
                                                   email=email
                                                 )

    def lalinfPostSampCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that LALInference posted posterior samples
        NOT IMPLEMENTED
        """
        raise NotImplementedError

class lalinfSkymapCheck(esUtils.EventSupervisorTask):
    """
    a check that LALInference posted a skymap
    """
    name = "lalinfSkymapCheck"
    description = "a check that LALInference posted a skymap"

    def __init__(self, timeout, tagnames=None, email=[]):
        self.tagnames = tagnames
        super(lalinfSkymapCheck, self).__init__( timeout,
                                                 self.lalinfSkymapCheck,
                                                 name=self.name,
                                                 descripiton=self.description,
                                                 email=email
                                               )

    def lalinfSkymapCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that LALInference posted a skymap
        """
        fitsname = "LALInference_skymap.fits.gz"
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

class lalinfFinishCheck(esUtils.EventSupervisorTask):
    """
    a check that LALInference finished
    """
    name = "lalinfFinishCheck"
    description = "a check that LALInference finished"

    def __init__(self, timeout, email=[]):
        super(lalinfFinishCheck, self).__init__( timeout,
                                                 self.lalinfFinishCheck,
                                                 name=self.name,
                                                 descripiton=self.description,
                                                 email=email
                                               )

    def lalinfFinishCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that LALInference finished
        """
        if verbose:
            print( "%s : %s"%(graceid, self.description) )
        if not esUtils.check4log( graceid, gdb, "LALInference online estimation finished", verbose=verbose ):
            self.warning = "found LALInference completion message"
            if verbose or annotate:
                message = "no action required : "+self.warning
                if verbose:
                    print( "    "+message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )
            return False ### action_required = False

        self.warning = "could not find LALInference completion message"
        if verbose or annotate:
            message = "action required : "+self.warning
            if verbose:
                print( "    "+self.warning )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )
        return True ### action_required = True

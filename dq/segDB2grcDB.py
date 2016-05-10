description = "a module housing checks of segDB2GraceDB functionality"
author = "reed.essick@ligo.org"

#---------------------------------------------------------------------------------------------------

import sys
sys.path.append("../")
import eventSupervisorUtils as esUtils

#---------------------------------------------------------------------------------------------------

class SegDB2GrcDBStartItem(esUtils.EventSupervisorQueueItem):
    """
    a check that segDB2grcDB started
    """
    description = "check that segDB2grcDB started"

    def __init__(self, graceid, gdb, t0, timeout, annotate=False, email=[]):
        tasks = [segDB2grcDBStartCheck(timeout, email=email)]
        super(SegDB2grcDBStartItem, self).__init__( graceid,
                                                    gdb,
                                                    t0,
                                                    tasks,
                                                    description=self.description,
                                                    annotate=annotate
                                                  )

class segDB2grcDBStartCheck(esUtils.EventSupervisorTask):
    """
    a check that segDB2grcDB started
    """
    name = "segDB2grcDBStartCheck"
    description = "check that segDB2grcDB started"

    def __init__(self, timeout, email=[]):
        super(segDB2grcDBStartCheck, self).__init__( timeout,
                                                     self.segDB2grcDBStartCheck,
                                                     name=self.name,
                                                     description=self.description,
                                                     email=email
                                                   )

    def segDB2grcDBStartCheck(self, graceid, gdb, verbose=False, annotate=False ):
        """
        a check that segDB2grcDB started
        """
        if verbose:
            print( "%s : %s"%(graceid, self.description) )
        if not esUtils.check4log( graceid, gdb, "began searching for segments in : ", verbose=verbose ):
            self.warning = "found LIB PE starting message"
            if verbose or annotate:
                message = "no action required : "+self.warning
                if verbose:
                    print( "    "+message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )
            return False ### action_required = False

        self.warning = "could not find LIB PE staring message"
        if verbose or annotate:
            message = "action required : "+self.warning
            if verbose:
                print( "    "+self.warning )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )
        return True ### action_required = True

class SegDB2GrcDBItem(esUtils.EventSupervisorQueueItem):
    """
    a check that segDB2grcDB uploaded the expected queries and finished
    """
    description = "check that segDB2grcDB posted the expected data and finished"
    
    def __init__(self, graceid, gdb, t0, timeout, annotate=False, email=[]):
        tasks = [segDB2grcDBFlagsCheck(timeout, email=email),
                 segDB2grcDBVetoDefCheck(timeout, email=email),
                 segDB2grcDBAnyCheck(timeout, email=email),
                 segDB2grcDBFinishCheck(timeout, email=email)
                ]
        super(SegDB2GrcDBItem, self).__init__( graceid,
                                               gdb, 
                                               t0,
                                               tasks,
                                               description=self.description,
                                               annotate=annotate
                                             )

class segDB2grcDBFlagsCheck(esUtils.EventSupervisorTask):
    """
    a check that segDB2grcDB uploaded the expected individual flags
    """
    name = "segDB2grcDBFlagsCheck"
    description = "check that segDB2grcDB posted the expected individual flags"

    def __init__(self, timeout, email=[]):
        super(segDB2grcDBFlagsCheck, self).__init__( timeout,
                                                     self.segDB2grcDBFlagsCheck,
                                                     name=self.name,
                                                     description=self.description,
                                                     email=email
                                                   )

    def segDB2grcDBFlagsCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that segDB2grcDB uploaded the expected individual flags
        NOT IMPLEMENTED
        """
        raise NotImplementedError
        ### raise a warning if the query failed, too

class segDB2grcDBVetoDefCheck(esUtils.EventSupervisorTask):
    """
    a check that segDB2grcDB uploaded the expected summary of VetoDefiner queries
    """
    name = "segDB2grcDBVetoDefCheck"
    description = "check that segDB2grcDB posted the expected Veto-Definer summaries"

    def __init__(self, timeout, email=[]):
        super(segDB2grcDBVetoDefCheck, self).__init__( timeout,
                                                     self.segDB2grcDBVetoDefCheck,
                                                     name=self.name,
                                                     description=self.description,
                                                     email=email
                                                   )

    def segDB2grcDBVetoDefCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that segDB2grcDB uploaded the expected individual flags
        NOT IMPLEMENTED
        """
        raise NotImplementedError
        ### raise a warning if query failed, too

class segDB2grcDBAnyCheck(esUtils.EventSupervisorTask):
    """
    a check that segDB2grcDB uploaded the expected query of any active segments
    """
    name = "segDB2grcDBAnyCheck"
    description = "check that segDB2grcDB posted the expected summaries of all active flags"

    def __init__(self, timeout, email=[]):
        super(segDB2grcDBAnyCheck, self).__init__( timeout,
                                                     self.segDB2grcDBAnyCheck,
                                                     name=self.name,
                                                     description=self.description,
                                                     email=email
                                                   )

    def segDB2grcDBANyCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that segDB2grcDB uploaded the query for any active segments
        NOT IMPLEMENTED
        """
        raise NotImplementedError
        ### raised a warning if query failed, too

class segDB2grcDBFinishCheck(esUtils.EventSupervisorTask):
    """
    a check that segDB2grcDB finished as expected
    """
    name = "segDB2grcDBFinishCheck"
    description = "check that segDB2grcDB finished"

    def __init__(self, timeout, email=[]):
        super(segDB2grcDBFinishCheck, self).__init__( timeout,
                                                     self.segDB2grcDBFinishCheck,
                                                     name=self.name,
                                                     description=self.description,
                                                     email=email
                                                   )

    def segDB2grcDBFinishCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that segDB2grcDB finished
        """
        if verbose:
            print( "%s : %s"%(graceid, self.description) )
        if not esUtils.check4log( graceid, gdb, "finished searching for segments in : ", verbose=verbose ):
            self.warning = "found LIB PE starting message"
            if verbose or annotate:
                message = "no action required : "+self.warning
                if verbose:
                    print( "    "+message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )
            return False ### action_required = False

        self.warning = "could not find LIB PE staring message"
        if verbose or annotate:
            message = "action required : "+self.warning
            if verbose:
                print( "    "+self.warning )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )
        return True ### action_required = True

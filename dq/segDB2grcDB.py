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
    name = "segdb2grcdb start"
    description = "check that segDB2grcDB started"

    def __init__(self, alert, t0, options, gdb, annotate=False):
        graceid = alert['uid']

        timeout = float(options['dt'])
        email = options['email'].split()

        tasks = [segDB2grcDBStartCheck(timeout, email=email)]
        super(SegDB2GrcDBStartItem, self).__init__( graceid,
                                                    gdb,
                                                    t0,
                                                    tasks,
                                                    annotate=annotate
                                                  )

class segDB2grcDBStartCheck(esUtils.EventSupervisorTask):
    """
    a check that segDB2grcDB started
    """
    name = "segDB2grcDBStart"
    description = "check that segDB2grcDB started"

    def __init__(self, timeout, email=[]):
        super(segDB2grcDBStartCheck, self).__init__( timeout,
                                                     self.segDB2grcDBStartCheck,
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
    name = "segdb2grcdb"
    description = "check that segDB2grcDB posted the expected data and finished"
    
    def __init__(self, alert, t0, options, gdb, annotate=False):
        graceid = alert['uid']


        flags_dt = float(options['flags dt'])
        flags = options['flags'].split()

        veto_def_dt = float(options['veto def dt'])
        veto_defs = options['veto defs'].split()

        any_dt = float(options['any dt'])

        email = options['email'].split()

        tasks = [segDB2grcDBFlagsCheck(flags_dt, flags, email=email),
                 segDB2grcDBVetoDefCheck(veto_def_dt, veto_defs, email=email),
                 segDB2grcDBAnyCheck(any_dt, email=email),
                 segDB2grcDBFinishCheck(timeout, email=email)
                ]
        super(SegDB2GrcDBItem, self).__init__( graceid,
                                               gdb, 
                                               t0,
                                               tasks,
                                               annotate=annotate
                                             )

class segDB2grcDBFlagsCheck(esUtils.EventSupervisorTask):
    """
    a check that segDB2grcDB uploaded the expected individual flags
    """
    name = "segDB2grcDBFlags"
    description = "check that segDB2grcDB posted the expected individual flags"

    def __init__(self, timeout, flags, email=[]):
        self.flags = flags
        super(segDB2grcDBFlagsCheck, self).__init__( timeout,
                                                     self.segDB2grcDBFlagsCheck,
                                                     email=email
                                                   )

    def segDB2grcDBFlagsCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that segDB2grcDB uploaded the expected individual flags
        NOT IMPLEMENTED
        """
        raise NotImplementedError(self.name)
        ### raise a warning if the query failed, too

class segDB2grcDBVetoDefCheck(esUtils.EventSupervisorTask):
    """
    a check that segDB2grcDB uploaded the expected summary of VetoDefiner queries
    """
    name = "segDB2grcDBVetoDef"
    description = "check that segDB2grcDB posted the expected Veto-Definer summaries"

    def __init__(self, timeout, vetoDefs, email=[]):
        self.vetoDefs = vetoDefs
        super(segDB2grcDBVetoDefCheck, self).__init__( timeout,
                                                     self.segDB2grcDBVetoDefCheck,
                                                     email=email
                                                   )

    def segDB2grcDBVetoDefCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that segDB2grcDB uploaded the expected individual flags
        NOT IMPLEMENTED
        """
        raise NotImplementedError(self.name)
        ### raise a warning if query failed, too

class segDB2grcDBAnyCheck(esUtils.EventSupervisorTask):
    """
    a check that segDB2grcDB uploaded the expected query of any active segments
    """
    name = "segDB2grcDBAny"
    description = "check that segDB2grcDB posted the expected summaries of all active flags"

    def __init__(self, timeout, email=[]):
        super(segDB2grcDBAnyCheck, self).__init__( timeout,
                                                     self.segDB2grcDBAnyCheck,
                                                     email=email
                                                   )

    def segDB2grcDBANyCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that segDB2grcDB uploaded the query for any active segments
        NOT IMPLEMENTED
        """
        raise NotImplementedError(self.name)
        ### raised a warning if query failed, too

class segDB2grcDBFinishCheck(esUtils.EventSupervisorTask):
    """
    a check that segDB2grcDB finished as expected
    """
    name = "segDB2grcDBFinish"
    description = "check that segDB2grcDB finished"

    def __init__(self, timeout, email=[]):
        super(segDB2grcDBFinishCheck, self).__init__( timeout,
                                                     self.segDB2grcDBFinishCheck,
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

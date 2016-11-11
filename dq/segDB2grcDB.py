description = "a module housing checks of segDB2GraceDB functionality"
author      = "reed.essick@ligo.org"

#---------------------------------------------------------------------------------------------------

import eventSupervisor.eventSupervisorUtils as esUtils

#---------------------------------------------------------------------------------------------------

### methods to identify updates by description

def is_segdb2grcdbStart( description ):
    ''' determine whether description is for a segdb2grcdb start alert by matching a string fragment '''
    return "began searching for segments in " in description

#---------------------------------------------------------------------------------------------------

class SegDB2GrcDBStartItem(esUtils.EventSupervisorQueueItem):
    """
    a check that segDB2grcDB started

    alert:
        graceid
    options:
        dt
        email
    """
    description = "check that segDB2grcDB started"
    name        = "segdb2grcdb start"

    def __init__(self, alert, t0, options, gdb, annotate=False, warnings=False):
        graceid = alert['uid']

        ### extract params
        timeout = float(options['dt'])
        email = options['email'].split()

        ### generate tasks
        tasks = [segDB2grcDBStartCheck(timeout, email=email)]

        ### wrap up instantiation
        super(SegDB2GrcDBStartItem, self).__init__( graceid,
                                                    gdb,
                                                    t0,
                                                    tasks,
                                                    annotate=annotate,
                                                    warnings=warnings
                                                  )

class segDB2grcDBStartCheck(esUtils.EventSupervisorTask):
    """
    a check that segDB2grcDB started
    """
    description = "check that segDB2grcDB started"
    name        = "segDB2grcDBStart"

    def __init__(self, timeout, email=[]):
        super(segDB2grcDBStartCheck, self).__init__( timeout,
                                                     email=email
                                                   )

    def segDB2grcDBStart(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that segDB2grcDB started
        """
        if verbose:
            print( "%s : %s"%(graceid, self.description) )

        if not esUtils.check4log( graceid, gdb, "began searching for segments in : ", verbose=verbose ): ### check for log
            self.warning = "found segDB2grcDB starting message"
            if verbose or annotate:
                message = "no action required : "+self.warning

                ### post message
                if verbose:
                    print( "    "+message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )

            return False ### action_required = False

        self.warning = "could not find segDB2grcDB staring message"
        if verbose or annotate:
            message = "action required : "+self.warning

            ### post message
            if verbose:
                print( "    "+self.warning )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )

        return True ### action_required = True

class SegDB2GrcDBItem(esUtils.EventSupervisorQueueItem):
    """
    a check that segDB2grcDB uploaded the expected queries and finished

    alert:
        graceid
    options:
        flags dt
        flags
        veto def dt
        veto defs
        any dt
        finish dt
        email
    """
    description = "check that segDB2grcDB posted the expected data and finished"
    name        = "segdb2grcdb"
    
    def __init__(self, alert, t0, options, gdb, annotate=False, warnings=False):
        graceid = alert['uid']

        ### extract params
        flags_dt = float(options['flags dt'])
        flags = options['flags'].split()

        veto_def_dt = float(options['veto def dt'])
        veto_defs = options['veto defs'].split()

        any_dt = float(options['any dt'])

        finish_dt = float(options['finish dt'])

        email = options['email'].split()

        ### generate tasks
        tasks = []
        if flags:
            tasks.append( segDB2grcDBFlagsCheck(flags_dt, flags, email=email) )
        if veto_defs:
            tasks.append( segDB2grcDBVetoDefCheck(veto_def_dt, veto_defs, email=email) )
        tasks.append( segDB2grcDBAnyCheck(any_dt, email=email) )
        tasks.append( segDB2grcDBFinishCheck(finish_dt, email=email) )

        ### wrap up instantiation
        super(SegDB2GrcDBItem, self).__init__( graceid,
                                               gdb, 
                                               t0,
                                               tasks,
                                               annotate=annotate,
                                               warnings=warnings,
                                             )

class segDB2grcDBFlagsCheck(esUtils.EventSupervisorTask):
    """
    a check that segDB2grcDB uploaded the expected individual flags
    """
    description = "check that segDB2grcDB posted the expected individual flags"
    name        = "segDB2grcDBFlags"

    def __init__(self, timeout, flags, email=[]):
        self.flags = flags
        super(segDB2grcDBFlagsCheck, self).__init__( timeout,
                                                     email=email
                                                   )

    def segDB2grcDBFlags(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
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
    description = "check that segDB2grcDB posted the expected Veto-Definer summaries"
    name        = "segDB2grcDBVetoDef"

    def __init__(self, timeout, vetoDefs, email=[]):
        self.vetoDefs = vetoDefs
        super(segDB2grcDBVetoDefCheck, self).__init__( timeout,
                                                     email=email
                                                   )

    def segDB2grcDBVetoDef(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
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
    description = "check that segDB2grcDB posted the expected summaries of all active flags"
    name        = "segDB2grcDBAny"

    def __init__(self, timeout, email=[]):
        super(segDB2grcDBAnyCheck, self).__init__( timeout,
                                                     email=email
                                                   )

    def segDB2grcDBAny(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
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
    description = "check that segDB2grcDB finished"
    name        = "segDB2grcDBFinish"

    def __init__(self, timeout, email=[]):
        super(segDB2grcDBFinishCheck, self).__init__( timeout,
                                                      email=email
                                                    )

    def segDB2grcDBFinish(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that segDB2grcDB finished
        """
        if verbose:
            print( "%s : %s"%(graceid, self.description) )
        if not esUtils.check4log( graceid, gdb, "finished searching for segments in : ", verbose=verbose ): ### check for log
            self.warning = "found segDB2grcDB finish message"
            if verbose or annotate:
                message = "no action required : "+self.warning

                ### post Log
                if verbose:
                    print( "    "+message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )

            return False ### action_required = False

        self.warning = "could not find segDB2grcDB finish message"
        if verbose or annotate:
            message = "action required : "+self.warning

            ### post Log
            if verbose:
                print( "    "+self.warning )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )

        return True ### action_required = True

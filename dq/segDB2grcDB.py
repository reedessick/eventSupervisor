description = "a module housing checks of segDB2GraceDB functionality"
author      = "reed.essick@ligo.org"

#---------------------------------------------------------------------------------------------------

import eventSupervisor.eventSupervisorUtils as esUtils

#---------------------------------------------------------------------------------------------------

### methods to identify updates by description

def is_segDB2grcDBStart( description ):
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

    def __init__(self, alert, t0, options, gdb, annotate=False, warnings=False, logDir='.', logTag='iQ'):
        graceid = alert['uid']

        ### extract params
        timeout = float(options['dt'])
        email = options['email'].split()

        ### generate tasks
        tasks = [segDB2grcDBStartCheck(timeout, email=email, logDir=logDir, logTag='%s.%s'%(logTag, self.name))]

        ### wrap up instantiation
        super(SegDB2GrcDBStartItem, self).__init__( graceid,
                                                    gdb,
                                                    t0,
                                                    tasks,
                                                    annotate=annotate,
                                                    warnings=warnings,
                                                    logDir=logDir,
                                                    logTag=logTag,
                                                  )

class segDB2grcDBStartCheck(esUtils.EventSupervisorTask):
    """
    a check that segDB2grcDB started
    """
    description = "check that segDB2grcDB started"
    name        = "segDB2grcDBStart"

    def __init__(self, timeout, email=[], logDir='.', logTag='iQ'):
        super(segDB2grcDBStartCheck, self).__init__( timeout,
                                                     email=email,
                                                     logDir=logDir,
                                                     logTag=logTag,
                                                   )

    def segDB2grcDBStart(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that segDB2grcDB started
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag )
            logger.info( "%s : %s"%(graceid, self.description) )

        if not esUtils.check4log( graceid, gdb, "began searching for segments in : ", verbose=verbose, logTag=logger.name if verbose else None ): ### check for log
            self.warning = "found segDB2grcDB starting message"
            if verbose or annotate:
                message = "no action required : "+self.warning

                ### post message
                if verbose:
                    logger.debug( message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )

            return False ### action_required = False

        self.warning = "could not find segDB2grcDB starting message"
        if verbose or annotate:
            message = "action required : "+self.warning

            ### post message
            if verbose:
                logger.debug( message )
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
    
    def __init__(self, alert, t0, options, gdb, annotate=False, warnings=False, logDir='.', logTag='iQ'):
        graceid = alert['uid']

        ### extract params
        flags_dt = float(options['flags dt'])
        flags = options['flags'].split()

        veto_def_dt = float(options['veto def dt'])
        veto_defs = options['veto defs'].split()

        any_dt = float(options['any dt']) if options.has_key('any dt') else None

        finish_dt = float(options['finish dt'])

        email = options['email'].split()

        ### generate tasks
        taskTag = '%s.%s'%(logTag, self.name)
        tasks = []
        for flag in flags:
            tasks.append( segDB2grcDBFlagCheck(flags_dt, flag, email=email, logDir=logDir, logTag=taskTag) )
        for veto_def in veto_defs:
            raise NotImplementedError('currently cannot monitor veto definer queries')
            tasks.append( segDB2grcDBVetoDefCheck(veto_def_dt, veto_def, email=email, logDir=logDir, logTag=taskTag) )
        if any_dt!=None:
            tasks.append( segDB2grcDBAnyCheck(any_dt, email=email, logDir=logDir, logTag=taskTag) )
        tasks.append( segDB2grcDBFinishCheck(finish_dt, email=email, logDir=logDir, logTag=taskTag) )

        ### wrap up instantiation
        super(SegDB2GrcDBItem, self).__init__( graceid,
                                               gdb, 
                                               t0,
                                               tasks,
                                               annotate=annotate,
                                               warnings=warnings,
                                               logDir=logDir,
                                               logTag=logTag,
                                             )

class segDB2grcDBFlagCheck(esUtils.EventSupervisorTask):
    """
    a check that segDB2grcDB uploaded the expected individual flags
    """
    description = "check that segDB2grcDB posted the expected individual flags"
    name        = "segDB2grcDBFlag"

    def __init__(self, timeout, flag, email=[], logDir='.', logTag='iQ'):
        self.flag = flag
        super(segDB2grcDBFlagCheck, self).__init__( timeout,
                                                    email=email,
                                                    logDir=logDir,
                                                    logTag=logTag,
                                                  )

    def segDB2grcDBFlag(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that segDB2grcDB uploaded the expected individual flags by requiring xml.gz files to exist (with expected nomenclature)
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag )
            logger.info( "%s : %s"%(graceid, self.description) )

        flagname = self.flag.split(":")
        flagname = "%s-%s-(.*)-(.*).xml.gz"%(flagname[0], "_".join(_.replace("-","_") for _ in flagname[1:]))
        self.warning, action_required = esUtils.check4file( graceid,
                                                            gdb,
                                                            flagname,
                                                            regex=True,
                                                            tagnames=None,
                                                            verbose=verbose,
                                                            logFragment=None,
                                                            logRegex=False,
                                                            logTag=logger.name if verbose else None,
                                                          )
        if verbose or annotate:
            ### format message
            if action_required:
                message = "action required : "+self.warning
            else:
                message = "no action required : "+self.warning

            ### post message
            if verbose:
                logger.debug( message )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )

        return action_required

class segDB2grcDBVetoDefCheck(esUtils.EventSupervisorTask):
    """
    a check that segDB2grcDB uploaded the expected summary of VetoDefiner queries
    """
    description = "check that segDB2grcDB posted the expected Veto-Definer summaries"
    name        = "segDB2grcDBVetoDef"

    def __init__(self, timeout, vetoDef, email=[], logDir='.', logTag='iQ'):
        self.vetoDef = vetoDef
        super(segDB2grcDBVetoDefCheck, self).__init__( timeout,
                                                     email=email,
                                                     logDir=logDir,
                                                     logTag=logTag,
                                                   )

    def segDB2grcDBVetoDef(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that segDB2grcDB uploaded the expected individual flags
        NOT IMPLEMENTED
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag )
            logger.info( "%s : %s"%(graceid, self.description) )

        raise NotImplementedError(self.name)
        ### raise a warning if query failed, too

class segDB2grcDBAnyCheck(esUtils.EventSupervisorTask):
    """
    a check that segDB2grcDB uploaded the expected query of any active segments by searching for associated json file
    """
    description = "check that segDB2grcDB posted the expected summaries of all active flags"
    name        = "segDB2grcDBAny"

    def __init__(self, timeout, email=[], logDir='.', logTag='iQ'):
        super(segDB2grcDBAnyCheck, self).__init__( timeout,
                                                     email=email,
                                                     logDir=logDir,
                                                     logTag=logTag,
                                                   )

    def segDB2grcDBAny(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that segDB2grcDB uploaded the query for any active segments
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag )
            logger.info( "%s : %s"%(graceid, self.description) )

        jsonname = "allActive-(.*)-(.*).json"
        self.warning, action_required = esUtils.check4file( graceid,
                                                            gdb,
                                                            jsonname,
                                                            regex=True,
                                                            tagnames=None,
                                                            verbose=verbose,
                                                            logFragment=None,
                                                            logRegex=False,
                                                            logTag=logger.name if verbose else None,
                                                          )
        if verbose or annotate:
            ### format message
            if action_required:
                message = "action required : "+self.warning
            else:
                message = "no action required : "+self.warning

            ### post message
            if verbose:
                logger.debug( message )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )

        return action_required

class segDB2grcDBFinishCheck(esUtils.EventSupervisorTask):
    """
    a check that segDB2grcDB finished as expected
    """
    description = "check that segDB2grcDB finished"
    name        = "segDB2grcDBFinish"

    def __init__(self, timeout, email=[], logDir='.', logTag='iQ'):
        super(segDB2grcDBFinishCheck, self).__init__( timeout,
                                                      email=email,
                                                      logDir=logDir,
                                                      logTag=logTag,
                                                    )

    def segDB2grcDBFinish(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that segDB2grcDB finished
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag ) 
            logger.info( "%s : %s"%(graceid, self.description) )
        if not esUtils.check4log( graceid, gdb, "finished searching for segments in : ", verbose=verbose, logTag=logger.name if verbose else None ): ### check for log
            self.warning = "found segDB2grcDB finish message"
            if verbose or annotate:
                message = "no action required : "+self.warning

                ### post Log
                if verbose:
                    logger.debug( message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )

            return False ### action_required = False

        self.warning = "could not find segDB2grcDB finish message"
        if verbose or annotate:
            message = "action required : "+self.warning

            ### post Log
            if verbose:
                logger.debug( message )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )

        return True ### action_required = True

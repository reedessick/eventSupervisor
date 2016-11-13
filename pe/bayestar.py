description = "a module housing checks of bayestar functionality"
author      = "reed.essick@ligo.org"

#---------------------------------------------------------------------------------------------------

import eventSupervisor.eventSupervisorUtils as esUtils

#---------------------------------------------------------------------------------------------------

### methods to identify updates by description

def is_bayestarStart( description ):
    ''' identify whether description is for a bayestar start alert by matching a string fragment '''
    return "INFO:BAYESTAR:starting sky localization" in description

#---------------------------------------------------------------------------------------------------

class BayestarStartItem(esUtils.EventSupervisorQueueItem):
    """
    a check that BayesStar started as expected

    alert:
        graceid
    options:
        dt
        email
    """
    description = "a check that BAYESTAR started as expected"
    name        = "bayestar start"

    def __init__(self, alert, t0, options, gdb, annotate=False, warnings=False, logDir='.', logTag='iQ'):
        graceid = alert['uid']

        timeout = float(options['dt'])
        email = options['email'].split()

        tasks = [bayestarStartCheck(timeout, email=email, logDir=logDir, logTag='%s.%s'%(logTag, self.name))]
        super(BayestarStartItem, self).__init__( graceid,
                                                 gdb,
                                                 t0,
                                                 tasks,
                                                 annotate=annotate,
                                                 warnings=warnings,
                                                 logDir=logDir,
                                                 logTag=logTag,
                                               )

class bayestarStartCheck(esUtils.EventSupervisorTask):
    """
    a check that bayestar started as expected
    """
    description = "a check that bayestar started as expected"
    name        = "bayestarStart"

    def __init__(self, timeout, email=[], logDir='.', logTag='iQ'):
        super(bayestarStartCheck, self).__init__( timeout,
                                                  email=email,
                                                  logDir=logDir,
                                                  logTag=logTag,
                                                )

    def bayestarStart(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that bayestar started as expected
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag )
            logger.info( "%s : %s"%(graceid, self.description) )
        if not esUtils.check4log( graceid, gdb, "INFO:BAYESTAR:starting sky localization", verbose=verbose, logTag=logger.name if verbose else None ):
            self.warning = "found BAYESTAR staring message"
            if verbose or annotate:
                message = "no action required : "+self.warning
                if verbose:
                    logger.debug( "    "+message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )
            return False ### action_required = False

        self.warning = "could not find a BAYESTAR staring message"
        if verbose or annotate:
            message = "action required : "+self.warning
            if verbose:
                logger.debug( "    "+self.warning )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )
        return True ### action_required = True


class BayestarItem(esUtils.EventSupervisorQueueItem):
    """
    a check that Bayestar produced the expected data and finished

    alert:
        graceid
    options:
        skymap dt
        skymap tagnames
        finish dt
        email
    """
    description = "a check that BAYESTAR produced the expected data and finished"
    name        = "bayestar"

    def __init__(self, alert, t0, options, gdb, annotate=False, warnings=False, logDir='.', logTag='iQ'):
        graceid = alert['uid']

        skymap_dt = float(options['skymap dt'])
        skymap_tagnames = options['skymap tagnames']
        if skymap_tagnames !=None:
            skymap_tagnames = skymap_tagnames.split()
        finish_dt = float(options['finish dt'])

        email = options['email'].split()

        taskTag = '%s.%s'%(logTag, self.name)
        tasks = [bayestarSkymapCheck(skymap_dt, tagnames=skymap_tagnames, email=email, logDir=logDir, logTag=taskTag),
                 bayestarFinishCheck(finish_dt, email=email, logDir=logDir, logTag=taskTag)
                ]
        super(BayestarItem, self).__init__( graceid,
                                            gdb,
                                            t0,
                                            tasks,
                                            annotate=annotate,
                                            warnings=warnings,
                                            logDir=logDir,
                                            logTag=logTag,
                                          )

class bayestarSkymapCheck(esUtils.EventSupervisorTask):
    """
    a check that Bayestar produced a skymap
    """
    description = "a check that bayestar produced a skymap"
    name        = "bayestarSkymap"

    def __init__(self, timeout, tagnames=None, email=[], logDir='.', logTag='iQ'):
        self.tagnames = tagnames
        super(bayestarSkymapCheck, self).__init__( timeout, 
                                                   email=email,
                                                   logDir=logDir,
                                                   logTag=logTag,
                                                 )

    def bayestarSkymap(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that bayestar produced a skymap
        looks for the existence of a skymap and the correct tagnames
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag ) 
            logger.info( "%s : %s"%(graceid, self.description) )
        fitsname = "bayestar.fits.gz"
        self.warning, action_required = check4file( graceid, gdb, fitsname, tagnames=self.tagnames, verbose=verbose, logTag=logger.name if verbose else None )
        if verbose or annotate:
            if action_required:
                message = "action required : "+self.warning
            else:
                message = "no action required : "+self.warning
            if verbose:
                logger.debug( message )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )
        return action_required

class bayestarFinishCheck(esUtils.EventSupervisorTask):
    """
    a check that bayestar finished as expected
    """
    description = "a check that bayestar finished as expected"
    name        = "bayestarFinish"

    def __init__(self, timeout, email=[], logDir='.', logTag='iQ'):
        super(bayestarFinishCheck, self).__init__( timeout,
                                                   email=email,
                                                   logDir=logDir,
                                                   logTag=logTag,
                                                 )

    def bayestarFinish(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that bayestar finished as expected
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag ) 
            logger.info( "%s : %s"%(graceid, self.description) )
        if not esUtils.check4log( graceid, gdb, "INFO:BAYESTAR:sky localization complete", verbose=verbose, logTag=logger.name if verbose else None ):
            self.warning = "found BAYESTAR completion message"
            if verbose or annotate:
                message = "no action required : "+self.warning
                if verbose:
                    logger.debug( message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )
            return False ### action_required = False

        self.warning = "could not find a BAYESTAR completion message"
        if verbose or annotate:
            message = "action required : "+self.warning
            if verbose:
                logger.debug( self.warning )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )
        return True ### action_required = True

description = "a module housing checks of LALInference-PE functionality"
author      = "reed.essick@ligo.org"

#---------------------------------------------------------------------------------------------------

import eventSupervisor.eventSupervisorUtils as esUtils

#---------------------------------------------------------------------------------------------------

### methods to identify updates by description

def is_lalinfStart( description ):
    ''' determine whether description is for a lalinference start alert by matching a string fragment '''
    return 'LALInference online estimation started' in description

#---------------------------------------------------------------------------------------------------

class LALInfStartItem(esUtils.EventSupervisorQueueItem):
    """
    a check that LALInference started

    alert:
        graceid
    options:
        dt
        email
    """
    description = "a check that LALInference started"
    name        = "lalinf start"

    def __init__(self, alert, t0, options, gdb, annotate=False, warnings=False, logDir='.', logTag='iQ'):
        graceid = alert['uid']

        timeout = float(options['dt'])
        email = options['email'].split()

        tasks = [lalinfStartCheck(timeout, email, logDir=logDir, logTag='%s.%s'%(logTag, self.name))]
        super(LALInfStartItem, self).__init__( graceid,
                                               gdb,
                                               t0,
                                               tasks,
                                               annotate=annotate,
                                               warnings=warnings,
                                               logDir=logDir,
                                               logTag=logTag,
                                             )

class lalinfStartCheck(esUtils.EventSupervisorTask):
    """
    a check that LALInference started
    """    
    description = "a check that LALInference started"
    name        = "lalinfStart"

    def __init__(self, timeout, email=[], logDir='.', logTag='iQ'):
        super(lalinfStartCheck, self).__init__( timeout,
                                                email=email,
                                                logDir=logDir,
                                                logTag=logTag,
                                              )

    def lalinfStart(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that LALInference started
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag )
            logger.info( "%s : %s"%(graceid, self.description) )
        if not esUtils.check4log( graceid, gdb, "LALInference online estimation started", verbose=verbose, logTag=logger.name if verbose else None ):
            self.warning = "found LALInference starting message"
            if verbose or annotate:
                message = "no action required : "+self.warning
                if verbose:
                    logger.debug( message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )
            return False ### action_required = False

        self.warning = "could not find LALInference staring message"
        if verbose or annotate:
            message = "action required : "+self.warning
            if verbose:
                logger.debug( "    "+self.warning )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )
        return True ### action_required = True

class LALInfItem(esUtils.EventSupervisorQueueItem):
    """
    a check that LALiInference produces the expected data and finished

    alert:
        graceid
    options:
        post samp dt
        skymap dt
        skymap tagnames
        finish dt
        email
    """
    description = "a check that LALInference produced the expected data and finished"
    name        = "lalinf"

    def __init__(self, alert, t0, options, gdb, annotate=False, warnings=False, logDir='.', logTag='iQ'):
        graceid = alert['uid']

        postsamp_dt = float(options['post samp dt'])
        skymap_dt = float(options['skymap dt'])
        skymap_tagnames = options['skymap tagnames']
        if skymap_tagnames !=None:
            skymap_tagnames = skymap_tagnames.split()
        finish_dt = float(options['finish dt'])

        email = options['email'].split()

        taskTag = '%s.%s'%(logTag, self.name)
        tasks = [
                 lalinfPostSampCheck(postsamp_dt, email=email, logDir=logDir, logTag=taskTag), 
                 lalinfSkymapCheck(skymap_dt, tagnames=skymap_tagnames, email=email, logDir=logDir, logTag=taskTag),
                 lalinfFinishCheck(finish_dt, email=email, logDir=logDir, logTag=taskTag)
                ]
        super(LALInfItem, self).__init__( graceid, 
                                          gdb,
                                          t0,
                                          tasks,
                                          annotate=annotate,
                                          warnings=warnings,
                                          logDir=logDir,
                                          logTag=logTag,
                                       )

class lalinfPostSampCheck(esUtils.EventSupervisorTask):
    """
    a check that LALInference posted posterior samples
    """
    description = "a check that LALInference posted posterior samples"
    name        = "lalinfPostSamp"

    def __init__(self, timeout, email=[], logDir='.', logTag='iQ'):
        super(lalinfPostSampCheck, self).__init__( timeout,
                                                   email=email,
                                                   logDir=logDir,
                                                   logTag=logTag,
                                                 )

    def lalinfPostSamp(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that LALInference posted posterior samples
        NOT IMPLEMENTED
        """
        raise NotImplementedError("not sure what the posterior_samples filename is for lalinference follow-ups...")

        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag ) 
            logger.info( "%s : %s"%(graceid, self.description) )

        filename = "posterior_samples.dat"
        self.warning, action_required = check4file( graceid, gdb, fitsname, verbose=verbose, logTag=logger.name if verbose else None )
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


class lalinfSkymapCheck(esUtils.EventSupervisorTask):
    """
    a check that LALInference posted a skymap
    """
    description = "a check that LALInference posted a skymap"
    name        = "lalinfSkymap"

    def __init__(self, timeout, tagnames=None, email=[], logDir='.', logTag='iQ'):
        self.tagnames = tagnames
        super(lalinfSkymapCheck, self).__init__( timeout,
                                                 email=email,
                                                 logDir=logDir,
                                                 logTag=logTag,
                                               )

    def lalinfSkymap(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that LALInference posted a skymap
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag )
            logger.info( "%s : %s"%(graceid, self.description) )

        fitsname = "LALInference_skymap.fits.gz"
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

class lalinfFinishCheck(esUtils.EventSupervisorTask):
    """
    a check that LALInference finished
    """
    description = "a check that LALInference finished"
    name        = "lalinfFinish"

    def __init__(self, timeout, email=[], logDir='.', logTag='iQ'):
        super(lalinfFinishCheck, self).__init__( timeout,
                                                 email=email,
                                                 logDir=logDir,
                                                 logTag=logTag,
                                               )

    def lalinfFinish(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that LALInference finished
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag )
            logger.info( "%s : %s"%(graceid, self.description) )
        if not esUtils.check4log( graceid, gdb, "LALInference online estimation finished", verbose=verbose, logTag=logger.name if verbose else None ):
            self.warning = "found LALInference completion message"
            if verbose or annotate:
                message = "no action required : "+self.warning
                if verbose:
                    logger.debug( message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )
            return False ### action_required = False

        self.warning = "could not find LALInference completion message"
        if verbose or annotate:
            message = "action required : "+self.warning
            if verbose:
                logger.debug( self.warning )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )
        return True ### action_required = True

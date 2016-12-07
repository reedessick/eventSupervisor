description = "a module housing checks of LIB-PE functionality"
author      = "reed.essick@ligo.org"

#---------------------------------------------------------------------------------------------------

import eventSupervisor.eventSupervisorUtils as esUtils

#---------------------------------------------------------------------------------------------------

### methods to identify updates by description

def is_libPEStart( description ):
    ''' determine whether description is for a lib pe start alert by matching a string fragment '''
    return 'LIB Parameter estimation started' in description

#---------------------------------------------------------------------------------------------------

class LIBPEStartItem(esUtils.EventSupervisorQueueItem):
    """
    a check that LIB PE started

    alert:
        graceid
    options:
        dt
        email
    """
    description = "a check that LIB PE started"
    name        = "lib pe start"

    def __init__(self, alert, t0, options, gdb, annotate=False, warnings=False, logDir='.', logTag='iQ'):
        graceid = alert['uid']

        timeout = float(options['dt'])
        email = options['email'].split()

        tasks = [libPEStartCheck(timeout, email, logDir=logDir, logTag='%s.%s'%(logTag, self.name))]
        super(LIBPEStartItem, self).__init__( graceid,
                                              gdb,
                                              t0,
                                              tasks,
                                              annotate=annotate,
                                              warnings=warnings,
                                              logDir=logDir,
                                              logTag=logTag,
                                            )

class libPEStartCheck(esUtils.EventSupervisorTask):
    """
    a check that LIB PE started
    """    
    description = "a check that LIB PE started"
    name        = "libPEStart"

    def __init__(self, timeout, email=[], logDir='.', logTag='iQ'):
        super(libPEStartCheck, self).__init__( timeout,
                                               email=email,
                                               logDir=logDir,
                                               logTag=logTag,
                                             )

    def libPEStart(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that LIB PE started
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag )
            logger.info( "%s : %s"%(graceid, self.description) )
        if not esUtils.check4log( graceid, gdb, "LIB Parameter estimation started.", verbose=verbose, logTag=logger.name if verbose else None ):
            self.warning = "found LIB PE starting message"
            if verbose or annotate:
                message = "no action required : "+self.warning
                if verbose:
                    logger.debug( message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )
            return False ### action_required = False

        self.warning = "could not find LIB PE starting message"
        if verbose or annotate:
            message = "action required : "+self.warning
            if verbose:
                logger.debug( message )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )
        return True ### action_required = True


class LIBPEItem(esUtils.EventSupervisorQueueItem):
    """
    a check that LIB PE produces the expected data and finished

    alert:
        graceid
    options:
        post samp dt
        bayes factor dt
        skymap dt
        skymap tagnames
        finish dt
        email
    """
    description = "a check that LIB PE produced the expected data and finished"
    name        = "lib pe"

    def __init__(self, alert, t0, options, gdb, annotate=False, warnings=False, logDir='.', logTag='iQ'):
        graceid = alert['uid']

        postsamp_dt = float(options['post samp dt'])
        bayesFct_dt = float(options['bayes factor dt'])
        skymap_dt = float(options['skymap dt'])
        skymap_tagnames = options['skymap tagnames']
        if skymap_tagnames !=None:
            skymap_tagnames = skymap_tagnames.split()
        finish_dt = float(options['finish dt'])

        email = options['email'].split()

        taskTag = '%s.%s'%(logTag, self.name)
        tasks = [libPEPostSampCheck(postsamp_dt, email=email, logDir=logDir, logTag=logTag),
                 libPEBayesFactorsCheck(bayesFct_dt, email=email, logDir=logDir, logTag=logTag),
                 libPESkymapCheck(skymap_dt, tagnames=skymap_tagnames, email=email, logDir=logDir, logTag=logTag),
                 libPEFinishCheck(finish_dt, email=email, logDir=logDir, logTag=logTag)
                ]
        super(LIBPEItem, self).__init__( graceid, 
                                         gdb,
                                         t0,
                                         tasks,
                                         annotate=annotate,
                                         warnings=warnings,
                                         logDir=logDir,
                                         logTag=logTag,
                                       )

class libPEPostSampCheck(esUtils.EventSupervisorTask):
    """
    a check that LIB PE posted posterior samples
    """
    description = "a check that LIB PE posted posterior samples"
    name        = "libPEPostSamp"

    def __init__(self, timeout, email=[], logDir='.', logTag='iQ'):
        super(libPEPostSampCheck, self).__init__( timeout,
                                                  email=email,
                                                  logDir=logDir,
                                                  logTag=logTag,
                                                )

    def libPEPostSamp(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that LIB PE posted posterior samples
        NOTE: this is likely associated with the same log message as libPEFinishCheck 
              and it is not clear that we should seprate them as we have...
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag )
            logger.info( "%s : %s"%(graceid, self.description) )
        filename = "posterior_samples.dat"
        self.warning, action_required = esUtils.check4file( graceid, gdb, filename, verbose=verbose, logTag=logger.name if verbose else None )
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

class libPEBayesFactorsCheck(esUtils.EventSupervisorTask):
    """
    a check that LIB PE posted BayesFactors
    """
    description = "a check that LIB PE posted Bayes Factors"
    name        = "libPEBayesFactors"

    def __init__(self, timeout, email=[], logDir='.', logTag='iQ'):
        super(libPEBayesFactorsCheck, self).__init__( timeout,
                                                  email=email,
                                                  logDir=logDir,
                                                  logTag=logTag,
                                                )

    def libPEBayesFactors(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that LIB PE posted Bayes Factors
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag )
            logger.info( "%s : %s"%(graceid, self.description) )

        if not esUtils.check4log( graceid, gdb, "LIB PE summary", verbose=verbose, logTag=logger.name if verbose else None ):
            self.warning = "found LIB PE BayesFactors message"
            if verbose or annotate:
                message = "no action required : "+self.warning
                if verbose:
                    logger.debug( message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )
            return False ### action_required = False

        self.warning = "could not find LIB PE BayesFactors message"
        if verbose or annotate:
            message = "action required : "+self.warning
            if verbose:
                logger.debug( message )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )
        return True ### action_required = True


class libPESkymapCheck(esUtils.EventSupervisorTask):
    """
    a check that LIB PE posted a skymap
    """
    description = "a check that LIB PE posted a skymap"
    name        = "libPESkymap"

    def __init__(self, timeout, tagnames=None, email=[], logDir='.', logTag='iQ'):
        self.tagnames = tagnames
        super(libPESkymapCheck, self).__init__( timeout,
                                                email=email,
                                                logDir=logDir,
                                                logTag=logTag,
                                              )

    def libPESkymap(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that LIB PE posted a skymap
        looks for the existence of a skymap and the correct tagnames
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag )
            logger.info( "%s : %s"%(graceid, self.description) )
        fitsname = "LIB_skymap.fits.gz"
        self.warning, action_required = esUtils.check4file( graceid, gdb, fitsname, tagnames=self.tagnames, verbose=verbose, logTag=logger.name if verbose else None )
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

class libPEFinishCheck(esUtils.EventSupervisorTask):
    """
    a check that LIB PE finished
    """
    description = "a check that LIB PE finished"
    name        = "libPEFinish"

    def __init__(self, timeout, email=[], logDir='.', logTag='iQ'):
        super(libPEFinishCheck, self).__init__( timeout,
                                                email=email,
                                                logDir=logDir,
                                                logTag=logTag,
                                              )

    def libPEFinish(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that LIB PE finished
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag )
            logger.info( "%s : %s"%(graceid, self.description) )

        if not esUtils.check4log( graceid, gdb, "LIB Parameter estimation finished.", verbose=verbose, logTag=logger.name if verbose else None ):
            self.warning = "found LIB PE completion message"
            if verbose or annotate:
                message = "no action required : "+self.warning
                if verbose:
                    logger.debug( message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )
            return False ### action_required = False

        self.warning = "could not find LIB PE completion message"
        if verbose or annotate:
            message = "action required : "+self.warning
            if verbose:
                logger.debug( message )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )
        return True ### action_required = True

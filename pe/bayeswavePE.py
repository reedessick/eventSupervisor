description = "a module housing checks of BayesWave-PE functionality"
author      = "reed.essick@ligo.org"

#---------------------------------------------------------------------------------------------------

import eventSupervisor.eventSupervisorUtils as esUtils

#---------------------------------------------------------------------------------------------------

### methods to identify updates by description

def is_bayeswavePEStart( description ):
    ''' determine if description is for a bayeswave pe start alert by matching a string fragment '''
    return 'BayesWaveBurst launched' in description

#---------------------------------------------------------------------------------------------------
class BayesWavePEStartItem(esUtils.EventSupervisorQueueItem):
    """
    a check that BayesWave PE started

    alert:
        graceid
    options:
        dt
        email on success
        email on failure
        email on exception
    """
    description = "a check that BayesWave PE started"
    name        = "bayeswave pe start"

    def __init__(self, alert, t0, options, gdb, annotate=False, warnings=False, logDir='.', logTag='iQ'):
        graceid = alert['uid']

        timeout = float(options['dt'])

        emailOnSuccess = options['email on success'].split()
        emailOnFailure = options['email on failure'].split()
        emailOnException = options['email on exception'].split()

        tasks = [bayeswavePEStartCheck(
                     timeout, 
                     emailOnSuccess=emailOnSuccess, 
                     emailOnFailure=emailOnFailure, 
                     emailOnException=emailOnException, 
                     logDir=logDir, 
                     logTag='%s.%s'%(logTag, self.name),
                 ),
        ]

        super(BayesWavePEStartItem, self).__init__( 
            graceid,
            gdb,
            t0,
            tasks,
            annotate=annotate,
            warnings=warnings,
            logDir=logDir,
            logTag=logTag,
        )

class bayeswavePEStartCheck(esUtils.EventSupervisorTask):
    """
    a check that Bayeswave PE started
    """    
    description = "a check that BayesWave PE started"
    name        = "bayeswavePEStart"

    def bayeswavePEStart(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that BayesWave PE started
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag )
            logger.info( "%s : %s"%(graceid, self.description) )
        if not esUtils.check4log( graceid, gdb, "BayesWave launched", verbose=verbose, logTag=logger.name if verbose else None ):
            self.warning = "found BayesWave PE starting message"
            if verbose or annotate:
                message = "no action required : "+self.warning
                if verbose:
                    logger.debug( message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )
            return False ### action_required = False

        self.warning = "could not find BayesWave PE starting message"
        if verbose or annotate:
            message = "action required : "+self.warning
            if verbose:
                logger.debug( message )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )
        return True ### action_required = True


class BayesWavePEItem(esUtils.EventSupervisorQueueItem):
    """
    a check that BayesWave PE produces the expected data and finished

    alert:
        graceid
    options:
        post samp dt
        estimate dt
        bayes factor dt
        skymap dt
        skymap tagnames
        email on success
        email on failure
        email on exception
    """
    description = "a check that BayesWave PE produced the expected data and finished"
    name        = "bayeswave pe"

    def __init__(self, alert, t0, options, gdb, annotate=False, warnings=False, logDir='.', logTag='iQ'):
        graceid = alert['uid']

        postsamp_dt = float(options['post samp dt'])
        estimate_dt = float(options['estimate dt'])
        bayesFct_dt = float(options['bayes factor dt'])
        skymap_dt = float(options['skymap dt'])
        skymap_tagnames = options['skymap tagnames'].split() if options.has_key('skymap tagnames') else None

        emailOnSuccess = options['email on success'].split()
        emailOnFailure = options['email on failure'].split()
        emailOnException = options['email on exception'].split()

        taskTag = "%s.%s"%(logTag, self.name)
        tasks = [bayeswavePEPostSampCheck(
                     postsamp_dt,
                     emailOnSuccess=emailOnSuccess, 
                     emailOnFailure=emailOnFailure, 
                     emailOnException=emailOnException, 
                     logDir=logDir, 
                     logTag=taskTag,
                 ),
                 bayeswavePEEstimateCheck(
                     estimate_dt, 
                     emailOnSuccess=emailOnSuccess, 
                     emailOnFailure=emailOnFailure, 
                     emailOnException=emailOnException, 
                     logDir=logDir, 
                     logTag=taskTag,
                 ),
                 bayeswavePEBayesFactorsCheck(
                     bayesFct_dt, 
                     emailOnSuccess=emailOnSuccess, 
                     emailOnFailure=emailOnFailure, 
                     emailOnException=emailOnException, 
                     logDir=logDir, 
                     logTag=taskTag,
                 ),
                 bayeswavePESkymapCheck(
                     skymap_dt, 
                     tagnames=skymap_tagnames, 
                     emailOnSuccess=emailOnSuccess, 
                     emailOnFailure=emailOnFailure, 
                     emailOnException=emailOnException, 
                     logDir=logDir, 
                     logTag=taskTag,
                 ),
#                 bayeswavePEFinishCheck(
#                     timeout, 
#                     emailOnSuccess=emailOnSuccess, 
#                     emailOnFailure=emailOnFailure, 
#                     emailOnException=emailOnException, 
#                     logDir=logDir, 
#                     logTag=taskTag,
#                 ), ### NOT IMPLEMENTED
                ]
        super(BayesWavePEItem, self).__init__( 
            graceid, 
            gdb,
            t0,
            tasks,
            annotate=annotate,
            warnings=warnings,
            logDir=logDir,
            logTag=logTag,
        )

class bayeswavePEPostSampCheck(esUtils.EventSupervisorTask):
    """
    a check that BayesWave PE posted posterior samples
    """
    description = "a check that BayesWave PE posted posterior samples"
    name        = "bayeswavePEPostSamp"

    def bayeswavePEPostSamp(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that BayesWave PE posted posterior samples
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag ) 
            logger.info( "%s : %s"%(graceid, self.description) )

        if not esUtils.check4log( graceid, gdb, "BWB Follow-up results", verbose=verbose, logTag=logger.name if verbose else None ):
            self.warning = "found Bayeswave link to follow-up results"
            if verbose or annotate:
                message = "no action required : "+self.warning
                if verbose:
                    logger.debug( message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )
            return False ### action_required = False

        self.warning = "could not find Bayeswave link to follow-up results"
        if verbose or annotate:
            message = "action required : "+self.warning
            if verbose:
                logger.debug( message )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )
        return True ### action_required = True

class bayeswavePEBayesFactorsCheck(esUtils.EventSupervisorTask):
    """
    a check that BayesWave PE posted Bayes Factors
    """
    description = "a check that BayesWave PE posted Bayes Factors"
    name        = "bayeswavePEBayesFactors"

    def bayeswavePEBayesFactors(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that BayesWave PE posted Bayes Factors
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag )
            logger.info( "%s : %s"%(graceid, self.description) )

        if not esUtils.check4log( graceid, gdb, "BWB Bayes Factors", verbose=verbose, logTag=logger.name if verbose else None ):
            self.warning = "found Bayeswave BayesFactors message"
            if verbose or annotate:
                message = "no action required : "+self.warning
                if verbose:
                    logger.debug( message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )
            return False ### action_required = False

        self.warning = "could not find Bayeswave BayesFactors message"
        if verbose or annotate:
            message = "action required : "+self.warning
            if verbose:
                logger.debug( message )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )
        return True ### action_required = True

class bayeswavePEEstimateCheck(esUtils.EventSupervisorTask):
    """
    a check that BayesWave PE posted estimates of parameters
    """
    description = "a check that BayesWave PE posted estimates of parameters"
    name        = "bayeswavePEEstimate"

    def bayeswavePEEstimate(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that BayesWave PE posted estimates of parameters
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag )
            logger.info( "%s : %s"%(graceid, self.description) )

        if not esUtils.check4log( graceid, gdb, "BWB parameter estimation", verbose=verbose, logTag=logger.name if verbose else None ):
            self.warning = "found Bayeswave BayesFactors message"
            if verbose or annotate:
                message = "no action required : "+self.warning
                if verbose:
                    logger.debug( message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )
            return False ### action_required = False

        self.warning = "could not find Bayeswave BayesFactors message"
        if verbose or annotate:
            message = "action required : "+self.warning
            if verbose:
                logger.debug( message )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )
        return True ### action_required = True

class bayeswavePESkymapCheck(esUtils.EventSupervisorTask):
    """
    a check that BayesWave PE posted a skymap
    """
    description = "a check that BayesWave PE posted a skymap"
    name        = "bayeswavePESkymap"

    def __init__(self, timeout, tagnames=None, emailOnSuccess=[], emailOnFailure=[], emailOnException=[], logDir='.', logTag='iQ' ):
        self.tagnames = tagnames
        super(bayeswavePESkymapCheck, self).__init__( 
            timeout,
            emailOnSuccess=emailOnSuccess,
            emailOnFailure=emailOnFailure,
            emailOnException=emailOnException,
            logDir=logDir,
            logTag=logTag,
        )

    def bayeswavePESkymap(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that BayesWave PE posted a skymap
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag )
            logger.info( "%s : %s"%(graceid, self.description) )
        fitsname = "BW_skymap.fits"
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

class bayeswavePEFinishCheck(esUtils.EventSupervisorTask):
    """
    a check that BayesWave PE finished
    """
    name = "bayeswavePEFinish"
    description = "a check that BayesWave PE finished"

    def bayeswavePEFinish(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that BayesWave PE finished
        NOT IMPLEMENTED
        """
        raise NotImplementedError
        ### NOTE: bayeswave may not report a "finish" statement and instead may only report data
        ###       if this is the case, then we should NOT have a finishCheck.

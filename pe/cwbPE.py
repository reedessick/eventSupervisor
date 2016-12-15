description = "a module housing checks of cWB-PE functionality"
author      = "reed.essick@ligo.org"

#---------------------------------------------------------------------------------------------------

import eventSupervisor.eventSupervisorUtils as esUtils

#---------------------------------------------------------------------------------------------------

### methods to identify updates by description

#---------------------------------------------------------------------------------------------------

class CWBPEStartItem(esUtils.EventSupervisorQueueItem):
    """
    a check that cWB PE started

    alert:
        graceid
    options:
        dt
        email on success
        email on failure
        email on exception
    """
    description = "a check that cWB PE started"
    name        = "cwb pe start"

    def __init__(self, alert, t0, options, gdb, annotate=False, warnings=False, logDir='.', logTag='iQ'):
        graceid = alert['uid']

        timeout = float(options['dt'])

        emailOnSuccess = options['email on success'].split()
        emailOnFailure = options['email on failure'].split()
        emailOnException = options['email on exception'].split()

        tasks = [cWBPEStartCheck(
                     timeout, 
                     emailOnSuccess=emailOnSuccess,
                     emailOnFailure=emailOnFailure,
                     emailOnException=emailOnException,
                     logDir=logDir, 
                     logTag='%s.%s'%(logTag, self.name),
                 ),
        ]

        super(CWBPEStartItem, self).__init__( 
            graceid,
            gdb,
            t0,
            tasks,
            annotate=annotate,
            warnings=warnings,
            logDir=logDir,
            logTag=logTag,
        )

class cWBPEStartCheck(esUtils.EventSupervisorTask):
    """
    a check that cWB PE started
    """    
    description = "a check that cWB PE started"
    name        = "cWBPEStart"

    def cWBPEStart(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that cWB PE started
        NOT IMPLEMENTED
        """
        raise NotImplementedError(self.name)
        ### NOTE: cWB PE may not have a cannonical "start" statement and may only report data
        ###       if this is the case, then we should NOT have a startCheck.

class CWBPEItem(esUtils.EventSupervisorQueueItem):
    """
    a check that cWB PE produces the expected data and finished

    alert:
        graceid
    options:
        ced dt
        estimate dt
        skymap dt
        skymap tagnames
        email on success
        email on failure
        email on exception
    """
    description = "a check that cWB PE produced the expected data and finished"
    name        = "cwb pe"

    def __init__(self, alert, t0, options, gdb, annotate=False, warnings=False, logDir='.', logTag='iQ'):
        graceid = alert['uid']

        ced_dt = float(options['ced dt'])
        estimate_dt = float(options['estimate dt'])
        skymap_dt = float(options['skymap dt'])
        skymap_tagnames = options['skymap tagnames'].split() if options.has_key('skymap tagnames') else None

        emailOnSuccess = options['email on success'].split()
        emailOnFailure = options['email on failure'].split()
        emailOnException = options['email on exception'].split()

        taskTag = '%s.%s'%(logTag, self.name)
        tasks = [cWBPECEDCheck(
                     ced_dt, 
                     emailOnSuccess=emailOnSuccess, 
                     emailOnFailure=emailOnFailure, 
                     emailOnException=emailOnException, 
                     logDir=logDir, 
                     logTag=taskTag,
                 ),
                 cWBPEEstimateCheck(
                     estimate_dt, 
                     emailOnSuccess=emailOnSuccess, 
                     emailOnFailure=emailOnFailure, 
                     emailOnException=emailOnException, 
                     logDir=logDir, 
                     logTag=taskTag,
                 ),
                 cWBPESkymapCheck(
                     skymap_dt, 
                     tagnames=skymap_tagnames, 
                     emailOnSuccess=emailOnSuccess, 
                     emailOnFailure=emailOnFailure, 
                     emailOnException=emailOnException, 
                     logDir=logDir, 
                     logTag=taskTag,
                 ),
#                 cWBPEFinishCheck(
#                     timeout, 
#                     emailOnSuccess=emailOnSuccess, 
#                     emailOnFailure=emailOnFailure, 
#                     emailOnException=emailOnException, 
#                     logDir=logDir, 
#                     logTag=taskTag,
#                 ), ### NOT IMPLEMENTED
                ]

        super(CWBPEItem, self).__init__( 
            graceid, 
            gdb,
            t0,
            tasks,
            annotate=annotate,
            warnings=warnings,
            logDir=logDir,
            logTag=logTag,
        )

class cWBPECEDCheck(esUtils.EventSupervisorTask):
    """
    a check that cWB PE posted estimates of parameters
    """
    description = "a check that cWB PE posted a link to a CED page"
    name        = "cWBPECED"

    def cWBPECED(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that cWB PE posted posterior samples
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag )
            logger.info( "%s : %s"%(graceid, self.description) )

        if not esUtils.check4log( graceid, gdb, "cWB CED", verbose=verbose, logTag=logger.name if verbose else None ):
            self.warning = "found link to cWB CED page"
            if verbose or annotate:
                message = "no action required : "+self.warning
                if verbose:
                    logger.debug( message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )
            return False ### action_required = False

        self.warning = "could not find link to cWB CED page"
        if verbose or annotate:
            message = "action required : "+self.warning
            if verbose:
                logger.debug( message )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )
        return True ### action_required = True

class cWBPEEstimateCheck(esUtils.EventSupervisorTask):
    """
    a check that cWB PE posted estimates of parameters
    """
    description = "a check that cWB PE posted estimates of parameters"
    name        = "cWBPEEstimate"

    def cWBPEEstimate(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that cWB PE posted posterior samples
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag )
            logger.info( "%s : %s"%(graceid, self.description) )

        if not esUtils.check4log( graceid, gdb, "cWB parameter estimation", verbose=verbose, logTag=logger.name if verbose else None ):
            self.warning = "found cWB estimates of parameters"
            if verbose or annotate:
                message = "no action required : "+self.warning
                if verbose:
                    logger.debug( message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )
            return False ### action_required = False

        self.warning = "could not find cWB estimates of parameters"
        if verbose or annotate:
            message = "action required : "+self.warning
            if verbose:
                logger.debug( message )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )
        return True ### action_required = True

class cWBPESkymapCheck(esUtils.EventSupervisorTask):
    """
    a check that cWB PE posted a skymap
    """
    description = "a check that cWB PE posted a skymap"
    name        = "cWBPESkymap"

    def __init__(self, timeout, tagnames=None, emailOnSuccess=[], emailOnFailure=[], emailOnException=[], logDir='.', logTag='iQ'):
        self.tagnames = tagnames
        super(cWBPESkymapCheck, self).__init__( 
            timeout,
            emailOnSuccess=emailOnSuccess,
            emailOnFailure=emailOnFailure,
            emailOnException=emailOnException,
            logDir=logDir,
            logTag=logTag,
        )

    def cWBPESkymap(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that cWB PE posted a skymap
        looks for the existence of a skymap and the correct tagnames
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag )
            logger.info( "%s : %s"%(graceid, self.description) )
        fitsname = "skyprobcc_cWB.fits"
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

class cWBPEFinishCheck(esUtils.EventSupervisorTask):
    """
    a check that cWB PE finished
    """
    description = "a check that cWB PE finished"
    name        = "cWBPEFinish"

    def cWBPEFinish(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that cWB PE finished
        NOT IMPLEMENTED
        """
        raise NotImplementedError(self.name)
        ### NOTE: cWB PE may not have a cannonical "finish" statement and may only report data
        ###       if this is the case, then we should NOT have a finishCheck.

description = "a module housing checks of EM bright classification functionality"
author      = "reed.essick@ligo.org"

#---------------------------------------------------------------------------------------------------

import eventSupervisor.eventSupervisorUtils as esUtils

#---------------------------------------------------------------------------------------------------

### methods to identify updates by description
### not needed

#---------------------------------------------------------------------------------------------------

class EMBrightItem(esUtils.EventSupervisorQueueItem):
    """
    a check that EM bright classifier posted a result

    alert:
        graceid
    options:
        dt
        email on success
        email on failure
        email on exception
    """
    description = "a check that EM bright classifer posted a result"
    name        = "em bright"

    def __init__(self, alert, t0, options, gdb, annotate=False, warnings=False, logDir='.', logTag='iQ'):
        graceid = alert['uid']

        timeout = float(options['dt'])

        emailOnSuccess = options['email on success'].split()
        emailOnFailure = options['email on failure'].split()
        emailOnException = options['email on exception'].split()

        tasks = [emBrightCheck(
                     timeout, 
                     emailOnSuccess=emailOnSuccess, 
                     emailOnFailure=emailOnFailure, 
                     emailOnException=emailOnException, 
                     logDir=logDir, 
                     logTag='%s.%s'%(logTag, self.name),
                 ),
        ]
        super(EMBrightItem, self).__init__( graceid,
                                              gdb,
                                              t0,
                                              tasks,
                                              annotate=annotate,
                                              warnings=warnings,
                                              logDir=logDir,
                                              logTag=logTag,
                                            )

class emBrightCheck(esUtils.EventSupervisorTask):
    """
    a check that EM bright classifier posted a result
    """    
    description = "a check that EM bright classifier posted a result"
    name        = "emBright"

    def emBright(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that emBright posted a result

        WARNING: currently only check for a file and do not check for log message or tags
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag )
            logger.info( "%s : %s"%(graceid, self.description) )

        jsonname = "Source_Classification_%s.json"%(graceid) ### NOTE: this may be fragile
        self.warning, action_required = esUtils.check4file( 
                                            graceid,
                                            gdb,
                                            jsonname,
                                            regex=False,
                                            tagnames=None,
                                            verbose=verbose,
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

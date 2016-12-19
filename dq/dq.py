description = "a module housing checks of DQ summary page functionality"
author      = "reed.essick@ligo.org"

#---------------------------------------------------------------------------------------------------

import eventSupervisor.eventSupervisorUtils as esUtils

#---------------------------------------------------------------------------------------------------

### methods to identify updates by description

#---------------------------------------------------------------------------------------------------

class LLDQReportItem(esUtils.EventSupervisorQueueItem):
    """
    a check that a link to the DQ Summary page was posted

    read from alert:

        - graceid

    read from options:

        - dt
        - email on success
        - email on failure
        - email on exception

    creates Task:

        - :func:`lldqReportCheck`
    """
    description = "a check that the lldq-report page was posted"
    name        = "lldqReport"

    def __init__(self, alert, t0, options, gdb, annotate=False, warnings=False, logDir='.', logTag='iQ'):
        graceid = alert['uid']

        ### extract params
        timeout = float(options['dt'])

        emailOnSuccess = options['email on success'].split()
        emailOnFailure = options['email on failure'].split()
        emailOnException = options['email on exception'].split()

        ### generate tasks
        tasks = [lldqReportCheck(
                     timeout, 
                     emailOnSuccess=emailOnSuccess, 
                     emailOnFailure=emailOnFailure, 
                     emailOnException=emailOnException, 
                     logDir=logDir, 
                     logTag='%s.%s'%(logTag, self.name),
                 ),
        ]

        ### wrap up instantiation
        super(LLDQReportItem, self).__init__( graceid,
                                             gdb,
                                             t0,
                                             tasks,
                                             annotate=annotate,
                                             warnings=warnings,
                                             logDir=logDir,
                                             logTag=logTag,
                                           )

class lldqReportCheck(esUtils.EventSupervisorTask):
    """
    a check that a link to the DQ Summary page was posted.
    Looks for a log comment while ignoring tagnames and files.

    created by:

        - :func:`LLDQReportItem`
    """
    description = "a check that the lldq-report page was posted"
    name        = "lldqReport"

    def lldqReport(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that a link to the lldq-report page was posted.
        looks for a log comment while ignoring tagnames and files
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag )
            logger.info( "%s : %s"%(graceid, self.description) )
        if not esUtils.check4log( graceid, gdb, "Automatic Data-quality report posted",  verbose=verbose, logTag=logger.name if verbose else None ):
            self.warning = "found lldq-report post"
            if verbose or annotate:
                message = "no action required : "+self.warning
                if verbose:
                    logger.debug( message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )
            return False ### action_required = False

        self.warning = "could not find a lldq-report post"
        if verbose or annotate:
            message = "action required : "+self.warning
            if verbose:
                logger.debug( message )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )
        return True ### action_required = True

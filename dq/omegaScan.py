description = "a module housing checks of OmegaScans functionality"
author      = "reed.essick@ligo.org"

#---------------------------------------------------------------------------------------------------

import eventSupervisor.eventSupervisorUtils as esUtils

#---------------------------------------------------------------------------------------------------

### methods to identify updates by description

def is_l1OmegaScanStart( description ):
    ''' identify whether description is for an l1 omega scan start alert by matching a fragment. NOT IMPLEMENTED -> return False '''
    raise NotImplementedError('is_l1OmegaScanStart')
    return False ### need to predict the chansets associated with this, meaning we need another input argument!

def is_h1OmegaScanStart( description ):
    ''' identify whether description is for an h1 omega scan start alert by matching a fragment. NOT IMPLEMENTED -> return False '''
    raise NotImplementedError('is_h1OmegaScanStart')
    return False ### need to predict the chansets associated with this, meaning we need another input argument!

#def is_idqOmegaScanStart( description ):
#    ''' identify whether description is for an idq omega scan start alert by matching a fragment. NOT IMPLEMENTED -> return False '''
#    return False

#---------------------------------------------------------------------------------------------------

class OmegaScanStartItem(esUtils.EventSupervisorQueueItem):
    """
    a check that OmegaScans were started

    alert:
        graceid
    options:
        dt
        email
    args:
        chansets
    """
    name = "omega scan start"

    def __init__(self, alert, t0, options, gdb, annotate=False, warnings=False, logDir='.', logTag='iQ'):
        graceid = alert['uid']

        ### extract params
        timeout = float(options['dt'])
        email = options['email'].split()

        self.chansets = options['chansets'].split()

        self.description = "a check that OmegaScans were started for %s"%(", ".join(self.chansets))

        ### generate tasks
        tasks = [omegaScanStartCheck(timeout, self.chansets, email=email, logDir=logDir, logTag='%s.%s'%(logTag, self.name))]

        ### wrap up instantiation
        super(OmegaScanStartItem, self).__init__( graceid,
                                                  gdb,
                                                  t0,
                                                  tasks,
                                                  annotate=annotate,
                                                  warnings=warnings,
                                                  logDir=logDir,
                                                  logTag=logTag,
                                                )

class omegaScanStartCheck(esUtils.EventSupervisorTask):
    """
    a check that OmegaScans were started
    """
    name = "omegaScanStart"

    def __init__(self, timeout, chansets, email=[], logDir='.', logTag='iQ'): 
        self.chansets = chansets
        self.description = "a check that OmegaScans were started for %s"%(", ".join(chansets))
        super(omegaScanStartCheck, self).__init__( timeout,
                                                  email=email,
                                                  logDir=logDir,
                                                  logTag=logTag,
                                                )

    def omegaScanStart(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that OmegaScans were started
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag )
            logger.info( "%s : %s"%(graceid, self.description) )
    
        fragment = "automatic OmegaScans begun for: %s"%(", ".join(self.chansets))
        if not check4log( graceid, gdb, fragment, tagnames=None, regex=False, verbose=verbose, logTag=logger.name if verbose else None ):
            self.warning = "found OmegaScan start message for %s"%(", ".join(self.chansets))
            if verbose or annotate:
                message = "no action required : "+self.warning
       
                ### post message
                if verbose:
                    logger.debug( "    "+message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )

            return False ### action_required = False

        self.warning = "could not find OmegaScan start message for %s"%(", ".join(self.chanests))
        if verbose or annotate:
            message = "action required : "+self.warning

            ### post message
            if verbose:
                logger.debug( "    "+self.warning )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )

        return True ### action_required = True

class OmegaScanItem(esUtils.EventSupervisorQueueItem):
    """
    a check that OmegaScans uploaded data and finished as expected

    alert:
        graceid
    options:
        data dt
        finish dt
        email
    """
    name = "omega scan"

    def __init__(self, alert, t0, options, gdb, annotate=False, warnings=False, logDir='.', logTag='iQ'):
        graceid = alert['uid']

        data_dt = float(options['data dt'])
        finish_dt = float(options['finish dt'])

        email = options['email'].split()

        self.chansets = options['chansets'].split()

        self.description = "a check that OmegaScans ran as expected for %s"%(", ".join(self.chansets))

        taskTag = '%s.%s'%(logTag, self.name)
        tasks = []
        for chanset in self.chansets:
            tasks.append( omegaScanDataCheck(data_dt, chanset, email=email, logDir=logDir, logTag=taskTag) )
        tasks.append( omegaScanFinishCheck(finish_dt, self.chansets, email=email, logDir=logDir, logTag=taskTag) )

        super(OmegaScanItem, self).__init__( graceid,
                                             gdb,
                                             t0,
                                             tasks,
                                             annotate=annotate,
                                             warnings=warnings,
                                             logDir=logDir,
                                             logTag=logTag,
                                           )

class omegaScanDataCheck(esUtils.EventSupervisorTask):
    """
    a check that OmegaScans uploaded data
    """
    name = "omegaScanData"

    def __init__(self, timeout, chanset, email=[], logDir='.', logTag='iQ'):
        self.chanset = chanset
        self.description = "a check that OmegaScans posted data for %s"%(chanset)
        super(omegaScanDataCheck, self).__init__( timeout, 
                                                  email=email,
                                                  logDir=logDir,
                                                  logTag=logTag,
                                                )

    def omegaScanData(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that OmegaScans uploaded data
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag )
            logger.info( "%s : %s"%(graceid, self.description) )

        jsonname = "%s.json"%chanset
        self.warning, action_required = check4file( graceid,
                                                    gdb,
                                                    jsonname,
                                                    regex=False,
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

class omegaScanFinishCheck(esUtils.EventSupervisorTask):
    """
    a check that OmegaScans finished as expected
    """
    name = "omegaScanFinish"

    def __init__(self, timeout, chansets, email=[], logDir='.', logTag='iQ'):
        self.chansets = chansets
        self.description = "a check that OmegaScans finished for %s"%(chansets)
        super(omegaScanFinishCheck, self).__init__( timeout,
                                                    email=email,
                                                    logDir=logDir,
                                                    logTag=logTag,
                                                  )

    def omegaScanFinish(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that OmegaScans finished
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag )
            logger.info( "%s : %s"%(graceid, self.description) )

        fragment = "automatic OmegaScans finished for: %s"%(", ".join(self.chansets))
        if not check4log( graceid, gdb, fragment, tagnames=None, regex=False, verbose=verbose, logTag=logger.name if verbose else None ):
            self.warning = "found OmegaScan start message for %s"%(", ".join(self.chansets))
            if verbose or annotate:
                message = "no action required : "+self.warning

                ### post message
                if verbose:
                    logger.debug( "    "+message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )

            return False ### action_required = False

        self.warning = "could not find OmegaScan finished message for %s"%(", ".join(self.chanests))
        if verbose or annotate:
            message = "action required : "+self.warning

            ### post message
            if verbose:
                logger.debug( "    "+self.warning )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )

        return True ### action_required = True

#---------------------------------------------------------------------------------------------------

class L1OmegaScanStartItem(OmegaScanStartItem):
    """
    child of OmegaScanStartItem that specifically looks for the L1 process
    this declaration is necessary for automated look-up within config file
    """
    name = "l1 omega scan start"

class L1OmegaScanItem(OmegaScanItem):
    """
    child of OmegaScanItem that specifically looks for the L1 process
    this declaration is necessary for automated look-up within config file
    """
    name = "l1 omega scan"
    
class H1OmegaScanStartItem(OmegaScanStartItem):
    """
    child of OmegaScanStartItem that specifically looks for the H1 process
    this declaration is necessary for automated look-up within config file
    """
    name = "h1 omega scan start"

class H1OmegaScanItem(OmegaScanItem):
    """
    child of OmegaScanItem that specifically looks for the H1 process
    this declaration is necessary for automated look-up within config file
    """
    name = "h1 omega scan start"

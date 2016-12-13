description = "a module housing checks of skymap summary functionality"
author      = "reed.essick@ligo.org"

#---------------------------------------------------------------------------------------------------

import re

import eventSupervisor.eventSupervisorUtils as esUtils

#---------------------------------------------------------------------------------------------------

### methods to identify updates by description

def is_snglFITSStart( description ):
    ''' determine whether description is for a snglFITS start alert by matching a string fragment.'''
    return "started skymap summary for" in description

def is_snglFITSFinish( description ):
    ''' determine whether description is for a snglFITS finish alert by matching a string fragment.'''
    return "finished skymap summary for" in description

def is_multFITSStart( description ):
    ''' determine whether description is for multFITS start alert by matching a string fragment.'''
    return "started skymap comparison for" in description

#---------------------------------------------------------------------------------------------------

#-------------------------------------------------
# skymap autosummary
#-------------------------------------------------

class SnglFITSStartItem(esUtils.EventSupervisorQueueItem):
    """
    a check that snglFITS started as expected

    alert:
        graceid
        fitsname
    options:
        dt
        email on success
        email on failure
        email on exception
    """
    name = "snglFITS start"

    def __init__(self, alert, t0, options, gdb, annotate=False, warnings=False, logDir='.', logTag='iQ'):
        graceid = alert['uid']
        self.fitsname = alert['file']
#        self.tagnames = alert['object']['tag_names'] ### how can we propagate these into future items without querying?
        self.tagnames = [] ### FIXME: just ignore these for now

        self.description = "check that snglFITS started processing %s"%self.fitsname

        ### extract params from config
        timeout = float(options['dt'])

        emailOnSuccess = options['email on success'].split()
        emailOnFailure = options['email on failure'].split()
        emailOnException = options['email on exception'].split()

        ### generate tasks
        tasks = [snglFITSStartCheck(
                     timeout, 
                     self.fitsname, 
                     tagnames=self.tagnames, 
                     emailOnSuccess=emailOnSuccess, 
                     emailOnFailure=emailOnFailure, 
                     emailOnException=emailOnException, 
                     logDir=logDir, 
                     logTag='%s.%s'%(logTag, self.name),
                 ),
        ]

        ### wrap up instantiation
        super(SnglFITSStartItem, self).__init__( 
            graceid,
            gdb,
            t0,
            tasks,
            annotate=annotate,
            warnings=warnings,
            logDir=logDir,
            logTag=logTag,
        )

class snglFITSStartCheck(esUtils.EventSupervisorTask):
    """
    a check that snglFITS started as expected
    """
    name = "snglFITSStart"

    def __init__(self, timeout, fitsname, tagnames=[], emailOnSuccess=[], emailOnFailure=[], emailOnException=[], logDir='.', logTag='iQ'):
        self.fitsname = fitsname
        self.tagnames = tagnames ### currently ignored...
        self.description = "check that snglFITS started processing %s"%fitsname
        super(snglFITSStartCheck, self).__init__( 
            timeout,
            emailOnSuccess=emailOnSuccess,
            emailOnFailure=emailOnFailure,
            emailOnException=emailOnException,
            logDir=logDir,
            logTag=logTag,
        )

    def snglFITSStart(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that snglFITS started as expected
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag )
            logger.info( "%s : %s"%(graceid, self.description) )

        if not esUtils.check4log( graceid, gdb, "started skymap summary for .*%s.*"%self.fitsname, regex=True, verbose=verbose, logTag=logger.name if verbose else None ):
            self.warning = "found snglFITS start message for %s"%self.fitsname
            if verbose or annotate:
                message = "no action required : "+self.warning
                if verbose:
                    logger.debug( "    "+message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )
            return False ### action_required = False

        self.warning = "could not find snglFITS start message for %s"%self.fitsname
        if verbose or annotate:
            message = "action required : "+self.warning
            if verbose:
                logger.debug( "    "+message )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )
        return True ### action_required = True

class SnglFITSItem(esUtils.EventSupervisorQueueItem):
    """
    a check that snglFITS ran as expected

    alert:
        graceid
        fitsname
    options:
        html dt
        finish dt
        email on success
        email on failure
        email on exception
    """
    name = "snglFITS"

    def __init__(self, alert, t0, options, gdb, annotate=False, warnings=False, logDir='.', logTag='iQ'):
        graceid = alert['uid']

        self.fitsname = alert['description'].strip('</a>').split('>')[-1] ### parse filename out of <a> html tag
#        self.tagnames = alert['object']['tag_names'] ### this extracts the tags of the "snglFITS start" log message, not the fits file...
        self.tagnames = [] ### FIXME: just ignore these for now

        self.description = "check that snglFITS processed %s"%self.fitsname

        ### extract params from config
        html_dt   = float(options['html dt'])
        finish_dt = float(options['finish dt'])

        emailOnSuccess = options['email on success'].split()
        emailOnFailure = options['email on failure'].split()
        emailOnException = options['email on exception'].split()

        ### generate tasks
        taskTag = '%s.%s'%(logTag, self.name)
        tasks = [snglFITShtmlCheck(
                     html_dt, 
                     self.fitsname, 
                     tagnames=self.tagnames, 
                     emailOnSuccess=emailOnSuccess, 
                     emailOnFailure=emailOnFailure, 
                     emailOnException=emailOnException, 
                     logDir=logDir, 
                     logTag=taskTag,
                 ),
                 snglFITSFinishCheck(
                     finish_dt, 
                     self.fitsname, 
                     tagnames=self.tagnames, 
                     emailOnSuccess=emailOnSuccess, 
                     emailOnFailure=emailOnFailure, 
                     emailOnException=emailOnException, 
                     logDir=logDir, 
                     logTag=taskTag,
                 ),
        ]

        ### wrap up instantiation
        super(SnglFITSItem, self).__init__( 
            graceid,
            gdb,
            t0,
            tasks,
            annotate=annotate,
            warnings=warnings,
            logDir=logDir,
            logTag=logTag,
        )

class snglFITShtmlCheck(esUtils.EventSupervisorTask):
    """
    a check that snglFITS posted an hmtl as expected
    """
    name = "snglFITShtml"

    def __init__(self, timeout, fitsname, tagnames=[], emailOnSuccess=[], emailOnFailure=[], emailOnException=[], logDir='.', logTag='iQ'):
        self.fitsname = fitsname
        self.tagnames = tagnames ### currently ignored
        self.description = "check that snglFITS posted an html for %s"%fitsname
        super(snglFITShtmlCheck, self).__init__( 
            timeout,
            emailOnSuccess=emailOnSuccess,
            emailOnFailure=emailOnFailure,
            emailOnException=emailOnException,
            logDir=logDir,
            logTag=logTag,
        )

    def snglFITShtml(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that snglFITS posted an html as expected
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag )
            logger.info( "%s : %s"%(graceid, self.description) )

        htmlname = "%s-skymapSummary.html"%(self.fitsname.split('.fits')[0]) ### NOTE: this may be fragile
        fragment = "skymap summary for .*%s.*can be found.*here.*"%(self.fitsname) ### NOTE: this may be fragile

        self.warning, action_required = esUtils.check4file( 
                                            graceid,
                                            gdb,
                                            htmlname,
                                            regex=False,
                                            tagnames=None,
                                            verbose=verbose,
                                            logFragment=fragment,
                                            logRegex=True,
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

class snglFITSFinishCheck(esUtils.EventSupervisorTask):
    """
    a check that snglFITS finished as expected
    """
    name = "snglFITSFinish"

    def __init__(self, timeout, fitsname, tagnames=[], emailOnSuccess=[], emailOnFailure=[], emailOnException=[], logDir='.', logTag='iQ'):
        self.fitsname = fitsname
        self.tagnames = tagnames ### currently ignored
        self.description = "check that snglFITS finished processing %s"%fitsname
        super(snglFITSFinishCheck, self).__init__( 
            timeout,
            emailOnSuccess=emailOnSuccess,
            emailOnFailure=emailOnFailure,
            emailOnException=emailOnException,
            logDir=logDir,
            logTag=logTag,
        )

    def snglFITSFinish(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that snglFITS finished as expected
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag )
            logger.info( "%s : %s"%(graceid, self.description) )

        if not esUtils.check4log( graceid, gdb, "finished skymap summary for .*%s.*"%self.fitsname, regex=True, verbose=verbose, logTag=logger.name if verbose else None ):
            self.warning = "found snglFITS finish message for %s"%self.fitsname
            if verbose or annotate:
                message = "no action required : "+self.warning
                if verbose:
                    logger.debug( "    "+message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )
            return False ### action_required = False

        self.warning = "could not find snglFITS finish message for %s"%self.fitsname
        if verbose or annotate:
            message = "action required : "+self.warning
            if verbose:
                logger.debug( "    "+message )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )
        return True ### action_required = True

#------------------------

class MultFITSStartItem(esUtils.EventSupervisorQueueItem):
    """
    a check that multFITS started as expected

    alert:
        graceid
    GraceDb:
        fitsnames
    options:
        dt
        email on success
        email on failure
        email on exception
    """
    name = "multFITS start"

    def __init__(self, alert, t0, options, gdb, annotate=False, warnings=False, logDir='.', logTag='iQ'):
        graceid = alert['uid']

        ### query GraceDb to get all fits files for this event
        self.fitsnames = [fits for fits in gdb.files( graceid ).json().keys() if fits.endswith('.fits') or fits.endswith('.fits.gz')] ### FIXME: subject to a race condition (another FITS is added between this query and when alert2html.py was launched

#        self.tagnames = alert['object']['tag_names'] ### these are the tags of the snglFITS finish message, not the fits file
        self.tagnames = [] ### FIXME: ignore these for now

        self.description = "check that multFITS started for %s"%(', '.join(self.fitsnames))

        ### extract params from config
        timeout = float(options['dt'])

        emailOnSuccess = options['email on success'].split()
        emailOnFailure = options['email on failure'].split()
        emailOnException = options['email on exception'].split()

        ### generate tasks
        tasks = [multFITSStartCheck(
                     timeout, 
                     self.fitsnames, 
                     tagnames=self.tagnames, 
                     emailOnSuccess=emailOnSuccess, 
                     emailOnFailure=emailOnFailure, 
                     emailOnException=emailOnException, 
                     logDir=logDir, 
                     logTag='%s.%s'%(logTag, self.name),
                 ),
        ]

        ### wrap up instantiation
        super(MultFITSStartItem, self).__init__( 
            graceid,
            gdb,
            t0,
            tasks,
            annotate=annotate,
            warnings=warnings,
            logDir=logDir,
            logTag=logTag,
        )

class multFITSStartCheck(esUtils.EventSupervisorTask):
    """
    a check that multFITS started as expected
    """
    name = "multFITSStart"

    def __init__(self, timeout, fitsnames, tagnames=[], emailOnSuccess=[], emailOnFailure=[], emailOnException=[], logDir='.', logTag='iQ'):
        self.fitsnames = fitsnames
        self.tagnames = tagnames ### currently ignored
        self.description = "check that multFITS started processing %s"%(", ".join(fitsnames))
        super(multFITSStartCheck, self).__init__( 
            timeout,
            emailOnSuccess=emailOnSuccess,
            emailOnFailure=emailOnFailure,
            emailOnException=emailOnException,
            logDir=logDir,
            logTag=logTag,
        )

    def multFITSStart(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that multFITS started as expected
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag )
            logger.info( "%s : %s"%(graceid, self.description) )

        if not esUtils.check4log( graceid, gdb, "started skymap comparison for .*%s.*"%(".*".join(self.fitsnames)), regex=True, verbose=verbose, logTag=logger.name if verbose else None ):
            self.warning = "found multFITS start message for %s"%(", ".join(self.fitsnames))
            if verbose or annotate:
                message = "no action required : "+self.warning
                if verbose:
                    logger.debug( "    "+message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )
            return False ### action_required = False

        self.warning = "could not find multFITS start message for %s"%(", ".join(self.fitsname))
        if verbose or annotate:
            message = "action required : "+self.warning
            if verbose:
                logger.debug( "    "+message )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )
        return True ### action_required = True

class MultFITSItem(esUtils.EventSupervisorQueueItem):
    """
    a check that multFITS ran as expected

    alert:
        graceid
        fitsnames
    options:
        html dt
        finish dt
        email on success
        email on failure
        email on exception
    """
    name = "multFITS"

    def __init__(self, alert, t0, options, gdb, annotate=False, warnings=False, logDir='.', logTag='iQ'):
        graceid = alert['uid']

        ### extrct fitsnames from log comment
        ### this is a bit complicated, and may be fragile
        self.fitsnames = []
        expr = re.compile( '(.*.fits.gz|.*.fits)' )
        for fragment in alert['description'].split(','):
            self.fitsnames.append( expr.match( fragment ).group().split('>')[-1] ) ### NOTE: may be fragile!

#        self.tagnames = alert['object']['tag_names'] ### these are the tags of the multFITS start message, not the FITS files
        self.tagnames = [] ### FIXME: ignore tags for now

        self.description = "check that multFITS processed %s"%(", ".join(self.fitsnames))

        ### extract params from config
        html_dt   = float(options['html dt'])
        finish_dt = float(options['finish dt'])

        emailOnSuccess = options['email on success'].split()
        emailOnFailure = options['email on failure'].split()
        emailOnException = options['email on exception'].split()

        ### generate tasks
        taskTag = '%s.%s'%(logTag, self.name)
        tasks = [multFITShtmlCheck(
                     html_dt, 
                     tagnames=self.tagnames, 
                     emailOnSuccess=emailOnSuccess, 
                     emailOnFailure=emailOnFailure, 
                     emailOnException=emailOnException, 
                     logDir=logDir, 
                     logTag=taskTag,
                 ),
                 multFITSFinishCheck(
                     finish_dt, 
                     self.fitsnames, 
                     tagnames=self.tagnames, 
                     emailOnSuccess=emailOnSuccess, 
                     emailOnFailure=emailOnFailure, 
                     emailOnException=emailOnException, 
                     logDir=logDir, 
                     logTag=taskTag,
                 ),
        ]

        ### wrap up instantiation
        super(MultFITSItem, self).__init__( 
            graceid,
            gdb,
            t0,
            tasks,
            annotate=annotate,
            warnings=warnings,
            logDir=logDir,
            logTag=logTag,
        )

class multFITShtmlCheck(esUtils.EventSupervisorTask):
    """
    a check that multFITS posted an html as expected
    """
    name = "multFITShtml"

    def __init__(self, timeout, tagnames=[], emailOnSuccess=[], emailOnFailure=[], emailOnException=[], logDir='.', logTag='iQ'):
        self.tagnames = tagnames ### currently ignored
        self.description = "check that multFITS posted an html"
        super(multFITShtmlCheck, self).__init__( 
            timeout,
            emailOnSuccess=emailOnSuccess,
            emailOnFailure=emailOnFailure,
            emailOnException=emailOnException,
            logDir=logDir,
            logTag=logTag,
        )

    def multFITShtml(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that multFITS posted an htmlas expected
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag )
            logger.info( "%s : %s"%(graceid, self.description) )

        htmlname = "%s-skymapComparison.html"%(graceid) ### NOTE: this may be fragile
        fragment = "comparison of skymaps can be found <a href=\"(.*)\">here</a>"

        self.warning, action_required = esUtils.check4file( 
                                            graceid,
                                            gdb,
                                            htmlname,
                                            regex=False,
                                            tagnames=None,
                                            verbose=verbose,
                                            logFragment=fragment,
                                            logRegex=True,
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

class multFITSFinishCheck(esUtils.EventSupervisorTask):
    """
    a check that multFITS finished as expected
    """
    name = "multFITSFinish"

    def __init__(self, timeout, fitsnames, tagnames=[], emailOnSuccess=[], emailOnFailure=[], emailOnException=[], logDir='.', logTag='iQ'):
        self.fitsnames = fitsnames
        self.tagnames = tagnames ### currently ignored...
        self.description = "check that multFITS fimished processing %s"%(", ".join(fitsnames))
        super(multFITSFinishCheck, self).__init__( 
            timeout,
            emailOnSuccess=emailOnSuccess,
            emailOnFailure=emailOnFailure,
            emailOnException=emailOnException,
            logDir=logDir,
            logTag=logTag,
        )

    def multFITSFinish(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that multFITS finish as expected
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag )
            logger.info( "%s : %s"%(graceid, self.description) )

        if not esUtils.check4log( graceid, gdb, "finished skymap comparison for .*%s.*"%(".*".join(self.fitsnames)), regex=True, verbose=verbose, logTag=logger.name if verbose else None ):
            self.warning = "found multFITS finish message for %s"%(", ".join(self.fitsnames))
            if verbose or annotate:
                message = "no action required : "+self.warning
                if verbose:
                    logger.debug( "    "+message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )
            return False ### action_required = False

        self.warning = "could not find multFITS finish message for %s"%(", ".join(self.fitsname))
        if verbose or annotate:
            message = "action required : "+self.warning
            if verbose:
                logger.debug( "    "+message )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )
        return True ### action_required = True

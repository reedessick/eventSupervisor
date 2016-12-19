description = "a module housing checks of basic event_supervisor functionality"
author      = "reed.essick@ligo.org"

#---------------------------------------------------------------------------------------------------

import eventSupervisor.eventSupervisorUtils as esUtils

import re

import numpy as np

from lal.gpstime import tconvert

#---------------------------------------------------------------------------------------------------

### methods to identify updates by description
def is_psd( filename ):
    """checks if the filename corresponds to a psd.xml.gz that would satisfy cbcPSDCheck"""
    return filename == "psd.xml.gz"

#---------------------------------------------------------------------------------------------------

#-------------------------------------------------
# EventCreation
#-------------------------------------------------

class EventCreationItem(esUtils.EventSupervisorQueueItem):
    """
    a check for propper event creation and readability of associated trigger files

    read from alert:

        - graceid
        - pipeline

    read from options:

        - dt
        - email on success
        - email on failure
        - email on exception

    creates Tasks (depending on pipeline)

        - :func:`cWBTriggerCheck`
        - :func:`oLIBTriggerCheck`
        - :func:`cbcCoincCheck` and :func:`cbcPSDCheck`
    """
    name = "event creation"

    def __init__(self, alert, t0, options, gdb, annotate=False, warnings=False, logDir='.', logTag='iQ'):
        graceid  = alert['uid']
        pipeline = alert['object']['pipeline']
        self.description = "check %s event creation and trigger files"%(pipeline)

        ### extract parameters from config file
        timeout = float(options['dt'])

        emailOnSuccess = options['email on success'].split()
        emailOnFailure = options['email on failure'].split()
        emailOnException = options['email on exception'].split()

        ### generate task instances
        taskTag = "%s.%s"%(logTag, self.name)
        if pipeline=="CWB":
            tasks = [cWBTriggerCheck(
                         timeout, 
                         emailOnSuccess=emailOnSuccess, 
                         emailOnFailure=emailOnFailure, 
                         emailOnException=emailOnException, 
                         logDir=logDir, 
                         logTag=taskTag
                     ),
            ]
        elif pipeline=="LIB":
            tasks = [oLIBTriggerCheck(
                         timeout, 
                         emailOnSuccess=emailOnSuccess, 
                         emailOnFailure=emailOnFailure, 
                         emailOnException=emailOnException, 
                         logDir=logDir, 
                         logTag=taskTag
                     ),
            ]
        elif pipeline in ["gstlal", "MBTAOnline", "gstlal-spiir", "pycbc"]:
            tasks = [cbcCoincCheck(
                         timeout, 
                         emailOnSuccess=emailOnSuccess, 
                         emailOnFailure=emailOnFailure, 
                         emailOnException=emailOnException, 
                         logDir=logDir, 
                         logTag=taskTag,
                     ), 
                     cbcPSDCheck(
                         timeout, 
                         emailOnSuccess=emailOnSuccess, 
                         emailOnFailure=emailOnFailure, 
                         emailOnException=emailOnException, 
                         logDir=logDir, 
                         logTag=taskTag,
                     ),
            ]
        else:
            raise ValueError("pipeline=%s not understood"%pipeline)

        ### wrap  up instantiation
        super(EventCreationItem, self).__init__( 
            graceid, 
            gdb,
            t0, 
            tasks, 
            annotate=annotate,
            warnings=warnings,
            logDir=logDir,
            logTag=logTag,
        )

class cWBTriggerCheck(esUtils.EventSupervisorTask):
    """
    check for cWB event creation, 
    checks for the existence of a cWB "trigger_*.txt" file by exact match by predicting the filename from the gpstime.
    ignores log comments and tagnames.

    created by:

        - :func:`EventCreationItem`
    """
    description = "a check of the trigger.txt file for cWB events"
    name        = "cWBTrigger"

    def cWBTrigger(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        query GraceDB to check for proper event creation
        we check for the existence of:

            trigger_%(gpstime).4f.txt

        while ignoring log messages and tagnames
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag )
            logger.info( "%s : %s"%(graceid, self.description) )
            logger.debug( "retrieving event details" )
        event = gdb.event( graceid ).json() ### we need the gpstime, so we query

        filename = "trigger_%.4f.txt"%event['gpstime'] ### NOTE: this may be fragile
        self.warning, action_required = esUtils.check4file( graceid, gdb, filename, tagnames=None, verbose=verbose, logTag=logger.name if verbose else None )
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
 
class oLIBTriggerCheck(esUtils.EventSupervisorTask):
    """
    check for oLIB event creation
    checks for the existence of a "*.json" file by predicting the filename template using the gpstime and matching via regular expressions
    ignores tagnames and log comments

    created by:

        - :func:`EventCreationItem`
    """
    description ="a check of the trigger.json file for oLIB events"
    name        = "oLIBTrigger"

    def oLIBTrigger(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        event creation sanity check for oLIB
        we check for the existence of :

            %(gpstime).2f-(.*).json

        while ignoring log messsages and tagnames
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag )
            logger.info( "%s : %s"%(graceid, self.description) )
            logger.debug( "retrieving event details" )
        event = gdb.event( graceid ).json() ### we need the gpstime, so we query

        template = "%.2f-(.*).json"%event['gpstime'] ### NOTE: may be fragile
        template = template.replace('.00', '.0') ### This is required because of the peculiarities of how oLIB 
                                                 ### names things when the event lands on an integer second
        self.warning, action_required = esUtils.check4file( graceid, gdb, template, tagnames=None, verbose=verbose, regex=True, logTag=logger.name if verbose else None )
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

class cbcCoincCheck(esUtils.EventSupervisorTask):
    """
    check for CBC event creation, 
    we check for the existence of a coinc.xml file while ignoring log messages and tagnames

    created by:

        - :func:`EventCreationItem`
    """
    description = "check coinc.xml file for CBC events"
    name        = "cbcCoinc"

    def cbcCoinc(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        check for coinc.xml file via direct string comparison while ignoring log comments and tagnames
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag )
            logger.info( "%s : %s"%(graceid, self.description) )

        filename = "coinc.xml"
        self.warning, action_required = esUtils.check4file( graceid, gdb, filename, tagnames=None, verbose=verbose, logTag=logger.name if verbose else None )
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

class cbcPSDCheck(esUtils.EventSupervisorTask):
    """
    check for CBC event creation, 
    we check for the existence of psd.xml.gz while ignoring log comments and tagnames
    if psd.xml.gz exists, we ensure that a string representation is longer than self.psdStrLenThr via

        len(gdb.files(graceid, filename).read()) < self.psdStrLenThr)

    this hopefully ensures the PSD is not "empty" or mal-formatted, although it is a pretty loose constraint.

    created by:

        - :func:`EventCreationItem`
    """
    description = "check psd.xml.gz file for CBC events"
    name        = "cbcPSD"

    def __init__(self, timeout, psdStrLenThr=100, emailOnSuccess=[], emailOnFailure=[], emailOnException=[], logDir='.', logTag='.'):
        self.psdStrLenThr = psdStrLenThr
        super(cbcPSDCheck, self).__init__(
            timeout,
            emailOnSuccess=emailOnSuccess,
            emailOnFailure=emailOnFailure,
            emailOnException=emailOnException,
            logDir=logDir,
            logTag=logTag,
        )

    def cbcPSD(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        check for existence of psd.xml.gz file while ignoring log comments and tagnames.
        if psd.xml.gz exists, we ensure that a string representation is longer than self.psdStrLenThr via

            len(gdb.files(graceid, filename).read()) < self.psdStrLenThr)

        this hopefully ensures the PSD is not "empty" or mal-formatted, although it is a pretty loose constraint.        
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag )
            logger.info( "%s : %s"%(graceid, self.description) )

        filename = "psd.xml.gz"
        self.warning, action_required = esUtils.check4file( graceid, gdb, filename, tagnames=None, verbose=verbose, logTag=logger.name if verbose else None )

        #     found the file                      check it's length
        if (not action_required) and (len(gdb.files(graceid, filename).read()) < self.psdStrLenThr): ### found file, but need to check whether it's empty
            self.warning += ". However, the file's size seems suspiciously small."
            action_required = True

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

#-------------------------------------------------
# FAR
#-------------------------------------------------

class FARItem(esUtils.EventSupervisorQueueItem):
    """
    a check for propper FAR

    read from alert:

        - graceid

    read from options:

        - min far
        - max far
        - dt
        - email on success
        - email on failure
        - email on exception

    creates Task

        - :func:`FARCheck`
    """
    description = "check sanity of reported FAR"
    name        = "far"

    def __init__(self, alert, t0, options, gdb, annotate=False, warnings=False, logDir='.', logTag='iQ'):
        graceid = alert['uid']

        ### extract parameters from config file
        self.minFAR = float(options['min far'])
        self.maxFAR = float(options['max far'])

        timeout = float(options['dt'])

        emailOnSuccess = options['email on success'].split()
        emailOnFailure = options['email on failure'].split()
        emailOnException = options['email on exception'].split()

        ### generate tasks
        tasks = [FARCheck(
                     timeout, 
                     maxFAR=self.maxFAR, 
                     minFAR=self.minFAR, 
                     emailOnSuccess=emailOnSuccess, 
                     emailOnFailure=emailOnFailure, 
                     emailOnException=emailOnException, 
                     logDir=logDir, 
                     logTag="%s.%s"%(logTag, self.name),
                 ),
        ]

        ### wrap up instantiation
        super(FARItem, self).__init__( 
            graceid, 
            gdb, 
            t0, 
            tasks, 
            annotate=annotate,
            warnings=warnings,
            logDir=logDir,
            logTag=logTag,
        )

class FARCheck(esUtils.EventSupervisorTask):
    """
    a check for propper FAR.
    ensures the FAR is defined and is within an acceptable range.
    Queries GraceDb to retrieve the event's FAR.

    created by:

        - :func:`FARItem`
    """
    description = "a check for propper FAR"
    name        = "far"

    def __init__(self, timeout, maxFAR=1.0, minFAR=0.0, emailOnSuccess=[], emailOnFailure=[], emailOnException=[], logDir='.', logTag='iQ'):
        self.maxFAR = maxFAR
        self.minFAR = minFAR
        
        super(FARCheck, self).__init__( 
            timeout, 
            emailOnSuccess=emailOnSuccess,
            emailOnFailure=emailOnFailure,
            emailOnException=emailOnException,
            logDir=logDir,
            logTag=logTag,
        )

    def far(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        check the sanity of the reported FAR
        Queries GraceDb for the event's data and ensures (FAR > self.minFAR) and (FAR < self.maxFAR)
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag )
            logger.info( "%s : %s"%(graceid, self.description) )
            logger.debug( "retrieving event details" )
        event = gdb.event( graceid ).json()

        if event.has_key("far") and event['far']!=None: ### ensure FAR exists and is set

            ### check bounds
            far = event['far']
            big = far > self.maxFAR
            sml = far < self.minFAR

            if big: ### far is too big
                self.warning = "FAR=%.3e > %.3e"%(far, self.maxFAR)
                if verbose or annotate:
                    message = "action required : "+self.warning

                    ### post message
                    if verbose:
                        logger.debug( message )
                    if annotate:
                        esUtils.writeGDBLog( gdb, graceid, message )

                return True ### action_required=True
                
            elif sml: ### far is too small
                self.warning = "FAR=%.3e < %.3e"%(far, self.minFAR)
                if verbose or annotate:
                    message = "action required : "+self.warning

                    ### post message
                    if verbose:
                        logger.debug( message )
                    if annotate:
                        esUtils.writeGDBLog( gdb, graceid, message )

                return True ### action_required=True

            else: ### far is within an uninteresting range
                self.warning = "%.3e <= FAR=%.3e <= %.3e"%(self.minFAR, far, self.maxFAR)
                if verbose or annotate:
                    message = "no action required : "+self.warning

                    ### post message
                    if verbose:
                        logger.debug( message )
                    if annotate:
                        esUtils.writeGDBLog( gdb, graceid, message )

                return False ### action_required=False

        else: ### something is very wrong...

            self.warning = "FAR is not defined!"
            if verbose or annotate:
                message = "action required : "+self.warning

                ### post message
                if verbose:
                    logger.warn( message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )

            return True ### action_required=True

#-------------------------------------------------
# localRate
#-------------------------------------------------

class LocalRateItem(esUtils.EventSupervisorQueueItem):
    """
    a check for local rate of events submitted to GraceDb around the event's gpstime

    read alert:

        - graceid
        - group
        - pipeline
        - search

    read from options:

        - win+
        - win-
        - maxRate
        - dt 
        - email on success
        - email on failure
        - email on exception

    creates Task

        - :func:`localRateCheck`
    """
    description = "check local rates of events"
    name        = "local rate"

    def __init__(self, alert, t0, options, gdb, annotate=False, warnings=False, logDir='.', logTag='iQ'):
        graceid  = alert['uid']
        group    = alert['object']['group']
        pipeline = alert['object']['pipeline']
        if alert['object'].has_key('search'):
            search = alert['object']['search']
        else:
            search = None

        ### extract parameters from config
        pWin = float(options['win+'])
        mWin = float(options['win-'])
        maxRate = float(options['max rate'])

        timeout = float(options['dt'])

        emailOnSuccess = options['email on success'].split()
        emailOnFailure = options['email on failure'].split()
        emailOnException = options['email on exception'].split()

        ### gnerate tasks
        tasks = [localRateCheck(
                     timeout, 
                     group, 
                     pipeline, 
                     search=search, 
                     pWin=pWin, 
                     mWin=mWin, 
                     maxRate=maxRate, 
                     emailOnSuccess=emailOnSuccess, 
                     emailOnFailure=emailOnFailure, 
                     emailOnException=emailOnException, 
                     logDir=logDir, 
                     logTag='%s.%s'%(logTag, self.name),
                 ),
        ] 

        ### wrap up instantiation
        super(LocalRateItem, self).__init__( 
            graceid, 
            gdb,
            t0, 
            tasks,
            annotate=annotate,
            warnings=warnings,
            logDir=logDir,
            logTag=logTag,
        )

class localRateCheck(esUtils.EventSupervisorTask):
    """
    a check for local rate of events submitted to GraceDB in the neighborhood of the event's gpstime.
    Queries GraceDb for neighbors within [gpstime-mWin, gpstime+pWin) and compares this to an acceptable rate.

    created by:

        - :func:`LocalRateItem`
    """
    name = "localRate"

    def __init__(self, timeout, group, pipeline, search=None, pWin=5.0, mWin=5.0, maxRate=2.0, emailOnSuccess=[], emailOnFailure=[], emailOnException=[], logDir='.', logTag='iQ'):
        self.description = "a check of local rates for %s_%s"%(group, pipeline)
        if search:
            self.description = "%s_%s"%(description, search)
        self.group    = group
        self.pipeline = pipeline
        self.search   = search

        self.pWin=pWin
        self.mWin=mWin
        self.maxRate=maxRate

        super(localRateCheck, self).__init__( 
            timeout, 
            emailOnSuccess=emailOnSuccess,
            emailOnFailure=emailOnFailure,
            emailOnException=emailOnException,
            logDir=logDir,
            logTag=logTag,
        )

    def localRate(self, graceid, gdb, verbose=None, annotate=False, **kwargs):
        """
        check the local rate of triggers submitted to GraceDB
        checks only around the event's gpstime : [gpstime-self.mWin, gpstime+self.pWin)
        Queries GraceDb to find neighboring events
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag )
            logger.info( "%s : %s"%(graceid, self.description) )

        ### get this event
        if verbose:
            logger.debug( "retrieving information about this event" )
        gdb_entry = gdb.event( graceid ).json()

        ### get event time
        event_time = float(gdb_entry['gpstime'])
        if verbose:
            logger.debug( "gpstime : %.6f"%(event_time) )
            logger.debug( "retrieving neighbors within [%.6f-%.6f, %.6f+%6f]"%(event_time, self.mWin, event_time, self.pWin) )

        ### count the number of neighbors
        count = 0
        for entry in gdb.events( "%d .. %d"%(np.floor(event_time-self.mWin), np.ceil(event_time+self.pWin)) ): ### query for neighbors in (t-mWin, t+pWin)
            if not entry.has_key('search'): 
                entry['search'] = None
            ###         not the 'current' event          belongs to the right group        associated with the right pipeline           from the correct search
            count += (entry['graceid'] != graceid) and (entry['group'] == self.group) and (entry['pipeline'] == self.pipeline) and (entry['search'] == self.search) ### add to count
            
        if count > (self.pWin+self.mWin)*self.maxRate: ### too many neighbors
            self.warning = "found %d events within (-%.3f, +%.3f) of %s"%(count, self.mWin, self.pWin, graceid)
            if verbose or annotate:
                message = "action required : "+self.warning

                ### post message
                if verbose:
                    logger.debug( message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message=message )  

            return True ### action_required = True

        else: ### an acceptable number of neighbors
            self.warning = "found %d events within (-%.3f, +%.3f) of %s"%(count, self.mWin, self.pWin, graceid)
            if verbose or annotate:
                message = "no action required : "+self.warning

                ### post message
                if verbose:
                    logger.debug( message )
                if annotate:
                    message = "event_supervisor : "+message
                    esUtils.writeGDBLog( gdb, graceid, message )

            return False ### action_required = False

class CreateRateItem(esUtils.EventSupervisorQueueItem):
    """
    a check for local rate of events submitted to GraceDb around the event's creation time

    read from alert:

        - graceid
        - group
        - pipeline
        - search

    read from options:

        - win+
        - win-
        - maxRate
        - dt 
        - email on success
        - email on failure
        - email on exception

    creates Task

        - :func:`createRateCheck`
    """
    description = "check creation rates of events"
    name        = "creation rate"

    def __init__(self, alert, t0, options, gdb, annotate=False, warnings=False, logDir='.', logTag='iQ'):
        graceid  = alert['uid']
        group    = alert['object']['group']
        pipeline = alert['object']['pipeline']
        if alert['object'].has_key('search'):
            search = alert['object']['search']
        else:
            search = None

        ### extract parameters from config
        pWin = float(options['win+'])
        mWin = float(options['win-'])
        maxRate = float(options['max rate'])

        timeout = float(options['dt'])

        emailOnSuccess = options['email on success'].split()
        emailOnFailure = options['email on failure'].split()
        emailOnException = options['email on exception'].split()

        ### generate tasks
        tasks = [createRateCheck(
                     timeout, 
                     group, 
                     pipeline, 
                     search=search, 
                     pWin=pWin, 
                     mWin=mWin, 
                     maxRate=maxRate, 
                     emailOnSuccess=emailOnSuccess, 
                     emailOnFailure=emailOnFailure, 
                     emailOnException=emailOnException, 
                     logDir=logDir, 
                     logTag='%s.%s'%(logTag, self.name),
                 ),
        ]

        ### wrap up instantiation
        super(CreateRateItem, self).__init__( 
            graceid,
            gdb,
            t0,
            tasks,
            annotate=annotate,
            warnings=warnings,
            logDir='.',
            logTag='.',
        )

class createRateCheck(esUtils.EventSupervisorTask):
    """
    a check for local rate of events submitted to GraceDB in the neighborhood of the event's creation time
    Queries GraceDb for neighbors within [gpstime-mWin, gpstime+pWin] and compares the result with an acceptable rate

    created by:

        - :func:`CreateRateItem`
    """
    name = "createRate"

    def __init__(self, timeout, group, pipeline, search=None, pWin=5.0, mWin=5.0, maxRate=2.0, emailOnSuccess=[], emailOnFailure=[], emailOnException=[], logDir='.', logTag='iQ'):
        self.description = "a check of creation rate for %s_%s"%(group, pipeline)
        if search:
            self.description = "%s_%s"%(self.description, search)
        self.group    = group
        self.pipeline = pipeline
        self.search   = search

        self.pWin=pWin
        self.mWin=mWin
        self.maxRate=maxRate

        super(createRateCheck, self).__init__( 
            timeout,
            emailOnSuccess=emailOnSuccess,
            emailOnFailure=emailOnFailure,
            emailOnException=emailOnException,
            logDir=logDir,
            logTag=logTag,
        )

    def createRate(self, graceid, gdb, verbose=None, annotate=False, **kwargs):
        """
        check the local rate of triggers submitted to GraceDB
        checks only around the event's creation time : [t-self.mWin, t+self.pWin)
        Queries GraceDb for neighbors
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag )
            logger.info( "%s : %s"%(graceid, self.description) )
            logger.debug( "retrieving information about this event" )
        gdb_entry = gdb.event( graceid ).json()

        ### get event time
        event_time = float(tconvert( gdb_entry['created'][:-4] )) ### we strip the time-zone to help tconvert format this 
        winstart = tconvert( np.floor(event_time-self.mWin ), form="%Y-%m-%d %H:%M:%S" )
        winstop  = tconvert( np.ceil( event_time+self.pWin ), form="%Y-%m-%d %H:%M:%S" )

        if verbose:
            logger.debug( "%s -> %.3f"%(gdb_entry['created'], event_time) )
            logger.debug( "retrieving neighbors within [%s, %s]"%(winstart, winstop) )

        ### count the number of neighbors
        count = 0
        for entry in gdb.events( "created: %s .. %s"%(winstart, winstop) ): ### query for neighbors in (t-mWin, t+pWin)
            if not entry.has_key('search'):
                entry['search'] = None
            ###         not the 'current' event          belongs to the right group        associated with the right pipeline           from the correct search
            count += (entry['graceid'] != graceid) and (entry['group'] == self.group) and (entry['pipeline'] == self.pipeline) and (entry['search'] == self.search) ### add to count

        if count > (self.pWin+self.mWin)*self.maxRate: ### too many neighbors
            self.warning = self.warning = "found %d events within (-%.3f, +%.3f) of %s"%(count, self.mWin, self.pWin, graceid)
            if verbose or annotate:
                message = "action required : found %d events within (-%.3f, +%.3f) of %s creation"%(count, self.mWin, self.pWin, graceid)

                ### post messsage
                if verbose:
                    logger.debug( message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message=message )

            return True ### action_required = True

        else: ### an acceptable number of neighbors
            self.warning = "found %d events within (-%.3f, +%.3f) of %s"%(count, self.mWin, self.pWin, graceid)
            if verbose or annotate:
                message = "no action required : found %d events within (-%.3f, +%.3f) of %s creation"%(count, self.mWin, self.pWin, graceid)

                ### post message
                if verbose:
                    logger.debug( message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )

            return False ### action_required = False

#-------------------------------------------------
# external triggers
#-------------------------------------------------

class ExternalTriggersItem(esUtils.EventSupervisorQueueItem):
    """
    a check that the external triggers search was completed

    read from alert:

        - graceid

    options:

        - dt
        - email on success
        - email on failure
        - email on exception

    creates Task:

        - :func:`externalTriggersCheck`
    """
    description = "check that the unblind injection search completed"
    name        = "external triggers"

    def __init__(self, alert, t0, options, gdb, annotate=False, warnings=False, logDir='.', logTag='iQ'):
        graceid = alert['uid']

        ### extract params from config
        timeout = float(options['dt'])

        emailOnSuccess = options['email on success'].split()
        emailOnFailure = options['email on failure'].split()
        emailOnException = options['email on exception'].split()

        ### generate tasks
        tasks = [externalTriggersCheck(
                     timeout, 
                     emailOnSuccess=emailOnSuccess, 
                     emailOnFailure=emailOnFailure, 
                     emailOnException=emailOnException, 
                     logDir=logDir, 
                     logTag='%s.%s'%(logTag,self.name),
                 ),
        ]

        ### wrap up instantiation
        super(ExternalTriggersItem, self).__init__( 
            graceid, 
            gdb,
            t0, 
            tasks, 
            annotate=annotate,
            warnings=warnings,
            logDir=logDir,
            logTag=logTag,
        )

class externalTriggersCheck(esUtils.EventSupervisorTask):
    """
    a check that the external triggers seach was completed.
    looks for a log message only, ignoring tagnames and files

    created by:

        - :func:`ExternalTriggersItem`
    """
    description = "a check that the external triggers search was completed"
    name        = "externalTriggers"

    def externalTriggers(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that the external triggers search was completed.
        looks for a log message only, ignoring tagnames and files
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag )
            logger.info( "%s : %s"%(graceid, self.description) )

        if not esUtils.check4log( graceid, gdb, "Coincidence search complete", verbose=verbose, logTag=logger.name if verbose else None ): ### check for log message
            self.warning = "found external triggers coinc search completion message"
            if verbose or annotate:
                message = "no action required : "+self.warning

                ### post message
                if verbose:
                    logger.debug( message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )

            return False ### action_required = False

        else:
            self.warning = "could not find external triggers search completion message"
            if verbose or annotate:
                message = "action required : "+self.warning

                ### post message
                if verbose:
                    logger.debug( message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )

            return True ### action_required = True

#-------------------------------------------------
# unblind injections
#-------------------------------------------------

class UnblindInjectionsItem(esUtils.EventSupervisorQueueItem):
    """
    a check that the unblind Injections search was completed

    read from alert:

        - graceid

    options:

        - dt 
        - email on success
        - email on failure
        - email on exception

    creates Task:

        - :func:`unblindInjectionsCheck`
    """
    description = "check that the unblind injection search completed"
    name        = "unblind injections"

    def __init__(self, alert, t0, options, gdb, annotate=False, warnings=False, logDir='.', logTag='iQ'):
        graceid = alert['uid']

        ### exract parameters from config
        timeout = float(options['dt'])

        emailOnSuccess = options['email on success'].split()
        emailOnFailure = options['email on failure'].split()
        emailOnException = options['email on exception'].split()

        ### generate tasks
        tasks = [unblindInjectionsCheck(
                     timeout, 
                     emailOnSuccess=emailOnSuccess, 
                     emailOnFailure=emailOnFailure, 
                     emailOnException=emailOnException, 
                     logDir=logDir, 
                     logTag='%s.%s'%(logTag, self.name),
                 )
        ]

        ### wrap up instantiation
        super(UnblindInjectionsItem, self).__init__( 
            graceid, 
            gdb,
            t0, 
            tasks, 
            annotate=annotate,
            warnings=warnings,
            logDir=logDir,
            logTag=logTag,
        )

class unblindInjectionsCheck(esUtils.EventSupervisorTask):
    """
    a check that the unblind injections search was completed.
    looks for a log message only while ignoring tagnames and files.

    created by:

        - :func:`UnblindInjectionsItem`
    """
    description = "a check that the unblind injections search was completed"
    name        = "unblindInjections"

    def unblindInjections(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that the unblind injections search was completed.
        looks for a log message only while ignoring tagnames and files
        """
        ### NOTE: we do not delegate to esUtils.check4log here because we need to look for mutliple logs...
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag )
            logger.info( "%s : %s"%(graceid, self.description) )
            logger.debug( "retrieving log messages" )
        logs = gdb.logs( graceid ).json()['log']

        if verbose:
            logger.debug( "parsing log" )

        if esUtils.check4log( graceid, gdb, "No unblind injections in window", verbose=verbose, logTag=logger.name if verbose else None ): ### check for log message
            self.warning = "process reported that no unblind injections were found"
            if verbose or annotate:
                message = "no action required : "+self.warning

                ### post message
                if verbose:
                    logger.debug( message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )

            return False ### action_required = False

        if verbose:
            logger.warn( "we do not currently know how to parse out statements when there *is* an unblind injection...raising an alarm anyway" )

        self.warning = "could not find a statement about unblind injections"
        if verbose or annotate:
            message = "action required : "+self.warning

            ### post message
            if verbose:
                logger.debug( message )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )

        return True ### action_required = True

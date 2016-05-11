description = "a module housing checks of basic event_supervisor functionality"
author = "reed.essick@ligo.org"

#---------------------------------------------------------------------------------------------------

import sys
sys.path.append("../")
import eventSupervisorUtils as esUtils

import re

import numpy as np

from lal.gpstime import tconvert

#---------------------------------------------------------------------------------------------------

### methods to identify updates by description

#---------------------------------------------------------------------------------------------------

#-------------------------------------------------
# EventCreation
#-------------------------------------------------

class EventCreationItem(esUtils.EventSupervisorQueueItem):
    """
    a check for propper event creation and readability of associated trigger files
    """
    name = "event creation"

    def __init__(self, alert, t0, options, gdb, annotate=False):
        graceid = alert['uid']
        pipeline = alert['pipeline']

        timeout = float(options['dt'])
        email = options['email'].split()

        if pipeline=="cwb":
            tasks = [cWBTriggerCheck(timeout, email=email)]
        elif pipeline=="lib":
            tasks = [oLIBTriggerCheck(timeout, email=email)]
        elif pipeline in ["gstlal", "mbtaonline", "gstlal-spiir", "pycbc"]:
            tasks = [cbcCoincCheck(timeout, email=email), 
                     cbcPSDCheck(timeout, email=email)
                    ]
        else:
            raise ValueError("pipeline=%s not understood"%pipeline)

        self.description = "check %s event creation and trigger files"%(pipeline)
        super(EventCreationItem, self).__init__( graceid, 
                                                 gdb,
                                                 t0, 
                                                 tasks, 
                                                 annotate=annotate 
                                                )

class cWBTriggerCheck(esUtils.EventSupervisorTask):
    """
    check for cWB event creation, checking the trigger.txt file
    """
    description = "a check of the trigger.txt file for cWB events"
    name = "cWBTrigger"

    def __init__(self, timeout, email=[]):
        super(cwbTriggerCheck, self).__init__( timeout, 
                                               self.cWBTriggerCheck, 
                                               email=email
                                             )

    def cWBTriggerCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        query GraceDB to check for proper event creation
        we check:
            trigger_gpstime.txt
        """
        if verbose:
            print( "%s : %s"%(graceid, self.description) )
            print( "    retrieving event details" )
        event = gdb.event( graceid ).json()

        filename = "trigger_%.4f.txt"%event['gpstime']
        self.warning, action_required = check4file( graceid, gdb, filename, tagnames=None, verbose=verbose )
        if verbose or annotate:
            if action_required:
                message = "action required : "+self.warning
            else:
                message = "no action required : "+self.warning
            if verbose:
                print( "    "+message )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )
        return action_required
 
class oLIBTriggerCheck(esUtils.EventSupervisorTask):
    """
    check for oLIB event creation
    """
    description="a check of the trigger.json file for oLIB events"
    name = "oLIBTrigger"

    def __init__(self, timeout, email=[]):
        super(oLIBTriggerCheck, self).__init__( timeout, 
                                                self.oLIBTriggerCheck, 
                                                email=email
                                              )

    def oLIBTriggerCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        event creation sanity check for oLIB
        we check:
            gpstime-.\.json
        """
        if verbose:
            print( "%s : %s"%(graceid, self.description) )
            print( "    retrieving event details" )
        event = gdb.event( graceid ).json()

        template = ("%.2f-d.json"%event['gpstime']).replace(".","\.").replace("d",".") 
        self.warning, action_required = check4file( graceid, gdb, template, tagnames=None, verbose=verbose, regex=True )
        if verbose or annotate:
            if action_required:
                message = "action required : "+self.warning
            else:
                message = "no action required : "+self.warning
            if verbose:
                print( "    "+message )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )
        return action_required

class cbcCoincCheck(esUtils.EventSupervisorTask):
    """
    check for CBC event creation, checking coinc.xml file
    """
    description = "check coinc.xml file for CBC events"
    name = "cbcCoinc"

    def __init__(self, timeout, email=[]):
        super(cbcCoincCheck, self).__init__( timeout, 
                                             self.cbcCoincCheck, 
                                             email=email
                                           )

    def cbcTriggerCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        check for coinc.xml file
        """
        if verbose:
            print( "%s : %s"%(graceid, self.description) )

        filename = "coinc.xml"
        self.warning, action_required = check4file( graceid, gdb, filename, tagnames=None, verbose=verbose )
        if verbose or annotate:
            if action_required:
                message = "action required : "+self.warning
            else:
                message = "no action required : "+self.warning
            if verbose:
                print( "    "+message )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )
        return action_required

class cbcPSDCheck(esUtils.EventSupervisorTask):
    """
    check for CBC event creation, checking PSD.xml file
    """
    description = "check psd.xml.gz file for CBC events"
    name = "cbcPSD"

    def __init__(self, timeout, email=[]):
        super(cbcPSDCheck, self).__init__( timeout, 
                                           self.cbcPSDCheck, 
                                           email=email
                                         )

    def cbcPSDCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        check for psd.xml.gz file
        """
        if verbose:
            print( "%s : %s"%(graceid, self.description) )
        filename = "psd.xml.gz"
        self.warning, action_required = check4file( graceid, gdb, filename, tagnames=None, verbose=verbose )
        if verbose or annotate:
            if action_required:
                message = "action required : "+self.warning
            else:
                message = "no action required : "+self.warning
            if verbose:
                print( "    "+message )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )
        return action_required

#-------------------------------------------------
# FAR
#-------------------------------------------------

class FARItem(esUtils.EventSupervisorQueueItem):
    """
    a check for propper FAR
    """
    name = "far"
    description = "check sanity of reported FAR"

    def __init__(self, alert, t0, options, gdb, annotate=False):
        graceid = alert['uid']

        timeout = float(options['dt'])
        email = options['email'].split()

        tasks = [FARCheck(timeout, email=email)]
        super(FARItem, self).__init__( graceid, 
                                       gdb, 
                                       t0, 
                                       tasks, 
                                       annotate=annotate
                                     )

class FARCheck(esUtils.EventSupervisorTask):
    """
    a check for propper FAR
    """
    description = "a check for propper FAR"
    name = "FAR"

    def __init__(self, timeout, maxFAR=1.0, minFAR=0.0, annotate=False, email=[]):
        self.maxFAR = maxFAR
        self.minFAR = minFAR
        
        super(farCheck, self).__init__( timeout, 
                                        self.FARCheck, 
                                        email=email
                                      )

    def FARCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        check the sanity of the reported FAR
        """
        if verbose:
            print( "%s : %s"%(graceid, self.description) )
            print( "    retrieving event details" )
        event = gdb.event( gdb_id ).json()

        if event.has_key("far"): ### check bounds
            far = event['far']
            big = far > maxFAR
            sml = far < minFAR

            if big:
                self.warning = "FAR=%.3e > %.3e"%(far, maxFAR)
                if verbose or annotate:
                    message = "action required : "+self.warning
                    if verbose:
                        print( message )
                    if annotate:
                        esUtils.writeGDBLog( gdb, graceid, message )
                return True ### action_required=True
                
            elif sml:
                self.warning = "FAR=%.3e < %.3e"%(far, minFAR)
                if verbose or annotate:
                    message = "action required : "+self.warning
                    if verbose:
                        print( message )
                    if annotate:
                        gdb.writeGDBLog( gdb, graceid, message )
                return True ### action_required=True

            else:
                self.warning = "%.3e <= FAR=%.3e <= %.3e"%(minFAR, far, maxFAR)
                if verbose or annotate:
                    message = "no action required : "+self.warning
                    if verbose:
                        print( message )
                    if annotate:
                        gdb.writeGDBLog( gdb, graceid, message )
                return False ### action_required=False

        else: ### something is very wrong...
            self.warning = "FAR is not defined!"
            if verbose or annotate:
                message = "action required : "+self.warning
                if verbose:
                    print( message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )

            return True ### action_required=True

#-------------------------------------------------
# localRate
#-------------------------------------------------

class LocalRateItem(esUtils.EventSupervisorQueueItem):
    """
    a check for local rate of events submitted to GraceDb around the event's gpstime
    """
    name = "local rate"
    description = "check local rates of events"

    def __init__(self, alert, t0, options, gdb, annotate=False):
        graceid = alert['uid']
        group = alert['group']
        pipeline = alert['pipeline']
        if alert.has_key('search'):
            search = alert['search']
        else:
            search = None

        pWin = float(options['win+'])
        mWin = float(options['win-'])
        maxRate = float(options['max rate'])

        timeout = float(options['dt'])
        email = options['email'].split()

        tasks = [ localRateCheck(timeout, group, pipeline, search=search, pWin=pWin, mWin=mWin, maxRate=maxRate, email=email) ] 
        super(LocalRateItem, self).__init__( graceid, 
                                             gdb,
                                             t0, 
                                             tasks,
                                             annotate=annotate
                                           )

class localRateCheck(esUtils.EventSupervisorTask):
    """
    a check for local rate of events submitted to GraceDB in the neighborhood of the event's gpstime
    """
    name = "localRate"

    def __init__(self, timeout, group, pipeline, search=None, pWin=5.0, mWin=5.0, maxRate=2.0, email=[]):
        description = "a check of local rates for %s_%s"%(group, pipline)
        if search:
            description = "%s_%s"%(description, search)
        self.group = group
        self.pipeline = pipeline
        self.search = search
        super(localRateCheck, self).__init__( timeout, 
                                              self.localRateCheck, 
                                              email=email
                                            )

    def localRateCheck(self, graceid, gdb, verbose=None, annotate=False):
        """
        check the local rate of triggers submitted to GraceDB
        checks only around the event's gpstime : (gpstime-self.mWin, gpstime+self.pWin)
        """
        if verbose:
            report( "%s : %s"%(graceid, self.description) )

        ### get this event
        if verbose:
            print( "    retrieving information about this event" )
        gdb_entry = gdb.event( graceid ).json()

        ### get event time
        event_time = float(gdb_entry['gpstime'])
        if verbose:
            print( "    gpstime : %.6f"%(event_time) )
        if verbose:
            report( "    retrieving neighbors within [%.6f-%.6f, %.6f+%6f]"%(event_time, mWin, event_time, pWin) )

        count = 0
        for entry in gdb.events( "%d .. %d"%(np.floor(event_time-self.mWin), np.ceil(event_time+self.pWin)) ): ### query for neighbors in (t-mWin, t+pWin)
            if not entry.has_key('search'): 
                entry['search'] = None
            ###         not the 'current' event          belongs to the right group        associated with the right pipeline           from the correct search
            count += (entry['graceid'] != graceid) and (entry['group'] == self.group) and (entry['pipeline'] == self.pipeline) and (entry['search'] == self.search) ### add to count
            
        if count > (pWin+mWin)*maxRate:
            self.warning = "found %d events within (-%.3f, +%.3f) of %s"%(count, self.mWin, self.pWin, graceid)
            if verbose or annotate:
                message = "action required : "+self.warning
                if verbose:
                    print( "    "+message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message=message )  
            return True ### action_required = True
        else:
            self.warning = "found %d events within (-%.3f, +%.3f) of %s"%(count, self.mWin, self.pWin, graceid)
            if verbose or annotate:
                message = "no action required : "+self.warning
                if verbose:
                    print( "    "+message )
                if annotate:
                    message = "event_supervisor : "+message
                    esUtils.writeGDBLog( gdb, graceid, message )
            return False ### action_required = False

class CreateRateItem(esUtils.EventSupervisorQueueItem):
    """
    a check for local rate of events submitted to GraceDb around the event's creation time
    """
    name = "creation rate"
    description = "check creation rates of events"

    def __init__(self, alert, t0, options, gdb, annotate=False):
        graceid = alert['uid']
        group = alert['group']
        pipeline = alert['pipeline']
        if alert.has_key('search'):
            search = alert['search']
        else:
            search = None

        pWin = float(options['win+'])
        mWin = float(options['win-'])
        maxRate = float(options['max rate'])

        timeout = float(options['dt'])
        email = options['email'].split()

        tasks = [ createRateCheck(timeout, group, pipeline, search=search, pWin=pWin, mWin=mWin, maxRate=maxRate, email=email) ]
        super(CreateRateItem, self).__init__( graceid,
                                             gdb,
                                             t0,
                                             tasks,
                                             annotate=annotate
                                           )

class createRateCheck(esUtils.EventSupervisorTask):
    """
    a check for local rate of events submitted to GraceDB in the neighborhood of the event's creation time
    """
    name = "createRate"

    def __init__(self, timeout, group, pipeline, search=None, pWin=5.0, mWin=5.0, maxRate=2.0, email=[]):
        description = "a check of creation rate for %s_%s"%(group, pipline)
        if search:
            description = "%s_%s"%(description, search)
        self.group = group
        self.pipeline = pipeline
        self.search = search
        super(createRateCheck, self).__init__( timeout,
                                              self.createRateCheck,
                                              email=email
                                            )

    def createRateCheck(self, graceid, gdb, verbose=None, annotate=False):
        """
        check the local rate of triggers submitted to GraceDB
        checks only around the event's creation time : (t-self.mWin, t+self.pWin)
        """
        if verbose:
            report( "%s : %s"%(graceid, self.description) )

        ### get this event
        if verbose:
            print( "    retrieving information about this event" )
        gdb_entry = gdb.event( graceid ).json()

        ### get event time
        event_time = tconvert( gdb_entry['created'] )
        if verbose: 
            print( "    %s -> %.3f"%(gdb_entry['created'], event_time) )

        winstart = tconvert( np.floor(event_time-mWin ), form="%Y-%m-%d %H:%M:%S" )
        winstop  = tconvert( np.ceil( event_time+pWin ), form="%Y-%m-%d %H:%M:%S" )

        if verbose:
            print( "\tretrieving neighbors within [%s, %s]"%(winstart, winstop) )

        count = 0
        for entry in gdb.events( "created: %s .. %s"%(winstart, winstop) ): ### query for neighbors in (t-mWin, t+pWin)
            if not entry.has_key('search'):
                entry['search'] = None
            ###         not the 'current' event          belongs to the right group        associated with the right pipeline           from the correct search
            count += (entry['graceid'] != graceid) and (entry['group'] == self.group) and (entry['pipeline'] == self.pipeline) and (entry['search'] == self.search) ### add to count

        if count > (pWin+mWin)*maxRate:
            self.warning = self.warning = "found %d events within (-%.3f, +%.3f) of %s"%(count, self.mWin, self.pWin, graceid)
            if verbose or annotate:
                message = "action required : found %d events within (-%.3f, +%.3f) of %s creation"%(count, self.mWin, self.pWin, graceid)
                if verbose:
                    print( "    "+message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message=message )
            return True ### action_required = True
        else:
            self.warning = "found %d events within (-%.3f, +%.3f) of %s"%(count, self.mWin, self.pWin, graceid)
            if verbose or annotate:
                message = "no action required : found %d events within (-%.3f, +%.3f) of %s creation"%(count, self.mWin, self.pWin, graceid)
                if verbose:
                    print( "    "+message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )
            return False ### action_required = False

#-------------------------------------------------
# external triggers
#-------------------------------------------------

class ExternalTriggersItem(esUtils.EventSupervisorQueueItem):
    """
    a check that the external triggers search was completed
    """
    name = "external triggers"
    description = "check that the unblind injection search completed"

    def __init__(self, alert, t0, options, gdb, annotate=False):
        graceid = alert['uid']

        timeout = float(options['dt'])
        email = options['email'].split()

        tasks = [externalTriggersCheck(timeout, email=email)]
        super(ExternalTriggersItem, self).__init__( graceid, 
                                                    gdb,
                                                    t0, 
                                                    tasks, 
                                                    annotate=annotate
                                                  )

class externalTriggersCheck(esUtils.EventSupervisorTask):
    """
    a check that the external triggers seach was completed
    """
    description = "a check that the external triggers search was completed"
    name = "ExternalTriggers"

    def __init__(self, timeout, email=[]):
        """
        a check that the external triggers search was completed
        """
        super(externalTriggersCheck, self).__init__( timeout, 
                                                     self.externalTriggersCheck, 
                                                     email=email
                                                   )
    
    def externalTriggersCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that the external triggers search was completed
        """
        if verbose:
            print( "%s : %s"%(graceid, self.description) )
        if not esUtils.check4log( graceid, gdb, "Coincidence search complete", verbose=verbose ):
            self.warning = "found external triggers coinc search completion message"
            if verbose or annotate:
                message = "no action required : "+self.warning
                if verbose:
                    print( "    "+message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )
            return False ### action_required = False

        self.warning = "could not find external triggers search completion message"
        if verbose or annotate:
            message = "action required : "+self.warning
            if verbose:
                print( "    "+self.warning )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )
        return True ### action_required = True

#-------------------------------------------------
# unblind injections
#-------------------------------------------------

class UnblindInjectionsItem(esUtils.EventSupervisorQueueItem):
    """
    a check that the unblind Injections search was completed
    """
    name = "unblind injections"
    description = "check that the unblind injection search completed"

    def __init__(self, alert, t0, options, gdb, annotate=False):
        graceid = alert['uid']

        timeout = float(options['dt'])
        email = options['email'].split()

        tasks = [unblindInjectionsCheck(timeout, email=email)]
        super(UnblindInjectionsItem, self).__init__( graceid, 
                                                     gdb,
                                                     t0, 
                                                     tasks, 
                                                     annotate=annotate
                                                   )

class unblindInjectionsCheck(esUtils.EventSupervisorTask):
    """
    a check that the unblind injections search was completed
    """
    description = "a check that the unblind injections search was completed"
    name = "unblindInjections"

    def __init__(self, timeout, email=[]):
        """
        a check that the unblind injections search was completed
        """
        super(unblindInjectionsCheck, self).__init__( timeout, 
                                                      self.unblindInjectionsCheck, 
                                                      email=email
                                                    )

    def unblindInjectionsCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that the unblind injections search was completed
        """
        ### NOTE: we do not delegate to esUtils.check4log here because we need to look for mutliple logs...
        if verbose:
            print( "%s : %s"%(graceid, self.description) )
            print( "    retrieving log messages" )
        logs = gdb.logs( graceid ).json()['log']

        if verbose:
            print( "    parsing log" )
        for log in logs:
            comment = log['comment']
            if "No unblind injections in window" in comment:
                self.warning = "process reported that no unblind injections were found"
                if verbose or annotate:
                    message = "no action required : "+self.warning
                    if verbose:
                        print( "    "+message )
                    if annotate:
                        esUtils.writeGDBLog( gdb, graceid, message )
                return False ### action_required = False

        print( "    WARNING: we do not currently know how to parse out statements when there *is* an unblind injection...raising an alarm anyway" )

        self.warning = "could not find a statement about unblind injections"
        if verbose or annotate:
            message = "action required : "+self.warning
            if verbose:
                print( "    "+message )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )
        return True ### action_required = True

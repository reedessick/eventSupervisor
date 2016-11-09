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
        email
    """
    name = "cwb pe start"
    description = "a check that cWB PE started"

    def __init__(self, alert, t0, options, gdb, annotate=False):
        graceid = alert['uid']

        timeout = float(options['dt'])
        email = options['email'].split()

        tasks = [cWBPEStartCheck(timeout, email)]
        super(CWBPEStartItem, self).__init__( graceid,
                                              gdb,
                                              t0,
                                              tasks,
                                              annotate=annotate
                                            )

class cWBPEStartCheck(esUtils.EventSupervisorTask):
    """
    a check that cWB PE started
    """    
    name = "cWBPEStart"
    description = "a check that cWB PE started"

    def __init__(self, timeout, email=[]):
        super(cWBPEStartCheck, self).__init__( timeout,
                                               email=email
                                             )

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
        email
    """
    name = "cwb pe"
    description = "a check that cWB PE produced the expected data and finished"

    def __init__(self, alert, t0, options, gdb, annotate=False):
        graceid = alert['uid']

        ced_dt = float(options['ced dt'])
        estimate_dt = float(options['estimate dt'])
        skymap_dt = float(options['skymap dt'])
        skymap_tagnames = options['skymap tagnames']
        if skymap_tagnames !=None:
            skymap_tagnames = skymap_tagnames.split()

        email = options['email'].split()

        tasks = [cWBPECEDCheck(ced_dt, email=email),
                 cWBPEEstimateCheck(estimate_dt, email=email),
                 cWBPESkymapCheck(skymap_dt, tagnames=skymap_tagnames, email=email),
#                 cWBPEFinishCheck(timeout, email=email) ### NOT IMPLEMENTED
                ]
        super(CWBPEItem, self).__init__( graceid, 
                                         gdb,
                                         t0,
                                         tasks,
                                         annotate=annotate
                                       )

class cWBPECEDCheck(esUtils.EventSupervisorTask):
    """
    a check that cWB PE posted estimates of parameters
    """
    name = "cWBPECED"
    description = "a check that cWB PE posted a link to a CED page"

    def __init__(self, timeout, email=[]):
        super(cWBPECEDCheck, self).__init__( timeout,
                                                  email=email
                                                )

    def cWBPECED(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that cWB PE posted posterior samples
        """
        if verbose:
            print( "%s : %s"%(graceid, self.description) )

        if not esUtils.check4log( graceid, gdb, "cWB CED", verbose=verbose ):
            self.warning = "found link to cWB CED page"
            if verbose or annotate:
                message = "no action required : "+self.warning
                if verbose:
                    print( "    "+message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )
            return False ### action_required = False

        self.warning = "could not find link to cWB CED page"
        if verbose or annotate:
            message = "action required : "+self.warning
            if verbose:
                print( "    "+self.warning )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )
        return True ### action_required = True

class cWBPEEstimateCheck(esUtils.EventSupervisorTask):
    """
    a check that cWB PE posted estimates of parameters
    """
    name = "cWBPEEstimate"
    description = "a check that cWB PE posted estimates of parameters"

    def __init__(self, timeout, email=[]):
        super(cWBPEEstimateCheck, self).__init__( timeout,
                                                  email=email
                                                )

    def cWBPEEstimate(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that cWB PE posted posterior samples
        """
        if verbose:
            print( "%s : %s"%(graceid, self.description) )

        if not esUtils.check4log( graceid, gdb, "cWB parameter estimation", verbose=verbose ):
            self.warning = "found cWB estimates of parameters"
            if verbose or annotate:
                message = "no action required : "+self.warning
                if verbose:
                    print( "    "+message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )
            return False ### action_required = False

        self.warning = "could not find cWB estimates of parameters"
        if verbose or annotate:
            message = "action required : "+self.warning
            if verbose:
                print( "    "+self.warning )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )
        return True ### action_required = True

class cWBPESkymapCheck(esUtils.EventSupervisorTask):
    """
    a check that cWB PE posted a skymap
    """
    name = "cWBPESkymap"
    description = "a check that cWB PE posted a skymap"

    def __init__(self, timeout, tagnames=None, email=[]):
        self.tagnames = tagnames
        super(cWBPESkymapCheck, self).__init__( timeout,
                                                email=email
                                              )

    def cWBPESkymap(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that cWB PE posted a skymap
        looks for the existence of a skymap and the correct tagnames
        """
        if verbose:
            print( "%s : %s"%(graceid, self.description) )
        fitsname = "skyprobcc_cWB.fits"
        self.warning, action_required = check4file( graceid, gdb, fitsname, tagnames=self.tagnames, verbose=verbose )
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

class cWBPEFinishCheck(esUtils.EventSupervisorTask):
    """
    a check that cWB PE finished
    """
    name = "cWBPEFinish"
    description = "a check that cWB PE finished"

    def __init__(self, timeout, email=[]):
        super(cWBPEFinishCheck, self).__init__( timeout,
                                                email=email
                                              )

    def cWBPEFinish(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that cWB PE finished
        NOT IMPLEMENTED
        """
        raise NotImplementedError(self.name)
        ### NOTE: cWB PE may not have a cannonical "finish" statement and may only report data
        ###       if this is the case, then we should NOT have a finishCheck.

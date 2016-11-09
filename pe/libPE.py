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
    name = "lib pe start"
    description = "a check that LIB PE started"

    def __init__(self, alert, t0, options, gdb, annotate=False):
        graceid = alert['uid']

        timeout = float(options['dt'])
        email = options['email'].split()

        tasks = [libPEStartCheck(timeout, email)]
        super(LIBPEStartItem, self).__init__( graceid,
                                              gdb,
                                              t0,
                                              tasks,
                                              annotate=annotate
                                            )

class libPEStartCheck(esUtils.EventSupervisorTask):
    """
    a check that LIB PE started
    """    
    name = "libPEStart"
    description = "a check that LIB PE started"

    def __init__(self, timeout, email=[]):
        super(libPEStartCheck, self).__init__( timeout,
                                               email=email
                                             )

    def libPEStart(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that LIB PE started
        """
        if verbose:
            print( "%s : %s"%(graceid, self.description) )
        if not esUtils.check4log( graceid, gdb, "LIB Parameter estimation started.", verbose=verbose ):
            self.warning = "found LIB PE starting message"
            if verbose or annotate:
                message = "no action required : "+self.warning
                if verbose:
                    print( "    "+message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )
            return False ### action_required = False

        self.warning = "could not find LIB PE staring message"
        if verbose or annotate:
            message = "action required : "+self.warning
            if verbose:
                print( "    "+self.warning )
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
    name = "lib pe"
    description = "a check that LIB PE produced the expected data and finished"

    def __init__(self, alert, t0, options, gdb, annotate=False):
        graceid = alert['uid']

        postsamp_dt = float(options['post samp dt'])
        bayesFct_dt = float(options['bayes factor dt'])
        skymap_dt = float(options['skymap dt'])
        skymap_tagnames = options['skymap tagnames']
        if skymap_tagnames !=None:
            skymap_tagnames = skymap_tagnames.split()
        finish_dt = float(options['finish dt'])

        email = options['email'].split()

        tasks = [libPEPostSampCheck(postsamp_dt, email=email),
                 libPEBayesFactorsCheck(bayesFct_dt, email=email),
                 libPESkymapCheck(skymap_dt, tagnames=skymap_tagnames, email=email),
                 libPEFinishCheck(finish_dt, email=email)
                ]
        super(LIBPEItem, self).__init__( graceid, 
                                         gdb,
                                         t0,
                                         tasks,
                                         annotate=annotate
                                       )

class libPEPostSampCheck(esUtils.EventSupervisorTask):
    """
    a check that LIB PE posted posterior samples
    """
    name = "libPEPostSamp"
    description = "a check that LIB PE posted posterior samples"

    def __init__(self, timeout, email=[]):
        super(libPEPostSampCheck, self).__init__( timeout,
                                                  email=email
                                                )

    def libPEPostSamp(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that LIB PE posted posterior samples
        NOTE: this is likely associated with the same log message as libPEFinishCheck 
              and it is not clear that we should seprate them as we have...
        """
        if verbose:
            print( "%s : %s"%(graceid, self.description) )
        filename = "posterior_samples.dat"
        self.warning, action_required = check4file( graceid, gdb, fitsname, verbose=verbose )
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

class libPEBayesFactorsCheck(esUtils.EventSupervisorTask):
    """
    a check that LIB PE posted BayesFactors
    """
    name = "libPEBayesFactors"
    description = "a check that LIB PE posted Bayes Factors"

    def __init__(self, timeout, email=[]):
        super(libPEBayesFactorsCheck, self).__init__( timeout,
                                                  email=email
                                                )

    def libPEBayesFactors(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that LIB PE posted Bayes Factors
        """
        if verbose:
            print( "%s : %s"%(graceid, self.description) )

        if not esUtils.check4log( graceid, gdb, "LIB PE summary", verbose=verbose ):
            self.warning = "found LIB PE BayesFactors message"
            if verbose or annotate:
                message = "no action required : "+self.warning
                if verbose:
                    print( "    "+message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )
            return False ### action_required = False

        self.warning = "could not find LIB PE BayesFactors message"
        if verbose or annotate:
            message = "action required : "+self.warning
            if verbose:
                print( "    "+self.warning )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )
        return True ### action_required = True


class libPESkymapCheck(esUtils.EventSupervisorTask):
    """
    a check that LIB PE posted a skymap
    """
    name = "libPESkymap"
    description = "a check that LIB PE posted a skymap"

    def __init__(self, timeout, tagnames=None, email=[]):
        self.tagnames = tagnames
        super(libPESkymapCheck, self).__init__( timeout,
                                                email=email
                                              )

    def libPESkymap(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that LIB PE posted a skymap
        looks for the existence of a skymap and the correct tagnames
        """
        if verbose:
            print( "%s : %s"%(graceid, self.description) )
        fitsname = "LIB_skymap.fits.gz"
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

class libPEFinishCheck(esUtils.EventSupervisorTask):
    """
    a check that LIB PE finished
    """
    name = "libPEFinish"
    description = "a check that LIB PE finished"

    def __init__(self, timeout, email=[]):
        super(libPEFinishCheck, self).__init__( timeout,
                                                email=email
                                              )

    def libPEFinish(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that LIB PE finished
        """
        if verbose:
            print( "%s : %s"%(graceid, self.description) )

        if not esUtils.check4log( graceid, gdb, "LIB Parameter estimation finished.", verbose=verbose ):
            self.warning = "found LIB PE completion message"
            if verbose or annotate:
                message = "no action required : "+self.warning
                if verbose:
                    print( "    "+message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )
            return False ### action_required = False

        self.warning = "could not find LIB PE completion message"
        if verbose or annotate:
            message = "action required : "+self.warning
            if verbose:
                print( "    "+self.warning )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )
        return True ### action_required = True

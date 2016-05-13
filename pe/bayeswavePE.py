description = "a module housing checks of BayesWave-PE functionality"
author = "reed.essick@ligo.org"

#---------------------------------------------------------------------------------------------------

import sys
sys.path.append("../")
import eventSupervisorUtils as esUtils

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
        email
    """
    name = "bayeswave pe start"
    description = "a check that BayesWave PE started"

    def __init__(self, alert, t0, options, gdb, annotate=False):
        graceid = alert['uid']

        timeout = float(options['dt'])
        email = options['email'].split()

        tasks = [bayeswavePEStartCheck(timeout, email)]
        super(BayesWavePEStartItem, self).__init__( graceid,
                                                    gdb,
                                                    t0,
                                                    tasks,
                                                    annotate=annotate
                                                  )

class bayeswavePEStartCheck(esUtils.EventSupervisorTask):
    """
    a check that Bayeswave PE started
    """    
    name = "bayeswavePEStart"
    description = "a check that BayesWave PE started"

    def __init__(self, timeout, email=[]):
        super(bayeswavePEStartCheck, self).__init__( timeout,
                                                     self.libPEStartCheck,
                                                     email=email
                                                   )

    def bayeswavePEStartCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that BayesWave PE started
        """
        if verbose:
            print( "%s : %s"%(graceid, self.description) )
        if not esUtils.check4log( graceid, gdb, "BayesWaveBurst launched", verbose=verbose ):
            self.warning = "found BayesWave PE starting message"
            if verbose or annotate:
                message = "no action required : "+self.warning
                if verbose:
                    print( "    "+message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )
            return False ### action_required = False

        self.warning = "could not find BayesWave PE staring message"
        if verbose or annotate:
            message = "action required : "+self.warning
            if verbose:
                print( "    "+self.warning )
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
        email
    """
    name = "bayeswave pe"
    description = "a check that BayesWave PE produced the expected data and finished"

    def __init__(self, alert, t0, options, gdb, annotate=False):
        graceid = alert['uid']

        postsamp_dt = float(options['post samp dt'])
        estimate_dt = float(options['estimate dt'])
        bayesFct_dt = float(options['bayes factor dt'])
        skymap_dt = float(options['skymap dt'])
        skymap_tagnames = options['skymap tagnames']
        if skymap_tangames !=None:
            skymap_tagnames = skymap_tagnames.split()

        email = options['email'].split()

        tasks = [bayeswavePEPostSampCheck(postsamp_dt, email=email),
                 bayeswavePEEstimateCheck(estimate_dt, email=email),
                 bayeswavePEBayesFactorsCheck(bayesFct_dt, email=email),
                 bayeswavePESkymapCheck(skymap_dt, tagnames=skymap_tagnames, email=email),
#                 bayeswavePEFinishCheck(timeout, email=email) ### NOT IMPLEMENTED
                ]
        super(BayesWavePEItem, self).__init__( graceid, 
                                               gdb,
                                               t0,
                                               tasks,
                                               annotate=annotate
                                             )

class bayeswavePEPostSampCheck(esUtils.EventSupervisorTask):
    """
    a check that BayesWave PE posted posterior samples
    """
    name = "bayeswavePEPostSamp"
    description = "a check that BayesWave PE posted posterior samples"

    def __init__(self, timeout, email=[]):
        super(bayeswavePEPostSampCheck, self).__init__( timeout,
                                                        self.bayeswavePEPostSampCheck,
                                                        email=email
                                                      )

    def bayeswavePEPostSampCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that BayesWave PE posted posterior samples
        """
        if verbose:
            print( "%s : %s"%(graceid, self.description) )

        if not esUtils.check4log( graceid, gdb, "BWB Follow-up results", verbose=verbose ):
            self.warning = "found Bayeswave link to follow-up results"
            if verbose or annotate:
                message = "no action required : "+self.warning
                if verbose:
                    print( "    "+message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )
            return False ### action_required = False

        self.warning = "could not find Bayeswave link to follow-up results"
        if verbose or annotate:
            message = "action required : "+self.warning
            if verbose:
                print( "    "+self.warning )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )
        return True ### action_required = True

class bayeswavePEBayesFactorsCheck(esUtils.EventSupervisorTask):
    """
    a check that BayesWave PE posted Bayes Factors
    """
    name = "bayeswavePEBayesFactors"
    description = "a check that BayesWave PE posted Bayes Factors"

    def __init__(self, timeout, email=[]):
        super(bayeswavePEBayesFactorsCheck, self).__init__( timeout,
                                                        self.bayeswavePEBayesFactorsCheck,
                                                        email=email
                                                      )

    def bayeswavePEBayesFactorsCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that BayesWave PE posted Bayes Factors
        """
        if verbose:
            print( "%s : %s"%(graceid, self.description) )

        if not esUtils.check4log( graceid, gdb, "BWB Bayes Factors", verbose=verbose ):
            self.warning = "found Bayeswave BayesFactors message"
            if verbose or annotate:
                message = "no action required : "+self.warning
                if verbose:
                    print( "    "+message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )
            return False ### action_required = False

        self.warning = "could not find Bayeswave BayesFactors message"
        if verbose or annotate:
            message = "action required : "+self.warning
            if verbose:
                print( "    "+self.warning )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )
        return True ### action_required = True

class bayeswavePEEstimateCheck(esUtils.EventSupervisorTask):
    """
    a check that BayesWave PE posted estimates of parameters
    """
    name = "bayeswavePEEstimate"
    description = "a check that BayesWave PE posted estimates of parameters"

    def __init__(self, timeout, email=[]):
        super(bayeswavePEEstimateCheck, self).__init__( timeout,
                                                        self.bayeswavePEEstimateCheck,
                                                        email=email
                                                      )

    def bayeswavePEBayesFactorsCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that BayesWave PE posted estimates of parameters
        """
        if verbose:
            print( "%s : %s"%(graceid, self.description) )

        if not esUtils.check4log( graceid, gdb, "BWB parameter estimation", verbose=verbose ):
            self.warning = "found Bayeswave BayesFactors message"
            if verbose or annotate:
                message = "no action required : "+self.warning
                if verbose:
                    print( "    "+message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )
            return False ### action_required = False

        self.warning = "could not find Bayeswave BayesFactors message"
        if verbose or annotate:
            message = "action required : "+self.warning
            if verbose:
                print( "    "+self.warning )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )
        return True ### action_required = True

class bayeswavePESkymapCheck(esUtils.EventSupervisorTask):
    """
    a check that BayesWave PE posted a skymap
    """
    name = "bayeswavePESkymap"
    description = "a check that BayesWave PE posted a skymap"

    def __init__(self, timeout, tagnames=None, email=[]):
        self.tagnames = tagnames
        super(bayeswavePESkymapCheck, self).__init__( timeout,
                                                      self.bayeswavePESkymapCheck,
                                                      email=email
                                                    )

    def bayeswavePESkymapCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that BayesWave PE posted a skymap
        """
        if verbose:
            print( "%s : %s"%(graceid, self.description) )
        fitsname = "BW_skymap.fits"
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

class bayeswavePEFinishCheck(esUtils.EventSupervisorTask):
    """
    a check that BayesWave PE finished
    """
    name = "bayeswavePEFinish"
    description = "a check that BayesWave PE finished"

    def __init__(self, timeout, email=[]):
        super(bayeswavePEFinishCheck, self).__init__( timeout,
                                                      self.bayeswavePEFinishCheck,
                                                      email=email
                                                    )

    def bayeswavePEFinishCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that BayesWave PE finished
        NOT IMPLEMENTED
        """
        raise NotImplementedError
        ### NOTE: bayeswave may not report a "finish" statement and instead may only report data
        ###       if this is the case, then we should NOT have a finishCheck.

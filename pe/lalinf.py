description = "a module housing checks of LALInference-PE functionality"
author = "reed.essick@ligo.org"

#---------------------------------------------------------------------------------------------------

import sys
sys.path.append("../")
import eventSupervisorUtils as esUtils

#---------------------------------------------------------------------------------------------------

### methods to identify updates by description

def is_lalinfStart( description ):
    ''' determine whether description is for a lalinference start alert by matching a string fragment '''
    return 'LALInference online estimation started' in description

#---------------------------------------------------------------------------------------------------

class LALInfStartItem(esUtils.EventSupervisorQueueItem):
    """
    a check that LALInference started

    alert:
        graceid
    options:
        dt
        email
    """
    name = "lalinf start"
    description = "a check that LALInference started"

    def __init__(self, alert, t0, options, gdb, annotate=False):
        graceid = alert['uid']

        timeout = float(options['dt'])
        email = options['email'].split()

        tasks = [lalinfStartCheck(timeout, email)]
        super(LALInfStartItem, self).__init__( graceid,
                                               gdb,
                                               t0,
                                               tasks,
                                               annotate=annotate
                                             )

class lalinfStartCheck(esUtils.EventSupervisorTask):
    """
    a check that LALInference started
    """    
    name = "lalinfStart"
    description = "a check that LALInference started"

    def __init__(self, timeout, email=[]):
        super(lalinfStartCheck, self).__init__( timeout,
                                               email=email
                                             )

    def lalinfStart(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that LALInference started
        """
        if verbose:
            print( "%s : %s"%(graceid, self.description) )
        if not esUtils.check4log( graceid, gdb, "LALInference online estimation started", verbose=verbose ):
            self.warning = "found LALInference starting message"
            if verbose or annotate:
                message = "no action required : "+self.warning
                if verbose:
                    print( "    "+message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )
            return False ### action_required = False

        self.warning = "could not find LALInference staring message"
        if verbose or annotate:
            message = "action required : "+self.warning
            if verbose:
                print( "    "+self.warning )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )
        return True ### action_required = True

class LALInfItem(esUtils.EventSupervisorQueueItem):
    """
    a check that LALiInference produces the expected data and finished

    alert:
        graceid
    options:
        post samp dt
        skymap dt
        skymap tagnames
        finish dt
        email
    """
    name = "lalinf"
    description = "a check that LALInference produced the expected data and finished"

    def __init__(self, alert, t0, options, gdb, annotate=False):
        graceid = alert['uid']

        postsamp_dt = float(options['post samp dt'])
        skymap_dt = float(options['skymap dt'])
        skymap_tagnames = options['skymap tagnames']
        if skymap_tagnames !=None:
            skymap_tagnames = skymap_tagnames.split()
        finish_dt = float(options['finish dt'])

        email = options['email'].split()


        tasks = [
                 lalinfPostSampCheck(postsamp_dt, email=email), 
                 lalinfSkymapCheck(skymap_dt, tagnames=skymap_tagnames, email=email),
                 lalinfFinishCheck(finish_dt, email=email)
                ]
        super(LALInfItem, self).__init__( graceid, 
                                          gdb,
                                          t0,
                                          tasks,
                                          annotate=annotate
                                       )

class lalinfPostSampCheck(esUtils.EventSupervisorTask):
    """
    a check that LALInference posted posterior samples
    """
    name = "lalinfPostSamp"
    description = "a check that LALInference posted posterior samples"

    def __init__(self, timeout, email=[]):
        super(lalinfPostSampCheck, self).__init__( timeout,
                                                   email=email
                                                 )

    def lalinfPostSamp(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that LALInference posted posterior samples
        NOT IMPLEMENTED
        """
        raise NotImplementedError("not sure what the posterior_samples filename is for lalinference follow-ups...")

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


class lalinfSkymapCheck(esUtils.EventSupervisorTask):
    """
    a check that LALInference posted a skymap
    """
    name = "lalinfSkymap"
    description = "a check that LALInference posted a skymap"

    def __init__(self, timeout, tagnames=None, email=[]):
        self.tagnames = tagnames
        super(lalinfSkymapCheck, self).__init__( timeout,
                                                 email=email
                                               )

    def lalinfSkymap(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that LALInference posted a skymap
        """
        fitsname = "LALInference_skymap.fits.gz"
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

class lalinfFinishCheck(esUtils.EventSupervisorTask):
    """
    a check that LALInference finished
    """
    name = "lalinfFinish"
    description = "a check that LALInference finished"

    def __init__(self, timeout, email=[]):
        super(lalinfFinishCheck, self).__init__( timeout,
                                                 email=email
                                               )

    def lalinfFinish(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that LALInference finished
        """
        if verbose:
            print( "%s : %s"%(graceid, self.description) )
        if not esUtils.check4log( graceid, gdb, "LALInference online estimation finished", verbose=verbose ):
            self.warning = "found LALInference completion message"
            if verbose or annotate:
                message = "no action required : "+self.warning
                if verbose:
                    print( "    "+message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )
            return False ### action_required = False

        self.warning = "could not find LALInference completion message"
        if verbose or annotate:
            message = "action required : "+self.warning
            if verbose:
                print( "    "+self.warning )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )
        return True ### action_required = True

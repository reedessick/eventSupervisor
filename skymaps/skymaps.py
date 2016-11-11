description = "a module housing checks of skymaps functionality"
author      = "reed.essick@ligo.org"

#---------------------------------------------------------------------------------------------------

import eventSupervisor.eventSupervisorUtils as esUtils

import numpy as np
import healpy as hp

#---------------------------------------------------------------------------------------------------

### methods to identify updates by description

#---------------------------------------------------------------------------------------------------

#-------------------------------------------------
# sanity and formatting
#-------------------------------------------------

class SkymapSanityItem(esUtils.EventSupervisorQueueItem):
    """
    a check for sane and properly formatted skymaps

    alert:
        graceid
        fitsname
    options:
        dt
        email
    """
    name = "skymap sanity"

    def __init__(self, alert, t0, options, gdb, annotate=False, warnings=False, logDir='.'):
        graceid = alert['uid']
        self.fitsname = alert['file']
        self.description = "check sanity and formatting of %s"%self.fitsname

        ### extract parameters from config
        timeout = float(options['dt'])
        email = options['email'].split()

        ### generate tasks
        tasks = [skymapSanityCheck(timeout, self.fitsname, email=email, logDir=logDir)]

        ### wrap up instantiation
        super(SkymapSanityItem, self).__init__( graceid,
                                                gdb,
                                                t0,
                                                tasks,
                                                annotate=annotate,
                                                warnings=warnings,
                                              )

class skymapSanityCheck(esUtils.EventSupervisorTask):
    """
    a check for sane and properly formatted skymaps
    """
    name = "skymapSanity"

    def __init__(self, timeout, fitsname, email=[], logDir='.'):
        self.description = "check sanity and formatting of %s"%fitsname
        self.fitsname = fitsname
        super(skymapSanityCheck, self).__init__( timeout,
                                                 email=email,
                                                 logDir=logDir,
                                               )
    
    def skymapSanity(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        check the skymap for sane and proper formatting
        checks that normalization is correct and that map is in Equatorial (C) coordinates
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag='iQ', graceid=graceid )
            logger.info( "%s : %s"%(graceid, self.description) )
            logger.debug( "downloading %s"%(self.fitsname) )

        ### download the fits file
        file_obj = open(self.fitsname, "w")
        file_obj.write( gdb.files( graceid, self.fitsname ).read() )
        file_obj.close()

        if verbose:
            logger.debug( "checking %s"%(self.fitsname) )
        post, header = hp.read_map( self.fitsname, h=True )
        header = dict(header)

        normed = np.sum(post) == 1.0      ### does it sum to 1?
        coord = header['COORDSYS'] == 'C' ### is it in Equatorial Celestial coordinates?

        if normed and coord:
            self.warning = "%s is properly normalized and in Equatorial coordinates"%self.fitsname
            if verbose or annotate:
                message = "no action required : "+self.warning

                ### post message
                if verbose:
                    logger.debug( message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )

            return False ### action_required = False

        elif normed:
            self.warning = "%s is not in Equatorial coordinates"%self.fitsname
            if verbose or annotate:
                message = "no action required : "+self.warning

                ### post message
                if verbose:
                    logger.debug( message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )

            return True ### action_required = False

        elif coord:
            self.warning = "%s is not properly normalized"%self.fitsname
            if verbose or annotate:
                message = "action required : "+self.warning

                ### post message
                if verbose:
                    logger.debug( message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )

            return True ### action_required = True

        else:
            self.warning = "%s is not properly normalized and is not in Equatorial coordinates"%self.fitsname
            if verbose or annotate:
                message = "action required : "+self.warning

                ### post message
                if verbose:
                    logger.debug( message )
                if annotate:
                    message = "event_supervisor : "+message
                    esUtils.writeGDBLog( gdb, graceid, message )

            return True ### action_required = True

#-------------------------------------------------
# plotting
#-------------------------------------------------

class PlotSkymapItem(esUtils.EventSupervisorQueueItem):
    """
    a check that plotting jobs ran and tagged figures properly

    alert:
        graceid
        fitsname
        tagnames
    options:
        dt
        email
    """
    name = "plot skymap"

    def __init__(self, alert, t0, options, gdb, annotate=False, warnings=False, logDir='.'):
        graceid = alert['uid']
        self.fitsname = alert['file']
        self.tagnames = alert['object']['tagnames']

        self.description = "check plotting jobs for %s"%self.fitsname

        ### extract parameters from config
        timeout = float(options['dt'])
        email = options['email'].split()

        ### generate tasks
        tasks = [plotSkymapCheck(timeout, self.fitsname, self.tagnames, email=email, logDir=logDir)]

        ### wrap up instantiation
        super(PlotSkymapItem, self).__init__( graceid,
                                              gdb,
                                              t0,
                                              tasks,
                                              annotate=annotate,
                                              warnings=warnings,
                                            )

class plotSkymapCheck(esUtils.EventSupervisorTask):
    """
    a check that plotting jobs ran and tagged figures properly
    """
    name = "plotSkymap"

    def __init__(self, timeout, fitsname, tagnames, email=[], logDir='.'):
        self.description = "check sanity and formatting of %s"%fitsname
        self.fitsname = fitsname
        self.tagnames = sorted(tagnames)
        super(plotSkymapCheck, self).__init__( timeout,
                                               email=email,
                                               logDir=logDir,
                                             )

    def plotSkymap(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that plotting jobs ran and tagged figures properly
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag='iQ', graceid=graceid )
            logger.info( "%s : %s"%(graceid, self.description) )

        figname = "%s.png"%(self.fitsname.split('.')[0]) ### NOTE: this may be fragile
        self.warning, action_required = check4file( graceid, gdb, figname, tagnames=self.tagnames, verbose=verbose, logTag=logger.name if verbose else None ) ### loog for the figure

        if verbose or annotate:
            ### format message
            if action_required:
                message = "action required : "+self.warning
            else:
                message = "no action required : "+self.warning

            ### post message
            if verbose:
                logger.debug( "    "+message )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )

        return action_required

#-------------------------------------------------
# skyviewer
#-------------------------------------------------

class SkyviewerItem(esUtils.EventSupervisorQueueItem):
    """
    a check that skyviewer ran and tagged files appropriately

    alert:
        graceid
        fitsname
        tagnames
    options:
        dt
        email
    """
    name = "skyviewer"

    def __init__(self, alert, t0, options, gdb, annotate=False, warnings=False, logDir='.'):
        graceid = alert['uid']
        self.fitsname = alert['file']
        self.tagnames = alert['object']['tagnames']

        self.description = "check plotting jobs for %s"%self.fitsname

        ### extract parameters from config
        timeout = float(options['dt'])
        email = options['email'].split()

        ### generate tasks
        tasks = [skyviewerCheck(timeout, self.fitsname, self.tagnames, email=email, logDir=logDir)]

        ### wrap up instantiation
        super(SkyviewerItem, self).__init__( graceid,
                                             gdb,
                                             t0,
                                             tasks,
                                             annotate=annotate,
                                             warnings=warnings,
                                           )

class skyviewerCheck(esUtils.EventSupervisorTask):
    """
    a check that skyviewer ran and tagged files appropriately
    """
    name = "skyviewer"

    def __init__(self, timeout, fitsname, tagnames, email=[], logDir='.'):
        self.description = "check sanity and formatting of %s"%fitsname
        self.fitsname = fitsname
        self.tagnames = sorted(tagnames)
        super(skyviewerCheck, self).__init__( timeout,
                                              email=email,
                                              logDir=logDir,
                                            )

    def skyviewer(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that plotting jobs ran and tagged figures properly
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag='iQ', graceid=graceid )
            logger.info( "%s : %s"%(graceid, self.description) )
            logger.debug( "retrieving files")

        jsonname = "%s.json"%(self.fitsname.strip(".gz").strip(".fits")) ### NOTE: this may be fragile
        self.warning, action_required = check4file( graceid, gdb, fitsname, tagnames=self.tagnames, verbose=verbose, logTag=logger.name if verbose else None )

        if verbose or annotate:
            ### format message
            if action_required:
                message = "action required : "+self.warning
            else:
                message = "no action required : "+self.warning

            ### post message
            if verbose:
                logger.debug( "    "+message )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )

        return action_required

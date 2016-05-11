description = "a module housing checks of skymaps functionality"
author = "reed.essick@ligo.org"

#---------------------------------------------------------------------------------------------------

import sys
sys.path.append("../")
import eventSupervisorUtils as esUtils

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
    """
    name = "skymap sanity"

    def __init__(self, alert, t0, options, gdb, annotate=False):
        graceid = alert['uid']

        timeout = float(options['dt'])
        email = options['email'].split()

        self.description = "check sanity and formatting of %s"%fitsname
        tasks = [skymapSanityCheck(timeout, fitsname, email=email)]
        super(SkymapSanityItem, self).__init__( graceid,
                                                gdb,
                                                t0,
                                                tasks,
                                                annotate=annotate
                                              )

class skymapSanityCheck(esUtils.EventSupervisorTask):
    """
    a check for sane and properly formatted skymaps
    """
    name = "skymapSanity"

    def __init__(self, timeout, fitsname, email=[]):
        self.description = "check sanity and formatting of %s"%fitsname
        self.fitsname = fitsname
        super(skymapSanityCheck, self).__init__( timeout,
                                                 self.skymapSanityCheck,
                                                 email=email
                                               )
    
    def skymapSanityCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        check the skymap for sane and proper formatting
        checks that normalization is correct and that map is in Equatorial (C) coordinates
        """
        if verbose:
            print( "%s : %s"%(graceid, self.description) )
            print( "    downloading %s"%(self.fitsname) )
        file_obj = open(self.fitsname, "w")
        file_obj.write( gdb.files( graceid, self.fitsname ).read() )
        file_obj.close()

        if verbose:
            print( "    checking %s"%(self.fitsname) )
        post, header = hp.read_map( self.fitsname, h=True )
        header = dict(header)

        normed = np.sum(post) == 1.0
        coord = header['COORDSYS'] == 'C'

        if normed and coord:
            self.warning = "%s is properly normalized and in Equatorial coordinates"%self.fitsname
            if verbose or annotate:
                message = "no action required : "+self.warning
                if verbose:
                    print( "    "+message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )
            return False ### action_required = False

        elif normed:
            self.warning = "%s is not in Equatorial coordinates"%self.fitsname
            if verbose or annotate:
                message = "no action required : "+self.warning
                if verbose:
                    print( "    "+message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )
            return True ### action_required = False

        elif coord:
            self.warning = "%s is not properly normalized"%self.fitsname
            if verbose or annotate:
                message = "action required : "+self.warning
                if verbose:
                    print( "    "+message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )
            return True ### action_required = True

        else:
            self.warning = "%s is not properly normalized and is not in Equatorial coordinates"%self.fitsname
            if verbose or annotate:
                message = "action required : "+self.warning
                if verbose:
                    print( "    "+message )
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
    """
    name = "plot skymap"

    def __init__(self, alert, t0, options, gdb, annotate=False):
        graceid = alert['uid']

        self.fitsname = alert['file']
        self.tagnames = alert['object']['tagnames']

        timeout = float(options['dt'])
        email = options['email'].split()

        self.description = "check plotting jobs for %s"%self.fitsname
        tasks = [plotSkymapCheck(timeout, self.fitsname, self.tagnames, email=email)]
        super(PlotSkymapItem, self).__init__( graceid,
                                               gdb,
                                               t0,
                                               tasks,
                                               annotate=annotate
                                             )

class plotSkymapCheck(esUtils.EventSupervisorTask):
    """
    a check that plotting jobs ran and tagged figures properly
    """
    name = "plotSkymap"

    def __init__(self, timeout, fitsname, tagnames, email=[]):
        self.description = "check sanity and formatting of %s"%fitsname
        self.fitsname = fitsname
        self.tagnames = sorted(tagnames)
        super(plotSkymapCheck, self).__init__( timeout,
                                               self.plotSkymapCheck,
                                               email=email
                                             )

    def plotSkymapCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that plotting jobs ran and tagged figures properly
        """
        if verbose:
            print( "%s : %s"%(graceid, self.description) )

        figname = "%s.png"%(self.fitsname.split('.')[0])
        self.warning, action_required = check4file( graceid, gdb, figname, tagnames=self.tagnames, verbose=verbose )
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
# skyviewer
#-------------------------------------------------

class SkyviewerItem(esUtils.EventSupervisorQueueItem):
    """
    a check that skyviewer ran and tagged files appropriately
    """
    name = "skyviewer"

    def __init__(self, alert, t0, options, gdb, annotate=False):
        graceid = alert['uid']

        self.fitsname = alert['file']
        self.tagnames = alert['object']['tagnames']

        timeout = float(options['dt'])
        email = options['email'].split()

        self.description = "check plotting jobs for %s"%self.fitsname
        tasks = [skyviewerCheck(timeout, self.fitsname, self.tagnames, email=email)]
        super(PlotSkymapItem, self).__init__( graceid,
                                               gdb,
                                               t0,
                                               tasks,
                                               annotate=annotate
                                             )

class skyviewerCheck(esUtils.EventSupervisorTask):
    """
    a check that skyviewer ran and tagged files appropriately
    """
    name = "skyviewer"

    def __init__(self, timeout, fitsname, tagnames, email=[]):
        self.description = "check sanity and formatting of %s"%fitsname
        self.fitsname = fitsname
        self.tagnames = sorted(tagnames)
        super(skyviewerCheck, self).__init__( timeout,
                                              self.skyviewerCheck,
                                              email=email
                                            )

    def skyviewerCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that plotting jobs ran and tagged figures properly
        """
        if verbose:
            print( "%s : %s"%(graceid, self.description) )
            print( "    retrieving files")
        files = gdb.files( graceid ).json().keys()

        jsonname = "%s.json"%(self.fitsname.strip(".gz").strip(".fits"))
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

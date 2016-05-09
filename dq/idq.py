description = "a module housing checks of iDQ functionality"
author = "reed.essick@ligo.org"

#---------------------------------------------------------------------------------------------------

import sys
sys.path.append("../")
import eventSupervisorUtils as esUtils

#---------------------------------------------------------------------------------------------------

#---
# start statement
#---
class IDQStartItem(esUtils.EventSupervisorQueueItem):
    """
    a check that iDQ started as expected
    """
    
    def __init__(self, graceid, gdb, t0, timeout, ifo, annotate=False, email=[]):
        self.ifo = ifo
        self.description = "a check that iDQ GraceDB follow-up started as expected at %s"%(self.ifo)
        tasks = [idqStartCheck(timeout, ifo, email=email)]
        super(IDQStartItem, self).__init__( graceid,
                                            gdb,
                                            t0,
                                            tasks,
                                            description=self.description,
                                            annotate=annotate
                                          )     

class idqStartCheck(esUtils.EventSupervisorTask):
    """
    a check that iDQ started as expected
    """
    name = "idqStartCheck"

    def __init__(self, timeout, ifo, email=[]):
        self.ifo = ifo
        self.description = "a check that iDQ GraceDB follow-up started as expected at %s"%(self.ifo)
        super(idqStartCheck, self).__init__( timeout,
                                             self.idqStartCheck,
                                             name=self.name,
                                             description=self.description,
                                             email=email
                                           )

    def idqStartCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that iDQ started as expected
        """
        if verbose:
            print( "%s : %s"%(graceid, self.description) )
        template = "Started searching for iDQ information within [(.*), (.*)] at %s"%(self.ifo)
        if not esUtils.check4log( graceid, gdb, template, verbose=verbose, regex=True ):
            self.warning = "found iDQ starting message at %s"%(self.ifo)
            if verbose or annotate:
                message = "no action required : "+self.warning
                if verbose:
                    print( "    "+message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )
            return False ### action_required = False

        self.warning = "could not find iDQ staring message at %s"%(self.ifo)
        if verbose or annotate:
            message = "action required : "+self.warning
            if verbose:
                print( "    "+self.warning )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )
        return True ### action_required = True

#---
# bulk of the iDQ follow-up
#---
class IDQItem(esUtils.EventSupervisorQueueItem):
    """
    a check that iDQ reported information as expected
    """

    def __init__(self, graceid, gdb, t0, timeout, ifo, classifier, annotate=False, email=[]):
        self.ifo = ifo
        self.classifier = classifier
        description = "a check that iDQ reported information as expected for %s at %s"%(self.classifier, self.ifo)
        tasks = [idqGlitchFAPCheck(timeout, ifo, classifier, email=email),
                 idqFAPFrameCheck(timeout, ifo, classifier, email=email),
                 idqRankFrameCheck(timeout, ifo, classifier, email=email),
                 idqTimeseriesPlotCheck(timeout, ifo, classifier, email=email),
                 idqActiveChanCheck(timeout, ifo, classifier, email=email),
                 idqActiveChanPlotCheck(timeout, ifo, classifier, email=email),
                 idqTablesCheck(timeout, ifo, classifier, email=email),
                 idqCalibrationCheck(timeout, ifo, classifier, email=email),
                 idqCalibrationPlotCheck(timeout, ifo, classifier, email=email),
                 idqROCCheck(timeout, ifo, classifier, email=email),
                 idqROCPlotCheck(timeout, ifo, classifier, email=email),
                 idqCalibStatsCheck(timeout, ifo, classifier, email=email),
                 idqTrainStatsCheck(timeout, ifo, classifier, email=email),
                 idqFinishCheck(timeout, ifo, email=email)
                ]
        super(IDQItem, self).__init__( graceid,
                                       gdb,
                                       t0,
                                       tasks,
                                       description=self.description,
                                       annotate=annotate
                                     )

#---
# reported by laldetchar-idq-gdb-timeseries.py
#---

class idqGlichFAPCheck(esUtils.EventSupervisorTask):
    """
    a check that iDQ reported the glitch-FAP as expected
    """
    name = "idqGlitchFAPCheck"

    def __init__(self, timeout, ifo, classifier, email=[]):
        self.ifo = ifo
        self.classifier = classifier
        self.description = "a check that iDQ reported a glitch-FAP for %s at %s"%(self.classifier, self.ifo)
        super(idqGlitchFAPCheck, self).__init__( timeout,
                                                 self.idqGlitchFAPCheck,
                                                 name=self.name,
                                                 description=self.description,
                                                 email=email
                                               )

    def idqGlitchFAPCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that iDQ reported the gltich-FAP as expected
        """
        if verbose:
            print( "%s : %s"%(graceid, self.description) )
        jsonname = "%s_%s(.*)-(.*)-(.*).json"%(self.ifo, self.classifier)
        fragment = "minimum glitch-FAP for %s at %s within [(.*), (.*)] is (.*)"%(self.classifier, self.ifo)
        self.warning, action_required = check4file( graceid, 
                                                    gdb, 
                                                    jsonname, 
                                                    regex=True,
                                                    tagnames=self.tagnames, 
                                                    verbose=verbose, 
                                                    logFragment=fragment, 
                                                    logRegex=True 
                                                  )
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

class idqFAPFrameCheck(esUtils.EventSupervisorTask):
    """
    check that iDQ uploads fap timeseries files
    """
    name = "idqFAPFrameCheck"

    def __init__(self, timeout, ifo, classifier, email=[]):
        self.ifo = ifo
        self.classifier = classifier
        self.description = "a check that iDQ uploads fap timeseries frames for %s at %s"%(self.classifier, self.ifo)
        super(idqFAPFrameCheck, self).__init__( timeout,
                                                self.idqFAPFrameCheck,
                                                name=self.name,
                                                description=self.description,
                                                email=email
                                              )

    def idqFAPFrameCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        check that iDQ uploads fap timeseries files
        """
        if verbose:
            print( "%s : %s"%(graceid, self.description) )
        framename = "%s_idq_%s_fap(.*)-(.*)-(.*).gwf"%(self.ifo, self.classifier)
        fragment = "iDQ fap timeseries for %s at %s within [(.*), (.*)] :"%(self.classifier, self.ifo)
        self.warning, action_required = check4file( graceid, 
                                                    gdb, 
                                                    framename, 
                                                    regex=True, 
                                                    tagnames=self.tagnames, 
                                                    verbose=verbose, 
                                                    logFragment=fragment, 
                                                    logRegex=True 
                                                  )
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

class idqRankFrameCheck(esUtils.EventSupervisorTask):
    """
    check that iDQ uploaded rank timeseries files
    """
    name = "idqRankFrameCheck"

    def __init__(self, timeout, ifo, classifier, email=[]):
        self.ifo = ifo
        self.classifier = classifier
        self.description = "a check that iDQ uploads rank timeseries frames for %s at %s"%(self.classifier, self.ifo)
        super(idqRankFrameCheck, self).__init__( timeout,
                                                self.idqRankFrameCheck,
                                                name=self.name,
                                                description=self.description,
                                                email=email
                                              )

    def idqRankFrameCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        check that iDQ uploads rank timeseries files
        """
        if verbose:
            print( "%s : %s"%(graceid, self.description) )
        framename = "%s_idq_%s_rank(.*)-(.*)-(.*).gwf"%(self.ifo, self.classifier)
        fragment = "iDQ glitch-rank frame for %s at %s within [(.*), (.*)] :"%(self.classifier, self.ifo)
        self.warning, action_required = check4file( graceid,
                                                    gdb,
                                                    framename,
                                                    regex=True,
                                                    tagnames=self.tagnames,
                                                    verbose=verbose,
                                                    logFragment=fragment,
                                                    logRegex=True
                                                  )
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

class idqTimeseriesPlotCheck(esUtils.EventSupervisorTask):
    """
    a check that iDQ reported timeseries plot as expected
    """
    name = "idqTimeseriesPlotCheck"

    def __init__(self, timeout, ifo, classifier, email=[]):
        self.ifo = ifo
        self.classifier = classifier
        self.description = "a check that iDQ reproted timeseries information as expected for %s at %s"%(self.classifier, self.ifo)
        super(idqTimeseriesPlotCheck, self).__init__( timeout,
                                                      self.idqTimeseriesPlotCheck,
                                                      name=self.name,
                                                      description=self.description,
                                                      email=email
                                                    )

    def idqTimeseriesPlotCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that iDQ reported timeseries information as expected
        """
        if verbose:
            print( "%s : %s"%(graceid, self.description) )
        figname = "%s_%s(.*)_timeseries-(.*)-(.*).png"%(self.ifo, self.classifier)
        fragment = "iDQ fap and glitch-rank timeseries plot for %s at %s:"%(self.classifier, self.ifo)
        self.warning, action_required = check4file( graceid,
                                                    gdb,
                                                    figname,
                                                    regex=True,
                                                    tagnames=self.tagnames,
                                                    verbose=verbose,
                                                    logFragment=fragment,
                                                    logRegex=True
                                                  )
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

class idqActiveChanCheck(esUtils.EventSupervisorTask):
    """
    check that iDQ uploaded a list of possible active channels
    """
    name = "idqActiveChanCheck"

    def __init__(self, timeout, ifo, classifier, email=[]):
        self.ifo = ifo
        self.classifier = classifier
        self.description = "a check that iDQ uploads a list of possible active channels for %s at %s"%(self.classifier, self.ifo)
        super(idqActiveChanCheck, self).__init__( timeout, 
                                                  self.idqActiveChanCheck,
                                                  name=self.name,
                                                  description=self.description,
                                                  email=email
                                                )

    def idqActiveChanCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        check that iDQ uploaded a list of possible active channels
        """
        if verbose:
            print( "%s : %s"%(graceid, self.description) )
        jsonname = "%s_%s_chanlist(.*)-(.*)-(.*).json"%(self.ifo, self.classifier)
        fragment = "iDQ (possible) active channels for %s at %s"%(self.classifier, self.ifo)
        self.warning, action_required = check4file( graceid,
                                                    gdb,
                                                    jsonname,
                                                    regex=True,
                                                    tagnames=self.tagnames,
                                                    verbose=verbose,
                                                    logFragment=fragment,
                                                    logRegex=False
                                                  )
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

class idqActiveChanPlotCheck(esUtils.EventSupervisorTask):
    """
    check that iDQ uploaded a plot of the possibly active channels
    """
    name = "idqActiveChanPlotCheck"

    def __init__(self, timeout, ifo, classifier, email=[]):
        self.ifo = ifo
        self.classifier = classifier
        self.description = "a check that iDQ uploads a plot of possible active channels for %s at %s"%(self.classifier, self.ifo)
        super(idqActiveChanPlotCheck, self).__init__( timeout,
                                                      self.idqActiveChanPlotCheck,
                                                      name=self.name,
                                                      description=self.description,
                                                      email=email
                                                    )

    def idqActiveChanPlotCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        check that iDQ uploaded a plot of possible active channels
        """
        if verbose:
            print( "%s : %s"%(graceid, self.description) )
        figname = "%s_%s(.*)_chanstrip-(.*)-(.*).%s"%(self.ifo, self.classifier)
        fragment = "iDQ channel strip chart for %s at %s"%(self.classifier, self.ifo)
        self.warning, action_required = check4file( graceid,
                                                    gdb,
                                                    figname,
                                                    regex=True,
                                                    tagnames=self.tagnames,
                                                    verbose=verbose,
                                                    logFragment=fragment,
                                                    logRegex=False
                                                  )
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

#---
# reported by laldetchar-idq-gdb-glitch-tables.py
#---
class idqTablesCheck(esUtils.EventSupervisorTask):
    """
    a check that iDQ reported the xml tables as expected
    """
    name = "idqTablesCheck"

    def __init__(self, timeout, ifo, classifier, email=[]):
        self.ifo = ifo
        self.classifier = classifier
        self.description = "a check that iDQ reported the xml tables as expected for %s at %s"%(self.classifier, self.ifo)
        super(idqTablesCheck, self).__init__( timeout,
                                              self.idqTablesCheck,
                                              name=self.name,
                                              description=self.description,
                                              email=email
                                            ) 

    def idqTablesCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that iDQ reported the xml tables as expected
        """
        if verbose:
            print( "%s : %s"%(graceid, self.description) )
        filename = "%s_idq_%s(.*)-(.*)-(.*).xml.gz"%(self.ifo, self.classifier)
        fragment = "iDQ glitch tables %s:"%(self.ifo) ### this is bad... but it's what we have at the moment within iDQ
        self.warning, action_required = check4file( graceid,
                                                    gdb,
                                                    filename,
                                                    regex=True,
                                                    tagnames=self.tagnames,
                                                    verbose=verbose,
                                                    logFragment=fragment,
                                                    logRegex=False
                                                  )
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

#---
# reported by laldetchar-idq-local-performance.py
#---
class idqCalibrationCheck(esUtils.EventSupervisorTask):
    """
    a check that iDQ reported historical calibration as expected
    """
    name = "idqCalibrationCheck"

    def __init__(self, timeout, ifo, classifier, email=[]):
        self.ifo = ifo
        self.classifier = classifier
        self.description = "a check that iDQ reported the calibration data as expected for %s at %s"%(self.classifier, self.ifo)
        super(idqCalibrationCheck, self).__init__( timeout, 
                                                   self.idqCalibrationCheck,
                                                   name=self.name,
                                                   description=self.description,
                                                   email=email
                                                 )

    def idqCalibrationCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that iDQ reported preformance metrics as expected
        """
        if verbose:
            print( "%s : %s"%(graceid, self.description) )
        jsonname = "%s_%s(.*)_calib-(.*)-(.*).json"%(self.ifo, self.classifier)
        fragment = "iDQ calibration sanity check for %s at %s"%(self.classifier, self.ifo)
        self.warning, action_required = check4file( graceid,
                                                    gdb,
                                                    jsonname,
                                                    regex=True,
                                                    tagnames=self.tagnames,
                                                    verbose=verbose,
                                                    logFragment=fragment,
                                                    logRegex=False
                                                  )
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

class idqCalibrationPlotCheck(esUtils.EventSupervisorTask):
    """
    a check that iDQ reported historical calibration plot as expected
    """
    name = "idqCalibrationPlotCheck"

    def __init__(self, timeout, ifo, classifier, email=[]):
        self.ifo = ifo
        self.classifier = classifier
        self.description = "a check that iDQ reported the calibration plot as expected for %s at %s"%(self.classifier, self.ifo)
        super(idqCalibrationPlotCheck, self).__init__( timeout,
                                                       self.idqCalibrationPlotCheck,
                                                       name=self.name,
                                                       description=self.description,
                                                       email=email
                                                     )

    def idqCalibrationPlotCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that iDQ reported preformance metrics as expected
        """
        if verbose:
            print( "%s : %s"%(graceid, self.description) )
        figname = "%s_%s(.*)_calib-(.*)-(.*).png"%(self.ifo, self.classifier)
        fragment = "iDQ calibration sanity check figure for %s at %s"%(self.classifier, self.ifo)
        self.warning, action_required = check4file( graceid,
                                                    gdb,
                                                    figname,
                                                    regex=True,
                                                    tagnames=self.tagnames,
                                                    verbose=verbose,
                                                    logFragment=fragment,
                                                    logRegex=False
                                                  )
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

class idqROCCheck(esUtils.EventSupervisorTask):
    """
    a check that iDQ reported the local ROC data
    """
    name = "idqROCCheck"

    def __init__(self, timeout, ifo, classifier, email=[]):
        self.ifo = ifo
        self.classifier = classifier
        self.description = "a check that iDQ reported the ROC data as expected for %s at %s"%(self.classifier, self.ifo)
        super(idqROCCheck, self).__init__( timeout,
                                           self.idqROCCheck,
                                           name=self.name,
                                           description=self.description,
                                           email=email
                                         )

    def idqROCCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that iDQ reported preformance metrics as expected
        """
        if verbose:
            print( "%s : %s"%(graceid, self.description) )
        jsonname = "%s_%s(.*)_ROC-(.*)-(.*).json"%(self.ifo, self.classifier)
        fragment = "iDQ local ROC curves for %s at %s"%(self.classifier, self.ifo)
        self.warning, action_required = check4file( graceid,
                                                    gdb,
                                                    jsonname,
                                                    regex=True,
                                                    tagnames=self.tagnames,
                                                    verbose=verbose,
                                                    logFragment=fragment,
                                                    logRegex=False
                                                  )
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

class idqROCPlotCheck(esUtils.EventSupervisorTask):
    """
    a check that iDQ reported the local ROC plot
    """
    name = "idqROCPlotCheck"

    def __init__(self, timeout, ifo, classifier, email=[]):
        self.ifo = ifo
        self.classifier = classifier
        self.description = "a check that iDQ reported the ROC plot as expected for %s at %s"%(self.classifier, self.ifo)
        super(idqROCPlotCheck, self).__init__( timeout,
                                               self.idqROCPlotCheck,
                                               name=self.name,
                                               description=self.description,
                                               email=email
                                             )

    def idqROCPlotCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that iDQ reported preformance metrics as expected
        """
        if verbose:
            print( "%s : %s"%(graceid, self.description) )
        figname = "%s_%s(.*)_ROC-(.*)-(.*).png"%(self.ifo, self.classifier)
        fragment = "iDQ local ROC figure for %s at %s"%(self.classifier, self.ifo)
        self.warning, action_required = check4file( graceid,
                                                    gdb,
                                                    figname,
                                                    regex=True,
                                                    tagnames=self.tagnames,
                                                    verbose=verbose,
                                                    logFragment=fragment,
                                                    logRegex=False
                                                  )
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

class idqCalibStatsCheck(esUtils.EventSupervisorTask):
    """
    a check that iDQ uploaded statistics about when calibration took place
    """
    name = "idqCalibStatsCheck"

    def __init__(self, timeout, ifo, classifier, email=[]):
        self.ifo = ifo
        self.classifier = classifier
        self.description = "a check that iDQ reported the calibration statistics as expected for %s at %s"%(self.classifier, self.ifo)
        super(idqCalibStatsCheck, self).__init__( timeout,
                                                  self.idqCalibStatsCheck,
                                                  name=self.name,
                                                  description=self.description,
                                                  email=email
                                                )

    def idqCalibStatsCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that iDQ reported preformance metrics as expected
        """
        if verbose:
            print( "%s : %s"%(graceid, self.description) )
        jsonname = "%s_%s(.*)_calibStats-(.*)-(.*).json"%(self.ifo, self.classifier)
        fragment = "iDQ local calibration vital statistics for %s at %s"%(self.classifier, self.ifo)
        self.warning, action_required = check4file( graceid,
                                                    gdb,
                                                    jsonname,
                                                    regex=True,
                                                    tagnames=self.tagnames,
                                                    verbose=verbose,
                                                    logFragment=fragment,
                                                    logRegex=False
                                                  )
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

class idqTrainStatsCheck(esUtils.EventSupervisorTask):
    """
    a check that iDQ uploaded statistics about when training took place
    """
    name = "idqTrainStatsCheck"

    def __init__(self, timeout, ifo, classifier, email=[]):
        self.ifo = ifo
        self.classifier = classifier
        self.description = "a check that iDQ reported the training statistics as expected for %s at %s"%(self.classifier, self.ifo)
        super(idqTrainStatsCheck, self).__init__( timeout,
                                                  self.idqTrainStatsCheck,
                                                  name=self.name,
                                                  description=self.description,
                                                  email=email
                                                )

    def idqTrainStatsCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that iDQ reported preformance metrics as expected
        """
        if verbose:
            print( "%s : %s"%(graceid, self.description) )
        jsonname = "%s_%s(.*)_trainStats-(.*)-(.*).json"%(self.ifo, self.classifier)
        fragment = "iDQ local training vital statistics for %s at %s"%(self.classifier, self.ifo)
        self.warning, action_required = check4file( graceid,
                                                    gdb,
                                                    jsonname,
                                                    regex=True,
                                                    tagnames=self.tagnames,
                                                    verbose=verbose,
                                                    logFragment=fragment,
                                                    logRegex=False
                                                  )
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

#---
# finish statement
#---
class idqFinishCheck(esUtils.EventSupervisorTask):
    """
    a check that iDQ finished as expected
    """
    name = "idqFinishCheck"

    def __init__(self, timeout, ifo, email=[]):
        self.ifo = ifo
        self.description = "a check that iDQ finished reporting as expected at %s"%(self.ifo)
        super(idqFinishCheck, self).__init__( timeout,
                                              self.idqFinishCheck,
                                              name=self.name,
                                              description=self.description,
                                              email=email
                                            )

    def idqFinishCheck(self, graceid, gdb, verbose=False, annoate=False):
        """
        a check that iDQ finished as expected
        """
        if verbose:
            print( "%s : %s"%(graceid, self.description) )
        template = "Finished searching for iDQ information within [(.*), (.*)] at %s"%(self.ifo)
        if not esUtils.check4log( graceid, gdb, template, verbose=verbose, regex=True ):
            self.warning = "found iDQ completion message at %s"%(self.ifo)
            if verbose or annotate:
                message = "no action required : "+self.warning
                if verbose:
                    print( "    "+message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )
            return False ### action_required = False

        self.warning = "could not find iDQ completion message at %s"%(self.ifo)
        if verbose or annotate:
            message = "action required : "+self.warning
            if verbose:
                print( "    "+self.warning )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )
        return True ### action_required = True


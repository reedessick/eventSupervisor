description = "a module housing checks of iDQ functionality"
author      = "reed.essick@ligo.org"

#---------------------------------------------------------------------------------------------------

import eventSupervisor.eventSupervisorUtils as esUtils

#---------------------------------------------------------------------------------------------------

### methods to identify updates by description

def is_idqStart( description ):
    ''' identify whether the description is for an idq start alert based on matching a string fragment '''
    return "Started searching for iDQ information within" in description

def is_idqGlitchFAP( description ):
    ''' identify whether the description is for an idq glitchFAP alert based on matching a string fragment '''
    return "minimum glitch-FAP for" in description

def is_idqActiveChan( description ):
    ''' identify whether the description is for an idq active channel alert based on matching a string fragment '''
    return "iDQ (possible) active channels for" in description

#---------------------------------------------------------------------------------------------------

#---
# start statement
#---
class IDQStartItem(esUtils.EventSupervisorQueueItem):
    """
    a check that iDQ started as expected

    alert:
        graceid
    options:
        ifos
        dt
        email
    """
    name = "idq start"
 
    def __init__(self, alert, t0, options, gdb, annotate=False, warnings=False, logDir='.', logTag='iQ'):
        graceid = alert['uid']

        ### extract params
        self.ifos = options['ifos'].split()

        timeout = float(options['dt'])
        email = options['email'].split()

        self.description = "a check that iDQ GraceDB follow-up started as expected at (%s)"%(",".join(self.ifos))

        ### generate tasks
        taskTag = '%s.%s'%(logTag, self.name)
        tasks = [ idqStartCheck(timeout, ifo, email=email, logDir=logDir, logTag=taskTag) for ifo in self.ifos ]

        ### wrap up instantiation
        super(IDQStartItem, self).__init__( graceid,
                                            gdb,
                                            t0,
                                            tasks,
                                            annotate=annotate,
                                            warnings=warnings,
                                            logDir=logDir,
                                            logTag=logTag,
                                          )     

class idqStartCheck(esUtils.EventSupervisorTask):
    """
    a check that iDQ started as expected
    """
    name = "idqStart"

    def __init__(self, timeout, ifo, email=[], logDir='.', logTag='iQ'):
        self.ifo = ifo
        self.description = "a check that iDQ GraceDB follow-up started as expected at %s"%(self.ifo)
        super(idqStartCheck, self).__init__( timeout,
                                             email=email,
                                             logDir=logDir,
                                             logTag=logTag,
                                           )

    def idqStart(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that iDQ started as expected
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag )
            logger.info( "%s : %s"%(graceid, self.description) )

        template = "Started searching for iDQ information within [(.*), (.*)] at %s"%(self.ifo)
        if not esUtils.check4log( graceid, gdb, template, verbose=verbose, regex=True, logTag=logger.name if verbose else None ): ### look for log message
            self.warning = "found iDQ starting message at %s"%(self.ifo)

            if verbose or annotate:
                message = "no action required : "+self.warning

                ### post message
                if verbose:
                    logger.debug( message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )

            return False ### action_required = False

        self.warning = "could not find iDQ starting message at %s"%(self.ifo)
        if verbose or annotate:
            message = "action required : "+self.warning

            ### post message
            if verbose:
                logger.debug( message )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )

        return True ### action_required = True

#---
# bulk of the iDQ follow-up
#---
class IDQItem(esUtils.EventSupervisorQueueItem):
    """
    a check that iDQ reported information as expected

    alert:
        graceid
        ifo
    options:
        tables dt
        glitch fap dt
        fap frame dt
        rank frame dt
        timeseries dt
        active chan dt
        active chan plot dt
        calib dt
        calib plot dt
        roc dt
        roc plot dt
        calib stats dt
        train stats dt
        finish dt
        email
    """
    name = "idq"

    def __init__(self, alert, t0, options, gdb, annotate=False, warnings=False, logDir='.', logTag='iQ'):
        graceid = alert['uid']
        self.ifo = alert['description'].split()[-1] ### assume a particular format for the log comment
                                                       ### this is based off iDQ start messages from a single IFO

        ### extract parameters from config
        self.classifiers = options['classifiers'].split()

        tables_dt           = float(options['tables dt'])
        glitch_fap_dt       = float(options['glitch fap dt'])
        fap_frame_dt        = float(options['fap frame dt'])
        rank_frame_dt       = float(options['rank frame dt'])
        timeseries_plot_dt  = float(options['timeseries plot dt'])
        active_chan_dt      = float(options['active chan dt'])
        active_chan_plot_dt = float(options['active chan plot dt'])
        calib_dt            = float(options['calib dt'])
        calib_plot_dt       = float(options['calib plot dt'])
        roc_dt              = float(options['roc dt'])
        roc_plot_dt         = float(options['roc plot dt'])
        calib_stats_dt      = float(options['calib stats dt'])
        train_stats_dt      = float(options['train stats dt'])
        finish_dt           = float(options['finish dt'])

        email = options['email'].split()

        self.description = "a check that iDQ reported information as expected for (%s) at %s"%(",".join(self.classifiers), self.ifo)

        ### generate tasks
        taskTag = '%s.%s'%(logTag, self.name)
        tasks = []
        for classifier in self.classifiers:
            tasks += [idqGlitchFAPCheck(glitch_fap_dt, self.ifo, classifier, email=email, logDir=logDir, logTag=taskTag),
                      idqFAPFrameCheck(fap_frame_dt, self.ifo, classifier, email=email, logDir=logDir, logTag=taskTag),
                      idqRankFrameCheck(rank_frame_dt, self.ifo, classifier, email=email, logDir=logDir, logTag=taskTag),
                      idqTimeseriesPlotCheck(timeseries_plot_dt, self.ifo, classifier, email=email, logDir=logDir, logTag=taskTag),
                      idqActiveChanCheck(active_chan_dt, self.ifo, classifier, email=email, logDir=logDir, logTag=taskTag),
                      idqActiveChanPlotCheck(active_chan_plot_dt, self.ifo, classifier, email=email, logDir=logDir, logTag=taskTag),
                      idqTablesCheck(tables_dt, self.ifo, classifier, email=email, logDir=logDir, logTag=taskTag),
                      idqCalibrationCheck(calib_dt, self.ifo, classifier, email=email, logDir=logDir, logTag=taskTag),
                      idqCalibrationPlotCheck(calib_plot_dt, self.ifo, classifier, email=email, logDir=logDir, logTag=taskTag),
                      idqROCCheck(roc_dt, self.ifo, classifier, email=email, logDir=logDir, logTag=taskTag),
                      idqROCPlotCheck(roc_plot_dt, self.ifo, classifier, email=email, logDir=logDir, logTag=taskTag),
                      idqCalibStatsCheck(calib_stats_dt, self.ifo, classifier, email=email, logDir=logDir, logTag=taskTag),
                      idqTrainStatsCheck(train_stats_dt, self.ifo, classifier, email=email, logDir=logDir, logTag=taskTag)
                     ]
        tasks.append( idqFinishCheck(finish_dt, self.ifo, email=email, logDir=logDir, logTag=taskTag) )

        ### wrap up instantiation
        super(IDQItem, self).__init__( graceid,
                                       gdb,
                                       t0,
                                       tasks,
                                       annotate=annotate,
                                       warnings=warnings,
                                       logDir=logDir,
                                       logTag=logTag,
                                     )

#---
# reported by laldetchar-idq-gdb-timeseries.py
#---

class idqGlitchFAPCheck(esUtils.EventSupervisorTask):
    """
    a check that iDQ reported the glitch-FAP as expected
    """
    name = "idqGlitchFAP"

    def __init__(self, timeout, ifo, classifier, email=[], logDir='.', logTag='iQ'):
        self.ifo = ifo
        self.classifier = classifier
        self.description = "a check that iDQ reported a glitch-FAP for %s at %s"%(self.classifier, self.ifo)
        super(idqGlitchFAPCheck, self).__init__( timeout,
                                                 email=email,
                                                 logDir=logDir,
                                                 logTag=logTag,
                                               )

    def idqGlitchFAP(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that iDQ reported the gltich-FAP as expected
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag )
            logger.info( "%s : %s"%(graceid, self.description) )
        jsonname = "%s_%s(.*)-(.*)-(.*).json"%(self.ifo, self.classifier) ### NOTE: this may be fragile
        fragment = "minimum glitch-FAP for %s at %s within [(.*), (.*)] is (.*)"%(self.classifier, self.ifo) ### NOTE: this may be fragile
        self.warning, action_required = esUtils.check4file( graceid, 
                                                    gdb, 
                                                    jsonname, 
                                                    regex=True,
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

class idqFAPFrameCheck(esUtils.EventSupervisorTask):
    """
    check that iDQ uploads fap timeseries files
    """
    name = "idqFAPFrame"

    def __init__(self, timeout, ifo, classifier, email=[], logDir='.', logTag='iQ'):
        self.ifo = ifo
        self.classifier = classifier
        self.description = "a check that iDQ uploads fap timeseries frames for %s at %s"%(self.classifier, self.ifo)
        super(idqFAPFrameCheck, self).__init__( timeout,
                                                email=email,
                                                logDir=logDir,
                                                logTag=logTag,
                                              )

    def idqFAPFrame(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        check that iDQ uploads fap timeseries files
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag )
            logger.info( "%s : %s"%(graceid, self.description) )
        framename = "%s_idq_%s_fap(.*)-(.*)-(.*).gwf"%(self.ifo, self.classifier) ### NOTE: this may be fragile
        fragment = "iDQ fap timeseries for %s at %s within [(.*), (.*)] :"%(self.classifier, self.ifo) ### NOTE: this may be fragile
        self.warning, action_required = esUtils.check4file( graceid, 
                                                    gdb, 
                                                    framename, 
                                                    regex=True, 
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

class idqRankFrameCheck(esUtils.EventSupervisorTask):
    """
    check that iDQ uploaded rank timeseries files
    """
    name = "idqRankFrame"

    def __init__(self, timeout, ifo, classifier, email=[], logDir='.', logTag='iQ'):
        self.ifo = ifo
        self.classifier = classifier
        self.description = "a check that iDQ uploads rank timeseries frames for %s at %s"%(self.classifier, self.ifo)
        super(idqRankFrameCheck, self).__init__( timeout,
                                                email=email,
                                                logDir=logDir,
                                                logTag=logTag,
                                              )

    def idqRankFrame(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        check that iDQ uploads rank timeseries files
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag ) 
            logger.info( "%s : %s"%(graceid, self.description) )
        framename = "%s_idq_%s_rank(.*)-(.*)-(.*).gwf"%(self.ifo, self.classifier) ### NOTE: this may be fragile
        fragment = "iDQ glitch-rank frame for %s at %s within [(.*), (.*)] :"%(self.classifier, self.ifo) ### NOTE: this may be fragile
        self.warning, action_required = esUtils.check4file( graceid,
                                                    gdb,
                                                    framename,
                                                    regex=True,
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

class idqTimeseriesPlotCheck(esUtils.EventSupervisorTask):
    """
    a check that iDQ reported timeseries plot as expected
    """
    name = "idqTimeseriesPlot"

    def __init__(self, timeout, ifo, classifier, email=[], logDir='.', logTag='iQ'):
        self.ifo = ifo
        self.classifier = classifier
        self.description = "a check that iDQ reproted timeseries information as expected for %s at %s"%(self.classifier, self.ifo)
        super(idqTimeseriesPlotCheck, self).__init__( timeout,
                                                      email=email,
                                                      logDir=logDir,
                                                      logTag=logTag,
                                                    )

    def idqTimeseriesPlot(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that iDQ reported timeseries information as expected
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag ) 
            logger.info( "%s : %s"%(graceid, self.description) )
        figname = "%s_%s(.*)_timeseries-(.*)-(.*).png"%(self.ifo, self.classifier) ### NOTE: this may be fragile
        fragment = "iDQ fap and glitch-rank timeseries plot for %s at %s:"%(self.classifier, self.ifo) ### NOTE: this may be fragile
        self.warning, action_required = esUtils.check4file( graceid,
                                                    gdb,
                                                    figname,
                                                    regex=True,
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

class idqActiveChanCheck(esUtils.EventSupervisorTask):
    """
    check that iDQ uploaded a list of possible active channels
    """
    name = "idqActiveChan"

    def __init__(self, timeout, ifo, classifier, email=[], logDir='.', logTag='iQ'):
        self.ifo = ifo
        self.classifier = classifier
        self.description = "a check that iDQ uploads a list of possible active channels for %s at %s"%(self.classifier, self.ifo)
        super(idqActiveChanCheck, self).__init__( timeout, 
                                                  email=email,
                                                  logDir=logDir,
                                                  logTag=logTag,
                                                )

    def idqActiveChan(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        check that iDQ uploaded a list of possible active channels
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag )
            logger.info( "%s : %s"%(graceid, self.description) )
        jsonname = "%s_%s_chanlist(.*)-(.*)-(.*).json"%(self.ifo, self.classifier) ### NOTE: this may be fragile
        fragment = "iDQ (possible) active channels for %s at %s"%(self.classifier, self.ifo) ### NOTE: this may be fragile
        self.warning, action_required = esUtils.check4file( graceid,
                                                    gdb,
                                                    jsonname,
                                                    regex=True,
                                                    tagnames=None,
                                                    verbose=verbose,
                                                    logFragment=fragment,
                                                    logRegex=False,
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

class idqActiveChanPlotCheck(esUtils.EventSupervisorTask):
    """
    check that iDQ uploaded a plot of the possibly active channels
    """
    name = "idqActiveChanPlot"

    def __init__(self, timeout, ifo, classifier, email=[], logDir='.', logTag='iQ'):
        self.ifo = ifo
        self.classifier = classifier
        self.description = "a check that iDQ uploads a plot of possible active channels for %s at %s"%(self.classifier, self.ifo)
        super(idqActiveChanPlotCheck, self).__init__( timeout,
                                                      email=email,
                                                      logDir=logDir,
                                                      logTag=logTag,
                                                    )

    def idqActiveChanPlot(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        check that iDQ uploaded a plot of possible active channels
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag )
            logger.info( "%s : %s"%(graceid, self.description) )
        figname = "%s_%s(.*)_chanstrip-(.*)-(.*).png"%(self.ifo, self.classifier) ### NOTE: this may be fragile
        fragment = "iDQ channel strip chart for %s at %s"%(self.classifier, self.ifo) ### NOTE: this may be fragile
        self.warning, action_required = esUtils.check4file( graceid,
                                                    gdb,
                                                    figname,
                                                    regex=True,
                                                    tagnames=None,
                                                    verbose=verbose,
                                                    logFragment=fragment,
                                                    logRegex=False,
                                                    logTag=logger.name if logger else None,
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

#---
# reported by laldetchar-idq-gdb-glitch-tables.py
#---
class idqTablesCheck(esUtils.EventSupervisorTask):
    """
    a check that iDQ reported the xml tables as expected
    """
    name = "idqTables"

    def __init__(self, timeout, ifo, classifier, email=[], logDir='.', logTag='iQ'):
        self.ifo = ifo
        self.classifier = classifier
        self.description = "a check that iDQ reported the xml tables as expected for %s at %s"%(self.classifier, self.ifo)
        super(idqTablesCheck, self).__init__( timeout,
                                              email=email,
                                              logDir=logDir,
                                              logTag=logTag,
                                            ) 

    def idqTables(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that iDQ reported the xml tables as expected
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag )
            logger.info( "%s : %s"%(graceid, self.description) )
        filename = "%s_idq_%s(.*)-(.*)-(.*).xml.gz"%(self.ifo, self.classifier) ### NOTE: this may be fragile
        fragment = "iDQ glitch tables %s:"%(self.ifo) ### NOTE: this is bad... but it's what we have at the moment within iDQ
        self.warning, action_required = esUtils.check4file( graceid,
                                                    gdb,
                                                    filename,
                                                    regex=True,
                                                    tagnames=None,
                                                    verbose=verbose,
                                                    logFragment=fragment,
                                                    logRegex=False,
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

#---
# reported by laldetchar-idq-local-performance.py
#---
class idqCalibrationCheck(esUtils.EventSupervisorTask):
    """
    a check that iDQ reported historical calibration as expected
    """
    name = "idqCalibration"

    def __init__(self, timeout, ifo, classifier, email=[], logDir='.', logTag='iQ'):
        self.ifo = ifo
        self.classifier = classifier
        self.description = "a check that iDQ reported the calibration data as expected for %s at %s"%(self.classifier, self.ifo)
        super(idqCalibrationCheck, self).__init__( timeout, 
                                                   email=email,
                                                   logDir=logDir,
                                                   logTag=logTag,
                                                 )

    def idqCalibration(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that iDQ reported preformance metrics as expected
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag )
            logger.info( "%s : %s"%(graceid, self.description) )
        jsonname = "%s_%s(.*)_calib-(.*)-(.*).json"%(self.ifo, self.classifier) ### NOTE: this may be fragile
        fragment = "iDQ calibration sanity check for %s at %s"%(self.classifier, self.ifo) ### NOTE: this may be fragile
        self.warning, action_required = esUtils.check4file( graceid,
                                                    gdb,
                                                    jsonname,
                                                    regex=True,
                                                    tagnames=None,
                                                    verbose=verbose,
                                                    logFragment=fragment,
                                                    logRegex=False,
                                                    logTag=logger.name if verbose else None
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

class idqCalibrationPlotCheck(esUtils.EventSupervisorTask):
    """
    a check that iDQ reported historical calibration plot as expected
    """
    name = "idqCalibrationPlot"

    def __init__(self, timeout, ifo, classifier, email=[], logDir='.', logTag='iQ'):
        self.ifo = ifo
        self.classifier = classifier
        self.description = "a check that iDQ reported the calibration plot as expected for %s at %s"%(self.classifier, self.ifo)
        super(idqCalibrationPlotCheck, self).__init__( timeout,
                                                       email=email,
                                                       logDir=logDir,
                                                       logTag=logTag,
                                                     )

    def idqCalibrationPlot(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that iDQ reported preformance metrics as expected
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag )
            logger.info( "%s : %s"%(graceid, self.description) )
        figname = "%s_%s(.*)_calib-(.*)-(.*).png"%(self.ifo, self.classifier) ### NOTE: this may be fragile
        fragment = "iDQ calibration sanity check figure for %s at %s"%(self.classifier, self.ifo) ### NOTE: this may be fragile
        self.warning, action_required = esUtils.check4file( graceid,
                                                    gdb,
                                                    figname,
                                                    regex=True,
                                                    tagnames=None,
                                                    verbose=verbose,
                                                    logFragment=fragment,
                                                    logRegex=False,
                                                    logTag=logger.name if verbose else None
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

class idqROCCheck(esUtils.EventSupervisorTask):
    """
    a check that iDQ reported the local ROC data
    """
    name = "idqROC"

    def __init__(self, timeout, ifo, classifier, email=[], logDir='.', logTag='iQ'):
        self.ifo = ifo
        self.classifier = classifier
        self.description = "a check that iDQ reported the ROC data as expected for %s at %s"%(self.classifier, self.ifo)
        super(idqROCCheck, self).__init__( timeout,
                                           email=email,
                                           logDir=logDir,
                                           logTag=logTag,
                                         )

    def idqROC(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that iDQ reported preformance metrics as expected
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag )
            logger.info( "%s : %s"%(graceid, self.description) )
        jsonname = "%s_%s(.*)_ROC-(.*)-(.*).json"%(self.ifo, self.classifier) ### NOTE: this may be fragile
        fragment = "iDQ local ROC curves for %s at %s"%(self.classifier, self.ifo) ### NOTE: this may be fragile
        self.warning, action_required = esUtils.check4file( graceid,
                                                    gdb,
                                                    jsonname,
                                                    regex=True,
                                                    tagnames=None,
                                                    verbose=verbose,
                                                    logFragment=fragment,
                                                    logRegex=False,
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

class idqROCPlotCheck(esUtils.EventSupervisorTask):
    """
    a check that iDQ reported the local ROC plot
    """
    name = "idqROCPlot"

    def __init__(self, timeout, ifo, classifier, email=[], logDir='.', logTag='iQ'):
        self.ifo = ifo
        self.classifier = classifier
        self.description = "a check that iDQ reported the ROC plot as expected for %s at %s"%(self.classifier, self.ifo)
        super(idqROCPlotCheck, self).__init__( timeout,
                                               email=email,
                                               logDir=logDir,
                                               logTag=logTag,
                                             )

    def idqROCPlot(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that iDQ reported preformance metrics as expected
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag )
            logger.info( "%s : %s"%(graceid, self.description) )
        figname = "%s_%s(.*)_ROC-(.*)-(.*).png"%(self.ifo, self.classifier) ### NOTE: this may be fragile
        fragment = "iDQ local ROC figure for %s at %s"%(self.classifier, self.ifo) ### NOTE: this may be fragile
        self.warning, action_required = esUtils.check4file( graceid,
                                                    gdb,
                                                    figname,
                                                    regex=True,
                                                    tagnames=None,
                                                    verbose=verbose,
                                                    logFragment=fragment,
                                                    logRegex=False,
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

class idqCalibStatsCheck(esUtils.EventSupervisorTask):
    """
    a check that iDQ uploaded statistics about when calibration took place
    """
    name = "idqCalibStats"

    def __init__(self, timeout, ifo, classifier, email=[], logDir='.', logTag='iQ'):
        self.ifo = ifo
        self.classifier = classifier
        self.description = "a check that iDQ reported the calibration statistics as expected for %s at %s"%(self.classifier, self.ifo)
        super(idqCalibStatsCheck, self).__init__( timeout,
                                                  email=email,
                                                  logDir=logDir,
                                                  logTag=logTag,
                                                )

    def idqCalibStats(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that iDQ reported preformance metrics as expected
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag )
            logger.info( "%s : %s"%(graceid, self.description) )
        jsonname = "%s_%s(.*)_calibStats-(.*)-(.*).json"%(self.ifo, self.classifier) ### NOTE: this may be fragile
        fragment = "iDQ local calibration vital statistics for %s at %s"%(self.classifier, self.ifo) ### NOTE: this may be fragile
        self.warning, action_required = esUtils.check4file( graceid,
                                                    gdb,
                                                    jsonname,
                                                    regex=True,
                                                    tagnames=None,
                                                    verbose=verbose,
                                                    logFragment=fragment,
                                                    logRegex=False,
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

class idqTrainStatsCheck(esUtils.EventSupervisorTask):
    """
    a check that iDQ uploaded statistics about when training took place
    """
    name = "idqTrainStats"

    def __init__(self, timeout, ifo, classifier, email=[], logDir='.', logTag='iQ'):
        self.ifo = ifo
        self.classifier = classifier
        self.description = "a check that iDQ reported the training statistics as expected for %s at %s"%(self.classifier, self.ifo)
        super(idqTrainStatsCheck, self).__init__( timeout,
                                                  email=email,
                                                  logDir=logDir,
                                                  logTag=logTag,
                                                )

    def idqTrainStats(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that iDQ reported preformance metrics as expected
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag )
            logger.info( "%s : %s"%(graceid, self.description) )
        jsonname = "%s_%s(.*)_trainStats-(.*)-(.*).json"%(self.ifo, self.classifier) ### NOTE: this may be fragile
        fragment = "iDQ local training vital statistics for %s at %s"%(self.classifier, self.ifo) ### NOTE: this may be fragile
        self.warning, action_required = esUtils.check4file( graceid,
                                                    gdb,
                                                    jsonname,
                                                    regex=True,
                                                    tagnames=None,
                                                    verbose=verbose,
                                                    logFragment=fragment,
                                                    logRegex=False,
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

#---
# finish statement
#---
class idqFinishCheck(esUtils.EventSupervisorTask):
    """
    a check that iDQ finished as expected
    """
    name = "idqFinish"

    def __init__(self, timeout, ifo, email=[], logDir='.', logTag='iQ'):
        self.ifo = ifo
        self.description = "a check that iDQ finished reporting as expected at %s"%(self.ifo)
        super(idqFinishCheck, self).__init__( timeout,
                                              email=email,
                                              logDir=logDir,
                                              logTag=logTag,
                                            )

    def idqFinish(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that iDQ finished as expected
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag )
            logger.info( "%s : %s"%(graceid, self.description) )

        template = "Finished searching for iDQ information within [(.*), (.*)] at %s"%(self.ifo) ### use regex
        if not esUtils.check4log( graceid, gdb, template, verbose=verbose, regex=True, logTag=logger.name if verbose else None ):
            self.warning = "found iDQ completion message at %s"%(self.ifo)
            if verbose or annotate:
                message = "no action required : "+self.warning

                ### post message
                if verbose:
                    logger.debug( message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )

            return False ### action_required = False

        self.warning = "could not find iDQ completion message at %s"%(self.ifo)
        if verbose or annotate:
            message = "action required : "+self.warning

            ### post message
            if verbose:
                logger.debug( message )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )

        return True ### action_required = True

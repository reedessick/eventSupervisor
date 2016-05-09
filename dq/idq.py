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

    def __init__(self, timeout, ifo, email=[]):
        self.ifo = ifo
        self.description = "a check that iDQ reported a glitch-FAP at %s"%(self.ifo)
        super(idqGlitchFAPCheck, self).__init__( timeout,
                                                 self.idqGlitchFAPCheck,
                                                 name=self.name,
                                                 description=self.description,
                                                 email=email
                                               )

    def idqGlitchFAPCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that iDQ reported the gltich-FAP as expected
        NOT IMPLEMENTED
        """
        raise NotImplementedError 
        ### minimum glitch-FAP for %s at %s within [%.3f, %.3f] is %.3e"%(opts.classifier, ifo, opts.start, opts.end, min_fap)
        ### jsonfilename = idq.gdb_minFap_json(gdbdir, opts.classifier, ifo, "_minFAP%s"%filetag, int(opts.start), int(opts.end-opts.start))
        ### just check for the filename?
        ###   this is sort-of a special case (everyone cares about the log message), so we can check explicitly for that too?
        ###   expand check4file to also require a match for the associated log message?

class idqFAPFrameCheck(esUtils.EventSupervisorTask):
    """
    check that iDQ uploads fap timeseries files
    """
    ### fapfr = idq.gdb_timeseriesgwf( gdbdir , opts.classifier, ifo, "_fap%s"%filetag, start, dur)
    ### "minimum glitch-FAP for %s at %s within [%.3f, %.3f] is %.3e"%(opts.classifier, ifo, opts.start, opts.end, min_fap)

class idqRankFrameCheck(esUtils.EventSupervisorTask):
    """
    check that iDQ uploaded rank timeseries files
    """
    ### rnkfr = idq.gdb_timeseriesgwf( gdbdir , opts.classifier, ifo, "_rank%s"%filetag, start, dur)
    ### iDQ glitch-rank frame for %s at %s within [%d, %d] :"%(opts.classifier, ifo, start, start+dur)

class idqTimeseriesPlotCheck(esUtils.EventSupervisorTask):
    """
    a check that iDQ reported timeseries plot as expected
    """
    name = "idqTimeseriesPlotCheck"

    def __init__(self, timeout, ifo, email=[]):
        self.ifo = ifo
        self.description = "a check that iDQ reproted timeseries information as expected at %s"%(self.ifo)
        super(idqTimeseriesPlotCheck, self).__init__( timeout,
                                                  self.idqTimeseriesPlotCheck,
                                                  name=self.name,
                                                  description=self.description,
                                                  email=email
                                                )

    def idqTimeseriesPlotCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that iDQ reported timeseries information as expected
        NOT IMPLEMENTED
        """
        raise NotImplementedError
        ### figname = isp.timeseriesfig(gdbdir, ifo, opts.classifier, filetag, int(opts.plotting_gps_start), int(opts.plotting_gps_end-opts.plotting_gps_start))
        ### "iDQ fap and glitch-rank timeseries plot for " + opts.classifier + " at "+ifo+":"

class idqActiveChanCheck(esUtils.EventSupervisorTask):
    """
    check that iDQ uploaded a list of possible active channels
    """
    ### "iDQ (possible) active channels for %s at %s between [%.3f, %.3f]"%(opts.classifier, ifo, opts.plotting_gps_start, opts.plotting_gps_end)
    ### jsonfilename = idq.gdb_ovlstripchart_json(gdbdir, opts.classifier, ifo, filetag, int(opts.plotting_gps_start), int(opts.plotting_gps_end-opts.plotting_gps_start))

class idqActiveChanPlotCheck(esUtils.EventSupervisorTask):
    """
    check that iDQ uploaded a plot of the possibly active channels
    """
    ### "iDQ channel strip chart for %s at %s between [%.3f, %.3f]"%(opts.classifier, ifo, opts.plotting_gps_start, opts.plotting_gps_end)
    ### figname = isp.ovlstripchart(gdbdir, ifo, opts.classifier, filetag, opts.plotting_gps_start, opts.plotting_gps_end-opts.plotting_gps_start, figtype="png")

#---
# reported by laldetchar-idq-gdb-glitch-tables.py
#---
class idqTablesCheck(esUtils.EventSupervisorTask):
    """
    a check that iDQ reported the xml tables as expected
    """
    name = "idqTablesCheck"

    def __init__(self, timeout, ifo, email=[]):
        self.ifo = ifo
        self.description = "a check that iDQ reported the xml tables as expected at %s"%(self.ifo)
        super(idqTablesCheck, self).__init__( timeout,
                                              self.idqTablesCheck,
                                              name=self.name,
                                              description=self.description,
                                              email=email
                                            ) 

    def idqTablesCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that iDQ reported the xml tables as expected
        NOT IMPLEMENTED
        """
        raise NotImplementedError
        ### "iDQ glitch tables " + ifo + ":",
        ### merged_xmldoc_filename = idq.gdb_xml(gdbdir, opts.classifier, ifo, tag, int(opts.start), int(opts.end-opts.start))

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
        self.description = "a check that iDQ reported the performance metrics as expected for %s at %s"%(self.classifier, self.ifo)
        super(idqPerformanceCheck, self).__init__( timeout, 
                                                   self.idqPerformanceCheck,
                                                   name=self.name,
                                                   description=self.description,
                                                   email=email
                                                 )

    def idqPerformanceCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that iDQ reported preformance metrics as expected
        NOT IMPLEMENTED
        """
        raise NotImplementedError
        ### "iDQ calibration sanity check for %s at %s within [%.3f, %.3f]"%(opts.classifier, ifo, opts.start, opts.end)
        ### jsonfilename = idq.gdb_calib_json( gdbdir, ifo, opts.classifier, filetag, opts.start, opts.end-opts.start )

class idqCalibrationPlotCheck(esUtils.EventSupervisorTask):
    """
    a check that iDQ reported historical calibration plot as expected
    """
    ### "iDQ calibration sanity check figure for %s at %s within [%.3f, %.3f]"%(opts.classifier, ifo, opts.start, opts.end)
    ### figname = isp.calibfig( gdbdir, ifo, opts.classifier, filetag, opts.start, opts.end-opts.start )


class idqROCCheck(esUtils.EventSupervisorTask):
    """
    a check that iDQ reported the local ROC data
    """
    ### jsonfilename = idq.gdb_roc_json(  gdbdir, opts.classifier, ifo, filetag, opts.start, opts.end-opts.start )
    ### "iDQ local ROC curves for %s at %s within [%.3f, %.3f]"%(opts.classifier, ifo, opts.start, opts.end)

class idqROCPlotCheck(esUtils.EventSupervisorTask):
    """
    a check that iDQ reported the local ROC plot
    """
    ### figname = isp.rocfig( gdbdir, opts.classifier, ifo, filetag, opts.start, opts.end-opts.start )
    ### "iDQ local ROC figure for %s at %s within [%.3f, %.3f]"%(ifo, opts.classifier, opts.start, opts.end)

class idqCalibStatsCheck(esUtils.EventSupervisorTask):
    """
    a check that iDQ uploaded statistics about when calibration took place
    """
    ### jsonfilename = idq.useSummary_json( gdbdir, ifo, opts.classifier, "%s_calibStats"%filetag, opts.start, opts.end-opts.start)
    ### "iDQ local calibration vital statistics for %s at %s within [%.3f, %.3f]"%(opts.classifier, ifo, opts.start, opts.end)

class idqTrainStatsCheck(esUtils.EventSupervisorTask):
    """
    a check that iDQ uploaded statistics about when training took place
    """
    ### jsonfilename = idq.useSummary_json( gdbdir, ifo, opts.classifier, "%s_trainStats"%filetag, opts.start, opts.end-opts.start)
    ### "iDQ local training vital statistics for %s at %s within [%.3f, %.3f]"%(opts.classifier, ifo, opts.start, opts.end)

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


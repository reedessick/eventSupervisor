# functionality

notify/notify
    NotifyItem
        notifyByEmail					***
        notifyBySMS					***
        notifyByPhone					***

basic/basic
    EventCreationItem
        cWBTriggerCheck
        oLIBTriggerCheck
        cbcCoincCheck
        cbcPSDCheck

    FARItem
        FARCheck

    LocalRateItem
        localRateCheck

    CreateRateItem
        createRateCheck

    ExternalTriggersItem
        externalTriggersCheck

    UnblindInjectionsItem
        unblindInjectionsCheck				*** unkown statement when there is something there
							    also, we don't know if this will continue to be done

basic/approvalProcessor
    ApprovalProcessorPrelimDQItem
        approvalProcessorFARCheck
        approvalProcessorSegDBStartCheck		***
    ApprovalProcessorSegDBItem
        approvalProcessorSegDBFlagsCheck		***
        approvalProcessorSegDBFinishCheck		***
    ApprovalProcessoriDQItem
        approvalProcessoriDQglitchFAPCheck		***
    ApprovalProcessorVOEventItem
        approvalProcessorVOEventCreationCheck		***
        approvalProcessorVOEventDistributionCheck	***
    ApprovalProcessorGCNItem
        approvalProcessorGCNCreationCheck		***
        approvalProcessorGCNDistributionCheck		***

    labeling?						***

dq/dq
    DQSummaryItem
        dqSummaryCheck					***

dq/idq
    IDQStartItem
        idqStartCheck
    IDQItem
        idqGlitchFapCheck
        idqFAPFrameCheck
        idqRankFrameCheck
        idqTimeseriesPlotcheck
        idqActiveChanCheck
        idqActiveChanPlotCheck
        idqTablesCheck
        idqCalibrationCheck
        idqCalibrationPlotCheck
        idqROCCheck
        idqROCPlotCheck
        idqCalibStatsCheck
        idqTrainStatsCheck
        idqFinishCheck

dq/segDB2grcDB
    SegDB2GrcDBStartItem
        segDB2grcDBStartCheck
    SegDB2GrcDBItem
        segDB2grcDBFlagsCheck				*** probably want to add in deadtime estimates as a check, too
        segDB2grcDBVetoDefCheck				***
        segDB2grcDBAnyCheck				***
        segDB2grcDBFinishCheck

dq/omegaScan						all these are inherited for certain channel sets (which are hard coded?). 
							we should only use the parent classes and never the hard-coded children (and remove those?)
    OmegaScanStartItem
        omegaScanStartCheck				***
    OmegaScanItem
        omegaScanDataCheck				***
        omegaScanFinishCheck				***

skymaps/skymaps
    SkymapSanityItem
        skymapSanityCheck
    PlotSkymapItem
        plotSkymapCheck
    SkyviewerItem
        skyviewerCheck

skymaps/skymapSummary
    SkymapSummaryStartItem
        skymapSummaryStartCheck				***
    SkymapSummaryItem
        skymapSummaryDatacheck 				***
        skymapSummaryFinishCheck			***

pe/bayestar
    BayestarStartItem
        bayestarStartCheck
    BayestarItem
        bayestarSkymapCheck
        bayestarFinishCheck

pe/bayeswavePE
    BayesWavePEStartItem
        bayeswavePEStartCheck
    BayesWavePEItem
        bayeswavePEPostSampCheck
        bayeswavePEEstimateCheck
        bayeswavePEBayesFactorsCheck
        bayeswavePESkymapCheck
        bayeswavePEFinishCheck				*** no known statement? May not be reported by the pipeline?

pe/cwbPE
    CWBPEStartItem
        cWBPEStartCheck					*** no statement may exist?
    CWBPEItem
        cWBPECEDCheck
        cWBPEEstimateCheck
        cWBPESkymapCheck
        cWBPEFinishCheck				*** no statement may exist?

pe/lalinf
    LALInfStartItem
        lalinfStartCheck
    LALInfItem
        lalinfPostSampCheck				***
        lalinfSkymapCheck
        lalinfFinishCheck

pe/libPE
    LIBPEStartItem
        libPEStartCheck
    LIBPEItem
        libPEPostSampCheck
        libPEBayesFactors
        libPESkymapCheck
        libPEFinishCheck

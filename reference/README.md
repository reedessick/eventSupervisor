# functionality

notify/notify
    NotifyItem
        notifyByEmail					
        notifyBySMS					*** leave unimplemented for the time being
        notifyByPhone					*** leave unimplemented for the time being

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
        externalTriggersCheck				*** don't know what it looks like when we do find one...

    UnblindInjectionsItem
        unblindInjectionsCheck				*** unkown statement when there is something there
							    also, we don't know if this will continue to be done

basic/approvalProcessor
    ApprovalProcessorPrelimDQItem
        approvalProcessorFARCheck
        approvalProcessorSegDBStartCheck		*** leave unimplemented for the time being
    ApprovalProcessorSegDBItem
        approvalProcessorSegDBFlagsCheck		*** leave unimplemented for the time being
        approvalProcessorSegDBFinishCheck		*** leave unimplemented for the time being
    ApprovalProcessoriDQItem
        approvalProcessoriDQglitchFAPCheck		*** leave unimplemented for the time being
    ApprovalProcessorVOEventItem
        approvalProcessorVOEventCreationCheck		*** leave unimplemented for the time being
        approvalProcessorVOEventDistributionCheck	*** leave unimplemented for the time being
    ApprovalProcessorGCNItem
        approvalProcessorGCNCreationCheck		*** leave unimplemented for the time being
        approvalProcessorGCNDistributionCheck		*** leave unimplemented for the time being

    labeling?						*** leave unimplemented for the time being

dq/dq
    DQSummaryItem
        dqSummaryCheck					*** don't know what this looks like...

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
        segDB2grcDBFlagsCheck				
        segDB2grcDBVetoDefCheck				*** leave this unimplemented for the moment
        segDB2grcDBAnyCheck				
        segDB2grcDBFinishCheck

dq/omegaScan					
    OmegaScanStartItem
        omegaScanStartCheck				
    OmegaScanItem
        omegaScanDataCheck				
        omegaScanFinishCheck				

skymaps/skymaps
    SkymapSanityItem
        skymapSanityCheck
    PlotSkymapItem
        plotSkymapCheck
    SkyviewerItem
        skyviewerCheck

skymaps/skymapSummary
    SkymapSummaryStartItem
        skymapSummaryStartCheck				*** leave this unimplemented until new skymapSummaries are running
    SkymapSummaryItem
        skymapSummaryDatacheck 				*** leave this unimplemented until new skymapSummaries are running
        skymapSummaryFinishCheck			*** leave this unimplemented until new skymapSummaries are running

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
        lalinfPostSampCheck				*** no known statement?
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

#include "TriggerEfficiencyCalculator.h"
#include "Muon.h"
#include "Electron.h"
#include "TRandom.h"

#define useFit

TriggerEfficiencyCalculator::TriggerEfficiencyCalculator(NanoAODTree& nat)
: theNanoAODTree_(nat)
{}

TriggerEfficiencyCalculator::~TriggerEfficiencyCalculator()
{}

std::tuple<float, float, float> TriggerEfficiencyCalculator::getTriggerScaleFactor(const std::vector<Jet>& selectedJets)
{
    extractInformationFromEvent(selectedJets);
    std::tuple<float, float, float> dataEfficiency       = calculateDataTriggerEfficiency();
    std::tuple<float, float, float> monteCarloEfficiency = calculateMonteCarloTriggerEfficiency();
    float scaleFactorCentral = (std::get<0>(monteCarloEfficiency) > 0) ? (std::get<0>(dataEfficiency) / std::get<0>(monteCarloEfficiency)) : 1.;
    float scaleFactorUp      = (std::get<2>(monteCarloEfficiency) > 0) ? (std::get<1>(dataEfficiency) / std::get<2>(monteCarloEfficiency)) : 1.;
    float scaleFactorDown    = (std::get<1>(monteCarloEfficiency) > 0) ? (std::get<2>(dataEfficiency) / std::get<1>(monteCarloEfficiency)) : 1.;
    return {scaleFactorCentral, scaleFactorUp, scaleFactorDown};
}

std::tuple<float, float, float> TriggerEfficiencyCalculator::getDataTriggerEfficiency(const std::vector<Jet>& selectedJets)
{
    extractInformationFromEvent(selectedJets);
    return calculateDataTriggerEfficiency();
}

std::tuple<float, float, float> TriggerEfficiencyCalculator::getMonteCarloTriggerEfficiency(const std::vector<Jet>& selectedJets)
{
    extractInformationFromEvent(selectedJets);
    return calculateMonteCarloTriggerEfficiency();
}

std::tuple<std::tuple<float,float,float>, std::tuple<float,float,float>, std::tuple<float,float,float>> TriggerEfficiencyCalculator::getScaleFactorDataAndMonteCarloEfficiency(const std::vector<Jet>& selectedJets)
{
    extractInformationFromEvent(selectedJets);
    std::tuple<float, float, float> dataEfficiency       = calculateDataTriggerEfficiency();
    std::tuple<float, float, float> monteCarloEfficiency = calculateMonteCarloTriggerEfficiency();
    float scaleFactorCentral = (std::get<0>(monteCarloEfficiency) > 0) ? (std::get<0>(dataEfficiency) / std::get<0>(monteCarloEfficiency)) : 1.;
    float scaleFactorUp      = (std::get<2>(monteCarloEfficiency) > 0) ? (std::get<1>(dataEfficiency) / std::get<2>(monteCarloEfficiency)) : 1.;
    float scaleFactorDown    = (std::get<1>(monteCarloEfficiency) > 0) ? (std::get<2>(dataEfficiency) / std::get<1>(monteCarloEfficiency)) : 1.;
    return {{scaleFactorCentral, scaleFactorUp, scaleFactorDown} , dataEfficiency , monteCarloEfficiency};

}

void TriggerEfficiencyCalculator::simulateTrigger(OutputTree* theOutputTree)
{
  theOutputTree_ = theOutputTree;
  simulateTrigger_ = true;
  createTriggerSimulatedBranches();
}






/*
// 2016
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

TriggerEfficiencyCalculator_2016::TriggerEfficiencyCalculator_2016(std::string inputFileName, NanoAODTree& nat)
: TriggerEfficiencyCalculator(nat)
, fTriggerFitCurves(inputFileName)
{}

TriggerEfficiencyCalculator_2016::~TriggerEfficiencyCalculator_2016()
{}

bool TriggerEfficiencyCalculator_2016::isPassingTurnOnCuts(std::vector<std::string> listOfPassedTriggers, const std::vector<Jet>& selectedJets)
{
    extractInformationFromEvent(selectedJets);

    if(!applyTurnOnCut_) return true;
    bool Double90Doule30Passed = (std::find(listOfPassedTriggers.begin(), listOfPassedTriggers.end(), "HLT_DoubleJet90_Double30_TripleBTagCSV_p087") != listOfPassedTriggers.end());
    bool Quad45Passed          = (std::find(listOfPassedTriggers.begin(), listOfPassedTriggers.end(), "HLT_QuadJet45_TripleBTagCSV_p087") != listOfPassedTriggers.end());
    return (Double90Doule30Passed && sumPt_>double90Double30_minSumPt_ && pt2_>double90Double30_minPt2_ && pt4_>double90Double30_minPt4_) || (Quad45Passed && sumPt_>quad45_minSumPt_ && pt4_>quad45_minPt4_); 
}

std::tuple<float, float, float> TriggerEfficiencyCalculator_2016::calculateDataTriggerEfficiency()
{
    std::tuple<float, float, float> Double90Double30Efficiency = calculateDataDouble90Double30Efficiency();
    std::tuple<float, float, float> Quad45Efficiency           = calculateDataQuad45Efficiency          ();
    std::tuple<float, float, float> AndEfficiency              = calculateDataAndEfficiency             ();
    if(simulateTrigger_)
    {

        if((sumPt_>double90Double30_minSumPt_ && pt2_>double90Double30_minPt2_ && pt4_>double90Double30_minPt4_) || !applyTurnOnCut_)
        {
            float Double90Double30Random = gRandom->Rndm();
            if(Double90Double30Random < std::get<0>(Double90Double30Efficiency)) theOutputTree_->userInt("HLT_DoubleJet90_Double30_TripleBTagCSV_p087_Simulated"    ) = 1;
            if(Double90Double30Random < std::get<1>(Double90Double30Efficiency)) theOutputTree_->userInt("HLT_DoubleJet90_Double30_TripleBTagCSV_p087_SimulatedUp"  ) = 1;
            if(Double90Double30Random < std::get<2>(Double90Double30Efficiency)) theOutputTree_->userInt("HLT_DoubleJet90_Double30_TripleBTagCSV_p087_SimulatedDown") = 1;
        }
        
        if((sumPt_>quad45_minSumPt_ && pt4_>quad45_minPt4_) || !applyTurnOnCut_)
        {
            float Quad45Random = gRandom->Rndm();
            if(Quad45Random < std::get<0>(Quad45Efficiency          )) theOutputTree_->userInt("HLT_QuadJet45_TripleBTagCSV_p087_Simulated"    ) = 1;
            if(Quad45Random < std::get<1>(Quad45Efficiency          )) theOutputTree_->userInt("HLT_QuadJet45_TripleBTagCSV_p087_SimulatedUp"  ) = 1;
            if(Quad45Random < std::get<2>(Quad45Efficiency          )) theOutputTree_->userInt("HLT_QuadJet45_TripleBTagCSV_p087_SimulatedDown") = 1;
        }

        if(theOutputTree_->userInt("HLT_QuadJet45_TripleBTagCSV_p087_Simulated"    ) || theOutputTree_->userInt("HLT_DoubleJet90_Double30_TripleBTagCSV_p087_Simulated"    )) theOutputTree_->userInt("HLT_Simulated"    ) = 1;
        if(theOutputTree_->userInt("HLT_QuadJet45_TripleBTagCSV_p087_SimulatedUp"  ) || theOutputTree_->userInt("HLT_DoubleJet90_Double30_TripleBTagCSV_p087_SimulatedUp"  )) theOutputTree_->userInt("HLT_SimulatedUp"  ) = 1;
        if(theOutputTree_->userInt("HLT_QuadJet45_TripleBTagCSV_p087_SimulatedDown") || theOutputTree_->userInt("HLT_DoubleJet90_Double30_TripleBTagCSV_p087_SimulatedDown")) theOutputTree_->userInt("HLT_SimulatedDown") = 1;

    }

    // std::cout << "Data Efficiency -> Double90Double30Efficiency = " << Double90Double30Efficiency << " Quad45Efficiency = " << Quad45Efficiency << " AndEfficiency = " << AndEfficiency << " Double90Double30Efficiency * AndEfficiency = " << (Double90Double30Efficiency * AndEfficiency) << std::endl;
    float efficiencyCentral = std::get<0>(Double90Double30Efficiency) + std::get<0>(Quad45Efficiency) - (std::get<0>(Double90Double30Efficiency) * std::get<0>(AndEfficiency));
    float efficiencyUp      = std::get<1>(Double90Double30Efficiency) + std::get<1>(Quad45Efficiency) - (std::get<1>(Double90Double30Efficiency) * std::get<2>(AndEfficiency));
    float efficiencyDown    = std::get<2>(Double90Double30Efficiency) + std::get<2>(Quad45Efficiency) - (std::get<2>(Double90Double30Efficiency) * std::get<1>(AndEfficiency));
    return {efficiencyCentral, efficiencyUp, efficiencyDown};
}

std::tuple<float, float, float> TriggerEfficiencyCalculator_2016::calculateMonteCarloTriggerEfficiency()
{
    std::tuple<float, float, float> Double90Double30Efficiency = calculateMonteCarloDouble90Double30Efficiency();
    std::tuple<float, float, float> Quad45Efficiency           = calculateMonteCarloQuad45Efficiency          ();
    std::tuple<float, float, float> AndEfficiency              = calculateMonteCarloAndEfficiency             ();

    if(simulateTrigger_)
    {
        if((sumPt_>double90Double30_minSumPt_ && pt2_>double90Double30_minPt2_ && pt4_>double90Double30_minPt4_) || !applyTurnOnCut_)
        {
            float Double90Double30Random = gRandom->Rndm();
            if(Double90Double30Random < std::get<0>(Double90Double30Efficiency)) theOutputTree_->userInt("HLT_DoubleJet90_Double30_TripleBTagCSV_p087_SimulatedMc"    ) = 1;
            if(Double90Double30Random < std::get<1>(Double90Double30Efficiency)) theOutputTree_->userInt("HLT_DoubleJet90_Double30_TripleBTagCSV_p087_SimulatedMcUp"  ) = 1;
            if(Double90Double30Random < std::get<2>(Double90Double30Efficiency)) theOutputTree_->userInt("HLT_DoubleJet90_Double30_TripleBTagCSV_p087_SimulatedMcDown") = 1;
        }

        if((sumPt_>quad45_minSumPt_ && pt4_>quad45_minPt4_) || !applyTurnOnCut_)
        {
            float Quad45Random = gRandom->Rndm();
            if(Quad45Random < std::get<0>(Quad45Efficiency          )) theOutputTree_->userInt("HLT_QuadJet45_TripleBTagCSV_p087_SimulatedMc"    ) = 1;
            if(Quad45Random < std::get<1>(Quad45Efficiency          )) theOutputTree_->userInt("HLT_QuadJet45_TripleBTagCSV_p087_SimulatedMcUp"  ) = 1;
            if(Quad45Random < std::get<2>(Quad45Efficiency          )) theOutputTree_->userInt("HLT_QuadJet45_TripleBTagCSV_p087_SimulatedMcDown") = 1;
        }

        if(theOutputTree_->userInt("HLT_QuadJet45_TripleBTagCSV_p087_SimulatedMc"    ) || theOutputTree_->userInt("HLT_DoubleJet90_Double30_TripleBTagCSV_p087_SimulatedMc"    )) theOutputTree_->userInt("HLT_SimulatedMc"    ) = 1;
        if(theOutputTree_->userInt("HLT_QuadJet45_TripleBTagCSV_p087_SimulatedMcUp"  ) || theOutputTree_->userInt("HLT_DoubleJet90_Double30_TripleBTagCSV_p087_SimulatedMcUp"  )) theOutputTree_->userInt("HLT_SimulatedMcUp"  ) = 1;
        if(theOutputTree_->userInt("HLT_QuadJet45_TripleBTagCSV_p087_SimulatedMcDown") || theOutputTree_->userInt("HLT_DoubleJet90_Double30_TripleBTagCSV_p087_SimulatedMcDown")) theOutputTree_->userInt("HLT_SimulatedMcDown") = 1;

    }


    // std::cout << "MonteCarlo Efficiency -> Double90Double30Efficiency = " << Double90Double30Efficiency << " Quad45Efficiency = " << Quad45Efficiency << " AndEfficiency = " << AndEfficiency << " Double90Double30Efficiency * AndEfficiency = " << (Double90Double30Efficiency * AndEfficiency) << std::endl;
    float efficiencyCentral = std::get<0>(Double90Double30Efficiency) + std::get<0>(Quad45Efficiency) - (std::get<0>(Double90Double30Efficiency) * std::get<0>(AndEfficiency));
    float efficiencyUp      = std::get<1>(Double90Double30Efficiency) + std::get<1>(Quad45Efficiency) - (std::get<1>(Double90Double30Efficiency) * std::get<2>(AndEfficiency));
    float efficiencyDown    = std::get<2>(Double90Double30Efficiency) + std::get<2>(Quad45Efficiency) - (std::get<2>(Double90Double30Efficiency) * std::get<1>(AndEfficiency));
    return {efficiencyCentral, efficiencyUp, efficiencyDown};
}

std::tuple<float, float, float> TriggerEfficiencyCalculator_2016::calculateDataDouble90Double30Efficiency()
{
    #ifdef useFit
        float bTagEffJet0        = fTriggerFitCurves.fSingleMuon_Double90Quad30_Efficiency_BTagCaloCSVp087TriplePair.first      ->Eval(deepFlavBVector[0]);
        float bTagEffJet1        = fTriggerFitCurves.fSingleMuon_Double90Quad30_Efficiency_BTagCaloCSVp087TriplePair.first      ->Eval(deepFlavBVector[1]);
        float bTagEffJet2        = fTriggerFitCurves.fSingleMuon_Double90Quad30_Efficiency_BTagCaloCSVp087TriplePair.first      ->Eval(deepFlavBVector[2]);
        float bTagEffJet3        = fTriggerFitCurves.fSingleMuon_Double90Quad30_Efficiency_BTagCaloCSVp087TriplePair.first      ->Eval(deepFlavBVector[3]);
        float bTagEffJet0Error        = getFitError(fTriggerFitCurves.fSingleMuon_Double90Quad30_Efficiency_BTagCaloCSVp087TriplePair.second      , deepFlavBVector[0]);
        float bTagEffJet1Error        = getFitError(fTriggerFitCurves.fSingleMuon_Double90Quad30_Efficiency_BTagCaloCSVp087TriplePair.second      , deepFlavBVector[1]);
        float bTagEffJet2Error        = getFitError(fTriggerFitCurves.fSingleMuon_Double90Quad30_Efficiency_BTagCaloCSVp087TriplePair.second      , deepFlavBVector[2]);
        float bTagEffJet3Error        = getFitError(fTriggerFitCurves.fSingleMuon_Double90Quad30_Efficiency_BTagCaloCSVp087TriplePair.second      , deepFlavBVector[3]);
    #else
        // float bTagEffJet0        = getPointValue<0>(fTriggerFitCurves.fSingleMuon_Double90Quad30_Efficiency_BTagCaloCSVp087TripleGraphs, deepFlavBVector[0]);
        // float bTagEffJet1        = getPointValue<0>(fTriggerFitCurves.fSingleMuon_Double90Quad30_Efficiency_BTagCaloCSVp087TripleGraphs, deepFlavBVector[1]);
        // float bTagEffJet2        = getPointValue<0>(fTriggerFitCurves.fSingleMuon_Double90Quad30_Efficiency_BTagCaloCSVp087TripleGraphs, deepFlavBVector[2]);
        // float bTagEffJet3        = getPointValue<0>(fTriggerFitCurves.fSingleMuon_Double90Quad30_Efficiency_BTagCaloCSVp087TripleGraphs, deepFlavBVector[3]);
        // float bTagEffJet0Up      = getPointValue<1>(fTriggerFitCurves.fSingleMuon_Double90Quad30_Efficiency_BTagCaloCSVp087TripleGraphs, deepFlavBVector[0]);
        // float bTagEffJet1Up      = getPointValue<1>(fTriggerFitCurves.fSingleMuon_Double90Quad30_Efficiency_BTagCaloCSVp087TripleGraphs, deepFlavBVector[1]);
        // float bTagEffJet2Up      = getPointValue<1>(fTriggerFitCurves.fSingleMuon_Double90Quad30_Efficiency_BTagCaloCSVp087TripleGraphs, deepFlavBVector[2]);
        // float bTagEffJet3Up      = getPointValue<1>(fTriggerFitCurves.fSingleMuon_Double90Quad30_Efficiency_BTagCaloCSVp087TripleGraphs, deepFlavBVector[3]);
        // float bTagEffJet0Down    = getPointValue<2>(fTriggerFitCurves.fSingleMuon_Double90Quad30_Efficiency_BTagCaloCSVp087TripleGraphs, deepFlavBVector[0]);
        // float bTagEffJet1Down    = getPointValue<2>(fTriggerFitCurves.fSingleMuon_Double90Quad30_Efficiency_BTagCaloCSVp087TripleGraphs, deepFlavBVector[1]);
        // float bTagEffJet2Down    = getPointValue<2>(fTriggerFitCurves.fSingleMuon_Double90Quad30_Efficiency_BTagCaloCSVp087TripleGraphs, deepFlavBVector[2]);
        // float bTagEffJet3Down    = getPointValue<2>(fTriggerFitCurves.fSingleMuon_Double90Quad30_Efficiency_BTagCaloCSVp087TripleGraphs, deepFlavBVector[3]);
        float bTagEffJet0        = std::get<0>(fTriggerFitCurves.fSingleMuon_Double90Quad30_Efficiency_BTagCaloCSVp087TripleGraphs)  ->Eval(deepFlavBVector[0], 0, "S");
        float bTagEffJet1        = std::get<0>(fTriggerFitCurves.fSingleMuon_Double90Quad30_Efficiency_BTagCaloCSVp087TripleGraphs)  ->Eval(deepFlavBVector[1], 0, "S");
        float bTagEffJet2        = std::get<0>(fTriggerFitCurves.fSingleMuon_Double90Quad30_Efficiency_BTagCaloCSVp087TripleGraphs)  ->Eval(deepFlavBVector[2], 0, "S");
        float bTagEffJet3        = std::get<0>(fTriggerFitCurves.fSingleMuon_Double90Quad30_Efficiency_BTagCaloCSVp087TripleGraphs)  ->Eval(deepFlavBVector[3], 0, "S");
        float bTagEffJet0Up      = std::get<1>(fTriggerFitCurves.fSingleMuon_Double90Quad30_Efficiency_BTagCaloCSVp087TripleGraphs)  ->Eval(deepFlavBVector[0], 0, "S");
        float bTagEffJet1Up      = std::get<1>(fTriggerFitCurves.fSingleMuon_Double90Quad30_Efficiency_BTagCaloCSVp087TripleGraphs)  ->Eval(deepFlavBVector[1], 0, "S");
        float bTagEffJet2Up      = std::get<1>(fTriggerFitCurves.fSingleMuon_Double90Quad30_Efficiency_BTagCaloCSVp087TripleGraphs)  ->Eval(deepFlavBVector[2], 0, "S");
        float bTagEffJet3Up      = std::get<1>(fTriggerFitCurves.fSingleMuon_Double90Quad30_Efficiency_BTagCaloCSVp087TripleGraphs)  ->Eval(deepFlavBVector[3], 0, "S");
        float bTagEffJet0Down    = std::get<2>(fTriggerFitCurves.fSingleMuon_Double90Quad30_Efficiency_BTagCaloCSVp087TripleGraphs)  ->Eval(deepFlavBVector[0], 0, "S");
        float bTagEffJet1Down    = std::get<2>(fTriggerFitCurves.fSingleMuon_Double90Quad30_Efficiency_BTagCaloCSVp087TripleGraphs)  ->Eval(deepFlavBVector[1], 0, "S");
        float bTagEffJet2Down    = std::get<2>(fTriggerFitCurves.fSingleMuon_Double90Quad30_Efficiency_BTagCaloCSVp087TripleGraphs)  ->Eval(deepFlavBVector[2], 0, "S");
        float bTagEffJet3Down    = std::get<2>(fTriggerFitCurves.fSingleMuon_Double90Quad30_Efficiency_BTagCaloCSVp087TripleGraphs)  ->Eval(deepFlavBVector[3], 0, "S");
    #endif
    
    float effL1              = fTriggerFitCurves.fSingleMuon_Double90Quad30_Efficiency_L1filterHTPair.first                 ->Eval(sumPt_);
    float effQuad30CaloJet   = fTriggerFitCurves.fSingleMuon_Double90Quad30_Efficiency_QuadCentralJet30Pair.first           ->Eval(pt4_  );
    float effDouble90CaloJet = fTriggerFitCurves.fSingleMuon_Double90Quad30_Efficiency_DoubleCentralJet90Pair.first         ->Eval(pt2_  );
    float effQuad30PFJet     = fTriggerFitCurves.fSingleMuon_Double90Quad30_Efficiency_QuadPFCentralJetLooseID30Pair.first  ->Eval(pt4_  );
    float effDouble90PFJet   = fTriggerFitCurves.fSingleMuon_Double90Quad30_Efficiency_DoublePFCentralJetLooseID90Pair.first->Eval(pt2_  );
    
    float effL1Error              = getFitError(fTriggerFitCurves.fSingleMuon_Double90Quad30_Efficiency_L1filterHTPair.second                 , sumPt_            );
    float effQuad30CaloJetError   = getFitError(fTriggerFitCurves.fSingleMuon_Double90Quad30_Efficiency_QuadCentralJet30Pair.second           , pt4_              );
    float effDouble90CaloJetError = getFitError(fTriggerFitCurves.fSingleMuon_Double90Quad30_Efficiency_DoubleCentralJet90Pair.second         , pt2_              );
    float effQuad30PFJetError     = getFitError(fTriggerFitCurves.fSingleMuon_Double90Quad30_Efficiency_QuadPFCentralJetLooseID30Pair.second  , pt4_              );
    float effDouble90PFJetError   = getFitError(fTriggerFitCurves.fSingleMuon_Double90Quad30_Efficiency_DoublePFCentralJetLooseID90Pair.second, pt2_              );

    float threeBtagEfficiency          = computeThreeBtagEfficiency(bTagEffJet0, bTagEffJet1, bTagEffJet2, bTagEffJet3);
    float threeBtagEfficiencyErrorUp   = computeThreeBtagEfficiency(bTagEffJet0 + bTagEffJet0Error, bTagEffJet1 + bTagEffJet1Error, bTagEffJet2 + bTagEffJet2Error, bTagEffJet3 + bTagEffJet3Error);
    float threeBtagEfficiencyErrorDown = computeThreeBtagEfficiency(bTagEffJet0 - bTagEffJet0Error, bTagEffJet1 - bTagEffJet1Error, bTagEffJet2 - bTagEffJet2Error, bTagEffJet3 - bTagEffJet3Error);
    

    theOutputTree_->userFloat("HLT_Data_DoubleJet90_Double30_effL1"              ) = effL1              ;
    theOutputTree_->userFloat("HLT_Data_DoubleJet90_Double30_effQuad30CaloJet"   ) = effQuad30CaloJet   ;
    theOutputTree_->userFloat("HLT_Data_DoubleJet90_Double30_effDouble90CaloJet" ) = effDouble90CaloJet ;
    theOutputTree_->userFloat("HLT_Data_DoubleJet90_Double30_effQuad30PFJet"     ) = effQuad30PFJet     ;
    theOutputTree_->userFloat("HLT_Data_DoubleJet90_Double30_effDouble90PFJet"   ) = effDouble90PFJet   ;
    theOutputTree_->userFloat("HLT_Data_DoubleJet90_Double30_threeBtagEfficiency") = threeBtagEfficiency;

    float efficiencyCentral = computeDouble90Double30Efficiency(threeBtagEfficiency, effL1, effQuad30CaloJet, effDouble90CaloJet, effQuad30PFJet, effDouble90PFJet);
    #ifdef useFit
        float efficiencyUp      = computeDouble90Double30Efficiency(threeBtagEfficiencyErrorUp, effL1 + effL1Error, effQuad30CaloJet + effQuad30CaloJetError, effDouble90CaloJet + effDouble90CaloJetError, effQuad30PFJet + effQuad30PFJetError, effDouble90PFJet + effDouble90PFJetError);
        float efficiencyDown    = computeDouble90Double30Efficiency(threeBtagEfficiencyErrorDown, effL1 - effL1Error, effQuad30CaloJet - effQuad30CaloJetError, effDouble90CaloJet - effDouble90CaloJetError, effQuad30PFJet - effQuad30PFJetError, effDouble90PFJet - effDouble90PFJetError);
    #else
        float efficiencyUp      = computeDouble90Double30Efficiency(bTagEffJet0Up  , bTagEffJet1Up  , bTagEffJet2Up  , bTagEffJet3Up  , effL1 + effL1Error, effQuad30CaloJet + effQuad30CaloJetError, effDouble90CaloJet + effDouble90CaloJetError, effQuad30PFJet + effQuad30PFJetError, effDouble90PFJet + effDouble90PFJetError);
        float efficiencyDown    = computeDouble90Double30Efficiency(bTagEffJet0Down, bTagEffJet1Down, bTagEffJet2Down, bTagEffJet3Down, effL1 - effL1Error, effQuad30CaloJet - effQuad30CaloJetError, effDouble90CaloJet - effDouble90CaloJetError, effQuad30PFJet - effQuad30PFJetError, effDouble90PFJet - effDouble90PFJetError);
    #endif

    return {efficiencyCentral, efficiencyUp, efficiencyDown};
}

std::tuple<float, float, float> TriggerEfficiencyCalculator_2016::calculateDataQuad45Efficiency()
{
    
    #ifdef useFit
        float bTagEffJet0      = fTriggerFitCurves.fSingleMuon_Quad45_Efficiency_BTagCaloCSVp087TriplePair.first    ->Eval(deepFlavBVector[0]);
        float bTagEffJet1      = fTriggerFitCurves.fSingleMuon_Quad45_Efficiency_BTagCaloCSVp087TriplePair.first    ->Eval(deepFlavBVector[1]);
        float bTagEffJet2      = fTriggerFitCurves.fSingleMuon_Quad45_Efficiency_BTagCaloCSVp087TriplePair.first    ->Eval(deepFlavBVector[2]);
        float bTagEffJet3      = fTriggerFitCurves.fSingleMuon_Quad45_Efficiency_BTagCaloCSVp087TriplePair.first    ->Eval(deepFlavBVector[3]);
        float bTagEffJet0Error      = getFitError(fTriggerFitCurves.fSingleMuon_Quad45_Efficiency_BTagCaloCSVp087TriplePair.second    , deepFlavBVector[0]);
        float bTagEffJet1Error      = getFitError(fTriggerFitCurves.fSingleMuon_Quad45_Efficiency_BTagCaloCSVp087TriplePair.second    , deepFlavBVector[1]);
        float bTagEffJet2Error      = getFitError(fTriggerFitCurves.fSingleMuon_Quad45_Efficiency_BTagCaloCSVp087TriplePair.second    , deepFlavBVector[2]);
        float bTagEffJet3Error      = getFitError(fTriggerFitCurves.fSingleMuon_Quad45_Efficiency_BTagCaloCSVp087TriplePair.second    , deepFlavBVector[3]);
    #else
        // float bTagEffJet0        = getPointValue<0>(fTriggerFitCurves.fSingleMuon_Quad45_Efficiency_BTagCaloCSVp087TripleGraphs, deepFlavBVector[0]);
        // float bTagEffJet1        = getPointValue<0>(fTriggerFitCurves.fSingleMuon_Quad45_Efficiency_BTagCaloCSVp087TripleGraphs, deepFlavBVector[1]);
        // float bTagEffJet2        = getPointValue<0>(fTriggerFitCurves.fSingleMuon_Quad45_Efficiency_BTagCaloCSVp087TripleGraphs, deepFlavBVector[2]);
        // float bTagEffJet3        = getPointValue<0>(fTriggerFitCurves.fSingleMuon_Quad45_Efficiency_BTagCaloCSVp087TripleGraphs, deepFlavBVector[3]);
        // float bTagEffJet0Up      = getPointValue<1>(fTriggerFitCurves.fSingleMuon_Quad45_Efficiency_BTagCaloCSVp087TripleGraphs, deepFlavBVector[0]);
        // float bTagEffJet1Up      = getPointValue<1>(fTriggerFitCurves.fSingleMuon_Quad45_Efficiency_BTagCaloCSVp087TripleGraphs, deepFlavBVector[1]);
        // float bTagEffJet2Up      = getPointValue<1>(fTriggerFitCurves.fSingleMuon_Quad45_Efficiency_BTagCaloCSVp087TripleGraphs, deepFlavBVector[2]);
        // float bTagEffJet3Up      = getPointValue<1>(fTriggerFitCurves.fSingleMuon_Quad45_Efficiency_BTagCaloCSVp087TripleGraphs, deepFlavBVector[3]);
        // float bTagEffJet0Down    = getPointValue<2>(fTriggerFitCurves.fSingleMuon_Quad45_Efficiency_BTagCaloCSVp087TripleGraphs, deepFlavBVector[0]);
        // float bTagEffJet1Down    = getPointValue<2>(fTriggerFitCurves.fSingleMuon_Quad45_Efficiency_BTagCaloCSVp087TripleGraphs, deepFlavBVector[1]);
        // float bTagEffJet2Down    = getPointValue<2>(fTriggerFitCurves.fSingleMuon_Quad45_Efficiency_BTagCaloCSVp087TripleGraphs, deepFlavBVector[2]);
        // float bTagEffJet3Down    = getPointValue<2>(fTriggerFitCurves.fSingleMuon_Quad45_Efficiency_BTagCaloCSVp087TripleGraphs, deepFlavBVector[3]);
        float bTagEffJet0        = std::get<0>(fTriggerFitCurves.fSingleMuon_Quad45_Efficiency_BTagCaloCSVp087TripleGraphs)  ->Eval(deepFlavBVector[0], 0, "S");
        float bTagEffJet1        = std::get<0>(fTriggerFitCurves.fSingleMuon_Quad45_Efficiency_BTagCaloCSVp087TripleGraphs)  ->Eval(deepFlavBVector[1], 0, "S");
        float bTagEffJet2        = std::get<0>(fTriggerFitCurves.fSingleMuon_Quad45_Efficiency_BTagCaloCSVp087TripleGraphs)  ->Eval(deepFlavBVector[2], 0, "S");
        float bTagEffJet3        = std::get<0>(fTriggerFitCurves.fSingleMuon_Quad45_Efficiency_BTagCaloCSVp087TripleGraphs)  ->Eval(deepFlavBVector[3], 0, "S");
        float bTagEffJet0Up      = std::get<1>(fTriggerFitCurves.fSingleMuon_Quad45_Efficiency_BTagCaloCSVp087TripleGraphs)  ->Eval(deepFlavBVector[0], 0, "S");
        float bTagEffJet1Up      = std::get<1>(fTriggerFitCurves.fSingleMuon_Quad45_Efficiency_BTagCaloCSVp087TripleGraphs)  ->Eval(deepFlavBVector[1], 0, "S");
        float bTagEffJet2Up      = std::get<1>(fTriggerFitCurves.fSingleMuon_Quad45_Efficiency_BTagCaloCSVp087TripleGraphs)  ->Eval(deepFlavBVector[2], 0, "S");
        float bTagEffJet3Up      = std::get<1>(fTriggerFitCurves.fSingleMuon_Quad45_Efficiency_BTagCaloCSVp087TripleGraphs)  ->Eval(deepFlavBVector[3], 0, "S");
        float bTagEffJet0Down    = std::get<2>(fTriggerFitCurves.fSingleMuon_Quad45_Efficiency_BTagCaloCSVp087TripleGraphs)  ->Eval(deepFlavBVector[0], 0, "S");
        float bTagEffJet1Down    = std::get<2>(fTriggerFitCurves.fSingleMuon_Quad45_Efficiency_BTagCaloCSVp087TripleGraphs)  ->Eval(deepFlavBVector[1], 0, "S");
        float bTagEffJet2Down    = std::get<2>(fTriggerFitCurves.fSingleMuon_Quad45_Efficiency_BTagCaloCSVp087TripleGraphs)  ->Eval(deepFlavBVector[2], 0, "S");
        float bTagEffJet3Down    = std::get<2>(fTriggerFitCurves.fSingleMuon_Quad45_Efficiency_BTagCaloCSVp087TripleGraphs)  ->Eval(deepFlavBVector[3], 0, "S");
    #endif

    float effL1            = fTriggerFitCurves.fSingleMuon_Quad45_Efficiency_L1filterHTPair.first               ->Eval(sumPt_            );
    float effQuad45CaloJet = fTriggerFitCurves.fSingleMuon_Quad45_Efficiency_QuadCentralJet45Pair.first         ->Eval(pt4_              );
    float effQuad45PFJet   = fTriggerFitCurves.fSingleMuon_Quad45_Efficiency_QuadPFCentralJetLooseID45Pair.first->Eval(pt4_              );

    float effL1Error            = getFitError(fTriggerFitCurves.fSingleMuon_Quad45_Efficiency_L1filterHTPair.second               , sumPt_            );
    float effQuad45CaloJetError = getFitError(fTriggerFitCurves.fSingleMuon_Quad45_Efficiency_QuadCentralJet45Pair.second         , pt4_              );
    float effQuad45PFJetError   = getFitError(fTriggerFitCurves.fSingleMuon_Quad45_Efficiency_QuadPFCentralJetLooseID45Pair.second, pt4_              );

    float threeBtagEfficiency          = computeThreeBtagEfficiency(bTagEffJet0, bTagEffJet1, bTagEffJet2, bTagEffJet3);
    float threeBtagEfficiencyErrorUp   = computeThreeBtagEfficiency(bTagEffJet0 + bTagEffJet0Error, bTagEffJet1 + bTagEffJet1Error, bTagEffJet2 + bTagEffJet2Error, bTagEffJet3 + bTagEffJet3Error);
    float threeBtagEfficiencyErrorDown = computeThreeBtagEfficiency(bTagEffJet0 - bTagEffJet0Error, bTagEffJet1 - bTagEffJet1Error, bTagEffJet2 - bTagEffJet2Error, bTagEffJet3 - bTagEffJet3Error);
    
    theOutputTree_->userFloat("HLT_Data_QuadJet45_effL1"              ) = effL1              ;
    theOutputTree_->userFloat("HLT_Data_QuadJet45_effQuad45CaloJet"   ) = effQuad45CaloJet   ;
    theOutputTree_->userFloat("HLT_Data_QuadJet45_effQuad45PFJet"     ) = effQuad45PFJet     ;
    theOutputTree_->userFloat("HLT_Data_QuadJet45_threeBtagEfficiency") = threeBtagEfficiency;

    float efficiencyCentral = computeQuad45Efficiency(threeBtagEfficiency, effL1, effQuad45CaloJet, effQuad45PFJet);
    #ifdef useFit
        float efficiencyUp      = computeQuad45Efficiency(threeBtagEfficiencyErrorUp  , effL1 + effL1Error, effQuad45CaloJet + effQuad45CaloJetError, effQuad45PFJet + effQuad45PFJetError);
        float efficiencyDown    = computeQuad45Efficiency(threeBtagEfficiencyErrorDown, effL1 - effL1Error, effQuad45CaloJet - effQuad45CaloJetError, effQuad45PFJet - effQuad45PFJetError);
    #else
        float efficiencyUp      = computeQuad45Efficiency(bTagEffJet0Up  , bTagEffJet1Up  , bTagEffJet2Up  , bTagEffJet3Up  , effL1 + effL1Error, effQuad45CaloJet + effQuad45CaloJetError, effQuad45PFJet + effQuad45PFJetError);
        float efficiencyDown    = computeQuad45Efficiency(bTagEffJet0Down, bTagEffJet1Down, bTagEffJet2Down, bTagEffJet3Down, effL1 - effL1Error, effQuad45CaloJet - effQuad45CaloJetError, effQuad45PFJet - effQuad45PFJetError);
    #endif

    return {efficiencyCentral, efficiencyUp, efficiencyDown};
}

std::tuple<float, float, float> TriggerEfficiencyCalculator_2016::calculateDataAndEfficiency()
{
    float effL1            = fTriggerFitCurves.fSingleMuon_And_Efficiency_L1filterQuad45HTPair.first         ->Eval(sumPt_);
    float effQuad45CaloJet = fTriggerFitCurves.fSingleMuon_And_Efficiency_QuadCentralJet45Pair.first         ->Eval(pt4_  );
    float effQuad45PFJet   = fTriggerFitCurves.fSingleMuon_And_Efficiency_QuadPFCentralJetLooseID45Pair.first->Eval(pt4_  );

    float effL1Error            = getFitError(fTriggerFitCurves.fSingleMuon_And_Efficiency_L1filterQuad45HTPair.second         , sumPt_);
    float effQuad45CaloJetError = getFitError(fTriggerFitCurves.fSingleMuon_And_Efficiency_QuadCentralJet45Pair.second         , pt4_  );
    float effQuad45PFJetError   = getFitError(fTriggerFitCurves.fSingleMuon_And_Efficiency_QuadPFCentralJetLooseID45Pair.second, pt4_  );

    float efficiencyCentral = computeAndEfficiency(effL1, effQuad45CaloJet, effQuad45PFJet);
    float efficiencyUp      = computeAndEfficiency(effL1 + effL1Error, effQuad45CaloJet + effQuad45CaloJetError, effQuad45PFJet + effQuad45PFJetError);
    float efficiencyDown    = computeAndEfficiency(effL1 - effL1Error, effQuad45CaloJet - effQuad45CaloJetError, effQuad45PFJet - effQuad45PFJetError);

    theOutputTree_->userFloat("HLT_Data_And_effL1"              ) = effL1              ;
    theOutputTree_->userFloat("HLT_Data_And_effQuad45CaloJet"   ) = effQuad45CaloJet   ;
    theOutputTree_->userFloat("HLT_Data_And_effQuad45PFJet"     ) = effQuad45PFJet     ;

    return {efficiencyCentral, efficiencyUp, efficiencyDown};
}


std::tuple<float, float, float> TriggerEfficiencyCalculator_2016::calculateMonteCarloDouble90Double30Efficiency()
{
    #ifdef useFit
        float bTagEffJet0        = fTriggerFitCurves.fTTbar_Double90Quad30_Efficiency_BTagCaloCSVp087TriplePair.first      ->Eval(deepFlavBVector[0]);
        float bTagEffJet1        = fTriggerFitCurves.fTTbar_Double90Quad30_Efficiency_BTagCaloCSVp087TriplePair.first      ->Eval(deepFlavBVector[1]);
        float bTagEffJet2        = fTriggerFitCurves.fTTbar_Double90Quad30_Efficiency_BTagCaloCSVp087TriplePair.first      ->Eval(deepFlavBVector[2]);
        float bTagEffJet3        = fTriggerFitCurves.fTTbar_Double90Quad30_Efficiency_BTagCaloCSVp087TriplePair.first      ->Eval(deepFlavBVector[3]);
        float bTagEffJet0Error        = getFitError(fTriggerFitCurves.fTTbar_Double90Quad30_Efficiency_BTagCaloCSVp087TriplePair.second      , deepFlavBVector[0]);
        float bTagEffJet1Error        = getFitError(fTriggerFitCurves.fTTbar_Double90Quad30_Efficiency_BTagCaloCSVp087TriplePair.second      , deepFlavBVector[1]);
        float bTagEffJet2Error        = getFitError(fTriggerFitCurves.fTTbar_Double90Quad30_Efficiency_BTagCaloCSVp087TriplePair.second      , deepFlavBVector[2]);
        float bTagEffJet3Error        = getFitError(fTriggerFitCurves.fTTbar_Double90Quad30_Efficiency_BTagCaloCSVp087TriplePair.second      , deepFlavBVector[3]);
    #else
        // float bTagEffJet0        = getPointValue<0>(fTriggerFitCurves.fTTbar_Double90Quad30_Efficiency_BTagCaloCSVp087TripleGraphs, deepFlavBVector[0]);
        // float bTagEffJet1        = getPointValue<0>(fTriggerFitCurves.fTTbar_Double90Quad30_Efficiency_BTagCaloCSVp087TripleGraphs, deepFlavBVector[1]);
        // float bTagEffJet2        = getPointValue<0>(fTriggerFitCurves.fTTbar_Double90Quad30_Efficiency_BTagCaloCSVp087TripleGraphs, deepFlavBVector[2]);
        // float bTagEffJet3        = getPointValue<0>(fTriggerFitCurves.fTTbar_Double90Quad30_Efficiency_BTagCaloCSVp087TripleGraphs, deepFlavBVector[3]);
        // float bTagEffJet0Up      = getPointValue<1>(fTriggerFitCurves.fTTbar_Double90Quad30_Efficiency_BTagCaloCSVp087TripleGraphs, deepFlavBVector[0]);
        // float bTagEffJet1Up      = getPointValue<1>(fTriggerFitCurves.fTTbar_Double90Quad30_Efficiency_BTagCaloCSVp087TripleGraphs, deepFlavBVector[1]);
        // float bTagEffJet2Up      = getPointValue<1>(fTriggerFitCurves.fTTbar_Double90Quad30_Efficiency_BTagCaloCSVp087TripleGraphs, deepFlavBVector[2]);
        // float bTagEffJet3Up      = getPointValue<1>(fTriggerFitCurves.fTTbar_Double90Quad30_Efficiency_BTagCaloCSVp087TripleGraphs, deepFlavBVector[3]);
        // float bTagEffJet0Down    = getPointValue<2>(fTriggerFitCurves.fTTbar_Double90Quad30_Efficiency_BTagCaloCSVp087TripleGraphs, deepFlavBVector[0]);
        // float bTagEffJet1Down    = getPointValue<2>(fTriggerFitCurves.fTTbar_Double90Quad30_Efficiency_BTagCaloCSVp087TripleGraphs, deepFlavBVector[1]);
        // float bTagEffJet2Down    = getPointValue<2>(fTriggerFitCurves.fTTbar_Double90Quad30_Efficiency_BTagCaloCSVp087TripleGraphs, deepFlavBVector[2]);
        // float bTagEffJet3Down    = getPointValue<2>(fTriggerFitCurves.fTTbar_Double90Quad30_Efficiency_BTagCaloCSVp087TripleGraphs, deepFlavBVector[3]);
        float bTagEffJet0        = std::get<0>(fTriggerFitCurves.fTTbar_Double90Quad30_Efficiency_BTagCaloCSVp087TripleGraphs)  ->Eval(deepFlavBVector[0], 0, "S");
        float bTagEffJet1        = std::get<0>(fTriggerFitCurves.fTTbar_Double90Quad30_Efficiency_BTagCaloCSVp087TripleGraphs)  ->Eval(deepFlavBVector[1], 0, "S");
        float bTagEffJet2        = std::get<0>(fTriggerFitCurves.fTTbar_Double90Quad30_Efficiency_BTagCaloCSVp087TripleGraphs)  ->Eval(deepFlavBVector[2], 0, "S");
        float bTagEffJet3        = std::get<0>(fTriggerFitCurves.fTTbar_Double90Quad30_Efficiency_BTagCaloCSVp087TripleGraphs)  ->Eval(deepFlavBVector[3], 0, "S");
        float bTagEffJet0Up      = std::get<1>(fTriggerFitCurves.fTTbar_Double90Quad30_Efficiency_BTagCaloCSVp087TripleGraphs)  ->Eval(deepFlavBVector[0], 0, "S");
        float bTagEffJet1Up      = std::get<1>(fTriggerFitCurves.fTTbar_Double90Quad30_Efficiency_BTagCaloCSVp087TripleGraphs)  ->Eval(deepFlavBVector[1], 0, "S");
        float bTagEffJet2Up      = std::get<1>(fTriggerFitCurves.fTTbar_Double90Quad30_Efficiency_BTagCaloCSVp087TripleGraphs)  ->Eval(deepFlavBVector[2], 0, "S");
        float bTagEffJet3Up      = std::get<1>(fTriggerFitCurves.fTTbar_Double90Quad30_Efficiency_BTagCaloCSVp087TripleGraphs)  ->Eval(deepFlavBVector[3], 0, "S");
        float bTagEffJet0Down    = std::get<2>(fTriggerFitCurves.fTTbar_Double90Quad30_Efficiency_BTagCaloCSVp087TripleGraphs)  ->Eval(deepFlavBVector[0], 0, "S");
        float bTagEffJet1Down    = std::get<2>(fTriggerFitCurves.fTTbar_Double90Quad30_Efficiency_BTagCaloCSVp087TripleGraphs)  ->Eval(deepFlavBVector[1], 0, "S");
        float bTagEffJet2Down    = std::get<2>(fTriggerFitCurves.fTTbar_Double90Quad30_Efficiency_BTagCaloCSVp087TripleGraphs)  ->Eval(deepFlavBVector[2], 0, "S");
        float bTagEffJet3Down    = std::get<2>(fTriggerFitCurves.fTTbar_Double90Quad30_Efficiency_BTagCaloCSVp087TripleGraphs)  ->Eval(deepFlavBVector[3], 0, "S");
    #endif

    float effL1              = fTriggerFitCurves.fTTbar_Double90Quad30_Efficiency_L1filterHTPair.first                 ->Eval(sumPt_            );
    float effQuad30CaloJet   = fTriggerFitCurves.fTTbar_Double90Quad30_Efficiency_QuadCentralJet30Pair.first           ->Eval(pt4_              );
    float effDouble90CaloJet = fTriggerFitCurves.fTTbar_Double90Quad30_Efficiency_DoubleCentralJet90Pair.first         ->Eval(pt2_              );
    float effQuad30PFJet     = fTriggerFitCurves.fTTbar_Double90Quad30_Efficiency_QuadPFCentralJetLooseID30Pair.first  ->Eval(pt4_              );
    float effDouble90PFJet   = fTriggerFitCurves.fTTbar_Double90Quad30_Efficiency_DoublePFCentralJetLooseID90Pair.first->Eval(pt2_              );

    float effL1Error              = getFitError(fTriggerFitCurves.fTTbar_Double90Quad30_Efficiency_L1filterHTPair.second                 , sumPt_            );
    float effQuad30CaloJetError   = getFitError(fTriggerFitCurves.fTTbar_Double90Quad30_Efficiency_QuadCentralJet30Pair.second           , pt4_              );
    float effDouble90CaloJetError = getFitError(fTriggerFitCurves.fTTbar_Double90Quad30_Efficiency_DoubleCentralJet90Pair.second         , pt2_              );
    float effQuad30PFJetError     = getFitError(fTriggerFitCurves.fTTbar_Double90Quad30_Efficiency_QuadPFCentralJetLooseID30Pair.second  , pt4_              );
    float effDouble90PFJetError   = getFitError(fTriggerFitCurves.fTTbar_Double90Quad30_Efficiency_DoublePFCentralJetLooseID90Pair.second, pt2_              );

    float threeBtagEfficiency          = computeThreeBtagEfficiency(bTagEffJet0, bTagEffJet1, bTagEffJet2, bTagEffJet3);
    float threeBtagEfficiencyErrorUp   = computeThreeBtagEfficiency(bTagEffJet0 + bTagEffJet0Error, bTagEffJet1 + bTagEffJet1Error, bTagEffJet2 + bTagEffJet2Error, bTagEffJet3 + bTagEffJet3Error);
    float threeBtagEfficiencyErrorDown = computeThreeBtagEfficiency(bTagEffJet0 - bTagEffJet0Error, bTagEffJet1 - bTagEffJet1Error, bTagEffJet2 - bTagEffJet2Error, bTagEffJet3 - bTagEffJet3Error);
    
    theOutputTree_->userFloat("HLT_MC_DoubleJet90_Double30_effL1"              ) = effL1              ;
    theOutputTree_->userFloat("HLT_MC_DoubleJet90_Double30_effQuad30CaloJet"   ) = effQuad30CaloJet   ;
    theOutputTree_->userFloat("HLT_MC_DoubleJet90_Double30_effDouble90CaloJet" ) = effDouble90CaloJet ;
    theOutputTree_->userFloat("HLT_MC_DoubleJet90_Double30_effQuad30PFJet"     ) = effQuad30PFJet     ;
    theOutputTree_->userFloat("HLT_MC_DoubleJet90_Double30_effDouble90PFJet"   ) = effDouble90PFJet   ;
    theOutputTree_->userFloat("HLT_MC_DoubleJet90_Double30_threeBtagEfficiency") = threeBtagEfficiency;

    float efficiencyCentral = computeDouble90Double30Efficiency(threeBtagEfficiency, effL1, effQuad30CaloJet, effDouble90CaloJet, effQuad30PFJet, effDouble90PFJet);
    #ifdef useFit
        float efficiencyUp      = computeDouble90Double30Efficiency(threeBtagEfficiencyErrorUp  , effL1 + effL1Error, effQuad30CaloJet + effQuad30CaloJetError, effDouble90CaloJet + effDouble90CaloJetError, effQuad30PFJet + effQuad30PFJetError, effDouble90PFJet + effDouble90PFJetError);
        float efficiencyDown    = computeDouble90Double30Efficiency(threeBtagEfficiencyErrorDown, effL1 - effL1Error, effQuad30CaloJet - effQuad30CaloJetError, effDouble90CaloJet - effDouble90CaloJetError, effQuad30PFJet - effQuad30PFJetError, effDouble90PFJet - effDouble90PFJetError);
    #else
        float efficiencyUp      = computeDouble90Double30Efficiency(bTagEffJet0Up  , bTagEffJet1Up  , bTagEffJet2Up  , bTagEffJet3Up  , effL1 + effL1Error, effQuad30CaloJet + effQuad30CaloJetError, effDouble90CaloJet + effDouble90CaloJetError, effQuad30PFJet + effQuad30PFJetError, effDouble90PFJet + effDouble90PFJetError);
        float efficiencyDown    = computeDouble90Double30Efficiency(bTagEffJet0Down, bTagEffJet1Down, bTagEffJet2Down, bTagEffJet3Down, effL1 - effL1Error, effQuad30CaloJet - effQuad30CaloJetError, effDouble90CaloJet - effDouble90CaloJetError, effQuad30PFJet - effQuad30PFJetError, effDouble90PFJet - effDouble90PFJetError);
    #endif

    return {efficiencyCentral, efficiencyUp, efficiencyDown};
}

std::tuple<float, float, float> TriggerEfficiencyCalculator_2016::calculateMonteCarloQuad45Efficiency()
{
    
    #ifdef useFit
        float bTagEffJet0      = fTriggerFitCurves.fTTbar_Quad45_Efficiency_BTagCaloCSVp087TriplePair.first    ->Eval(deepFlavBVector[0]);
        float bTagEffJet1      = fTriggerFitCurves.fTTbar_Quad45_Efficiency_BTagCaloCSVp087TriplePair.first    ->Eval(deepFlavBVector[1]);
        float bTagEffJet2      = fTriggerFitCurves.fTTbar_Quad45_Efficiency_BTagCaloCSVp087TriplePair.first    ->Eval(deepFlavBVector[2]);
        float bTagEffJet3      = fTriggerFitCurves.fTTbar_Quad45_Efficiency_BTagCaloCSVp087TriplePair.first    ->Eval(deepFlavBVector[3]);
        float bTagEffJet0Error      = getFitError(fTriggerFitCurves.fTTbar_Quad45_Efficiency_BTagCaloCSVp087TriplePair.second    , deepFlavBVector[0]);
        float bTagEffJet1Error      = getFitError(fTriggerFitCurves.fTTbar_Quad45_Efficiency_BTagCaloCSVp087TriplePair.second    , deepFlavBVector[1]);
        float bTagEffJet2Error      = getFitError(fTriggerFitCurves.fTTbar_Quad45_Efficiency_BTagCaloCSVp087TriplePair.second    , deepFlavBVector[2]);
        float bTagEffJet3Error      = getFitError(fTriggerFitCurves.fTTbar_Quad45_Efficiency_BTagCaloCSVp087TriplePair.second    , deepFlavBVector[3]);
    #else
        // float bTagEffJet0        = getPointValue<0>(fTriggerFitCurves.fTTbar_Quad45_Efficiency_BTagCaloCSVp087TripleGraphs, deepFlavBVector[0]);
        // float bTagEffJet1        = getPointValue<0>(fTriggerFitCurves.fTTbar_Quad45_Efficiency_BTagCaloCSVp087TripleGraphs, deepFlavBVector[1]);
        // float bTagEffJet2        = getPointValue<0>(fTriggerFitCurves.fTTbar_Quad45_Efficiency_BTagCaloCSVp087TripleGraphs, deepFlavBVector[2]);
        // float bTagEffJet3        = getPointValue<0>(fTriggerFitCurves.fTTbar_Quad45_Efficiency_BTagCaloCSVp087TripleGraphs, deepFlavBVector[3]);
        // float bTagEffJet0Up      = getPointValue<1>(fTriggerFitCurves.fTTbar_Quad45_Efficiency_BTagCaloCSVp087TripleGraphs, deepFlavBVector[0]);
        // float bTagEffJet1Up      = getPointValue<1>(fTriggerFitCurves.fTTbar_Quad45_Efficiency_BTagCaloCSVp087TripleGraphs, deepFlavBVector[1]);
        // float bTagEffJet2Up      = getPointValue<1>(fTriggerFitCurves.fTTbar_Quad45_Efficiency_BTagCaloCSVp087TripleGraphs, deepFlavBVector[2]);
        // float bTagEffJet3Up      = getPointValue<1>(fTriggerFitCurves.fTTbar_Quad45_Efficiency_BTagCaloCSVp087TripleGraphs, deepFlavBVector[3]);
        // float bTagEffJet0Down    = getPointValue<2>(fTriggerFitCurves.fTTbar_Quad45_Efficiency_BTagCaloCSVp087TripleGraphs, deepFlavBVector[0]);
        // float bTagEffJet1Down    = getPointValue<2>(fTriggerFitCurves.fTTbar_Quad45_Efficiency_BTagCaloCSVp087TripleGraphs, deepFlavBVector[1]);
        // float bTagEffJet2Down    = getPointValue<2>(fTriggerFitCurves.fTTbar_Quad45_Efficiency_BTagCaloCSVp087TripleGraphs, deepFlavBVector[2]);
        // float bTagEffJet3Down    = getPointValue<2>(fTriggerFitCurves.fTTbar_Quad45_Efficiency_BTagCaloCSVp087TripleGraphs, deepFlavBVector[3]);
        float bTagEffJet0        = std::get<0>(fTriggerFitCurves.fTTbar_Quad45_Efficiency_BTagCaloCSVp087TripleGraphs)  ->Eval(deepFlavBVector[0], 0, "S");
        float bTagEffJet1        = std::get<0>(fTriggerFitCurves.fTTbar_Quad45_Efficiency_BTagCaloCSVp087TripleGraphs)  ->Eval(deepFlavBVector[1], 0, "S");
        float bTagEffJet2        = std::get<0>(fTriggerFitCurves.fTTbar_Quad45_Efficiency_BTagCaloCSVp087TripleGraphs)  ->Eval(deepFlavBVector[2], 0, "S");
        float bTagEffJet3        = std::get<0>(fTriggerFitCurves.fTTbar_Quad45_Efficiency_BTagCaloCSVp087TripleGraphs)  ->Eval(deepFlavBVector[3], 0, "S");
        float bTagEffJet0Up      = std::get<1>(fTriggerFitCurves.fTTbar_Quad45_Efficiency_BTagCaloCSVp087TripleGraphs)  ->Eval(deepFlavBVector[0], 0, "S");
        float bTagEffJet1Up      = std::get<1>(fTriggerFitCurves.fTTbar_Quad45_Efficiency_BTagCaloCSVp087TripleGraphs)  ->Eval(deepFlavBVector[1], 0, "S");
        float bTagEffJet2Up      = std::get<1>(fTriggerFitCurves.fTTbar_Quad45_Efficiency_BTagCaloCSVp087TripleGraphs)  ->Eval(deepFlavBVector[2], 0, "S");
        float bTagEffJet3Up      = std::get<1>(fTriggerFitCurves.fTTbar_Quad45_Efficiency_BTagCaloCSVp087TripleGraphs)  ->Eval(deepFlavBVector[3], 0, "S");
        float bTagEffJet0Down    = std::get<2>(fTriggerFitCurves.fTTbar_Quad45_Efficiency_BTagCaloCSVp087TripleGraphs)  ->Eval(deepFlavBVector[0], 0, "S");
        float bTagEffJet1Down    = std::get<2>(fTriggerFitCurves.fTTbar_Quad45_Efficiency_BTagCaloCSVp087TripleGraphs)  ->Eval(deepFlavBVector[1], 0, "S");
        float bTagEffJet2Down    = std::get<2>(fTriggerFitCurves.fTTbar_Quad45_Efficiency_BTagCaloCSVp087TripleGraphs)  ->Eval(deepFlavBVector[2], 0, "S");
        float bTagEffJet3Down    = std::get<2>(fTriggerFitCurves.fTTbar_Quad45_Efficiency_BTagCaloCSVp087TripleGraphs)  ->Eval(deepFlavBVector[3], 0, "S");
    #endif

    float effL1            = fTriggerFitCurves.fTTbar_Quad45_Efficiency_L1filterHTPair.first               ->Eval(sumPt_            );
    float effQuad45CaloJet = fTriggerFitCurves.fTTbar_Quad45_Efficiency_QuadCentralJet45Pair.first         ->Eval(pt4_              );
    float effQuad45PFJet   = fTriggerFitCurves.fTTbar_Quad45_Efficiency_QuadPFCentralJetLooseID45Pair.first->Eval(pt4_              );

    float effL1Error            = getFitError(fTriggerFitCurves.fTTbar_Quad45_Efficiency_L1filterHTPair.second               , sumPt_            );
    float effQuad45CaloJetError = getFitError(fTriggerFitCurves.fTTbar_Quad45_Efficiency_QuadCentralJet45Pair.second         , pt4_              );
    float effQuad45PFJetError   = getFitError(fTriggerFitCurves.fTTbar_Quad45_Efficiency_QuadPFCentralJetLooseID45Pair.second, pt4_              );

    float threeBtagEfficiency          = computeThreeBtagEfficiency(bTagEffJet0, bTagEffJet1, bTagEffJet2, bTagEffJet3);
    float threeBtagEfficiencyErrorUp   = computeThreeBtagEfficiency(bTagEffJet0 + bTagEffJet0Error, bTagEffJet1 + bTagEffJet1Error, bTagEffJet2 + bTagEffJet2Error, bTagEffJet3 + bTagEffJet3Error);
    float threeBtagEfficiencyErrorDown = computeThreeBtagEfficiency(bTagEffJet0 - bTagEffJet0Error, bTagEffJet1 - bTagEffJet1Error, bTagEffJet2 - bTagEffJet2Error, bTagEffJet3 - bTagEffJet3Error);

    theOutputTree_->userFloat("HLT_MC_QuadJet45_effL1"              ) = effL1              ;
    theOutputTree_->userFloat("HLT_MC_QuadJet45_effQuad45CaloJet"   ) = effQuad45CaloJet   ;
    theOutputTree_->userFloat("HLT_MC_QuadJet45_effQuad45PFJet"     ) = effQuad45PFJet     ;
    theOutputTree_->userFloat("HLT_MC_QuadJet45_threeBtagEfficiency") = threeBtagEfficiency;

    float efficiencyCentral = computeQuad45Efficiency(threeBtagEfficiency, effL1, effQuad45CaloJet, effQuad45PFJet);
    #ifdef useFit
        float efficiencyUp      = computeQuad45Efficiency(threeBtagEfficiencyErrorUp  , effL1 + effL1Error, effQuad45CaloJet + effQuad45CaloJetError, effQuad45PFJet + effQuad45PFJetError);
        float efficiencyDown    = computeQuad45Efficiency(threeBtagEfficiencyErrorDown, effL1 - effL1Error, effQuad45CaloJet - effQuad45CaloJetError, effQuad45PFJet - effQuad45PFJetError);
    #else
        float efficiencyUp      = computeQuad45Efficiency(bTagEffJet0Up  , bTagEffJet1Up  , bTagEffJet2Up  , bTagEffJet3Up  , effL1 + effL1Error, effQuad45CaloJet + effQuad45CaloJetError, effQuad45PFJet + effQuad45PFJetError);
        float efficiencyDown    = computeQuad45Efficiency(bTagEffJet0Down, bTagEffJet1Down, bTagEffJet2Down, bTagEffJet3Down, effL1 - effL1Error, effQuad45CaloJet - effQuad45CaloJetError, effQuad45PFJet - effQuad45PFJetError);
    #endif

    return {efficiencyCentral, efficiencyUp, efficiencyDown};
}

std::tuple<float, float, float> TriggerEfficiencyCalculator_2016::calculateMonteCarloAndEfficiency()
{
    float effL1            = fTriggerFitCurves.fTTbar_And_Efficiency_L1filterQuad45HTPair.first         ->Eval(sumPt_);
    float effQuad45CaloJet = fTriggerFitCurves.fTTbar_And_Efficiency_QuadCentralJet45Pair.first         ->Eval(pt4_  );
    float effQuad45PFJet   = fTriggerFitCurves.fTTbar_And_Efficiency_QuadPFCentralJetLooseID45Pair.first->Eval(pt4_  );

    float effL1Error            = getFitError(fTriggerFitCurves.fTTbar_And_Efficiency_L1filterQuad45HTPair.second         , sumPt_);
    float effQuad45CaloJetError = getFitError(fTriggerFitCurves.fTTbar_And_Efficiency_QuadCentralJet45Pair.second         , pt4_  );
    float effQuad45PFJetError   = getFitError(fTriggerFitCurves.fTTbar_And_Efficiency_QuadPFCentralJetLooseID45Pair.second, pt4_  );

    float efficiencyCentral = computeAndEfficiency(effL1, effQuad45CaloJet, effQuad45PFJet);
    float efficiencyUp      = computeAndEfficiency(effL1 + effL1Error, effQuad45CaloJet + effQuad45CaloJetError, effQuad45PFJet + effQuad45PFJetError);
    float efficiencyDown    = computeAndEfficiency(effL1 - effL1Error, effQuad45CaloJet - effQuad45CaloJetError, effQuad45PFJet - effQuad45PFJetError);

    theOutputTree_->userFloat("HLT_MC_And_effL1"              ) = effL1              ;
    theOutputTree_->userFloat("HLT_MC_And_effQuad45CaloJet"   ) = effQuad45CaloJet   ;
    theOutputTree_->userFloat("HLT_MC_And_effQuad45PFJet"     ) = effQuad45PFJet     ;

    return {efficiencyCentral, efficiencyUp, efficiencyDown};
}


void TriggerEfficiencyCalculator_2016::extractInformationFromEvent(std::vector<Jet> selectedJets)
{
  
    assert(selectedJets.size()==4);

    uint16_t positionInVector = 0;
    for(const auto& theJet : selectedJets)
    {
        deepFlavBVector[positionInVector++] = get_property(theJet, Jet_btagDeepFlavB); //This has to be the deep flavor!!
    }
    
    stable_sort(selectedJets.begin(), selectedJets.end(), [](const Jet & a, const Jet & b) -> bool
    {
        return ( a.P4().Pt() > b.P4().Pt() );
    });

    pt2_ = selectedJets[1].P4().Pt();
    pt4_ = selectedJets[3].P4().Pt();

    sumPt_ = 0;
    for (uint ij = 0; ij < *(theNanoAODTree_.nJet); ++ij)
    {
        // here preselect jets
        Jet jet (ij, &theNanoAODTree_);

        bool isMuon = false;
        for (uint candIt = 0; candIt < *(theNanoAODTree_.nMuon); ++candIt)
        {
            Muon theMuon (candIt, &theNanoAODTree_);
            if(get_property(theMuon, Muon_pfRelIso04_all) > 0.3) continue;
            if(jet.getIdx() == get_property(theMuon, Muon_jetIdx))
            {
                isMuon = true;
                break;
            }
        }
        if(isMuon) continue;

        if (jet.P4().Pt() >= 30. && std::abs(jet.P4().Eta()) < 2.5) sumPt_ += jet.P4().Pt();
    }

    theOutputTree_->userFloat("HLT_Pt2"  ) = pt2_  ;
    theOutputTree_->userFloat("HLT_Pt4"  ) = pt4_  ;
    theOutputTree_->userFloat("HLT_SumPt") = sumPt_;

}


void  TriggerEfficiencyCalculator_2016::createTriggerSimulatedBranches()
{
    theOutputTree_->declareUserIntBranch("HLT_DoubleJet90_Double30_TripleBTagCSV_p087_Simulated"      , 0);
    theOutputTree_->declareUserIntBranch("HLT_DoubleJet90_Double30_TripleBTagCSV_p087_SimulatedUp"    , 0);
    theOutputTree_->declareUserIntBranch("HLT_DoubleJet90_Double30_TripleBTagCSV_p087_SimulatedDown"  , 0);

    theOutputTree_->declareUserIntBranch("HLT_DoubleJet90_Double30_TripleBTagCSV_p087_SimulatedMc"    , 0);
    theOutputTree_->declareUserIntBranch("HLT_DoubleJet90_Double30_TripleBTagCSV_p087_SimulatedMcUp"  , 0);
    theOutputTree_->declareUserIntBranch("HLT_DoubleJet90_Double30_TripleBTagCSV_p087_SimulatedMcDown", 0);

    theOutputTree_->declareUserIntBranch("HLT_QuadJet45_TripleBTagCSV_p087_Simulated"                 , 0);
    theOutputTree_->declareUserIntBranch("HLT_QuadJet45_TripleBTagCSV_p087_SimulatedUp"               , 0);
    theOutputTree_->declareUserIntBranch("HLT_QuadJet45_TripleBTagCSV_p087_SimulatedDown"             , 0);

    theOutputTree_->declareUserIntBranch("HLT_QuadJet45_TripleBTagCSV_p087_SimulatedMc"               , 0);
    theOutputTree_->declareUserIntBranch("HLT_QuadJet45_TripleBTagCSV_p087_SimulatedMcUp"             , 0);
    theOutputTree_->declareUserIntBranch("HLT_QuadJet45_TripleBTagCSV_p087_SimulatedMcDown"           , 0);

    theOutputTree_->declareUserIntBranch("HLT_Simulated"                 , 0);
    theOutputTree_->declareUserIntBranch("HLT_SimulatedUp"               , 0);
    theOutputTree_->declareUserIntBranch("HLT_SimulatedDown"             , 0);

    theOutputTree_->declareUserIntBranch("HLT_SimulatedMc"               , 0);
    theOutputTree_->declareUserIntBranch("HLT_SimulatedMcUp"             , 0);
    theOutputTree_->declareUserIntBranch("HLT_SimulatedMcDown"           , 0);

    theOutputTree_->declareUserFloatBranch("HLT_Pt2"             , 0);
    theOutputTree_->declareUserFloatBranch("HLT_Pt4"             , 0);
    theOutputTree_->declareUserFloatBranch("HLT_SumPt"           , 0);

    theOutputTree_->declareUserFloatBranch("HLT_MC_DoubleJet90_Double30_effL1"              , 0.);
    theOutputTree_->declareUserFloatBranch("HLT_MC_DoubleJet90_Double30_effQuad30CaloJet"   , 0.);
    theOutputTree_->declareUserFloatBranch("HLT_MC_DoubleJet90_Double30_effDouble90CaloJet" , 0.);
    theOutputTree_->declareUserFloatBranch("HLT_MC_DoubleJet90_Double30_effQuad30PFJet"     , 0.);
    theOutputTree_->declareUserFloatBranch("HLT_MC_DoubleJet90_Double30_effDouble90PFJet"   , 0.);
    theOutputTree_->declareUserFloatBranch("HLT_MC_DoubleJet90_Double30_threeBtagEfficiency", 0.);

    theOutputTree_->declareUserFloatBranch("HLT_MC_QuadJet45_effL1"              , 0.);
    theOutputTree_->declareUserFloatBranch("HLT_MC_QuadJet45_effQuad45CaloJet"   , 0.);
    theOutputTree_->declareUserFloatBranch("HLT_MC_QuadJet45_effQuad45PFJet"     , 0.);
    theOutputTree_->declareUserFloatBranch("HLT_MC_QuadJet45_threeBtagEfficiency", 0.);

    theOutputTree_->declareUserFloatBranch("HLT_MC_And_effL1"              , 0.);
    theOutputTree_->declareUserFloatBranch("HLT_MC_And_effQuad45CaloJet"   , 0.);
    theOutputTree_->declareUserFloatBranch("HLT_MC_And_effQuad45PFJet"     , 0.);


    theOutputTree_->declareUserFloatBranch("HLT_Data_DoubleJet90_Double30_effL1"              , 0.);
    theOutputTree_->declareUserFloatBranch("HLT_Data_DoubleJet90_Double30_effQuad30CaloJet"   , 0.);
    theOutputTree_->declareUserFloatBranch("HLT_Data_DoubleJet90_Double30_effDouble90CaloJet" , 0.);
    theOutputTree_->declareUserFloatBranch("HLT_Data_DoubleJet90_Double30_effQuad30PFJet"     , 0.);
    theOutputTree_->declareUserFloatBranch("HLT_Data_DoubleJet90_Double30_effDouble90PFJet"   , 0.);
    theOutputTree_->declareUserFloatBranch("HLT_Data_DoubleJet90_Double30_threeBtagEfficiency", 0.);

    theOutputTree_->declareUserFloatBranch("HLT_Data_QuadJet45_effL1"              , 0.);
    theOutputTree_->declareUserFloatBranch("HLT_Data_QuadJet45_effQuad45CaloJet"   , 0.);
    theOutputTree_->declareUserFloatBranch("HLT_Data_QuadJet45_effQuad45PFJet"     , 0.);
    theOutputTree_->declareUserFloatBranch("HLT_Data_QuadJet45_threeBtagEfficiency", 0.);

    theOutputTree_->declareUserFloatBranch("HLT_Data_And_effL1"              , 0.);
    theOutputTree_->declareUserFloatBranch("HLT_Data_And_effQuad45CaloJet"   , 0.);
    theOutputTree_->declareUserFloatBranch("HLT_Data_And_effQuad45PFJet"     , 0.);

}


*/

// 2017
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
TriggerEfficiencyCalculator_2017::TriggerEfficiencyCalculator_2017(std::string inputFileName, NanoAODTree& nat)
: TriggerEfficiencyCalculator(nat)
, fTriggerFitCurves(inputFileName)
{}

TriggerEfficiencyCalculator_2017::~TriggerEfficiencyCalculator_2017()
{}

void  TriggerEfficiencyCalculator_2017::createTriggerSimulatedBranches()
{
  /*
    theOutputTree_->declareUserFloatBranch("HLT_Pt1"             , 0);
    theOutputTree_->declareUserFloatBranch("HLT_Pt2"             , 0);
    theOutputTree_->declareUserFloatBranch("HLT_Pt3"             , 0);
    theOutputTree_->declareUserFloatBranch("HLT_Pt4"             , 0);
    theOutputTree_->declareUserFloatBranch("HLT_SumPtCaloJet"    , 0.);
    theOutputTree_->declareUserFloatBranch("HLT_SumPtPfJet"      , 0.);
    theOutputTree_->declareUserFloatBranch("HLT_SumPtJetOnly"    , 0.);
  */
  
  theOutputTree_->declareUserFloatBranch("HLT_Data_effL1"              , 0.);
  theOutputTree_->declareUserFloatBranch("HLT_Data_effQuad30CaloJet"   , 0.);
  theOutputTree_->declareUserFloatBranch("HLT_Data_effCaloHT"          , 0.);
  theOutputTree_->declareUserFloatBranch("HLT_Data_effQuad30PFJet"     , 0.);
  theOutputTree_->declareUserFloatBranch("HLT_Data_effSingle75PFJet"   , 0.);
  theOutputTree_->declareUserFloatBranch("HLT_Data_effDouble60PFJet"   , 0.);
  theOutputTree_->declareUserFloatBranch("HLT_Data_effTriple54PFJet"   , 0.);
  theOutputTree_->declareUserFloatBranch("HLT_Data_effQuad40PFJet"     , 0.);
  theOutputTree_->declareUserFloatBranch("HLT_Data_effPFHT"            , 0.);
  theOutputTree_->declareUserFloatBranch("HLT_Data_threeBtagEfficiency", 0.);
  theOutputTree_->declareUserFloatBranch("HLT_Data_twoBtagEfficiency"  , 0.);
  
  theOutputTree_->declareUserFloatBranch("HLT_MC_effL1"              , 0.);
  theOutputTree_->declareUserFloatBranch("HLT_MC_effQuad30CaloJet"   , 0.);
  theOutputTree_->declareUserFloatBranch("HLT_MC_effCaloHT"          , 0.);
  theOutputTree_->declareUserFloatBranch("HLT_MC_effQuad30PFJet"     , 0.);
  theOutputTree_->declareUserFloatBranch("HLT_MC_effSingle75PFJet"   , 0.);
  theOutputTree_->declareUserFloatBranch("HLT_MC_effDouble60PFJet"   , 0.);
  theOutputTree_->declareUserFloatBranch("HLT_MC_effTriple54PFJet"   , 0.);
  theOutputTree_->declareUserFloatBranch("HLT_MC_effQuad40PFJet"     , 0.);
  theOutputTree_->declareUserFloatBranch("HLT_MC_effPFHT"            , 0.);
  theOutputTree_->declareUserFloatBranch("HLT_MC_threeBtagEfficiency", 0.);
  theOutputTree_->declareUserFloatBranch("HLT_MC_twoBtagEfficiency"  , 0.);
}

void TriggerEfficiencyCalculator_2017::extractInformationFromEvent(std::vector<Jet> selectedJets)
{
  // Sort jets by b-tagging score
  std::sort(selectedJets.begin(), selectedJets.end(),[](Jet& j1, Jet& j2){ return j1.get_btag()>j2.get_btag();});
  for(unsigned int i=0; i<selectedJets.size(); i++)
    {
      // Keep only the leading four in b-tagging score jets
      if (i > 3) break;
      deepFlavBVector[i] = get_property(selectedJets.at(i), Jet_btagDeepFlavB);
    }
  
  // Sort jets by pT
  stable_sort(selectedJets.begin(), selectedJets.end(), [](const Jet & a, const Jet & b) -> bool{return (a.P4().Pt() > b.P4().Pt()); });

  // Save the pT of the leading four jets
  pt1_ = selectedJets[0].P4().Pt();
  pt2_ = selectedJets[1].P4().Pt();
  pt3_ = selectedJets[2].P4().Pt();
  pt4_ = selectedJets[3].P4().Pt();
  
  // Calculate the event sums
  caloJetSum_ = 0.;
  pfJetSum_   = 0.;
  onlyJetSum_ = 0.;
  for (uint ij = 0; ij < *(theNanoAODTree_.nJet); ++ij)
    {
      // here preselect jets
      Jet jet (ij, &theNanoAODTree_);
      
      if (jet.P4().Pt() >= 30. && std::abs(jet.P4().Eta()) < 2.5) pfJetSum_ += jet.P4().Pt();
      
      bool isMuon = false;
      for (uint candIt = 0; candIt < *(theNanoAODTree_.nMuon); ++candIt)
        {
	  Muon theMuon (candIt, &theNanoAODTree_);
	  if(get_property(theMuon, Muon_pfRelIso04_all) > 0.3) continue;
	  if(jet.getIdx() == get_property(theMuon, Muon_jetIdx))
            {
	      isMuon = true;
	      break;
            }
        }
      if(isMuon) continue;
      
      if (jet.P4().Pt() >= 30. && std::abs(jet.P4().Eta()) < 2.5) caloJetSum_ += jet.P4().Pt();
      
      bool isElectron = false;
      for (uint candIt = 0; candIt < *(theNanoAODTree_.nElectron); ++candIt)
        {
	  Electron theElectron (candIt, &theNanoAODTree_);
	  if(get_property(theElectron, Electron_pfRelIso03_all) > 0.3) continue;
	  if(jet.getIdx() == get_property(theElectron, Electron_jetIdx))
            {
	      isElectron = true;
	      break;
            }
        }
      if(isElectron) continue;
      
      if (jet.P4().Pt() >= 30. && std::abs(jet.P4().Eta()) < 2.5) onlyJetSum_ += jet.P4().Pt();
    }  
}

std::tuple<float, float, float> TriggerEfficiencyCalculator_2017::calculateDataTriggerEfficiency()
{
  if (0) std::cout << "\n====== 2017 Data Trigger Efficiency"<<std::endl;
#ifdef useFit
  std::vector<float> bTagEffJetsForDouble;
  std::vector<float> bTagEffJetsForDoubleError;
  std::vector<float> bTagEffJetsForTriple;
  std::vector<float> bTagEffJetsForTripleError;
  for (unsigned int i=0; i<deepFlavBVector.size(); i++)
    {
      bTagEffJetsForDouble.push_back(fTriggerFitCurves.fSingleMuon__Efficiency_BTagCaloCSVp05DoublePair.first->Eval(deepFlavBVector.at(i)));
      bTagEffJetsForDoubleError.push_back(getFitError(fTriggerFitCurves.fSingleMuon__Efficiency_BTagCaloCSVp05DoublePair.second, deepFlavBVector.at(i)));
      bTagEffJetsForTriple.push_back(fTriggerFitCurves.fSingleMuon__Efficiency_BTagPFCSVp070TriplePair.first->Eval(deepFlavBVector.at(i)));
      bTagEffJetsForTripleError.push_back(getFitError(fTriggerFitCurves.fSingleMuon__Efficiency_BTagPFCSVp070TriplePair.second, deepFlavBVector.at(i)));
    }
#else
  static_assert(false, "Do not use fit not implemented for TriggerEfficiencyCalculator_2017");
#endif
  
  float effL1            = fTriggerFitCurves.fSingleMuon__Efficiency_L1filterHTPair.first                     ->Eval(caloJetSum_);
  float effQuad30CaloJet = fTriggerFitCurves.fSingleMuon__Efficiency_QuadCentralJet30Pair.first               ->Eval(pt4_       );
  float effCaloHT        = fTriggerFitCurves.fSingleMuon__Efficiency_CaloQuadJet30HT300Pair.first             ->Eval(caloJetSum_);
  float effQuad30PFJet   = fTriggerFitCurves.fSingleMuon__Efficiency_PFCentralJetLooseIDQuad30Pair.first      ->Eval(pt4_       );
  float effSingle75PFJet = fTriggerFitCurves.fSingleMuon__Efficiency_1PFCentralJetLooseID75Pair.first         ->Eval(pt1_       );
  float effDouble60PFJet = fTriggerFitCurves.fSingleMuon__Efficiency_2PFCentralJetLooseID60Pair.first         ->Eval(pt2_       );
  float effTriple54PFJet = fTriggerFitCurves.fSingleMuon__Efficiency_3PFCentralJetLooseID45Pair.first         ->Eval(pt3_       );
  float effQuad40PFJet   = fTriggerFitCurves.fSingleMuon__Efficiency_4PFCentralJetLooseID40Pair.first         ->Eval(pt4_       );
  float effPFHT          = fTriggerFitCurves.fSingleMuon__Efficiency_PFCentralJetsLooseIDQuad30HT300Pair.first->Eval(pfJetSum_  );
  
  float effL1Error            = getFitError(fTriggerFitCurves.fSingleMuon__Efficiency_L1filterHTPair.second                     , caloJetSum_);
  float effQuad30CaloJetError = getFitError(fTriggerFitCurves.fSingleMuon__Efficiency_QuadCentralJet30Pair.second               , pt4_       );
  float effCaloHTError        = getFitError(fTriggerFitCurves.fSingleMuon__Efficiency_CaloQuadJet30HT300Pair.second             , caloJetSum_);
  float effQuad30PFJetError   = getFitError(fTriggerFitCurves.fSingleMuon__Efficiency_PFCentralJetLooseIDQuad30Pair.second      , pt4_       );
  float effSingle75PFJetError = getFitError(fTriggerFitCurves.fSingleMuon__Efficiency_1PFCentralJetLooseID75Pair.second         , pt1_       );
  float effDouble60PFJetError = getFitError(fTriggerFitCurves.fSingleMuon__Efficiency_2PFCentralJetLooseID60Pair.second         , pt2_       );
  float effTriple54PFJetError = getFitError(fTriggerFitCurves.fSingleMuon__Efficiency_3PFCentralJetLooseID45Pair.second         , pt3_       );
  float effQuad40PFJetError   = getFitError(fTriggerFitCurves.fSingleMuon__Efficiency_4PFCentralJetLooseID40Pair.second         , pt4_       );
  float effPFHTError          = getFitError(fTriggerFitCurves.fSingleMuon__Efficiency_PFCentralJetsLooseIDQuad30HT300Pair.second, pfJetSum_  );
  
  //================================================================================================================================================================================
  float threeBtagEfficiency          = computeThreeBtagEfficiency(bTagEffJetsForTriple.at(0), bTagEffJetsForTriple.at(1), bTagEffJetsForTriple.at(2), bTagEffJetsForTriple.at(3));
  float threeBtagEfficiencyErrorUp   = computeThreeBtagEfficiency(bTagEffJetsForTriple.at(0) + bTagEffJetsForTripleError.at(0),
								  bTagEffJetsForTriple.at(1) + bTagEffJetsForTripleError.at(1),
								  bTagEffJetsForTriple.at(2) + bTagEffJetsForTripleError.at(2),
								  bTagEffJetsForTriple.at(3) + bTagEffJetsForTripleError.at(3));
  float threeBtagEfficiencyErrorDown = computeThreeBtagEfficiency(bTagEffJetsForTriple.at(0) - bTagEffJetsForTripleError.at(0),
								  bTagEffJetsForTriple.at(1) - bTagEffJetsForTripleError.at(1),
								  bTagEffJetsForTriple.at(2) - bTagEffJetsForTripleError.at(2),
								  bTagEffJetsForTriple.at(3) - bTagEffJetsForTripleError.at(3));
  //=================================================================================================================================================================================
  float twoBtagEfficiency            = computeTwoBtagEfficiency(bTagEffJetsForDouble.at(0), bTagEffJetsForDouble.at(1), bTagEffJetsForDouble.at(2), bTagEffJetsForDouble.at(3));
  float twoBtagEfficiencyErrorUp     = computeTwoBtagEfficiency(bTagEffJetsForDouble.at(0) + bTagEffJetsForDoubleError.at(0),
								bTagEffJetsForDouble.at(1) + bTagEffJetsForDoubleError.at(1),
								bTagEffJetsForDouble.at(2) + bTagEffJetsForDoubleError.at(2),
								bTagEffJetsForDouble.at(3) + bTagEffJetsForDoubleError.at(3));
  float twoBtagEfficiencyErrorDown   = computeTwoBtagEfficiency(bTagEffJetsForDouble.at(0) - bTagEffJetsForDoubleError.at(0),
								bTagEffJetsForDouble.at(1) - bTagEffJetsForDoubleError.at(1),
								bTagEffJetsForDouble.at(2) - bTagEffJetsForDoubleError.at(2),
								bTagEffJetsForDouble.at(3) - bTagEffJetsForDoubleError.at(3));
  //=================================================================================================================================================================================
  if (simulateTrigger_)
    {
      theOutputTree_->userFloat("HLT_Data_effL1"              ) = effL1              ;
      theOutputTree_->userFloat("HLT_Data_effQuad30CaloJet"   ) = effQuad30CaloJet   ;
      theOutputTree_->userFloat("HLT_Data_effCaloHT"          ) = effCaloHT          ;
      theOutputTree_->userFloat("HLT_Data_effQuad30PFJet"     ) = effQuad30PFJet     ;
      theOutputTree_->userFloat("HLT_Data_effSingle75PFJet"   ) = effSingle75PFJet   ;
      theOutputTree_->userFloat("HLT_Data_effDouble60PFJet"   ) = effDouble60PFJet   ;
      theOutputTree_->userFloat("HLT_Data_effTriple54PFJet"   ) = effTriple54PFJet   ;
      theOutputTree_->userFloat("HLT_Data_effQuad40PFJet"     ) = effQuad40PFJet     ;
      theOutputTree_->userFloat("HLT_Data_effPFHT"            ) = effPFHT            ;
      theOutputTree_->userFloat("HLT_Data_threeBtagEfficiency") = threeBtagEfficiency;
      theOutputTree_->userFloat("HLT_Data_twoBtagEfficiency"  ) = twoBtagEfficiency  ;
    }
  
  float efficiencyCentral = computeTriggerEfficiency(threeBtagEfficiency,
						     twoBtagEfficiency,
						     effL1,
						     effQuad30CaloJet,
						     effCaloHT,
						     effQuad30PFJet,
						     effSingle75PFJet,
						     effDouble60PFJet,
						     effTriple54PFJet,
						     effQuad40PFJet,
						     effPFHT);
#ifdef useFit
  float efficiencyUp      = computeTriggerEfficiency(threeBtagEfficiencyErrorUp,
						     twoBtagEfficiencyErrorUp,
						     effL1 + effL1Error, 
						     effQuad30CaloJet + effQuad30CaloJetError, 
						     effCaloHT + effCaloHTError, 
						     effQuad30PFJet + effQuad30PFJetError, 
						     effSingle75PFJet + effSingle75PFJetError, 
						     effDouble60PFJet + effDouble60PFJetError, 
						     effTriple54PFJet + effTriple54PFJetError, 
						     effQuad40PFJet + effQuad40PFJetError, 
						     effPFHT + effPFHTError);
  
  float efficiencyDown    = computeTriggerEfficiency(threeBtagEfficiencyErrorDown, 
						     twoBtagEfficiencyErrorDown, 
						     effL1 - effL1Error, 
						     effQuad30CaloJet - effQuad30CaloJetError, 
						     effCaloHT - effCaloHTError, 
						     effQuad30PFJet - effQuad30PFJetError, 
						     effSingle75PFJet - effSingle75PFJetError, 
						     effDouble60PFJet - effDouble60PFJetError, 
						     effTriple54PFJet - effTriple54PFJetError, 
						     effQuad40PFJet - effQuad40PFJetError, 
						     effPFHT - effPFHTError);
#else
  static_assert(false, "Do not use fit not implemented for TriggerEfficiencyCalculator_2017");
#endif
  
  // debugging
  if (0)
    {
      std::cout << "Individual efficiencies for Double:"<<std::endl;  
      std::cout << "bTagEffJet0ForDouble = "<<bTagEffJetsForDouble.at(0)<<std::endl;
      std::cout << "bTagEffJet1ForDouble = "<<bTagEffJetsForDouble.at(1)<<std::endl;
      std::cout << "bTagEffJet2ForDouble = "<<bTagEffJetsForDouble.at(2)<<std::endl;
      std::cout << "bTagEffJet3ForDouble = "<<bTagEffJetsForDouble.at(3)<<std::endl;
      std::cout << "\nIndividual efficiencies for Triple:"<<std::endl;  
      std::cout << "bTagEffJet0ForTriple = "<<bTagEffJetsForTriple.at(0)<<std::endl;
      std::cout << "bTagEffJet1ForTriple = "<<bTagEffJetsForTriple.at(1)<<std::endl;
      std::cout << "bTagEffJet2ForTriple = "<<bTagEffJetsForTriple.at(2)<<std::endl;
      std::cout << "bTagEffJet3ForTriple = "<<bTagEffJetsForTriple.at(3)<<std::endl;
      std::cout << "\n"<<std::endl;
      std::cout << "threeBtagEfficiency = "<<threeBtagEfficiency<<std::endl;
      std::cout << "twoBtagEfficiency   = "<<twoBtagEfficiency<<std::endl;
      std::cout << "effL1               = "<<effL1<<std::endl;
      std::cout << "effQuad30CaloJet    = "<<effQuad30CaloJet<<std::endl;
      std::cout << "effCaloHT           = "<<effCaloHT<<std::endl;
      std::cout << "effQuad30PFJet      = "<<effQuad30PFJet<<std::endl;
      std::cout << "effSingle75PFJet    = "<<effSingle75PFJet<<std::endl;
      std::cout << "effDouble60PFJet    = "<<effDouble60PFJet<<std::endl;
      std::cout << "effTriple54PFJet    = "<<effTriple54PFJet<<std::endl;
      std::cout << "effQuad40PFJet      = "<<effQuad40PFJet<<std::endl;
      std::cout << "effPFHT             = "<<effPFHT<<std::endl;
      std::cout << "======== efficiencyCentral = "<<efficiencyCentral<<std::endl;
      std::cout << "         efficiencyUp      = "<<efficiencyUp<<std::endl;
      std::cout << "         efficiencyDown    = "<<efficiencyDown<<std::endl;
      std::cout << "\n"<<std::endl;
    }
  return {efficiencyCentral, efficiencyUp, efficiencyDown};
}

std::tuple<float, float, float> TriggerEfficiencyCalculator_2017::calculateMonteCarloTriggerEfficiency()
{
  if (0) std::cout << "\n====== 2017 MC Trigger Efficiency"<<std::endl;
#ifdef useFit
  std::vector<float> bTagEffJetsForDouble;
  std::vector<float> bTagEffJetsForDoubleError;
  std::vector<float> bTagEffJetsForTriple;
  std::vector<float> bTagEffJetsForTripleError;
  for (unsigned int i=0; i<deepFlavBVector.size(); i++)
    {
      bTagEffJetsForDouble.push_back(fTriggerFitCurves.fTTbar__Efficiency_BTagCaloCSVp05DoublePair.first->Eval(deepFlavBVector.at(i)));
      bTagEffJetsForDoubleError.push_back(getFitError(fTriggerFitCurves.fTTbar__Efficiency_BTagCaloCSVp05DoublePair.second, deepFlavBVector.at(i)));
      bTagEffJetsForTriple.push_back(fTriggerFitCurves.fTTbar__Efficiency_BTagPFCSVp070TriplePair.first->Eval(deepFlavBVector.at(i)));
      bTagEffJetsForTripleError.push_back(getFitError(fTriggerFitCurves.fTTbar__Efficiency_BTagPFCSVp070TriplePair.second, deepFlavBVector.at(i)));
    }
#else
  static_assert(false, "Do not use fit not implemented for TriggerEfficiencyCalculator_2017");
#endif
  
  float effL1            = fTriggerFitCurves.fTTbar__Efficiency_L1filterHTPair.first                     ->Eval(caloJetSum_);
  float effQuad30CaloJet = fTriggerFitCurves.fTTbar__Efficiency_QuadCentralJet30Pair.first               ->Eval(pt4_       );
  float effCaloHT        = fTriggerFitCurves.fTTbar__Efficiency_CaloQuadJet30HT300Pair.first             ->Eval(caloJetSum_);
  float effQuad30PFJet   = fTriggerFitCurves.fTTbar__Efficiency_PFCentralJetLooseIDQuad30Pair.first      ->Eval(pt4_       );
  float effSingle75PFJet = fTriggerFitCurves.fTTbar__Efficiency_1PFCentralJetLooseID75Pair.first         ->Eval(pt1_       );
  float effDouble60PFJet = fTriggerFitCurves.fTTbar__Efficiency_2PFCentralJetLooseID60Pair.first         ->Eval(pt2_       );
  float effTriple54PFJet = fTriggerFitCurves.fTTbar__Efficiency_3PFCentralJetLooseID45Pair.first         ->Eval(pt3_       );
  float effQuad40PFJet   = fTriggerFitCurves.fTTbar__Efficiency_4PFCentralJetLooseID40Pair.first         ->Eval(pt4_       );
  float effPFHT          = fTriggerFitCurves.fTTbar__Efficiency_PFCentralJetsLooseIDQuad30HT300Pair.first->Eval(pfJetSum_  );
  
  float effL1Error            = getFitError(fTriggerFitCurves.fTTbar__Efficiency_L1filterHTPair.second                     , caloJetSum_);
  float effQuad30CaloJetError = getFitError(fTriggerFitCurves.fTTbar__Efficiency_QuadCentralJet30Pair.second               , pt4_       );
  float effCaloHTError        = getFitError(fTriggerFitCurves.fTTbar__Efficiency_CaloQuadJet30HT300Pair.second             , caloJetSum_);
  float effQuad30PFJetError   = getFitError(fTriggerFitCurves.fTTbar__Efficiency_PFCentralJetLooseIDQuad30Pair.second      , pt4_       );
  float effSingle75PFJetError = getFitError(fTriggerFitCurves.fTTbar__Efficiency_1PFCentralJetLooseID75Pair.second         , pt1_       );
  float effDouble60PFJetError = getFitError(fTriggerFitCurves.fTTbar__Efficiency_2PFCentralJetLooseID60Pair.second         , pt2_       );
  float effTriple54PFJetError = getFitError(fTriggerFitCurves.fTTbar__Efficiency_3PFCentralJetLooseID45Pair.second         , pt3_       );
  float effQuad40PFJetError   = getFitError(fTriggerFitCurves.fTTbar__Efficiency_4PFCentralJetLooseID40Pair.second         , pt4_       );
  float effPFHTError          = getFitError(fTriggerFitCurves.fTTbar__Efficiency_PFCentralJetsLooseIDQuad30HT300Pair.second, pfJetSum_  );
  //================================================================================================================================================================================ 
  float threeBtagEfficiency          = computeThreeBtagEfficiency(bTagEffJetsForTriple.at(0), bTagEffJetsForTriple.at(1), bTagEffJetsForTriple.at(2), bTagEffJetsForTriple.at(3));
  float threeBtagEfficiencyErrorUp   = computeThreeBtagEfficiency(bTagEffJetsForTriple.at(0) + bTagEffJetsForTripleError.at(0),
								  bTagEffJetsForTriple.at(1) + bTagEffJetsForTripleError.at(1),
								  bTagEffJetsForTriple.at(2) + bTagEffJetsForTripleError.at(2),
								  bTagEffJetsForTriple.at(3) + bTagEffJetsForTripleError.at(3));
  float threeBtagEfficiencyErrorDown = computeThreeBtagEfficiency(bTagEffJetsForTriple.at(0) - bTagEffJetsForTripleError.at(0),
								  bTagEffJetsForTriple.at(1) - bTagEffJetsForTripleError.at(1),
								  bTagEffJetsForTriple.at(2) - bTagEffJetsForTripleError.at(2),
								  bTagEffJetsForTriple.at(3) - bTagEffJetsForTripleError.at(3));
  //=================================================================================================================================================================================
  float twoBtagEfficiency            = computeTwoBtagEfficiency(bTagEffJetsForDouble.at(0), bTagEffJetsForDouble.at(1), bTagEffJetsForDouble.at(2), bTagEffJetsForDouble.at(3));
  float twoBtagEfficiencyErrorUp     = computeTwoBtagEfficiency(bTagEffJetsForDouble.at(0) + bTagEffJetsForDoubleError.at(0),
								bTagEffJetsForDouble.at(1) + bTagEffJetsForDoubleError.at(1),
								bTagEffJetsForDouble.at(2) + bTagEffJetsForDoubleError.at(2),
								bTagEffJetsForDouble.at(3) + bTagEffJetsForDoubleError.at(3));
  float twoBtagEfficiencyErrorDown   = computeTwoBtagEfficiency(bTagEffJetsForDouble.at(0) - bTagEffJetsForDoubleError.at(0),
								bTagEffJetsForDouble.at(1) - bTagEffJetsForDoubleError.at(1),
								bTagEffJetsForDouble.at(2) - bTagEffJetsForDoubleError.at(2),
								bTagEffJetsForDouble.at(3) - bTagEffJetsForDoubleError.at(3));
  //=================================================================================================================================================================================
  if (simulateTrigger_)
    {
      theOutputTree_->userFloat("HLT_MC_effL1"              ) = effL1              ;
      theOutputTree_->userFloat("HLT_MC_effQuad30CaloJet"   ) = effQuad30CaloJet   ;
      theOutputTree_->userFloat("HLT_MC_effCaloHT"          ) = effCaloHT          ;
      theOutputTree_->userFloat("HLT_MC_effQuad30PFJet"     ) = effQuad30PFJet     ;
      theOutputTree_->userFloat("HLT_MC_effSingle75PFJet"   ) = effSingle75PFJet   ;
      theOutputTree_->userFloat("HLT_MC_effDouble60PFJet"   ) = effDouble60PFJet   ;
      theOutputTree_->userFloat("HLT_MC_effTriple54PFJet"   ) = effTriple54PFJet   ;
      theOutputTree_->userFloat("HLT_MC_effQuad40PFJet"     ) = effQuad40PFJet     ;
      theOutputTree_->userFloat("HLT_MC_effPFHT"            ) = effPFHT            ;
      theOutputTree_->userFloat("HLT_MC_threeBtagEfficiency") = threeBtagEfficiency;
      theOutputTree_->userFloat("HLT_MC_twoBtagEfficiency"  ) = twoBtagEfficiency  ;
    }
  
  float efficiencyCentral = computeTriggerEfficiency(threeBtagEfficiency, 
						     twoBtagEfficiency, 
						     effL1, 
						     effQuad30CaloJet, 
						     effCaloHT, 
						     effQuad30PFJet, 
						     effSingle75PFJet, 
						     effDouble60PFJet, 
						     effTriple54PFJet, 
						     effQuad40PFJet, 
						     effPFHT);
#ifdef useFit
  float efficiencyUp      = computeTriggerEfficiency(threeBtagEfficiencyErrorUp,
						     twoBtagEfficiencyErrorUp,
						     effL1 + effL1Error, 
						     effQuad30CaloJet + effQuad30CaloJetError, 
						     effCaloHT + effCaloHTError, 
						     effQuad30PFJet + effQuad30PFJetError, 
						     effSingle75PFJet + effSingle75PFJetError, 
						     effDouble60PFJet + effDouble60PFJetError, 
						     effTriple54PFJet + effTriple54PFJetError, 
						     effQuad40PFJet + effQuad40PFJetError,
						     effPFHT + effPFHTError);
  
  float efficiencyDown    = computeTriggerEfficiency(threeBtagEfficiencyErrorDown, 
						     twoBtagEfficiencyErrorDown, 
						     effL1 - effL1Error, 
						     effQuad30CaloJet - effQuad30CaloJetError,
						     effCaloHT - effCaloHTError, 
						     effQuad30PFJet - effQuad30PFJetError, 
						     effSingle75PFJet - effSingle75PFJetError, 
						     effDouble60PFJet - effDouble60PFJetError,
						     effTriple54PFJet - effTriple54PFJetError, 
						     effQuad40PFJet - effQuad40PFJetError,
						     effPFHT - effPFHTError);
#else
  static_assert(false, "Do not use fit not implemented for TriggerEfficiencyCalculator_2017");
#endif
  
  // debugging
  if (0)
    {
      std::cout << "Individual efficiencies for Double:"<<std::endl;  
      std::cout << "bTagEffJet0ForDouble = "<<bTagEffJetsForDouble.at(0)<<std::endl;
      std::cout << "bTagEffJet1ForDouble = "<<bTagEffJetsForDouble.at(1)<<std::endl;
      std::cout << "bTagEffJet2ForDouble = "<<bTagEffJetsForDouble.at(2)<<std::endl;
      std::cout << "bTagEffJet3ForDouble = "<<bTagEffJetsForDouble.at(3)<<std::endl;
      std::cout << "\nIndividual efficiencies for Triple:"<<std::endl;  
      std::cout << "bTagEffJet0ForTriple = "<<bTagEffJetsForTriple.at(0)<<std::endl;
      std::cout << "bTagEffJet1ForTriple = "<<bTagEffJetsForTriple.at(1)<<std::endl;
      std::cout << "bTagEffJet2ForTriple = "<<bTagEffJetsForTriple.at(2)<<std::endl;
      std::cout << "bTagEffJet3ForTriple = "<<bTagEffJetsForTriple.at(3)<<std::endl;
      std::cout << "\n"<<std::endl;
      std::cout << "threeBtagEfficiency = "<<threeBtagEfficiency<<std::endl;
      std::cout << "twoBtagEfficiency   = "<<twoBtagEfficiency<<std::endl;
      std::cout << "effL1               = "<<effL1<<std::endl;
      std::cout << "effQuad30CaloJet    = "<<effQuad30CaloJet<<std::endl;
      std::cout << "effCaloHT           = "<<effCaloHT<<std::endl;
      std::cout << "effQuad30PFJet      = "<<effQuad30PFJet<<std::endl;
      std::cout << "effSingle75PFJet    = "<<effSingle75PFJet<<std::endl;
      std::cout << "effDouble60PFJet    = "<<effDouble60PFJet<<std::endl;
      std::cout << "effTriple54PFJet    = "<<effTriple54PFJet<<std::endl;
      std::cout << "effQuad40PFJet      = "<<effQuad40PFJet<<std::endl;
      std::cout << "effPFHT             = "<<effPFHT<<std::endl;
      std::cout << "======== efficiencyCentral = "<<efficiencyCentral<<std::endl;
      std::cout << "         efficiencyUp      = "<<efficiencyUp<<std::endl;
      std::cout << "         efficiencyDown    = "<<efficiencyDown<<std::endl;
      std::cout << "\n"<<std::endl;
    }
  return {efficiencyCentral, efficiencyUp, efficiencyDown};
}

TriggerEfficiencyCalculator_2018::TriggerEfficiencyCalculator_2018(std::string inputFileName, NanoAODTree& nat)
: TriggerEfficiencyCalculator(nat)
, fTriggerFitCurves(inputFileName)
{}

TriggerEfficiencyCalculator_2018::~TriggerEfficiencyCalculator_2018()
{}

void TriggerEfficiencyCalculator_2018::createTriggerSimulatedBranches()
{
  /*
  theOutputTree_->declareUserFloatBranch("HLT_Pt1"             , 0.);
  theOutputTree_->declareUserFloatBranch("HLT_Pt2"             , 0.);
  theOutputTree_->declareUserFloatBranch("HLT_Pt3"             , 0.);
  theOutputTree_->declareUserFloatBranch("HLT_Pt4"             , 0.);
  theOutputTree_->declareUserFloatBranch("HLT_SumPtCaloJet"    , 0.);
  theOutputTree_->declareUserFloatBranch("HLT_SumPtPfJet"      , 0.);
  theOutputTree_->declareUserFloatBranch("HLT_SumPtJetOnly"    , 0.);
  */
  theOutputTree_->declareUserFloatBranch("HLT_Data_effL1"              , 0.);
  theOutputTree_->declareUserFloatBranch("HLT_Data_effQuad30CaloJet"   , 0.);
  theOutputTree_->declareUserFloatBranch("HLT_Data_effCaloHT"          , 0.);
  theOutputTree_->declareUserFloatBranch("HLT_Data_effQuad30PFJet"     , 0.);
  theOutputTree_->declareUserFloatBranch("HLT_Data_effSingle75PFJet"   , 0.);
  theOutputTree_->declareUserFloatBranch("HLT_Data_effDouble60PFJet"   , 0.);
  theOutputTree_->declareUserFloatBranch("HLT_Data_effTriple54PFJet"   , 0.);
  theOutputTree_->declareUserFloatBranch("HLT_Data_effQuad40PFJet"     , 0.);
  theOutputTree_->declareUserFloatBranch("HLT_Data_effPFHT"            , 0.);
  theOutputTree_->declareUserFloatBranch("HLT_Data_threeBtagEfficiency", 0.);
  theOutputTree_->declareUserFloatBranch("HLT_Data_twoBtagEfficiency"  , 0.);
  
  theOutputTree_->declareUserFloatBranch("HLT_MC_effL1"              , 0.);
  theOutputTree_->declareUserFloatBranch("HLT_MC_effQuad30CaloJet"   , 0.);
  theOutputTree_->declareUserFloatBranch("HLT_MC_effCaloHT"          , 0.);
  theOutputTree_->declareUserFloatBranch("HLT_MC_effQuad30PFJet"     , 0.);
  theOutputTree_->declareUserFloatBranch("HLT_MC_effSingle75PFJet"   , 0.);
  theOutputTree_->declareUserFloatBranch("HLT_MC_effDouble60PFJet"   , 0.);
  theOutputTree_->declareUserFloatBranch("HLT_MC_effTriple54PFJet"   , 0.);
  theOutputTree_->declareUserFloatBranch("HLT_MC_effQuad40PFJet"     , 0.);
  theOutputTree_->declareUserFloatBranch("HLT_MC_effPFHT"            , 0.);
  theOutputTree_->declareUserFloatBranch("HLT_MC_threeBtagEfficiency", 0.);
  theOutputTree_->declareUserFloatBranch("HLT_MC_twoBtagEfficiency"  , 0.);
}

void TriggerEfficiencyCalculator_2018::extractInformationFromEvent(std::vector<Jet> selectedJets)
{
  // Sort jets by b-tagging score
  std::sort(selectedJets.begin(), selectedJets.end(),[](Jet& j1, Jet& j2){ return j1.get_btag()>j2.get_btag();});
  for(unsigned int i=0; i<selectedJets.size(); i++)
    {
      // Keep only the leading four in b-tagging score jets
      if (i > 3) break;
      deepFlavBVector[i] = get_property(selectedJets.at(i), Jet_btagDeepFlavB);
    }
  
  // Sort jets by pT
  stable_sort(selectedJets.begin(), selectedJets.end(), [](const Jet & a, const Jet & b) -> bool{return (a.P4().Pt() > b.P4().Pt()); });
  
  // Save the pT of the leading four jets
  pt1_ = selectedJets[0].P4().Pt();
  pt2_ = selectedJets[1].P4().Pt();
  pt3_ = selectedJets[2].P4().Pt();
  pt4_ = selectedJets[3].P4().Pt();
  
  // Calculate the event sums
  caloJetSum_ = 0.;
  pfJetSum_   = 0.;
  onlyJetSum_ = 0.;
  for (uint ij=0; ij<*(theNanoAODTree_.nJet); ++ij)
    {
      // here preselect jets
      Jet jet (ij, &theNanoAODTree_);
      if (jet.P4().Pt() >= 30. && std::abs(jet.P4().Eta()) < 2.5) pfJetSum_ += jet.P4().Pt();
      
      bool isMuon = false;
      for (uint candIt = 0; candIt < *(theNanoAODTree_.nMuon); ++candIt)
        {
	  Muon theMuon (candIt, &theNanoAODTree_);
	  if(get_property(theMuon, Muon_pfRelIso04_all) > 0.3) continue;
	  if(jet.getIdx() == get_property(theMuon, Muon_jetIdx))
            {
	      isMuon = true;
	      break;
            }
        }
      if(isMuon) continue;
      
      if (jet.P4().Pt() >= 30. && std::abs(jet.P4().Eta()) < 2.5) caloJetSum_ += jet.P4().Pt();
      
      bool isElectron = false;
      for (uint candIt = 0; candIt < *(theNanoAODTree_.nElectron); ++candIt)
        {
	  Electron theElectron (candIt, &theNanoAODTree_);
	  if(get_property(theElectron, Electron_pfRelIso03_all) > 0.3) continue;
	  if(jet.getIdx() == get_property(theElectron, Electron_jetIdx))
            {
	      isElectron = true;
	      break;
            }
        }
      if(isElectron) continue;
      
      if (jet.P4().Pt() >= 30. && std::abs(jet.P4().Eta()) < 2.5) onlyJetSum_ += jet.P4().Pt();      
    }
  
  /*
  if (0)
    {
      theOutputTree_->userFloat("HLT_Pt1"         ) = pt1_;
      theOutputTree_->userFloat("HLT_Pt2"         ) = pt2_;
      theOutputTree_->userFloat("HLT_Pt3"         ) = pt3_;
      theOutputTree_->userFloat("HLT_Pt4"         ) = pt4_;
      theOutputTree_->userFloat("HLT_SumPtCaloJet") = caloJetSum_;
      theOutputTree_->userFloat("HLT_SumPtPfJet"  ) = pfJetSum_;
      theOutputTree_->userFloat("HLT_SumPtJetOnly") = onlyJetSum_;
    }
  */
}

std::tuple<float, float, float> TriggerEfficiencyCalculator_2018::calculateDataTriggerEfficiency()
{
  if (0) std::cout << "\n====== Data Trigger Efficiency"<<std::endl;
#ifdef useFit
  std::vector<float> bTagEffJetsForDouble;
  std::vector<float> bTagEffJetsForDoubleError;
  std::vector<float> bTagEffJetsForTriple;
  std::vector<float> bTagEffJetsForTripleError;
  for (unsigned int i=0; i<deepFlavBVector.size(); i++)
    {
      bTagEffJetsForDouble.push_back(fTriggerFitCurves.fSingleMuon__Efficiency_BTagCaloDeepCSVp17DoublePair.first->Eval(deepFlavBVector.at(i)));
      bTagEffJetsForDoubleError.push_back(getFitError(fTriggerFitCurves.fSingleMuon__Efficiency_BTagCaloDeepCSVp17DoublePair.second, deepFlavBVector.at(i)));
      bTagEffJetsForTriple.push_back(fTriggerFitCurves.fSingleMuon__Efficiency_BTagPFDeepCSV4p5TriplePair.first->Eval(deepFlavBVector.at(i)));
      bTagEffJetsForTripleError.push_back(getFitError(fTriggerFitCurves.fSingleMuon__Efficiency_BTagPFDeepCSV4p5TriplePair.second, deepFlavBVector.at(i)));
    }
#else
  static_assert(false, "Do not use fit not implemented for TriggerEfficiencyCalculator_2018");
#endif
  
  float effL1                 = fTriggerFitCurves.fSingleMuon__Efficiency_L1filterHTPair.first                     ->Eval(caloJetSum_);
  float effQuad30CaloJet      = fTriggerFitCurves.fSingleMuon__Efficiency_QuadCentralJet30Pair.first               ->Eval(pt4_       );
  float effCaloHT             = fTriggerFitCurves.fSingleMuon__Efficiency_CaloQuadJet30HT320Pair.first             ->Eval(caloJetSum_);
  float effQuad30PFJet        = fTriggerFitCurves.fSingleMuon__Efficiency_PFCentralJetLooseIDQuad30Pair.first      ->Eval(pt4_       );
  float effSingle75PFJet      = fTriggerFitCurves.fSingleMuon__Efficiency_1PFCentralJetLooseID75Pair.first         ->Eval(pt1_       );
  float effDouble60PFJet      = fTriggerFitCurves.fSingleMuon__Efficiency_2PFCentralJetLooseID60Pair.first         ->Eval(pt2_       );
  float effTriple54PFJet      = fTriggerFitCurves.fSingleMuon__Efficiency_3PFCentralJetLooseID45Pair.first         ->Eval(pt3_       );
  float effQuad40PFJet        = fTriggerFitCurves.fSingleMuon__Efficiency_4PFCentralJetLooseID40Pair.first         ->Eval(pt4_       );
  float effPFHT               = fTriggerFitCurves.fSingleMuon__Efficiency_PFCentralJetsLooseIDQuad30HT330Pair.first->Eval(pfJetSum_  );
  float effL1Error            = getFitError(fTriggerFitCurves.fSingleMuon__Efficiency_L1filterHTPair.second                     , caloJetSum_);
  float effQuad30CaloJetError = getFitError(fTriggerFitCurves.fSingleMuon__Efficiency_QuadCentralJet30Pair.second               , pt4_       );
  float effCaloHTError        = getFitError(fTriggerFitCurves.fSingleMuon__Efficiency_CaloQuadJet30HT320Pair.second             , caloJetSum_);
  float effQuad30PFJetError   = getFitError(fTriggerFitCurves.fSingleMuon__Efficiency_PFCentralJetLooseIDQuad30Pair.second      , pt4_       );
  float effSingle75PFJetError = getFitError(fTriggerFitCurves.fSingleMuon__Efficiency_1PFCentralJetLooseID75Pair.second         , pt1_       );
  float effDouble60PFJetError = getFitError(fTriggerFitCurves.fSingleMuon__Efficiency_2PFCentralJetLooseID60Pair.second         , pt2_       );
  float effTriple54PFJetError = getFitError(fTriggerFitCurves.fSingleMuon__Efficiency_3PFCentralJetLooseID45Pair.second         , pt3_       );
  float effQuad40PFJetError   = getFitError(fTriggerFitCurves.fSingleMuon__Efficiency_4PFCentralJetLooseID40Pair.second         , pt4_       );
  float effPFHTError          = getFitError(fTriggerFitCurves.fSingleMuon__Efficiency_PFCentralJetsLooseIDQuad30HT330Pair.second, pfJetSum_  );
  
  //================================================================================================================================================================================ 
  float threeBtagEfficiency          = computeThreeBtagEfficiency(bTagEffJetsForTriple.at(0), bTagEffJetsForTriple.at(1), bTagEffJetsForTriple.at(2), bTagEffJetsForTriple.at(3));
  float threeBtagEfficiencyErrorUp   = computeThreeBtagEfficiency(bTagEffJetsForTriple.at(0) + bTagEffJetsForTripleError.at(0),
								  bTagEffJetsForTriple.at(1) + bTagEffJetsForTripleError.at(1),
								  bTagEffJetsForTriple.at(2) + bTagEffJetsForTripleError.at(2),
								  bTagEffJetsForTriple.at(3) + bTagEffJetsForTripleError.at(3));
  float threeBtagEfficiencyErrorDown = computeThreeBtagEfficiency(bTagEffJetsForTriple.at(0) - bTagEffJetsForTripleError.at(0),
								  bTagEffJetsForTriple.at(1) - bTagEffJetsForTripleError.at(1),
								  bTagEffJetsForTriple.at(2) - bTagEffJetsForTripleError.at(2),
								  bTagEffJetsForTriple.at(3) - bTagEffJetsForTripleError.at(3));
  //=================================================================================================================================================================================
  float twoBtagEfficiency            = computeTwoBtagEfficiency(bTagEffJetsForDouble.at(0), bTagEffJetsForDouble.at(1), bTagEffJetsForDouble.at(2), bTagEffJetsForDouble.at(3));
  float twoBtagEfficiencyErrorUp     = computeTwoBtagEfficiency(bTagEffJetsForDouble.at(0) + bTagEffJetsForDoubleError.at(0),
								bTagEffJetsForDouble.at(1) + bTagEffJetsForDoubleError.at(1),
								bTagEffJetsForDouble.at(2) + bTagEffJetsForDoubleError.at(2),
								bTagEffJetsForDouble.at(3) + bTagEffJetsForDoubleError.at(3));
  float twoBtagEfficiencyErrorDown   = computeTwoBtagEfficiency(bTagEffJetsForDouble.at(0) - bTagEffJetsForDoubleError.at(0),
								bTagEffJetsForDouble.at(1) - bTagEffJetsForDoubleError.at(1),
								bTagEffJetsForDouble.at(2) - bTagEffJetsForDoubleError.at(2),
								bTagEffJetsForDouble.at(3) - bTagEffJetsForDoubleError.at(3));
  //=================================================================================================================================================================================
  if (simulateTrigger_)
    {
      theOutputTree_->userFloat("HLT_Data_effL1"              ) = effL1;
      theOutputTree_->userFloat("HLT_Data_effQuad30CaloJet"   ) = effQuad30CaloJet;
      theOutputTree_->userFloat("HLT_Data_effCaloHT"          ) = effCaloHT;
      theOutputTree_->userFloat("HLT_Data_effQuad30PFJet"     ) = effQuad30PFJet;
      theOutputTree_->userFloat("HLT_Data_effSingle75PFJet"   ) = effSingle75PFJet;
      theOutputTree_->userFloat("HLT_Data_effDouble60PFJet"   ) = effDouble60PFJet;
      theOutputTree_->userFloat("HLT_Data_effTriple54PFJet"   ) = effTriple54PFJet;
      theOutputTree_->userFloat("HLT_Data_effQuad40PFJet"     ) = effQuad40PFJet;
      theOutputTree_->userFloat("HLT_Data_effPFHT"            ) = effPFHT;
      theOutputTree_->userFloat("HLT_Data_threeBtagEfficiency") = threeBtagEfficiency;
      theOutputTree_->userFloat("HLT_Data_twoBtagEfficiency"  ) = twoBtagEfficiency;
    }
  
  float efficiencyCentral = computeTriggerEfficiency(threeBtagEfficiency, 
						     twoBtagEfficiency, 
						     effL1, 
						     effQuad30CaloJet, 
						     effCaloHT, 
						     effQuad30PFJet, 
						     effSingle75PFJet, 
						     effDouble60PFJet, 
						     effTriple54PFJet, 
						     effQuad40PFJet, 
						     effPFHT);
#ifdef useFit
  float efficiencyUp = computeTriggerEfficiency(threeBtagEfficiencyErrorUp,
						twoBtagEfficiencyErrorUp,
						effL1 + effL1Error, 
						effQuad30CaloJet + effQuad30CaloJetError,
						effCaloHT + effCaloHTError, 
						effQuad30PFJet + effQuad30PFJetError, 
						effSingle75PFJet + effSingle75PFJetError,
						effDouble60PFJet + effDouble60PFJetError,
						effTriple54PFJet + effTriple54PFJetError, 
						effQuad40PFJet + effQuad40PFJetError, 
						effPFHT + effPFHTError);
  float efficiencyDown=computeTriggerEfficiency(threeBtagEfficiencyErrorDown, 
						twoBtagEfficiencyErrorDown, 
						effL1 - effL1Error, 
						effQuad30CaloJet - effQuad30CaloJetError,
						effCaloHT - effCaloHTError, 
						effQuad30PFJet - effQuad30PFJetError, 
						effSingle75PFJet - effSingle75PFJetError,
						effDouble60PFJet - effDouble60PFJetError, 
						effTriple54PFJet - effTriple54PFJetError, 
						effQuad40PFJet - effQuad40PFJetError,
						effPFHT - effPFHTError);
#else
  static_assert(false, "Do not use fit not implemented for TriggerEfficiencyCalculator_2018");
#endif
  
  // debugging
  if (0)
    {
      std::cout << "Individual efficiencies for Double:"<<std::endl;  
      std::cout << "bTagEffJet0ForDouble = "<<bTagEffJetsForDouble.at(0)<<std::endl;
      std::cout << "bTagEffJet1ForDouble = "<<bTagEffJetsForDouble.at(1)<<std::endl;
      std::cout << "bTagEffJet2ForDouble = "<<bTagEffJetsForDouble.at(2)<<std::endl;
      std::cout << "bTagEffJet3ForDouble = "<<bTagEffJetsForDouble.at(3)<<std::endl;
      std::cout << "\nIndividual efficiencies for Triple:"<<std::endl;  
      std::cout << "bTagEffJet0ForTriple = "<<bTagEffJetsForTriple.at(0)<<std::endl;
      std::cout << "bTagEffJet1ForTriple = "<<bTagEffJetsForTriple.at(1)<<std::endl;
      std::cout << "bTagEffJet2ForTriple = "<<bTagEffJetsForTriple.at(2)<<std::endl;
      std::cout << "bTagEffJet3ForTriple = "<<bTagEffJetsForTriple.at(3)<<std::endl;
      std::cout << "\n"<<std::endl;
      std::cout << "threeBtagEfficiency = "<<threeBtagEfficiency<<std::endl;
      std::cout << "twoBtagEfficiency   = "<<twoBtagEfficiency<<std::endl;
      std::cout << "effL1               = "<<effL1<<std::endl;
      std::cout << "effQuad30CaloJet    = "<<effQuad30CaloJet<<std::endl;
      std::cout << "effCaloHT           = "<<effCaloHT<<std::endl;
      std::cout << "effQuad30PFJet      = "<<effQuad30PFJet<<std::endl;
      std::cout << "effSingle75PFJet    = "<<effSingle75PFJet<<std::endl;
      std::cout << "effDouble60PFJet    = "<<effDouble60PFJet<<std::endl;
      std::cout << "effTriple54PFJet    = "<<effTriple54PFJet<<std::endl;
      std::cout << "effQuad40PFJet      = "<<effQuad40PFJet<<std::endl;
      std::cout << "effPFHT             = "<<effPFHT<<std::endl;
      std::cout << "======== efficiencyCentral = "<<efficiencyCentral<<std::endl;
      std::cout << "         efficiencyUp      = "<<efficiencyUp<<std::endl;
      std::cout << "         efficiencyDown    = "<<efficiencyDown<<std::endl;
      std::cout << "\n"<<std::endl;
    }
  return {efficiencyCentral, efficiencyUp, efficiencyDown};
}

std::tuple<float, float, float> TriggerEfficiencyCalculator_2018::calculateMonteCarloTriggerEfficiency()
{
  if (0) std::cout << "\n====== MC Trigger Efficiency"<<std::endl;
#ifdef useFit
  std::vector<float> bTagEffJetsForDouble;
  std::vector<float> bTagEffJetsForDoubleError;
  std::vector<float> bTagEffJetsForTriple;
  std::vector<float> bTagEffJetsForTripleError;
  for (unsigned int i=0; i<deepFlavBVector.size(); i++)
    {
      bTagEffJetsForDouble.push_back(fTriggerFitCurves.fTTbar__Efficiency_BTagCaloDeepCSVp17DoublePair.first->Eval(deepFlavBVector.at(i)));
      bTagEffJetsForDoubleError.push_back(getFitError(fTriggerFitCurves.fTTbar__Efficiency_BTagCaloDeepCSVp17DoublePair.second, deepFlavBVector.at(i)));
      bTagEffJetsForTriple.push_back(fTriggerFitCurves.fTTbar__Efficiency_BTagPFDeepCSV4p5TriplePair.first->Eval(deepFlavBVector.at(i)));
      bTagEffJetsForTripleError.push_back(getFitError(fTriggerFitCurves.fTTbar__Efficiency_BTagPFDeepCSV4p5TriplePair.second, deepFlavBVector.at(i)));
    }
#else
  static_assert(false, "Do not use fit not implemented for TriggerEfficiencyCalculator_2018");
#endif
  float effL1                 = fTriggerFitCurves.fTTbar__Efficiency_L1filterHTPair.first                     ->Eval(caloJetSum_);
  float effQuad30CaloJet      = fTriggerFitCurves.fTTbar__Efficiency_QuadCentralJet30Pair.first               ->Eval(pt4_       );
  float effCaloHT             = fTriggerFitCurves.fTTbar__Efficiency_CaloQuadJet30HT320Pair.first             ->Eval(caloJetSum_);
  float effQuad30PFJet        = fTriggerFitCurves.fTTbar__Efficiency_PFCentralJetLooseIDQuad30Pair.first      ->Eval(pt4_       );
  float effSingle75PFJet      = fTriggerFitCurves.fTTbar__Efficiency_1PFCentralJetLooseID75Pair.first         ->Eval(pt1_       );
  float effDouble60PFJet      = fTriggerFitCurves.fTTbar__Efficiency_2PFCentralJetLooseID60Pair.first         ->Eval(pt2_       );
  float effTriple54PFJet      = fTriggerFitCurves.fTTbar__Efficiency_3PFCentralJetLooseID45Pair.first         ->Eval(pt3_       );
  float effQuad40PFJet        = fTriggerFitCurves.fTTbar__Efficiency_4PFCentralJetLooseID40Pair.first         ->Eval(pt4_       );
  float effPFHT               = fTriggerFitCurves.fTTbar__Efficiency_PFCentralJetsLooseIDQuad30HT330Pair.first->Eval(pfJetSum_  );
  float effL1Error            = getFitError(fTriggerFitCurves.fTTbar__Efficiency_L1filterHTPair.second                     , caloJetSum_);
  float effQuad30CaloJetError = getFitError(fTriggerFitCurves.fTTbar__Efficiency_QuadCentralJet30Pair.second               , pt4_       );
  float effCaloHTError        = getFitError(fTriggerFitCurves.fTTbar__Efficiency_CaloQuadJet30HT320Pair.second             , caloJetSum_);
  float effQuad30PFJetError   = getFitError(fTriggerFitCurves.fTTbar__Efficiency_PFCentralJetLooseIDQuad30Pair.second      , pt4_       );
  float effSingle75PFJetError = getFitError(fTriggerFitCurves.fTTbar__Efficiency_1PFCentralJetLooseID75Pair.second         , pt1_       );
  float effDouble60PFJetError = getFitError(fTriggerFitCurves.fTTbar__Efficiency_2PFCentralJetLooseID60Pair.second         , pt2_       );
  float effTriple54PFJetError = getFitError(fTriggerFitCurves.fTTbar__Efficiency_3PFCentralJetLooseID45Pair.second         , pt3_       );
  float effQuad40PFJetError   = getFitError(fTriggerFitCurves.fTTbar__Efficiency_4PFCentralJetLooseID40Pair.second         , pt4_       );
  float effPFHTError          = getFitError(fTriggerFitCurves.fTTbar__Efficiency_PFCentralJetsLooseIDQuad30HT330Pair.second, pfJetSum_  );
  //================================================================================================================================================================================ 
  float threeBtagEfficiency          = computeThreeBtagEfficiency(bTagEffJetsForTriple.at(0), bTagEffJetsForTriple.at(1), bTagEffJetsForTriple.at(2), bTagEffJetsForTriple.at(3));
  float threeBtagEfficiencyErrorUp   = computeThreeBtagEfficiency(bTagEffJetsForTriple.at(0) + bTagEffJetsForTripleError.at(0),
								  bTagEffJetsForTriple.at(1) + bTagEffJetsForTripleError.at(1),
								  bTagEffJetsForTriple.at(2) + bTagEffJetsForTripleError.at(2),
								  bTagEffJetsForTriple.at(3) + bTagEffJetsForTripleError.at(3));
  float threeBtagEfficiencyErrorDown = computeThreeBtagEfficiency(bTagEffJetsForTriple.at(0) - bTagEffJetsForTripleError.at(0),
								  bTagEffJetsForTriple.at(1) - bTagEffJetsForTripleError.at(1),
								  bTagEffJetsForTriple.at(2) - bTagEffJetsForTripleError.at(2),
								  bTagEffJetsForTriple.at(3) - bTagEffJetsForTripleError.at(3));
  //=================================================================================================================================================================================
  float twoBtagEfficiency            = computeTwoBtagEfficiency(bTagEffJetsForDouble.at(0), bTagEffJetsForDouble.at(1), bTagEffJetsForDouble.at(2), bTagEffJetsForDouble.at(3));
  float twoBtagEfficiencyErrorUp     = computeTwoBtagEfficiency(bTagEffJetsForDouble.at(0) + bTagEffJetsForDoubleError.at(0),
								bTagEffJetsForDouble.at(1) + bTagEffJetsForDoubleError.at(1),
								bTagEffJetsForDouble.at(2) + bTagEffJetsForDoubleError.at(2),
								bTagEffJetsForDouble.at(3) + bTagEffJetsForDoubleError.at(3));
  float twoBtagEfficiencyErrorDown   = computeTwoBtagEfficiency(bTagEffJetsForDouble.at(0) - bTagEffJetsForDoubleError.at(0),
								bTagEffJetsForDouble.at(1) - bTagEffJetsForDoubleError.at(1),
								bTagEffJetsForDouble.at(2) - bTagEffJetsForDoubleError.at(2),
								bTagEffJetsForDouble.at(3) - bTagEffJetsForDoubleError.at(3));
  //=================================================================================================================================================================================
  if (simulateTrigger_)
    {
      theOutputTree_->userFloat("HLT_MC_effL1"              ) = effL1              ;
      theOutputTree_->userFloat("HLT_MC_effQuad30CaloJet"   ) = effQuad30CaloJet   ;
      theOutputTree_->userFloat("HLT_MC_effCaloHT"          ) = effCaloHT          ;
      theOutputTree_->userFloat("HLT_MC_effQuad30PFJet"     ) = effQuad30PFJet     ;
      theOutputTree_->userFloat("HLT_MC_effSingle75PFJet"   ) = effSingle75PFJet   ;
      theOutputTree_->userFloat("HLT_MC_effDouble60PFJet"   ) = effDouble60PFJet   ;
      theOutputTree_->userFloat("HLT_MC_effTriple54PFJet"   ) = effTriple54PFJet   ;
      theOutputTree_->userFloat("HLT_MC_effQuad40PFJet"     ) = effQuad40PFJet     ;
      theOutputTree_->userFloat("HLT_MC_effPFHT"            ) = effPFHT            ;
      theOutputTree_->userFloat("HLT_MC_threeBtagEfficiency") = threeBtagEfficiency;
      theOutputTree_->userFloat("HLT_MC_twoBtagEfficiency"  ) = twoBtagEfficiency  ;
    }
  
  float efficiencyCentral = computeTriggerEfficiency(threeBtagEfficiency,
						     twoBtagEfficiency, 
						     effL1,
						     effQuad30CaloJet,
						     effCaloHT,
						     effQuad30PFJet,
						     effSingle75PFJet,
						     effDouble60PFJet,
						     effTriple54PFJet,
						     effQuad40PFJet,
						     effPFHT);
#ifdef useFit
  float efficiencyUp = computeTriggerEfficiency(threeBtagEfficiencyErrorUp, 
						twoBtagEfficiencyErrorUp, 
						effL1 + effL1Error, 
						effQuad30CaloJet + effQuad30CaloJetError, 
						effCaloHT + effCaloHTError, 
						effQuad30PFJet + effQuad30PFJetError, 
						effSingle75PFJet + effSingle75PFJetError,
						effDouble60PFJet + effDouble60PFJetError, 
						effTriple54PFJet + effTriple54PFJetError, 
						effQuad40PFJet + effQuad40PFJetError, 
						effPFHT + effPFHTError);
 
  float efficiencyDown = computeTriggerEfficiency(threeBtagEfficiencyErrorDown, 
						  twoBtagEfficiencyErrorDown, 
						  effL1 - effL1Error,
						  effQuad30CaloJet - effQuad30CaloJetError, 
						  effCaloHT - effCaloHTError,
						  effQuad30PFJet - effQuad30PFJetError, 
						  effSingle75PFJet - effSingle75PFJetError, 
						  effDouble60PFJet - effDouble60PFJetError, 
						  effTriple54PFJet - effTriple54PFJetError, 
						  effQuad40PFJet - effQuad40PFJetError, 
						  effPFHT - effPFHTError);
#else
  static_assert(false, "Do not use fit not implemented for TriggerEfficiencyCalculator_2018");
#endif
  
  // debugging
  if (0)
    {
      std::cout << "Individual efficiencies for Double:"<<std::endl;  
      std::cout << "bTagEffJet0ForDouble = "<<bTagEffJetsForDouble.at(0)<<std::endl;
      std::cout << "bTagEffJet1ForDouble = "<<bTagEffJetsForDouble.at(1)<<std::endl;
      std::cout << "bTagEffJet2ForDouble = "<<bTagEffJetsForDouble.at(2)<<std::endl;
      std::cout << "bTagEffJet3ForDouble = "<<bTagEffJetsForDouble.at(3)<<std::endl;
      std::cout << "\nIndividual efficiencies for Triple:"<<std::endl;  
      std::cout << "bTagEffJet0ForTriple = "<<bTagEffJetsForTriple.at(0)<<std::endl;
      std::cout << "bTagEffJet1ForTriple = "<<bTagEffJetsForTriple.at(1)<<std::endl;
      std::cout << "bTagEffJet2ForTriple = "<<bTagEffJetsForTriple.at(2)<<std::endl;
      std::cout << "bTagEffJet3ForTriple = "<<bTagEffJetsForTriple.at(3)<<std::endl;
      std::cout << "\n"<<std::endl;
      std::cout << "threeBtagEfficiency = "<<threeBtagEfficiency<<std::endl;
      std::cout << "twoBtagEfficiency   = "<<twoBtagEfficiency<<std::endl;
      std::cout << "effL1               = "<<effL1<<std::endl;
      std::cout << "effQuad30CaloJet    = "<<effQuad30CaloJet<<std::endl;
      std::cout << "effCaloHT           = "<<effCaloHT<<std::endl;
      std::cout << "effQuad30PFJet      = "<<effQuad30PFJet<<std::endl;
      std::cout << "effSingle75PFJet    = "<<effSingle75PFJet<<std::endl;
      std::cout << "effDouble60PFJet    = "<<effDouble60PFJet<<std::endl;
      std::cout << "effTriple54PFJet    = "<<effTriple54PFJet<<std::endl;
      std::cout << "effQuad40PFJet      = "<<effQuad40PFJet<<std::endl;
      std::cout << "effPFHT             = "<<effPFHT<<std::endl;
      std::cout << "======== efficiencyCentral = "<<efficiencyCentral<<std::endl;
      std::cout << "         efficiencyUp      = "<<efficiencyUp<<std::endl;
      std::cout << "         efficiencyDown    = "<<efficiencyDown<<std::endl;
      std::cout << "\n"<<std::endl;
    }
  return {efficiencyCentral, efficiencyUp, efficiencyDown};
}

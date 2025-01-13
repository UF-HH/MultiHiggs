#include "NanoAODTree.h"
#include "OutputTree.h"
#include "Jet.h"
#include "TAxis.h"
#include "TFitResult.h"
#include "TriggerFitCurves2016.h"
#include "TriggerFitCurves2017.h"
#include "TriggerFitCurves2018.h"

class TriggerEfficiencyCalculator
{
 public:
  TriggerEfficiencyCalculator(NanoAODTree& nat);
  virtual ~TriggerEfficiencyCalculator();
  
  virtual std::tuple<float, float, float> getMonteCarloTriggerEfficiency(const std::vector<Jet>& selectedJets);
  virtual std::tuple<float, float, float> getDataTriggerEfficiency      (const std::vector<Jet>& selectedJets);
  virtual std::tuple<float, float, float> getTriggerScaleFactor         (const std::vector<Jet>& selectedJets);
  virtual std::tuple<std::tuple<float, float, float>, std::tuple<float, float, float>, std::tuple<float, float, float>> getScaleFactorDataAndMonteCarloEfficiency(const std::vector<Jet>& selectedJets);
  void simulateTrigger(OutputTree* theOutputTree);
  void applyTurnOnCut(bool applyCuts) {applyTurnOnCut_ = applyCuts;}
  virtual bool isPassingTurnOnCuts(std::vector<std::string> listOfPassedTriggers, const std::vector<Jet>& selectedJets) = 0;
  
 protected:
  template<size_t N>
    double getPointValue(std::tuple<TGraphAsymmErrors*, TGraph*, TGraph*> theGraphTuple, double xValue)
    {
      auto theGraph = std::get<0>(theGraphTuple);
      double yRetrievedValue = 0.;
      int pointNumber=0;
      for(; pointNumber<theGraph->GetN(); ++pointNumber)
        {
	  double xRetrievedValue = 0.;
	  theGraph->GetPoint(pointNumber, xRetrievedValue, yRetrievedValue);
	  double lowEdge  = xRetrievedValue - theGraph->GetErrorXlow (pointNumber);
	  double highEdge = xRetrievedValue + theGraph->GetErrorXhigh(pointNumber);
	  if(xValue > lowEdge && xValue <=highEdge)
            {
	      if(N == 1) yRetrievedValue += theGraph->GetErrorYhigh (pointNumber);
	      if(N == 2) yRetrievedValue -= theGraph->GetErrorYlow (pointNumber);
	      break;
            }
        }
      return yRetrievedValue;
    }
  virtual void   createTriggerSimulatedBranches()                              = 0;
  virtual void   extractInformationFromEvent   (std::vector<Jet> selectedJets) = 0;
  inline  float  fixInLimits                   (float efficiency)
  {
    if(efficiency > 1.) return 1.;
    if(efficiency < 0.) return 0.;
    return efficiency;
  }
  
  inline float getFitError(TFitResult* theFitResult, float xValue)
  {
    double xValueDouble = xValue;
    double yError = 0.;
    theFitResult->GetConfidenceIntervals(1, 1, 1, &xValueDouble, &yError, 0.68);
    return yError;
  }
  
  inline float computeThreeBtagEfficiency(float bTagEffJet0, float bTagEffJet1, float bTagEffJet2, float bTagEffJet3)
  {
    float effJet0 = fixInLimits(bTagEffJet0);
    float effJet1 = fixInLimits(bTagEffJet1);
    float effJet2 = fixInLimits(bTagEffJet2);
    float effJet3 = fixInLimits(bTagEffJet3);
    
    // Probability of 3 out 4: P(all) + P(3, 1)
    return   effJet0   *   effJet1   *   effJet2   *   effJet3   +
           (1-effJet0) *   effJet1   *   effJet2   *   effJet3   +
             effJet0   * (1-effJet1) *   effJet2   *   effJet3   +
             effJet0   *   effJet1   * (1-effJet2) *   effJet3   +
	     effJet0   *   effJet1   *   effJet2   * (1-effJet3) ;
  }
  
  inline float computeTwoBtagEfficiency(float bTagEffJet0, float bTagEffJet1, float bTagEffJet2, float bTagEffJet3)
  {
    float effJet0 = fixInLimits(bTagEffJet0);
    float effJet1 = fixInLimits(bTagEffJet1);
    float effJet2 = fixInLimits(bTagEffJet2);
    float effJet3 = fixInLimits(bTagEffJet3);
    
    float ineffJet0 = 1 - effJet0;
    float ineffJet1 = 1 - effJet1;
    float ineffJet2 = 1 - effJet2;
    float ineffJet3 = 1 - effJet3;
    
    // Probability of 2 out of 4: P(all) + P(3, 1) + P(2, 2) = 1 - P(!all) - P(1, 3)
    return 1 - ineffJet0 * ineffJet1 * ineffJet2 * ineffJet3 -
               effJet0   * ineffJet1 * ineffJet2 * ineffJet3 -
               ineffJet0 *  effJet1  * ineffJet2 * ineffJet3 -
               ineffJet0 * ineffJet1 *  effJet2  * ineffJet3 -
               ineffJet0 * ineffJet1 * ineffJet2 *  effJet3 ;
  }
  virtual std::tuple<float, float, float>  calculateDataTriggerEfficiency      () = 0;
  virtual std::tuple<float, float, float>  calculateMonteCarloTriggerEfficiency() = 0;
  NanoAODTree &theNanoAODTree_;
  OutputTree* theOutputTree_ {nullptr};
  bool simulateTrigger_ {false};
  bool applyTurnOnCut_ {false};
};

// ================= 2016
class TriggerEfficiencyCalculator_2016 : public TriggerEfficiencyCalculator
{
public:
    TriggerEfficiencyCalculator_2016(std::string inputFileName, NanoAODTree& nat);
    ~TriggerEfficiencyCalculator_2016();
    bool isPassingTurnOnCuts(std::vector<std::string> listOfPassedTriggers, const std::vector<Jet>& selectedJets) override;
    void setTurnOnCuts(float double90Double30_minSumPt, float double90Double30_minPt2, float double90Double30_minPt4, float quad45_minSumPt, float quad45_minPt4)
    {
        double90Double30_minSumPt_ = double90Double30_minSumPt;
        double90Double30_minPt2_   = double90Double30_minPt2  ;
        double90Double30_minPt4_   = double90Double30_minPt4  ;
        quad45_minSumPt_           = quad45_minSumPt          ;
        quad45_minPt4_             = quad45_minPt4            ;
    }
    
    
private:
    void  createTriggerSimulatedBranches()                                    override;
    void  extractInformationFromEvent         (std::vector<Jet> selectedJets) override;
    std::tuple<float, float, float> calculateMonteCarloTriggerEfficiency() override;
    std::tuple<float, float, float> calculateDataTriggerEfficiency      () override;

    std::tuple<float, float, float> calculateDataDouble90Double30Efficiency ();
    std::tuple<float, float, float> calculateDataQuad45Efficiency           ();
    std::tuple<float, float, float> calculateDataAndEfficiency              ();

    std::tuple<float, float, float> calculateMonteCarloDouble90Double30Efficiency ();
    std::tuple<float, float, float> calculateMonteCarloQuad45Efficiency           ();
    std::tuple<float, float, float> calculateMonteCarloAndEfficiency              ();

    inline float computeDouble90Double30Efficiency(float bTagEfficiency, float effL1, float effQuad30CaloJet, float effDouble90CaloJet, float effQuad30PFJet, float effDouble90PFJet)
    {
        return fixInLimits(effL1) * fixInLimits(effQuad30CaloJet) * fixInLimits(effDouble90CaloJet) * fixInLimits(bTagEfficiency) * fixInLimits(effQuad30PFJet) * fixInLimits(effDouble90PFJet);
    }

    inline float computeQuad45Efficiency(float bTagEfficiency, float effL1, float effQuad45CaloJet, float effQuad45PFJet)
    {
        return fixInLimits(effL1) * fixInLimits(effQuad45CaloJet) * fixInLimits(bTagEfficiency) * fixInLimits(effQuad45PFJet);
    }

    inline float computeAndEfficiency(float effL1, float effQuad45CaloJet, float effQuad45PFJet)
    {
        return fixInLimits(effL1) * fixInLimits(effQuad45CaloJet) *fixInLimits(effQuad45PFJet);
    }

    
    TriggerFitCurves2016 fTriggerFitCurves;
    float double90Double30_minSumPt_  {0.};
    float double90Double30_minPt2_    {0.};
    float double90Double30_minPt4_    {0.};
    float quad45_minSumPt_            {0.};
    float quad45_minPt4_              {0.};
    
    float pt1_        {0.};
    float pt2_        {0.};
    float pt3_        {0.};
    float pt4_        {0.};
    float sumPt_      {0.};
    float caloJetSum_  {0.};
    float pfJetSum_    {0.};
    float onlyJetSum_  {0.};
    std::vector<float> deepFlavBVector{0., 0., 0., 0.} ;
};

//================= 2017
class TriggerEfficiencyCalculator_2017 : public TriggerEfficiencyCalculator
{
public:
    TriggerEfficiencyCalculator_2017(std::string inputFileName, NanoAODTree& nat);
    ~TriggerEfficiencyCalculator_2017();
    bool isPassingTurnOnCuts(std::vector<std::string> listOfPassedTriggers, const std::vector<Jet>& selectedJets) override {return false;}
    
    
private:
    void  createTriggerSimulatedBranches()                                    override;
    void  extractInformationFromEvent         (std::vector<Jet> selectedJets) override;
    std::tuple<float, float, float> calculateMonteCarloTriggerEfficiency()    override;
    std::tuple<float, float, float> calculateDataTriggerEfficiency      ()    override;

    inline float computeTriggerEfficiency(float threeBtagEfficiency, float twoBtagEfficiency, float effL1, float effQuad30CaloJet, float effCaloHT, float effQuad30PFJet, float effSingle75PFJet, float effDouble60PFJet, float effTriple54PFJet, float effQuad40PFJet, float effPFHT)
    {
      return threeBtagEfficiency * twoBtagEfficiency * fixInLimits(effL1) * fixInLimits(effQuad30CaloJet) * fixInLimits(effCaloHT) * fixInLimits(effQuad30PFJet) * fixInLimits(effSingle75PFJet) * fixInLimits(effDouble60PFJet) * fixInLimits(effTriple54PFJet) * fixInLimits(effQuad40PFJet) * fixInLimits(effPFHT);
    }
    
    TriggerFitCurves2017 fTriggerFitCurves;
    float pt1_         {0.};
    float pt2_         {0.};
    float pt3_         {0.};
    float pt4_         {0.};
    float caloJetSum_  {0.};
    float pfJetSum_    {0.};
    float onlyJetSum_  {0.};
    std::vector<float> deepFlavBVector{0., 0., 0., 0.} ;
};

//================= 2018
class TriggerEfficiencyCalculator_2018 : public TriggerEfficiencyCalculator
{
public:
    TriggerEfficiencyCalculator_2018(std::string inputFileName, NanoAODTree& nat);
    ~TriggerEfficiencyCalculator_2018();
    bool isPassingTurnOnCuts(std::vector<std::string> listOfPassedTriggers, const std::vector<Jet>& selectedJets) override {return false;}

private:
    void  createTriggerSimulatedBranches()                                    override;
    void  extractInformationFromEvent         (std::vector<Jet> selectedJets) override;
    std::tuple<float, float, float> calculateMonteCarloTriggerEfficiency()    override;
    std::tuple<float, float, float> calculateDataTriggerEfficiency      ()    override;

    inline float computeTriggerEfficiency(float threeBtagEfficiency, float twoBtagEfficiency, float effL1, float effQuad30CaloJet, float effCaloHT, float effQuad30PFJet, float effSingle75PFJet, float effDouble60PFJet, float effTriple54PFJet, float effQuad40PFJet, float effPFHT)
    {
      return threeBtagEfficiency * twoBtagEfficiency * fixInLimits(effL1) * fixInLimits(effQuad30CaloJet) * fixInLimits(effCaloHT) * fixInLimits(effQuad30PFJet) * fixInLimits(effSingle75PFJet) * fixInLimits(effDouble60PFJet) * fixInLimits(effTriple54PFJet) * fixInLimits(effQuad40PFJet) * fixInLimits(effPFHT);
    }
    
    TriggerFitCurves2018 fTriggerFitCurves;
    float pt1_         {0.};
    float pt2_         {0.};
    float pt3_         {0.};
    float pt4_         {0.};
    float caloJetSum_  {0.};
    float pfJetSum_    {0.};
    float onlyJetSum_  {0.};
    std::vector<float> deepFlavBVector{0., 0., 0., 0.} ;
};

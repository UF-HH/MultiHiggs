#include "TFile.h"
#include "TF1.h"
#include "TFitResult.h"
#include "TGraphAsymmErrors.h"
#include "Math/WrappedMultiTF1.h"

class TriggerFitCurves2017
{
 private:
  class KFitResult : public TFitResult
   {
   public:
     using TFitResult::TFitResult;
     KFitResult* ResetModelFunction(TF1* func){
       this->SetModelFunction(std::shared_ptr<IModelFunction>(dynamic_cast<IModelFunction*>(ROOT::Math::WrappedMultiTF1(*func).Clone())));
       return this;
     }
   };

 std::pair<TF1*,KFitResult*> createPair(TF1* theFunction, KFitResult* theFitResult )
   {
     theFitResult->ResetModelFunction(theFunction);
     return {theFunction, theFitResult};
   }
 
 TFile triggerFitFile;
 
 public:
 
 TriggerFitCurves2017(std::string fileName)
   : triggerFitFile(fileName.data())
   {
     fSingleMuon__Efficiency_L1calojetsPFHTPair = createPair(((TGraphAsymmErrors*)triggerFitFile.Get("Data__Efficiency_L1calojetsPFHT"))->GetFunction("cdf"),
							 (KFitResult*)triggerFitFile.Get("Data__Efficiency_L1calojetsPFHT_FitResult"));
     
     fSingleMuon__Efficiency_QuadCentralJet30Pair = createPair(((TGraphAsymmErrors*)triggerFitFile.Get("Data__Efficiency_QuadCentralJet30"))->GetFunction("cdf"),
							       (KFitResult*)triggerFitFile.Get("Data__Efficiency_QuadCentralJet30_FitResult"));
     
     fSingleMuon__Efficiency_CaloQuadJet30HT300Pair = createPair(((TGraphAsymmErrors*)triggerFitFile.Get("Data__Efficiency_CaloQuadJet30HT300"))->GetFunction("cdf"),
								 (KFitResult*)triggerFitFile.Get("Data__Efficiency_CaloQuadJet30HT300_FitResult"));
     
     fSingleMuon__Efficiency_BTagCaloCSVp05DoublePair = createPair(((TGraphAsymmErrors*)triggerFitFile.Get("Data__Efficiency_BTagCaloCSVp05Double"))->GetFunction("cdf"),
								   (KFitResult*)triggerFitFile.Get("Data__Efficiency_BTagCaloCSVp05Double_FitResult"));
     
     fSingleMuon__Efficiency_PFCentralJetLooseIDQuad30Pair = createPair(((TGraphAsymmErrors*)triggerFitFile.Get("Data__Efficiency_PFCentralJetLooseIDQuad30"))->GetFunction("cdf"),
									(KFitResult*)triggerFitFile.Get("Data__Efficiency_PFCentralJetLooseIDQuad30_FitResult"));
     
     fSingleMuon__Efficiency_1PFCentralJetLooseID75Pair = createPair(((TGraphAsymmErrors*)triggerFitFile.Get("Data__Efficiency_1PFCentralJetLooseID75"))->GetFunction("cdf"),
								     (KFitResult*)triggerFitFile.Get("Data__Efficiency_1PFCentralJetLooseID75_FitResult"));
     
     fSingleMuon__Efficiency_2PFCentralJetLooseID60Pair = createPair(((TGraphAsymmErrors*)triggerFitFile.Get("Data__Efficiency_2PFCentralJetLooseID60"))->GetFunction("cdf"),
								     (KFitResult*)triggerFitFile.Get("Data__Efficiency_2PFCentralJetLooseID60_FitResult"));
     
     fSingleMuon__Efficiency_3PFCentralJetLooseID45Pair = createPair(((TGraphAsymmErrors*)triggerFitFile.Get("Data__Efficiency_3PFCentralJetLooseID45"))->GetFunction("cdf"),
								     (KFitResult*)triggerFitFile.Get("Data__Efficiency_3PFCentralJetLooseID45_FitResult"));
     
     fSingleMuon__Efficiency_4PFCentralJetLooseID40Pair = createPair(((TGraphAsymmErrors*)triggerFitFile.Get("Data__Efficiency_4PFCentralJetLooseID40"))->GetFunction("cdf"),
								     (KFitResult*)triggerFitFile.Get("Data__Efficiency_4PFCentralJetLooseID40_FitResult"));

     fSingleMuon__Efficiency_PFCentralJetsLooseIDQuad30HT300Pair = createPair(((TGraphAsymmErrors*)triggerFitFile.Get("Data__Efficiency_PFCentralJetsLooseIDQuad30HT300"))->GetFunction("cdf"),
									      (KFitResult*)triggerFitFile.Get("Data__Efficiency_PFCentralJetsLooseIDQuad30HT300_FitResult"));
     
     fSingleMuon__Efficiency_BTagPFCSVp070TriplePair = createPair(((TGraphAsymmErrors*)triggerFitFile.Get("Data__Efficiency_BTagPFCSVp070Triple"))->GetFunction("cdf"),
								  (KFitResult*)triggerFitFile.Get("Data__Efficiency_BTagPFCSVp070Triple_FitResult"));

     fTTbar__Efficiency_L1calojetsPFHTPair = createPair(((TGraphAsymmErrors*)triggerFitFile.Get("Simulation__Efficiency_L1calojetsPFHT"))->GetFunction("cdf"),
						    (KFitResult*)triggerFitFile.Get("Simulation__Efficiency_L1calojetsPFHT_FitResult"));
     
     fTTbar__Efficiency_QuadCentralJet30Pair = createPair(((TGraphAsymmErrors*)triggerFitFile.Get("Simulation__Efficiency_QuadCentralJet30"))->GetFunction("cdf"),
							  (KFitResult*)triggerFitFile.Get("Simulation__Efficiency_QuadCentralJet30_FitResult"));
     
     fTTbar__Efficiency_CaloQuadJet30HT300Pair = createPair(((TGraphAsymmErrors*)triggerFitFile.Get("Simulation__Efficiency_CaloQuadJet30HT300"))->GetFunction("cdf"),
							    (KFitResult*)triggerFitFile.Get("Simulation__Efficiency_CaloQuadJet30HT300_FitResult"));
     
     fTTbar__Efficiency_BTagCaloCSVp05DoublePair = createPair(((TGraphAsymmErrors*)triggerFitFile.Get("Simulation__Efficiency_BTagCaloCSVp05Double"))->GetFunction("cdf"),
							      (KFitResult*)triggerFitFile.Get("Simulation__Efficiency_BTagCaloCSVp05Double_FitResult"));

     fTTbar__Efficiency_PFCentralJetLooseIDQuad30Pair = createPair(((TGraphAsymmErrors*)triggerFitFile.Get("Simulation__Efficiency_PFCentralJetLooseIDQuad30"))->GetFunction("cdf"),
								   (KFitResult*)triggerFitFile.Get("Simulation__Efficiency_PFCentralJetLooseIDQuad30_FitResult"));

     fTTbar__Efficiency_1PFCentralJetLooseID75Pair = createPair(((TGraphAsymmErrors*)triggerFitFile.Get("Simulation__Efficiency_1PFCentralJetLooseID75"))->GetFunction("cdf"),
								(KFitResult*)triggerFitFile.Get("Simulation__Efficiency_1PFCentralJetLooseID75_FitResult"));

     fTTbar__Efficiency_2PFCentralJetLooseID60Pair = createPair(((TGraphAsymmErrors*)triggerFitFile.Get("Simulation__Efficiency_2PFCentralJetLooseID60"))->GetFunction("cdf"),
								(KFitResult*)triggerFitFile.Get("Simulation__Efficiency_2PFCentralJetLooseID60_FitResult"));

     fTTbar__Efficiency_3PFCentralJetLooseID45Pair = createPair(((TGraphAsymmErrors*)triggerFitFile.Get("Simulation__Efficiency_3PFCentralJetLooseID45"))->GetFunction("cdf"),
								(KFitResult*)triggerFitFile.Get("Simulation__Efficiency_3PFCentralJetLooseID45_FitResult"));

     fTTbar__Efficiency_4PFCentralJetLooseID40Pair = createPair(((TGraphAsymmErrors*)triggerFitFile.Get("Simulation__Efficiency_4PFCentralJetLooseID40"))->GetFunction("cdf"),
								(KFitResult*)triggerFitFile.Get("Simulation__Efficiency_4PFCentralJetLooseID40_FitResult"));
     
     fTTbar__Efficiency_PFCentralJetsLooseIDQuad30HT300Pair = createPair(((TGraphAsymmErrors*)triggerFitFile.Get("Simulation__Efficiency_PFCentralJetsLooseIDQuad30HT300"))->GetFunction("cdf"),
									 (KFitResult*)triggerFitFile.Get("Simulation__Efficiency_PFCentralJetsLooseIDQuad30HT300_FitResult"));
     
     fTTbar__Efficiency_BTagPFCSVp070TriplePair = createPair(((TGraphAsymmErrors*)triggerFitFile.Get("Simulation__Efficiency_BTagPFCSVp070Triple"))->GetFunction("cdf"),
							     (KFitResult*)triggerFitFile.Get("Simulation__Efficiency_BTagPFCSVp070Triple_FitResult"));
   }
 ~TriggerFitCurves2017()
   {
     triggerFitFile.Close();
   }
 std::pair<TF1*, KFitResult*> fSingleMuon__Efficiency_L1calojetsPFHTPair;
 std::pair<TF1*, KFitResult*> fSingleMuon__Efficiency_QuadCentralJet30Pair;
 std::pair<TF1*, KFitResult*> fSingleMuon__Efficiency_CaloQuadJet30HT300Pair;
 std::pair<TF1*, KFitResult*> fSingleMuon__Efficiency_BTagCaloCSVp05DoublePair;
 std::pair<TF1*, KFitResult*> fSingleMuon__Efficiency_PFCentralJetLooseIDQuad30Pair;
 std::pair<TF1*, KFitResult*> fSingleMuon__Efficiency_1PFCentralJetLooseID75Pair;
 std::pair<TF1*, KFitResult*> fSingleMuon__Efficiency_2PFCentralJetLooseID60Pair;
 std::pair<TF1*, KFitResult*> fSingleMuon__Efficiency_3PFCentralJetLooseID45Pair;
 std::pair<TF1*, KFitResult*> fSingleMuon__Efficiency_4PFCentralJetLooseID40Pair;
 std::pair<TF1*, KFitResult*> fSingleMuon__Efficiency_PFCentralJetsLooseIDQuad30HT300Pair;
 std::pair<TF1*, KFitResult*> fSingleMuon__Efficiency_BTagPFCSVp070TriplePair;
 std::pair<TF1*, KFitResult*> fTTbar__Efficiency_L1calojetsPFHTPair;
 std::pair<TF1*, KFitResult*> fTTbar__Efficiency_QuadCentralJet30Pair;
 std::pair<TF1*, KFitResult*> fTTbar__Efficiency_CaloQuadJet30HT300Pair;
 std::pair<TF1*, KFitResult*> fTTbar__Efficiency_BTagCaloCSVp05DoublePair;
 std::pair<TF1*, KFitResult*> fTTbar__Efficiency_PFCentralJetLooseIDQuad30Pair;
 std::pair<TF1*, KFitResult*> fTTbar__Efficiency_1PFCentralJetLooseID75Pair;
 std::pair<TF1*, KFitResult*> fTTbar__Efficiency_2PFCentralJetLooseID60Pair;
 std::pair<TF1*, KFitResult*> fTTbar__Efficiency_3PFCentralJetLooseID45Pair;
 std::pair<TF1*, KFitResult*> fTTbar__Efficiency_4PFCentralJetLooseID40Pair;
 std::pair<TF1*, KFitResult*> fTTbar__Efficiency_PFCentralJetsLooseIDQuad30HT300Pair;
 std::pair<TF1*, KFitResult*> fTTbar__Efficiency_BTagPFCSVp070TriplePair;
};

#include "TFile.h"
#include "TF1.h"
#include "TFitResult.h"
#include "TGraphAsymmErrors.h"
#include "Math/WrappedMultiTF1.h"

class TriggerFitCurves2018
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

        TriggerFitCurves2018(std::string fileName)
        : triggerFitFile(fileName.data())
        {

            fSingleMuon__Efficiency_L1filterHTPair = createPair(
                ((TGraphAsymmErrors*)triggerFitFile.Get("SingleMuon__Efficiency_L1filterHT"))->GetFunction("cdf"),
                (KFitResult*)triggerFitFile.Get("SingleMuon__Efficiency_L1filterHT_FitResult")
            );

            fSingleMuon__Efficiency_QuadCentralJet30Pair = createPair(
                ((TGraphAsymmErrors*)triggerFitFile.Get("SingleMuon__Efficiency_QuadCentralJet30"))->GetFunction("cdf"),
                (KFitResult*)triggerFitFile.Get("SingleMuon__Efficiency_QuadCentralJet30_FitResult")
            );

            fSingleMuon__Efficiency_CaloQuadJet30HT320Pair = createPair(
                ((TGraphAsymmErrors*)triggerFitFile.Get("SingleMuon__Efficiency_CaloQuadJet30HT320"))->GetFunction("cdf"),
                (KFitResult*)triggerFitFile.Get("SingleMuon__Efficiency_CaloQuadJet30HT320_FitResult")
            );

            fSingleMuon__Efficiency_BTagCaloDeepCSVp17DoublePair = createPair(
                ((TGraphAsymmErrors*)triggerFitFile.Get("SingleMuon__Efficiency_BTagCaloDeepCSVp17Double"))->GetFunction("cdf"),
                (KFitResult*)triggerFitFile.Get("SingleMuon__Efficiency_BTagCaloDeepCSVp17Double_FitResult")
            );

            fSingleMuon__Efficiency_PFCentralJetLooseIDQuad30Pair = createPair(
                ((TGraphAsymmErrors*)triggerFitFile.Get("SingleMuon__Efficiency_PFCentralJetLooseIDQuad30"))->GetFunction("cdf"),
                (KFitResult*)triggerFitFile.Get("SingleMuon__Efficiency_PFCentralJetLooseIDQuad30_FitResult")
            );

            fSingleMuon__Efficiency_1PFCentralJetLooseID75Pair = createPair(
                ((TGraphAsymmErrors*)triggerFitFile.Get("SingleMuon__Efficiency_1PFCentralJetLooseID75"))->GetFunction("cdf"),
                (KFitResult*)triggerFitFile.Get("SingleMuon__Efficiency_1PFCentralJetLooseID75_FitResult")
            );

            fSingleMuon__Efficiency_2PFCentralJetLooseID60Pair = createPair(
                ((TGraphAsymmErrors*)triggerFitFile.Get("SingleMuon__Efficiency_2PFCentralJetLooseID60"))->GetFunction("cdf"),
                (KFitResult*)triggerFitFile.Get("SingleMuon__Efficiency_2PFCentralJetLooseID60_FitResult")
            );

            fSingleMuon__Efficiency_3PFCentralJetLooseID45Pair = createPair(
                ((TGraphAsymmErrors*)triggerFitFile.Get("SingleMuon__Efficiency_3PFCentralJetLooseID45"))->GetFunction("cdf"),
                (KFitResult*)triggerFitFile.Get("SingleMuon__Efficiency_3PFCentralJetLooseID45_FitResult")
            );

            fSingleMuon__Efficiency_4PFCentralJetLooseID40Pair = createPair(
                ((TGraphAsymmErrors*)triggerFitFile.Get("SingleMuon__Efficiency_4PFCentralJetLooseID40"))->GetFunction("cdf"),
                (KFitResult*)triggerFitFile.Get("SingleMuon__Efficiency_4PFCentralJetLooseID40_FitResult")
            );

            fSingleMuon__Efficiency_PFCentralJetsLooseIDQuad30HT330Pair = createPair(
                ((TGraphAsymmErrors*)triggerFitFile.Get("SingleMuon__Efficiency_PFCentralJetsLooseIDQuad30HT330"))->GetFunction("cdf"),
                (KFitResult*)triggerFitFile.Get("SingleMuon__Efficiency_PFCentralJetsLooseIDQuad30HT330_FitResult")
            );

            fSingleMuon__Efficiency_BTagPFDeepCSV4p5TriplePair = createPair(
                ((TGraphAsymmErrors*)triggerFitFile.Get("SingleMuon__Efficiency_BTagPFDeepCSV4p5Triple"))->GetFunction("cdf"),
                (KFitResult*)triggerFitFile.Get("SingleMuon__Efficiency_BTagPFDeepCSV4p5Triple_FitResult")
            );

            fTTbar__Efficiency_L1filterHTPair = createPair(
                ((TGraphAsymmErrors*)triggerFitFile.Get("TTbar__Efficiency_L1filterHT"))->GetFunction("cdf"),
                (KFitResult*)triggerFitFile.Get("TTbar__Efficiency_L1filterHT_FitResult")
            );

            fTTbar__Efficiency_QuadCentralJet30Pair = createPair(
                ((TGraphAsymmErrors*)triggerFitFile.Get("TTbar__Efficiency_QuadCentralJet30"))->GetFunction("cdf"),
                (KFitResult*)triggerFitFile.Get("TTbar__Efficiency_QuadCentralJet30_FitResult")
            );

            fTTbar__Efficiency_CaloQuadJet30HT320Pair = createPair(
                ((TGraphAsymmErrors*)triggerFitFile.Get("TTbar__Efficiency_CaloQuadJet30HT320"))->GetFunction("cdf"),
                (KFitResult*)triggerFitFile.Get("TTbar__Efficiency_CaloQuadJet30HT320_FitResult")
            );

            fTTbar__Efficiency_BTagCaloDeepCSVp17DoublePair = createPair(
                ((TGraphAsymmErrors*)triggerFitFile.Get("TTbar__Efficiency_BTagCaloDeepCSVp17Double"))->GetFunction("cdf"),
                (KFitResult*)triggerFitFile.Get("TTbar__Efficiency_BTagCaloDeepCSVp17Double_FitResult")
            );

            fTTbar__Efficiency_PFCentralJetLooseIDQuad30Pair = createPair(
                ((TGraphAsymmErrors*)triggerFitFile.Get("TTbar__Efficiency_PFCentralJetLooseIDQuad30"))->GetFunction("cdf"),
                (KFitResult*)triggerFitFile.Get("TTbar__Efficiency_PFCentralJetLooseIDQuad30_FitResult")
            );

            fTTbar__Efficiency_1PFCentralJetLooseID75Pair = createPair(
                ((TGraphAsymmErrors*)triggerFitFile.Get("TTbar__Efficiency_1PFCentralJetLooseID75"))->GetFunction("cdf"),
                (KFitResult*)triggerFitFile.Get("TTbar__Efficiency_1PFCentralJetLooseID75_FitResult")
            );

            fTTbar__Efficiency_2PFCentralJetLooseID60Pair = createPair(
                ((TGraphAsymmErrors*)triggerFitFile.Get("TTbar__Efficiency_2PFCentralJetLooseID60"))->GetFunction("cdf"),
                (KFitResult*)triggerFitFile.Get("TTbar__Efficiency_2PFCentralJetLooseID60_FitResult")
            );

            fTTbar__Efficiency_3PFCentralJetLooseID45Pair = createPair(
                ((TGraphAsymmErrors*)triggerFitFile.Get("TTbar__Efficiency_3PFCentralJetLooseID45"))->GetFunction("cdf"),
                (KFitResult*)triggerFitFile.Get("TTbar__Efficiency_3PFCentralJetLooseID45_FitResult")
            );

            fTTbar__Efficiency_4PFCentralJetLooseID40Pair = createPair(
                ((TGraphAsymmErrors*)triggerFitFile.Get("TTbar__Efficiency_4PFCentralJetLooseID40"))->GetFunction("cdf"),
                (KFitResult*)triggerFitFile.Get("TTbar__Efficiency_4PFCentralJetLooseID40_FitResult")
            );

            fTTbar__Efficiency_PFCentralJetsLooseIDQuad30HT330Pair = createPair(
                ((TGraphAsymmErrors*)triggerFitFile.Get("TTbar__Efficiency_PFCentralJetsLooseIDQuad30HT330"))->GetFunction("cdf"),
                (KFitResult*)triggerFitFile.Get("TTbar__Efficiency_PFCentralJetsLooseIDQuad30HT330_FitResult")
            );

            fTTbar__Efficiency_BTagPFDeepCSV4p5TriplePair = createPair(
                ((TGraphAsymmErrors*)triggerFitFile.Get("TTbar__Efficiency_BTagPFDeepCSV4p5Triple"))->GetFunction("cdf"),
                (KFitResult*)triggerFitFile.Get("TTbar__Efficiency_BTagPFDeepCSV4p5Triple_FitResult")
            );


        }
        ~TriggerFitCurves2018()
        {
            triggerFitFile.Close();
        }

        std::pair<TF1*, KFitResult*> fSingleMuon__Efficiency_L1filterHTPair;
        std::pair<TF1*, KFitResult*> fSingleMuon__Efficiency_QuadCentralJet30Pair;
        std::pair<TF1*, KFitResult*> fSingleMuon__Efficiency_CaloQuadJet30HT320Pair;
        std::pair<TF1*, KFitResult*> fSingleMuon__Efficiency_BTagCaloDeepCSVp17DoublePair;
        std::pair<TF1*, KFitResult*> fSingleMuon__Efficiency_PFCentralJetLooseIDQuad30Pair;
        std::pair<TF1*, KFitResult*> fSingleMuon__Efficiency_1PFCentralJetLooseID75Pair;
        std::pair<TF1*, KFitResult*> fSingleMuon__Efficiency_2PFCentralJetLooseID60Pair;
        std::pair<TF1*, KFitResult*> fSingleMuon__Efficiency_3PFCentralJetLooseID45Pair;
        std::pair<TF1*, KFitResult*> fSingleMuon__Efficiency_4PFCentralJetLooseID40Pair;
        std::pair<TF1*, KFitResult*> fSingleMuon__Efficiency_PFCentralJetsLooseIDQuad30HT330Pair;
        std::pair<TF1*, KFitResult*> fSingleMuon__Efficiency_BTagPFDeepCSV4p5TriplePair;
        std::pair<TF1*, KFitResult*> fTTbar__Efficiency_L1filterHTPair;
        std::pair<TF1*, KFitResult*> fTTbar__Efficiency_QuadCentralJet30Pair;
        std::pair<TF1*, KFitResult*> fTTbar__Efficiency_CaloQuadJet30HT320Pair;
        std::pair<TF1*, KFitResult*> fTTbar__Efficiency_BTagCaloDeepCSVp17DoublePair;
        std::pair<TF1*, KFitResult*> fTTbar__Efficiency_PFCentralJetLooseIDQuad30Pair;
        std::pair<TF1*, KFitResult*> fTTbar__Efficiency_1PFCentralJetLooseID75Pair;
        std::pair<TF1*, KFitResult*> fTTbar__Efficiency_2PFCentralJetLooseID60Pair;
        std::pair<TF1*, KFitResult*> fTTbar__Efficiency_3PFCentralJetLooseID45Pair;
        std::pair<TF1*, KFitResult*> fTTbar__Efficiency_4PFCentralJetLooseID40Pair;
        std::pair<TF1*, KFitResult*> fTTbar__Efficiency_PFCentralJetsLooseIDQuad30HT330Pair;
        std::pair<TF1*, KFitResult*> fTTbar__Efficiency_BTagPFDeepCSV4p5TriplePair;

};

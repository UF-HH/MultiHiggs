#include "TFile.h"
#include "TF1.h"
#include "TFitResult.h"
#include "TGraphAsymmErrors.h"
#include "Math/WrappedMultiTF1.h"

class TriggerFitCurves2016
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

        TriggerFitCurves2016(std::string fileName)
        : triggerFitFile(fileName.data())
        {
            fSingleMuon_Double90Quad30_Efficiency_L1filterHTPair = createPair(
                ((TGraphAsymmErrors*)triggerFitFile.Get("SingleMuon_Double90Quad30_Efficiency_L1filterHT"))->GetFunction("cdf"),
                (KFitResult*)triggerFitFile.Get("SingleMuon_Double90Quad30_Efficiency_L1filterHT_FitResult")
            );

            fSingleMuon_Double90Quad30_Efficiency_QuadCentralJet30Pair = createPair(
                ((TGraphAsymmErrors*)triggerFitFile.Get("SingleMuon_Double90Quad30_Efficiency_QuadCentralJet30"))->GetFunction("cdf"),
                (KFitResult*)triggerFitFile.Get("SingleMuon_Double90Quad30_Efficiency_QuadCentralJet30_FitResult")
            );

            fSingleMuon_Double90Quad30_Efficiency_DoubleCentralJet90Pair = createPair(
                ((TGraphAsymmErrors*)triggerFitFile.Get("SingleMuon_Double90Quad30_Efficiency_DoubleCentralJet90"))->GetFunction("cdf"),
                (KFitResult*)triggerFitFile.Get("SingleMuon_Double90Quad30_Efficiency_DoubleCentralJet90_FitResult")
            );

            fSingleMuon_Double90Quad30_Efficiency_BTagCaloCSVp087TriplePair = createPair(
                ((TGraphAsymmErrors*)triggerFitFile.Get("SingleMuon_Double90Quad30_Efficiency_BTagCaloCSVp087Triple"))->GetFunction("cdf"),
                (KFitResult*)triggerFitFile.Get("SingleMuon_Double90Quad30_Efficiency_BTagCaloCSVp087Triple_FitResult")
            );

            fSingleMuon_Double90Quad30_Efficiency_QuadPFCentralJetLooseID30Pair = createPair(
                ((TGraphAsymmErrors*)triggerFitFile.Get("SingleMuon_Double90Quad30_Efficiency_QuadPFCentralJetLooseID30"))->GetFunction("cdf"),
                (KFitResult*)triggerFitFile.Get("SingleMuon_Double90Quad30_Efficiency_QuadPFCentralJetLooseID30_FitResult")
            );

            fSingleMuon_Double90Quad30_Efficiency_DoublePFCentralJetLooseID90Pair = createPair(
                ((TGraphAsymmErrors*)triggerFitFile.Get("SingleMuon_Double90Quad30_Efficiency_DoublePFCentralJetLooseID90"))->GetFunction("cdf"),
                (KFitResult*)triggerFitFile.Get("SingleMuon_Double90Quad30_Efficiency_DoublePFCentralJetLooseID90_FitResult")
            );

            fSingleMuon_Quad45_Efficiency_L1filterHTPair = createPair(
                ((TGraphAsymmErrors*)triggerFitFile.Get("SingleMuon_Quad45_Efficiency_L1filterHT"))->GetFunction("cdf"),
                (KFitResult*)triggerFitFile.Get("SingleMuon_Quad45_Efficiency_L1filterHT_FitResult")
            );

            fSingleMuon_Quad45_Efficiency_QuadCentralJet45Pair = createPair(
                ((TGraphAsymmErrors*)triggerFitFile.Get("SingleMuon_Quad45_Efficiency_QuadCentralJet45"))->GetFunction("cdf"),
                (KFitResult*)triggerFitFile.Get("SingleMuon_Quad45_Efficiency_QuadCentralJet45_FitResult")
            );

            fSingleMuon_Quad45_Efficiency_BTagCaloCSVp087TriplePair = createPair(
                ((TGraphAsymmErrors*)triggerFitFile.Get("SingleMuon_Quad45_Efficiency_BTagCaloCSVp087Triple"))->GetFunction("cdf"),
                (KFitResult*)triggerFitFile.Get("SingleMuon_Quad45_Efficiency_BTagCaloCSVp087Triple_FitResult")
            );

            fSingleMuon_Quad45_Efficiency_QuadPFCentralJetLooseID45Pair = createPair(
                ((TGraphAsymmErrors*)triggerFitFile.Get("SingleMuon_Quad45_Efficiency_QuadPFCentralJetLooseID45"))->GetFunction("cdf"),
                (KFitResult*)triggerFitFile.Get("SingleMuon_Quad45_Efficiency_QuadPFCentralJetLooseID45_FitResult")
            );

            fSingleMuon_And_Efficiency_L1filterQuad45HTPair = createPair(
                ((TGraphAsymmErrors*)triggerFitFile.Get("SingleMuon_And_Efficiency_L1filterQuad45HT"))->GetFunction("cdf"),
                (KFitResult*)triggerFitFile.Get("SingleMuon_And_Efficiency_L1filterQuad45HT_FitResult")
            );

            fSingleMuon_And_Efficiency_QuadCentralJet45Pair = createPair(
                ((TGraphAsymmErrors*)triggerFitFile.Get("SingleMuon_And_Efficiency_QuadCentralJet45"))->GetFunction("cdf"),
                (KFitResult*)triggerFitFile.Get("SingleMuon_And_Efficiency_QuadCentralJet45_FitResult")
            );

            fSingleMuon_And_Efficiency_QuadPFCentralJetLooseID45Pair = createPair(
                ((TGraphAsymmErrors*)triggerFitFile.Get("SingleMuon_And_Efficiency_QuadPFCentralJetLooseID45"))->GetFunction("cdf"),
                (KFitResult*)triggerFitFile.Get("SingleMuon_And_Efficiency_QuadPFCentralJetLooseID45_FitResult")
            );

            fTTbar_Double90Quad30_Efficiency_L1filterHTPair = createPair(
                ((TGraphAsymmErrors*)triggerFitFile.Get("TTbar_Double90Quad30_Efficiency_L1filterHT"))->GetFunction("cdf"),
                (KFitResult*)triggerFitFile.Get("TTbar_Double90Quad30_Efficiency_L1filterHT_FitResult")
            );

            fTTbar_Double90Quad30_Efficiency_QuadCentralJet30Pair = createPair(
                ((TGraphAsymmErrors*)triggerFitFile.Get("TTbar_Double90Quad30_Efficiency_QuadCentralJet30"))->GetFunction("cdf"),
                (KFitResult*)triggerFitFile.Get("TTbar_Double90Quad30_Efficiency_QuadCentralJet30_FitResult")
            );

            fTTbar_Double90Quad30_Efficiency_DoubleCentralJet90Pair = createPair(
                ((TGraphAsymmErrors*)triggerFitFile.Get("TTbar_Double90Quad30_Efficiency_DoubleCentralJet90"))->GetFunction("cdf"),
                (KFitResult*)triggerFitFile.Get("TTbar_Double90Quad30_Efficiency_DoubleCentralJet90_FitResult")
            );

            fTTbar_Double90Quad30_Efficiency_BTagCaloCSVp087TriplePair = createPair(
                ((TGraphAsymmErrors*)triggerFitFile.Get("TTbar_Double90Quad30_Efficiency_BTagCaloCSVp087Triple"))->GetFunction("cdf"),
                (KFitResult*)triggerFitFile.Get("TTbar_Double90Quad30_Efficiency_BTagCaloCSVp087Triple_FitResult")
            );

            fTTbar_Double90Quad30_Efficiency_QuadPFCentralJetLooseID30Pair = createPair(
                ((TGraphAsymmErrors*)triggerFitFile.Get("TTbar_Double90Quad30_Efficiency_QuadPFCentralJetLooseID30"))->GetFunction("cdf"),
                (KFitResult*)triggerFitFile.Get("TTbar_Double90Quad30_Efficiency_QuadPFCentralJetLooseID30_FitResult")
            );

            fTTbar_Double90Quad30_Efficiency_DoublePFCentralJetLooseID90Pair = createPair(
                ((TGraphAsymmErrors*)triggerFitFile.Get("TTbar_Double90Quad30_Efficiency_DoublePFCentralJetLooseID90"))->GetFunction("cdf"),
                (KFitResult*)triggerFitFile.Get("TTbar_Double90Quad30_Efficiency_DoublePFCentralJetLooseID90_FitResult")
            );

            fTTbar_Quad45_Efficiency_L1filterHTPair = createPair(
                ((TGraphAsymmErrors*)triggerFitFile.Get("TTbar_Quad45_Efficiency_L1filterHT"))->GetFunction("cdf"),
                (KFitResult*)triggerFitFile.Get("TTbar_Quad45_Efficiency_L1filterHT_FitResult")
            );

            fTTbar_Quad45_Efficiency_QuadCentralJet45Pair = createPair(
                ((TGraphAsymmErrors*)triggerFitFile.Get("TTbar_Quad45_Efficiency_QuadCentralJet45"))->GetFunction("cdf"),
                (KFitResult*)triggerFitFile.Get("TTbar_Quad45_Efficiency_QuadCentralJet45_FitResult")
            );

            fTTbar_Quad45_Efficiency_BTagCaloCSVp087TriplePair = createPair(
                ((TGraphAsymmErrors*)triggerFitFile.Get("TTbar_Quad45_Efficiency_BTagCaloCSVp087Triple"))->GetFunction("cdf"),
                (KFitResult*)triggerFitFile.Get("TTbar_Quad45_Efficiency_BTagCaloCSVp087Triple_FitResult")
            );

            fTTbar_Quad45_Efficiency_QuadPFCentralJetLooseID45Pair = createPair(
                ((TGraphAsymmErrors*)triggerFitFile.Get("TTbar_Quad45_Efficiency_QuadPFCentralJetLooseID45"))->GetFunction("cdf"),
                (KFitResult*)triggerFitFile.Get("TTbar_Quad45_Efficiency_QuadPFCentralJetLooseID45_FitResult")
            );

            fTTbar_And_Efficiency_L1filterQuad45HTPair = createPair(
                ((TGraphAsymmErrors*)triggerFitFile.Get("TTbar_And_Efficiency_L1filterQuad45HT"))->GetFunction("cdf"),
                (KFitResult*)triggerFitFile.Get("TTbar_And_Efficiency_L1filterQuad45HT_FitResult")
            );

            fTTbar_And_Efficiency_QuadCentralJet45Pair = createPair(
                ((TGraphAsymmErrors*)triggerFitFile.Get("TTbar_And_Efficiency_QuadCentralJet45"))->GetFunction("cdf"),
                (KFitResult*)triggerFitFile.Get("TTbar_And_Efficiency_QuadCentralJet45_FitResult")
            );

            fTTbar_And_Efficiency_QuadPFCentralJetLooseID45Pair = createPair(
                ((TGraphAsymmErrors*)triggerFitFile.Get("TTbar_And_Efficiency_QuadPFCentralJetLooseID45"))->GetFunction("cdf"),
                (KFitResult*)triggerFitFile.Get("TTbar_And_Efficiency_QuadPFCentralJetLooseID45_FitResult")
            );

            fSingleMuon_Double90Quad30_Efficiency_BTagCaloCSVp087TripleGraphs = 
            {
                ((TGraphAsymmErrors*)triggerFitFile.Get("SingleMuon_Double90Quad30_Efficiency_BTagCaloCSVp087Triple"    )),
                ((TGraphAsymmErrors*)triggerFitFile.Get("SingleMuon_Double90Quad30_Efficiency_BTagCaloCSVp087TripleUp"  )),
                ((TGraphAsymmErrors*)triggerFitFile.Get("SingleMuon_Double90Quad30_Efficiency_BTagCaloCSVp087TripleDown"))
            };
            std::get<0>(fSingleMuon_Double90Quad30_Efficiency_BTagCaloCSVp087TripleGraphs)->SetBit(TGraph::kIsSortedX);
            std::get<1>(fSingleMuon_Double90Quad30_Efficiency_BTagCaloCSVp087TripleGraphs)->SetBit(TGraph::kIsSortedX);
            std::get<2>(fSingleMuon_Double90Quad30_Efficiency_BTagCaloCSVp087TripleGraphs)->SetBit(TGraph::kIsSortedX);

            fSingleMuon_Quad45_Efficiency_BTagCaloCSVp087TripleGraphs = 
            {
                ((TGraphAsymmErrors*)triggerFitFile.Get("SingleMuon_Quad45_Efficiency_BTagCaloCSVp087Triple"    )),
                ((TGraphAsymmErrors*)triggerFitFile.Get("SingleMuon_Quad45_Efficiency_BTagCaloCSVp087TripleUp"  )),
                ((TGraphAsymmErrors*)triggerFitFile.Get("SingleMuon_Quad45_Efficiency_BTagCaloCSVp087TripleDown"))
            };
            std::get<0>(fSingleMuon_Quad45_Efficiency_BTagCaloCSVp087TripleGraphs)->SetBit(TGraph::kIsSortedX);
            std::get<1>(fSingleMuon_Quad45_Efficiency_BTagCaloCSVp087TripleGraphs)->SetBit(TGraph::kIsSortedX);
            std::get<2>(fSingleMuon_Quad45_Efficiency_BTagCaloCSVp087TripleGraphs)->SetBit(TGraph::kIsSortedX);

            fTTbar_Double90Quad30_Efficiency_BTagCaloCSVp087TripleGraphs = 
            {
                ((TGraphAsymmErrors*)triggerFitFile.Get("TTbar_Double90Quad30_Efficiency_BTagCaloCSVp087Triple"    )),
                ((TGraphAsymmErrors*)triggerFitFile.Get("TTbar_Double90Quad30_Efficiency_BTagCaloCSVp087TripleUp"  )),
                ((TGraphAsymmErrors*)triggerFitFile.Get("TTbar_Double90Quad30_Efficiency_BTagCaloCSVp087TripleDown"))
            };
            std::get<0>(fTTbar_Double90Quad30_Efficiency_BTagCaloCSVp087TripleGraphs)->SetBit(TGraph::kIsSortedX);
            std::get<1>(fTTbar_Double90Quad30_Efficiency_BTagCaloCSVp087TripleGraphs)->SetBit(TGraph::kIsSortedX);
            std::get<2>(fTTbar_Double90Quad30_Efficiency_BTagCaloCSVp087TripleGraphs)->SetBit(TGraph::kIsSortedX);

            fTTbar_Quad45_Efficiency_BTagCaloCSVp087TripleGraphs = 
            {
                ((TGraphAsymmErrors*)triggerFitFile.Get("TTbar_Quad45_Efficiency_BTagCaloCSVp087Triple"    )),
                ((TGraphAsymmErrors*)triggerFitFile.Get("TTbar_Quad45_Efficiency_BTagCaloCSVp087TripleUp"  )),
                ((TGraphAsymmErrors*)triggerFitFile.Get("TTbar_Quad45_Efficiency_BTagCaloCSVp087TripleDown"))
            };
            std::get<0>(fTTbar_Quad45_Efficiency_BTagCaloCSVp087TripleGraphs)->SetBit(TGraph::kIsSortedX);
            std::get<1>(fTTbar_Quad45_Efficiency_BTagCaloCSVp087TripleGraphs)->SetBit(TGraph::kIsSortedX);
            std::get<2>(fTTbar_Quad45_Efficiency_BTagCaloCSVp087TripleGraphs)->SetBit(TGraph::kIsSortedX);

        }
        ~TriggerFitCurves2016()
        {
            triggerFitFile.Close();
        }

        std::pair<TF1*, KFitResult*> fSingleMuon_Double90Quad30_Efficiency_L1filterHTPair                 ;
        std::pair<TF1*, KFitResult*> fSingleMuon_Double90Quad30_Efficiency_QuadCentralJet30Pair           ;
        std::pair<TF1*, KFitResult*> fSingleMuon_Double90Quad30_Efficiency_DoubleCentralJet90Pair         ;
        std::pair<TF1*, KFitResult*> fSingleMuon_Double90Quad30_Efficiency_BTagCaloCSVp087TriplePair      ;
        std::pair<TF1*, KFitResult*> fSingleMuon_Double90Quad30_Efficiency_QuadPFCentralJetLooseID30Pair  ;
        std::pair<TF1*, KFitResult*> fSingleMuon_Double90Quad30_Efficiency_DoublePFCentralJetLooseID90Pair;
        std::pair<TF1*, KFitResult*> fSingleMuon_Quad45_Efficiency_L1filterHTPair                         ;
        std::pair<TF1*, KFitResult*> fSingleMuon_Quad45_Efficiency_QuadCentralJet45Pair                   ;
        std::pair<TF1*, KFitResult*> fSingleMuon_Quad45_Efficiency_BTagCaloCSVp087TriplePair              ;
        std::pair<TF1*, KFitResult*> fSingleMuon_Quad45_Efficiency_QuadPFCentralJetLooseID45Pair          ;
        std::pair<TF1*, KFitResult*> fSingleMuon_And_Efficiency_L1filterQuad45HTPair                      ;
        std::pair<TF1*, KFitResult*> fSingleMuon_And_Efficiency_QuadCentralJet45Pair                      ;
        std::pair<TF1*, KFitResult*> fSingleMuon_And_Efficiency_QuadPFCentralJetLooseID45Pair             ;
        std::pair<TF1*, KFitResult*> fTTbar_Double90Quad30_Efficiency_L1filterHTPair                      ;
        std::pair<TF1*, KFitResult*> fTTbar_Double90Quad30_Efficiency_QuadCentralJet30Pair                ;
        std::pair<TF1*, KFitResult*> fTTbar_Double90Quad30_Efficiency_DoubleCentralJet90Pair              ;
        std::pair<TF1*, KFitResult*> fTTbar_Double90Quad30_Efficiency_BTagCaloCSVp087TriplePair           ;
        std::pair<TF1*, KFitResult*> fTTbar_Double90Quad30_Efficiency_QuadPFCentralJetLooseID30Pair       ;
        std::pair<TF1*, KFitResult*> fTTbar_Double90Quad30_Efficiency_DoublePFCentralJetLooseID90Pair     ;
        std::pair<TF1*, KFitResult*> fTTbar_Quad45_Efficiency_L1filterHTPair                              ;
        std::pair<TF1*, KFitResult*> fTTbar_Quad45_Efficiency_QuadCentralJet45Pair                        ;
        std::pair<TF1*, KFitResult*> fTTbar_Quad45_Efficiency_BTagCaloCSVp087TriplePair                   ;
        std::pair<TF1*, KFitResult*> fTTbar_Quad45_Efficiency_QuadPFCentralJetLooseID45Pair               ;
        std::pair<TF1*, KFitResult*> fTTbar_And_Efficiency_L1filterQuad45HTPair                           ;
        std::pair<TF1*, KFitResult*> fTTbar_And_Efficiency_QuadCentralJet45Pair                           ;
        std::pair<TF1*, KFitResult*> fTTbar_And_Efficiency_QuadPFCentralJetLooseID45Pair                  ;

        std::tuple<TGraphAsymmErrors*, TGraph*, TGraph*> fSingleMuon_Double90Quad30_Efficiency_BTagCaloCSVp087TripleGraphs;
        std::tuple<TGraphAsymmErrors*, TGraph*, TGraph*> fSingleMuon_Quad45_Efficiency_BTagCaloCSVp087TripleGraphs;
        std::tuple<TGraphAsymmErrors*, TGraph*, TGraph*> fTTbar_Double90Quad30_Efficiency_BTagCaloCSVp087TripleGraphs;
        std::tuple<TGraphAsymmErrors*, TGraph*, TGraph*> fTTbar_Quad45_Efficiency_BTagCaloCSVp087TripleGraphs;

};
#include <Riostream.h>
#include <TH1F.h>
#include <TTree.h>
#include <TTreeFormula.h>
#include <TFile.h>
#include <TCanvas.h>
#include "TTreeReaderArray.h"
#include "TTreeReader.h"
#include "TGraphAsymmErrors.h"
#include "TROOT.h"
#include <thread>

template<typename T , typename V>
void customBinCreator(std::vector<T>& theOutputBinVector, V&& xMin)
{
    return;
}

template<typename T, typename V, typename... BinList>
void customBinCreator(std::vector<T>& theOutputBinVector, V&& xMin, V&& xMax, V&& binSize, BinList&&... theBinList)
{
    uint nBins = (xMax - xMin)/binSize;
    if(theOutputBinVector.size()==0) theOutputBinVector.push_back(xMin);
    for(uint bin=1; bin<=nBins; ++bin) theOutputBinVector.push_back( xMin + (xMax-xMin)*(float(bin)/float(nBins)) );
    customBinCreator(theOutputBinVector, xMax, theBinList...);
}

template<typename T, typename V, typename... BinList>
void customBinCreator(std::vector<T>& theOutputBinVector, V&& xMin, BinList&&... theBinList);


struct TriggerEfficiencyTool
{
    TriggerEfficiencyTool(std::string datasetName, TTree* inputTree, TTreeReader* theTreeReader, std::string triggerName, std::string filterCut, std::string variable, std::string normalizationCut, std::string plotTitle, std::vector<float> binVector, Color_t theColor)
        : fVariableHandler(*theTreeReader, variable.data())
        , fFilterEfficiencyCut("filterEfficiencyCut", filterCut.data(), inputTree)
        , fNormalizationEfficiencyCut("normalizationEfficiencyCut", normalizationCut.data(), inputTree)
    {
        std::string plotName =  plotTitle.substr(0, plotTitle.find(";"));
        fFilterEfficiencyHistogram = std::make_shared<TH1F>((datasetName + "_" + triggerName + "_Normalization_"+plotName).data(), ("Normalization "+plotTitle).data(), binVector.size()-1, binVector.data());
        fFilterEfficiencyHistogram->SetDirectory(0);
        fFilterEfficiencyHistogram->Sumw2();
        fFilterEfficiencyHistogram->SetLineColor(theColor);
        fFilterEfficiencyHistogram->SetMarkerColor(theColor);

        fFilterNormalizationHistogram = std::make_shared<TH1F>((datasetName + "_" + triggerName + "_Distribution_"+plotName).data(), ("Distribution "+plotTitle).data(), binVector.size()-1, binVector.data());
        fFilterNormalizationHistogram->SetDirectory(0);
        fFilterNormalizationHistogram->Sumw2();
        fFilterNormalizationHistogram->SetLineColor(theColor);
        fFilterNormalizationHistogram->SetMarkerColor(theColor);


        fEfficiency = std::make_shared<TGraphAsymmErrors>();
        fEfficiency->SetNameTitle((datasetName + "_" + triggerName + "_Efficiency_"+plotName).data(), ("Efficiency "+plotTitle).data());
        fEfficiency->GetYaxis()->SetRangeUser(0., 1.2);
        fEfficiency->SetLineColor(theColor);
        fEfficiency->SetMarkerColor(theColor);
    }

    ~TriggerEfficiencyTool()
    {
    }

    void fillEfficiency(float weightValue, float btag_SFValue)
    {
        if(fNormalizationEfficiencyCut.EvalInstance())
        {
            float variableValue = *fVariableHandler.Get();

            fFilterNormalizationHistogram->Fill(variableValue,weightValue);

            if(fFilterEfficiencyCut.EvalInstance())
            {
                fFilterEfficiencyHistogram->Fill(variableValue,weightValue);
            }
        }   
    }

    std::tuple<std::shared_ptr<TGraphAsymmErrors>,std::shared_ptr<TH1F> > getEfficiencyAndDistribution(float renormalizationValue)
    {
        int numberOfEntries =  fFilterEfficiencyHistogram.get()->GetNbinsX();
        for(Int_t i = 0; i < numberOfEntries+1; ++i) {
            if(fFilterEfficiencyHistogram.get()->GetBinContent(i) > fFilterNormalizationHistogram.get()->GetBinContent(i)) {
                TCanvas theTmpCanvas("c1", "c1");
                auto tmpNormalization = (TH1F*)fFilterNormalizationHistogram.get()->Clone("fTmpNormalization");
                auto tmpEfficiency    = (TH1F*)fFilterEfficiencyHistogram   .get()->Clone("fTmpEfficiency"   );
                tmpNormalization->SetDirectory(0);
                tmpEfficiency   ->SetDirectory(0);
                tmpNormalization->SetLineColor(kBlue);
                tmpEfficiency   ->SetLineColor(kRed );
                tmpNormalization->Draw("hist");
                tmpEfficiency   ->Draw("same");
                theTmpCanvas.SaveAs("tmpsCanvas.png");
                delete tmpNormalization;
                delete tmpEfficiency   ;
                std::cout<<"NumberOfEntries not consisten for Bin " << i << " values - "<<  fFilterEfficiencyHistogram.get()->GetBinContent(0) << " - " << fFilterNormalizationHistogram.get()->GetBinContent(0) << std::endl;
                fFilterEfficiencyHistogram.get()->SetBinContent(i,0.);
                fFilterNormalizationHistogram.get()->SetBinContent(i,0.);
            }
        }
        fEfficiency->Divide(fFilterEfficiencyHistogram.get(),fFilterNormalizationHistogram.get(),"cl=0.683 b(1,1) mode");
        fFilterNormalizationHistogram->Scale(renormalizationValue);
        for(int bin=0; bin<= fFilterNormalizationHistogram->GetNbinsX(); ++bin)
        {
            float binWidth =  fFilterNormalizationHistogram->GetBinWidth(bin);
            fFilterNormalizationHistogram->SetBinContent(bin, fFilterNormalizationHistogram->GetBinContent(bin)/binWidth);
            fFilterNormalizationHistogram->SetBinError  (bin, fFilterNormalizationHistogram->GetBinError  (bin)/binWidth);
        }
        return {fEfficiency, fFilterNormalizationHistogram};
    }

    TTreeReaderValue<float> fVariableHandler;
    std::shared_ptr<TH1F> fFilterEfficiencyHistogram;
    std::shared_ptr<TH1F> fFilterNormalizationHistogram;
    std::shared_ptr<TGraphAsymmErrors> fEfficiency;
    TTreeFormula fFilterEfficiencyCut;
    TTreeFormula fNormalizationEfficiencyCut;

    // stringhe con cut!!!
};

struct DatasetEfficiencyEvaluator
{
  DatasetEfficiencyEvaluator(std::string inputFileName, std::string datasetName, float expectedNumberOfEvents)
    : fInputFileName(inputFileName)
    , fDatasetName(datasetName)
    , fRenormalizationValue(1.)
  {
    fInputFile = TFile::Open(inputFileName.data());
    if(fInputFile == nullptr)
      {
	std::cout << "File " << inputFileName << " does not exist. Aborting..." << std::endl;
      }
    fInputTree = (TTree*)fInputFile->Get("TrgTree");
    fTheTreeReader  = new TTreeReader(fInputTree);
    fWeightHandler  = new TTreeReaderValue<float>(*fTheTreeReader, "weight" );
    fBtag_SFHandler = new TTreeReaderValue<float>(*fTheTreeReader, "btag_SF");
    
    if(expectedNumberOfEvents>0) fRenormalizationValue = expectedNumberOfEvents/static_cast<TH1F*>(fInputFile->Get("eff_histo"))->GetBinContent(2);
  }
  
  ~DatasetEfficiencyEvaluator()
  {
    for(auto& efficiencyTool : fTriggerEfficiencyToolVector) delete efficiencyTool;
    fTriggerEfficiencyToolVector.clear();
    delete fWeightHandler;
    delete fBtag_SFHandler;
    delete fTheTreeReader;
    fInputFile->Close();
    delete fInputFile;
  }
  
  void addTrigger(std::string triggerName, std::string filterCut, std::string variable, std::string normalizationCut, std::string plotTitle, std::vector<float> binVector, Color_t theColor)
  {
    fTriggerEfficiencyToolVector.emplace_back(new TriggerEfficiencyTool(fDatasetName, fInputTree, fTheTreeReader, triggerName, filterCut, variable, normalizationCut, plotTitle, binVector, theColor));
  }
  
  void addTrigger(std::string triggerName, std::string filterCut, std::string variable, std::string normalizationCut, std::string plotTitle, uint nBins, float xMin, float xMax, Color_t theColor)
  {
    std::vector<float> binVector(nBins+1);
    for(uint bin=0; bin<=nBins; ++bin) binVector[bin] = xMin + (xMax-xMin)*(float(bin)/float(nBins));
    addTrigger(triggerName, filterCut, variable, normalizationCut, plotTitle, binVector, theColor);
  }
  
  void fillTriggerEfficiency()
  {
    for(int it=0; it<fInputTree->GetEntries(); ++it)
      {
	fInputTree->GetEntry(it);
	fTheTreeReader->Next();
	float weightValue   = *fWeightHandler ->Get();
	float btag_SFValue  = *fBtag_SFHandler->Get();
	
	for(auto& triggerEfficiency : fTriggerEfficiencyToolVector ) triggerEfficiency->fillEfficiency(weightValue, btag_SFValue);
        
      }
  }
  
  std::vector<std::tuple<std::shared_ptr<TGraphAsymmErrors>,std::shared_ptr<TH1F> > > getEfficiencyAndDistribution()
  {
    std::vector<std::tuple<std::shared_ptr<TGraphAsymmErrors>,std::shared_ptr<TH1F> > > result;
    for(auto& triggerEfficiency : fTriggerEfficiencyToolVector ) result.emplace_back(triggerEfficiency->getEfficiencyAndDistribution(fRenormalizationValue));
    return result;
  }
  
  std::vector<TriggerEfficiencyTool*> fTriggerEfficiencyToolVector;
  std::string fInputFileName;
  std::string fDatasetName;
  float fRenormalizationValue;
  TFile *fInputFile;
  TTree *fInputTree;
  TTreeReader *fTheTreeReader;
  TTreeReaderValue<float> *fWeightHandler;
  TTreeReaderValue<float> *fBtag_SFHandler;
};



//--------------------------- Trigger efficiency 2018 ------------------------------------------
void ProduceAllTriggerEfficiencyInAFile2018(std::vector<std::tuple<std::shared_ptr<TGraphAsymmErrors>, 
					    std::shared_ptr<TH1F> > >& theOutputResultVector, 
					    std::string inputFileName,
					    std::string datasetName,
					    float expectedNumberOfEvents, Color_t theColor, bool useTTbarCut)
{
  DatasetEfficiencyEvaluator theEfficiencyEvaluator(inputFileName, datasetName, expectedNumberOfEvents);
  
  std::cout << "datasetName = "<<datasetName<<std::endl;
  
  std::string preselectionCut  = "1";
  std::string preselectionBTag = "";
  if(useTTbarCut && datasetName != "NMSSM" ) preselectionCut   = "highestIsoElecton_pt>10. && electronTimesMuoncharge<0.";
  std::vector<float> customBinning;
  bool isSingleMuon = (datasetName == "SingleMuon");
  
  std::string triggerName = "";
  
  std::string normalizationCut = preselectionCut;
  std::string filterCut = normalizationCut + "&& QuadCentralJet30>=1";
  theEfficiencyEvaluator.addTrigger(triggerName, filterCut, "caloJetSum", normalizationCut, "L1filterHT; #sum p_{T} [GeV]; online efficiency"                 ,60, 100, 1500, theColor);
  
  normalizationCut = filterCut;
  filterCut = normalizationCut + "&& QuadCentralJet30>=4";
  customBinning.clear();
  customBinCreator(customBinning, 20., 100., 5.,  180., 20.,  220., 40.,  300., 40.);
  theEfficiencyEvaluator.addTrigger(triggerName, filterCut, "jetForthHighestPt_pt"          , normalizationCut, "QuadCentralJet30; p_{T}^{4} [GeV]; online efficiency"           , customBinning, theColor);
  
  normalizationCut = filterCut;
  filterCut = normalizationCut + "&& CaloQuadJet30HT320_MaxHT>=320 && numberOfJetsCaloHT>=4";
  theEfficiencyEvaluator.addTrigger(triggerName, filterCut, "caloJetSum"                  , normalizationCut, "CaloQuadJet30HT320; #sum p_{T} with p_{T}>30 GeV [GeV]; online efficiency"         ,50, 200., 1200., theColor);
  
  normalizationCut = filterCut;
  filterCut = normalizationCut + "&& BTagCaloDeepCSVp17Double_jetFirstHighestDeepFlavB_triggerFlag>=1";
  customBinning.clear();
  customBinCreator(customBinning, 0., 0.5, 0.1, 0.9, 0.08,  1., 0.02);
  theEfficiencyEvaluator.addTrigger(triggerName, filterCut, "jetFirstHighestDeepFlavB_deepFlavB", normalizationCut, "BTagCaloDeepCSVp17Double; DeepFlavB^{1}; online efficliency"      , customBinning  , theColor);
  
  normalizationCut = normalizationCut + "&& BTagCaloDeepCSVp17Double>=2";
  filterCut = normalizationCut + "&& PFCentralJetLooseIDQuad30>=4";
  customBinning.clear();
  customBinCreator(customBinning, 20., 100., 5., 150., 10.,  250., 20.);
  theEfficiencyEvaluator.addTrigger(triggerName, filterCut, "jetForthHighestPt_pt"         , normalizationCut, "PFCentralJetLooseIDQuad30; p_{T}^{4} [GeV]; online efficiency"         ,customBinning, theColor);
  
  normalizationCut = normalizationCut;
  filterCut = normalizationCut + "&& 1PFCentralJetLooseID75>=1";
  theEfficiencyEvaluator.addTrigger(triggerName, filterCut, "jetFirstHighestPt_pt"         , normalizationCut, "1PFCentralJetLooseID75; p_{T}^{1} [GeV]; online efficiency"         ,50, 20 , 500, theColor);
  
  normalizationCut = filterCut;
  filterCut = normalizationCut + "&& 2PFCentralJetLooseID60>=2";
  theEfficiencyEvaluator.addTrigger(triggerName, filterCut, "jetSecondHighestPt_pt"         , normalizationCut, "2PFCentralJetLooseID60; p_{T}^{2} [GeV]; online efficiency"         ,50, 20 , 300, theColor);
  
  normalizationCut = filterCut;
  filterCut = normalizationCut + "&& 3PFCentralJetLooseID45>=3";
  theEfficiencyEvaluator.addTrigger(triggerName, filterCut, "jetThirdHighestPt_pt"         , normalizationCut, "3PFCentralJetLooseID45; p_{T}^{3} [GeV]; online efficiency"         ,50, 20 , 300, theColor);
  
  normalizationCut = filterCut;
  filterCut = normalizationCut + "&& 4PFCentralJetLooseID40>=4";
  theEfficiencyEvaluator.addTrigger(triggerName, filterCut, "jetForthHighestPt_pt"         , normalizationCut, "4PFCentralJetLooseID40; p_{T}^{4} [GeV]; online efficiency"         ,40, 20 , 200, theColor);
  
  normalizationCut = filterCut;
  filterCut = normalizationCut + "&& PFCentralJetsLooseIDQuad30HT330_MaxHT>=330 && numberOfJetsPfHT>=4";
  customBinning.clear();
  customBinCreator(customBinning, 200., 300., 100., 1500., 30.);
  theEfficiencyEvaluator.addTrigger(triggerName, filterCut, "pfJetSum"                  , normalizationCut, "PFCentralJetsLooseIDQuad30HT330; #sum p_{T} with p_{T}>30 GeV [GeV]; online efficiency"         ,customBinning, theColor);
  
  normalizationCut = filterCut;
  filterCut = normalizationCut + "&& BTagPFDeepCSV4p5Triple_jetFirstHighestDeepFlavB_triggerFlag>=1";
  customBinning.clear();
  if(isSingleMuon) customBinCreator(customBinning, 0., 0.8, 0.05, 1., 0.04);
  else             customBinCreator(customBinning, 0., 0.5, 0.1, 0.9, 0.08,  1., 0.02);
  theEfficiencyEvaluator.addTrigger(triggerName, filterCut, "jetFirstHighestDeepFlavB_deepFlavB", normalizationCut, "BTagPFDeepCSV4p5Triple; DeepFlavB^{1}; online efficliency"      , customBinning , theColor);
  
  theEfficiencyEvaluator.fillTriggerEfficiency();
  
  theOutputResultVector = theEfficiencyEvaluator.getEfficiencyAndDistribution();
}

void ProduceAllTriggerEfficienciesFiles2018(std::string singleMuonInputFileName, std::string ttbarInputFileName, std::string xyhInputSignal, std::string outputFileName, bool useTTbarCut)
{
  float luminosity = 59700.; //pb-1
  
  float ttbarCrossSection =   88.29; //pb
  float wjetCrossSection  = 61526.7; //pb
  float xyhCrossSection   =      1.; //pb
  
  float ttbarExpectedEvents = luminosity*ttbarCrossSection;
  float wjetExpectedEvents  = luminosity*wjetCrossSection ;
  float xyhExpectedEvents   = luminosity*xyhCrossSection  ;
  
  
  gROOT->SetBatch();
  std::vector<std::string> inputFilesNames = {singleMuonInputFileName, ttbarInputFileName , xyhInputSignal     };
  std::vector<std::string> datasetName     = {"SingleMuon"           , "TTbar"            , "NMSSM"            };
  std::vector<float>       expectedEvents  = {-1.                    , ttbarExpectedEvents, xyhExpectedEvents  };
  std::vector<Color_t>     theColorVector =  {kBlack                 , kBlue              , kRed               };
  std::vector<std::vector<std::tuple<std::shared_ptr<TGraphAsymmErrors>,std::shared_ptr<TH1F> > > > vectorOfDatasetResults(inputFilesNames.size());
  
  std::vector<std::thread> theThreadList;
  for(uint it =0; it<inputFilesNames.size(); ++it)
    {
      theThreadList.emplace_back(std::thread(ProduceAllTriggerEfficiencyInAFile2018, std::ref(vectorOfDatasetResults[it]), std::ref(inputFilesNames[it]), std::ref(datasetName[it]), std::ref(expectedEvents[it]), std::ref(theColorVector[it]), useTTbarCut));
    }
  
  for(auto& theThread : theThreadList) theThread.join();
  
  TFile outputFile(outputFileName.data(),"RECREATE");
  
  for(auto& datasetVectorResult : vectorOfDatasetResults)
    {
      for(auto& efficiencyAndDistribution : datasetVectorResult)
        {
	  std::get<0>(efficiencyAndDistribution).get()->Write();
	  std::get<1>(efficiencyAndDistribution).get()->Write();
        }
    }
  
  outputFile.Close();
  gROOT->SetBatch(false);
}

void ProduceAllTriggerEfficiencies2018()
{
  ROOT::EnableThreadSafety();
  
  std::string DataFile   = "root://cmseos.fnal.gov//store/user/mkolosov/HHHTo6B/TriggerStudies/Summer2018UL_TRGcurves_wTrgMatching_08Nov2022/SingleMuon/ntuple.root";
  std::string TTFile     = "root://cmseos.fnal.gov//store/user/mkolosov/HHHTo6B/TriggerStudies/Summer2018UL_TRGcurves_wTrgMatching_08Nov2022/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/ntuple.root";
  std::string SignalFile = "root://cmseos.fnal.gov//store/user/mkolosov/HHHTo6B/TriggerStudies/Summer2018UL_TRGcurves_wTrgMatching_08Nov2022/srosenzw_NMSSM_XYH_YToHH_6b_MX_700_MY_400_sl7_nano_2M/ntuple.root";
  

  std::cout << "\n Will procude trigger efficiencies for 2018"<<std::endl;

  std::thread theMatchedTriggerThread(ProduceAllTriggerEfficienciesFiles2018, DataFile, TTFile, SignalFile, "TriggerEfficiencies_2018.root", true);
  theMatchedTriggerThread.join();
}

void TriggerEfficiencyByFilter()
{
  ProduceAllTriggerEfficiencies2018();
}

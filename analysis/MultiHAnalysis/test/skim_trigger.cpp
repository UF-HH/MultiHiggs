/*
** class  : skim_for_das.cpp
** author : L. Cadamuro (UF)
** date   : 12/11/2019
** brief  : transforms a NanoAOD into a bbbb ntuple for the subsequent plots/analysis
*/
#include <iostream>
#include <string>
#include <iomanip>
#include <any>

#include <boost/program_options.hpp>
namespace po = boost::program_options;

#include "CfgParser.h"
#include "NanoAODTree.h"
#include "EventInfo.h"
#include "JetTools.h"

#include "SkimUtils.h"
namespace su = SkimUtils;

// #include "OutputTree.h"
#include "jsonLumiFilter.h"

#include "TFile.h"
#include "TROOT.h"
#include "TH1F.h"
#include "TH2D.h"

using namespace std;

std::vector<std::string> split_by_delimiter(std::string input, std::string delimiter)
{
  std::vector<std::string> tokens;
  if(input == "")
    return tokens;
  size_t pos = 0;
  while ((pos = input.find(delimiter)) != std::string::npos)
    {
      tokens.push_back(input.substr(0, pos));
      input.erase(0, pos + delimiter.length());
    }
  tokens.push_back(input); // last part splitted
  return tokens;
}

Variation string_to_jer_variation (std::string s)
{
  if (s == "nominal")
    return Variation::NOMINAL;
  if (s == "up")
    return Variation::UP;
  if (s == "down")
    return Variation::DOWN;
  throw std::runtime_error(string("Cannot parse the variation ") + s);
}

bool checkBit(int number, int bitpos)
{
  return (number & (1 << bitpos));
}

float deltaPhi(float phi1, float phi2)
{
  float delphi = TMath::Abs(TMath::Abs(TMath::Abs(phi1 - phi2) - TMath::Pi())-TMath::Pi());
  return delphi;
}

float computePUweight(TH1* histo_pileup, double npu)
{
  int nbin = histo_pileup->FindBin(npu);
  return histo_pileup->GetBinContent(nbin);
}

std::tuple<int,float,float> getClosestJetIndexToTriggerObject(float triggerObjectEta, float triggerObjectPhi, std::vector<Jet>& theJetList, float maxDeltaRaccepted)
{
  int closestJetIndex = -1;
  int currentJetIndex = 0;
  float minDeltaR = 1024;
  float minDeltaRjetPt = -1;
  for(const auto & theJet : theJetList)
    {
      float tmpDeltaR = deltaPhi(theJet.P4().Phi(),triggerObjectPhi)*deltaPhi(theJet.P4().Phi(),triggerObjectPhi) + (theJet.P4().Eta()-triggerObjectEta)*(theJet.P4().Eta()-triggerObjectEta);
      if( tmpDeltaR<minDeltaR)
	{
	  minDeltaR = tmpDeltaR;
	  closestJetIndex = currentJetIndex;
	  minDeltaRjetPt = theJet.P4().Pt();
	}
      currentJetIndex++;
    }
  if(minDeltaR > (maxDeltaRaccepted*maxDeltaRaccepted))
    {
      closestJetIndex = -1;
    }
  return {closestJetIndex, minDeltaR, minDeltaRjetPt};
}

std::vector<std::vector<float> > getJetVetoMap(std::string filename, std::string histoname)
{
  TFile* f  = TFile::Open(filename.c_str());
  if (!f->IsOpen())
    {
      std::cout << "Veto map file not open!"<<std::endl;
    }
  TH2D* h2D = (TH2D*) f->Get(histoname.c_str());
  std::vector<std::vector<float> > map(4);
  for (int i=1; i < h2D->GetNbinsX()+1; ++i)
    {
      for (int j=1; j < h2D->GetNbinsY()+1; ++j)
	{
	  if (h2D->GetBinContent(i, j) > 0.0)
	    {
	      map[0].push_back(h2D->GetXaxis()->GetBinLowEdge(i)); 
	      map[1].push_back(h2D->GetXaxis()->GetBinLowEdge(i) + h2D->GetXaxis()->GetBinWidth(i));
	      map[2].push_back(h2D->GetYaxis()->GetBinLowEdge(j));
	      map[3].push_back(h2D->GetYaxis()->GetBinLowEdge(j) + h2D->GetYaxis()->GetBinWidth(j));
	    }
	}
    }
  f->Close();
  return map;
}

//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
// MAIN
//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
int main(int argc, char** argv)
{
  std::cout << "\n\033[1;33m skim_trigger: \033[0m"<<std::endl;
  
  // Declare command line options
  po::options_description desc("Skim options");
  desc.add_options()
    ("help", "produce help message")
    // required
    ("cfg"   , po::value<string>()->required(), "skim config")
    ("input" , po::value<string>()->required(), "input file list")
    ("output", po::value<string>()->required(), "output file LFN")
    // optional
    ("maxEvts"  , po::value<int>()->default_value(-1), "max number of events to process")
    ("puWeight" , po::value<string>()->default_value(""), "PU weight file name")
    ("seed"      , po::value<int>()->default_value(12345), "seed to be used in systematic uncertainties such as JEC, JER, etc")
    ("jes-shift-syst",  po::value<string>()->default_value("nominal"), "Name of the JES (scale) source uncertainty to be shifted. Usage as <name>:<up/down>. Pass -nominal- to not shift the jets")
    ("jer-shift-syst",  po::value<string>()->default_value("nominal"), "Name of the JER (resolution) source uncertainty to be shifted. Usage as <up/down>. Pass -nominal- to not shift the jets")
    ("bjer-shift-syst",po::value<string>()->default_value("nominal"),"Name of the b regressed JER (resolution) source uncertainty to be shifted. Usage as <up/down>. Pass -nominal- to not shift the jets")
    // flags
    ("is-data",    po::value<bool>()->zero_tokens()->implicit_value(true)->default_value(false), "mark as a data sample (default is false)")
    ("match",      po::value<bool>()->zero_tokens()->implicit_value(true)->default_value(false), "match with four highest b-Jets")
    ("is-signal",  po::value<bool>()->zero_tokens()->implicit_value(true)->default_value(false), "is signal (skip searching for iso muon")
    ("skip-trigger"  , po::value<bool>()->zero_tokens()->implicit_value(true)->default_value(false), "Skip trigger check")
    ;
  
  po::variables_map opts;
  try {
    po::store(parse_command_line(argc, argv, desc, po::command_line_style::unix_style ^ po::command_line_style::allow_short), opts);
    if (opts.count("help")) {
      cout << desc << "\n";
      return 1;
    }
    po::notify(opts);
  }    
  catch (po::error& e) {
    cerr << "** [ERROR] " << e.what() << endl;
    return 1;
  }
  
  ////////////////////////////////////////////////////////////////////////
  // Read config and other cmd line options for skims
  ////////////////////////////////////////////////////////////////////////
  CfgParser config;
  if (!config.init(opts["cfg"].as<string>())) return 1;
  std::cout << "\n\033[1;34m Config          : \033[0m" << opts["cfg"].as<string>() <<std::endl;
  
  const string year  = config.readStringOpt("parameters::year");
  const bool is_data   = opts["is-data"].as<bool>();
  const bool is_signal = opts["is-signal"].as<bool>();
  
  std::cout << "\033[1;34m Year            : \033[0m"<< year <<std::endl;
  std::cout << "\033[1;34m Sample type     : \033[0m";
  if (is_data) std::cout<<"Data"<<std::endl;
  else
    {
      std::cout << "Simulated";
      if (is_signal) std::cout<<" signal"<<std::endl;
      else std::cout<<" background"<<std::endl;
    }
  
  const bool matchWithFourHighestBjets =  opts["match"].as<bool>();
  
  
  ////////////////////////////////////////////////////////////////////////
  // Prepare event loop
  ////////////////////////////////////////////////////////////////////////
  cout << "[INFO] ... opening file list : " << opts["input"].as<string>().c_str() << endl;
  if ( access( opts["input"].as<string>().c_str(), F_OK ) == -1 ){
    cerr << "** [ERROR] The input file list does not exist, aborting" << endl;
    return 1;        
  }
  
  // Joining all the NANOAD input file in a TChain in order to be used like an unique three
  TChain ch("Events");
  int nfiles = su::appendFromFileList(&ch, opts["input"].as<string>());
  if (nfiles == 0){
    cerr << "** [ERROR] The input file list contains no files, aborting" << endl;
    return 1;
  }
  cout << "[INFO] ... file list contains " << nfiles << " files" << endl;
  cout << "[INFO] ... creating tree reader" << endl;
  
  
  // The TChain is passed to the NanoAODTree_SetBranchImpl to parse all the brances
  NanoAODTree nat (&ch);
  
  cout << "[INFO] ... loading the following triggers" << endl;
  for (auto trg : config.readStringListOpt("triggers::makeORof"))
    cout << "   - " << trg << endl;
  nat.triggerReader().setTriggers(config.readStringListOpt("triggers::makeORof"));
  
  bool skipTriggerCheck = opts["skip-trigger"].as<bool>();
  if(!skipTriggerCheck) 
    {
      cout << "[INFO] ... loading the following triggers" << endl;
      for (auto trg : config.readStringListOpt("triggers::makeORof"))
	cout << "   - " << trg << endl;
      nat.triggerReader().setTriggers(config.readStringListOpt("triggers::makeORof"));
    }
  
  jsonLumiFilter jlf;
  if (is_data) jlf.loadJSON(config.readStringOpt("data::lumimask")); // just read the info for data, so if I just skim MC I'm not forced to parse a JSON
  
  //%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  // Jet veto maps
  //%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  std::string jetVetoMapEraE  = config.readStringOpt("parameters::JetVetoMapsEraE");
  std::string jetVetoMapEraCD = config.readStringOpt("parameters::JetVetoMapsEraCD");
  
  std::cout << "\033[1;34m Jet-veto map for Era E : \033[0m" << jetVetoMapEraE << std::endl;
  std::cout << "\033[1;34m Jet-veto map for Era CD: \033[0m" << jetVetoMapEraCD << std::endl;
  std::vector<std::vector<float> > vetoMap_EraE(4);
  std::vector<std::vector<float> > vetoMap_EraCD(4);
  std::vector<std::vector<float> > vetoMapEEP_EraE(4);
  std::vector<std::vector<float> > vetoMapEEP_EraCD(4);
  
  vetoMap_EraE  = getJetVetoMap(jetVetoMapEraE, "jetvetomap");
  vetoMap_EraCD = getJetVetoMap(jetVetoMapEraCD, "jetvetomap");
  vetoMapEEP_EraE  = getJetVetoMap(jetVetoMapEraE, "jetvetomap_eep");
  vetoMapEEP_EraCD = getJetVetoMap(jetVetoMapEraCD, "jetvetomap_eep");
  
  //%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  // PU
  //%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  std::string pufName = config.readStringOpt("parameters::PUweightFile");
  std::cout << "pufName = "<<pufName<<std::endl;
  
  TFile* fPileUp = TFile::Open(pufName.c_str());
  TH1* histo_pileup = (TH1*) fPileUp->Get("PUweights");
  NormWeightTree nwt;
  
  std::string pu_weight_file;
  pu_weight_file = opts["puWeight"].as<string>();
  
  //%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  // Prepare the output
  //%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  
  string outputFileName = opts["output"].as<string>();
  std::cout << "\033[1;34m Output file is  : \033[0m" << outputFileName << "\n"<<std::endl;
  TFile outputFile(outputFileName.c_str(), "recreate");
  
  // TTree with a custom format
  TTree* tOut = new TTree("TrgTree", "TrgTree");
  
  // common
  unsigned int run_;
  unsigned int luminosityBlock_;
  long long    event_;
  
  float btag_SF_;
  float weight_;
  
  // leptons
  float highestIsoElecton_pt_;
  float electronTimesMuoncharge_;
  
  // jets
  float jetFirstHighestPt_pt_;
  float jetSecondHighestPt_pt_;
  float jetThirdHighestPt_pt_;
  float jetForthHighestPt_pt_;
  float fourHighestJetPt_sum_;
  
  float jetFirstHighestDeepFlavB_deepFlavB_;
  float jetFirstHighestDeepFlavB_pt_;
  float jetFirstHighestDeepFlavB_eta_;
  int jetFirstHighestDeepFlavB_hadronFlavour_;
  
  // HT
  float caloJetSum_;
  float pfJetSum_;
  float onlyJetSum_;
  
  int numberOfJetsCaloHT_;
  int numberOfJetsPfHT_;
  int numberOfJetsOnlyHT_;
    
  tOut->Branch("run",              &run_);
  tOut->Branch("luminosityBlock",  &luminosityBlock_);
  tOut->Branch("event",            &event_);
  
  tOut->Branch("btag_SF",           &btag_SF_);
  tOut->Branch("weight",            &weight_);
  
  tOut->Branch("highestIsoElecton_pt"    , &highestIsoElecton_pt_ );
  tOut->Branch("electronTimesMuoncharge" , &electronTimesMuoncharge_ );
  
  tOut->Branch("jetFirstHighestPt_pt" , &jetFirstHighestPt_pt_ );
  tOut->Branch("jetSecondHighestPt_pt", &jetSecondHighestPt_pt_);
  tOut->Branch("jetThirdHighestPt_pt" , &jetThirdHighestPt_pt_ );
  tOut->Branch("jetForthHighestPt_pt" , &jetForthHighestPt_pt_ );
  tOut->Branch("fourHighestJetPt_sum" , &fourHighestJetPt_sum_ );
  
  tOut->Branch("jetFirstHighestDeepFlavB_deepFlavB" , &jetFirstHighestDeepFlavB_deepFlavB_ );
  tOut->Branch("jetFirstHighestDeepFlavB_pt" , &jetFirstHighestDeepFlavB_pt_ );
  tOut->Branch("jetFirstHighestDeepFlavB_eta" , &jetFirstHighestDeepFlavB_eta_ );
  tOut->Branch("jetFirstHighestDeepFlavB_hadronFlavour" , &jetFirstHighestDeepFlavB_hadronFlavour_ );
  
  tOut->Branch("caloJetSum", &caloJetSum_);
  tOut->Branch("pfJetSum",   &pfJetSum_);
  tOut->Branch("onlyJetSum", &onlyJetSum_);
  
  tOut->Branch("numberOfJetsCaloHT"    , &numberOfJetsCaloHT_    );
  tOut->Branch("numberOfJetsPfHT"    , &numberOfJetsPfHT_    );
  tOut->Branch("numberOfJetsOnlyHT"    , &numberOfJetsOnlyHT_    );
  
  bool bPassedL1Seeds_ = false;
  if (year == "2022")
    {
      const string L1SeedEDFilter = config.readStringOpt("l1seeds::EDFilter");
      tOut->Branch(std::string("Passed_" + L1SeedEDFilter).data(), &bPassedL1Seeds_);
    }
  
  // Enable trigger filters
  std::map<std::pair<int,int>, std::string > triggerObjectsForStudies        ; // <<objectId, FilterId> , filterName>
  std::map<std::pair<int,int>, float >       HTFilterHt                      ; // <<objectId, FilterId> , HTthreshold>
  std::map<std::pair<int,int>, int > triggerObjectsForStudiesCount           ; // <<objectId, FilterId> , numberOfObjects>
  std::map<std::pair<int,int>, float > triggerObjectsForStudiesMinDeltaR     ; // <<objectId, FilterId> , minDeltaR>
  std::map<std::pair<int,int>, float > triggerObjectsForStudiesMinDeltaRjetPt; // <<objectId, FilterId> , minDeltaRJetPt>
  std::map<std::pair<int,int>, int > jetFirstHighestDeepFlavB_triggerFlag_   ; // <<objectId, FilterId> , triggerFlag>
  
  std::vector<std::map<std::pair<int,int>, bool  >> triggerObjectPerJetCount  (4); 
  std::vector<std::map<std::pair<int,int>, float >> triggerObjectPerJetDeltaR (4);
  std::vector<std::map<std::pair<int,int>, float >> triggerObjectPerJetDeltaPt(4);
  std::vector<std::tuple<float,float,float>>        selectedJetPtEtaPhiVector (4); // <Pt, Eta Phi> for the four selected jets
  // std::vector< std::map<string,bool> >              filterForMatchedJets      (4);
  
  for(uint i=0; i<4; ++i)
    {
      selectedJetPtEtaPhiVector.at(i) = {-999,-999,-999};
      tOut->Branch(std::string( "Jet" + to_string(i) + "_pt" ).data(), &std::get<0>(selectedJetPtEtaPhiVector[i]));
      tOut->Branch(std::string( "Jet" + to_string(i) + "_eta").data(), &std::get<1>(selectedJetPtEtaPhiVector[i]));
      tOut->Branch(std::string( "Jet" + to_string(i) + "_phi").data(), &std::get<2>(selectedJetPtEtaPhiVector[i]));
    }
  
  const string objectsForCut = config.readStringOpt("parameters::ObjectsForCut");
  if(objectsForCut == "TriggerObjects")
    {
      std::vector<std::string> triggerObjectMatchingVector = config.readStringListOpt("parameters::ListOfTriggerObjectsAndBit");
      
      std::string delimiter = ":";
      size_t pos = 0;
      
      for (auto & triggerObject : triggerObjectMatchingVector)
	{
	  std::cout << "Trigger Object = "<<triggerObject<<std::endl;
	  
	  std::vector<std::string> triggerObjectTokens;
	  while ((pos = triggerObject.find(delimiter)) != std::string::npos)
            {
	      triggerObjectTokens.push_back(triggerObject.substr(0, pos));
	      triggerObject.erase(0, pos + delimiter.length());
            }
	  triggerObjectTokens.push_back(triggerObject); // last part splitted
	  if (triggerObjectTokens.size() != 3)
            {
	      throw std::runtime_error("** skim_ntuple : could not parse triggerObject for Cuts entry " + triggerObject + " , aborting");
            }
	  
	  std::pair<int,int> objectAndFilter = std::make_pair(atoi(triggerObjectTokens[0].data()),atoi(triggerObjectTokens[1].data())); // <objectId, Filter Id>
	  triggerObjectsForStudies[objectAndFilter] = triggerObjectTokens[2]; // filterName
	  triggerObjectsForStudiesCount[objectAndFilter] = 0;
	  triggerObjectsForStudiesMinDeltaR     [objectAndFilter] = -1;
	  triggerObjectsForStudiesMinDeltaRjetPt[objectAndFilter] = -1;
	  tOut->Branch(triggerObjectsForStudies[objectAndFilter].data(), &triggerObjectsForStudiesCount[objectAndFilter]);
	  if(objectAndFilter.first == 3 /*is HT*/) tOut->Branch((triggerObjectsForStudies[objectAndFilter] + "_MaxHT").data(), &HTFilterHt[objectAndFilter]);
	  if(matchWithFourHighestBjets)
            {
	      tOut->Branch(std::string(triggerObjectTokens[2] + "_minDeltaR"      ).data(), &triggerObjectsForStudiesMinDeltaR     [objectAndFilter]);
	      tOut->Branch(std::string(triggerObjectTokens[2] + "_minDeltaR_jetPt").data(), &triggerObjectsForStudiesMinDeltaRjetPt[objectAndFilter]);
	      for(uint i=0; i<4; ++i)
                {
		  // filterForMatchedJets.at(i)[triggerObjectsForStudies[objectAndFilter]] = false;
		  triggerObjectPerJetCount  .at(i)[objectAndFilter] = false; 
		  triggerObjectPerJetDeltaR .at(i)[objectAndFilter] =  999.;
		  triggerObjectPerJetDeltaPt.at(i)[objectAndFilter] = -999.;
		  
		  tOut->Branch(std::string( "Jet" + to_string(i) +  "_" + triggerObjectTokens[2]             ).data(), &triggerObjectPerJetCount  [i][objectAndFilter]);
		  tOut->Branch(std::string( "Jet" + to_string(i) +  "_" + triggerObjectTokens[2] + "_deltaR" ).data(), &triggerObjectPerJetDeltaR [i][objectAndFilter]);
		  tOut->Branch(std::string( "Jet" + to_string(i) +  "_" + triggerObjectTokens[2] + "_deltaPt").data(), &triggerObjectPerJetDeltaPt[i][objectAndFilter]);
                }
            }
        }
      
      std::vector<std::string> btagTriggerObject = config.readStringListOpt("parameters::ListOfBtagTrigger");
      pos = 0;
      for (auto & triggerObject : btagTriggerObject)
        {
	  std::vector<std::string> triggerObjectTokens;
	  while ((pos = triggerObject.find(delimiter)) != std::string::npos)
            {
	      triggerObjectTokens.push_back(triggerObject.substr(0, pos));
	      triggerObject.erase(0, pos + delimiter.length());
            }
	  triggerObjectTokens.push_back(triggerObject); // last part splitted
	  if (triggerObjectTokens.size() != 2)
            {
	      throw std::runtime_error("** skim_ntuple : could not parse triggerObject for Cuts entry " + triggerObject + " , aborting");
            }
	  
	  auto objectAndFilter = std::make_pair(atoi(triggerObjectTokens[0].data()),atoi(triggerObjectTokens[1].data()));
	  jetFirstHighestDeepFlavB_triggerFlag_[objectAndFilter] = 0;
	  tOut->Branch((triggerObjectsForStudies[objectAndFilter] + "_jetFirstHighestDeepFlavB_triggerFlag").data(), &jetFirstHighestDeepFlavB_triggerFlag_[objectAndFilter]);
	}
    }
  
  //%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  // JetTools
  //%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  JetTools jt;
  string jes_shift = opts["jes-shift-syst"].as<string>();
  bool do_jes_shift = (jes_shift != "nominal");
  std::cout << "[INFO] ... shifting jet energy scale? " << std::boolalpha << do_jes_shift << std::noboolalpha << std::endl;
  bool dir_jes_shift_is_up;
  if (do_jes_shift && !is_data)
    {
      string JECFileName = config.readStringOpt("parameters::JECFileName");
      auto tokens = split_by_delimiter(opts["jes-shift-syst"].as<string>(), ":");
      if (tokens.size() != 2)
	throw std::runtime_error(string("Cannot parse the jes shift name : ") + opts["jes-shift-syst"].as<string>());
      string jes_syst_name = tokens.at(0);
      dir_jes_shift_is_up   = (tokens.at(1) == "up"   ? true  :
			       tokens.at(1) == "down" ? false :
			       throw std::runtime_error(string("Could not parse jes direction ") + tokens.at(1)));
      cout << "       ... jec file name           : " << JECFileName << endl;
      cout << "       ... jet energy scale syst   : " << jes_syst_name << endl;
      cout << "       ... jet energy scale is up? : " << std::boolalpha << dir_jes_shift_is_up << std::noboolalpha << endl;
      jt.init_jec_shift(JECFileName, jes_syst_name);
    }
  
  string JERScaleFactorFile = config.readStringOpt("parameters::JERScaleFactorFile");
  string JERResolutionFile  = config.readStringOpt("parameters::JERResolutionFile");
  const int rndm_seed = opts["seed"].as<int>();
  cout << "[INFO] ... initialising JER corrector with the following parameters" << endl;
  cout << "       ... SF file         : " << JERScaleFactorFile << endl;
  cout << "       ... resolution file : " << JERResolutionFile << endl;
  cout << "       ... rndm seed       : " << rndm_seed << endl;
  jt.init_smear(JERScaleFactorFile, JERResolutionFile, rndm_seed);
  
  std::cout << "[INFO] ... jet resolution syst is    : " << opts["jer-shift-syst"].as<string>() << std::endl;
  const Variation jer_var  = string_to_jer_variation(opts["jer-shift-syst"].as<string>());
  const Variation bjer_var = string_to_jer_variation(opts["bjer-shift-syst"].as<string>());
  //%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  







  ////////////////////////////////////////////////////////////////////////
  // Execute event loop
  ////////////////////////////////////////////////////////////////////////
  
  int maxEvts = opts["maxEvts"].as<int>();
  if (maxEvts >= 0)
    cout << "[INFO] ... running on : " << maxEvts << " events" << endl;
  
  for (int iEv = 0; true; ++iEv)
    {
      if (maxEvts >= 0 && iEv >= maxEvts)
	break;
      
      if (!nat.Next()) break;
      if (iEv % 10000 == 0) cout << "... processing event " << iEv << endl;
      
      // aply json filter to data
      if (is_data && !jlf.isValid(*nat.run, *nat.luminosityBlock)){
	continue; // not a valid lumi
      }
      
      EventInfo ei;
      run_             = *(nat.run);
      luminosityBlock_ = *(nat.luminosityBlock);
      event_           = *(nat.event);
      
      float w_PU = 1.0;
      if (year != "2022")
	{
	  if (!is_data)
	    {
	      w_PU = computePUweight(histo_pileup, *(nat.Pileup_nTrueInt));
	    }
	}
      
      float genWeight = (is_data ? 1 : *(nat.genWeight));
      weight_ = w_PU * genWeight;
      // std::cout << w_PU << " " << genWeight << " " << weight_ << std::endl;
      
      //====================================
      // Apply MET Filters
      //====================================
      bool bMETFilters = *nat.Flag_goodVertices && *nat.Flag_globalSuperTightHalo2016Filter && *nat.Flag_HBHENoiseFilter && *nat.Flag_HBHENoiseIsoFilter && *nat.Flag_EcalDeadCellTriggerPrimitiveFilter && *nat.Flag_BadPFMuonFilter && *nat.Flag_eeBadScFilter && (*nat.Flag_ecalBadCalibFilter || (year == "2016"));
      bool applyMETFilters = config.readBoolOpt("configurations::applyMETFilters");
      if (applyMETFilters)
	{
	  if (!bMETFilters) continue;
	}
      
      //====================================
      // Apply trigger
      //====================================
      if(!is_signal) if( !nat.getTrgOr() ) continue;
      
      if (year == "2022")
	{
	  bPassedL1Seeds_ = *nat.L1_QuadJet60er2p5 || *nat.L1_HTT280er || *nat.L1_HTT320er || *nat.L1_HTT360er || *nat.L1_HTT400er || *nat.L1_HTT450er || *nat.L1_HTT280er_QuadJet_70_55_40_35_er2p5 || *nat.L1_HTT320er_QuadJet_70_55_40_40_er2p5 || *nat.L1_HTT320er_QuadJet_80_60_er2p1_45_40_er2p3 || *nat.L1_HTT320er_QuadJet_80_60_er2p1_50_45_er2p3 || *nat.L1_Mu6_HTT240er;
	}

      //====================================
      // Muon Selection
      //====================================
      int numberOfIsoMuon01    = 0;
      int numberOfIsoMuon03    = 0;
      int isoMuonJetId         = -1;
      electronTimesMuoncharge_ = 1;
      float muonPtCut;
      if (year == "2016" or year == "2018" or year == "2022")
	{
	  muonPtCut = 26;
	}
      else if (year == "2017")
	{
	  muonPtCut = 29;
	}
      
      // Loop over muons
      for (uint candIt = 0; candIt < *(nat.nMuon); ++candIt)
        {
	  Muon muon(candIt, &nat);
	  
	  float pt      = muon.P4().Pt();
	  float iso     = get_property(muon, Muon_pfRelIso04_all);
	  bool mediumID = get_property(muon, Muon_mediumId);
	  bool charge   = get_property(muon, Muon_charge);
	  
	  if(iso<0.3 && mediumID && pt >= muonPtCut)
            {
	      if(iso < 0.1) 
                {
		  ++numberOfIsoMuon01;
		  isoMuonJetId = get_property(muon, Muon_jetIdx);
		  electronTimesMuoncharge_ = charge;
                }
	      ++numberOfIsoMuon03;
	      if(numberOfIsoMuon03>1) break;
            }
	} // Closes loop over muons
      
      if(!is_signal) if(numberOfIsoMuon01!=1 || numberOfIsoMuon03>1) continue;
      
      //%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
      // Jets
      //%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
      std::vector<Jet> all_jets;
      for (unsigned int j=0; j<*(nat.nJet); ++j)
	{
	  Jet jet(j, &nat);
	  all_jets.push_back(jet);
	}
      
      std::vector<Jet> nonvetoed_jets;
      if (!is_data)
	{
	  // Apply JEC scale shift to jets
	  if (do_jes_shift)
	    {
	      nonvetoed_jets = jt.jec_shift_jets(nat, all_jets, dir_jes_shift_is_up);
	    }
	  // Apply JER smearing to jets
	  nonvetoed_jets = jt.smear_jets(nat, all_jets, jer_var, bjer_var);
	}
      else
	{
	  // Apply jet veto maps
	  if (year == "2022")
	    {
	      bool vetoEvent = false;
	      unsigned int FirstRun_2022C = 355794;
	      unsigned int LastRun_2022D  = 359021;
	      unsigned int FirstRun_2022E = 359022;
	      for (unsigned int j=0; j<all_jets.size(); ++j)
		{
		  Jet jet = all_jets.at(j);
		  bool vetoJet = false;
		  
		  float pt = jet.P4().Pt();
		  float eta = jet.P4().Eta();
		  float phi = jet.P4().Phi();
		  if (run_ >= FirstRun_2022C && run_ <= LastRun_2022D)
		    {
		      for (int k=0; k<vetoMap_EraCD[0].size(); ++k)
			{
			  if ((eta >= vetoMap_EraCD[0][k]) && (eta <= vetoMap_EraCD[1][k]) && (phi >= vetoMap_EraCD[2][k]) && (phi <= vetoMap_EraCD[3][k])) vetoJet = true;
			}
		      if (pt > 30)
			{
			  for (int k=0; k<vetoMapEEP_EraCD[0].size(); ++k)
			    {
			      if ((eta >= vetoMapEEP_EraCD[0][k]) && (eta <= vetoMapEEP_EraCD[1][k]) && (phi >= vetoMapEEP_EraCD[2][k]) && (phi <= vetoMapEEP_EraCD[3][k])) vetoEvent = true;
			    }
			}
		    } // Run is C-D
		  else if (run_ >= FirstRun_2022E)
		    {
		      for (int k=0; k<vetoMap_EraE[0].size(); ++k)
			{
			  if ((eta >= vetoMap_EraE[0][k]) && (eta <= vetoMap_EraE[1][k]) && (phi >= vetoMap_EraE[2][k]) && (phi <= vetoMap_EraE[3][k])) vetoJet = true;
			}
		      if (pt > 30.0)
			{
			  for (int k=0; k<vetoMapEEP_EraE[0].size(); ++k)
			    {
			      if ((eta >= vetoMapEEP_EraE[0][k]) && (eta <= vetoMapEEP_EraE[1][k]) && (phi >= vetoMapEEP_EraE[2][k]) && (phi <= vetoMapEEP_EraE[3][k])) vetoEvent = true;
			    }
			}
		    } // Run is E
		  
		  if (vetoJet) continue;
		  nonvetoed_jets.push_back(jet);
		}// Loop over jets
	      
	      if (vetoEvent) continue;
	    } // Year is 2022
	} // is-data
      
      // Skip event if there are no jets at all
      if (nonvetoed_jets.size() == 0) continue;
      
      //%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
      // Initialize variables
      //%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
      caloJetSum_         = 0.;
      pfJetSum_           = 0.;
      onlyJetSum_         = 0.;
      
      numberOfJetsCaloHT_ = 0;
      numberOfJetsPfHT_   = 0;
      numberOfJetsOnlyHT_ = 0;
      
      std::vector<Jet> jets;
      for (unsigned int ij=0; ij<nonvetoed_jets.size(); ij++)
	{
	  Jet jet = nonvetoed_jets.at(ij);
	  float jet_pt = jet.P4().Pt();
	  float jet_eta= jet.P4().Eta();
	  
	  // PF HT calculated from all jets (including muons/electrons)
	  if (jet_pt >= 30. && std::abs(jet_eta) < 2.5) 
            {
	      pfJetSum_ += jet_pt;
	      numberOfJetsPfHT_++;
            }
	  
	  // No overlap between jet-muon
	  bool isMuon = false;
	  for (uint candIt = 0; candIt < *(nat.nMuon); ++candIt)
            {
	      Muon muon(candIt, &nat);
	      if (get_property(muon, Muon_pfRelIso04_all) > 0.3) continue;
	      if (jet.getIdx() == get_property(muon, Muon_jetIdx))
                {
		  isMuon = true;
		  break;
                }
	    } 
	  if(isMuon) continue;
	  
	  // Calo jets calculated from all jets except muons
	  if (jet_pt >= 30. && std::abs(jet_eta) < 2.5) 
            {
	      caloJetSum_ += jet_pt;
	      numberOfJetsCaloHT_++;
            }
	  
	  // No overlap between jet-electrons
	  bool isElectron = false;
	  for (uint candIt = 0; candIt < *(nat.nElectron); ++candIt)
            {
	      Electron ele(candIt, &nat);
	      if(get_property(ele, Electron_pfRelIso03_all) > 0.3) continue;
	      if(jet.getIdx() == get_property(ele, Electron_jetIdx))
                {
		  isElectron = true;
		  break;
                }
            }
	  if(isElectron) continue;
	  
	  // PF Jet-only calculated from all jets except muons/electrons
	  if (jet_pt >= 30. && std::abs(jet_eta) < 2.5) 
            {
	      onlyJetSum_ += jet_pt;
	      numberOfJetsOnlyHT_++;
            }
	  
	  // Select jets with pT > 25 GeV, |eta|<2.4, Tight-ID 
	  // Jet ID flags bit1 is loose (always false in 2017 since it does not exist), bit2 is tight, bit3 is tightLepVeto
	  // but note that bit1 means idx 0 and so on
	  int jetid = get_property(jet, Jet_jetId); 
	  if (!checkBit(jetid, 1)) continue;
	  if (jet_pt < 25) continue;
	  if (std::abs(jet_eta) > 2.4) continue;
	  if (jet.get_btag() < 0.0) continue; 
	  // Skip PUID for 2022 (not included in NanoAOD yet)
	  if (year != "2022")
	    {
	      if (!checkBit(get_property( jet,Jet_puId), 1) && jet.P4().Pt() <= 50) // medium PU Id - NOTE : not to be applied beyond 50 GeV: https://twiki.cern.ch/twiki/bin/viewauth/CMS/PileupJetID
		continue;
	    }
	  jets.emplace_back(jet);
        } // Loop over jets
      
      // Skim events to have 4 jets with pT > 25 GeV, |eta|<2.4, Tight-ID, PUID
      if (jets.size() < 4)
	continue;
      
      // Loop over electrons
      highestIsoElecton_pt_ = -999.;
      for (uint candIt = 0; candIt < *(nat.nElectron); ++candIt)
        {
	  Electron ele(candIt, &nat);
	  if (get_property(ele, Electron_pfRelIso03_all) > 0.1) continue;
	  
	  highestIsoElecton_pt_ = ele.P4().Pt();
	  electronTimesMuoncharge_ *= get_property(ele, Electron_charge);
	  break;
        }
      
      // Use the four leading-in-btagging score jets for matching
      if (matchWithFourHighestBjets)
        {
	  stable_sort(jets.begin(), jets.end(), [](const Jet & a, const Jet & b) -> bool
		      {
			return ( a.get_btag() > b.get_btag() );
		      });
	  jets.erase(jets.begin()+4, jets.end());
        }
      
      // Sort them in pT
      stable_sort(jets.begin(), jets.end(), [](const Jet & a, const Jet & b) -> bool
		  {
		    return ( a.P4().Pt() > b.P4().Pt() );
		  });
      
      jetFirstHighestPt_pt_  = jets.at(0).P4().Pt();
      jetSecondHighestPt_pt_ = jets.at(1).P4().Pt();
      jetThirdHighestPt_pt_  = jets.at(2).P4().Pt();
      jetForthHighestPt_pt_  = jets.at(3).P4().Pt();
      fourHighestJetPt_sum_  = jetFirstHighestPt_pt_ + jetSecondHighestPt_pt_ + jetThirdHighestPt_pt_ + jetForthHighestPt_pt_;
      
      // Sort them again in b-tagging score
      stable_sort(jets.begin(), jets.end(), [](const Jet & a, const Jet & b) -> bool
		  {
		    return ( a.get_btag() > b.get_btag() );
		  });
      
      jetFirstHighestDeepFlavB_deepFlavB_ = jets.at(0).get_btag();
      if (!is_data) jetFirstHighestDeepFlavB_hadronFlavour_ = get_property(jets.at(0),Jet_hadronFlavour);
      else jetFirstHighestDeepFlavB_hadronFlavour_ = -999;
      jetFirstHighestDeepFlavB_pt_ = jets.at(0).P4().Pt();
      jetFirstHighestDeepFlavB_eta_ = jets.at(0).P4().Eta();
      int highestDeepFlavBjetID = jets.at(0).getIdx();
      
      // reorder by jet pt
      stable_sort(jets.begin(), jets.end(), [](const Jet & a, const Jet & b) -> bool
		  {
		    return ( a.P4().Pt() > b.P4().Pt() );
		  });
      
      int highestDeepFlavBjetPosition = -1;
      for(uint pos=0; pos<jets.size(); ++pos)
        {
	  if(jets.at(pos).getIdx() == highestDeepFlavBjetID)
            {
	      highestDeepFlavBjetPosition = pos;
            }
        }
      assert(highestDeepFlavBjetPosition != -1);
      
      //=======================================================================================================
      // get number of trigger filters
      //=======================================================================================================
      // reset maps
      for(auto &triggerFilter : triggerObjectsForStudiesCount) triggerFilter.second = 0;
      for(auto &btagFlag : jetFirstHighestDeepFlavB_triggerFlag_) btagFlag.second = 0;
      for(auto &triggerHT : HTFilterHt) triggerHT.second = -1.;
      
      if(matchWithFourHighestBjets)
        {
	  // for(auto& filterMap : filterForMatchedJets) for(auto &filter : filterMap) filter.second = false;
	  for(auto& filterIdAndMaxDeltaR      : triggerObjectsForStudiesMinDeltaR     ) filterIdAndMaxDeltaR     .second = -1;
	  for(auto& filterIdAndMaxDeltaRjetPt : triggerObjectsForStudiesMinDeltaRjetPt) filterIdAndMaxDeltaRjetPt.second = -1;
	  
	  for(auto& jetAndFilterCounts  : triggerObjectPerJetCount  ) for(auto& filterCount   : jetAndFilterCounts ) filterCount  .second = false;
	  for(auto& jetAndFilterDeltaR  : triggerObjectPerJetDeltaR ) for(auto& filterDeltaR  : jetAndFilterDeltaR ) filterDeltaR .second =  999.;
	  for(auto& jetAndFilterDeltaPt : triggerObjectPerJetDeltaPt) for(auto& filterDeltaPt : jetAndFilterDeltaPt) filterDeltaPt.second = -999.;
	  
	  int jetCounter=0;
	  for(const auto & jet : jets)
            {
	      selectedJetPtEtaPhiVector.at(jetCounter) = {jet.P4().Pt(), jet.P4().Eta(), jet.P4().Phi()};
	      jetCounter++;
            }
	}
      
      // Loop over all trigger objects
      for (uint trigObjIt = 0; trigObjIt < *(nat.nTrigObj); ++trigObjIt)
        {
	  int triggerObjectId     = nat.TrigObj_id.At(trigObjIt);
	  int triggerFilterBitSum = nat.TrigObj_filterBits.At(trigObjIt);
	  
	  for(auto &triggerFilter : triggerObjectsForStudiesCount)
            {
	      // Keep only the the ones mentioned in the config file
	      if(triggerObjectId != triggerFilter.first.first) continue;
	      
	      if( (triggerFilterBitSum >> triggerFilter.first.second) & 0x1 ) //check object passes the filter
                {
		  if(matchWithFourHighestBjets)
                    {
		      auto jetIdAndMinDeltaRandPt = getClosestJetIndexToTriggerObject(nat.TrigObj_eta.At(trigObjIt), nat.TrigObj_phi.At(trigObjIt), jets, 0.5);
		      int bestMatchingIndex = std::get<0>( jetIdAndMinDeltaRandPt );
		      if(bestMatchingIndex>=0)
                        {
			  // filterForMatchedJets.at(bestMatchingIndex).at(triggerObjectsForStudies.at(triggerFilter.first)) = true;
			  triggerObjectPerJetCount.at(bestMatchingIndex).at(triggerFilter.first) = true;
			  // float &previousDeltaR = triggerObjectPerJetDeltaR.at(bestMatchingIndex).at(triggerFilter.first);
			  // float &currentDeltaR  = std::get<1>( jetIdAndMinDeltaRandPt );
			  // if(currentDeltaR < previousDeltaR)
			  // {
			  //     previousDeltaR = currentDeltaR;
			  //     triggerObjectPerJetDeltaPt.at(bestMatchingIndex).at(triggerFilter.first) = std::get<2>( jetIdAndMinDeltaRandPt );
			  // }
			  // float& maxDeltaR      = triggerObjectsForStudiesMinDeltaR     .at(triggerFilter.first);
			  // float& maxDeltaRjetPt = triggerObjectsForStudiesMinDeltaRjetPt.at(triggerFilter.first);
			  // if(maxDeltaR < std::get<1>( jetIdAndMinDeltaRandPt ) )
			  // {
			  //     maxDeltaR      = std::get<1>( jetIdAndMinDeltaRandPt );
			  //     maxDeltaRjetPt = std::get<2>( jetIdAndMinDeltaRandPt );
			  // }
                        }
		      
		    } // match with four highest b-tagging jets
		  else
                    {
		      ++triggerFilter.second;
		      if(jetFirstHighestDeepFlavB_triggerFlag_.find(triggerFilter.first) != jetFirstHighestDeepFlavB_triggerFlag_.end()) ++jetFirstHighestDeepFlavB_triggerFlag_[triggerFilter.first];
                    }
		  
		  if(triggerObjectId == 3 /*is HT*/)
                    {
		      HTFilterHt.at(triggerFilter.first) = nat.TrigObj_pt.At(trigObjIt);
                    }
		  
		} // Closes if checking which object passes the filter
            } // Closes loop over all trigger filters to study
        } // Closes loop over all trigger objects
      
      
      if(matchWithFourHighestBjets)
        {
	  for(auto &triggerFilter : triggerObjectsForStudiesCount) // for all the trigger filters
            {
	      for(auto &jetFiltersMap : triggerObjectPerJetCount) //for all the 4 selected jets
                {
		  if(jetFiltersMap.at(triggerFilter.first)) ++triggerFilter.second; //if selected jet was matched with the filter object I increment the count
                }
            }
	  for(auto & btagFilter : jetFirstHighestDeepFlavB_triggerFlag_) // for all the btag filters
            {
	      if(triggerObjectPerJetCount[highestDeepFlavBjetPosition][btagFilter.first]) btagFilter.second = 1; //if jet with highest offline btag passed the filter I increment the count
            }
        }
      
      
      if (!is_data)
	{
	  std::vector<Jet> preselected_jets = {
	    jets.at(0),
	    jets.at(1),
	    jets.at(2),
	    jets.at(3)
	  };
	}
      btag_SF_ = 1.0;
      tOut->Fill();
    }
  
  cout << "[INFO] ... done, saving output file" << endl;
  outputFile.cd();
  tOut->Write();
}

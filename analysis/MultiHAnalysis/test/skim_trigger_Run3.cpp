/*
** class  : skim_trigger_Run3.cpp
** author : Marina Kolosova (UF)
** date   : 04/04/2023
*/
#include <iostream>
#include <string>
#include <iomanip>
#include <any>

#include "Math/VectorUtil.h"
#include "Math/Vector3D.h"
#include "Math/Functions.h"

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

std::tuple<int,float,float> getClosestJetIndexToTriggerObject(float triggerObjectEta, float triggerObjectPhi, std::vector<Jet>& jets, float maxDeltaRaccepted)
{
  int closestJetIndex = -1;
  int currentJetIndex = 0;
  float minDeltaR = 1024;
  float minDeltaRjetPt = -1;
  for(const auto & theJet : jets)
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
  //std::cout << "   (Closest jet index = "<<closestJetIndex << "  minDR="<<minDeltaR<<"   jet pt="<<minDeltaRjetPt<<")"<<std::endl;
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
    ("is-signal",  po::value<bool>()->zero_tokens()->implicit_value(true)->default_value(false), "is signal (skip searching for iso muon")
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
  
  float weight_;
  
  float tagMuon_pt;
  float tagMuon_eta;
  float tagMuon_phi;
  float tagMuon_mass;
  float tagMuon_dxy;
  float tagMuon_dz;
  int tagMuon_charge;
  bool tagMuon_mediumID;
  float tagMuon_iso;
  
  float tagElectron_pt;
  float tagElectron_eta;
  float tagElectron_phi;
  float tagElectron_mass;
  float tagElectron_dxy;
  float tagElectron_dz;
  int tagElectron_charge;
  float tagElectron_iso;
  
  int NMediumPNetJets = 0;
  float MeanPNetScore;
  
  float LdgInBDiscJet_pt;
  float LdgInBDiscJet_eta;
  float LdgInBDiscJet_phi;
  float LdgInBDiscJet_mass;
  float LdgInBDiscJet_bDisc;
  
  float SubldgInBDiscJet_pt;
  float SubldgInBDiscJet_eta;
  float SubldgInBDiscJet_phi;
  float SubldgInBDiscJet_mass;
  float SubldgInBDiscJet_bDisc;
  
  float ThirdldgInBDiscJet_pt;
  float ThirdldgInBDiscJet_eta;
  float ThirdldgInBDiscJet_phi;
  float ThirdldgInBDiscJet_mass;
  float ThirdldgInBDiscJet_bDisc;
  
  float ForthldgInBDiscJet_pt;
  float ForthldgInBDiscJet_eta;
  float ForthldgInBDiscJet_phi;
  float ForthldgInBDiscJet_mass;
  float ForthldgInBDiscJet_bDisc;
  //==================================
  float LdgInPtJet_pt;
  float LdgInPtJet_eta;
  float LdgInPtJet_phi;
  float LdgInPtJet_mass;
  float LdgInPtJet_bDisc;
  
  float SubldgInPtJet_pt;
  float SubldgInPtJet_eta;
  float SubldgInPtJet_phi;
  float SubldgInPtJet_mass;
  float SubldgInPtJet_bDisc;
  
  float ThirdldgInPtJet_pt;
  float ThirdldgInPtJet_eta;
  float ThirdldgInPtJet_phi;
  float ThirdldgInPtJet_mass;
  float ThirdldgInPtJet_bDisc;
  
  float ForthldgInPtJet_pt;
  float ForthldgInPtJet_eta;
  float ForthldgInPtJet_phi;
  float ForthldgInPtJet_mass;
  float ForthldgInPtJet_bDisc;
  
  int NonVetoedJets = 0;
  int NSelectedJets = 0;
  int NSelectedBJets = 0; 
  int NJetsForPFHT = 0;
  float PFHT = 0;
  
  bool b_HLT_IsoMu24;
  bool b_HLT_IsoMu27;
  bool b_HLT_Mu50;
  bool b_HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ;
  bool b_HLT_QuadPFJet70_50_40_30;
  bool b_HLT_QuadPFJet70_50_40_35_PFBTagParticleNet_2BTagSum0p65;
  bool b_HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_QuadPFJet70_50_40_30;
  bool b_HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_QuadPFJet70_50_40_30_PFBTagParticleNet_2BTagSum0p65;
  bool b_HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_PFDiJet30_PFBTagParticleNet_2BTagSum0p65;
  bool b_HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_PFDiJet30;

  tOut->Branch("run",              &run_);
  tOut->Branch("luminosityBlock",  &luminosityBlock_);
  tOut->Branch("event",            &event_);
  
  // tag muon 
  tOut->Branch("tagMuon_pt", &tagMuon_pt);
  tOut->Branch("tagMuon_eta", &tagMuon_eta);
  tOut->Branch("tagMuon_phi", &tagMuon_phi);
  tOut->Branch("tagMuon_mass", &tagMuon_mass);
  tOut->Branch("tagMuon_dxy", &tagMuon_dxy);
  tOut->Branch("tagMuon_dz", &tagMuon_dz);
  tOut->Branch("tagMuon_charge", &tagMuon_charge);
  tOut->Branch("tagMuon_mediumID", &tagMuon_mediumID);
  tOut->Branch("tagMuon_iso", &tagMuon_iso);
  
  // tag electron
  tOut->Branch("tagElectron_pt", &tagElectron_pt);
  tOut->Branch("tagElectron_eta", &tagElectron_eta);
  tOut->Branch("tagElectron_phi", &tagElectron_phi);
  tOut->Branch("tagElectron_mass", &tagElectron_mass);
  tOut->Branch("tagElectron_dxy", &tagElectron_dxy);
  tOut->Branch("tagElectron_dz", &tagElectron_dz);
  tOut->Branch("tagElectron_charge", &tagElectron_charge);
  tOut->Branch("tagElectron_iso", &tagElectron_iso);

  tOut->Branch("NonVetoedJets", &NonVetoedJets);
  tOut->Branch("NSelectedJets", &NSelectedJets);
  tOut->Branch("NSelectedBJets", &NSelectedBJets);
  tOut->Branch("NJetsForPFHT", &NJetsForPFHT);
  tOut->Branch("PFHT",         &PFHT);
    
  tOut->Branch("NMediumPNetJets", &NMediumPNetJets);
  tOut->Branch("MeanPNetScore", &MeanPNetScore);
  tOut->Branch("LdgInBDiscJet_pt", &LdgInBDiscJet_pt);
  tOut->Branch("LdgInBDiscJet_eta", &LdgInBDiscJet_eta);
  tOut->Branch("LdgInBDiscJet_phi", &LdgInBDiscJet_phi);
  tOut->Branch("LdgInBDiscJet_mass", &LdgInBDiscJet_mass);
  tOut->Branch("LdgInBDiscJet_bDisc", &LdgInBDiscJet_bDisc);
  
  tOut->Branch("SubldgInBDiscJet_pt", &SubldgInBDiscJet_pt);
  tOut->Branch("SubldgInBDiscJet_eta", &SubldgInBDiscJet_eta);
  tOut->Branch("SubldgInBDiscJet_phi", &SubldgInBDiscJet_phi);
  tOut->Branch("SubldgInBDiscJet_mass", &SubldgInBDiscJet_mass);
  tOut->Branch("SubldgInBDiscJet_bDisc", &SubldgInBDiscJet_bDisc);
  
  tOut->Branch("ThirdldgInBDiscJet_pt", &ThirdldgInBDiscJet_pt);
  tOut->Branch("ThirdldgInBDiscJet_eta", &ThirdldgInBDiscJet_eta);
  tOut->Branch("ThirdldgInBDiscJet_phi", &ThirdldgInBDiscJet_phi);
  tOut->Branch("ThirdldgInBDiscJet_mass", &ThirdldgInBDiscJet_mass);
  tOut->Branch("ThirdldgInBDiscJet_bDisc", &ThirdldgInBDiscJet_bDisc);
  
  tOut->Branch("ForthldgInBDiscJet_pt", &ForthldgInBDiscJet_pt);
  tOut->Branch("ForthldgInBDiscJet_eta", &ForthldgInBDiscJet_eta);
  tOut->Branch("ForthldgInBDiscJet_phi", &ForthldgInBDiscJet_phi);
  tOut->Branch("ForthldgInBDiscJet_mass", &ForthldgInBDiscJet_mass);
  tOut->Branch("ForthldgInBDiscJet_bDisc", &ForthldgInBDiscJet_bDisc);
  
  tOut->Branch("LdgInPtJet_pt", &LdgInPtJet_pt);
  tOut->Branch("LdgInPtJet_eta", &LdgInPtJet_eta);
  tOut->Branch("LdgInPtJet_phi", &LdgInPtJet_phi);
  tOut->Branch("LdgInPtJet_mass", &LdgInPtJet_mass);
  tOut->Branch("LdgInPtJet_bDisc", &LdgInPtJet_bDisc);
  
  tOut->Branch("SubldgInPtJet_pt", &SubldgInPtJet_pt);
  tOut->Branch("SubldgInPtJet_eta", &SubldgInPtJet_eta);
  tOut->Branch("SubldgInPtJet_phi", &SubldgInPtJet_phi);
  tOut->Branch("SubldgInPtJet_mass", &SubldgInPtJet_mass);
  tOut->Branch("SubldgInPtJet_bDisc", &SubldgInPtJet_bDisc);
  
  tOut->Branch("ThirdldgInPtJet_pt", &ThirdldgInPtJet_pt);
  tOut->Branch("ThirdldgInPtJet_eta", &ThirdldgInPtJet_eta);
  tOut->Branch("ThirdldgInPtJet_phi", &ThirdldgInPtJet_phi);
  tOut->Branch("ThirdldgInPtJet_mass", &ThirdldgInPtJet_mass);
  tOut->Branch("ThirdldgInPtJet_bDisc", &ThirdldgInPtJet_bDisc);
  
  tOut->Branch("ForthldgInPtJet_pt", &ForthldgInPtJet_pt);
  tOut->Branch("ForthldgInPtJet_eta", &ForthldgInPtJet_eta);
  tOut->Branch("ForthldgInPtJet_phi", &ForthldgInPtJet_phi);
  tOut->Branch("ForthldgInPtJet_mass", &ForthldgInPtJet_mass);
  tOut->Branch("ForthldgInPtJet_bDisc", &ForthldgInPtJet_bDisc);
  
  tOut->Branch("HLT_IsoMu24", &b_HLT_IsoMu24);
  tOut->Branch("HLT_IsoMu27", &b_HLT_IsoMu27);
  tOut->Branch("HLT_Mu50",    &b_HLT_Mu50);
  tOut->Branch("HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ", &b_HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ);
  tOut->Branch("HLT_QuadPFJet70_50_40_30", &b_HLT_QuadPFJet70_50_40_30);
  tOut->Branch("HLT_QuadPFJet70_50_40_35_PFBTagParticleNet_2BTagSum0p65", &b_HLT_QuadPFJet70_50_40_35_PFBTagParticleNet_2BTagSum0p65);
  tOut->Branch("HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_QuadPFJet70_50_40_30", &b_HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_QuadPFJet70_50_40_30);
  tOut->Branch("HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_QuadPFJet70_50_40_30_PFBTagParticleNet_2BTagSum0p65", &b_HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_QuadPFJet70_50_40_30_PFBTagParticleNet_2BTagSum0p65);
  tOut->Branch("HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_PFDiJet30_PFBTagParticleNet_2BTagSum0p65", &b_HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_PFDiJet30_PFBTagParticleNet_2BTagSum0p65);
  tOut->Branch("HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_PFDiJet30", &b_HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_PFDiJet30);
  
  bool bPassedL1Seeds_ = false;
  if (year == "2022")
    {
      const string L1SeedEDFilter = config.readStringOpt("l1seeds::EDFilter");
      tOut->Branch(std::string("L1_" + L1SeedEDFilter).data(), &bPassedL1Seeds_);
    }
  
  // Are these needed at this point?
  tOut->Branch("weight",            &weight_);
  
  // Trigger Filters
  std::map<std::pair<int,int>, std::string > triggerObjectsForStudies; // < <objectID, FilterID>, filterName >
  std::map<std::pair<int,int>, int > triggerObjectsForStudiesCount;
  
  std::vector<std::map<std::pair<int,int>, bool> > triggerObjectPerJetCount(4); 
  
  bool matchWithFourHighestBjets = true;
  
  
  const string objectsForCut = config.readStringOpt("parameters::ObjectsForCut");
  
  if (objectsForCut == "TriggerObjects")
    {
      std::vector<std::string> triggerObjectMatchingVector = config.readStringListOpt("parameters::ListOfTriggerObjectsAndBit");
      
      std::string delimiter = ":";
      size_t pos = 0;
      for (auto & triggerObject : triggerObjectMatchingVector)
	{
	  //std::cout << "Trigger object from my list = "<<triggerObject<<std::endl;
	  
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

	  //std::cout << "objectAndFilter [objectID, FilterID] = "<<atoi(triggerObjectTokens[0].data())<<", "<< atoi(triggerObjectTokens[1].data())<<",  Filter name ="<<triggerObjectTokens[2]<<std::endl;
	  //std::cout << "\n"<<std::endl;
	  
	  std::pair<int,int> objectAndFilter = std::make_pair(atoi(triggerObjectTokens[0].data()),atoi(triggerObjectTokens[1].data())); // <objectId, Filter Id>
	  triggerObjectsForStudies[objectAndFilter] = triggerObjectTokens[2]; // filterName
	  triggerObjectsForStudiesCount[objectAndFilter] = 0;
	  
	  // Save Filter Name
	  tOut->Branch(triggerObjectsForStudies[objectAndFilter].data(), &triggerObjectsForStudiesCount[objectAndFilter]);

	  if (matchWithFourHighestBjets)
	    {
	      for(uint i=0; i<4; ++i)
		{
		  triggerObjectPerJetCount.at(i)[objectAndFilter] = false; 
		  
		  tOut->Branch(std::string( "Jet" + to_string(i) +  "_" + triggerObjectTokens[2]).data(), &triggerObjectPerJetCount  [i][objectAndFilter]);
		}
	      
	    }
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
  
  //%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  // Loop over all events
  //%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
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
      
      // Keep only runs after 356426 where control paths were introduced
      if (is_data)
	{
	  if (run_ < 356426){
	    std::cout << "Run = "<<run_<<std::endl;
	    continue;
	  }
	}
      
      //%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
      // Get trigger bits
      //%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
      if (year == "2022")
	{
	  b_HLT_Mu50 = nat.getTrgResult("HLT_Mu50");
	  b_HLT_IsoMu24 = nat.getTrgResult("HLT_IsoMu24");
	  b_HLT_IsoMu27 = nat.getTrgResult("HLT_IsoMu27");
	  b_HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ = nat.getTrgResult("HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ");
	  b_HLT_QuadPFJet70_50_40_30 = nat.getTrgResult("HLT_QuadPFJet70_50_40_30");
	  b_HLT_QuadPFJet70_50_40_35_PFBTagParticleNet_2BTagSum0p65 = nat.getTrgResult("HLT_QuadPFJet70_50_40_35_PFBTagParticleNet_2BTagSum0p65");
	  b_HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_QuadPFJet70_50_40_30 = nat.getTrgResult("HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_QuadPFJet70_50_40_30");
	  b_HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_QuadPFJet70_50_40_30_PFBTagParticleNet_2BTagSum0p65 = nat.getTrgResult("HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_QuadPFJet70_50_40_30_PFBTagParticleNet_2BTagSum0p65");
	  b_HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_PFDiJet30_PFBTagParticleNet_2BTagSum0p65 = nat.getTrgResult("HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_PFDiJet30_PFBTagParticleNet_2BTagSum0p65");
	  b_HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_PFDiJet30 = nat.getTrgResult("HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_PFDiJet30");
	  
	  bPassedL1Seeds_ = *nat.L1_QuadJet60er2p5 || *nat.L1_HTT280er || *nat.L1_HTT320er || *nat.L1_HTT360er || *nat.L1_HTT400er || *nat.L1_HTT450er || *nat.L1_HTT280er_QuadJet_70_55_40_35_er2p5 || *nat.L1_HTT320er_QuadJet_70_55_40_40_er2p5 || *nat.L1_HTT320er_QuadJet_80_60_er2p1_45_40_er2p3 || *nat.L1_HTT320er_QuadJet_80_60_er2p1_50_45_er2p3 || *nat.L1_Mu6_HTT240er;
	}
      //%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

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
      
      //====================================
      // Apply trigger
      //====================================
      bool bDenHLT = b_HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ;
      if (!is_signal) if (!bDenHLT) continue;
      if (1) std::cout << "\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"<<std::endl;
      if (1) std::cout << " Event number ="<<iEv<<std::endl;
      if (1) std::cout << " Trigger HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ passed"<<std::endl;
      
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
      // Apply muon selection
      //====================================
      std::vector<Muon> tagMuons;
      std::vector<Muon> additionalMuons;

      for (uint candIt = 0; candIt < *(nat.nMuon); ++candIt)
	{
	  Muon mu(candIt, &nat);
	  
	  float pt      = mu.P4().Pt();
          float eta     = mu.P4().Eta();

	  bool looseID        = get_property(mu, Muon_looseId);
	  bool mediumID       = get_property(mu, Muon_mediumId);
	  //bool mediumPromptID = get_property(mu, Muon_mediumPromptId);
	  
	  int charge    = get_property(mu, Muon_charge);
	  float dz      = get_property(mu, Muon_dz);
	  float dxy     = get_property(mu, Muon_dxy);
	  float iso     = get_property(mu, Muon_pfRelIso04_all);
	  
	  std::cout << " Muon "<<candIt<<"   pt="<<pt<<"   eta="<<eta<<"   mediumID="<<mediumID<<"   dz="<<dz<<"  dxy="<<dxy<<"  charge="<<charge<<"  iso="<<iso<<std::endl;
	  
	  if (abs(eta) > 2.4) continue;
	  if (pt < 10) continue;
	  if (std::abs(dz) > 0.5) continue;
	  if (std::abs(dxy) > 0.2) continue;
	  
	  // Tag muon
	  if (mediumID && iso < 0.20)
	    {
	      if (0) std::cout << "Tag muon pt="<<pt<<" eta="<<eta<<"  mediumID="<<mediumID<<"   dz="<<dz<<"  dxy="<<dxy<<"  charge="<<charge<<"  iso="<<iso<<std::endl;
	      tagMuons.push_back(mu);
	    }
	  else
	    {
	      // Additional muons
	      if (pt > 10 && looseID && iso < 0.25)
		{
		  if (0) std::cout << "Additional muons pt="<<pt<<" eta="<<eta<<"  mediumID="<<mediumID<<"   dz="<<dz<<"  dxy="<<dxy<<"  charge="<<charge<<"  iso="<<iso<<std::endl;
		  additionalMuons.push_back(mu);
		}
	    }
	} // Loop over muons
      
      //std::cout << "Number of tag muons        : "<<tagMuons.size()<<std::endl;
      //std::cout << "Number of additional muons : "<<additionalMuons.size()<<std::endl;
      
      // Reject event if no muon is found
      if(!is_signal) if (tagMuons.size() != 1) continue;
      // Reject event if additional muons are found
      if(!is_signal) if (additionalMuons.size() != 0) continue;
      
      //std::cout << "Passed muon selection"<<std::endl;
      
      std::vector<Electron> tagElectrons;
      std::vector<Electron> additionalElectrons;
      
      //std::cout << "==== Loop over electrons"<<std::endl;
      for (uint candIt = 0; candIt < *(nat.nElectron); ++candIt)
	{
	  Electron ele(candIt, &nat);
	  
	  float pt  = ele.P4().Pt();
	  float eta = ele.P4().Eta();
	  
	  float dxy = get_property(ele, Electron_dxy);
	  float dz  = get_property(ele, Electron_dz);
	  
	  float iso     = get_property(ele, Electron_pfRelIso03_all);
	  bool tightID  = get_property(ele, Electron_mvaIso_WP80);
	  bool mediumID = get_property(ele, Electron_mvaIso_WP90);
	  
	  int charge   = get_property(ele, Electron_charge);
	  
	  if (std::abs(eta) > 2.5) continue;
	  if (pt < 15) continue;
	  
	  std::cout << "Electron "<<candIt<<"   pt="<<pt<<"   eta="<<eta<<"   dxy="<<dxy<<"   dz="<<dz<<"    tightID="<<tightID<<"    mediumID="<<mediumID<<"   charge="<<charge<<std::endl;
	  
	  if (pt > 25 && tightID)
	    {
	      if (0) std::cout << "Tag electron pt="<<pt<<"  eta="<<eta<<"  iso="<<iso<<"  tightID="<<tightID<<"  charge="<<charge<<std::endl;
	      tagElectrons.push_back(ele);
	    }
	  else
	    {
	      if (pt > 15 && mediumID)
		{
		  if (0) std::cout << "Additional electron pt="<<pt<<"  eta="<<eta<<" iso="<<iso<<"   mediumID="<<mediumID<<"  charge="<<charge<<std::endl;
		  additionalElectrons.push_back(ele);
		}
	    }
	}
            
      // Skip event if tag-electron is available
      if(!is_signal) if (tagElectrons.size() != 1) continue;
      
      // Reject event addtional loose electrons are present
      if(!is_signal) if (additionalElectrons.size() !=0) continue;
      
      
      // Require the charge of e and mu to be OS (=enchance the fraction of ttbar events)
      if (!is_signal)
	{
	  int charge_ele_mu = get_property(tagElectrons.at(0), Electron_charge) * get_property(tagMuons.at(0), Muon_charge);
	  if (0) std::cout << "Electron * muon charge : "<<charge_ele_mu<<std::endl;
	  if (charge_ele_mu != -1) continue;
	}
      
      if (!is_signal)
	{
	  float InvMass_ele_mu = (tagElectrons.at(0).P4() + tagMuons.at(0).P4()).M();
	  if (0) std::cout << "Invariant mass(ele, mu) = "<<InvMass_ele_mu<<std::endl;
	  if (InvMass_ele_mu < 20) continue;
	}
      
      if (1)
	{
	  // Leptonic selection
	  for (unsigned int mu=0; mu<tagMuons.size(); mu++)
	    {
	      std::cout << "Tag muon     :   pt="<<tagMuons.at(mu).P4().Pt()<<"  eta="<<tagMuons.at(mu).P4().Eta()<<"    phi="<<tagMuons.at(mu).P4().Phi()<<std::endl;
	    }
	  for (unsigned int ele=0; ele<tagElectrons.size(); ele++)
	    {
	      std::cout << "Tag electron :   pt="<<tagElectrons.at(ele).P4().Pt()<<"   eta="<<tagElectrons.at(ele).P4().Eta()<<"   phi="<<tagElectrons.at(ele).P4().Phi()<<std::endl;
	    }
	}
      
      if (1) std::cout << "Number of all jets saved in Nano= "<<*(nat.nJet)<<std::endl;
      
      //%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
      // Jets (Clean overlap with electrons and muons)
      //%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
      std::vector<Jet> all_jets;
      std::vector<Jet> nonvetoed_jets;
      for (unsigned int j=0; j<*(nat.nJet); ++j)
	{
	  Jet jet(j, &nat);
	  all_jets.push_back(jet);
	  if (!is_data) nonvetoed_jets.push_back(jet); // For the moment since missing variable in NanoAOD
	} // Loop over jets
      
      if (!is_data)
	{
	  // Apply JEC scale shift to jets
	  if (do_jes_shift)
	    {
	      nonvetoed_jets = jt.jec_shift_jets(nat, all_jets, dir_jes_shift_is_up);
	    }
	  // Apply JER smearing to jets
	  //nonvetoed_jets = jt.smear_jets(nat, all_jets, jer_var, bjer_var);
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
		      for (unsigned int k=0; k<vetoMap_EraCD[0].size(); ++k)
			{
			  if ((eta >= vetoMap_EraCD[0][k]) && (eta <= vetoMap_EraCD[1][k]) && (phi >= vetoMap_EraCD[2][k]) && (phi <= vetoMap_EraCD[3][k])) vetoJet = true;
			}
		      if (pt > 30)
			{
			  for (unsigned int k=0; k<vetoMapEEP_EraCD[0].size(); ++k)
			    {
			      if ((eta >= vetoMapEEP_EraCD[0][k]) && (eta <= vetoMapEEP_EraCD[1][k]) && (phi >= vetoMapEEP_EraCD[2][k]) && (phi <= vetoMapEEP_EraCD[3][k])) vetoEvent = true;
			    }
			}
		    } // Run is C-D
		  else if (run_ >= FirstRun_2022E)
		    {
		      for (unsigned int k=0; k<vetoMap_EraE[0].size(); ++k)
			{
			  if ((eta >= vetoMap_EraE[0][k]) && (eta <= vetoMap_EraE[1][k]) && (phi >= vetoMap_EraE[2][k]) && (phi <= vetoMap_EraE[3][k])) vetoJet = true;
			}
		      if (pt > 30.0)
			{
			  for (unsigned int k=0; k<vetoMapEEP_EraE[0].size(); ++k)
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
      
      if (1) std::cout << "Number of non-vetoed jets = "<<nonvetoed_jets.size()<<std::endl;

      //%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
      // Cross-clean and select jets
      //%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
      std::vector<Jet> selected_jets;
      for (unsigned int j=0; j<nonvetoed_jets.size(); j++)
	{
	  Jet jet = nonvetoed_jets.at(j);
	  
	  float pt = jet.P4().Pt();
	  float eta= jet.P4().Eta();
	  
	  int jetid = get_property(jet, Jet_jetId);
          float btagPNetBvsAll = get_property(jet, Jet_btagPNetBvsAll);
	  
	  if (!checkBit(jetid, 1)) continue;
	  if (pt < 30) continue;
	  if (std::abs(eta) > 2.5) continue;
	  	  
	  double dR_ele = ROOT::Math::VectorUtil::DeltaR(jet.P4(), tagElectrons.at(0).P4());
	  double dR_mu  = ROOT::Math::VectorUtil::DeltaR(jet.P4(), tagMuons.at(0).P4());
	  
	  if (dR_ele < 0.4) continue;
	  if (dR_mu  < 0.4) continue;
	  
	  if (0) std::cout << "jet = "<<j<<"  pt="<<pt<<"  eta="<<eta<<"   DR(jet, electron)="<<dR_ele<<"   DR(jet, muon)="<<dR_mu<<"   PNet="<<btagPNetBvsAll<<std::endl;
	  
	  selected_jets.push_back(jet);
	} // Loop over jets
      if (1) std::cout << "Number of selected (non-leptonic) jets="<<selected_jets.size()<<std::endl;
      
      //%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
      // Select events with at least 4 jets
      //%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
      if (selected_jets.size()  < 4) continue;
      
      // Apply the trigger cuts
      if (selected_jets.at(0).P4().Pt() < 70.0) continue;
      if (selected_jets.at(1).P4().Pt() < 50.0) continue;
      if (selected_jets.at(2).P4().Pt() < 40.0) continue;
      if (selected_jets.at(3).P4().Pt() < 35.0) continue;
      
      std::vector<Jet> selected_bjets;
      std::vector<Jet> LeadingFour_selected_bjets;
      
      if (0) std::cout << "\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"<<std::endl;
      if (0) std::cout << " Event number ="<<iEv<<std::endl;
      float MediumPNetWP  = 0.387;
      
      NMediumPNetJets = 0;
      for (unsigned int j=0; j<selected_jets.size(); j++)
	{
	  Jet jet = selected_jets.at(j);
	  float btagPNetBvsAll = get_property(jet, Jet_btagPNetBvsAll);
	  if (btagPNetBvsAll > 0.0) selected_bjets.push_back(jet);
	  if (btagPNetBvsAll > MediumPNetWP) NMediumPNetJets++;
	}
      
      // Require at least 2 jets with PNet > 0.0
      if (selected_bjets.size() < 2) continue;
            
      // Sort b-jets by b-tagging score
      stable_sort(selected_bjets.begin(), selected_bjets.end(), [](const Jet & a, const Jet & b) -> bool{return(get_property(a, Jet_btagPNetBvsAll) > get_property(b, Jet_btagPNetBvsAll)); });
      if (0)
	{
	  std::cout << "\n After sorting"<<std::endl;
	  for (unsigned int j=0; j<selected_bjets.size(); j++)
	    {
	      Jet jet = selected_bjets.at(j);
	      float btag = get_property(jet, Jet_btagPNetBvsAll);
	      std::cout << "btag = "<<btag<<std::endl;
	    }
	}
      
      // Get the average of the two leading in b-tagging jets
      float PNetMean = (get_property(selected_bjets.at(0), Jet_btagPNetBvsAll) + get_property(selected_bjets.at(1), Jet_btagPNetBvsAll))/2.0;
      MeanPNetScore = PNetMean;
      
      //std::cout << "PNet average score of the two leading in b-tagging jets = "<<PNetMean<<std::endl;
      // Store the 4 leading-in-b-tagging jets 
      for (unsigned int j=0; j<selected_bjets.size(); j++)
	{
	  Jet jet = selected_bjets.at(j);
	  if (j < 4) LeadingFour_selected_bjets.push_back(jet);
	}
      
      //if (b_HLT_QuadPFJet70_50_40_35_PFBTagParticleNet_2BTagSum0p65) std::cout << "Passed signal trigger"<<std::endl;
      //else std::cout << "Failed signal trigger"<<std::endl;
            
      if (selected_bjets.size() >=1)
	{
	  LdgInBDiscJet_pt = selected_bjets.at(0).P4().Pt();
	  LdgInBDiscJet_eta = selected_bjets.at(0).P4().Eta();
	  LdgInBDiscJet_phi = selected_bjets.at(0).P4().Phi();
	  LdgInBDiscJet_mass = selected_bjets.at(0).P4().M();
	  LdgInBDiscJet_bDisc = get_property(selected_bjets.at(0), Jet_btagPNetBvsAll);
	  
	  if (selected_bjets.size() >= 2)
	    {
	      SubldgInBDiscJet_pt = selected_bjets.at(1).P4().Pt();
	      SubldgInBDiscJet_eta = selected_bjets.at(1).P4().Eta();
	      SubldgInBDiscJet_phi = selected_bjets.at(1).P4().Phi();
	      SubldgInBDiscJet_mass = selected_bjets.at(1).P4().M();
	      SubldgInBDiscJet_bDisc = get_property(selected_bjets.at(1), Jet_btagPNetBvsAll);
	      
	      if (selected_bjets.size() >= 3)
		{
		  ThirdldgInBDiscJet_pt = selected_bjets.at(2).P4().Pt();
		  ThirdldgInBDiscJet_eta = selected_bjets.at(2).P4().Eta();
		  ThirdldgInBDiscJet_phi = selected_bjets.at(2).P4().Phi();
		  ThirdldgInBDiscJet_mass = selected_bjets.at(2).P4().M();
		  ThirdldgInBDiscJet_bDisc = get_property(selected_bjets.at(2), Jet_btagPNetBvsAll);
		  
		  if (selected_bjets.size() >= 4)
		    {
		      ForthldgInBDiscJet_pt  = selected_bjets.at(3).P4().Pt();
		      ForthldgInBDiscJet_eta = selected_bjets.at(3).P4().Eta();
		      ForthldgInBDiscJet_phi = selected_bjets.at(3).P4().Phi();
		      ForthldgInBDiscJet_mass= selected_bjets.at(3).P4().M();
		      ForthldgInBDiscJet_bDisc = get_property(selected_bjets.at(3), Jet_btagPNetBvsAll);
		    }
		}
	    }
	}
      
      // Sort jets in pT and store the leading four
      stable_sort(selected_jets.begin(), selected_jets.end(), [](const Jet & a, const Jet & b) -> bool { return ( a.P4().Pt() > b.P4().Pt() ); });
      if (selected_jets.size() >= 1)
	{
	  LdgInPtJet_pt  = selected_jets.at(0).P4().Pt();
	  LdgInPtJet_eta = selected_jets.at(0).P4().Eta();
	  LdgInPtJet_phi = selected_jets.at(0).P4().Phi();
	  LdgInPtJet_mass = selected_jets.at(0).P4().M();
	  LdgInPtJet_bDisc = get_property(selected_jets.at(0), Jet_btagPNetBvsAll);
	  if (selected_jets.size() >= 2)
	    {
	      SubldgInPtJet_pt = selected_jets.at(1).P4().Pt();
	      SubldgInPtJet_eta = selected_jets.at(1).P4().Eta();
	      SubldgInPtJet_phi = selected_jets.at(1).P4().Phi();
	      SubldgInPtJet_mass = selected_jets.at(1).P4().M();
	      SubldgInPtJet_bDisc = get_property(selected_jets.at(1), Jet_btagPNetBvsAll);
	      if (selected_jets.size() >= 3)
		{
		  ThirdldgInPtJet_pt = selected_jets.at(2).P4().Pt();
		  ThirdldgInPtJet_eta = selected_jets.at(2).P4().Eta();
		  ThirdldgInPtJet_phi = selected_jets.at(2).P4().Phi();
		  ThirdldgInPtJet_mass = selected_jets.at(2).P4().M();
		  ThirdldgInPtJet_bDisc = get_property(selected_jets.at(2), Jet_btagPNetBvsAll);
		  if (selected_jets.size() >= 4)
		    {
		      ForthldgInPtJet_pt = selected_jets.at(3).P4().Pt();
		      ForthldgInPtJet_eta = selected_jets.at(3).P4().Eta();
		      ForthldgInPtJet_phi = selected_jets.at(3).P4().Phi();
		      ForthldgInPtJet_mass = selected_jets.at(3).P4().M();
		      ForthldgInPtJet_bDisc = get_property(selected_jets.at(3), Jet_btagPNetBvsAll);
		    }
		}
	    }
	}
      
      //%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
      // End of selections: fill the treee
      //%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
      tagMuon_pt       = tagMuons.at(0).P4().Pt();
      tagMuon_eta      = tagMuons.at(0).P4().Eta();
      tagMuon_phi      = tagMuons.at(0).P4().Phi();
      tagMuon_mass     = tagMuons.at(0).P4().M();
      tagMuon_dxy      = get_property(tagMuons.at(0), Muon_dxy);
      tagMuon_dz       = get_property(tagMuons.at(0), Muon_dz);
      tagMuon_charge   = get_property(tagMuons.at(0), Muon_charge); 
      tagMuon_mediumID = get_property(tagMuons.at(0), Muon_mediumId);
      tagMuon_iso      = get_property(tagMuons.at(0), Muon_pfRelIso04_all);
      
      tagElectron_pt   = tagElectrons.at(0).P4().Pt();
      tagElectron_eta  = tagElectrons.at(0).P4().Eta();
      tagElectron_phi  = tagElectrons.at(0).P4().Phi();
      tagElectron_mass = tagElectrons.at(0).P4().M();
      tagElectron_dxy  = get_property(tagElectrons.at(0), Electron_dxy);
      tagElectron_dz   = get_property(tagElectrons.at(0), Electron_dz);
      tagElectron_charge = get_property(tagElectrons.at(0), Electron_charge);
      tagElectron_iso  = get_property(tagElectrons.at(0), Electron_pfRelIso03_all);
      
      NonVetoedJets  = nonvetoed_jets.size();
      NSelectedJets  = selected_jets.size();
      NSelectedBJets = selected_bjets.size();
      NJetsForPFHT   = 0;
      PFHT           = 0.0;
      
      // Event PFHT (calculated from all jets including muons/electrons)
      for (unsigned int ij=0; ij<nonvetoed_jets.size(); ij++)
        {
          Jet jet = nonvetoed_jets.at(ij);
          float pt = jet.P4().Pt();
          float eta= jet.P4().Eta();
	  
	  if (pt < 30.0) continue;
	  if (std::abs(eta) > 2.5) continue;
	  
	  NJetsForPFHT++;
	  PFHT+=pt;
	}
      
      // Trigger matching
      for(auto &triggerFilter : triggerObjectsForStudiesCount) triggerFilter.second = 0;
      if (matchWithFourHighestBjets)
	{
	  for(auto& jetAndFilterCounts : triggerObjectPerJetCount) for(auto& filterCount : jetAndFilterCounts) filterCount.second = false;
	}
      
      // Loop over trigger objects in NanoAOD
      for (uint trigObjIt=0; trigObjIt < *(nat.nTrigObj); ++trigObjIt)
	{
	  // Get the trigger object ID (1: Jets)
	  int triggerObjectId = nat.TrigObj_id.At(trigObjIt);
	  
	  // Skip filters related to Electrons (11), Muons (13), Photons (22), Taus (15), Boosted taus (1515), Fatjets (6), MET (2)
	  if (triggerObjectId == 11 || triggerObjectId == 13 || triggerObjectId == 22 || triggerObjectId == 15 || triggerObjectId == 1515 || triggerObjectId == 6 || triggerObjectId == 2) continue;
	  
	  // Keep only triggerObjectId == 1 (Jets)
	  if (!(triggerObjectId == 1)) continue;
	  
	  // Get the filter bits
	  int triggerFilterBitSum = nat.TrigObj_filterBits.At(trigObjIt);
	  
	  //std::cout << "\n Trigger object index = "<<trigObjIt<<std::endl;
	  //std::cout << "triggerObjectID=1, triggerFilterBitSum = "<<triggerFilterBitSum<<std::endl;
	  //std::cout <<" Loop over trigger filters that I am interested in"<<std::endl;
	  
	  for(auto &triggerFilter : triggerObjectsForStudiesCount)
	    {
	      // Keep only the the ones mentioned in the config file 
	      if(triggerObjectId != triggerFilter.first.first) continue;
	      
	      //std::cout << "Checking if filter sum ("<<triggerFilterBitSum<<")"<<"  passes filter "<<triggerFilter.first.second;
	      
	      if( (triggerFilterBitSum >> triggerFilter.first.second) & 0x1 )
		{
		  //std::cout << " PASSED!";
		  
		  if (matchWithFourHighestBjets)
		    {
		      auto jetIdAndMinDeltaRandPt = getClosestJetIndexToTriggerObject(nat.TrigObj_eta.At(trigObjIt), nat.TrigObj_phi.At(trigObjIt), LeadingFour_selected_bjets, 0.5);
		      int bestMatchingIndex = std::get<0>( jetIdAndMinDeltaRandPt );
		      
		      if (bestMatchingIndex >= 0)
			{
			  float matchedJet_minDR = std::get<1>(jetIdAndMinDeltaRandPt);
			  float matchedJet_pt    = std::get<2>(jetIdAndMinDeltaRandPt);
			  triggerObjectPerJetCount.at(bestMatchingIndex).at(triggerFilter.first) = true;
			}
		      //else
		      //{
		      //std::cout<<""<<std::endl;
		      //}
		    }
		  else
		    {
		      ++triggerFilter.second;
		    }
		}
	      //else
	      //{
	      //std::cout << " FAILED!"<<std::endl;
	      //}
	    }
	} // Closes Loop over trigger objects
      
      if(matchWithFourHighestBjets)
	{
	  for(auto &triggerFilter : triggerObjectsForStudiesCount) // for all the trigger filters
	    {
	      for(auto &jetFiltersMap : triggerObjectPerJetCount) //for all the 4 selected jets
		{
		  if(jetFiltersMap.at(triggerFilter.first)) ++triggerFilter.second; //if selected jet was matched with the filter object I increment the count
		}
	    }
	}
      
      // Fill the output tree
      tOut->Fill();
    } // Closes event loop
  
  std::cout << "[INFO] ... done, saving output file" << std::endl;
  outputFile.cd();
  tOut->Write();
}

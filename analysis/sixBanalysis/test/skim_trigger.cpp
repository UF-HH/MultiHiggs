/*
 DESCRIPTION:
 
 USAGE:
 skim_trigger.exe --input input/PrivateMC_2018/NMSSM_XYH_YToHH_6b_MX_600_MY_400.txt --cfg config/skim_trigger_2018.cfg  --output prova.root --is-signal --match
*/
#include <iostream>
#include <string>
#include <iomanip>
#include <any>
#include <chrono>

#include <boost/program_options.hpp>
namespace po = boost::program_options;

#include "DirectionalCut.h"
#include "CfgParser.h"
#include "NanoAODTree.h"
#include "NormWeightTree.h"

#include "SkimUtils.h"
namespace su = SkimUtils;

#include "OutputTree.h"
#include "jsonLumiFilter.h"
#include "Skim_functions.h"

#include "JetTools.h"
//#include "BtagSF.h"
#include "Cutflow.h"

#include "Timer.h"
#include "DebugUtils.h"

#include "TFile.h"
#include "TROOT.h"
#include "TH1F.h"

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

// -----------------------------------
// shortcuts to access cfgParser options with defaults

template <typename T>
T readCfgOptWithDefault(CfgParser& config, std::string optName, T default_ret){
  throw std::runtime_error("please provide an override template implementation for this type");
}

template <>
bool readCfgOptWithDefault<bool>(CfgParser& config, std::string optName, bool default_ret){
  if (config.hasOpt(optName))
    return config.readBoolOpt(optName);
  else
    return default_ret;
}

template <>
int readCfgOptWithDefault<int>(CfgParser& config, std::string optName, int default_ret){
  if (config.hasOpt(optName))
    return config.readIntOpt(optName);
  else
    return default_ret;
}

template <>
float readCfgOptWithDefault<float>(CfgParser& config, std::string optName, float default_ret){
  if (config.hasOpt(optName))
    return config.readFloatOpt(optName);
  else
    return default_ret;
}

template <>
double readCfgOptWithDefault<double>(CfgParser& config, std::string optName, double default_ret){
  if (config.hasOpt(optName))
    return config.readDoubleOpt(optName);
  else
    return default_ret;
}

template <>
std::string readCfgOptWithDefault<std::string>(CfgParser& config, std::string optName, std::string default_ret){
  if (config.hasOpt(optName))
    return config.readStringOpt(optName);
  else
    return default_ret;
}

template <typename T>
bool checkBit(T value, int bitpos)
{
  T unit = 1;
  return value & (unit << bitpos);
}

float computePUweight(TH1* histo_pileup, double npu)
{
  int nbin = histo_pileup->FindBin(npu);
  return histo_pileup->GetBinContent(nbin);
}

float deltaPhi(float phi1, float phi2)
{
  float delphi = TMath::Abs(TMath::Abs(TMath::Abs(phi1 - phi2) - TMath::Pi())-TMath::Pi());
  return delphi;
}

std::tuple<int,float,float> getClosestJetIndexToTriggerObject(float triggerObjectEta, float triggerObjectPhi, std::vector<Jet>& jets, float maxDR)
{
  int closestJetIndex = -1;
  float minDR         = 1024;
  float minDRjetPt    = -1;
  
  for (unsigned int i=0; i<jets.size(); i++)
    {
      Jet jet = jets.at(i);
      
      float dPhi = deltaPhi(jet.get_phi(), triggerObjectPhi);
      float dEta = jet.get_eta() - triggerObjectEta;
      
      float dR2 = dPhi*dPhi + dEta*dEta;
      float dR  = std::sqrt(dR2);
      
      if (dR > maxDR) continue;
      
      minDR = dR;
      closestJetIndex = i;
      minDRjetPt  = jet.get_pt();
    }
  
  //std::cout << "Jet with index ="<<closestJetIndex<<"  and pt="<<minDRjetPt<<"  is closest to trigger object with dR="<<minDR<<std::endl;
  if(minDR > maxDR)
    {
      closestJetIndex = -1;
    }
  return {closestJetIndex, minDR, minDRjetPt};
}


int main(int argc, char** argv)
{
  cout << "[INFO] ... starting program" << endl;
  const auto start_prog_t = chrono::high_resolution_clock::now();
  
  // Declare command line options
  po::options_description desc("Skim options");
  desc.add_options()
    ("help", "produce help message")
    ("cfg"   , po::value<string>()->required(), "skim config")
    ("input" , po::value<string>()->required(), "input file list")
    ("output", po::value<string>()->required(), "output file LFN")
    // optional
    ("maxEvts"   , po::value<int>()->default_value(-1), "max number of events to process")
    ("pickEvt"   , po::value<string>()->default_value(""), "run on this run:lumi:event number only (for debug). Use wildcard * to match all")
    ("puWeight"  , po::value<string>()->default_value(""), "PU weight file name")
    ("seed"      , po::value<int>()->default_value(12345), "seed to be used in systematic uncertainties such as JEC, JER, etc")
    // flags
    ("is-data",       po::value<bool>()->zero_tokens()->implicit_value(true)->default_value(false), "mark as a data sample (default is false)")
    ("is-signal",     po::value<bool>()->zero_tokens()->implicit_value(true)->default_value(false), "mark as a HH signal sample (default is false)")
    ("match",         po::value<bool>()->zero_tokens()->implicit_value(true)->default_value(false), "match with four highest b-tagged jets")
    ("save-p4",       po::value<bool>()->zero_tokens()->implicit_value(true)->default_value(false), "save the tlorentzvectors in the output")
    ("debug",         po::value<bool>()->zero_tokens()->implicit_value(true)->default_value(false), "debug this event (verbose printing)");
  
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
  
  // Read config and other cmd line options for skims
  const bool is_data = opts["is-data"].as<bool>();
  cout << "[INFO] ... is a data sample? " << std::boolalpha << is_data << std::noboolalpha << endl;
  
  const bool is_signal = (is_data ? false : opts["is-signal"].as<bool>());
  cout << "[INFO] ... is a signal sample? " << std::boolalpha << is_signal << std::noboolalpha << endl;
  
  const bool matchWithFourHighestBjets =  opts["match"].as<bool>();
  cout << "[INFO] ... perform matching with four highest b-jets? "<<std::boolalpha << matchWithFourHighestBjets<< std::noboolalpha << endl;
  
  CfgParser config;
  if (!config.init(opts["cfg"].as<string>()))
    {
      cerr << "** [ERROR] no config file was provided" << endl;
      return 1;
    }
  cout << "[INFO] ... using config file " << opts["cfg"].as<string>() << endl;
  
  enum SkimTypes
  {
    kTrgEff,
    knull
  };
  
  string year = config.readStringOpt("parameters::year");
  
  // Prepare event loop
  cout << "[INFO] ... opening file list : " << opts["input"].as<string>().c_str() << endl;
  if ( access( opts["input"].as<string>().c_str(), F_OK ) == -1 ){
    cerr << "** [ERROR] The input file list does not exist, aborting" << endl;
    return 1;        
  }
  
  // Joining all the NANOAOD input file in a TChain in order to be used like an unique three
  TChain ch("Events");
  int nfiles = su::appendFromFileList(&ch, opts["input"].as<string>());
  
  if (nfiles == 0){
    cerr << "** [ERROR] The input file list contains no files, aborting" << endl;
    return 1;
  }
  cout << "[INFO] ... file list contains " << nfiles << " files" << endl;
  cout << "[INFO] ... creating tree reader" << endl;
  
  // The TChain is passed to the NanoAODTree_SetBranchImpl to parse all the branches
  NanoAODTree nat (&ch);
  
  cout << "[INFO] ... loading the following triggers" << endl;
  for (auto trg : config.readStringListOpt("triggers::makeORof"))
    {
      cout << "   - " << trg << endl;
    }
  nat.triggerReader().setTriggers(config.readStringListOpt("triggers::makeORof"));
  
  jsonLumiFilter jlf;
  if (is_data)
    jlf.loadJSON(config.readStringOpt("data::lumimask")); // just read the info for data, so if I just skim MC I'm not forced to parse a JSON
  
  std::cout << "Opening the file "<<std::endl;
  
  std::string pufName = config.readStringOpt("parameters::PUweightFile");
  std::cout << "pufName = "<<pufName<<std::endl;
  
  TFile* fPileUp = TFile::Open(pufName.c_str());
  TH1* histo_pileup = (TH1*) fPileUp->Get("PUweights");
  NormWeightTree nwt;
  
  std::string pu_weight_file;
  pu_weight_file = opts["puWeight"].as<string>();
  
  /*
  // b-tag reweighting
  std::unique_ptr<BTagCalibration> btagCalibration;
  std::unique_ptr<BTagCalibrationReader> btcr;
  if (!is_data)
    {
      cout << "[INFO] : b tag SF file : " << config.readStringOpt("parameters::BJetScaleFactorsFile") << endl;
      btagCalibration = std::unique_ptr<BTagCalibration> (new BTagCalibration ("DeepCSV",any_cast<string>(config.readStringOpt("parameters::BJetScaleFactorsFile"))));
      btcr            = std::unique_ptr<BTagCalibrationReader> (new BTagCalibrationReader(BTagEntry::OP_MEDIUM,"central",{"up", "down"}));
      btcr->load(*btagCalibration, BTagEntry::FLAV_UDSG, "incl"  );
      btcr->load(*btagCalibration, BTagEntry::FLAV_C   , "mujets");
      btcr->load(*btagCalibration, BTagEntry::FLAV_B   , "mujets");
    }
  */
  
  ////////////////////////////////////////////////////////////////////////
  // Prepare the output
  ////////////////////////////////////////////////////////////////////////
  string outputFileName = opts["output"].as<string>();
  cout << "[INFO] ... saving output to file : " << outputFileName << endl;
  TFile outputFile(outputFileName.c_str(), "recreate");
  
  // TTree with a custom format
  TTree* tOut = new TTree("TrgTree", "TrgTree");
  
  Timer loop_timer;
  Skim_functions* skf;
  skf = new Skim_functions();
  
  skf->Print();
  skf->set_timer(&loop_timer);
  
  // common
  unsigned int run_;
  unsigned int luminosityBlock_;
  long long    event_;
  
  float btag_SF_;
  float weight_;
  
  // Leptons
  float highestIsoElecton_pt_;
  float electronTimesMuoncharge_;
  
  // jets
  float jetFirstHighestPt_pt_;
  float jetSecondHighestPt_pt_;
  float jetThirdHighestPt_pt_;
  float jetForthHighestPt_pt_;
  float fourHighestJetPt_sum_;
  float caloJetSum_;
  int numberOfJetsCaloHT_;
  float pfJetSum_;
  int numberOfJetsPfHT_;
  float onlyJetSum_;
  int numberOfJetsOnlyHT_;
  float jetFirstHighestDeepFlavB_deepFlavB_;
  float jetFirstHighestDeepFlavB_pt_;
  float jetFirstHighestDeepFlavB_eta_;
  int jetFirstHighestDeepFlavB_hadronFlavour_;
  
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
  tOut->Branch("caloJetSum"  , &caloJetSum_  );
  tOut->Branch("numberOfJetsCaloHT"    , &numberOfJetsCaloHT_    );
  tOut->Branch("pfJetSum"  , &pfJetSum_  );
  tOut->Branch("numberOfJetsPfHT"    , &numberOfJetsPfHT_    );
  tOut->Branch("onlyJetSum"  , &onlyJetSum_  );
  tOut->Branch("numberOfJetsOnlyHT"    , &numberOfJetsOnlyHT_    );
  tOut->Branch("jetFirstHighestDeepFlavB_deepFlavB" , &jetFirstHighestDeepFlavB_deepFlavB_ );
  tOut->Branch("jetFirstHighestDeepFlavB_pt" , &jetFirstHighestDeepFlavB_pt_ );
  tOut->Branch("jetFirstHighestDeepFlavB_eta" , &jetFirstHighestDeepFlavB_eta_ );
  tOut->Branch("jetFirstHighestDeepFlavB_hadronFlavour" , &jetFirstHighestDeepFlavB_hadronFlavour_ );
  
  //enable trigger filters
  std::map<std::pair<int,int>, std::string > triggerObjectsForStudies        ; // <<objectId, FilterId> , filterName>
  std::map<std::pair<int,int>, float >       HTFilterHt                      ; // <<objectId, FilterId> , HTthreshold>
  std::map<std::pair<int,int>, int > triggerObjectsForStudiesCount           ; // <<objectId, FilterId> , numberOfObjects>
  std::map<std::pair<int,int>, float > triggerObjectsForStudiesMinDeltaR     ; // <<objectId, FilterId> , minDeltaR>
  std::map<std::pair<int,int>, float > triggerObjectsForStudiesMinDeltaRjetPt; // <<objectId, FilterId> , minDeltaRJetPt>
  std::map<std::pair<int,int>, int > jetFirstHighestDeepFlavB_triggerFlag_   ; // <<objectId, FilterId> , triggerFlag>
  std::vector<std::map<std::pair<int,int>, bool  >> triggerObjectPerJetCount  (4);
  std::vector<std::map<std::pair<int,int>, float >> triggerObjectPerJetDeltaR (4);
  std::vector<std::map<std::pair<int,int>, float >> triggerObjectPerJetDeltaPt(4);
  std::vector<std::tuple<float,float,float>>        selectedJetPtEtaPhiVector (4);
  
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
      
      for (auto& triggerObject : triggerObjectMatchingVector)
	{
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
	  
	  //std::cout << "triggerObjectTokens[0].data() = "<<triggerObjectTokens[0].data()<<"   triggerObjectTokens[1].data() = "<<triggerObjectTokens[1].data()<<std::endl;
	  //std::cout << "objectAndFilter = "<<objectAndFilter<<std::endl;
	  
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
  
  
  Cutflow cutflow;
  Cutflow cutflow_Unweighted("h_cutflow_unweighted", "Unweighted selection cutflow");
  
  skf->initialize_params_from_cfg(config);
  
  //%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  // Execute event loop
  //%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  int maxEvts = opts["maxEvts"].as<int>();
  std::cout << "Will run on "<<maxEvts<<"    events"<<std::endl;
  
  if (maxEvts >= 0)
    cout << "[INFO] ... running on : " << maxEvts << " events" << endl;
  
  for (int iEv=0; true; ++iEv)
    {
      if (maxEvts >= 0 && iEv >= maxEvts)
      	break;
      
      loop_timer.start_lap();
            
      if (iEv % 1000 == 0) cout << "... processing event " << iEv << endl;
      if (!nat.Next()) break;
            
      // Skip invalid lumis
      if (is_data && !jlf.isValid(*nat.run, *nat.luminosityBlock)){
	continue;
      }
      
      EventInfo ei;
      
      run_             = *(nat.run);
      luminosityBlock_ = *(nat.luminosityBlock);
      event_           = *(nat.event);
      
      // calculate here weights used for the analysis
      float genWeight = (is_data ? 1 : *(nat.genWeight));
      weight_ = genWeight;
      
      // events can start be filtered from here (after saving all gen weights)                                                                                                                            
      cutflow.add("total", nwt);
      cutflow_Unweighted.add("total");

      float w_PU = 1.0;
      if (!is_data)
	{
	  w_PU = computePUweight(histo_pileup, *(nat.Pileup_nTrueInt));
	}
      weight_ = w_PU * genWeight;
            
      //===================================================================
      // Apply HLT_IsoMu path
      //===================================================================
      if(!is_signal)
	{
	  if(!nat.getTrgOr()) continue;
	}
      cutflow.add("trigger", nwt);
      cutflow_Unweighted.add("trigger");
      
      //==================================
      // Apply METFilters
      //==================================
      bool applyMETFilters = config.readBoolOpt("configurations::applyMETFilters");
      bool bMETFilters = *nat.Flag_goodVertices && *nat.Flag_globalSuperTightHalo2016Filter && *nat.Flag_HBHENoiseFilter && *nat.Flag_HBHENoiseIsoFilter && *nat.Flag_EcalDeadCellTriggerPrimitiveFilter && *nat.Flag_BadPFMuonFilter && *nat.Flag_eeBadScFilter && (*nat.Flag_ecalBadCalibFilter || (year=="2016"));
      if (applyMETFilters)
	{
	  if (!bMETFilters) continue;
	}
      loop_timer.click("MET Filters");
      cutflow.add("met filters", nwt);
      cutflow_Unweighted.add("met filters");
      
      //=====================================================================
      // Apply muon selection
      //=====================================================================
      float muonPtCut  = config.readFloatOpt("configurations::muonPtCut");
      float muonEtaCut = config.readFloatOpt("configurations::muonEtaCut");
      float muonIsoCut= config.readFloatOpt("configurations::muonIsoCut");
      float additionalMuonIsoCut = config.readFloatOpt("configurations::additionalMuonIsoCut");
      string muonID    = config.readStringOpt("configurations::muonID");
      
      std::vector<Muon> selected_muons;
      std::vector<Muon> additional_muons;
      
      electronTimesMuoncharge_ = 1.0;
      //int isoMuonJetId         = -1;      
      for (unsigned int imu=0; imu < *(nat.nMuon); ++imu)
	{
	  Muon mu(imu, &nat);
	  float pt  = get_property(mu, Muon_pt);
	  float eta = get_property(mu, Muon_eta);
	  
	  // Apply pt & eta cuts
	  if (pt < muonPtCut) continue;
	  if (std::abs(eta) > muonEtaCut) continue;
	  
	  bool ID_WPL = get_property(mu, Muon_looseId);
	  bool ID_WPM = get_property(mu, Muon_mediumId);
	  bool ID_WPT = get_property(mu, Muon_tightId);
	  
	  // Apply ID requirement
	  if (muonID == "Loose")
	    {
	      if (!ID_WPL) continue;
	    }
	  else if (muonID == "Medium")
	    {
	      if (!ID_WPM) continue;
	    }
	  else if (muonID == "Tight")
	    {
	      if (!ID_WPT) continue;
	    }
	  
	  // Apply isolation cut
	  float iso = get_property(mu, Muon_pfRelIso04_all);
	  if (iso < muonIsoCut)
	    {
	      selected_muons.push_back(mu);
	      electronTimesMuoncharge_ = get_property(mu, Muon_charge);
	      //isoMuonJetId             = get_property(mu, Muon_jetIdx);
	    }
	  else if (iso < additionalMuonIsoCut)
	    {
	      additional_muons.push_back(mu);
	    }
	} // Closes loop over all muons in the event
      
      const DirectionalCut<int> cfg_nMuons(config, "configurations::nMuonsCut");
      const DirectionalCut<int> cfg_nAddMuons(config, "configurations::nAdditionalMuonsCut");
      if (!is_signal)
	{
	  if (!cfg_nMuons.passedCut(selected_muons.size())) continue;
	  if (!cfg_nAddMuons.passedCut(additional_muons.size())) continue;
	  if (0)
	    {
	      std::cout << "\n" <<std::endl;
	      std::cout << "Selected muons   = "<<selected_muons.size()<<std::endl;
	      std::cout << "Additional muons = "<<additional_muons.size()<<std::endl;
	    }
	}
      cutflow.add("#mu selection", nwt);
      cutflow_Unweighted.add("#mu selection");
      
      //====================================================================================
      // Electron selection
      //====================================================================================
      float elePtCut  = config.readFloatOpt("configurations::elePtCut");
      float eleEtaCut = config.readFloatOpt("configurations::eleEtaCut");
      float eleIsoCut= config.readFloatOpt("configurations::eleIsoCut");
      float additionalEleIsoCut = config.readFloatOpt("configurations::additionalEleIsoCut");
      string eleID    = config.readStringOpt("configurations::eleID");
      
      std::vector<Electron> selected_electrons;
      std::vector<Electron> additional_electrons;
      
      for (unsigned int iele=0; iele< *(nat.nElectron); ++iele)
        {
          Electron ele(iele, &nat);
          float pt  = get_property(ele, Electron_pt);
          float eta = get_property(ele, Electron_eta);
	  
	  // Apply pt & eta cuts
          if (pt < elePtCut) continue;
          if (std::abs(eta) > eleEtaCut) continue;
	  
	  // Apply ID cut
	  bool ID_WPL = get_property(ele, Electron_mvaFall17V2Iso_WPL);
	  bool ID_WP90 = get_property(ele, Electron_mvaFall17V2Iso_WP90);
	  bool ID_WP80 = get_property(ele, Electron_mvaFall17V2Iso_WP80);
	  if (eleID == "Loose")
	    {
	      if (!ID_WPL) continue;
	    }
	  else if (eleID == "90")
	    {
	      if (!ID_WP90) continue;
	    }
	  else if (eleID == "80")
	    {
	      if (!ID_WP80) continue;
	    }
	  
	  // Apply isolation cut
	  float iso = get_property(ele, Electron_pfRelIso03_all);
	  if (iso < eleIsoCut)
	    {
	      selected_electrons.push_back(ele);
	      highestIsoElecton_pt_ = pt;
	      electronTimesMuoncharge_ *= get_property(ele, Electron_charge);
	    }
	  else if (iso < additionalEleIsoCut)
	    {
	      additional_electrons.push_back(ele);
	    }
	}
      
      const DirectionalCut<int> cfg_nElectrons(config, "configurations::nEleCut");
      const DirectionalCut<int> cfg_nAdditionalElectrons(config, "configurations::nAdditionalEleCut");
      bool bEleMuOS = config.readBoolOpt("configurations::EleMuOS");
      
      if (!is_signal)
	{
	  if (!cfg_nElectrons.passedCut(selected_electrons.size())) continue;
	  if (!cfg_nAdditionalElectrons.passedCut(additional_electrons.size())) continue;
	  if (bEleMuOS)
	    {
	      if (electronTimesMuoncharge_ == 1) continue;
	    }
	  
	  if (0)
	    {
	      std::cout << "Number of electrons = "<<selected_electrons.size()<<std::endl;
	      std::cout << "Number of additional electrons = "<<additional_electrons.size()<<std::endl;
	      std::cout << "\n Electron Charge * Muon Charge = "<<electronTimesMuoncharge_<<std::endl;
	    }
	}
      cutflow.add("ele selection", nwt);
      cutflow_Unweighted.add("ele selection");
      
      //====================================================================================
      // Jet selection
      //====================================================================================
      std::vector<Jet> selected_jets;
      
      numberOfJetsCaloHT_ = 0;
      numberOfJetsPfHT_   = 0;
      numberOfJetsOnlyHT_ = 0;
      
      caloJetSum_         = 0.;
      pfJetSum_           = 0.;
      onlyJetSum_         = 0.;
      
      float PFJetPtCut      = config.readFloatOpt("configurations::PFJetPtCut");
      float PFJetPtCutForHT = config.readFloatOpt("configurations::PFJetPtCutForHT");
      float PFJetEtaCut     = config.readFloatOpt("configurations::PFJetEtaCut");
      int PFJetIDCut        = config.readIntOpt("configurations::PFJetIDCut");
      int PFJetPUIDCut      = config.readIntOpt("configurations::PFJetPUIDCut");
      
      // Loop over all jets
      for (unsigned int ij=0; ij < *(nat.nJet); ++ij)
	{
	  Jet jet(ij, &nat);
	  
	  float pt  = jet.get_pt();
	  float eta = jet.get_eta();
	  int index = jet.getIdx();
	  int ID    = jet.get_id();
	  int PUID  = jet.get_puid();
	  float btagDisc = jet.get_btag();
	  
	  if (0) std::cout << "Jet="<<ij<<"   pT="<<pt<<"  eta="<<eta<<"  index="<<index;
	  
	  // Calculate the HT based on the hadronic jets, muon jets and electron jets
	  bool passedCutsForHT = pt >= PFJetPtCutForHT && std::abs(eta) <= PFJetEtaCut;
	  if (passedCutsForHT)
	    {
	      numberOfJetsPfHT_++;
	      pfJetSum_ += jet.get_pt();
	    }
	  
	  // Skip jet if it overlaps with a muon
	  bool isMuon = false;
	  for (unsigned int im=0; im<selected_muons.size(); ++im)
	    {
	      Muon mu = selected_muons.at(im);
	      int mu_jetIdx = get_property(mu, Muon_jetIdx);
	      if(index == mu_jetIdx)
		{
		  if (0) std::cout << "      | index same as the mu index, mu pt="<<mu.get_pt()<<"  eta="<<mu.get_eta()<<"   isolation="<<get_property(mu, Muon_pfRelIso04_all)<<std::endl;
		  isMuon = true;
		  break;
		}
	    }
	  if (isMuon) continue;
	  
	  // Calculate the caloHT without the muons, electrons still contribute
	  if (passedCutsForHT)
	    {
	      caloJetSum_ += pt;
	      numberOfJetsCaloHT_++;
	    }
	  
	  bool isElectron = false;
	  for (unsigned int ie=0; ie<selected_electrons.size(); ++ie)
	    {
	      Electron ele   = selected_electrons.at(ie);
	      int ele_jetIdx = get_property(ele, Electron_jetIdx);
	      if (index == ele_jetIdx)
		{
		  if (0) std::cout << "     | index same as the ele index, ele pt="<<ele.get_pt()<<"  eta="<<ele.get_eta()<<"   isolation="<<get_property(ele, Electron_pfRelIso03_all)<<std::endl;
		  isElectron = true;
		  break;
		}
	    }
	  if (isElectron) continue;
	  if (0) std::cout << " "<<std::endl;
	  
	  // Calculate the HT only for hadronic jets
	  if (passedCutsForHT)
	    {
	      numberOfJetsOnlyHT_++;
	      onlyJetSum_+= pt;
	    }
	  
	  // Select remaining four jets
	  if (pt < PFJetPtCut) continue;
	  if (std::abs(eta) > PFJetEtaCut) continue;
	  if (btagDisc < 0) continue;
	  if (!checkBit(ID, PFJetIDCut)) continue;
	  if (pt < 50 && !checkBit(PUID, PFJetPUIDCut)) continue;
	  
	  // Save above jets
	  selected_jets.push_back(jet);
	} // Closes loop over all jets in the event
      
      const DirectionalCut<int> cfg_nJets(config, "configurations::nPFJetCut");
      if (!cfg_nJets.passedCut(selected_jets.size())) continue;
      cutflow.add("hadronic jet selection", nwt);
      cutflow_Unweighted.add("hadronic jet selection");
      
      if (0)
	{
	  std::cout << "\n=========================================================================="<<std::endl;
	  std::cout << "                Event = "<<iEv<<std::endl;
	  std::cout << "\n=========================================================================="<<std::endl;
	  std::cout << "\nNumber of selected hadronic jets : "<<selected_jets.size()<<std::endl;
	  std::cout << "PF HT       = "<<pfJetSum_  <<"   (from "<<numberOfJetsPfHT_<<"  jets)"<<std::endl; 
	  std::cout << "Calo HT     = "<<caloJetSum_<<"   (from "<<numberOfJetsCaloHT_<<" jets)"<<std::endl;
	  std::cout << "Hadronic HT = "<<onlyJetSum_<<"   (from "<<numberOfJetsOnlyHT_<<"  jets)"<<std::endl;
	}
      
      // Before sorting
      if (0)
	{
	  std::cout << "\n Before sorting \n"<<std::endl;
	  for (unsigned int ij=0; ij<selected_jets.size(); ij++)
	    {
	      Jet jet = selected_jets.at(ij);
	      float pt  = jet.get_pt();
	      float eta = jet.get_eta();
	      float btagDisc = jet.get_btag();
	      std::cout << "i="<<ij<<"   pt="<<pt<<"   eta="<<eta<<"   btag="<<btagDisc<<std::endl;
	    }
	}
      
      // After sorting by b-tagging score
      std::vector<Jet> jets_sorted_bTag = skf->btag_sort_jets(nat, ei, selected_jets);
      std::vector<Jet> jetsForTrgMatching_sorted_btag;
      
      if (0) std::cout << "\n After sorting by b-tagging score: \n"<<std::endl;
      for (unsigned int ij=0; ij<jets_sorted_bTag.size(); ij++)
	{
	  Jet jet = jets_sorted_bTag.at(ij);
	  float pt  = jet.get_pt();
	  float eta = jet.get_eta();
	  float btagDisc = jet.get_btag();
	  if (ij < 4)
	    {
	      jetsForTrgMatching_sorted_btag.push_back(jet);
	      if (0) std::cout<< "i="<<ij<<"   pt="<<pt<<"   eta="<<eta<<"   btag="<<btagDisc<<std::endl;
	    }
	}
      
      // selected_jets                  : all hadronic jets in the event
      // jets_sorted_bTag               : all hadronic jets in the event, sorted by b-tagging score
      // jetsForTrgMatching_sorted_btag : four leading in b-tagging score hadronic jets, to be used in the trigger matching
      // jetsForTrgMatching_sorted_pt   : four leading in b-tagging score hadronic jets, sorted by pT, to be used in the trigger matching
      std::vector<Jet> jetsForTrgMatching_sorted_pt = skf->pt_sort_jets(nat, ei, jetsForTrgMatching_sorted_btag);
      
      // After sorting by pT
      if (0) std::cout << "\nAfter sorting by pT"<<std::endl;
      for (unsigned int ij=0; ij<jetsForTrgMatching_sorted_pt.size(); ij++)
	{
	  Jet jet = jetsForTrgMatching_sorted_pt.at(ij);
	  float pt  = jet.get_pt();
	  float eta = jet.get_eta();
	  float btagDisc = jet.get_btag();
	  if (0) std::cout<< "i="<<ij<<"   pt="<<pt<<"   eta="<<eta<<"   btag="<<btagDisc<<std::endl;
	}
      
      // Save the pt of the four leading in b-tagging score jets
      jetFirstHighestPt_pt_  = jetsForTrgMatching_sorted_pt.at(0).get_pt();
      jetSecondHighestPt_pt_ = jetsForTrgMatching_sorted_pt.at(1).get_pt();
      jetThirdHighestPt_pt_  = jetsForTrgMatching_sorted_pt.at(2).get_pt();
      jetForthHighestPt_pt_  = jetsForTrgMatching_sorted_pt.at(3).get_pt();
      fourHighestJetPt_sum_  = jetFirstHighestPt_pt_ + jetSecondHighestPt_pt_ + jetThirdHighestPt_pt_ + jetForthHighestPt_pt_;
      
      // Save the b-tag score, pt, eta, and hadron flavour of the leading in b-tagging score jet
      jetFirstHighestDeepFlavB_deepFlavB_ = jetsForTrgMatching_sorted_btag.at(0).get_btag();
      if (is_data)
	{
	  jetFirstHighestDeepFlavB_hadronFlavour_ = -999;
	}
      else
	{
	  jetFirstHighestDeepFlavB_hadronFlavour_ = get_property(jetsForTrgMatching_sorted_btag.at(0), Jet_hadronFlavour);
	}
      jetFirstHighestDeepFlavB_pt_  = jetsForTrgMatching_sorted_btag.at(0).get_pt();
      jetFirstHighestDeepFlavB_eta_ = jetsForTrgMatching_sorted_btag.at(0).get_eta();
      int highestDeepFlavBjetID = jetsForTrgMatching_sorted_btag.at(0).getIdx();
      
      int highestDeepFlavBjetPosition = -1;
      for(uint pos=0; pos<jetsForTrgMatching_sorted_pt.size(); ++pos)
	{
	  if(jetsForTrgMatching_sorted_pt.at(pos).getIdx() == highestDeepFlavBjetID)
	    {
	      highestDeepFlavBjetPosition = pos;
	    }
	}
      assert(highestDeepFlavBjetPosition != -1);
      if (0) std::cout << "Highest Deep Flavour b-jet position in the vector sorted by pT= "<<highestDeepFlavBjetPosition<<std::endl;
      
      // Get number of trigger filters
      
      // reset map
      for(auto &triggerFilter : triggerObjectsForStudiesCount)         triggerFilter.second = 0;
      for(auto &btagFlag      : jetFirstHighestDeepFlavB_triggerFlag_) btagFlag.second = 0;
      for(auto &triggerHT     : HTFilterHt)                            triggerHT.second = -1.;
      if (matchWithFourHighestBjets)
	{
	  for(auto& filterIdAndMaxDeltaR      : triggerObjectsForStudiesMinDeltaR     ) filterIdAndMaxDeltaR     .second = -1;
	  for(auto& filterIdAndMaxDeltaRjetPt : triggerObjectsForStudiesMinDeltaRjetPt) filterIdAndMaxDeltaRjetPt.second = -1;
	  
	  for(auto& jetAndFilterCounts  : triggerObjectPerJetCount  ) for(auto& filterCount   : jetAndFilterCounts ) filterCount  .second = false;
	  for(auto& jetAndFilterDeltaR  : triggerObjectPerJetDeltaR ) for(auto& filterDeltaR  : jetAndFilterDeltaR ) filterDeltaR .second =  999.;
	  for(auto& jetAndFilterDeltaPt : triggerObjectPerJetDeltaPt) for(auto& filterDeltaPt : jetAndFilterDeltaPt) filterDeltaPt.second = -999.;
	  
	  int jetCounter=0;
	  for(const auto & jet : jetsForTrgMatching_sorted_pt)
	    {
	      selectedJetPtEtaPhiVector.at(jetCounter) = {jet.P4().Pt(), jet.P4().Eta(), jet.P4().Phi()};
	      jetCounter++;
	    }
	}
      
      //std::cout << "\nLoop over all trigger objects in the event\n"<<std::endl;
      float deltaR = config.readFloatOpt("parameters::deltaR");
      
      // Loop over all trigger objects
      for (uint trigObjIt=0; trigObjIt<*(nat.nTrigObj); ++trigObjIt)
	{
	  int triggerObjectId = nat.TrigObj_id.At(trigObjIt);
	  
	  // Skip trigger objects related to Electrons (11), Photons (22), Muons (13), Taus (15), Fatjets (6), MET (2)
	  if (triggerObjectId == 11 || triggerObjectId == 22 || triggerObjectId == 13 || triggerObjectId == 15 || triggerObjectId == 6 || triggerObjectId == 2) continue; 
	  
	  // TrigObj_filterBits
	  int triggerFilterBitSum = nat.TrigObj_filterBits.At(trigObjIt);
	  
	  for(auto &triggerFilter : triggerObjectsForStudiesCount)
	    {
	      if(triggerObjectId != triggerFilter.first.first) continue;
	      if((triggerFilterBitSum >> triggerFilter.first.second) & 0x1)
		{
		  std::pair<int,int> objectAndFilter = std::make_pair( triggerFilter.first.first, triggerFilter.first.second);
		  std::string triggerFilterName = triggerObjectsForStudies[objectAndFilter].data();
		  
		  if(matchWithFourHighestBjets)
		    {
		      // Return the jet ID with the minDR, the minDR and pT
		      auto jetIdAndMinDeltaRandPt = getClosestJetIndexToTriggerObject(nat.TrigObj_eta.At(trigObjIt), nat.TrigObj_phi.At(trigObjIt), jetsForTrgMatching_sorted_pt, deltaR);
		      
		      if (0)
			{
			  std::cout << "Trigger obj. index = "<<trigObjIt
				    << "  matched with jet ="<<jetIdAndMinDeltaRandPt
				    <<"   filter name: "<<triggerFilterName
				    <<std::endl;
			}
		      
		      int bestMatchingIndex = std::get<0>(jetIdAndMinDeltaRandPt);
		      if (bestMatchingIndex >= 0)
			{
			  triggerObjectPerJetCount.at(bestMatchingIndex).at(triggerFilter.first)   = true;
			  
			  triggerObjectPerJetDeltaR.at(bestMatchingIndex).at(triggerFilter.first)  = std::get<1>(jetIdAndMinDeltaRandPt);
			  triggerObjectPerJetDeltaPt.at(bestMatchingIndex).at(triggerFilter.first) = std::get<2>(jetIdAndMinDeltaRandPt); 
			
			  float maxDeltaR      = triggerObjectsForStudiesMinDeltaR.at(triggerFilter.first);
			  //float maxDeltaRjetPt = triggerObjectsForStudiesMinDeltaRjetPt.at(triggerFilter.first);
			  if(maxDeltaR < std::get<1>( jetIdAndMinDeltaRandPt))
			    {
			      triggerObjectsForStudiesMinDeltaR.at(triggerFilter.first) = std::get<1>( jetIdAndMinDeltaRandPt );
			      triggerObjectsForStudiesMinDeltaRjetPt.at(triggerFilter.first) = std::get<2>( jetIdAndMinDeltaRandPt );
			    }
			} // Closes if statement: matched jet is found
		    }
		  else
		    {
		      ++triggerFilter.second;
		      if( jetFirstHighestDeepFlavB_triggerFlag_.find(triggerFilter.first) != jetFirstHighestDeepFlavB_triggerFlag_.end()) ++jetFirstHighestDeepFlavB_triggerFlag_[triggerFilter.first];
		    }
		  
		  // HT
		  if(triggerObjectId == 3)
		    {
		      HTFilterHt.at(triggerFilter.first) = nat.TrigObj_pt.At(trigObjIt);
		    }
		}
	    }
	} // Closes loop over trigger objects
      
      
      if (matchWithFourHighestBjets)
	{
	  for(auto &triggerFilter : triggerObjectsForStudiesCount)
	    {
	      for(auto &jetFiltersMap : triggerObjectPerJetCount)
		{
		  if (jetFiltersMap.at(triggerFilter.first)) ++triggerFilter.second;
		}
	    }
	  
	  for(auto & btagFilter : jetFirstHighestDeepFlavB_triggerFlag_)
	    {
	      if(triggerObjectPerJetCount[highestDeepFlavBjetPosition][btagFilter.first]) btagFilter.second = 1;
	    }
	}
      
      if (!is_data)
	{
	  std::vector<Jet> preselected_jets = {
	    jetsForTrgMatching_sorted_pt.at(0),
	    jetsForTrgMatching_sorted_pt.at(1),
	    jetsForTrgMatching_sorted_pt.at(2),
	    jetsForTrgMatching_sorted_pt.at(3)
	  };
	  // marina #fixme
	  // btag_SF = 1.0;
	  //auto all_btag_SF = computeBtagSF(preselected_jets, btcr.get());
	  // btag_SF_ = std::get<0>(all_btag_SF);
	}
      else
	{
	  btag_SF_ = 1.0;
	}
      
      tOut->Fill();
    } // Loop over all events
  
  cout << "[INFO] ... done, saving output file" << endl;
  outputFile.cd();
  
  cutflow.write(outputFile);
  cutflow_Unweighted.write(outputFile);
  
  tOut->Write();
}

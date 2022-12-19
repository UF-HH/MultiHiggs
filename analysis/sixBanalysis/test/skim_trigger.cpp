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

#include "SkimUtils.h"
namespace su = SkimUtils;

// #include "OutputTree.h"
#include "jsonLumiFilter.h"

#include "TFile.h"
#include "TROOT.h"
#include "TH1F.h"
using namespace std;

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

int main(int argc, char** argv)
{
  cout << "[INFO] ... starting program" << endl;
  
  ////////////////////////////////////////////////////////////////////////
  // Decalre command line options
  ////////////////////////////////////////////////////////////////////////
  
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
  
  const bool is_data = opts["is-data"].as<bool>();
  cout << "[INFO] ... is a data sample? " << std::boolalpha << is_data << std::noboolalpha << endl;
  
  const bool matchWithFourHighestBjets =  opts["match"].as<bool>();
  const bool isSignal =  opts["is-signal"].as<bool>();
  
  CfgParser config;
  if (!config.init(opts["cfg"].as<string>())) return 1;
  cout << "[INFO] ... using config file " << opts["cfg"].as<string>() << endl;
  
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
  if (is_data)
    jlf.loadJSON(config.readStringOpt("data::lumimask")); // just read the info for data, so if I just skim MC I'm not forced to parse a JSON
  
  std::string pufName = config.readStringOpt("parameters::PUweightFile");
  std::cout << "pufName = "<<pufName<<std::endl;
  
  TFile* fPileUp = TFile::Open(pufName.c_str());
  TH1* histo_pileup = (TH1*) fPileUp->Get("PUweights");
  NormWeightTree nwt;
  
  std::string pu_weight_file;
  pu_weight_file = opts["puWeight"].as<string>();
  
  
  
  ////////////////////////////////////////////////////////////////////////
  // Prepare the output
  ////////////////////////////////////////////////////////////////////////
  
  string outputFileName = opts["output"].as<string>();
  cout << "[INFO] ... saving output to file : " << outputFileName << endl;
  TFile outputFile(outputFileName.c_str(), "recreate");
  
  // TTree with a custom format
  TTree* tOut = new TTree("TrgTree", "TrgTree");
  
  // common
  unsigned int run_;
  unsigned int luminosityBlock_;
  long long    event_;
  
  float btag_SF_;
  
  float weight_;
  
  //leptons
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
      if (!is_data)
	{
	  w_PU = computePUweight(histo_pileup, *(nat.Pileup_nTrueInt));
	}
      
      float genWeight = (is_data ? 1 : *(nat.genWeight));
      weight_ = w_PU * genWeight;
      // std::cout << w_PU << " " << genWeight << " " << weight_ << std::endl;
      
      // check the trigger
      if(!isSignal) if( !nat.getTrgOr() ) continue;
      
      //Check if there is and iso muon with Pt>30 GeV
      int numberOfIsoMuon01 = 0;
      int numberOfIsoMuon03 = 0;
      int isoMuonJetId      = -1;
      electronTimesMuoncharge_ = 1;
      float muonPtCut = 29; // 26 GeV for 2018, 29 GeV for 2017
      for (uint candIt = 0; candIt < *(nat.nMuon); ++candIt)
        {
	  Muon theMuon (candIt, &nat);
	  float muonIsolation = get_property(theMuon, Muon_pfRelIso04_all);
	  if(muonIsolation<0.3 && get_property(theMuon, Muon_mediumId) && theMuon.P4().Pt() >= muonPtCut)
            {
	      if(muonIsolation<0.1 ) 
                {
		  ++numberOfIsoMuon01;
		  isoMuonJetId = get_property(theMuon, Muon_jetIdx);
		  electronTimesMuoncharge_ = get_property(theMuon, Muon_charge);
                }
	      ++numberOfIsoMuon03;
	      if(numberOfIsoMuon03>1) break;
            }
	  
        }
      if(!isSignal) if(numberOfIsoMuon01!=1 || numberOfIsoMuon03>1) continue;
      
      // find the four most b tagged jets and save them in the output
      
      std::vector<Jet> all_jets;
      all_jets.reserve(*(nat.nJet));
      caloJetSum_ = 0.;
      numberOfJetsCaloHT_ = 0;
      pfJetSum_ = 0.;
      numberOfJetsPfHT_ = 0;
      onlyJetSum_ = 0.;
      numberOfJetsOnlyHT_ = 0;
      
      for (uint ij = 0; ij < *(nat.nJet); ++ij)
        {
	  // here preselect jets
	  Jet jet (ij, &nat);
	  
	  if (jet.P4().Pt() >= 30. && std::abs(jet.P4().Eta()) < 2.5) 
            {
	      pfJetSum_ += jet.P4().Pt();
	      numberOfJetsPfHT_++;
            }
	  
	  bool isMuon = false;
	  for (uint candIt = 0; candIt < *(nat.nMuon); ++candIt)
            {
	      Muon theMuon (candIt, &nat);
	      if(get_property(theMuon, Muon_pfRelIso04_all) > 0.3) continue;
	      if(jet.getIdx() == get_property(theMuon, Muon_jetIdx))
                {
		  isMuon = true;
		  break;
                }
            }
	  if(isMuon) continue;
	  
	  if (jet.P4().Pt() >= 30. && std::abs(jet.P4().Eta()) < 2.5) 
            {
	      caloJetSum_ += jet.P4().Pt();
	      numberOfJetsCaloHT_++;
            }
	  
	  bool isElectron = false;
	  for (uint candIt = 0; candIt < *(nat.nElectron); ++candIt)
            {
	      Electron theElectron (candIt, &nat);
	      if(get_property(theElectron, Electron_pfRelIso03_all) > 0.3) continue;
	      if(jet.getIdx() == get_property(theElectron, Electron_jetIdx))
                {
		  isElectron = true;
		  break;
                }
            }
	  if(isElectron) continue;
	  
	  if (jet.P4().Pt() >= 30. && std::abs(jet.P4().Eta()) < 2.5) 
            {
	      onlyJetSum_ += jet.P4().Pt();
	      numberOfJetsOnlyHT_++;
            }
	  
	  // Jet ID flags bit1 is loose (always false in 2017 since it does not exist), bit2 is tight, bit3 is tightLepVeto
	  // but note that bit1 means idx 0 and so on
	  int jetid = get_property(jet, Jet_jetId); 
	  
	  if (!checkBit(jetid, 1)) // tight jet Id
	    continue;
	  
	  if (jet.P4().Pt() <= 25)
	    continue;
	  
	  if (std::abs(jet.P4().Eta()) > 2.4)
	    continue;
	  
	  if(jet.get_btag() < 0.) continue; 
	  if (!checkBit(get_property( jet,Jet_puId), 1) && jet.P4().Pt() <= 50) // medium PU Id - NOTE : not to be applied beyond 50 GeV: https://twiki.cern.ch/twiki/bin/viewauth/CMS/PileupJetID
	    continue;
	  
	  all_jets.emplace_back(jet);
        }
      
      if (all_jets.size() < 4) // I don't have 4 preselected jets
	continue;
      
      highestIsoElecton_pt_ = -999.;
      
      for (uint candIt = 0; candIt < *(nat.nElectron); ++candIt)
        {
	  Electron theElectron (candIt, &nat);
	  if(get_property(theElectron, Electron_pfRelIso03_all) > 0.1) continue;
	  highestIsoElecton_pt_ = theElectron.P4().Pt();
	  electronTimesMuoncharge_ *= get_property(theElectron, Electron_charge);
	  break;
        }
      
      if(matchWithFourHighestBjets)
        {
	  stable_sort(all_jets.begin(), all_jets.end(), [](const Jet & a, const Jet & b) -> bool
		      {
			return ( a.get_btag() > b.get_btag() );
		      });
	  all_jets.erase(all_jets.begin()+4, all_jets.end());
        }
      
      stable_sort(all_jets.begin(), all_jets.end(), [](const Jet & a, const Jet & b) -> bool
		  {
		    return ( a.P4().Pt() > b.P4().Pt() );
		  });
      
      jetFirstHighestPt_pt_  = all_jets.at(0).P4().Pt();
      jetSecondHighestPt_pt_ = all_jets.at(1).P4().Pt();
      jetThirdHighestPt_pt_  = all_jets.at(2).P4().Pt();
      jetForthHighestPt_pt_  = all_jets.at(3).P4().Pt();
      fourHighestJetPt_sum_  = jetFirstHighestPt_pt_ + jetSecondHighestPt_pt_ + jetThirdHighestPt_pt_ + jetForthHighestPt_pt_;
      
      // NOTE that this sorts from small to large, with A < B implemented as btagA > btagB, so the first element in the vector has the largest btag score
      stable_sort(all_jets.begin(), all_jets.end(), [](const Jet & a, const Jet & b) -> bool
		  {
		    return ( a.get_btag() > b.get_btag() );
		  });
      
      jetFirstHighestDeepFlavB_deepFlavB_ = all_jets.at(0).get_btag();
      if(!is_data) jetFirstHighestDeepFlavB_hadronFlavour_ = get_property(all_jets.at(0),Jet_hadronFlavour);
      else jetFirstHighestDeepFlavB_hadronFlavour_ = -999;
      jetFirstHighestDeepFlavB_pt_ = all_jets.at(0).P4().Pt();
      jetFirstHighestDeepFlavB_eta_ = all_jets.at(0).P4().Eta();
      int highestDeepFlavBjetID = all_jets.at(0).getIdx();
      
      // reorder by jet pt
      stable_sort(all_jets.begin(), all_jets.end(), [](const Jet & a, const Jet & b) -> bool
		  {
		    return ( a.P4().Pt() > b.P4().Pt() );
		  });
      
      int highestDeepFlavBjetPosition = -1;
      for(uint pos=0; pos<all_jets.size(); ++pos)
        {
	  if(all_jets.at(pos).getIdx() == highestDeepFlavBjetID)
            {
	      highestDeepFlavBjetPosition = pos;
            }
        }
      assert(highestDeepFlavBjetPosition != -1);
      
      // get number of trigger filters
      
      // reset map
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
	  for(const auto & jet : all_jets)
            {
	      selectedJetPtEtaPhiVector.at(jetCounter) = {jet.P4().Pt(), jet.P4().Eta(), jet.P4().Phi()};
	      jetCounter++;
            }
	  
        }
      
      // loop over all trigger objects
      for (uint trigObjIt = 0; trigObjIt < *(nat.nTrigObj); ++trigObjIt) //for over all trigger objects
        {
	  int triggerObjectId = nat.TrigObj_id.At(trigObjIt);
	  int triggerFilterBitSum = nat.TrigObj_filterBits.At(trigObjIt);
	  
	  for(auto &triggerFilter : triggerObjectsForStudiesCount)
            {
	      if(triggerObjectId != triggerFilter.first.first) continue;
	      if( (triggerFilterBitSum >> triggerFilter.first.second) & 0x1 ) //check object passes the filter
                {
		  if(matchWithFourHighestBjets)
                    {
		      auto jetIdAndMinDeltaRandPt = getClosestJetIndexToTriggerObject(nat.TrigObj_eta.At(trigObjIt), nat.TrigObj_phi.At(trigObjIt), all_jets, 0.5);
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
		      
                    }
		  else
                    {
		      ++triggerFilter.second;
		      if(jetFirstHighestDeepFlavB_triggerFlag_.find(triggerFilter.first) != jetFirstHighestDeepFlavB_triggerFlag_.end()) ++jetFirstHighestDeepFlavB_triggerFlag_[triggerFilter.first];
                    }
		  
		  if(triggerObjectId == 3 /*is HT*/)
                    {
		      HTFilterHt.at(triggerFilter.first) = nat.TrigObj_pt.At(trigObjIt);
                    }
		  
                }
            }
        }
      
      
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
	    all_jets.at(0),
	    all_jets.at(1),
	    all_jets.at(2),
	    all_jets.at(3)
	  };
	}
      btag_SF_            = 1.0;
      tOut->Fill();
    }
  
  cout << "[INFO] ... done, saving output file" << endl;
  outputFile.cd();
  tOut->Write();
}

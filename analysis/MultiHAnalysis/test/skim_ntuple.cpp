// skim_ntuple.exe --input input/PrivateMC_2018/NMSSM_XYH_YToHH_6b_MX_600_MY_400.txt --cfg config/skim_ntuple_2018.cfg  --output prova.root --is-signal
// skim_ntuple.exe --input input/Run2_UL/2018/TTJets.txt --cfg config/skim_ntuple_2018_ttbar.cfg  --output prova_ttbar.root
// skim_ntuple.exe --input input/Run2_UL/2018/SingleMuon_Run2.txt --cfg config/skim_ntuple_2018_ttbar.cfg  --output prova_singlemu_ttbarskim.root --is-data

#include <iostream>
#include <string>
#include <iomanip>
#include <any>
#include <chrono>

#include <boost/unordered_map.hpp>
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
#include "FourB_functions.h"
#include "SixB_functions.h"
#include "EightB_functions.h"
#include "TTBar_functions.h"
#include "JetTools.h"
#include "BtagSF.h"

#include "EventShapeCalculator.h"
#include "TriggerEfficiencyCalculator.h"

#include "Cutflow.h"
#include "HistoCollection.h"
#include "EvalNN.h"

#include "Timer.h"
#include "DebugUtils.h"

#include "TFile.h"
#include "TROOT.h"
#include "TH1F.h"

using namespace std;

std::vector<std::string> split_by_delimiter(std::string input, std::string delimiter) {
  std::vector<std::string> tokens;
  if (input == "")
    return tokens;

  size_t pos = 0;
  while ((pos = input.find(delimiter)) != std::string::npos) {
    tokens.push_back(input.substr(0, pos));
    input.erase(0, pos + delimiter.length());
  }
  tokens.push_back(input);  // last part splitted

  return tokens;
}

Variation string_to_jer_variation(std::string s) {
  if (s == "nominal")
    return Variation::NOMINAL;
  if (s == "up")
    return Variation::UP;
  if (s == "down")
    return Variation::DOWN;
  throw std::runtime_error(string("Cannot parse the variation ") + s);
}

// -----------------------------------
// shortcuts to access cfgParser options with defaults

template <typename T>
T readCfgOptWithDefault(CfgParser& config, std::string optName, T default_ret) {
  throw std::runtime_error("please provide an override template implementation for this type");
}

template <>
bool readCfgOptWithDefault<bool>(CfgParser& config, std::string optName, bool default_ret) {
  if (config.hasOpt(optName))
    return config.readBoolOpt(optName);
  else
    return default_ret;
}

template <>
int readCfgOptWithDefault<int>(CfgParser& config, std::string optName, int default_ret) {
  if (config.hasOpt(optName))
    return config.readIntOpt(optName);
  else
    return default_ret;
}

template <>
float readCfgOptWithDefault<float>(CfgParser& config, std::string optName, float default_ret) {
  if (config.hasOpt(optName))
    return config.readFloatOpt(optName);
  else
    return default_ret;
}

template <>
double readCfgOptWithDefault<double>(CfgParser& config, std::string optName, double default_ret) {
  if (config.hasOpt(optName))
    return config.readDoubleOpt(optName);
  else
    return default_ret;
}

template <>
std::string readCfgOptWithDefault<std::string>(CfgParser& config, std::string optName, std::string default_ret) {
  if (config.hasOpt(optName))
    return config.readStringOpt(optName);
  else
    return default_ret;
}

float deltaPhi(float phi1, float phi2) {
  float delphi = TMath::Abs(TMath::Abs(TMath::Abs(phi1 - phi2) - TMath::Pi()) - TMath::Pi());
  return delphi;
}

std::tuple<int, float, float> getClosestJetIndexToTriggerObject(float triggerObjectEta,
                                                                float triggerObjectPhi,
                                                                std::vector<Jet>& jets,
                                                                float maxDR) {
  int closestJetIndex = -1;
  float minDR = 1024;
  float minDRjetPt = -1;
  for (unsigned int i = 0; i < jets.size(); i++) {
    Jet jet = jets.at(i);

    float dPhi = deltaPhi(jet.get_phi(), triggerObjectPhi);
    float dEta = jet.get_eta() - triggerObjectEta;

    float dR2 = dPhi * dPhi + dEta * dEta;
    float dR = std::sqrt(dR2);

    if (dR > maxDR)
      continue;

    minDR = dR;
    closestJetIndex = i;
    minDRjetPt = jet.get_pt();
  }
  //std::cout << "Jet with index ="<<closestJetIndex<<"  and pt="<<minDRjetPt<<"  is closest to trigger object with dR="<<minDR<<std::endl;
  if (minDR > maxDR) {
    closestJetIndex = -1;
  }
  return {closestJetIndex, minDR, minDRjetPt};
}

bool performTriggerMatching(
    NanoAODTree& nat,
    OutputTree& ot,
    CfgParser& config,
    std::map<std::string, std::map<std::pair<int, int>, int>>& triggerObjectAndMinNumberMap,
    std::map<std::string, std::vector<std::map<std::pair<int, int>, bool>>>& triggerObjectPerJetCount_,
    std::map<std::string, std::map<std::pair<int, int>, int>>& triggerObjectTotalCount_,
    std::vector<Jet> selected_jets) {
  bool triggerMatched = false;
  //std::vector<int> matched_jets;
  const float trgMatchingDeltaR = config.readFloatOpt("triggers::MaxDeltaR");

  // Reset all jet flags
  for (auto& triggerAndJetVector : triggerObjectPerJetCount_) {
    for (auto& jetMap : triggerAndJetVector.second) {
      for (auto& filterAndFlag : jetMap) {
        filterAndFlag.second = false;
      }
    }
  }
  // Reset all filter counts
  for (auto& triggerAndFilterMapCount : triggerObjectTotalCount_) {
    for (auto& filterAndCount : triggerAndFilterMapCount.second)
      filterAndCount.second = 0;
  }

  // Loop over all trigger objects
  for (uint trigObjIt = 0; trigObjIt < *(nat.nTrigObj); ++trigObjIt) {
    int triggerObjectId = nat.TrigObj_id.At(trigObjIt);
    int triggerFilterBitSum = nat.TrigObj_filterBits.At(trigObjIt);

    for (auto& triggerAndJetsFilterMap : triggerObjectPerJetCount_)  // One path at a time
    {
      for (auto& triggerFilter : triggerAndJetsFilterMap.second[0])  // I use the first jet map to search for filters
      {
        if (triggerObjectId != triggerFilter.first.first)
          continue;
        if ((triggerFilterBitSum >> triggerFilter.first.second) & 0x1)  //check object passes the filter
        {
          auto jetIdAndMinDeltaRandPt = getClosestJetIndexToTriggerObject(
              nat.TrigObj_eta.At(trigObjIt), nat.TrigObj_phi.At(trigObjIt), selected_jets, trgMatchingDeltaR);

          if (0) {
            std::cout << "Trigger obj. index = " << trigObjIt << "  trigger bit = " << triggerFilter.first.second
                      << "  matched with jet =" << jetIdAndMinDeltaRandPt;
            if (triggerFilter.first.second == 1)
              std::cout << "  Filter = hltBTagCaloCSVp087Triple   ";
            else if (triggerFilter.first.second == 2)
              std::cout << "  Filter = hltDoubleCentralJet90      ";
            else if (triggerFilter.first.second == 3)
              std::cout << "  Filter = hltDoublePFCentralJetLooseID90     ";
            else if (triggerFilter.first.second == 4)
              std::cout << "  Filter = hltL1sTripleJetVBFIorHTTIorDoubleJetCIorSingleJet    ";
            else if (triggerFilter.first.second == 5)
              std::cout << "  Filter = hltQuadCentralJet30    ";
            else if (triggerFilter.first.second == 6)
              std::cout << "  Filter = hltQuadPFCentralJetLooseID30    ";
            else if (triggerFilter.first.second == 10)
              std::cout << "  Filter = hltL1sQuadJetC60IorHTT380IorHTT280QuadJetIorHTT300QuadJet    ";
            else if (triggerFilter.first.second == 11)
              std::cout << "  Filter = hltBTagCaloDeepCSVp17Double     ";
            else if (triggerFilter.first.second == 12)
              std::cout << "  Filter = hltPFCentralJetLooseIDQuad30    ";
            else if (triggerFilter.first.second == 13)
              std::cout << "  Filter = hlt1PFCentralJetLooseID75     ";
            else if (triggerFilter.first.second == 14)
              std::cout << "  Filter = hlt2PFCentralJetLooseID60     ";
            else if (triggerFilter.first.second == 15)
              std::cout << "  Filter = hlt3PFCentralJetLooseID45     ";
            else if (triggerFilter.first.second == 16)
              std::cout << "  Filter = hlt4PFCentralJetLooseID40     ";
            else if (triggerFilter.first.second == 17)
              std::cout << "  Filter = hltBTagPFDeepCSV4p5Triple     ";
            else
              std::cout << " Other filter (HT?)" << std::endl;
            if (triggerObjectId == 1)
              std::cout << "   (Jet)" << std::endl;
            else if (triggerObjectId == 3)
              std::cout << "    (HT)" << std::endl;
            else
              std::cout << " " << std::endl;
          }
          int bestMatchingIndex = std::get<0>(jetIdAndMinDeltaRandPt);
          if (bestMatchingIndex >= 0) {
            triggerAndJetsFilterMap.second.at(bestMatchingIndex).at(triggerFilter.first) = true;
            //matched_jets.push_back(bestMatchingIndex);
          }
        }
      }
    }
  }  // Closes loop over trigger objects

  // Count all filters passed
  for (auto& triggerAndJetVector : triggerObjectPerJetCount_) {
    if (0)
      std::cout << "Trigger path = " << triggerAndJetVector.first << std::endl;
    for (auto& jetMap : triggerAndJetVector.second) {
      for (auto& filterAndFlag : jetMap) {
        if (0)
          std::cout << " Trigger Object ID " << filterAndFlag.first.first << " -  Filter " << filterAndFlag.first.second
                    << " -> ";
        if (filterAndFlag.second) {
          if (0)
            std::cout << "true" << std::endl;
          ++triggerObjectTotalCount_.at(triggerAndJetVector.first).at(filterAndFlag.first);
        }
        //else std::cout<< "false" << std::endl;
      }
    }
  }

  // Check if trigger matching is satisfied
  std::map<std::string, bool> triggerResult;
  for (const auto& triggerRequirements :
       any_cast<std::map<std::string, std::map<std::pair<int, int>, int>>>(triggerObjectAndMinNumberMap)) {
    triggerResult[triggerRequirements.first] = true;
    if (std::find(nat.getTrgPassed().begin(), nat.getTrgPassed().end(), triggerRequirements.first) ==
        nat.getTrgPassed().end())  // triggers not fired
    {
      triggerResult[triggerRequirements.first] = false;
      continue;
    }

    for (const auto& requiredNumberOfObjects : triggerRequirements.second)  // triggers fired
    {
      if (0) {
        std::cout << "Id = " << requiredNumberOfObjects.first.first
                  << " - Filter = " << requiredNumberOfObjects.first.second;
        std::cout << "  -> Required = " << requiredNumberOfObjects.second;
        std::cout << "  -> Passed = "
                  << triggerObjectTotalCount_[triggerRequirements.first][requiredNumberOfObjects.first];
      }
      if (triggerObjectTotalCount_[triggerRequirements.first][requiredNumberOfObjects.first] <
          requiredNumberOfObjects.second) {
        triggerResult[triggerRequirements.first] = false;  // Number of object not enough
        //std::cout << " false"<<std::endl;
      }
      //else
      //  {
      //std::cout << " true"<<std::endl;
      // }
    }
  }

  for (const auto& triggerChecked : triggerResult) {
    if (triggerChecked.second) {
      ot.userInt(triggerChecked.first + "_ObjectMatched") = 1;
      triggerMatched = true;
    }
  }
  return triggerMatched;
}

void initializeTriggerRequirements(
    CfgParser& config,
    OutputTree& ot,
    std::vector<std::string>& triggerVector,
    std::map<std::string, std::map<std::pair<int, int>, int>>& triggerObjectAndMinNumberMap,
    std::map<std::string, std::vector<std::map<std::pair<int, int>, bool>>>& triggerObjectPerJetCount_,
    std::map<std::string, std::map<std::pair<int, int>, int>>& triggerObjectTotalCount_) {
  std::vector<std::string> triggerAndNameVector = config.readStringListOpt("triggers::makeORof");
  if (triggerAndNameVector.size() == 0)
    std::cout << " No trigger listed" << std::endl;
  else
    std::cout << " Use the logical OR of the following triggers:" << std::endl;

  for (auto& trigger : triggerAndNameVector) {
    if (trigger == "")
      continue;
    std::string delimiter = ":";
    size_t pos = 0;

    std::vector<std::string> triggerTokens = split_by_delimiter(trigger, ":");
    if (triggerTokens.size() != 2)
      throw std::runtime_error("Could not parse trigger entry " + trigger + " , aborting");

    triggerVector.push_back(triggerTokens[1]);
    std::cout << "   - " << triggerTokens[0] << "  ==> " << triggerTokens[1] << std::endl;
    if (!config.hasOpt(Form("triggers::%s_ObjectRequirements", triggerTokens[0].data()))) {
      std::cout << " Config file does not contain any trigger object requirements for this trigger" << std::endl;
      continue;
    }
    std::vector<std::string> triggerObjectMatchingVector =
        config.readStringListOpt(Form("triggers::%s_ObjectRequirements", triggerTokens[0].data()));

    // Initialize the trigger object and min number for this trigger
    triggerObjectAndMinNumberMap[triggerTokens[1]] = std::map<std::pair<int, int>, int>();
    for (auto& triggerObject : triggerObjectMatchingVector) {
      std::vector<std::string> triggerObjectTokens;
      while ((pos = triggerObject.find(delimiter)) != std::string::npos) {
        triggerObjectTokens.push_back(triggerObject.substr(0, pos));
        triggerObject.erase(0, pos + delimiter.length());
      }
      triggerObjectTokens.push_back(triggerObject);  // last part splitted
      if (triggerObjectTokens.size() != 3) {
        throw std::runtime_error("** skim_ntuple : could not parse trigger entry " + triggerObject + " , aborting");
      }
      triggerObjectAndMinNumberMap[triggerTokens[1]][std::pair<int, int>(atoi(triggerObjectTokens[0].data()),
                                                                         atoi(triggerObjectTokens[1].data()))] =
          atoi(triggerObjectTokens[2].data());
    }
  }

  bool saveTrg = config.readBoolOpt("triggers::saveDecision");
  if (saveTrg) {
    for (auto& tname : triggerVector)
      ot.declareUserIntBranch(tname, 0);
  }

  int numberOfCandidates = config.readIntOpt("triggers::candidatesForTrgMatching");
  for (auto& triggerRequirements :
       any_cast<std::map<std::string, std::map<std::pair<int, int>, int>>>(triggerObjectAndMinNumberMap)) {
    ot.declareUserIntBranch(triggerRequirements.first + "_ObjectMatched", 0);
    std::map<std::pair<int, int>, bool> theTriggerFlagMap;
    std::map<std::pair<int, int>, int> theTriggerCountMap;
    for (const auto& triggerObject : triggerRequirements.second) {
      theTriggerFlagMap[triggerObject.first] = false;
      theTriggerCountMap[triggerObject.first] = 0;
    }
    triggerObjectTotalCount_[triggerRequirements.first] = theTriggerCountMap;
    for (int i = 0; i < numberOfCandidates; ++i) {
      triggerObjectPerJetCount_[triggerRequirements.first].push_back(theTriggerFlagMap);
    }
  }
  return;
}

// -----------------------------------

enum SkimTypes { kfourb, ksixb, keightb, kpass, kpresel, kttbar, kQCD, knull };

int main(int argc, char** argv) {
  const auto start_prog_t = chrono::high_resolution_clock::now();
  std::cout << "\n\033[1;33m skim_ntuple: \033[0m" << std::endl;

  //-------------------------------
  // Declare command line options
  //-------------------------------
  po::options_description desc("Skim options");
  desc.add_options()("help", "produce help message")
      // required
      ("cfg", po::value<string>()->required(), "skim config")(
          "input", po::value<string>()->required(), "input file list")(
          "output", po::value<string>()->required(), "output file LFN")
      // optional
      ("maxEvts", po::value<int>()->default_value(-1), "max number of events to process")(
          "pickEvt",
          po::value<string>()->default_value(""),
          "run on this run:lumi:event number only (for debug). Use wildcard * to match all")(
          "puWeight", po::value<string>()->default_value(""), "PU weight file name")(
          "seed",
          po::value<int>()->default_value(12345),
          "seed to be used in systematic uncertainties such as JEC, JER, etc")
      // ("kl-rew-list"  , po::value<std::vector<float>>()->multitoken()->default_value(std::vector<float>(0), "-"), "list of klambda values for reweight")
      // ("kl-rew"    , po::value<float>(),  "klambda value for reweighting")
      // ("kl-map"    , po::value<string>()->default_value(""), "klambda input map for reweighting")
      // ("kl-histo"  , po::value<string>()->default_value("hhGenLevelDistr"), "klambda histogram name for reweighting")
      ("jes-shift-syst",
       po::value<string>()->default_value("nominal"),
       "Name of the JES (scale) source uncertainty to be shifted. Usage as <name>:<up/down>. Pass -nominal- to not "
       "shift the jets")("jer-shift-syst",
                         po::value<string>()->default_value("nominal"),
                         "Name of the JER (resolution) source uncertainty to be shifted. Usage as <up/down>. Pass "
                         "-nominal- to not shift the jets")(
          "bjer-shift-syst",
          po::value<string>()->default_value("nominal"),
          "Name of the b regressed JER (resolution) source uncertainty to be shifted. Usage as <up/down>. Pass "
          "-nominal- to not shift the jets")
      // pairing variables
      // ("bbbbChoice"    , po::value<string>()->default_value("BothClosestToDiagonal"), "bbbb pairing choice")
      // ("mh1mh2"        , po::value<float>()->default_value(1.05), "Ratio Xo/Yo or 1/slope of the diagonal")
      // ("option"        , po::value<int>()->default_value(0), "Option: 0=Nominal, 1=Alternative 1, 2=Alternative 2")
      // flags
      ("is-data",
       po::value<bool>()->zero_tokens()->implicit_value(true)->default_value(false),
       "mark as a data sample (default is false)")(
          "is-signal",
          po::value<bool>()->zero_tokens()->implicit_value(true)->default_value(false),
          "mark as a signal sample (default is false)")
      //
      ("save-p4",
       po::value<bool>()->zero_tokens()->implicit_value(true)->default_value(false),
       "save the tlorentzvectors in the output")
      //
      ("no-genw-tree",
       po::value<bool>()->zero_tokens()->implicit_value(true)->default_value(false),
       "disable the storage of the genweight tree for normalizations")
      //
      ("debug",
       po::value<bool>()->zero_tokens()->implicit_value(true)->default_value(false),
       "debug this event (verbose printing)");

  po::variables_map opts;
  try {
    po::store(
        parse_command_line(argc, argv, desc, po::command_line_style::unix_style ^ po::command_line_style::allow_short),
        opts);
    if (opts.count("help")) {
      cout << desc << "\n";
      return 1;
    }
    po::notify(opts);
  } catch (po::error& e) {
    cerr << "** [ERROR] " << e.what() << endl;
    return 1;
  }

  CfgParser config;
  if (!config.init(opts["cfg"].as<string>()))
    throw std::runtime_error("No config file was provided");
  std::cout << "\n\033[1;34m Config          : \033[0m" << opts["cfg"].as<string>() << std::endl;

  const string year = config.readStringOpt("parameters::year");
  const bool is_data = opts["is-data"].as<bool>();
  const bool is_signal = (is_data ? false : opts["is-signal"].as<bool>());

  std::cout << "\033[1;34m Year            : \033[0m" << year << std::endl;
  std::cout << "\033[1;34m Sample type     : \033[0m";
  if (is_data)
    std::cout << "Data" << std::endl;
  else {
    std::cout << "Simulated";
    if (is_signal)
      std::cout << " signal" << std::endl;
    else
      std::cout << " background" << std::endl;
  }
  std::cout << "\033[1;34m Input file list : \033[0m" << opts["input"].as<string>().c_str() << std::endl;
  if (access(opts["input"].as<string>().c_str(), F_OK) == -1)
    throw std::runtime_error("The input file list does not exist.");

  const bool save_genw_tree = (is_data ? false : !opts["no-genw-tree"].as<bool>());
  const string skim_type_name = config.readStringOpt("configurations::skimType");
  std::cout << "\033[1;34m Skimming        : \033[0m" << skim_type_name << std::endl;
  const SkimTypes skim_type = (skim_type_name == "sixb"     ? ksixb
                               : skim_type_name == "fourb"  ? kfourb
                               : skim_type_name == "eightb" ? keightb
                               : skim_type_name == "pass"   ? kpass
                               : skim_type_name == "presel" ? kpresel
                               : skim_type_name == "ttbar"  ? kttbar
			       : skim_type_name == "qcd"    ? kQCD
                                                            : knull);
  if (skim_type == knull)
    throw std::runtime_error("skim type not recognized");

  ////////////////////////////////////////////////////////////////////////
  // Prepare event loop
  ////////////////////////////////////////////////////////////////////////

  // Joining all the NANOAOD input file in a TChain in order to be used like an unique three
  TChain ch("Events");
  int nfiles = su::appendFromFileList(&ch, opts["input"].as<string>());
  if (nfiles == 0)
    throw std::runtime_error("The input file list is empty.");

  const string outputFileName = opts["output"].as<string>();
  std::cout << "\033[1;34m Output file is  : \033[0m" << outputFileName << "\n" << std::endl;
  TFile outputFile(outputFileName.c_str(), "RECREATE");
  OutputTree ot(opts["save-p4"].as<bool>(),
                map<string, bool>{
                    {"muon_coll", readCfgOptWithDefault<bool>(config, "configurations::saveMuonColl", false)},
                    {"ele_coll", readCfgOptWithDefault<bool>(config, "configurations::saveEleColl", false)},
                    {"jet_coll", readCfgOptWithDefault<bool>(config, "configurations::saveJetColl", false)},
                    {"fatjet_coll", readCfgOptWithDefault<bool>(config, "configurations::saveFatJetColl", false)},
                    {"shape_brs", readCfgOptWithDefault<bool>(config, "configurations::saveShapes", false)},
                    {"dijets_coll", readCfgOptWithDefault<bool>(config, "configurations::saveDiJets", false)},
                    {"fourb_brs", (skim_type == kfourb)},
                    {"sixb_brs", (skim_type == ksixb)},
                    {"eightb_brs", (skim_type == keightb)},
                    {"ttbar_brs", (skim_type == kttbar)},
		    {"QCD_brs", (skim_type == kQCD)},
                    {"run3_brs", (skim_type == kfourb)}, // fourb is running on run3 nanoAOD 
                    {"sig_gen_brs", (is_signal)},
                    {"gen_brs", (!is_data)},
		    {"bquark_coll", (!is_data) && readCfgOptWithDefault<bool>(config, "configurations::saveGenPColl", false)},
                    {"saveTrgSF", (!is_data) && readCfgOptWithDefault<bool>(config, "triggers::saveTrgSF", false)},
                });
  NormWeightTree nwt;
  NanoAODTree nat(&ch);

  //---------------------------------------------------------------------
  // Trigger information
  //---------------------------------------------------------------------
  std::cout << "\n\033[1;33m Trigger selection: \033[0m" << std::endl;
  const bool applyTrg = config.readBoolOpt("triggers::applyTrigger");
  const bool saveTrg = config.readBoolOpt("triggers::saveDecision");
  const string trgEffFileName = config.readStringOpt("triggers::TriggerEfficiencyFileName");

  const bool saveTrgSF = (!is_data) && config.readBoolOpt("triggers::saveTrgSF");
  const bool simulateTrg = (!is_data) && applyTrg && config.readBoolOpt("triggers::SimulateTrigger");
  const bool applyTrgMatching = applyTrg && config.readBoolOpt("triggers::applyTrgObjectMatching");
  //const bool applyTurnOnCuts    = applyTrg && config.readBoolOpt("triggers::applyTurnOnCuts");

  std::cout << "\033[1;34m Apply decision  : \033[0m" << std::boolalpha << applyTrg << std::noboolalpha << std::endl;
  std::cout << "\033[1;34m Save decisions  : \033[0m" << std::boolalpha << saveTrg << std::noboolalpha << std::endl;
  std::cout << "\033[1;34m Save SFs        : \033[0m" << std::boolalpha << saveTrgSF << std::noboolalpha << std::endl;
  std::cout << "\033[1;34m Simulate        : \033[0m" << std::boolalpha << simulateTrg << std::noboolalpha << std::endl;
  std::cout << "\033[1;34m Apply matching  : \033[0m" << std::boolalpha << applyTrgMatching << std::noboolalpha
            << std::endl;

  std::vector<std::string> triggerVector;  // Contains the names of the triggers used
  std::map<std::string, std::map<std::pair<int, int>, int>>
      triggerObjectAndMinNumberMap;  // <triggerName, <filter bit, minimum number of objects> >
  std::map<std::string, std::vector<std::map<std::pair<int, int>, bool>>> triggerObjectPerJetCount_;
  std::map<std::string, std::map<std::pair<int, int>, int>> triggerObjectTotalCount_;
  initializeTriggerRequirements(
      config, ot, triggerVector, triggerObjectAndMinNumberMap, triggerObjectPerJetCount_, triggerObjectTotalCount_);

  std::vector<std::string> cleanedTrgVector;
  for (unsigned int i = 0; i < triggerVector.size(); i++) {
    bool trgExists = ch.FindBranch(triggerVector.at(i).c_str());
    if (!trgExists)
      continue;
    cleanedTrgVector.push_back(triggerVector.at(i));
  }

  // Store the trigger names
  nat.triggerReader().setTriggers(cleanedTrgVector);

  // Initialize the trigger scale factors
  TriggerEfficiencyCalculator* trgEfficiencyCalculator_{nullptr};
  if (year == "2018") {
    trgEfficiencyCalculator_ = new TriggerEfficiencyCalculator_2018(trgEffFileName, nat);
  } else if (year == "2017") {
    trgEfficiencyCalculator_ = new TriggerEfficiencyCalculator_2017(trgEffFileName, nat);
  } else {
    throw std::invalid_argument("No trigger efficiency file exists for the year requested");
  }
  if (simulateTrg)
    trgEfficiencyCalculator_->simulateTrigger(&ot);
  //trgEfficiencyCalculator_ -> applyTurnOnCut(applyTurnOnCuts);

  //----------------------------------
  // PU weights
  //----------------------------------
  std::string pu_weight_file;
  if (!is_data) {
    if (opts["puWeight"].as<string>().size() != 0) {  // a valid option is passed from cmd line
      pu_weight_file = opts["puWeight"].as<string>();
    } else {
      pu_weight_file = readCfgOptWithDefault<string>(config, "parameters::PUweightFile", "");
    }
    std::cout << "\n\033[1;33m PU reweighting: \033[0m" << std::endl;
    std::cout << "\033[1;34m PU Weights : \033[0m" << pu_weight_file << "\n" << std::endl;
  }

  map<string, string> pu_data{
      {"filename", pu_weight_file},
      {"name_PU_w", "PUweights"},
      {"name_PU_w_up", "PUweights_up"},
      {"name_PU_w_do", "PUweights_down"},
  };

  // // just a test
  // nwt.add_weight("test1", {"test1_up", "test1_down"});
  // nwt.add_weight("test2", {"test2_A", "test2_B", "test2_C"});
  // nwt.add_weight("test3", {});

  //---------------------------------------------------------------------
  // All pre-running configurations (corrections, methods from cfg, etc)
  //---------------------------------------------------------------------
  jsonLumiFilter jlf;
  if (is_data)
    jlf.loadJSON(config.readStringOpt(
        "data::lumimask"));  // just read the info for data, so if I just skim MC I'm not forced to parse a JSON

  Timer loop_timer;
  Skim_functions* skf;
  switch (skim_type) {
    case kfourb:
      skf = new FourB_functions();
      break;
    case ksixb:
      skf = new SixB_functions();
      break;
    case keightb:
      skf = new EightB_functions();
      break;
    case kpresel:
      skf = new SixB_functions();
      break;
    case kttbar:
      skf = new TTBar_functions();
      break;
    default:
      skf = new Skim_functions();
      break;
  }
  skf->Print();
  skf->set_timer(&loop_timer);
  // skf->set_debug(true);

  const std::vector<double> btag_WPs = config.readDoubleListOpt("configurations::bTagWPDef");
  const int nMinBtag = config.readIntOpt("configurations::nMinBtag");
  const int bTagWP = config.readIntOpt("configurations::bTagWP");
  skf->set_btag_WPs(config.readDoubleListOpt("configurations::bTagWPDef"));

  cout << "[INFO] ... events must contain >= " << nMinBtag << " jets passing WP (0:L, 1:M, 2:T) : " << bTagWP << endl;
  cout << "[INFO] ... the WPs are: (L/M/T) : " << btag_WPs.at(0) << "/" << btag_WPs.at(1) << "/" << btag_WPs.at(2)
       << endl;

  BtagSF btsf;
  if (!is_data) {
    string btsffile = config.readStringOpt("parameters::DeepJetScaleFactorFile");
    btsf.init_reader("DeepJet", btsffile);
    btsf.set_WPs(btag_WPs.at(0), btag_WPs.at(1), btag_WPs.at(2));
  }

  bool blind = false;
  if (config.hasOpt("configurations::blinded"))
    blind = config.readBoolOpt("configurations::blinded");

  // --------------------------------------------------------------
  JetTools jt;

  string jes_shift = opts["jes-shift-syst"].as<string>();
  bool do_jes_shift = (jes_shift != "nominal");
  cout << "[INFO] ... shifting jet energy scale? " << std::boolalpha << do_jes_shift << std::noboolalpha << endl;
  bool dir_jes_shift_is_up;
  if (do_jes_shift && !is_data) {
    string JECFileName = config.readStringOpt("parameters::JECFileName");
    auto tokens = split_by_delimiter(opts["jes-shift-syst"].as<string>(), ":");
    if (tokens.size() != 2)
      throw std::runtime_error(string("Cannot parse the jes shift name : ") + opts["jes-shift-syst"].as<string>());
    string jes_syst_name = tokens.at(0);
    dir_jes_shift_is_up =
        (tokens.at(1) == "up"     ? true
         : tokens.at(1) == "down" ? false
                                  : throw std::runtime_error(string("Could not parse jes direction ") + tokens.at(1)));
    cout << "       ... jec file name           : " << JECFileName << endl;
    cout << "       ... jet energy scale syst   : " << jes_syst_name << endl;
    cout << "       ... jet energy scale is up? : " << std::boolalpha << dir_jes_shift_is_up << std::noboolalpha
         << endl;
    jt.init_jec_shift(JECFileName, jes_syst_name);
  }

  // FIXME: block below to be run only if !is_data?
  string JERScaleFactorFile = config.readStringOpt("parameters::JERScaleFactorFile");
  string JERResolutionFile = config.readStringOpt("parameters::JERResolutionFile");
  const int rndm_seed = opts["seed"].as<int>();
  cout << "[INFO] ... initialising JER corrector with the following parameters" << endl;
  cout << "       ... SF file         : " << JERScaleFactorFile << endl;
  cout << "       ... resolution file : " << JERResolutionFile << endl;
  cout << "       ... rndm seed       : " << rndm_seed << endl;
  jt.init_smear(JERScaleFactorFile, JERResolutionFile, rndm_seed);

  cout << "[INFO] ... jet resolution syst is    : " << opts["jer-shift-syst"].as<string>() << endl;
  cout << "[INFO] ... b regr resolution syst is : " << opts["bjer-shift-syst"].as<string>() << endl;
  const Variation jer_var = string_to_jer_variation(opts["jer-shift-syst"].as<string>());
  const Variation bjer_var = string_to_jer_variation(opts["bjer-shift-syst"].as<string>());

  // ------------------------------------------------------------------
  skf->initialize_params_from_cfg(config);
  skf->initialize_functions(outputFile);

  ////////////////////////////////////////////////////////////////////////
  // Execute event loop
  ////////////////////////////////////////////////////////////////////////
  const int maxEvts = opts["maxEvts"].as<int>();
  if (maxEvts >= 0)
    cout << "[INFO] ... running on : " << maxEvts << " events" << endl;

  // single Ev debug
  std::vector<std::string> RunLumiEvtStr = split_by_delimiter(opts["pickEvt"].as<string>(), ":");
  const int pickRunNr = (RunLumiEvtStr.size() != 3    ? -1
                         : RunLumiEvtStr.at(0) == "*" ? -1
                                                      : std::stoi(RunLumiEvtStr.at(0)));
  const int pickLumiNr = (RunLumiEvtStr.size() != 3    ? -1
                          : RunLumiEvtStr.at(1) == "*" ? -1
                                                       : std::stoi(RunLumiEvtStr.at(1)));
  const long long pickEvtNr = (RunLumiEvtStr.size() != 3    ? -1
                               : RunLumiEvtStr.at(2) == "*" ? -1
                                                            : std::stoll(RunLumiEvtStr.at(2)));
  const bool doPickEvt = (pickEvtNr >= 0 || pickRunNr >= 0 || pickLumiNr >= 0);
  if (RunLumiEvtStr.size() > 0)
    cout << "[INFO] ... running on a single run:lumi:event for debug: " << opts["pickEvt"].as<string>()
         << " --> run:lumi:evt " << pickRunNr << ":" << pickLumiNr << ":" << pickEvtNr << endl;
  // if (RunLumiEvtStr.size() > 0 && RunLumiEvtStr.size() != 3){
  //   cout << "[ERROR] ... pickEvt string must be formatted as evt:run:lumi " << endl;
  // }

  const bool debug = opts["debug"].as<bool>();
  if (debug)
    skf->set_debug(debug);

  const auto start_loop_t = chrono::high_resolution_clock::now();

  Cutflow cutflow;
  Cutflow cutflow_Unweighted("h_cutflow_unweighted", "Unweighted selection cutflow");
  HistoCollection histograms;

  for (int iEv = 0; true; ++iEv) {
    if (maxEvts >= 0 && iEv >= maxEvts)
      break;

    loop_timer.start_lap();

    if (!nat.Next())
      break;
    if (iEv % 1000 == 0 || debug) {
      cout << "... processing event " << iEv << endl;
      // auto bsize  = ot.getTree()->GetBranch("Run")->GetBasketSize();
      // cout << "... tree basket size (branch Run) : " << bsize  << endl;
    }

    // use the tree content to initialise weight tree in the first event
    if (iEv == 0 && !is_data && save_genw_tree) {
      nwt.init_weights(nat, pu_data);  // get the syst structure from nanoAOD
      su::init_gen_weights(ot, nwt);   // and forward it to the output tree
    }

    // pick a specific event for debug
    if (doPickEvt &&
        ((pickEvtNr >= 0 && (long long)*(nat.event) != pickEvtNr) || (pickRunNr >= 0 && (int)*(nat.run) != pickRunNr) ||
         (pickLumiNr >= 0 && (long long)*(nat.luminosityBlock) != pickLumiNr)))
      continue;

    // apply certification json file
    if (is_data && !jlf.isValid(*nat.run, *nat.luminosityBlock)) {
      continue;  // not a valid lumi
    }

    EventInfo ei;
    ot.clear();
    loop_timer.click("Input read");

    //==========================================================
    // Normalization weights: to be saved before any filtering
    //==========================================================
    if (!is_data && save_genw_tree) {
      nwt.read_weights(nat);
      // example to fill user weights
      // auto& w1 = nwt.get_weight("test1");
      // auto& w2 = nwt.get_weight("test2");
      // auto& w3 = nwt.get_weight("test3");
      // w1.w = iEv;
      // w2.w = 10*iEv;
      // w3.w = 100*iEv;
      // w1.syst_val = {iEv + 1., iEv - 1.};
      // w2.syst_val = {10. * iEv - 10, 10. * iEv - 20, 10. * iEv - 30};
      // w3.syst_val = {};
      nwt.fill();
      loop_timer.click("Norm weight read + fill");
    }

    // ------- events can start be filtered from here (after saving all gen weights)
    cutflow.add("total", nwt);
    cutflow_Unweighted.add("total");

    //====================================
    // Apply trigger
    //====================================
    if (applyTrg && !(nat.getTrgOr()))
      continue;
    cutflow.add("trigger", nwt);
    cutflow_Unweighted.add("trigger");
    std::vector<std::string> listOfPassedTriggers = nat.getTrgPassed();
    if (saveTrg) {
      for (auto& t : listOfPassedTriggers)
        ot.userInt(t) = 1;
    }
    loop_timer.click("Trigger");

    //==================================
    // Save global event info
    //==================================
    skf->copy_event_info(nat, ei, !is_data);
    loop_timer.click("Global info");

    //==================================
    // Apply METFilters
    //==================================
    bool bMETFilters = *nat.Flag_goodVertices && *nat.Flag_globalSuperTightHalo2016Filter &&
                       *nat.Flag_HBHENoiseFilter && *nat.Flag_HBHENoiseIsoFilter &&
                       *nat.Flag_EcalDeadCellTriggerPrimitiveFilter && *nat.Flag_BadPFMuonFilter &&
                       *nat.Flag_eeBadScFilter && (*nat.Flag_ecalBadCalibFilter || (year == "2016"));
    bool applyMETFilters = config.readBoolOpt("configurations::applyMETFilters");
    if (applyMETFilters) {
      if (!bMETFilters)
        continue;
      loop_timer.click("MET Filters");
      cutflow.add("met filters", nwt);
      cutflow_Unweighted.add("met filters");
    }

    //==================================
    // Apply muon selection or veto
    //==================================
    std::vector<Muon> selected_muons = skf->select_muons(config, nat, ei);
    ei.n_muon = selected_muons.size();
    ei.muon_list = selected_muons;
    histograms.get("n_mu", ";N Muons;Events", 10, 0, 10).Fill(selected_muons.size(), nwt);

    bool applyMuonVeto = config.readBoolOpt("configurations::applyMuonVeto");
    bool applyMuonSelection = config.readBoolOpt("configurations::applyMuonSelection");
    if (applyMuonVeto) {
      if (selected_muons.size() != 0)
        continue;
      cutflow.add("#mu veto", nwt);
      cutflow_Unweighted.add("#mu veto");
      loop_timer.click("#mu veto");
    } else if (applyMuonSelection) {
      const DirectionalCut<int> cfg_nMuons(config, "configurations::nMuonsCut");
      if (!cfg_nMuons.passedCut(selected_muons.size()))
        continue;
      cutflow.add("#mu selection", nwt);
      cutflow_Unweighted.add("#mu selection");
      loop_timer.click("#mu selection");
    }

    //=====================================
    // Apply electron selection or veto
    //=====================================
    std::vector<Electron> selected_electrons = skf->select_electrons(config, nat, ei);
    ei.n_ele = selected_electrons.size();
    ei.ele_list = selected_electrons;
    histograms.get("n_ele", ";N Electrons;Events", 10, 0, 10).Fill(selected_electrons.size(), nwt);

    bool applyEleVeto = config.readBoolOpt("configurations::applyEleVeto");
    bool applyEleSelection = config.readBoolOpt("configurations::applyEleSelection");
    if (applyEleVeto) {
      if (selected_electrons.size() != 0)
        continue;
      cutflow.add("e veto", nwt);
      cutflow_Unweighted.add("e veto");
      loop_timer.click("e veto");
    } else if (applyEleSelection) {
      const DirectionalCut<int> cfg_nElectrons(config, "configurations::nEleCut");
      if (!cfg_nElectrons.passedCut(selected_electrons.size()))
        continue;
      cutflow.add("e selection", nwt);
      cutflow_Unweighted.add("e selection");
      loop_timer.click("e selection");
    }

    bool saveFatJets = readCfgOptWithDefault<bool>(config, "configurations::saveFatJetColl", false);

    //======================================
    // Save signal specific GEN info
    //======================================
    if (is_signal) {
      skf->select_gen_particles(nat, ei);         // find gen level X, Y, H, b
      skf->match_genbs_to_genjets(nat, ei);       // match the b quarks found above to the genjets
      skf->match_genbs_genjets_to_reco(nat, ei);  // match the genjets found above to the reco jets

      if (saveFatJets) {
        skf->match_genbs_to_genfatjets(nat, ei);       // match the b quarks found above to the gen fatjets
        skf->match_genbs_genfatjets_to_reco(nat, ei);  // match the gen fatjets found above to the reco fatjets
      }
      loop_timer.click("Signal gen level");
    }

    //======================================
    // Jet Selection
    //======================================
    std::vector<Jet> all_jets = skf->get_all_jets(nat);  // dump all nanoAOD jets into a vector<Jet>
    ei.nfound_all = skf->n_gjmatched_in_jetcoll(nat, ei, all_jets);
    ei.nfound_all_h = skf->n_ghmatched_in_jetcoll(nat, ei, all_jets);
    loop_timer.click("All jets copy");

    if (!is_data) {
      if (do_jes_shift)
        all_jets = jt.jec_shift_jets(nat, all_jets, dir_jes_shift_is_up);  // apply JEC scale shift to jets
      all_jets = jt.smear_jets(nat, all_jets, jer_var, bjer_var);          // apply JER smearing to jets
      loop_timer.click("JEC + JER");
    }

    // Apply preselections to jets (min pT / max eta / PU ID / PF ID)
    std::vector<Jet> presel_jets = skf->preselect_jets(nat, ei, all_jets);
    histograms.get("n_presel_jet", ";N Preselected Jets;Events", 20, 0, 20).Fill(presel_jets.size(), nwt);

    if (is_signal) {
      skf->match_signal_recojets(nat, ei, presel_jets);
      std::vector<GenJet> all_genjets = skf->get_all_genjets(nat);
      skf->match_genjets_to_reco(nat, ei, all_genjets, presel_jets);
      skf->match_signal_genjets(nat, ei, all_genjets);
      ei.genjet_list = all_genjets;
    }

    ei.n_jet = presel_jets.size();
    ei.jet_list = presel_jets;

    ei.nfound_presel = skf->n_gjmatched_in_jetcoll(nat, ei, presel_jets);
    //std::cout << "Number of selected jets found matched with GEN-level objects = "<<ei.nfound_presel<<std::endl;
    ei.nfound_presel_h = skf->n_ghmatched_in_jetcoll(nat, ei, presel_jets);
    //std::cout << "Number of selected jets found matched to Higgs objects = "<<ei.nfound_presel_h<<std::endl;

    loop_timer.click("Jet selection");
    if (debug)
      dumpObjColl(presel_jets, "==== PRESELECTED JETS ===");

    // Save event PFHT
    ei.PFHT = skf->getPFHT(nat, ei);

    //=================================
    // Fatjet selection
    //=================================
    if (saveFatJets) {
      std::vector<FatJet> all_fatjets = skf->get_all_fatjets(nat);
      ei.n_fatjet = all_fatjets.size();
      ei.fatjet_list = all_fatjets;
      loop_timer.click("FatJet selection");
      if (is_signal) {
        std::vector<GenJetAK8> all_genfatjets = skf->get_all_genfatjets(nat);
        ei.n_genfatjet = all_genfatjets.size();
        ei.genfatjet_list = all_genfatjets;
      }
    }

    //=================================
    // Apply analysis-specific skims
    //=================================
    if (skim_type == keightb) {
      if (presel_jets.size() < 8)
        continue;
      cutflow.add("npresel_jets>=8", nwt);
      cutflow_Unweighted.add("npresel_jets>=8");

      // std::vector<DiJet> dijets = skf->make_dijets(nat, ei, presel_jets);
      // ei.dijet_list = dijets;

      std::vector<Jet> selected_jets = skf->select_jets(nat, ei, presel_jets);
      loop_timer.click("Eight B Selection");

      if (selected_jets.size() < 8)
        continue;

      if (readCfgOptWithDefault<bool>(config, "configurations::saveSelected", false))
        ei.jet_list = selected_jets;

      cutflow.add("nselect_jets>=8", nwt);
      cutflow_Unweighted.add("nselect_jets>=8");

      //========================================
      // Apply trigger matching
      //========================================
      if (applyTrgMatching) {
        bool triggerMatched = performTriggerMatching(nat,
                                                     ot,
                                                     config,
                                                     triggerObjectAndMinNumberMap,
                                                     triggerObjectPerJetCount_,
                                                     triggerObjectTotalCount_,
                                                     selected_jets);
        if (!triggerMatched)
          continue;
        cutflow.add("Trigger matching", nwt);
        cutflow_Unweighted.add("Trigger matching");
        loop_timer.click("Trigger object - offline object matching");
      }

      //=======================================
      // Calculate trigger scale factor
      //=======================================
      if (saveTrgSF) {
        if (trgEfficiencyCalculator_ != nullptr) {
          auto triggerScaleFactorDataAndMonteCarloEfficiency =
              trgEfficiencyCalculator_->getScaleFactorDataAndMonteCarloEfficiency(selected_jets);
          ot.triggerScaleFactor = std::get<0>(std::get<0>(triggerScaleFactorDataAndMonteCarloEfficiency));
          ot.triggerDataEfficiency = std::get<0>(std::get<1>(triggerScaleFactorDataAndMonteCarloEfficiency));
          ot.triggerMcEfficiency = std::get<0>(std::get<2>(triggerScaleFactorDataAndMonteCarloEfficiency));
          ot.triggerScaleFactorUp = std::get<1>(std::get<0>(triggerScaleFactorDataAndMonteCarloEfficiency));
          ot.triggerDataEfficiencyUp = std::get<1>(std::get<1>(triggerScaleFactorDataAndMonteCarloEfficiency));
          ot.triggerMcEfficiencyUp = std::get<1>(std::get<2>(triggerScaleFactorDataAndMonteCarloEfficiency));
          ot.triggerScaleFactorDown = std::get<2>(std::get<0>(triggerScaleFactorDataAndMonteCarloEfficiency));
          ot.triggerDataEfficiencyDown = std::get<2>(std::get<1>(triggerScaleFactorDataAndMonteCarloEfficiency));
          ot.triggerMcEfficiencyDown = std::get<2>(std::get<2>(triggerScaleFactorDataAndMonteCarloEfficiency));
          if (0) {
            std::cout << "\nTrigger scale factor = " << ot.triggerScaleFactor << std::endl;
            std::cout << "Data Efficiency      = " << ot.triggerDataEfficiency << std::endl;
            std::cout << "MC Efficiency        = " << ot.triggerMcEfficiency << std::endl;
          }
        }
      }

      //================================================
      // Proceed with the jets pairing
      //================================================
      skf->pair_jets(nat, ei, selected_jets);
      skf->compute_seljets_btagmulti(nat, ei);
      loop_timer.click("Eight b jet pairing");

      if (is_signal) {
        skf->compute_seljets_genmatch_flags(nat, ei);
        loop_timer.click("Eight b pairing flags");
      }
      skf->compute_event_shapes(nat, ei, selected_jets);
      loop_timer.click("Event shapes calculation");
    } else if (skim_type == kfourb) {
      // Marina
      std::cout << "" << std::endl;
    } else if (skim_type == ksixb) {
      // Preselected jets are all jets in the event sorted in pT
      const DirectionalCut<int> cfg_nJets(config, "presel::njetsCut");
      if (!cfg_nJets.passedCut(presel_jets.size()))
        continue;
      cutflow.add("selected jets >= 6", nwt);
      cutflow_Unweighted.add("selected jets >= 6");

      //=============================================
      // Jets for pairing selection (either 6 or 0)
      //=============================================
      std::vector<Jet> selected_jets = skf->select_jets(nat, ei, presel_jets);
      if (selected_jets.size() < 6)
        continue;

      if (readCfgOptWithDefault<bool>(config, "configurations::saveSelected", false))
        ei.jet_list = selected_jets;

      cutflow.add("Jets for pairing selection", nwt);
      cutflow_Unweighted.add("Jets for pairing selection");

      loop_timer.click("Six b jet selection");

      ei.nfound_select = skf->n_gjmatched_in_jetcoll(nat, ei, selected_jets);
      ei.nfound_select_h = skf->n_ghmatched_in_jetcoll(nat, ei, selected_jets);

      if (debug) {
        dumpObjColl(selected_jets, "==== SELECTED 6b JETS ===");
      }

      if (0) {
        std::cout << "\n SELECTED JETS:" << std::endl;
        for (unsigned int ij = 0; ij < selected_jets.size(); ij++) {
          std::cout << "jet = " << ij << "   pT=" << selected_jets.at(ij).get_pt()
                    << "    b-tag=" << selected_jets.at(ij).get_btag() << std::endl;
        }
      }

      //========================================
      // Apply trigger matching
      //========================================
      if (applyTrgMatching) {
        bool triggerMatched = performTriggerMatching(nat,
                                                     ot,
                                                     config,
                                                     triggerObjectAndMinNumberMap,
                                                     triggerObjectPerJetCount_,
                                                     triggerObjectTotalCount_,
                                                     selected_jets);
        if (!triggerMatched)
          continue;
        cutflow.add("Trigger matching", nwt);
        cutflow_Unweighted.add("Trigger matching");
        loop_timer.click("Trigger object - offline object matching");
      }

      //=======================================
      // Calculate trigger scale factor
      //=======================================
      if (saveTrgSF) {
        if (trgEfficiencyCalculator_ != nullptr) {
          auto triggerScaleFactorDataAndMonteCarloEfficiency =
              trgEfficiencyCalculator_->getScaleFactorDataAndMonteCarloEfficiency(selected_jets);
          ot.triggerScaleFactor = std::get<0>(std::get<0>(triggerScaleFactorDataAndMonteCarloEfficiency));
          ot.triggerDataEfficiency = std::get<0>(std::get<1>(triggerScaleFactorDataAndMonteCarloEfficiency));
          ot.triggerMcEfficiency = std::get<0>(std::get<2>(triggerScaleFactorDataAndMonteCarloEfficiency));
          ot.triggerScaleFactorUp = std::get<1>(std::get<0>(triggerScaleFactorDataAndMonteCarloEfficiency));
          ot.triggerDataEfficiencyUp = std::get<1>(std::get<1>(triggerScaleFactorDataAndMonteCarloEfficiency));
          ot.triggerMcEfficiencyUp = std::get<1>(std::get<2>(triggerScaleFactorDataAndMonteCarloEfficiency));
          ot.triggerScaleFactorDown = std::get<2>(std::get<0>(triggerScaleFactorDataAndMonteCarloEfficiency));
          ot.triggerDataEfficiencyDown = std::get<2>(std::get<1>(triggerScaleFactorDataAndMonteCarloEfficiency));
          ot.triggerMcEfficiencyDown = std::get<2>(std::get<2>(triggerScaleFactorDataAndMonteCarloEfficiency));
          if (0) {
            std::cout << "Trigger scale factor = " << ot.triggerScaleFactor << std::endl;
            std::cout << "Data Efficiency      = " << ot.triggerDataEfficiency << std::endl;
            std::cout << "MC Efficiency        = " << ot.triggerMcEfficiency << std::endl;
          }
        }
      }

      //================================================
      // Proceed with the pairing of the 6 selected jets
      //=================================================
      skf->pair_jets(nat, ei, selected_jets);
      loop_timer.click("Six b jet pairing");

      if (is_signal) {
        skf->compute_seljets_genmatch_flags(nat, ei);
        loop_timer.click("Six b pairing flags");
      }
      skf->compute_event_shapes(nat, ei, selected_jets);
      loop_timer.click("Event shapes calculation");
    }  // Closes sixb skimming
    else if ( skim_type == kttbar ) {
      if (presel_jets.size() < 6)
        continue;
      cutflow.add("npresel_jets>=6", nwt);
      cutflow_Unweighted.add("npresel_jets>=6");
      
      std::vector<Jet> selected_jets = skf->select_jets(nat, ei, presel_jets);
      ei.nfound_select = skf->n_gjmatched_in_jetcoll(nat, ei, selected_jets);
      loop_timer.click("TT Bar Selection");

      if (selected_jets.size() < 6)
        continue;

      if (readCfgOptWithDefault<bool>(config, "configurations::saveSelected", false))
        ei.jet_list = selected_jets;

      cutflow.add("nselect_jets>=6", nwt);
      cutflow_Unweighted.add("nselect_jets>=6");
    }
    else if (skim_type == kQCD)
      {
	// Gen-information
	std::vector<GenJet> GenJets = skf->get_all_genjets(nat);
	std::vector<GenPart> bQuarks = skf->select_b_quarks(nat, ei);
	std::vector<GenPart*> bQuarks_ptr;
	for (unsigned int b=0; b<bQuarks.size(); b++)
	  {
	    bQuarks_ptr.push_back(&bQuarks.at(b));
	  }
	// Save only the gen-level b-quarks
	ei.genpb_list  = bQuarks;
	// Save all gen-level jets
	ei.genjet_list = GenJets;

	std::vector<GenPart*> matched_quarks;
	std::vector<GenJet> matched_genjets;
	skf->GetMatchedPairs(0.4, bQuarks_ptr, GenJets, matched_quarks, matched_genjets);
	std::vector<Jet> matched_recojets;
	for (unsigned int j=0; j<presel_jets.size(); j++)
	  {
	    Jet jet = presel_jets.at(j);
	    int genJetIdx = get_property(jet, Jet_genJetIdx);
	    for (unsigned int igen = 0; igen < matched_genjets.size(); igen++)
	      {
		GenJet genjet = matched_genjets.at(igen);
		int genJet_idx = genjet.getIdx();
		if (genJetIdx == genJet_idx) matched_recojets.push_back(jet);
	      }
	  }

	loop_timer.click("QCD gen-level matching");

	// Do something if needed for the matched objects (matched_quarks, matched_genjets, matched_recojets)
	// ...

      } // kQCD skim
    if (blind && is_data && skf->is_blinded(nat, ei, is_data))
      continue;

    if (!is_data && save_genw_tree) {
      su::copy_gen_weights(ot, nwt);
      loop_timer.click("Read and copy gen weights");
    }
    su::fill_output_tree(ot, nat, ei);
    loop_timer.click("Output tree fill");
  }  // Closes Event Loop

  const auto end_loop_t = chrono::high_resolution_clock::now();
  outputFile.cd();

  // Write cutflow histograms to file
  cutflow.write(outputFile);
  cutflow_Unweighted.write(outputFile);
  histograms.write(outputFile);
  ot.write();
  if (!is_data)
    nwt.write();

  // timing statistics
  const auto end_prog_t = chrono::high_resolution_clock::now();
  cout << endl;
  cout << "[INFO] : summary of skim loop execution time" << endl;
  loop_timer.print_summary();
  cout << endl;
  cout << "[INFO] : total elapsed time : "
       << chrono::duration_cast<chrono::milliseconds>(end_prog_t - start_prog_t).count() / 1000. << " s" << endl;
  cout << "       : startup time       : "
       << chrono::duration_cast<chrono::milliseconds>(start_loop_t - start_prog_t).count() / 1000. << " s" << endl;
  cout << "       : loop time          : "
       << chrono::duration_cast<chrono::milliseconds>(end_loop_t - start_loop_t).count() / 1000. << " s" << endl;
  cout << "       : post-loop time     : "
       << chrono::duration_cast<chrono::milliseconds>(end_prog_t - end_loop_t).count() / 1000. << " s" << endl;
  cout << endl;
  cout << "[INFO] ... skim finished" << endl;
}

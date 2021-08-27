// skim_ntuple.exe --input input/PrivateMC_2018/NMSSM_XYH_YToHH_6b_MX_600_MY_400.txt --cfg config/skim_ntuple_2018.cfg  --output prova.root --is-signal
// skim_ntuple.exe --input input/Run2_UL/2018/TTJets.txt --cfg config/skim_ntuple_2018_ttbar.cfg  --output prova_ttbar.root
// skim_ntuple.exe --input input/Run2_UL/2018/SingleMuon_Run2.txt --cfg config/skim_ntuple_2018_ttbar.cfg  --output prova_singlemu_ttbarskim.root --is-data

#include <iostream>
#include <string>
#include <iomanip>
#include <any>
#include <chrono>

#include <boost/program_options.hpp>
namespace po = boost::program_options;

#include "CfgParser.h"
#include "NanoAODTree.h"
#include "NormWeightTree.h"
#include "SkimUtils.h"
namespace su = SkimUtils;

#include "OutputTree.h"
#include "jsonLumiFilter.h"

#include "SixB_functions.h"
#include "JetTools.h"
#include "BtagSF.h"
#include "EventShapeCalculator.h"
#include "Cutflow.h"
#include "EvalNN.h"

#include "Timer.h"

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

int main(int argc, char** argv)
{
  cout << "[INFO] ... starting program" << endl;
  const auto start_prog_t = chrono::high_resolution_clock::now();

  ////////////////////////////////////////////////////////////////////////
  // Declare command line options
  ////////////////////////////////////////////////////////////////////////
    
  po::options_description desc("Skim options");
  desc.add_options()
    ("help", "produce help message")
    // required
    ("cfg"   , po::value<string>()->required(), "skim config")
    ("input" , po::value<string>()->required(), "input file list")
    ("output", po::value<string>()->required(), "output file LFN")
    // optional
    // ("xs"        , po::value<float>(), "cross section [pb]")
    ("maxEvts"   , po::value<int>()->default_value(-1), "max number of events to process")
    ("puWeight"  , po::value<string>()->default_value(""), "PU weight file name")
    ("seed"      , po::value<int>()->default_value(12345), "seed to be used in systematic uncertainties such as JEC, JER, etc")
    // ("kl-rew-list"  , po::value<std::vector<float>>()->multitoken()->default_value(std::vector<float>(0), "-"), "list of klambda values for reweight")
    // ("kl-rew"    , po::value<float>(),  "klambda value for reweighting")
    // ("kl-map"    , po::value<string>()->default_value(""), "klambda input map for reweighting")
    // ("kl-histo"  , po::value<string>()->default_value("hhGenLevelDistr"), "klambda histogram name for reweighting")
    ("jes-shift-syst",  po::value<string>()->default_value("nominal"), "Name of the JES (scale) source uncertainty to be shifted. Usage as <name>:<up/down>. Pass -nominal- to not shift the jets")
    ("jer-shift-syst",  po::value<string>()->default_value("nominal"), "Name of the JER (resolution) source uncertainty to be shifted. Usage as <up/down>. Pass -nominal- to not shift the jets")
    ("bjer-shift-syst", po::value<string>()->default_value("nominal"), "Name of the b regressed JER (resolution) source uncertainty to be shifted. Usage as <up/down>. Pass -nominal- to not shift the jets")
    // pairing variables
    // ("bbbbChoice"    , po::value<string>()->default_value("BothClosestToDiagonal"), "bbbb pairing choice")
    // ("mh1mh2"        , po::value<float>()->default_value(1.05), "Ratio Xo/Yo or 1/slope of the diagonal") 
    // ("option"        , po::value<int>()->default_value(0), "Option: 0=Nominal, 1=Alternative 1, 2=Alternative 2") 
    // flags
    ("is-data",       po::value<bool>()->zero_tokens()->implicit_value(true)->default_value(false), "mark as a data sample (default is false)")
    ("is-signal",     po::value<bool>()->zero_tokens()->implicit_value(true)->default_value(false), "mark as a HH signal sample (default is false)")
    //
    ("save-p4",       po::value<bool>()->zero_tokens()->implicit_value(true)->default_value(false), "save the tlorentzvectors in the output")
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

  const bool is_signal = (is_data ? false : opts["is-signal"].as<bool>());
  cout << "[INFO] ... is a signal sample? " << std::boolalpha << is_signal << std::noboolalpha << endl;

  CfgParser config;
  if (!config.init(opts["cfg"].as<string>())){
    cerr << "** [ERROR] no config file was provuded" << endl;
    return 1;
  }
  cout << "[INFO] ... using config file " << opts["cfg"].as<string>() << endl;

  enum SkimTypes
    {
      ksixb,
      kttbar,
      kshapecr,
      khiggscr,
      kqcd,
      knull
    };

  string skim_type_name = config.readStringOpt("configurations::skimType");
  cout << "[INFO] ... skim type " << skim_type_name << endl;
  const SkimTypes skim_type = (
                               skim_type_name == "sixb"    ? ksixb    :
                               skim_type_name == "ttbar"   ? kttbar   :
                               skim_type_name == "shapecr" ? kshapecr :
                               skim_type_name == "higgscr" ? khiggscr :
                               skim_type_name == "qcd"     ? kqcd     :
                               knull
                               );
  if (skim_type == knull)
    throw std::runtime_error("skim type not recognized");

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

  // The TChain is passed to the NanoAODTree_SetBranchImpl to parse all the branches
  NanoAODTree nat (&ch);

  ////////////////////////////////////////////////////////////////////////
  // Trigger information
  ////////////////////////////////////////////////////////////////////////

  cout << "[INFO] ... loading " << config.readStringListOpt("triggers::makeORof").size() << " triggers" << endl;

  const bool apply_trigger     = config.readBoolOpt("triggers::applyTrigger");
  const bool save_trg_decision = config.readBoolOpt("triggers::saveDecision");
  cout << "[INFO] ... is the OR decision of these triggers applied? " << std::boolalpha << apply_trigger << std::noboolalpha << endl;
  cout << "[INFO] ... will save the trigger decision? " << std::boolalpha << save_trg_decision << std::noboolalpha << endl;

  // std::vector<std::string> triggerAndNameVector;
  // if(apply_trigger) triggerAndNameVector = config.readStringListOpt("triggers::makeORof");
  // <triggerName , < objectBit, minNumber> >
  // std::map<std::string, std::map< std::pair<int,int>, int > > triggerObjectAndMinNumberMap;

  std::vector<std::string> triggerAndNameVector = config.readStringListOpt("triggers::makeORof");
  std::vector<std::string> triggerVector;

  cout << "[INFO] ... listing the triggers applied" << endl;
  for (auto & trigger : triggerAndNameVector)
    {
      if(trigger == "")
	continue;
        
      std::vector<std::string> triggerTokens = split_by_delimiter(trigger, ":");
      if (triggerTokens.size() != 2)
	throw std::runtime_error("** skim_ntuple : could not parse trigger entry " + trigger + " , aborting");

      triggerVector.push_back(triggerTokens[1]);
      cout << "   - " << triggerTokens[0] << "  ==> " << triggerTokens[1] << endl;

      // if(!config.hasOpt( Form("triggers::%s_ObjectRequirements",triggerTokens[0].data()) ))
      // {
      //     cout<<Form("triggers::%s_ObjectRequirements",triggerTokens[0].data())<<std::endl;
      //     cout<<"Trigger "<< triggerTokens[1] <<" does not have ObjectRequirements are not defined";
      //     continue;
      // }

      // triggerObjectAndMinNumberMap[triggerTokens[1]] = std::map< std::pair<int,int>, int>();   

      // std::vector<std::string> triggerObjectMatchingVector = config.readStringListOpt(Form("triggers::%s_ObjectRequirements",triggerTokens[0].data()));

      // for (auto & triggerObject : triggerObjectMatchingVector)
      // {

      //     std::vector<std::string> triggerObjectTokens;
      //     while ((pos = triggerObject.find(delimiter)) != std::string::npos)
      //     {
      //         triggerObjectTokens.push_back(triggerObject.substr(0, pos));
      //         triggerObject.erase(0, pos + delimiter.length());
      //     }
      //     triggerObjectTokens.push_back(triggerObject); // last part splitted
      //     if (triggerObjectTokens.size() != 3)
      //     {
      //         throw std::runtime_error("** skim_ntuple : could not parse trigger entry " + triggerObject + " , aborting");
      //     }

      //     triggerObjectAndMinNumberMap[triggerTokens[1]][std::pair<int,int>(atoi(triggerObjectTokens[0].data()),atoi(triggerObjectTokens[1].data()))] = atoi(triggerObjectTokens[2].data());
      // }
    }

  nat.triggerReader().setTriggers(triggerVector);

  ////////////////////////////////////////////////////////////////////////
  // Prepare the output
  ////////////////////////////////////////////////////////////////////////
 
  string outputFileName = opts["output"].as<string>();
  cout << "[INFO] ... saving output to file : " << outputFileName << endl;
  TFile outputFile(outputFileName.c_str(), "recreate");
  OutputTree ot(
                opts["save-p4"].as<bool>(),
                map<string, bool>{
                  {"leptons_p4", config.readBoolOpt("configurations::saveLeptons")},
                  {"jet_coll",   config.readBoolOpt("configurations::saveJetColl")},
                  {"shape_brs",  config.readBoolOpt("configurations::saveShapes")},
                  {"sixb_brs",    (skim_type == ksixb)},
                  {"ttbar_brs",   (skim_type == kttbar)},
                  {"sig_gen_brs", (is_signal)},
                  {"gen_brs",     (!is_data)},
                });

  ot.declareUserIntBranch("nfound_all",    0);
  ot.declareUserIntBranch("nfound_presel", 0);
  ot.declareUserIntBranch("nfound_sixb",   0);

  if (save_trg_decision) {
    for (auto& tname : triggerVector)
      ot.declareUserIntBranch(tname,   0);
  }

  std::string pu_weight_file;
  if (!is_data){
    if (opts["puWeight"].as<string>().size() != 0){ // a valid option is passed from cmd line
      cout << "[INFO] Using custom PU weight file passed from cmd line options" << endl;
      pu_weight_file = opts["puWeight"].as<string>();
    }
    else { // revert to default in skim cfg
      cout << "[INFO] Using PU weight file from skim cfg" << endl;
      pu_weight_file = config.readStringOpt("parameters::PUweightFile");
    }
  }

  NormWeightTree nwt;
  // map<string, string> pu_data{
  //     {"filename", pu_weight_file},
  //     {"name_PU_w", "PUweights"},
  //     {"name_PU_w_up", "PUweights_up"},
  //     {"name_PU_w_do", "PUweights_down"},
  // };

  // // just a test
  // nwt.add_weight("test1", {"test1_up", "test1_down"});
  // nwt.add_weight("test2", {"test2_A", "test2_B", "test2_C"});
  // nwt.add_weight("test3", {});

  ////////////////////////////////////////////////////////////////////////
  // All pre-running configurations (corrections, methods from cfg, etc)
  ////////////////////////////////////////////////////////////////////////

  jsonLumiFilter jlf;
  if (is_data)
    jlf.loadJSON(config.readStringOpt("data::lumimask")); // just read the info for data, so if I just skim MC I'm not forced to parse a JSON

  // -----------

  Timer loop_timer;

  // -----------

  SixB_functions sbf;

  // -----------
    
  const std::vector<double> btag_WPs = config.readDoubleListOpt("configurations::bTagWPDef");
  const int nMinBtag = config.readIntOpt("configurations::nMinBtag");
  const int bTagWP   = config.readIntOpt("configurations::bTagWP");

  sbf.set_btag_WPs(config.readDoubleListOpt("configurations::bTagWPDef"));

  cout << "[INFO] ... events must contain >= " << nMinBtag << " jets passing WP (0:L, 1:M, 2:T) : " << bTagWP << endl;
  cout << "[INFO] ... the WPs are: (L/M/T) : " << btag_WPs.at(0) << "/" << btag_WPs.at(1) << "/" << btag_WPs.at(2) << endl;

  ot.declareUserIntBranch("nloose_btag",  0);
  ot.declareUserIntBranch("nmedium_btag", 0);
  ot.declareUserIntBranch("ntight_btag",  0);

  ot.declareUserFloatBranch("jet6_btagsum", 0.0);

  BtagSF btsf;
  if (!is_data){
    string btsffile = config.readStringOpt("parameters::DeepJetScaleFactorFile");
    btsf.init_reader("DeepJet", btsffile);
    btsf.set_WPs(btag_WPs.at(0), btag_WPs.at(1), btag_WPs.at(2));
  }

  // -----------

  const bool applyJetCuts = config.readBoolOpt("configurations::applyJetCuts");
  std::vector<double> pt_cuts; 
  std::vector<int> btagWP_cuts;

  if (applyJetCuts) {
    pt_cuts = config.readDoubleListOpt("configurations::pt_cuts");    
    btagWP_cuts = config.readIntListOpt("configurations::btagWP_cuts");
  }

  // -----------

  string f_2j_classifier = config.readStringOpt("configurations::2jet_classifier");
  string f_6j_classifier = config.readStringOpt("configurations::6jet_classifier");

  EvalNN n_2j_classifier(f_2j_classifier);
  EvalNN n_6j_classifier(f_6j_classifier);

  cout << "[INFO] Loading 2 Jet Classifier: " << f_2j_classifier << endl;
  cout << "[INFO] Loading 6 Jet Classifier: " << f_6j_classifier << endl;

  // -----------

  JetTools jt;

  string jes_shift = opts["jes-shift-syst"].as<string>();
  bool do_jes_shift = (jes_shift != "nominal");
  cout << "[INFO] ... shifting jet energy scale? " << std::boolalpha << do_jes_shift << std::noboolalpha << endl;
  bool dir_jes_shift_is_up;
  if (do_jes_shift && !is_data){
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

  // FIXME: block below to be run only if !is_data?
  string JERScaleFactorFile = config.readStringOpt("parameters::JERScaleFactorFile");
  string JERResolutionFile  = config.readStringOpt("parameters::JERResolutionFile");
  const int rndm_seed = opts["seed"].as<int>();
  cout << "[INFO] ... initialising JER corrector with the following parameters" << endl;
  cout << "       ... SF file         : " << JERScaleFactorFile << endl;
  cout << "       ... resolution file : " << JERResolutionFile << endl;
  cout << "       ... rndm seed       : " << rndm_seed << endl;
  jt.init_smear(JERScaleFactorFile, JERResolutionFile, rndm_seed);

  cout << "[INFO] ... jet resolution syst is    : " << opts["jer-shift-syst"].as<string>() << endl;
  cout << "[INFO] ... b regr resolution syst is : " << opts["bjer-shift-syst"].as<string>() << endl;
  const Variation jer_var  = string_to_jer_variation(opts["jer-shift-syst"].as<string>());
  const Variation bjer_var = string_to_jer_variation(opts["bjer-shift-syst"].as<string>());

  ////////////////////////////////////////////////////////////////////////
  // Execute event loop
  ////////////////////////////////////////////////////////////////////////

  const int maxEvts = opts["maxEvts"].as<int>();
  if (maxEvts >= 0)
    cout << "[INFO] ... running on : " << maxEvts << " events" << endl;

  const auto start_loop_t = chrono::high_resolution_clock::now();

  Cutflow cutflow;
    
  for (int iEv = 0; true; ++iEv)
    {
      if (maxEvts >= 0 && iEv >= maxEvts)
	break;

      loop_timer.start_lap();

      if (!nat.Next()) break;
      if (iEv % 10000 == 0) {
	cout << "... processing event " << iEv << endl;
	// auto bsize  = ot.getTree()->GetBranch("Run")->GetBasketSize();
	// cout << "... tree basket size (branch Run) : " << bsize  << endl;
      }
      // use the tree content to initialise weight tree in the first event
      if (iEv == 0 && !is_data){
	// nwt.init_weights(nat, pu_data); // get the syst structure from nanoAOD
	su::init_gen_weights(ot, nwt);  // and forward it to the output tree
      }

      if (is_data && !jlf.isValid(*nat.run, *nat.luminosityBlock)){
	continue; // not a valid lumi
      }

      EventInfo ei;
      ot.clear();

      cutflow.add("total");

      loop_timer.click("Input read");

      if (!is_data){
	// nwt.read_weights(nat);
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
	// nwt.fill();
	// loop_timer.click("Norm weight read + fill");
      }
      // ------- events can start be filtered from here (after saving all gen weights)
        
      // trigger requirements
      if (apply_trigger && !(nat.getTrgOr()) )
	continue;
      cutflow.add("trigger");
        
      if (save_trg_decision) {
	auto listOfPassedTriggers = nat.getTrgPassed();
	for (auto& t : listOfPassedTriggers)
	  ot.userInt(t) = 1; // defaults are left to 0
      }
      loop_timer.click("Trigger");

      // global event info
      sbf.copy_event_info(nat, ei, !is_data);
      loop_timer.click("Global info");

      // signal-specific gen info
      if (is_signal){
	sbf.select_gen_particles   (nat, ei);
	sbf.match_genbs_to_genjets (nat, ei);
	sbf.match_genbs_genjets_to_reco (nat, ei);
	loop_timer.click("Signal gen level");
      }

      // jet selections
      std::vector<Jet> all_jets    = sbf.get_all_jets (nat);
      int nfound_all = sbf.n_gjmatched_in_jetcoll(nat, ei, all_jets);
      ot.userInt("nfound_all")    = nfound_all;
        
      loop_timer.click("All jets copy");

      if (!is_data){
	if (do_jes_shift)
	  all_jets = jt.jec_shift_jets(nat, all_jets, dir_jes_shift_is_up);
	all_jets = jt.smear_jets(nat, all_jets, jer_var, bjer_var);
	loop_timer.click("JEC + JER");
      }

      std::vector<Jet> presel_jets = sbf.preselect_jets   (nat, all_jets);
      sbf.btag_bias_pt_sort(presel_jets);
      int n_presel_jet = presel_jets.size();
      int nfound_presel = sbf.n_gjmatched_in_jetcoll(nat, ei, presel_jets);
      sbf.match_signal_recojets(ei,presel_jets);
      ot.userInt("nfound_presel") = nfound_presel;

      std::vector<DiJet> all_higgs;
      std::vector<DiJet> nn_higgs;
      if (n_presel_jet >= 6) {
	// Make sure there are 6 jets to be able to do the pairings
	all_higgs = sbf.get_tri_higgs_D_HHH(presel_jets);
	nn_higgs = sbf.get_tri_higgs_NN(ei,presel_jets,n_6j_classifier,n_2j_classifier);
            
	ei.n_higgs = all_higgs.size();
	ei.higgs_list = all_higgs;

	ei.n_nn_higgs = nn_higgs.size();
	ei.nn_higgs_list = nn_higgs;
      }
        
      if (!is_data) {
	std::vector<GenJet> all_genjets = sbf.get_all_genjets(nat);
	sbf.match_genjets_to_reco(all_genjets,presel_jets);

	if (skim_type == ksixb) {
	  sbf.match_signal_genjets(ei,all_genjets);
	}
            
	ei.genjet_list = all_genjets;
      }
        
      EventShapeCalculator esc(presel_jets);
      EventShapes event_shapes = esc.get_sphericity_shapes();
      ei.event_shapes = event_shapes;
        
      ei.jet_list = presel_jets;
      ei.n_jet = n_presel_jet;


      float jet6_btagsum = 0.0;
      for (unsigned int i = 0; i < TMath::Min(6,n_presel_jet); i++) jet6_btagsum += presel_jets[i].get_btag();
      ot.userFloat("jet6_btagsum") = jet6_btagsum;
            
      std::vector<int> njet_btagwp = {0,0,0};
      for (Jet& jet : presel_jets)
	{
	  float btag = jet.get_btag();
	  for (int i = 0; i < 3; i++)
	    if ( btag > btag_WPs[i] )
	      njet_btagwp[i] += 1;
	}

      ot.userInt("nloose_btag") = njet_btagwp[0];
      ot.userInt("nmedium_btag") = njet_btagwp[1];
      ot.userInt("ntight_btag") = njet_btagwp[2];
        
      loop_timer.click("Preselection");

      if (skim_type == kqcd){
            
	if (presel_jets.size() < 2)
	  continue;
	cutflow.add("npresel_jets>=2");

	if (njet_btagwp[2] < 2)
	  continue;
	cutflow.add("ntight_btag>=2");
            
	if ( presel_jets[0].get_pt() <= 40 || presel_jets[1].get_pt() <= 40 )
	  continue;
	cutflow.add("top2_jet_pt>40");
            
	loop_timer.click("QCD selection");
      }

      if (skim_type == ksixb){
	if (presel_jets.size() < 6)
	  continue;
	cutflow.add("npresel_jets>=6");

	if ( applyJetCuts && !sbf.pass_jet_cut(cutflow,pt_cuts,btagWP_cuts,presel_jets) )
	  continue;
            
	std::vector<Jet> sixb_jets = sbf.select_sixb_jets(nat, presel_jets);
	int nfound_sixb = sbf.n_gjmatched_in_jetcoll(nat, ei, sixb_jets);
	ot.userInt("nfound_sixb")   = nfound_sixb;
	loop_timer.click("Six b selection");
      }

      if (skim_type == khiggscr){
	if (presel_jets.size() < 6)
	  continue;
	cutflow.add("npresel_jets>=6");

	if ( applyJetCuts && !sbf.pass_jet_cut(cutflow,pt_cuts,btagWP_cuts,presel_jets) )
	  continue;

	if ( !sbf.pass_higgs_cr(all_higgs) )
	  continue;
	cutflow.add("higgs_veto_cr");

	if ( jet6_btagsum >= 3.8 )
	  continue;
	cutflow.add("jet6_btagsum<3.8");
            
	loop_timer.click("Higgs CR selection");
      }

      if (skim_type == kttbar){
	if (presel_jets.size() < 2)
	  continue;
	cutflow.add("npresel_jets>=2");
            
	std::vector<Jet> ttjets = sbf.select_ttbar_jets(nat, ei, presel_jets); // ttjets sorted by DeepJet
	double deepjet1 = get_property(ttjets.at(0), Jet_btagDeepFlavB);
	double deepjet2 = get_property(ttjets.at(1), Jet_btagDeepFlavB);
	int nbtag = 0;
	if (deepjet1 > btag_WPs.at(bTagWP)) nbtag += 1;
	if (deepjet2 > btag_WPs.at(bTagWP)) nbtag += 1;
	if (nbtag < nMinBtag)
	  continue;
	cutflow.add("ttbar_jet_cut");
	if (!is_data)
	  ei.btagSF_WP_M = btsf.get_SF_allJetsPassWP({ttjets.at(0), ttjets.at(1)}, BtagSF::btagWP::medium);
	loop_timer.click("ttbar b jet selection");
      }

      sbf.select_leptons(nat, ei);
      loop_timer.click("Lepton selection");

      if (!is_data){
	su::copy_gen_weights(ot, nwt);
	loop_timer.click("Read and copy gen weights");
      }

      su::fill_output_tree(ot, nat, ei);
      loop_timer.click("Output tree fill");
    }
  const auto end_loop_t = chrono::high_resolution_clock::now();

  outputFile.cd();
  cutflow.write(outputFile);
  ot.write();
  // if (!is_data)
  // nwt.write();
  const auto end_prog_t = chrono::high_resolution_clock::now();

  // timing statistics
  cout << endl;
  cout << "[INFO] : sumary of skim loop execution time" << endl;
  loop_timer.print_summary();
  cout << endl;
  cout << "[INFO] : total elapsed time : " << chrono::duration_cast<chrono::milliseconds>(end_prog_t - start_prog_t).count()/1000.   << " s" << endl;
  cout << "       : startup time       : " << chrono::duration_cast<chrono::milliseconds>(start_loop_t - start_prog_t).count()/1000. << " s" << endl;
  cout << "       : loop time          : " << chrono::duration_cast<chrono::milliseconds>(end_loop_t - start_loop_t).count()/1000.   << " s" << endl;
  cout << "       : post-loop time     : " << chrono::duration_cast<chrono::milliseconds>(end_prog_t - end_loop_t).count()/1000.     << " s" << endl;

  cout << endl;
  cout << "[INFO] ... skim finished" << endl;
}

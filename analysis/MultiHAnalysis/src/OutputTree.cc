#include "OutputTree.h"

#include <iostream>

using namespace std;

OutputTree::OutputTree(bool savetlv, std::map<std::string, bool> branch_switches, string name, string title) :
BaseOutTree(name, title, "OutputTree"),
  savetlv_(savetlv)
{
  init_branches(branch_switches);
  clear();
}

void OutputTree::init_branches(std::map<std::string, bool> branch_switches)
{
  auto is_enabled = [&branch_switches](std::string opt) -> bool {
    auto search = branch_switches.find(opt);
    if (search == branch_switches.end())
      return true; // if no opt given, enabled by default
    return search->second; // otherwise, use the value of the option
  };

  //event information
  tree_->Branch("Run",     &Run);
  tree_->Branch("LumiSec", &LumiSec);
  tree_->Branch("Event",   &Event);

  tree_->Branch("genEventSumw",   &genEventSumw);

  tree_->Branch("n_other_pv",     &n_other_pv);
  tree_->Branch("rhofastjet_all", &rhofastjet_all);
  tree_->Branch("PFHT", &PFHT);

  tree_->Branch("HEMWeight", &HEMWeight);

  tree_->Branch("PUIDWeight", &PUIDWeight);
  tree_->Branch("PUIDWeight_up", &PUIDWeight_up);
  tree_->Branch("PUIDWeight_down", &PUIDWeight_down);
  
  if (is_enabled("saveTrgSF"))
    {
      std::cout << "[INFO] OutputTree : enabling trigger scale factor branches"<<std::endl;
      tree_->Branch("triggerScaleFactor", &triggerScaleFactor);
      tree_->Branch("triggerDataEfficiency", &triggerDataEfficiency);
      tree_->Branch("triggerMcEfficiency", &triggerMcEfficiency);
      tree_->Branch("triggerScaleFactorUp", &triggerScaleFactorUp);
      tree_->Branch("triggerDataEfficiencyUp", &triggerDataEfficiencyUp);
      tree_->Branch("triggerMcEfficiencyUp", &triggerMcEfficiencyUp);
      tree_->Branch("triggerScaleFactorDown", &triggerScaleFactorDown);
      tree_->Branch("triggerDataEfficiencyDown", &triggerDataEfficiencyDown);
      tree_->Branch("triggerMcEfficiencyDown", &triggerMcEfficiencyDown);
    }
  
  if (is_enabled("fourb_brs"))
    {
      if (is_enabled("sig_gen_brs"))
	{
	  REGISTER_BRANCH_COLLECTION(gen_H1_fc);
	  REGISTER_BRANCH_COLLECTION(gen_H2_fc);
	  REGISTER_BRANCH_COLLECTION(gen_H1);
	  REGISTER_BRANCH_COLLECTION(gen_H2);
	  REGISTER_BRANCH_COLLECTION(gen_H1_b1);
	  REGISTER_BRANCH_COLLECTION(gen_H1_b2);
	  REGISTER_BRANCH_COLLECTION(gen_H2_b1);
	  REGISTER_BRANCH_COLLECTION(gen_H2_b2);
	  
	  REGISTER_BRANCH_COLLECTION(gen_H1_b1_genjet);
	  REGISTER_BRANCH_COLLECTION(gen_H1_b2_genjet);
	  REGISTER_BRANCH_COLLECTION(gen_H2_b1_genjet);
	  REGISTER_BRANCH_COLLECTION(gen_H2_b2_genjet);
	  
	  REGISTER_BRANCH_COLLECTION(gen_H1_b1_recojet);
	  REGISTER_BRANCH_COLLECTION(gen_H1_b2_recojet);
	  REGISTER_BRANCH_COLLECTION(gen_H2_b1_recojet);
	  REGISTER_BRANCH_COLLECTION(gen_H2_b2_recojet);
	  
	  if (is_enabled("fatjet_coll"))
	    {
	      REGISTER_BRANCH_COLLECTION(gen_H1_b1_genfatjet);
	      REGISTER_BRANCH_COLLECTION(gen_H1_b2_genfatjet);
	      REGISTER_BRANCH_COLLECTION(gen_H2_b1_genfatjet);
	      REGISTER_BRANCH_COLLECTION(gen_H2_b2_genfatjet);
	      REGISTER_BRANCH_COLLECTION(gen_H1_b1_recofatjet);
	      REGISTER_BRANCH_COLLECTION(gen_H1_b2_recofatjet);
	      REGISTER_BRANCH_COLLECTION(gen_H2_b1_recofatjet);
	      REGISTER_BRANCH_COLLECTION(gen_H2_b2_recofatjet);
	    }
	}
    } // 4b final state


  if (is_enabled("sixb_brs"))
  {
    if (is_enabled("sig_gen_brs"))
    {
      REGISTER_BRANCH_COLLECTION(gen_X_fc);
      REGISTER_BRANCH_COLLECTION(gen_X);
      REGISTER_BRANCH_COLLECTION(gen_Y);
      REGISTER_BRANCH_COLLECTION(gen_HX);
      REGISTER_BRANCH_COLLECTION(gen_H1);
      REGISTER_BRANCH_COLLECTION(gen_H2);

      REGISTER_BRANCH_COLLECTION(gen_HX_b1);
      REGISTER_BRANCH_COLLECTION(gen_HX_b2);
      REGISTER_BRANCH_COLLECTION(gen_H1_b1);
      REGISTER_BRANCH_COLLECTION(gen_H1_b2);
      REGISTER_BRANCH_COLLECTION(gen_H2_b1);
      REGISTER_BRANCH_COLLECTION(gen_H2_b2);

      REGISTER_BRANCH_COLLECTION(gen_HX_b1_genjet);
      REGISTER_BRANCH_COLLECTION(gen_HX_b2_genjet);
      REGISTER_BRANCH_COLLECTION(gen_H1_b1_genjet);
      REGISTER_BRANCH_COLLECTION(gen_H1_b2_genjet);
      REGISTER_BRANCH_COLLECTION(gen_H2_b1_genjet);
      REGISTER_BRANCH_COLLECTION(gen_H2_b2_genjet);

      REGISTER_BRANCH_COLLECTION(gen_HX_b1_recojet);
      REGISTER_BRANCH_COLLECTION(gen_HX_b2_recojet);
      REGISTER_BRANCH_COLLECTION(gen_H1_b1_recojet);
      REGISTER_BRANCH_COLLECTION(gen_H1_b2_recojet);
      REGISTER_BRANCH_COLLECTION(gen_H2_b1_recojet);
      REGISTER_BRANCH_COLLECTION(gen_H2_b2_recojet);

      tree_->Branch("HX_b1_genHflag", &HX_b1_genHflag);
      tree_->Branch("HX_b2_genHflag", &HX_b2_genHflag);
      tree_->Branch("H1_b1_genHflag", &H1_b1_genHflag);
      tree_->Branch("H1_b2_genHflag", &H1_b2_genHflag);
      tree_->Branch("H2_b1_genHflag", &H2_b1_genHflag);
      tree_->Branch("H2_b2_genHflag", &H2_b2_genHflag);

      tree_->Branch("gen_bs_N_reco_match", &gen_bs_N_reco_match);
      tree_->Branch("gen_bs_N_reco_match_in_acc", &gen_bs_N_reco_match_in_acc);
      tree_->Branch("gen_bs_match_recojet_minv", &gen_bs_match_recojet_minv);
      tree_->Branch("gen_bs_match_in_acc_recojet_minv", &gen_bs_match_in_acc_recojet_minv);

      tree_->Branch("nfound_all", &nfound_all);
      tree_->Branch("nfound_all_h", &nfound_all_h);
      tree_->Branch("nfound_presel", &nfound_presel);
      tree_->Branch("nfound_presel_h", &nfound_presel_h);
      tree_->Branch("nfound_select", &nfound_select);
      tree_->Branch("nfound_select_h", &nfound_select_h);
      tree_->Branch("nfound_paired_h", &nfound_paired_h);
    }

    REGISTER_BRANCH_COLLECTION(X);
    REGISTER_BRANCH_COLLECTION(Y);
    REGISTER_BRANCH_COLLECTION(HX);
    REGISTER_BRANCH_COLLECTION(H1);
    REGISTER_BRANCH_COLLECTION(H2);

    REGISTER_BRANCH_COLLECTION(HX_b1);
    REGISTER_BRANCH_COLLECTION(HX_b2);
    REGISTER_BRANCH_COLLECTION(H1_b1);
    REGISTER_BRANCH_COLLECTION(H1_b2);
    REGISTER_BRANCH_COLLECTION(H2_b1);
    REGISTER_BRANCH_COLLECTION(H2_b2);
  }

  if (is_enabled("eightb_brs"))
  {

    if (is_enabled("sig_gen_brs"))
    {
      REGISTER_BRANCH_COLLECTION(gen_X_fc);
      REGISTER_BRANCH_COLLECTION(gen_X);
      REGISTER_BRANCH_COLLECTION(gen_Y1);
      REGISTER_BRANCH_COLLECTION(gen_Y2);
      REGISTER_BRANCH_COLLECTION(gen_H1Y1);
      REGISTER_BRANCH_COLLECTION(gen_H2Y1);
      REGISTER_BRANCH_COLLECTION(gen_H1Y2);
      REGISTER_BRANCH_COLLECTION(gen_H2Y2);

      REGISTER_BRANCH_COLLECTION(gen_H1Y1_b1);
      REGISTER_BRANCH_COLLECTION(gen_H1Y1_b2);
      REGISTER_BRANCH_COLLECTION(gen_H2Y1_b1);
      REGISTER_BRANCH_COLLECTION(gen_H2Y1_b2);
      REGISTER_BRANCH_COLLECTION(gen_H1Y2_b1);
      REGISTER_BRANCH_COLLECTION(gen_H1Y2_b2);
      REGISTER_BRANCH_COLLECTION(gen_H2Y2_b1);
      REGISTER_BRANCH_COLLECTION(gen_H2Y2_b2);

      REGISTER_BRANCH_COLLECTION(gen_H1Y1_b1_genjet);
      REGISTER_BRANCH_COLLECTION(gen_H1Y1_b2_genjet);
      REGISTER_BRANCH_COLLECTION(gen_H2Y1_b1_genjet);
      REGISTER_BRANCH_COLLECTION(gen_H2Y1_b2_genjet);
      REGISTER_BRANCH_COLLECTION(gen_H1Y2_b1_genjet);
      REGISTER_BRANCH_COLLECTION(gen_H1Y2_b2_genjet);
      REGISTER_BRANCH_COLLECTION(gen_H2Y2_b1_genjet);
      REGISTER_BRANCH_COLLECTION(gen_H2Y2_b2_genjet);

      REGISTER_BRANCH_COLLECTION(gen_H1Y1_b1_recojet);
      REGISTER_BRANCH_COLLECTION(gen_H1Y1_b2_recojet);
      REGISTER_BRANCH_COLLECTION(gen_H2Y1_b1_recojet);
      REGISTER_BRANCH_COLLECTION(gen_H2Y1_b2_recojet);
      REGISTER_BRANCH_COLLECTION(gen_H1Y2_b1_recojet);
      REGISTER_BRANCH_COLLECTION(gen_H1Y2_b2_recojet);
      REGISTER_BRANCH_COLLECTION(gen_H2Y2_b1_recojet);
      REGISTER_BRANCH_COLLECTION(gen_H2Y2_b2_recojet);

      tree_->Branch("gen_bs_N_reco_match", &gen_bs_N_reco_match);
      tree_->Branch("gen_bs_N_reco_match_in_acc", &gen_bs_N_reco_match_in_acc);
      tree_->Branch("gen_bs_match_recojet_minv", &gen_bs_match_recojet_minv);
      tree_->Branch("gen_bs_match_in_acc_recojet_minv", &gen_bs_match_in_acc_recojet_minv);

      tree_->Branch("nfound_all", &nfound_all);
      tree_->Branch("nfound_all_h", &nfound_all_h);
      tree_->Branch("nfound_presel", &nfound_presel);
      tree_->Branch("nfound_presel_h", &nfound_presel_h);
      tree_->Branch("nfound_select", &nfound_select);
      tree_->Branch("nfound_select_h", &nfound_select_h);
      tree_->Branch("nfound_paired_h", &nfound_paired_h);
      tree_->Branch("nfound_select_y", &nfound_select_y);
      tree_->Branch("nfound_paired_y", &nfound_paired_y);
    }

    REGISTER_BRANCH_COLLECTION(X);
    REGISTER_BRANCH_COLLECTION(Y1);
    REGISTER_BRANCH_COLLECTION(Y2);
    REGISTER_BRANCH_COLLECTION(H1Y1);
    REGISTER_BRANCH_COLLECTION(H2Y1);
    REGISTER_BRANCH_COLLECTION(H1Y2);
    REGISTER_BRANCH_COLLECTION(H2Y2);

    REGISTER_BRANCH_COLLECTION(H1Y1_b1);
    REGISTER_BRANCH_COLLECTION(H1Y1_b2);
    REGISTER_BRANCH_COLLECTION(H2Y1_b1);
    REGISTER_BRANCH_COLLECTION(H2Y1_b2);
    REGISTER_BRANCH_COLLECTION(H1Y2_b1);
    REGISTER_BRANCH_COLLECTION(H1Y2_b2);
    REGISTER_BRANCH_COLLECTION(H2Y2_b1);
    REGISTER_BRANCH_COLLECTION(H2Y2_b2);

    tree_->Branch("n_loose_btag", &n_loose_btag);
    tree_->Branch("n_medium_btag", &n_medium_btag);
    tree_->Branch("n_tight_btag", &n_tight_btag);
    tree_->Branch("btagavg", &btagavg);
  }
  
  tree_->Branch("n_muon", &n_muon);
  if (is_enabled("muon_coll"))
    {
      std::cout << "[INFO] OutputTree : enabling muon collection branches" << std::endl;
      REGISTER_BRANCH_COLLECTION(muon);
    }
  
  tree_->Branch("n_ele", &n_ele);
  if (is_enabled("ele_coll"))
    {
      std::cout << "[INFO] OutputTree : enabling electron collection branches" << std::endl;
      REGISTER_BRANCH_COLLECTION(ele);
    }
  
  if (is_enabled("ttbar_brs"))
    {
      std::cout << "[INFO] OutputTree : enabling ttbar branches" << std::endl;
      if (is_enabled("sig_gen_brs")) {
        tree_->Branch("nfound_all", &nfound_all);
        tree_->Branch("nfound_presel", &nfound_presel);
        tree_->Branch("nfound_select", &nfound_select);
      }
    }
  
  tree_->Branch("n_total_jet",&n_total_jet);
  tree_->Branch("n_jet", &n_jet);
  if (is_enabled("jet_coll"))
    {
      std::cout << "[INFO] OutputTree : enabling jet collection branches" << std::endl;
      REGISTER_BRANCH_COLLECTION(jet);
      tree_->Branch("b_6j_score", &b_6j_score);
    }

  if (is_enabled("fatjet_coll"))
    {
      std::cout << "[INFO] OutputTree : enabling fatjet collection branches" << std::endl;
      tree_->Branch("n_fatjet", &n_fatjet);
      REGISTER_BRANCH_COLLECTION(fatjet);
    }

  if (is_enabled("gen_brs"))
    {
      std::cout << "[INFO] OutputTree : enabling gen-only related branches" << std::endl;
      tree_->Branch("n_pu",        &n_pu);
      tree_->Branch("n_true_int",  &n_true_int);
      tree_->Branch("lhe_ht",         &lhe_ht);
      tree_->Branch("btagSF_WP_M", &btagSF_WP_M);
      tree_->Branch("n_genjet",    &n_genjet);

      if (is_enabled("jet_coll"))
	{
	  REGISTER_BRANCH_COLLECTION(genjet);
	}
      if (is_enabled("bquark_coll"))
	{
	  REGISTER_BRANCH_COLLECTION(genpb);
	}
      if (is_enabled("fatjet_coll"))
	{
	  tree_->Branch("n_genfatjet", &n_genfatjet);
	  REGISTER_BRANCH_COLLECTION(genfatjet);
	}
    }
  if (is_enabled("shape_brs"))
    {
      std::cout << "[INFO] OutputTree : enabling event shape-only related branches" << std::endl;
      tree_->Branch("sphericity",  &sphericity);
      tree_->Branch("sphericity_t",&sphericity_t);
      tree_->Branch("aplanarity",  &aplanarity);
    }
  // note that the initialization of the user branches is made separately when calling declareUser*Branch
}

void OutputTree::clear()
{
  Run     = 0;
  LumiSec = 0;
  Event   = 0;
  genEventSumw = 0;

  n_other_pv     = 0;
  n_pu           = 0;
  n_true_int     = 0;
  rhofastjet_all = 0;
  
  PFHT = 0;

  HEMWeight = 1.;

  PUIDWeight = 1.;
  PUIDWeight_up = 1.;
  PUIDWeight_down = 1.;

  triggerScaleFactor        = 1.;
  triggerDataEfficiency     = 1.;
  triggerMcEfficiency       = 1.;
  triggerScaleFactorUp      = 1.;
  triggerDataEfficiencyUp   = 1.;
  triggerMcEfficiencyUp     = 1.;
  triggerScaleFactorDown    = 1.;
  triggerDataEfficiencyDown = 1.;
  triggerMcEfficiencyDown   = 1.;
  
  n_jet = 0;
  n_genjet = 0;
  n_higgs = 0;
  n_genfatjet = 0;
  n_fatjet = 0;
  n_ele = 0;
  n_muon = 0;
  
  b_6j_score = 0;
  b_3d_score = 0;

  genpb.Clear();
  genjet.Clear();
  genfatjet.Clear();

  ele.Clear();
  muon.Clear();
  jet.Clear();
  fatjet.Clear();

  // Start Gen 4b Objects
  gen_H1_fc.Clear();
  gen_H2_fc.Clear();
  gen_H1_b1_genfatjet.Clear();
  gen_H1_b2_genfatjet.Clear();
  gen_H2_b1_genfatjet.Clear();
  gen_H2_b2_genfatjet.Clear();
  gen_H1_b1_recofatjet.Clear();
  gen_H1_b2_recofatjet.Clear();
  gen_H2_b1_recofatjet.Clear();
  gen_H2_b2_recofatjet.Clear();

  gen_X_fc.Clear();
  gen_X.Clear();

  // Start Gen 6B Objects
  gen_Y.Clear();
  gen_HX.Clear();
  gen_H1.Clear();
  gen_H2.Clear();

  gen_HX_b1.Clear();
  gen_HX_b2.Clear();
  gen_H1_b1.Clear();
  gen_H1_b2.Clear();
  gen_H2_b1.Clear();
  gen_H2_b2.Clear();

  gen_HX_b1_genjet.Clear();
  gen_HX_b2_genjet.Clear();
  gen_H1_b1_genjet.Clear();
  gen_H1_b2_genjet.Clear();
  gen_H2_b1_genjet.Clear();
  gen_H2_b2_genjet.Clear();

  gen_HX_b1_recojet.Clear();
  gen_HX_b2_recojet.Clear();
  gen_H1_b1_recojet.Clear();
  gen_H1_b2_recojet.Clear();
  gen_H2_b1_recojet.Clear();
  gen_H2_b2_recojet.Clear();
  // End Gen 6B Objects

  // Start Gen 8B Objects 
  gen_Y1.Clear();
  gen_Y2.Clear();
  gen_H1Y1.Clear();
  gen_H2Y1.Clear();
  gen_H1Y2.Clear();
  gen_H2Y2.Clear();

  gen_H1Y1_b1.Clear();
  gen_H1Y1_b2.Clear();
  gen_H2Y1_b1.Clear();
  gen_H2Y1_b2.Clear();
  gen_H1Y2_b1.Clear();
  gen_H1Y2_b2.Clear();
  gen_H2Y2_b1.Clear();
  gen_H2Y2_b2.Clear();
  
  gen_H1Y1_b1_genjet.Clear();
  gen_H1Y1_b2_genjet.Clear();
  gen_H2Y1_b1_genjet.Clear();
  gen_H2Y1_b2_genjet.Clear();
  gen_H1Y2_b1_genjet.Clear();
  gen_H1Y2_b2_genjet.Clear();
  gen_H2Y2_b1_genjet.Clear();
  gen_H2Y2_b2_genjet.Clear();
  
  gen_H1Y1_b1_recojet.Clear();
  gen_H1Y1_b2_recojet.Clear();
  gen_H2Y1_b1_recojet.Clear();
  gen_H2Y1_b2_recojet.Clear();
  gen_H1Y2_b1_recojet.Clear();
  gen_H1Y2_b2_recojet.Clear();
  gen_H2Y2_b1_recojet.Clear();
  gen_H2Y2_b2_recojet.Clear();
  // End Gen 8B Objects

  gen_bs_N_reco_match        = -999;
  gen_bs_N_reco_match_in_acc = -999;
  gen_bs_match_recojet_minv        = -999;
  gen_bs_match_in_acc_recojet_minv = -999;

  nfound_all = -999;
  nfound_all_h = -999;
  nfound_presel = -999;
  nfound_presel_h = -999;
  nfound_select = -999;
  nfound_select_h = -999;
  nfound_paired_h = -999;

  X.Clear();
  // Start Reco 6B Objects
  Y.Clear();
  HX.Clear();
  H1.Clear();
  H2.Clear();

  HX_b1.Clear();
  HX_b2.Clear();
  H1_b1.Clear();
  H1_b2.Clear();
  H2_b1.Clear();
  H2_b2.Clear();

  HX_b1_genHflag  = -999;
  HX_b2_genHflag  = -999;
  H1_b1_genHflag = -999;
  H1_b2_genHflag = -999;
  H2_b1_genHflag = -999;
  H2_b2_genHflag = -999;
  // End Reco 6B Objects

  // Start Reco 8B Objects
  Y.Clear();
  HX.Clear();
  H1.Clear();
  H2.Clear();

  H1Y1_b1.Clear();
  H1Y1_b2.Clear();
  H2Y1_b1.Clear();
  H2Y1_b2.Clear();
  H1Y2_b1.Clear();
  H1Y2_b2.Clear();
  H2Y2_b1.Clear();
  H2Y2_b2.Clear();

  n_loose_btag = -1;
  n_medium_btag = -1;
  n_tight_btag = -1;
  btagavg = -1.;
  // End Reco 8B Objects

  //CLEAR_m_pt_ptRegressed_eta_phi_DeepJet_p4(bjet1);
  //CLEAR_m_pt_ptRegressed_eta_phi_DeepJet_p4(bjet2);
  //bjet1_hadflav = -999;
  //bjet2_hadflav = -999;

  btagSF_WP_M = -999.;

  // reset all user-defined branches
  userFloats_.resetAll();
  userInts_.resetAll();

}

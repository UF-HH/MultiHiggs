#include "OutputTree.h"

#include <iostream>

using namespace std;

// helper: creates the pt/eta/phi/p4 branches of a variable OBJ
#define BRANCH_m_pt_eta_phi_p4(OBJ)			\
  tree_->Branch(#OBJ "_m",  &OBJ ## _m);		\
  tree_->Branch(#OBJ "_pt",  &OBJ ## _pt);		\
  tree_->Branch(#OBJ "_eta", &OBJ ## _eta);		\
  tree_->Branch(#OBJ "_phi", &OBJ ## _phi);		\
  if (savetlv_) tree_->Branch(#OBJ "_p4", &OBJ ## _p4);

#define CLEAR_m_pt_eta_phi_p4(OBJ)		\
  OBJ ## _m    = -999.;				\
  OBJ ## _pt   = -999.;				\
  OBJ ## _eta  = -999.;				\
  OBJ ## _phi  = -999.;				\
  OBJ ## _p4 . SetCoordinates(0,0,0,0);

#define BRANCH_m_pt_ptRegressed_eta_phi_p4(OBJ)			\
  tree_->Branch(#OBJ "_m"          ,  &OBJ ## _m);		\
  tree_->Branch(#OBJ "_pt"         ,  &OBJ ## _pt);		\
  tree_->Branch(#OBJ "_ptRegressed",  &OBJ ## _ptRegressed);	\
  tree_->Branch(#OBJ "_eta"        , &OBJ ## _eta);		\
  tree_->Branch(#OBJ "_phi"        , &OBJ ## _phi);		\
  if (savetlv_) tree_->Branch(#OBJ "_p4", &OBJ ## _p4);

#define CLEAR_m_pt_ptRegressed_eta_phi_p4(OBJ)		\
  OBJ ## _m             = -999.;			\
  OBJ ## _pt            = -999.;			\
  OBJ ## _ptRegressed   = -999.;			\
  OBJ ## _eta           = -999.;			\
  OBJ ## _phi           = -999.;			\
  OBJ ## _p4            . SetCoordinates(0,0,0,0);

#define BRANCH_m_pt_ptRegressed_eta_phi_DeepJet_p4(OBJ)		\
  tree_->Branch(#OBJ "_m"          ,  &OBJ ## _m);		\
  tree_->Branch(#OBJ "_pt"         ,  &OBJ ## _pt);		\
  tree_->Branch(#OBJ "_ptRegressed",  &OBJ ## _ptRegressed);	\
  tree_->Branch(#OBJ "_eta"        , &OBJ ## _eta);		\
  tree_->Branch(#OBJ "_phi"        , &OBJ ## _phi);		\
  tree_->Branch(#OBJ "_DeepJet"    , &OBJ ## _DeepJet);		\
  if (savetlv_) tree_->Branch(#OBJ "_p4", &OBJ ## _p4);

#define CLEAR_m_pt_ptRegressed_eta_phi_DeepJet_p4(OBJ)	\
  OBJ ## _m             = -999.;			\
  OBJ ## _pt            = -999.;			\
  OBJ ## _ptRegressed   = -999.;			\
  OBJ ## _eta           = -999.;			\
  OBJ ## _phi           = -999.;			\
  OBJ ## _DeepJet       = -999.;			\
  OBJ ## _p4            . SetCoordinates(0,0,0,0);

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

  tree_->Branch("n_other_pv",     &n_other_pv);
  tree_->Branch("rhofastjet_all", &rhofastjet_all);

  if (is_enabled("sig_gen_brs"))
    {
      BRANCH_m_pt_eta_phi_p4(gen_X_fc);
      BRANCH_m_pt_eta_phi_p4(gen_X);
      BRANCH_m_pt_eta_phi_p4(gen_Y);
      BRANCH_m_pt_eta_phi_p4(gen_HX);
      BRANCH_m_pt_eta_phi_p4(gen_HY1);
      BRANCH_m_pt_eta_phi_p4(gen_HY2);

      BRANCH_m_pt_eta_phi_p4(gen_HX_b1);
      BRANCH_m_pt_eta_phi_p4(gen_HX_b2);
      BRANCH_m_pt_eta_phi_p4(gen_HY1_b1);
      BRANCH_m_pt_eta_phi_p4(gen_HY1_b2);
      BRANCH_m_pt_eta_phi_p4(gen_HY2_b1);
      BRANCH_m_pt_eta_phi_p4(gen_HY2_b2);

      BRANCH_m_pt_eta_phi_p4(gen_HX_b1_genjet);
      BRANCH_m_pt_eta_phi_p4(gen_HX_b2_genjet);
      BRANCH_m_pt_eta_phi_p4(gen_HY1_b1_genjet);
      BRANCH_m_pt_eta_phi_p4(gen_HY1_b2_genjet);
      BRANCH_m_pt_eta_phi_p4(gen_HY2_b1_genjet);
      BRANCH_m_pt_eta_phi_p4(gen_HY2_b2_genjet);

      BRANCH_m_pt_ptRegressed_eta_phi_p4(gen_HX_b1_recojet);
      BRANCH_m_pt_ptRegressed_eta_phi_p4(gen_HX_b2_recojet);
      BRANCH_m_pt_ptRegressed_eta_phi_p4(gen_HY1_b1_recojet);
      BRANCH_m_pt_ptRegressed_eta_phi_p4(gen_HY1_b2_recojet);
      BRANCH_m_pt_ptRegressed_eta_phi_p4(gen_HY2_b1_recojet);
      BRANCH_m_pt_ptRegressed_eta_phi_p4(gen_HY2_b2_recojet);
      tree_->Branch("gen_bs_N_reco_match",        &gen_bs_N_reco_match);
      tree_->Branch("gen_bs_N_reco_match_in_acc", &gen_bs_N_reco_match_in_acc);
      tree_->Branch("gen_bs_match_recojet_minv",        &gen_bs_match_recojet_minv);
      tree_->Branch("gen_bs_match_in_acc_recojet_minv", &gen_bs_match_in_acc_recojet_minv);
    }

  if (is_enabled("sixb_brs"))
    {
      BRANCH_m_pt_eta_phi_p4(X);
      BRANCH_m_pt_eta_phi_p4(Y);
      BRANCH_m_pt_eta_phi_p4(HX);
      BRANCH_m_pt_eta_phi_p4(HY1);
      BRANCH_m_pt_eta_phi_p4(HY2);

      BRANCH_m_pt_ptRegressed_eta_phi_p4(HX_b1);
      BRANCH_m_pt_ptRegressed_eta_phi_p4(HX_b2);
      BRANCH_m_pt_ptRegressed_eta_phi_p4(HY1_b1);
      BRANCH_m_pt_ptRegressed_eta_phi_p4(HY1_b2);
      BRANCH_m_pt_ptRegressed_eta_phi_p4(HY2_b1);
      BRANCH_m_pt_ptRegressed_eta_phi_p4(HY2_b2);
    }

  tree_->Branch("n_mu_loose",  &n_mu_loose);
  tree_->Branch("n_ele_loose", &n_ele_loose);
    
  if (is_enabled("leptons_p4"))
    {
      std::cout << "[INFO] OutputTree : enabling lepton p4 branches" << std::endl;
      BRANCH_m_pt_eta_phi_p4(mu_1);
      BRANCH_m_pt_eta_phi_p4(mu_2);
      BRANCH_m_pt_eta_phi_p4(ele_1);
      BRANCH_m_pt_eta_phi_p4(ele_2);
    }

  if (is_enabled("ttbar_brs"))
    {
      std::cout << "[INFO] OutputTree : enabling ttbar branches" << std::endl;
      BRANCH_m_pt_ptRegressed_eta_phi_DeepJet_p4(bjet1);
      if (is_enabled("gen_brs")) tree_->Branch("bjet1_hadflav", &bjet1_hadflav);

      BRANCH_m_pt_ptRegressed_eta_phi_DeepJet_p4(bjet2);
      if (is_enabled("gen_brs")) tree_->Branch("bjet2_hadflav", &bjet2_hadflav);
    }

  tree_->Branch("n_total_jet",&n_total_jet);
	
  if (is_enabled("jet_coll"))
    {
      std::cout << "[INFO] OutputTree : enabling jet collection branches" << std::endl;
      tree_->Branch("n_jet",         &n_jet);
      tree_->Branch("jet_E",         &jet_E);	    
      tree_->Branch("jet_m",         &jet_m);		
      tree_->Branch("jet_pt",        &jet_pt);		
      tree_->Branch("jet_eta",       &jet_eta);		
      tree_->Branch("jet_phi",       &jet_phi);		
      // tree_->Branch("jet_partonFlav",&jet_partonFlav);
      // tree_->Branch("jet_hadronFlav",&jet_hadronFlav);
      tree_->Branch("jet_signalId",  &jet_signalId);
      tree_->Branch("jet_higgsId",   &jet_higgsId);
      tree_->Branch("jet_nn_higgsId",   &jet_nn_higgsId);
      tree_->Branch("jet_genIdx",    &jet_genIdx);
      tree_->Branch("jet_btag",      &jet_btag);
      tree_->Branch("jet_qgl",       &jet_qgl);
      tree_->Branch("jet_id",        &jet_id);
      tree_->Branch("jet_puid",      &jet_puid);

      tree_->Branch("n_higgs",       &n_higgs);
      tree_->Branch("higgs_E",       &higgs_E);	    
      tree_->Branch("higgs_m",       &higgs_m);		
      tree_->Branch("higgs_pt",      &higgs_pt);		
      tree_->Branch("higgs_eta",     &higgs_eta);		
      tree_->Branch("higgs_phi",     &higgs_phi);
      tree_->Branch("higgs_signalId",&higgs_signalId);

      tree_->Branch("b_6j_score",    &b_6j_score);
      tree_->Branch("b_3h_score",    &b_3h_score);
		
      tree_->Branch("n_nn_higgs",       &n_nn_higgs);
      tree_->Branch("nn_higgs_E",       &nn_higgs_E);	    
      tree_->Branch("nn_higgs_m",       &nn_higgs_m);		
      tree_->Branch("nn_higgs_pt",      &nn_higgs_pt);		
      tree_->Branch("nn_higgs_eta",     &nn_higgs_eta);		
      tree_->Branch("nn_higgs_phi",     &nn_higgs_phi);
      tree_->Branch("nn_higgs_signalId",&nn_higgs_signalId);
      tree_->Branch("nn_higgs_2j_score",&nn_higgs_2j_score);
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
	  tree_->Branch("genjet_E",         &genjet_E);	    
	  tree_->Branch("genjet_m",         &genjet_m);		
	  tree_->Branch("genjet_pt",        &genjet_pt);		
	  tree_->Branch("genjet_eta",       &genjet_eta);		
	  tree_->Branch("genjet_phi",       &genjet_phi);		
	  tree_->Branch("genjet_partonFlav",&genjet_partonFlav);
	  tree_->Branch("genjet_hadronFlav",&genjet_hadronFlav);
	  tree_->Branch("genjet_signalId",  &genjet_signalId);
	  tree_->Branch("genjet_recoIdx",   &genjet_recoIdx);
	}
    }

  if (is_enabled("shape_brs"))
    {
      std::cout << "[INFO] OutputTree : enabling shape-only related branches" << std::endl;
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

  n_other_pv     = 0;
  n_pu           = 0;
  n_true_int     = 0;
  rhofastjet_all = 0;

  n_jet = 0;
  n_genjet = 0;
  n_higgs = 0;
  n_nn_higgs = 0;

  b_6j_score = 0;
  b_3h_score = 0;

  genjet_E.clear();	    
  genjet_m.clear();		
  genjet_pt.clear();		
  genjet_eta.clear();		
  genjet_phi.clear();		
  genjet_partonFlav.clear();
  genjet_hadronFlav.clear();
  genjet_signalId.clear();
  genjet_recoIdx.clear();
	
  jet_E.clear();	    
  jet_m.clear();		
  jet_pt.clear();		
  jet_eta.clear();		
  jet_phi.clear();		
  jet_partonFlav.clear();
  jet_hadronFlav.clear();
  jet_signalId.clear();
  jet_higgsId.clear();
  jet_nn_higgsId.clear();
  jet_genIdx.clear();
  jet_btag.clear();
  jet_qgl.clear();
  jet_id.clear();
  jet_puid.clear();
	
  higgs_E.clear();	    
  higgs_m.clear();		
  higgs_pt.clear();		
  higgs_eta.clear();		
  higgs_phi.clear();
  higgs_signalId.clear();
	
  nn_higgs_E.clear();	    
  nn_higgs_m.clear();		
  nn_higgs_pt.clear();		
  nn_higgs_eta.clear();		
  nn_higgs_phi.clear();
  nn_higgs_signalId.clear();
  nn_higgs_2j_score.clear();

  CLEAR_m_pt_eta_phi_p4(gen_X_fc);
  CLEAR_m_pt_eta_phi_p4(gen_X);
  CLEAR_m_pt_eta_phi_p4(gen_Y);
  CLEAR_m_pt_eta_phi_p4(gen_HX);
  CLEAR_m_pt_eta_phi_p4(gen_HY1);
  CLEAR_m_pt_eta_phi_p4(gen_HY2);

  CLEAR_m_pt_eta_phi_p4(gen_HX_b1);
  CLEAR_m_pt_eta_phi_p4(gen_HX_b2);
  CLEAR_m_pt_eta_phi_p4(gen_HY1_b1);
  CLEAR_m_pt_eta_phi_p4(gen_HY1_b2);
  CLEAR_m_pt_eta_phi_p4(gen_HY2_b1);
  CLEAR_m_pt_eta_phi_p4(gen_HY2_b2);

  CLEAR_m_pt_eta_phi_p4(gen_HX_b1_genjet);
  CLEAR_m_pt_eta_phi_p4(gen_HX_b2_genjet);
  CLEAR_m_pt_eta_phi_p4(gen_HY1_b1_genjet);
  CLEAR_m_pt_eta_phi_p4(gen_HY1_b2_genjet);
  CLEAR_m_pt_eta_phi_p4(gen_HY2_b1_genjet);
  CLEAR_m_pt_eta_phi_p4(gen_HY2_b2_genjet);

  CLEAR_m_pt_ptRegressed_eta_phi_p4(gen_HX_b1_recojet);
  CLEAR_m_pt_ptRegressed_eta_phi_p4(gen_HX_b2_recojet);
  CLEAR_m_pt_ptRegressed_eta_phi_p4(gen_HY1_b1_recojet);
  CLEAR_m_pt_ptRegressed_eta_phi_p4(gen_HY1_b2_recojet);
  CLEAR_m_pt_ptRegressed_eta_phi_p4(gen_HY2_b1_recojet);
  CLEAR_m_pt_ptRegressed_eta_phi_p4(gen_HY2_b2_recojet);
  gen_bs_N_reco_match        = -999;
  gen_bs_N_reco_match_in_acc = -999;
  gen_bs_match_recojet_minv        = -999;
  gen_bs_match_in_acc_recojet_minv = -999;

  CLEAR_m_pt_eta_phi_p4(X);
  CLEAR_m_pt_eta_phi_p4(Y);
  CLEAR_m_pt_eta_phi_p4(HX);
  CLEAR_m_pt_eta_phi_p4(HY1);
  CLEAR_m_pt_eta_phi_p4(HY2);

  CLEAR_m_pt_ptRegressed_eta_phi_p4(HX_b1);
  CLEAR_m_pt_ptRegressed_eta_phi_p4(HX_b2);
  CLEAR_m_pt_ptRegressed_eta_phi_p4(HY1_b1);
  CLEAR_m_pt_ptRegressed_eta_phi_p4(HY1_b2);
  CLEAR_m_pt_ptRegressed_eta_phi_p4(HY2_b1);
  CLEAR_m_pt_ptRegressed_eta_phi_p4(HY2_b2);

  CLEAR_m_pt_eta_phi_p4(mu_1);
  CLEAR_m_pt_eta_phi_p4(mu_2);
  CLEAR_m_pt_eta_phi_p4(ele_1);
  CLEAR_m_pt_eta_phi_p4(ele_2);

  n_mu_loose  = 0;
  n_ele_loose = 0;

  CLEAR_m_pt_ptRegressed_eta_phi_DeepJet_p4(bjet1);
  CLEAR_m_pt_ptRegressed_eta_phi_DeepJet_p4(bjet2);

  bjet1_hadflav = -999;
  bjet2_hadflav = -999;

  btagSF_WP_M = -999.;

  // reset all user-defined branches
  userFloats_.resetAll();
  userInts_.resetAll();

}

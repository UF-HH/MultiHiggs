#include "OutputTree.h"

#include <iostream>

using namespace std;

// helper: creates the pt/eta/phi/p4 branches of a variable OBJ
#define BRANCH_m_pt_eta_phi_p4(OBJ)       \
  tree_->Branch(#OBJ "_m", &OBJ##_m);     \
  tree_->Branch(#OBJ "_pt", &OBJ##_pt);   \
  tree_->Branch(#OBJ "_eta", &OBJ##_eta); \
  tree_->Branch(#OBJ "_phi", &OBJ##_phi); \
  if (savetlv_)                           \
    tree_->Branch(#OBJ "_p4", &OBJ##_p4);

#define CLEAR_m_pt_eta_phi_p4(OBJ) \
  OBJ##_m = -999.;                 \
  OBJ##_pt = -999.;                \
  OBJ##_eta = -999.;               \
  OBJ##_phi = -999.;               \
  OBJ##_p4.SetCoordinates(0, 0, 0, 0);

  
// helper: creates the pt/eta/phi/p4 branches of a variable OBJ
#define BRANCH_m_pt_eta_phi_score_p4(OBJ)     \
  tree_->Branch(#OBJ "_m", &OBJ##_m);         \
  tree_->Branch(#OBJ "_pt", &OBJ##_pt);       \
  tree_->Branch(#OBJ "_eta", &OBJ##_eta);     \
  tree_->Branch(#OBJ "_phi", &OBJ##_phi);     \
  tree_->Branch(#OBJ "_score", &OBJ##_score); \
  if (savetlv_)                               \
    tree_->Branch(#OBJ "_p4", &OBJ##_p4);

#define CLEAR_m_pt_eta_phi_score_p4(OBJ) \
  OBJ##_m = -999.;                       \
  OBJ##_pt = -999.;                      \
  OBJ##_eta = -999.;                     \
  OBJ##_phi = -999.;                     \
  OBJ##_score = -999.;                   \
  OBJ##_p4.SetCoordinates(0, 0, 0, 0);

#define BRANCH_m_pt_ptRegressed_eta_phi_p4(OBJ)           \
  tree_->Branch(#OBJ "_m", &OBJ##_m);                     \
  tree_->Branch(#OBJ "_mRegressed", &OBJ##_mRegressed);   \
  tree_->Branch(#OBJ "_pt", &OBJ##_pt);                   \
  tree_->Branch(#OBJ "_ptRegressed", &OBJ##_ptRegressed); \
  tree_->Branch(#OBJ "_eta", &OBJ##_eta);                 \
  tree_->Branch(#OBJ "_phi", &OBJ##_phi);                 \
  if (savetlv_)                                           \
    tree_->Branch(#OBJ "_p4", &OBJ##_p4);

#define CLEAR_m_pt_ptRegressed_eta_phi_p4(OBJ) \
  OBJ##_m = -999.;                             \
  OBJ##_mRegressed = -999.;                    \
  OBJ##_pt = -999.;                            \
  OBJ##_ptRegressed = -999.;                   \
  OBJ##_eta = -999.;                           \
  OBJ##_phi = -999.;                           \
  OBJ##_p4.SetCoordinates(0, 0, 0, 0);

#define BRANCH_m_pt_ptRegressed_eta_phi_DeepJet_p4(OBJ)   \
  tree_->Branch(#OBJ "_m", &OBJ##_m);                     \
  tree_->Branch(#OBJ "_mRegressed", &OBJ##_mRegressed);   \
  tree_->Branch(#OBJ "_pt", &OBJ##_pt);                   \
  tree_->Branch(#OBJ "_ptRegressed", &OBJ##_ptRegressed); \
  tree_->Branch(#OBJ "_eta", &OBJ##_eta);                 \
  tree_->Branch(#OBJ "_phi", &OBJ##_phi);                 \
  tree_->Branch(#OBJ "_btag", &OBJ##_btag);               \
  if (savetlv_)                                           \
    tree_->Branch(#OBJ "_p4", &OBJ##_p4);

#define CLEAR_m_pt_ptRegressed_eta_phi_DeepJet_p4(OBJ) \
  OBJ##_m = -999.;                                     \
  OBJ##_mRegressed = -999.;                            \
  OBJ##_pt = -999.;                                    \
  OBJ##_ptRegressed = -999.;                           \
  OBJ##_eta = -999.;                                   \
  OBJ##_phi = -999.;                                   \
  OBJ##_btag = -999.;                                  \
  OBJ##_p4.SetCoordinates(0, 0, 0, 0);

#define BRANCH_m_pt_ptRegressed_eta_phi_DeepJet_score_p4(OBJ) \
  tree_->Branch(#OBJ "_m", &OBJ##_m);                         \
  tree_->Branch(#OBJ "_mRegressed", &OBJ##_mRegressed);       \
  tree_->Branch(#OBJ "_pt", &OBJ##_pt);                       \
  tree_->Branch(#OBJ "_ptRegressed", &OBJ##_ptRegressed);     \
  tree_->Branch(#OBJ "_eta", &OBJ##_eta);                     \
  tree_->Branch(#OBJ "_phi", &OBJ##_phi);                     \
  tree_->Branch(#OBJ "_btag", &OBJ##_btag);                   \
  tree_->Branch(#OBJ "_score", &OBJ##_score);                 \
  if (savetlv_)                                               \
    tree_->Branch(#OBJ "_p4", &OBJ##_p4);

#define CLEAR_m_pt_ptRegressed_eta_phi_DeepJet_score_p4(OBJ) \
  OBJ##_m = -999.;                                           \
  OBJ##_mRegressed = -999.;                                  \
  OBJ##_pt = -999.;                                          \
  OBJ##_ptRegressed = -999.;                                 \
  OBJ##_eta = -999.;                                         \
  OBJ##_phi = -999.;                                         \
  OBJ##_btag = -999.;                                        \
  OBJ##_score = -999.;                                       \
  OBJ##_p4.SetCoordinates(0, 0, 0, 0);

#define BRANCH_jet_list(OBJ)                              \
  tree_->Branch(#OBJ "_E", &OBJ##_E);                     \
  tree_->Branch(#OBJ "_m", &OBJ##_m);                     \
  tree_->Branch(#OBJ "_mRegressed", &OBJ##_mRegressed);   \
  tree_->Branch(#OBJ "_pt", &OBJ##_pt);                   \
  tree_->Branch(#OBJ "_ptRegressed", &OBJ##_ptRegressed); \
  tree_->Branch(#OBJ "_eta", &OBJ##_eta);                 \
  tree_->Branch(#OBJ "_phi", &OBJ##_phi);                 \
  tree_->Branch(#OBJ "_signalId", &OBJ##_signalId);       \
  tree_->Branch(#OBJ "_higgsIdx", &OBJ##_higgsIdx);       \
  tree_->Branch(#OBJ "_genIdx", &OBJ##_genIdx);           \
  tree_->Branch(#OBJ "_btag", &OBJ##_btag);               \
  tree_->Branch(#OBJ "_qgl", &OBJ##_qgl);                 \
  tree_->Branch(#OBJ "_id", &OBJ##_id);                   \
  tree_->Branch(#OBJ "_puid", &OBJ##_puid);

#define CLEAR_jet_list(OBJ)  \
  OBJ##_E.clear();           \
  OBJ##_m.clear();           \
  OBJ##_mRegressed.clear();  \
  OBJ##_pt.clear();          \
  OBJ##_ptRegressed.clear(); \
  OBJ##_eta.clear();         \
  OBJ##_phi.clear();         \
  OBJ##_partonFlav.clear();  \
  OBJ##_hadronFlav.clear();  \
  OBJ##_signalId.clear();    \
  OBJ##_higgsIdx.clear();    \
  OBJ##_genIdx.clear();      \
  OBJ##_btag.clear();        \
  OBJ##_qgl.clear();         \
  OBJ##_id.clear();          \
  OBJ##_puid.clear();

#define BRANCH_dijet_list(OBJ)                      \
  tree_->Branch(#OBJ "_pt", &OBJ##_pt);             \
  tree_->Branch(#OBJ "_eta", &OBJ##_eta);           \
  tree_->Branch(#OBJ "_phi", &OBJ##_phi);           \
  tree_->Branch(#OBJ "_m", &OBJ##_m);               \
  tree_->Branch(#OBJ "_E", &OBJ##_E);               \
  tree_->Branch(#OBJ "_dr", &OBJ##_dr);             \
  tree_->Branch(#OBJ "_signalId", &OBJ##_signalId); \
  tree_->Branch(#OBJ "_2j_score", &OBJ##_2j_score);

#define CLEAR_dijet_list(OBJ) \
  OBJ##_pt.clear();           \
  OBJ##_eta.clear();          \
  OBJ##_phi.clear();          \
  OBJ##_m.clear();            \
  OBJ##_E.clear();            \
  OBJ##_dr.clear();           \
  OBJ##_signalId.clear();     \
  OBJ##_2j_score.clear();

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

  if (is_enabled("sixb_brs"))
  {
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

      tree_->Branch("HX_b1_genHflag", &HX_b1_genHflag);
      tree_->Branch("HX_b2_genHflag", &HX_b2_genHflag);
      tree_->Branch("HY1_b1_genHflag", &HY1_b1_genHflag);
      tree_->Branch("HY1_b2_genHflag", &HY1_b2_genHflag);
      tree_->Branch("HY2_b1_genHflag", &HY2_b1_genHflag);
      tree_->Branch("HY2_b2_genHflag", &HY2_b2_genHflag);

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

    BRANCH_m_pt_eta_phi_p4(X);
    BRANCH_m_pt_eta_phi_p4(Y);
    BRANCH_m_pt_eta_phi_p4(HX);
    BRANCH_m_pt_eta_phi_p4(HY1);
    BRANCH_m_pt_eta_phi_p4(HY2);

    BRANCH_m_pt_ptRegressed_eta_phi_DeepJet_p4(HX_b1);
    BRANCH_m_pt_ptRegressed_eta_phi_DeepJet_p4(HX_b2);
    BRANCH_m_pt_ptRegressed_eta_phi_DeepJet_p4(HY1_b1);
    BRANCH_m_pt_ptRegressed_eta_phi_DeepJet_p4(HY1_b2);
    BRANCH_m_pt_ptRegressed_eta_phi_DeepJet_p4(HY2_b1);
    BRANCH_m_pt_ptRegressed_eta_phi_DeepJet_p4(HY2_b2);
  }

  if (is_enabled("eightb_brs"))
  {

    if (is_enabled("sig_gen_brs"))
    {
      BRANCH_m_pt_eta_phi_p4(gen_X_fc);
      BRANCH_m_pt_eta_phi_p4(gen_X);
      BRANCH_m_pt_eta_phi_p4(gen_Y1);
      BRANCH_m_pt_eta_phi_p4(gen_Y2);
      BRANCH_m_pt_eta_phi_p4(gen_H1Y1);
      BRANCH_m_pt_eta_phi_p4(gen_H2Y1);
      BRANCH_m_pt_eta_phi_p4(gen_H1Y2);
      BRANCH_m_pt_eta_phi_p4(gen_H2Y2);

      BRANCH_m_pt_eta_phi_p4(gen_H1Y1_b1);
      BRANCH_m_pt_eta_phi_p4(gen_H1Y1_b2);
      BRANCH_m_pt_eta_phi_p4(gen_H2Y1_b1);
      BRANCH_m_pt_eta_phi_p4(gen_H2Y1_b2);
      BRANCH_m_pt_eta_phi_p4(gen_H1Y2_b1);
      BRANCH_m_pt_eta_phi_p4(gen_H1Y2_b2);
      BRANCH_m_pt_eta_phi_p4(gen_H2Y2_b1);
      BRANCH_m_pt_eta_phi_p4(gen_H2Y2_b2);

      BRANCH_m_pt_eta_phi_p4(gen_H1Y1_b1_genjet);
      BRANCH_m_pt_eta_phi_p4(gen_H1Y1_b2_genjet);
      BRANCH_m_pt_eta_phi_p4(gen_H2Y1_b1_genjet);
      BRANCH_m_pt_eta_phi_p4(gen_H2Y1_b2_genjet);
      BRANCH_m_pt_eta_phi_p4(gen_H1Y2_b1_genjet);
      BRANCH_m_pt_eta_phi_p4(gen_H1Y2_b2_genjet);
      BRANCH_m_pt_eta_phi_p4(gen_H2Y2_b1_genjet);
      BRANCH_m_pt_eta_phi_p4(gen_H2Y2_b2_genjet);

      BRANCH_m_pt_ptRegressed_eta_phi_DeepJet_p4(gen_H1Y1_b1_recojet);
      BRANCH_m_pt_ptRegressed_eta_phi_DeepJet_p4(gen_H1Y1_b2_recojet);
      BRANCH_m_pt_ptRegressed_eta_phi_DeepJet_p4(gen_H2Y1_b1_recojet);
      BRANCH_m_pt_ptRegressed_eta_phi_DeepJet_p4(gen_H2Y1_b2_recojet);
      BRANCH_m_pt_ptRegressed_eta_phi_DeepJet_p4(gen_H1Y2_b1_recojet);
      BRANCH_m_pt_ptRegressed_eta_phi_DeepJet_p4(gen_H1Y2_b2_recojet);
      BRANCH_m_pt_ptRegressed_eta_phi_DeepJet_p4(gen_H2Y2_b1_recojet);
      BRANCH_m_pt_ptRegressed_eta_phi_DeepJet_p4(gen_H2Y2_b2_recojet);

      tree_->Branch("H1Y1_b1_genHflag", &H1Y1_b1_genHflag);
      tree_->Branch("H1Y1_b2_genHflag", &H1Y1_b2_genHflag);
      tree_->Branch("H2Y1_b1_genHflag", &H2Y1_b1_genHflag);
      tree_->Branch("H2Y1_b2_genHflag", &H2Y1_b2_genHflag);
      tree_->Branch("H1Y2_b1_genHflag", &H1Y2_b1_genHflag);
      tree_->Branch("H1Y2_b2_genHflag", &H1Y2_b2_genHflag);
      tree_->Branch("H2Y2_b1_genHflag", &H2Y2_b1_genHflag);
      tree_->Branch("H2Y2_b2_genHflag", &H2Y2_b2_genHflag);

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

    BRANCH_m_pt_eta_phi_p4(X);
    BRANCH_m_pt_eta_phi_p4(Y1);
    BRANCH_m_pt_eta_phi_p4(Y2);
    BRANCH_m_pt_eta_phi_score_p4(H1Y1);
    BRANCH_m_pt_eta_phi_score_p4(H2Y1);
    BRANCH_m_pt_eta_phi_score_p4(H1Y2);
    BRANCH_m_pt_eta_phi_score_p4(H2Y2);

    BRANCH_m_pt_ptRegressed_eta_phi_DeepJet_score_p4(H1Y1_b1);
    BRANCH_m_pt_ptRegressed_eta_phi_DeepJet_score_p4(H1Y1_b2);
    BRANCH_m_pt_ptRegressed_eta_phi_DeepJet_score_p4(H2Y1_b1);
    BRANCH_m_pt_ptRegressed_eta_phi_DeepJet_score_p4(H2Y1_b2);
    BRANCH_m_pt_ptRegressed_eta_phi_DeepJet_score_p4(H1Y2_b1);
    BRANCH_m_pt_ptRegressed_eta_phi_DeepJet_score_p4(H1Y2_b2);
    BRANCH_m_pt_ptRegressed_eta_phi_DeepJet_score_p4(H2Y2_b1);
    BRANCH_m_pt_ptRegressed_eta_phi_DeepJet_score_p4(H2Y2_b2);

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
  tree_->Branch("n_jet", &n_jet);

  if (is_enabled("jet_coll"))
    {
      std::cout << "[INFO] OutputTree : enabling jet collection branches" << std::endl;

      BRANCH_jet_list(jet);
      tree_->Branch("b_6j_score",    &b_6j_score);
    }

  if (is_enabled("dijet_coll"))
  {
    std::cout << "[INFO] OutputTree : enabling dijet collection branches" << std::endl;

    tree_->Branch("n_dijet", &n_dijet);
    tree_->Branch("dijet_m", &dijet_m);
    tree_->Branch("dijet_pt", &dijet_pt);
    tree_->Branch("dijet_eta", &dijet_eta);
    tree_->Branch("dijet_phi", &dijet_phi);
    tree_->Branch("dijet_dr", &dijet_dr);
    tree_->Branch("dijet_score", &dijet_score);
    tree_->Branch("dijet_signalId", &dijet_signalId);
    tree_->Branch("dijet_j1Idx", &dijet_j1Idx);
    tree_->Branch("dijet_j2Idx", &dijet_j2Idx);
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
        tree_->Branch("genjet_E", &genjet_E);
        tree_->Branch("genjet_m", &genjet_m);
        tree_->Branch("genjet_pt", &genjet_pt);
        tree_->Branch("genjet_eta", &genjet_eta);
        tree_->Branch("genjet_phi", &genjet_phi);
        tree_->Branch("genjet_partonFlav", &genjet_partonFlav);
        tree_->Branch("genjet_hadronFlav", &genjet_hadronFlav);
        tree_->Branch("genjet_signalId", &genjet_signalId);
        tree_->Branch("genjet_recoIdx", &genjet_recoIdx);
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

  n_other_pv     = 0;
  n_pu           = 0;
  n_true_int     = 0;
  rhofastjet_all = 0;

  n_jet = 0;
  n_genjet = 0;
  n_higgs = 0;

  b_6j_score = 0;
  b_3d_score = 0;

  genjet_E.clear();	    
  genjet_m.clear();		
  genjet_pt.clear();		
  genjet_eta.clear();		
  genjet_phi.clear();		
  genjet_partonFlav.clear();
  genjet_hadronFlav.clear();
  genjet_signalId.clear();
  genjet_recoIdx.clear();

  CLEAR_jet_list(jet);

  n_dijet = 0;
  dijet_m.clear();
  dijet_pt.clear();
  dijet_eta.clear();
  dijet_phi.clear();
  dijet_dr.clear();
  dijet_score.clear();
  dijet_signalId.clear();
  dijet_j1Idx.clear();
  dijet_j2Idx.clear();

  CLEAR_m_pt_eta_phi_p4(gen_X_fc);
  CLEAR_m_pt_eta_phi_p4(gen_X);

  // Start Gen 6B Objects
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
  // End Gen 6B Objects

  // Start Gen 8B Objects 
  CLEAR_m_pt_eta_phi_p4(gen_Y1);
  CLEAR_m_pt_eta_phi_p4(gen_Y2);
  CLEAR_m_pt_eta_phi_p4(gen_H1Y1);
  CLEAR_m_pt_eta_phi_p4(gen_H2Y1);
  CLEAR_m_pt_eta_phi_p4(gen_H1Y2);
  CLEAR_m_pt_eta_phi_p4(gen_H2Y2);

  CLEAR_m_pt_eta_phi_p4(gen_H1Y1_b1);
  CLEAR_m_pt_eta_phi_p4(gen_H1Y1_b2);
  CLEAR_m_pt_eta_phi_p4(gen_H2Y1_b1);
  CLEAR_m_pt_eta_phi_p4(gen_H2Y1_b2);
  CLEAR_m_pt_eta_phi_p4(gen_H1Y2_b1);
  CLEAR_m_pt_eta_phi_p4(gen_H1Y2_b2);
  CLEAR_m_pt_eta_phi_p4(gen_H2Y2_b1);
  CLEAR_m_pt_eta_phi_p4(gen_H2Y2_b2);
  
  CLEAR_m_pt_eta_phi_p4(gen_H1Y1_b1_genjet);
  CLEAR_m_pt_eta_phi_p4(gen_H1Y1_b2_genjet);
  CLEAR_m_pt_eta_phi_p4(gen_H2Y1_b1_genjet);
  CLEAR_m_pt_eta_phi_p4(gen_H2Y1_b2_genjet);
  CLEAR_m_pt_eta_phi_p4(gen_H1Y2_b1_genjet);
  CLEAR_m_pt_eta_phi_p4(gen_H1Y2_b2_genjet);
  CLEAR_m_pt_eta_phi_p4(gen_H2Y2_b1_genjet);
  CLEAR_m_pt_eta_phi_p4(gen_H2Y2_b2_genjet);
  
  CLEAR_m_pt_ptRegressed_eta_phi_DeepJet_p4(gen_H1Y1_b1_recojet);
  CLEAR_m_pt_ptRegressed_eta_phi_DeepJet_p4(gen_H1Y1_b2_recojet);
  CLEAR_m_pt_ptRegressed_eta_phi_DeepJet_p4(gen_H2Y1_b1_recojet);
  CLEAR_m_pt_ptRegressed_eta_phi_DeepJet_p4(gen_H2Y1_b2_recojet);
  CLEAR_m_pt_ptRegressed_eta_phi_DeepJet_p4(gen_H1Y2_b1_recojet);
  CLEAR_m_pt_ptRegressed_eta_phi_DeepJet_p4(gen_H1Y2_b2_recojet);
  CLEAR_m_pt_ptRegressed_eta_phi_DeepJet_p4(gen_H2Y2_b1_recojet);
  CLEAR_m_pt_ptRegressed_eta_phi_DeepJet_p4(gen_H2Y2_b2_recojet);
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

  CLEAR_m_pt_eta_phi_p4(X);
  // Start Reco 6B Objects
  CLEAR_m_pt_eta_phi_p4(Y);
  CLEAR_m_pt_eta_phi_p4(HX);
  CLEAR_m_pt_eta_phi_p4(HY1);
  CLEAR_m_pt_eta_phi_p4(HY2);

  CLEAR_m_pt_ptRegressed_eta_phi_DeepJet_p4(HX_b1);
  CLEAR_m_pt_ptRegressed_eta_phi_DeepJet_p4(HX_b2);
  CLEAR_m_pt_ptRegressed_eta_phi_DeepJet_p4(HY1_b1);
  CLEAR_m_pt_ptRegressed_eta_phi_DeepJet_p4(HY1_b2);
  CLEAR_m_pt_ptRegressed_eta_phi_DeepJet_p4(HY2_b1);
  CLEAR_m_pt_ptRegressed_eta_phi_DeepJet_p4(HY2_b2);

  HX_b1_genHflag  = -999;
  HX_b2_genHflag  = -999;
  HY1_b1_genHflag = -999;
  HY1_b2_genHflag = -999;
  HY2_b1_genHflag = -999;
  HY2_b2_genHflag = -999;
  // End Reco 6B Objects

  // Start Reco 8B Objects
  CLEAR_m_pt_eta_phi_p4(Y);
  CLEAR_m_pt_eta_phi_p4(HX);
  CLEAR_m_pt_eta_phi_p4(HY1);
  CLEAR_m_pt_eta_phi_p4(HY2);

  CLEAR_m_pt_ptRegressed_eta_phi_DeepJet_p4(HX_b1);
  CLEAR_m_pt_ptRegressed_eta_phi_DeepJet_p4(HX_b2);
  CLEAR_m_pt_ptRegressed_eta_phi_DeepJet_p4(HY1_b1);
  CLEAR_m_pt_ptRegressed_eta_phi_DeepJet_p4(HY1_b2);
  CLEAR_m_pt_ptRegressed_eta_phi_DeepJet_p4(HY2_b1);
  CLEAR_m_pt_ptRegressed_eta_phi_DeepJet_p4(HY2_b2);

  HX_b1_genHflag = -999;
  HX_b2_genHflag = -999;
  HY1_b1_genHflag = -999;
  HY1_b2_genHflag = -999;
  HY2_b1_genHflag = -999;
  HY2_b2_genHflag = -999;
  // End Reco 8B Objects

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

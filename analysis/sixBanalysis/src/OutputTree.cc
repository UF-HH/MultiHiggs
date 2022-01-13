#include "OutputTree.h"

#include <iostream>

using namespace std;

// helper: creates the pt/eta/phi/p4 branches of a variable OBJ
#define BRANCH_m_pt_eta_phi_p4(OBJ) \
    tree_->Branch(#OBJ "_m",  &OBJ ## _m); \
    tree_->Branch(#OBJ "_pt",  &OBJ ## _pt); \
    tree_->Branch(#OBJ "_eta", &OBJ ## _eta); \
    tree_->Branch(#OBJ "_phi", &OBJ ## _phi); \
    if (savetlv_) tree_->Branch(#OBJ "_p4", &OBJ ## _p4);

#define CLEAR_m_pt_eta_phi_p4(OBJ) \
    OBJ ## _m    = -999.; \
    OBJ ## _pt   = -999.; \
    OBJ ## _eta  = -999.; \
    OBJ ## _phi  = -999.; \
    OBJ ## _p4 . SetCoordinates(0,0,0,0);

#define BRANCH_m_pt_ptRegressed_eta_phi_p4(OBJ) \
    tree_->Branch(#OBJ "_m"          ,  &OBJ ## _m); \
    tree_->Branch(#OBJ "_pt"         ,  &OBJ ## _pt); \
    tree_->Branch(#OBJ "_ptRegressed",  &OBJ ## _ptRegressed); \
    tree_->Branch(#OBJ "_eta"        , &OBJ ## _eta); \
    tree_->Branch(#OBJ "_phi"        , &OBJ ## _phi); \
    tree_->Branch(#OBJ "_deepJet"    , &OBJ ## _deepJet); \
    if (savetlv_) tree_->Branch(#OBJ "_p4", &OBJ ## _p4);

#define CLEAR_m_pt_ptRegressed_eta_phi_p4(OBJ) \
    OBJ ## _m             = -999.; \
    OBJ ## _pt            = -999.; \
    OBJ ## _ptRegressed   = -999.; \
    OBJ ## _eta           = -999.; \
    OBJ ## _phi           = -999.; \
    OBJ ## _deepJet       = -999.; \
    OBJ ## _p4            . SetCoordinates(0,0,0,0);


OutputTree::OutputTree (bool savetlv, string name, string title) :
savetlv_ (savetlv)
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
    tree_->Branch("njet",    &njet);

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

        tree_->Branch("HX_b1_genHflag",  &HX_b1_genHflag);
        tree_->Branch("HX_b2_genHflag",  &HX_b2_genHflag);
        tree_->Branch("HY1_b1_genHflag", &HY1_b1_genHflag);
        tree_->Branch("HY1_b2_genHflag", &HY1_b2_genHflag);
        tree_->Branch("HY2_b1_genHflag", &HY2_b1_genHflag);
        tree_->Branch("HY2_b2_genHflag", &HY2_b2_genHflag);

        tree_->Branch("nsel_from_H", &nsel_from_H);
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

    if (is_enabled("gen_brs"))
    {
        std::cout << "[INFO] OutputTree : enabling gen-only related branches" << std::endl;
        tree_->Branch("n_pu",        &n_pu);
        tree_->Branch("n_true_int",  &n_true_int);

        tree_->Branch("btagSF_WP_M", &btagSF_WP_M);
    }

    // note that the initialization of the user branches is made separately when calling declareUser*Branch
}

void OutputTree::clear()
{
    Run     = 0;
    LumiSec = 0;
    Event   = 0;
    njet    = 0;

    n_other_pv     = 0;
    n_pu           = 0;
    n_true_int     = 0;
    rhofastjet_all = 0;

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

    HX_b1_genHflag  = -999;
    HX_b2_genHflag  = -999;
    HY1_b1_genHflag = -999;
    HY1_b2_genHflag = -999;
    HY2_b1_genHflag = -999;
    HY2_b2_genHflag = -999;

    nsel_from_H = -999;

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
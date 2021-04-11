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
    if (savetlv_) tree_->Branch(#OBJ "_p4", &OBJ ## _p4);

#define CLEAR_m_pt_ptRegressed_eta_phi_p4(OBJ) \
    OBJ ## _m             = -999.; \
    OBJ ## _pt            = -999.; \
    OBJ ## _ptRegressed   = -999.; \
    OBJ ## _eta           = -999.; \
    OBJ ## _phi           = -999.; \
    OBJ ## _p4            . SetCoordinates(0,0,0,0);

#define BRANCH_m_pt_ptRegressed_eta_phi_DeepJet_p4(OBJ) \
    tree_->Branch(#OBJ "_m"          ,  &OBJ ## _m); \
    tree_->Branch(#OBJ "_pt"         ,  &OBJ ## _pt); \
    tree_->Branch(#OBJ "_ptRegressed",  &OBJ ## _ptRegressed); \
    tree_->Branch(#OBJ "_eta"        , &OBJ ## _eta); \
    tree_->Branch(#OBJ "_phi"        , &OBJ ## _phi); \
    tree_->Branch(#OBJ "_DeepJet"    , &OBJ ## _DeepJet); \
    if (savetlv_) tree_->Branch(#OBJ "_p4", &OBJ ## _p4);

#define CLEAR_m_pt_ptRegressed_eta_phi_DeepJet_p4(OBJ) \
    OBJ ## _m             = -999.; \
    OBJ ## _pt            = -999.; \
    OBJ ## _ptRegressed   = -999.; \
    OBJ ## _eta           = -999.; \
    OBJ ## _phi           = -999.; \
    OBJ ## _DeepJet       = -999.; \
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
    //event information
    tree_->Branch("Run",     &Run);
    tree_->Branch("LumiSec", &LumiSec);
    tree_->Branch("Event",   &Event);

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

    tree_->Branch("n_mu_loose",  &n_mu_loose);
    tree_->Branch("n_ele_loose", &n_ele_loose);

    auto is_enabled = [&branch_switches](std::string opt) -> bool {
        auto search = branch_switches.find(opt);
        if (search == branch_switches.end())
            return true; // if no opt given, enabled by default
        return search->second; // otherwise, use the value of the option
    };
    
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
        BRANCH_m_pt_ptRegressed_eta_phi_DeepJet_p4(bjet2);
    }

    // note that the initialization of the user branches is made separately when calling declareUser*Branch
}

void OutputTree::clear()
{
    Run     = 0;
    LumiSec = 0;
    Event   = 0;

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

    // reset all user-defined branches
    userFloats_.resetAll();
    userInts_.resetAll();

}
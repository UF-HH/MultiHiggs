#ifndef OUTPUTTREE_H
#define OUTPUTTREE_H

/**
 ** class  : OutputTree
 ** author : L. Cadamuro (UF)
 ** date   : 10/01/2018
 ** brief  : the output tree of the skims
 ** NOTE   : for every new variable added:
 **        : 1) add the member variable
 **        : 2) add the corresponing branch in init_branches()
 **        : 3) set the variable clearing in clear()
 **        :
 **        : remember that the variables are set (from the EventInfo) in the SkimUtils::fill_output_tree function
 **        : so put the set instructions of the new variables there
 **
 **  NOTE 2 : handling of tree pointer and userFloat/int is done in the BaseOutTree class
 **         : so OutputTree only takes care of defining and resetting the outout variables
 **/

#include "BaseOutTree.h"
#include "TTree.h"
#include "Math/Vector4D.h"
typedef ROOT::Math::PtEtaPhiMVector p4_t;

#include "UserValCollection.h"
#include <string>
#include <memory>
#include <map>

// helper: declares the m/pt/eta/phi/p4 of a variable OBJ
#define DECLARE_m_pt_eta_phi_p4(OBJ) \
  float OBJ##_m;                     \
  float OBJ##_pt;                    \
  float OBJ##_eta;                   \
  float OBJ##_phi;                   \
  p4_t OBJ##_p4;

// helper: declares the m/pt/eta/phi/p4 of a variable OBJ
#define DECLARE_m_pt_eta_phi_score_p4(OBJ) \
  float OBJ##_m;                           \
  float OBJ##_pt;                          \
  float OBJ##_eta;                         \
  float OBJ##_phi;                         \
  float OBJ##_score;                       \
  p4_t OBJ##_p4;

// helper: declares the m/pt/eta/phi/p4 of a variable OBJ
#define DECLARE_m_pt_ptRegressed_eta_phi_p4(OBJ) \
  float OBJ##_m;                                 \
  float OBJ##_mRegressed;                        \
  float OBJ##_pt;                                \
  float OBJ##_ptRegressed;                       \
  float OBJ##_eta;                               \
  float OBJ##_phi;                               \
  p4_t OBJ##_p4;

// helper: declares the m/pt/eta/phi/p4/DeepJet of a variable OBJ
#define DECLARE_m_pt_ptRegressed_eta_phi_DeepJet_p4(OBJ) \
  float OBJ##_m;                                         \
  float OBJ##_mRegressed;                                \
  float OBJ##_pt;                                        \
  float OBJ##_ptRegressed;                               \
  float OBJ##_eta;                                       \
  float OBJ##_phi;                                       \
  float OBJ##_btag;                                      \
  p4_t OBJ##_p4;


// helper: declares the m/pt/eta/phi/p4/DeepJet of a variable OBJ
#define DECLARE_m_pt_ptRegressed_eta_phi_DeepJet_score_p4(OBJ) \
  float OBJ##_m;                                               \
  float OBJ##_mRegressed;                                      \
  float OBJ##_pt;                                              \
  float OBJ##_ptRegressed;                                     \
  float OBJ##_eta;                                             \
  float OBJ##_phi;                                             \
  float OBJ##_btag;                                            \
  float OBJ##_score;                                           \
  p4_t OBJ##_p4;

#define DECLARE_jet_list(OBJ)           \
  std::vector<float> OBJ##_E;           \
  std::vector<float> OBJ##_m;           \
  std::vector<float> OBJ##_mRegressed;  \
  std::vector<float> OBJ##_pt;          \
  std::vector<float> OBJ##_ptRegressed; \
  std::vector<float> OBJ##_eta;         \
  std::vector<float> OBJ##_phi;         \
  std::vector<int> OBJ##_partonFlav;    \
  std::vector<int> OBJ##_hadronFlav;    \
  std::vector<int> OBJ##_signalId;      \
  std::vector<int> OBJ##_higgsIdx;      \
  std::vector<int> OBJ##_genIdx;        \
  std::vector<float> OBJ##_btag;        \
  std::vector<float> OBJ##_qgl;         \
  std::vector<int> OBJ##_id;            \
  std::vector<int> OBJ##_puid;

#define DECLARE_dijet_list(OBJ)    \
  std::vector<float> OBJ##_pt;     \
  std::vector<float> OBJ##_eta;    \
  std::vector<float> OBJ##_phi;    \
  std::vector<float> OBJ##_m;      \
  std::vector<float> OBJ##_E;      \
  std::vector<float> OBJ##_dr;     \
  std::vector<int> OBJ##_signalId; \
  std::vector<float> OBJ##_2j_score;

class OutputTree : public BaseOutTree {
    
public:
  // branch_switches are forwarded to init_branches
  // they can be used to turn on (true) or off (false) some branches creation

  OutputTree(bool savetlv = false, std::map<std::string, bool> branch_switches = {}, std::string name = "sixBtree", std::string title = "sixBtree");
  ~OutputTree(){};
        
  void clear(); // to be called to reset the var values
  // int fill()  {return tree_->Fill();}
  // int write() {return tree_->Write();}
    
  // // returns false if the branch could not be created, true if all ok
  // // thje second optional value specifies what the branch should be reset to at clear()
  // bool declareUserIntBranch   (std::string name, int defaultClearValue = 0);
  // bool declareUserFloatBranch (std::string name, float defaultClearValue = 0.0);
  // //XYH
  // bool declareUserIntBranchList(std::vector<std::string> nameList, int defaultClearValue = 0);

  // // throws an exception if the branch name was not declared
  // int&   userInt   (std::string name) {return userInts_   . getVal(name);}
  // float& userFloat (std::string name) {return userFloats_ . getVal(name);}

  //////////////////////////
  //// saved variables
  //////////////////////////

  unsigned int           Run;
  unsigned int           LumiSec;
  unsigned long long int Event;

  int    n_other_pv;
  int    n_pu;
  double n_true_int;
  double rhofastjet_all;
  double lhe_ht;

  int n_genjet;
  int n_total_jet;
  int n_jet;
  int n_higgs;

  float b_6j_score;
  float b_3d_score;

  std::vector<float> genjet_E;	    
  std::vector<float> genjet_m;		
  std::vector<float> genjet_pt;		
  std::vector<float> genjet_eta;		
  std::vector<float> genjet_phi;		
  std::vector<int> genjet_partonFlav;
  std::vector<int> genjet_hadronFlav;
  std::vector<int> genjet_signalId;
  std::vector<int> genjet_recoIdx;

  DECLARE_jet_list(jet);

  int n_dijet;
  std::vector<float> dijet_m;
  std::vector<float> dijet_pt;
  std::vector<float> dijet_eta;
  std::vector<float> dijet_phi;
  std::vector<float> dijet_dr;
  std::vector<float> dijet_score;
  std::vector<int> dijet_signalId;
  std::vector<int> dijet_j1Idx;
  std::vector<int> dijet_j2Idx;

  float sphericity;
  float sphericity_t;
  float aplanarity;

  DECLARE_m_pt_eta_phi_p4(gen_X_fc);
  DECLARE_m_pt_eta_phi_p4(gen_X);
  // Start Gen 6B Objects
  DECLARE_m_pt_eta_phi_p4(gen_Y);
  DECLARE_m_pt_eta_phi_p4(gen_HX);
  DECLARE_m_pt_eta_phi_p4(gen_HY1);
  DECLARE_m_pt_eta_phi_p4(gen_HY2);

  DECLARE_m_pt_eta_phi_p4(gen_HX_b1);
  DECLARE_m_pt_eta_phi_p4(gen_HX_b2);
  DECLARE_m_pt_eta_phi_p4(gen_HY1_b1);
  DECLARE_m_pt_eta_phi_p4(gen_HY1_b2);
  DECLARE_m_pt_eta_phi_p4(gen_HY2_b1);
  DECLARE_m_pt_eta_phi_p4(gen_HY2_b2);

  DECLARE_m_pt_eta_phi_p4(gen_HX_b1_genjet);
  DECLARE_m_pt_eta_phi_p4(gen_HX_b2_genjet);
  DECLARE_m_pt_eta_phi_p4(gen_HY1_b1_genjet);
  DECLARE_m_pt_eta_phi_p4(gen_HY1_b2_genjet);
  DECLARE_m_pt_eta_phi_p4(gen_HY2_b1_genjet);
  DECLARE_m_pt_eta_phi_p4(gen_HY2_b2_genjet);

  DECLARE_m_pt_ptRegressed_eta_phi_p4(gen_HX_b1_recojet);
  DECLARE_m_pt_ptRegressed_eta_phi_p4(gen_HX_b2_recojet);
  DECLARE_m_pt_ptRegressed_eta_phi_p4(gen_HY1_b1_recojet);
  DECLARE_m_pt_ptRegressed_eta_phi_p4(gen_HY1_b2_recojet);
  DECLARE_m_pt_ptRegressed_eta_phi_p4(gen_HY2_b1_recojet);
  DECLARE_m_pt_ptRegressed_eta_phi_p4(gen_HY2_b2_recojet);
  // End Gen 6B Objects

  
  // Gen 8B Objects
  DECLARE_m_pt_eta_phi_p4(gen_Y1);
  DECLARE_m_pt_eta_phi_p4(gen_Y2);
  DECLARE_m_pt_eta_phi_p4(gen_H1Y1);
  DECLARE_m_pt_eta_phi_p4(gen_H2Y1);
  DECLARE_m_pt_eta_phi_p4(gen_H1Y2);
  DECLARE_m_pt_eta_phi_p4(gen_H2Y2);

  DECLARE_m_pt_eta_phi_p4(gen_H1Y1_b1);
  DECLARE_m_pt_eta_phi_p4(gen_H1Y1_b2);
  DECLARE_m_pt_eta_phi_p4(gen_H2Y1_b1);
  DECLARE_m_pt_eta_phi_p4(gen_H2Y1_b2);
  DECLARE_m_pt_eta_phi_p4(gen_H1Y2_b1);
  DECLARE_m_pt_eta_phi_p4(gen_H1Y2_b2);
  DECLARE_m_pt_eta_phi_p4(gen_H2Y2_b1);
  DECLARE_m_pt_eta_phi_p4(gen_H2Y2_b2);
  
  DECLARE_m_pt_eta_phi_p4(gen_H1Y1_b1_genjet);
  DECLARE_m_pt_eta_phi_p4(gen_H1Y1_b2_genjet);
  DECLARE_m_pt_eta_phi_p4(gen_H2Y1_b1_genjet);
  DECLARE_m_pt_eta_phi_p4(gen_H2Y1_b2_genjet);
  DECLARE_m_pt_eta_phi_p4(gen_H1Y2_b1_genjet);
  DECLARE_m_pt_eta_phi_p4(gen_H1Y2_b2_genjet);
  DECLARE_m_pt_eta_phi_p4(gen_H2Y2_b1_genjet);
  DECLARE_m_pt_eta_phi_p4(gen_H2Y2_b2_genjet);
  
  DECLARE_m_pt_ptRegressed_eta_phi_DeepJet_p4(gen_H1Y1_b1_recojet);
  DECLARE_m_pt_ptRegressed_eta_phi_DeepJet_p4(gen_H1Y1_b2_recojet);
  DECLARE_m_pt_ptRegressed_eta_phi_DeepJet_p4(gen_H2Y1_b1_recojet);
  DECLARE_m_pt_ptRegressed_eta_phi_DeepJet_p4(gen_H2Y1_b2_recojet);
  DECLARE_m_pt_ptRegressed_eta_phi_DeepJet_p4(gen_H1Y2_b1_recojet);
  DECLARE_m_pt_ptRegressed_eta_phi_DeepJet_p4(gen_H1Y2_b2_recojet);
  DECLARE_m_pt_ptRegressed_eta_phi_DeepJet_p4(gen_H2Y2_b1_recojet);
  DECLARE_m_pt_ptRegressed_eta_phi_DeepJet_p4(gen_H2Y2_b2_recojet);
  // End Gen 8B Objects
  
  int gen_bs_N_reco_match;
  int gen_bs_N_reco_match_in_acc;
  double gen_bs_match_recojet_minv;
  double gen_bs_match_in_acc_recojet_minv;

  DECLARE_m_pt_eta_phi_p4(X);
  // Start Reco 6B Objects
  DECLARE_m_pt_eta_phi_p4(Y);
  DECLARE_m_pt_eta_phi_p4(HX);
  DECLARE_m_pt_eta_phi_p4(HY1);
  DECLARE_m_pt_eta_phi_p4(HY2);

  DECLARE_m_pt_ptRegressed_eta_phi_DeepJet_p4(HX_b1);
  DECLARE_m_pt_ptRegressed_eta_phi_DeepJet_p4(HX_b2);
  DECLARE_m_pt_ptRegressed_eta_phi_DeepJet_p4(HY1_b1);
  DECLARE_m_pt_ptRegressed_eta_phi_DeepJet_p4(HY1_b2);
  DECLARE_m_pt_ptRegressed_eta_phi_DeepJet_p4(HY2_b1);
  DECLARE_m_pt_ptRegressed_eta_phi_DeepJet_p4(HY2_b2);

  int HX_b1_genHflag;
  int HX_b2_genHflag;
  int HY1_b1_genHflag;
  int HY1_b2_genHflag;
  int HY2_b1_genHflag;
  int HY2_b2_genHflag;
  // End Reco 6B Objects

  // Start Reco 8B Objects
  DECLARE_m_pt_eta_phi_p4(Y1);
  DECLARE_m_pt_eta_phi_p4(Y2);
  DECLARE_m_pt_eta_phi_score_p4(H1Y1);
  DECLARE_m_pt_eta_phi_score_p4(H2Y1);
  DECLARE_m_pt_eta_phi_score_p4(H1Y2);
  DECLARE_m_pt_eta_phi_score_p4(H2Y2);

  DECLARE_m_pt_ptRegressed_eta_phi_DeepJet_score_p4(H1Y1_b1);
  DECLARE_m_pt_ptRegressed_eta_phi_DeepJet_score_p4(H1Y1_b2);
  DECLARE_m_pt_ptRegressed_eta_phi_DeepJet_score_p4(H2Y1_b1);
  DECLARE_m_pt_ptRegressed_eta_phi_DeepJet_score_p4(H2Y1_b2);
  DECLARE_m_pt_ptRegressed_eta_phi_DeepJet_score_p4(H1Y2_b1);
  DECLARE_m_pt_ptRegressed_eta_phi_DeepJet_score_p4(H1Y2_b2);
  DECLARE_m_pt_ptRegressed_eta_phi_DeepJet_score_p4(H2Y2_b1);
  DECLARE_m_pt_ptRegressed_eta_phi_DeepJet_score_p4(H2Y2_b2);

  int H1Y1_b1_genHflag;
  int H1Y1_b2_genHflag;
  int H2Y1_b1_genHflag;
  int H2Y1_b2_genHflag;
  int H1Y2_b1_genHflag;
  int H1Y2_b2_genHflag;
  int H2Y2_b1_genHflag;
  int H2Y2_b2_genHflag;
  // End Reco 8B Objects


  int nfound_all;
  int nfound_all_h;
  int nfound_presel;
  int nfound_presel_h;
  int nfound_select;
  int nfound_select_h;
  int nfound_paired_h;

  DECLARE_m_pt_eta_phi_p4(mu_1);
  DECLARE_m_pt_eta_phi_p4(mu_2);
  DECLARE_m_pt_eta_phi_p4(ele_1);
  DECLARE_m_pt_eta_phi_p4(ele_2);

  int n_mu_loose;
  int n_ele_loose;

  DECLARE_m_pt_ptRegressed_eta_phi_DeepJet_p4(bjet1);
  int bjet1_hadflav;
        
  DECLARE_m_pt_ptRegressed_eta_phi_DeepJet_p4(bjet2);
  int bjet2_hadflav;

  double btagSF_WP_M;

private:
  void init_branches(std::map<std::string, bool> branch_switches);
  // std::unique_ptr<TTree> tree_;
  const bool savetlv_;
        
  // for user declared branches
  // UserValCollection<float> userFloats_;
  // UserValCollection<int>   userInts_;
};

#endif

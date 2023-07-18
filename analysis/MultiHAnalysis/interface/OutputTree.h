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

#include "CompositeCandidate.h"
#include "Jet.h"
#include "GenJet.h"
#include "GenPart.h"
#include "Muon.h"
#include "Electron.h"
#include "FatJet.h"
#include "GenJetAK8.h"

#include <string>
#include <memory>
#include <map>

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
  double PFHT;
  
  // Trigger scale factor branches
  float triggerScaleFactor;
  float triggerDataEfficiency;
  float triggerMcEfficiency;
  float triggerScaleFactorUp;
  float triggerDataEfficiencyUp;
  float triggerMcEfficiencyUp;
  float triggerScaleFactorDown;
  float triggerDataEfficiencyDown;
  float triggerMcEfficiencyDown;
  
  double lhe_ht;

  int n_genjet;
  int n_total_jet;
  int n_jet;
  int n_higgs;
  int n_fatjet;
  int n_genfatjet;
  
  int n_ele;
  int n_muon;
  
  float b_6j_score;
  float b_3d_score;

  GenPartListCollection genpb;
  GenJetListCollection genjet;
  GenJetAK8ListCollection genfatjet;
  
  ElectronListCollection ele;
  MuonListCollection muon;

  JetListCollection jet;
  FatJetListCollection fatjet;
  
  float sphericity;
  float sphericity_t;
  float aplanarity;

  GenPartCollection gen_H1_fc;
  GenPartCollection gen_H2_fc;
  GenJetAK8Collection gen_H1_b1_genfatjet = GenJetAK8Collection({"pt","m","eta","phi"});
  GenJetAK8Collection gen_H1_b2_genfatjet = GenJetAK8Collection({"pt","m","eta","phi"});
  GenJetAK8Collection gen_H2_b1_genfatjet = GenJetAK8Collection({"pt","m","eta","phi"});
  GenJetAK8Collection gen_H2_b2_genfatjet = GenJetAK8Collection({"pt","m","eta","phi"});
  FatJetCollection gen_H1_b1_recofatjet = FatJetCollection({"pt","m","eta","phi"});
  FatJetCollection gen_H1_b2_recofatjet = FatJetCollection({"pt","m","eta","phi"});
  FatJetCollection gen_H2_b1_recofatjet = FatJetCollection({"pt","m","eta","phi"});
  FatJetCollection gen_H2_b2_recofatjet = FatJetCollection({"pt","m","eta","phi"});
  
  GenPartCollection gen_X_fc;
  GenPartCollection gen_X;
  // Start Gen 6B Objects
  GenPartCollection gen_Y;
  GenPartCollection gen_HX;
  GenPartCollection gen_H1;
  GenPartCollection gen_H2;

  GenPartCollection gen_HX_b1;
  GenPartCollection gen_HX_b2;
  GenPartCollection gen_H1_b1;
  GenPartCollection gen_H1_b2;
  GenPartCollection gen_H2_b1;
  GenPartCollection gen_H2_b2;

  GenJetCollection gen_HX_b1_genjet = GenJetCollection({"pt","m","eta","phi"});
  GenJetCollection gen_HX_b2_genjet = GenJetCollection({"pt","m","eta","phi"});
  GenJetCollection gen_H1_b1_genjet = GenJetCollection({"pt","m","eta","phi"});
  GenJetCollection gen_H1_b2_genjet = GenJetCollection({"pt","m","eta","phi"});
  GenJetCollection gen_H2_b1_genjet = GenJetCollection({"pt","m","eta","phi"});
  GenJetCollection gen_H2_b2_genjet = GenJetCollection({"pt","m","eta","phi"});

  JetCollection gen_HX_b1_recojet = JetCollection({"pt","m","eta","phi","ptRegressed","mRegressed"});
  JetCollection gen_HX_b2_recojet = JetCollection({"pt","m","eta","phi","ptRegressed","mRegressed"});
  JetCollection gen_H1_b1_recojet = JetCollection({"pt","m","eta","phi","ptRegressed","mRegressed"});
  JetCollection gen_H1_b2_recojet = JetCollection({"pt","m","eta","phi","ptRegressed","mRegressed"});
  JetCollection gen_H2_b1_recojet = JetCollection({"pt","m","eta","phi","ptRegressed","mRegressed"});
  JetCollection gen_H2_b2_recojet = JetCollection({"pt","m","eta","phi","ptRegressed","mRegressed"});
  // End Gen 6B Objects

  
  // Gen 8B Objects
  GenPartCollection gen_Y1;
  GenPartCollection gen_Y2;
  GenPartCollection gen_H1Y1;
  GenPartCollection gen_H2Y1;
  GenPartCollection gen_H1Y2;
  GenPartCollection gen_H2Y2;

  GenPartCollection gen_H1Y1_b1;
  GenPartCollection gen_H1Y1_b2;
  GenPartCollection gen_H2Y1_b1;
  GenPartCollection gen_H2Y1_b2;
  GenPartCollection gen_H1Y2_b1;
  GenPartCollection gen_H1Y2_b2;
  GenPartCollection gen_H2Y2_b1;
  GenPartCollection gen_H2Y2_b2;
  
  GenJetCollection gen_H1Y1_b1_genjet;
  GenJetCollection gen_H1Y1_b2_genjet;
  GenJetCollection gen_H2Y1_b1_genjet;
  GenJetCollection gen_H2Y1_b2_genjet;
  GenJetCollection gen_H1Y2_b1_genjet;
  GenJetCollection gen_H1Y2_b2_genjet;
  GenJetCollection gen_H2Y2_b1_genjet;
  GenJetCollection gen_H2Y2_b2_genjet;
  
  JetCollection gen_H1Y1_b1_recojet = JetCollection({"pt","eta","phi","m","btag"});
  JetCollection gen_H1Y1_b2_recojet = JetCollection({"pt","eta","phi","m","btag"});
  JetCollection gen_H2Y1_b1_recojet = JetCollection({"pt","eta","phi","m","btag"});
  JetCollection gen_H2Y1_b2_recojet = JetCollection({"pt","eta","phi","m","btag"});
  JetCollection gen_H1Y2_b1_recojet = JetCollection({"pt","eta","phi","m","btag"});
  JetCollection gen_H1Y2_b2_recojet = JetCollection({"pt","eta","phi","m","btag"});
  JetCollection gen_H2Y2_b1_recojet = JetCollection({"pt","eta","phi","m","btag"});
  JetCollection gen_H2Y2_b2_recojet = JetCollection({"pt","eta","phi","m","btag"});
  // End Gen 8B Objects
  
  int gen_bs_N_reco_match;
  int gen_bs_N_reco_match_in_acc;
  double gen_bs_match_recojet_minv;
  double gen_bs_match_in_acc_recojet_minv;

  CompositeCandidateCollection X;
  // Start Reco 6B Objects
  CompositeCandidateCollection Y;
  CompositeCandidateCollection HX;
  CompositeCandidateCollection H1;
  CompositeCandidateCollection H2;

  JetCollection HX_b1 = JetCollection({"pt","eta","phi","m","btag"});
  JetCollection HX_b2 = JetCollection({"pt","eta","phi","m","btag"});
  JetCollection H1_b1 = JetCollection({"pt","eta","phi","m","btag"});
  JetCollection H1_b2 = JetCollection({"pt","eta","phi","m","btag"});
  JetCollection H2_b1 = JetCollection({"pt","eta","phi","m","btag"});
  JetCollection H2_b2 = JetCollection({"pt","eta","phi","m","btag"});

  int HX_b1_genHflag;
  int HX_b2_genHflag;
  int H1_b1_genHflag;
  int H1_b2_genHflag;
  int H2_b1_genHflag;
  int H2_b2_genHflag;
  // End Reco 6B Objects

  // Start Reco 8B Objects
  CompositeCandidateCollection Y1;
  CompositeCandidateCollection Y2;
  CompositeCandidateCollection H1Y1;
  CompositeCandidateCollection H2Y1;
  CompositeCandidateCollection H1Y2;
  CompositeCandidateCollection H2Y2;

  JetCollection H1Y1_b1 = JetCollection({"pt","eta","phi","m","btag"});
  JetCollection H1Y1_b2 = JetCollection({"pt","eta","phi","m","btag"});
  JetCollection H2Y1_b1 = JetCollection({"pt","eta","phi","m","btag"});
  JetCollection H2Y1_b2 = JetCollection({"pt","eta","phi","m","btag"});
  JetCollection H1Y2_b1 = JetCollection({"pt","eta","phi","m","btag"});
  JetCollection H1Y2_b2 = JetCollection({"pt","eta","phi","m","btag"});
  JetCollection H2Y2_b1 = JetCollection({"pt","eta","phi","m","btag"});
  JetCollection H2Y2_b2 = JetCollection({"pt","eta","phi","m","btag"});

  int n_loose_btag;
  int n_medium_btag;
  int n_tight_btag;
  float btagavg;
  // End Reco 8B Objects

  int nfound_all;
  int nfound_all_h;
  int nfound_presel;
  int nfound_presel_h;
  int nfound_select;
  int nfound_select_h;
  int nfound_paired_h;
  int nfound_select_y;
  int nfound_paired_y;
  
  //DECLARE_m_pt_ptRegressed_eta_phi_DeepJet_p4(bjet1);
  //int bjet1_hadflav;
  //DECLARE_m_pt_ptRegressed_eta_phi_DeepJet_p4(bjet2);
  //int bjet2_hadflav;

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

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

#define BRANCH_ele_list(OBJ)                                    \
  tree_->Branch(#OBJ "_E", &OBJ##_E);                           \
  tree_->Branch(#OBJ "_m", &OBJ##_m);                           \
  tree_->Branch(#OBJ "_pt", &OBJ##_pt);                         \
  tree_->Branch(#OBJ "_eta", &OBJ##_eta);                       \
  tree_->Branch(#OBJ "_phi", &OBJ##_phi);                       \
  tree_->Branch(#OBJ "_dxy", &OBJ##_dxy);                       \
  tree_->Branch(#OBJ "_dz",  &OBJ##_dz);                        \
  tree_->Branch(#OBJ "_charge", &OBJ##_charge);                 \
  tree_->Branch(#OBJ "_pfRelIso03_all", &OBJ##_pfRelIso03_all);           \
  tree_->Branch(#OBJ "_mvaFall17V2Iso_WPL", &OBJ##_mvaFall17V2Iso_WPL);   \
  tree_->Branch(#OBJ "_mvaFall17V2Iso_WP90", &OBJ##_mvaFall17V2Iso_WP90); \
  tree_->Branch(#OBJ "_mvaFall17V2Iso_WP80", &OBJ##_mvaFall17V2Iso_WP80); 

#define BRANCH_muon_list(OBJ)                                   \
  tree_->Branch(#OBJ "_E", &OBJ##_E);                           \
  tree_->Branch(#OBJ "_m", &OBJ##_m);                           \
  tree_->Branch(#OBJ "_pt", &OBJ##_pt);                         \
  tree_->Branch(#OBJ "_eta", &OBJ##_eta);                       \
  tree_->Branch(#OBJ "_phi", &OBJ##_phi);                       \
  tree_->Branch(#OBJ "_dxy", &OBJ##_dxy);                       \
  tree_->Branch(#OBJ "_dz",  &OBJ##_dz);                        \
  tree_->Branch(#OBJ "_charge", &OBJ##_charge);                 \
  tree_->Branch(#OBJ "_pfRelIso04_all", &OBJ##_pfRelIso04_all); \
  tree_->Branch(#OBJ "_isLoose", &OBJ##_looseId);               \
  tree_->Branch(#OBJ "_isMedium", &OBJ##_mediumId);             \
  tree_->Branch(#OBJ "_isTight", &OBJ##_tightId);

#define CLEAR_ele_list(OBJ)     \
  OBJ##_E.clear();              \
  OBJ##_m.clear();              \
  OBJ##_pt.clear();             \
  OBJ##_eta.clear();            \
  OBJ##_phi.clear();            \
  OBJ##_dxy.clear();            \
  OBJ##_dz.clear();             \
  OBJ##_charge.clear();         \
  OBJ##_pfRelIso03_all.clear(); \
  OBJ##_mvaFall17V2Iso_WPL.clear();  \
  OBJ##_mvaFall17V2Iso_WP90.clear(); \
  OBJ##_mvaFall17V2Iso_WP80.clear();

#define CLEAR_muon_list(OBJ)    \
  OBJ##_E.clear();              \
  OBJ##_m.clear();		\
  OBJ##_pt.clear();             \
  OBJ##_eta.clear();            \
  OBJ##_phi.clear();            \
  OBJ##_dxy.clear();            \
  OBJ##_dz.clear();             \
  OBJ##_charge.clear();         \
  OBJ##_pfRelIso04_all.clear(); \
  OBJ##_looseId.clear();        \
  OBJ##_mediumId.clear();       \
  OBJ##_tightId.clear();
  
#define BRANCH_fatjet_list(OBJ)            \
  tree_->Branch(#OBJ "_pt", &OBJ##_pt);    \
  tree_->Branch(#OBJ "_eta", &OBJ##_eta);  \
  tree_->Branch(#OBJ "_phi", &OBJ##_phi);  \
  tree_->Branch(#OBJ "_m", &OBJ##_m);	   \
  tree_->Branch(#OBJ "_mSD_UnCorrected", &OBJ##_mSD_UnCorrected);	\
  tree_->Branch(#OBJ "_area", &OBJ##_area);		\
  tree_->Branch(#OBJ "_n2b1", &OBJ##_n2b1);		\
  tree_->Branch(#OBJ "_n3b1", &OBJ##_n3b1);		\
  tree_->Branch(#OBJ "_rawFactor", &OBJ##_rawFactor);	\
  tree_->Branch(#OBJ "_tau1", &OBJ##_tau1);		\
  tree_->Branch(#OBJ "_tau2", &OBJ##_tau2);		\
  tree_->Branch(#OBJ "_tau3", &OBJ##_tau3);		\
  tree_->Branch(#OBJ "_tau4", &OBJ##_tau4);		\
  tree_->Branch(#OBJ "_jetId", &OBJ##_jetId);		\
  tree_->Branch(#OBJ "_genJetAK8Idx", &OBJ##_genJetAK8Idx); \
  tree_->Branch(#OBJ "_hadronFlavour", &OBJ##_hadronFlavour); \
  tree_->Branch(#OBJ "_nBHadrons", &OBJ##_nBHadrons); \
  tree_->Branch(#OBJ "_nCHadrons", &OBJ##_nCHadrons); \
  tree_->Branch(#OBJ "_nPFCand", &OBJ##_nPFCand);	\
  tree_->Branch(#OBJ "_PNetQCDb", &OBJ##_PNetQCDb);	\
  tree_->Branch(#OBJ "_PNetQCDbb", &OBJ##_PNetQCDbb);	\
  tree_->Branch(#OBJ "_PNetQCDc", &OBJ##_PNetQCDc);	\
  tree_->Branch(#OBJ "_PNetQCDcc", &OBJ##_PNetQCDcc);	\
  tree_->Branch(#OBJ "_PNetQCDothers", &OBJ##_PNetQCDothers);	\
  tree_->Branch(#OBJ "_PNetXbb", &OBJ##_PNetXbb);		\
  tree_->Branch(#OBJ "_PNetXcc", &OBJ##_PNetXcc);		\
  tree_->Branch(#OBJ "_PNetXqq", &OBJ##_PNetXqq);		\
  tree_->Branch(#OBJ "_deepTagMD_H4q", &OBJ##_deepTagMD_H4q);	\
  tree_->Branch(#OBJ "_deepTagMD_Hbb", &OBJ##_deepTagMD_Hbb);	\
  tree_->Branch(#OBJ "_deepTagMD_T", &OBJ##_deepTagMD_T);	\
  tree_->Branch(#OBJ "_deepTagMD_W", &OBJ##_deepTagMD_W);	\
  tree_->Branch(#OBJ "_deepTagMD_Z", &OBJ##_deepTagMD_Z);	\
  tree_->Branch(#OBJ "_deepTagMD_bbvsL", &OBJ##_deepTagMD_bbvsL);	\
  tree_->Branch(#OBJ "_deepTagMD_ccvsL", &OBJ##_deepTagMD_ccvsL);	\
  tree_->Branch(#OBJ "_deepTag_QCD", &OBJ##_deepTag_QCD);		\
  tree_->Branch(#OBJ "_deepTag_QCDothers", &OBJ##_deepTag_QCDothers);	\
  tree_->Branch(#OBJ "_deepTag_W", &OBJ##_deepTag_W);			\
  tree_->Branch(#OBJ "_deepTag_Z", &OBJ##_deepTag_Z);			\
  tree_->Branch(#OBJ "_nsubjets",  &OBJ##_nsubjets);			\
  tree_->Branch(#OBJ "_subjet1_pt",  &OBJ##_subjet1_pt);		\
  tree_->Branch(#OBJ "_subjet1_eta", &OBJ##_subjet1_eta);		\
  tree_->Branch(#OBJ "_subjet1_phi", &OBJ##_subjet1_phi);               \
  tree_->Branch(#OBJ "_subjet1_m",   &OBJ##_subjet1_m);			\
  tree_->Branch(#OBJ "_subjet1_btagDeepB", &OBJ##_subjet2_btagDeepB);   \
  tree_->Branch(#OBJ "_subjet2_pt",  &OBJ##_subjet2_pt);                \
  tree_->Branch(#OBJ "_subjet2_eta", &OBJ##_subjet2_eta);               \
  tree_->Branch(#OBJ "_subjet2_phi", &OBJ##_subjet2_phi);		\
  tree_->Branch(#OBJ "_subjet2_m",   &OBJ##_subjet2_m);			\
  tree_->Branch(#OBJ "_subjet2_btagDeepB", &OBJ##_subjet2_btagDeepB);
  

#define CLEAR_fatjet_list(OBJ) \
  OBJ##_pt.clear();            \
  OBJ##_eta.clear();           \
  OBJ##_phi.clear();	       \
  OBJ##_m.clear();	       \
  OBJ##_mSD_UnCorrected.clear();     \
  OBJ##_area.clear();	       \
  OBJ##_n2b1.clear();	       \
  OBJ##_n3b1.clear();	       \
  OBJ##_rawFactor.clear();     \
  OBJ##_tau1.clear();	       \
  OBJ##_tau2.clear();	       \
  OBJ##_tau3.clear();	       \
  OBJ##_tau4.clear();	       \
  OBJ##_jetId.clear();	       \
  OBJ##_genJetAK8Idx.clear();  \
  OBJ##_hadronFlavour.clear(); \
  OBJ##_nBHadrons.clear();     \
  OBJ##_nCHadrons.clear();     \
  OBJ##_nPFCand.clear();       \
  OBJ##_PNetQCDb.clear();      \
  OBJ##_PNetQCDbb.clear();     \
  OBJ##_PNetQCDc.clear();      \
  OBJ##_PNetQCDcc.clear();     \
  OBJ##_PNetQCDothers.clear(); \
  OBJ##_PNetXbb.clear();       \
  OBJ##_PNetXcc.clear();       \
  OBJ##_PNetXqq.clear();       \
  OBJ##_deepTagMD_H4q.clear(); \
  OBJ##_deepTagMD_Hbb.clear(); \
  OBJ##_deepTagMD_T.clear();   \
  OBJ##_deepTagMD_W.clear();   \
  OBJ##_deepTagMD_Z.clear();   \
  OBJ##_deepTagMD_bbvsL.clear();		\
  OBJ##_deepTagMD_ccvsL.clear();		\
  OBJ##_deepTag_QCD.clear();			\
  OBJ##_deepTag_QCDothers.clear();		\
  OBJ##_deepTag_W.clear();			\
  OBJ##_deepTag_Z.clear();			\
  OBJ##_nsubjets.clear();			\
  OBJ##_subjet1_pt.clear();			\
  OBJ##_subjet1_eta.clear();			\
  OBJ##_subjet1_phi.clear();			\
  OBJ##_subjet1_m.clear();			\
  OBJ##_subjet1_btagDeepB.clear();		\
  OBJ##_subjet2_pt.clear();			\
  OBJ##_subjet2_eta.clear();			\
  OBJ##_subjet2_phi.clear();			\
  OBJ##_subjet2_m.clear();			\
  OBJ##_subjet2_btagDeepB.clear();

#define BRANCH_jet_list(OBJ)                                  \
  tree_->Branch(#OBJ "_E", &OBJ##_E);                         \
  tree_->Branch(#OBJ "_m", &OBJ##_m);                         \
  tree_->Branch(#OBJ "_mRegressed", &OBJ##_mRegressed);       \
  tree_->Branch(#OBJ "_pt", &OBJ##_pt);                       \
  tree_->Branch(#OBJ "_ptRegressed", &OBJ##_ptRegressed);     \
  tree_->Branch(#OBJ "_eta", &OBJ##_eta);                     \
  tree_->Branch(#OBJ "_phi", &OBJ##_phi);                     \
  tree_->Branch(#OBJ "_signalId", &OBJ##_signalId);           \
  tree_->Branch(#OBJ "_higgsIdx", &OBJ##_higgsIdx);           \
  tree_->Branch(#OBJ "_genIdx", &OBJ##_genIdx);               \
  tree_->Branch(#OBJ "_btag", &OBJ##_btag);                   \
  tree_->Branch(#OBJ "_qgl", &OBJ##_qgl);                     \
  tree_->Branch(#OBJ "_chEmEF", &OBJ##_chEmEF);               \
  tree_->Branch(#OBJ "_chHEF", &OBJ##_chHEF);                 \
  tree_->Branch(#OBJ "_neEmEF", &OBJ##_neEmEF);               \
  tree_->Branch(#OBJ "_neHEF", &OBJ##_neHEF);                 \
  tree_->Branch(#OBJ "_nConstituents", &OBJ##_nConstituents); \
  tree_->Branch(#OBJ "_id", &OBJ##_id);                       \
  tree_->Branch(#OBJ "_puid", &OBJ##_puid);

#define CLEAR_jet_list(OBJ)    \
  OBJ##_E.clear();             \
  OBJ##_m.clear();             \
  OBJ##_mRegressed.clear();    \
  OBJ##_pt.clear();            \
  OBJ##_ptRegressed.clear();   \
  OBJ##_eta.clear();           \
  OBJ##_phi.clear();           \
  OBJ##_partonFlav.clear();    \
  OBJ##_hadronFlav.clear();    \
  OBJ##_signalId.clear();      \
  OBJ##_higgsIdx.clear();      \
  OBJ##_genIdx.clear();        \
  OBJ##_btag.clear();          \
  OBJ##_qgl.clear();           \
  OBJ##_chEmEF.clear();        \
  OBJ##_chHEF.clear();         \
  OBJ##_neEmEF.clear();        \
  OBJ##_neHEF.clear();         \
  OBJ##_nConstituents.clear(); \
  OBJ##_id.clear();            \
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
	  BRANCH_m_pt_eta_phi_p4(gen_H1_fc);
	  BRANCH_m_pt_eta_phi_p4(gen_H2_fc);
	  BRANCH_m_pt_eta_phi_p4(gen_H1);
	  BRANCH_m_pt_eta_phi_p4(gen_H2);
	  BRANCH_m_pt_eta_phi_p4(gen_H1_b1);
	  BRANCH_m_pt_eta_phi_p4(gen_H1_b2);
	  BRANCH_m_pt_eta_phi_p4(gen_H2_b1);
	  BRANCH_m_pt_eta_phi_p4(gen_H2_b2);
	  
	  BRANCH_m_pt_eta_phi_p4(gen_H1_b1_genjet);
	  BRANCH_m_pt_eta_phi_p4(gen_H1_b2_genjet);
	  BRANCH_m_pt_eta_phi_p4(gen_H2_b1_genjet);
	  BRANCH_m_pt_eta_phi_p4(gen_H2_b2_genjet);

	  BRANCH_m_pt_eta_phi_p4(gen_H1_b1_genfatjet);
	  BRANCH_m_pt_eta_phi_p4(gen_H1_b2_genfatjet);
	  BRANCH_m_pt_eta_phi_p4(gen_H2_b1_genfatjet);
	  BRANCH_m_pt_eta_phi_p4(gen_H2_b2_genfatjet);
	  
	  BRANCH_m_pt_ptRegressed_eta_phi_p4(gen_H1_b1_recojet);
	  BRANCH_m_pt_ptRegressed_eta_phi_p4(gen_H1_b2_recojet);
	  BRANCH_m_pt_ptRegressed_eta_phi_p4(gen_H2_b1_recojet);
	  BRANCH_m_pt_ptRegressed_eta_phi_p4(gen_H2_b2_recojet);
	  
	  BRANCH_m_pt_eta_phi_p4(gen_H1_b1_recofatjet);
	  BRANCH_m_pt_eta_phi_p4(gen_H1_b2_recofatjet);
	  BRANCH_m_pt_eta_phi_p4(gen_H2_b1_recofatjet);
	  BRANCH_m_pt_eta_phi_p4(gen_H2_b2_recofatjet);
	}
    } // 4b final state


  if (is_enabled("sixb_brs"))
  {
    if (is_enabled("sig_gen_brs"))
    {
      BRANCH_m_pt_eta_phi_p4(gen_X_fc);
      BRANCH_m_pt_eta_phi_p4(gen_X);
      BRANCH_m_pt_eta_phi_p4(gen_Y);
      BRANCH_m_pt_eta_phi_p4(gen_HX);
      BRANCH_m_pt_eta_phi_p4(gen_H1);
      BRANCH_m_pt_eta_phi_p4(gen_H2);

      BRANCH_m_pt_eta_phi_p4(gen_HX_b1);
      BRANCH_m_pt_eta_phi_p4(gen_HX_b2);
      BRANCH_m_pt_eta_phi_p4(gen_H1_b1);
      BRANCH_m_pt_eta_phi_p4(gen_H1_b2);
      BRANCH_m_pt_eta_phi_p4(gen_H2_b1);
      BRANCH_m_pt_eta_phi_p4(gen_H2_b2);

      BRANCH_m_pt_eta_phi_p4(gen_HX_b1_genjet);
      BRANCH_m_pt_eta_phi_p4(gen_HX_b2_genjet);
      BRANCH_m_pt_eta_phi_p4(gen_H1_b1_genjet);
      BRANCH_m_pt_eta_phi_p4(gen_H1_b2_genjet);
      BRANCH_m_pt_eta_phi_p4(gen_H2_b1_genjet);
      BRANCH_m_pt_eta_phi_p4(gen_H2_b2_genjet);

      BRANCH_m_pt_ptRegressed_eta_phi_p4(gen_HX_b1_recojet);
      BRANCH_m_pt_ptRegressed_eta_phi_p4(gen_HX_b2_recojet);
      BRANCH_m_pt_ptRegressed_eta_phi_p4(gen_H1_b1_recojet);
      BRANCH_m_pt_ptRegressed_eta_phi_p4(gen_H1_b2_recojet);
      BRANCH_m_pt_ptRegressed_eta_phi_p4(gen_H2_b1_recojet);
      BRANCH_m_pt_ptRegressed_eta_phi_p4(gen_H2_b2_recojet);

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

    BRANCH_m_pt_eta_phi_p4(X);
    BRANCH_m_pt_eta_phi_p4(Y);
    BRANCH_m_pt_eta_phi_p4(HX);
    BRANCH_m_pt_eta_phi_p4(H1);
    BRANCH_m_pt_eta_phi_p4(H2);

    BRANCH_m_pt_ptRegressed_eta_phi_DeepJet_p4(HX_b1);
    BRANCH_m_pt_ptRegressed_eta_phi_DeepJet_p4(HX_b2);
    BRANCH_m_pt_ptRegressed_eta_phi_DeepJet_p4(H1_b1);
    BRANCH_m_pt_ptRegressed_eta_phi_DeepJet_p4(H1_b2);
    BRANCH_m_pt_ptRegressed_eta_phi_DeepJet_p4(H2_b1);
    BRANCH_m_pt_ptRegressed_eta_phi_DeepJet_p4(H2_b2);
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
      tree_->Branch("nfound_select_y", &nfound_select_y);
      tree_->Branch("nfound_paired_y", &nfound_paired_y);
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

    tree_->Branch("n_loose_btag", &n_loose_btag);
    tree_->Branch("n_medium_btag", &n_medium_btag);
    tree_->Branch("n_tight_btag", &n_tight_btag);
    tree_->Branch("btagavg", &btagavg);

    tree_->Branch("quadh_score", &quadh_score);
  }
  
  tree_->Branch("n_muon", &n_muon);
  if (is_enabled("muon_coll"))
    {
      std::cout << "[INFO] OutputTree : enabling muon collection branches" << std::endl;
      BRANCH_muon_list(muon);
    }
  
  tree_->Branch("n_ele", &n_ele);
  if (is_enabled("ele_coll"))
    {
      std::cout << "[INFO] OutputTree : enabling electron collection branches" << std::endl;
      BRANCH_ele_list(ele);
    }
  
  /*
  if (is_enabled("ttbar_brs"))
    {
      std::cout << "[INFO] OutputTree : enabling ttbar branches" << std::endl;
      BRANCH_m_pt_ptRegressed_eta_phi_DeepJet_p4(bjet1);
      if (is_enabled("gen_brs")) tree_->Branch("bjet1_hadflav", &bjet1_hadflav);

      BRANCH_m_pt_ptRegressed_eta_phi_DeepJet_p4(bjet2);
      if (is_enabled("gen_brs")) tree_->Branch("bjet2_hadflav", &bjet2_hadflav);
    }
  */
  
  tree_->Branch("n_total_jet",&n_total_jet);
  tree_->Branch("n_jet", &n_jet);
  if (is_enabled("jet_coll"))
    {
      std::cout << "[INFO] OutputTree : enabling jet collection branches" << std::endl;

      BRANCH_jet_list(jet);
      tree_->Branch("b_6j_score",    &b_6j_score);
    }

  if (is_enabled("fatjet_coll"))
    {
      std::cout << "[INFO] OutputTree : enabling fatjet collection branches" << std::endl;
      tree_->Branch("n_fatjet", &n_fatjet);
      BRANCH_fatjet_list(fatjet);
    }
  
  if (is_enabled("dijets_coll"))
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
      
      if (is_enabled("fatjet_coll"))
	{
	  tree_->Branch("n_genfatjet", &n_genfatjet);
	  tree_->Branch("genfatjet_E", &genfatjet_E);
	  tree_->Branch("genfatjet_m", &genfatjet_m);
	  tree_->Branch("genfatjet_pt", &genfatjet_pt);
	  tree_->Branch("genfatjet_eta", &genfatjet_eta);
	  tree_->Branch("genfatjet_phi", &genfatjet_phi);
	  tree_->Branch("genfatjet_signalId", &genfatjet_signalId);
	  tree_->Branch("genfatjet_recoIdx", &genfatjet_recoIdx);
	  tree_->Branch("genfatjet_hadronFlav", &genfatjet_hadronFlav);
	  tree_->Branch("genfatjet_partonFlav", &genfatjet_partonFlav);
	  tree_->Branch("genfatjet_nsubjets", &genfatjet_nsubjets);
	  tree_->Branch("genfatjet_subjet1_pt", &genfatjet_subjet1_pt);
	  tree_->Branch("genfatjet_subjet1_m", &genfatjet_subjet1_m);
	  tree_->Branch("genfatjet_subjet1_eta", &genfatjet_subjet1_eta);
	  tree_->Branch("genfatjet_subjet1_phi", &genfatjet_subjet1_phi);
	  tree_->Branch("genfatjet_subjet2_pt", &genfatjet_subjet2_pt);
	  tree_->Branch("genfatjet_subjet2_m", &genfatjet_subjet2_m);
	  tree_->Branch("genfatjet_subjet2_eta", &genfatjet_subjet2_eta);
	  tree_->Branch("genfatjet_subjet2_phi", &genfatjet_subjet2_phi);
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
  quadh_score = 0;

  genjet_E.clear();	    
  genjet_m.clear();		
  genjet_pt.clear();		
  genjet_eta.clear();		
  genjet_phi.clear();		
  genjet_partonFlav.clear();
  genjet_hadronFlav.clear();
  genjet_signalId.clear();
  genjet_recoIdx.clear();

  genfatjet_E.clear();
  genfatjet_m.clear();
  genfatjet_pt.clear();
  genfatjet_eta.clear();
  genfatjet_phi.clear();
  genfatjet_signalId.clear();
  genfatjet_recoIdx.clear();
  genfatjet_partonFlav.clear();
  genfatjet_hadronFlav.clear();
  genfatjet_nsubjets.clear();
  genfatjet_subjet1_pt.clear();
  genfatjet_subjet1_m.clear();
  genfatjet_subjet1_eta.clear();
  genfatjet_subjet1_phi.clear();
  genfatjet_subjet2_pt.clear();
  genfatjet_subjet2_m.clear();
  genfatjet_subjet2_eta.clear();
  genfatjet_subjet2_phi.clear();
  
  CLEAR_ele_list(ele);
  CLEAR_muon_list(muon);
  CLEAR_jet_list(jet);
  CLEAR_fatjet_list(fatjet);
  
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

  // Start Gen 4b Objects
  CLEAR_m_pt_eta_phi_p4(gen_H1_fc);
  CLEAR_m_pt_eta_phi_p4(gen_H2_fc);
  CLEAR_m_pt_eta_phi_p4(gen_H1_b1_genfatjet);
  CLEAR_m_pt_eta_phi_p4(gen_H1_b2_genfatjet);
  CLEAR_m_pt_eta_phi_p4(gen_H2_b1_genfatjet);
  CLEAR_m_pt_eta_phi_p4(gen_H2_b2_genfatjet);
  CLEAR_m_pt_eta_phi_p4(gen_H1_b1_recofatjet);
  CLEAR_m_pt_eta_phi_p4(gen_H1_b2_recofatjet);
  CLEAR_m_pt_eta_phi_p4(gen_H2_b1_recofatjet);
  CLEAR_m_pt_eta_phi_p4(gen_H2_b2_recofatjet);

  CLEAR_m_pt_eta_phi_p4(gen_X_fc);
  CLEAR_m_pt_eta_phi_p4(gen_X);

  // Start Gen 6B Objects
  CLEAR_m_pt_eta_phi_p4(gen_Y);
  CLEAR_m_pt_eta_phi_p4(gen_HX);
  CLEAR_m_pt_eta_phi_p4(gen_H1);
  CLEAR_m_pt_eta_phi_p4(gen_H2);

  CLEAR_m_pt_eta_phi_p4(gen_HX_b1);
  CLEAR_m_pt_eta_phi_p4(gen_HX_b2);
  CLEAR_m_pt_eta_phi_p4(gen_H1_b1);
  CLEAR_m_pt_eta_phi_p4(gen_H1_b2);
  CLEAR_m_pt_eta_phi_p4(gen_H2_b1);
  CLEAR_m_pt_eta_phi_p4(gen_H2_b2);

  CLEAR_m_pt_eta_phi_p4(gen_HX_b1_genjet);
  CLEAR_m_pt_eta_phi_p4(gen_HX_b2_genjet);
  CLEAR_m_pt_eta_phi_p4(gen_H1_b1_genjet);
  CLEAR_m_pt_eta_phi_p4(gen_H1_b2_genjet);
  CLEAR_m_pt_eta_phi_p4(gen_H2_b1_genjet);
  CLEAR_m_pt_eta_phi_p4(gen_H2_b2_genjet);

  CLEAR_m_pt_ptRegressed_eta_phi_p4(gen_HX_b1_recojet);
  CLEAR_m_pt_ptRegressed_eta_phi_p4(gen_HX_b2_recojet);
  CLEAR_m_pt_ptRegressed_eta_phi_p4(gen_H1_b1_recojet);
  CLEAR_m_pt_ptRegressed_eta_phi_p4(gen_H1_b2_recojet);
  CLEAR_m_pt_ptRegressed_eta_phi_p4(gen_H2_b1_recojet);
  CLEAR_m_pt_ptRegressed_eta_phi_p4(gen_H2_b2_recojet);
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
  CLEAR_m_pt_eta_phi_p4(H1);
  CLEAR_m_pt_eta_phi_p4(H2);

  CLEAR_m_pt_ptRegressed_eta_phi_DeepJet_p4(HX_b1);
  CLEAR_m_pt_ptRegressed_eta_phi_DeepJet_p4(HX_b2);
  CLEAR_m_pt_ptRegressed_eta_phi_DeepJet_p4(H1_b1);
  CLEAR_m_pt_ptRegressed_eta_phi_DeepJet_p4(H1_b2);
  CLEAR_m_pt_ptRegressed_eta_phi_DeepJet_p4(H2_b1);
  CLEAR_m_pt_ptRegressed_eta_phi_DeepJet_p4(H2_b2);

  HX_b1_genHflag  = -999;
  HX_b2_genHflag  = -999;
  H1_b1_genHflag = -999;
  H1_b2_genHflag = -999;
  H2_b1_genHflag = -999;
  H2_b2_genHflag = -999;
  // End Reco 6B Objects

  // Start Reco 8B Objects
  CLEAR_m_pt_eta_phi_p4(Y);
  CLEAR_m_pt_eta_phi_p4(HX);
  CLEAR_m_pt_eta_phi_p4(H1);
  CLEAR_m_pt_eta_phi_p4(H2);

  CLEAR_m_pt_ptRegressed_eta_phi_DeepJet_p4(HX_b1);
  CLEAR_m_pt_ptRegressed_eta_phi_DeepJet_p4(HX_b2);
  CLEAR_m_pt_ptRegressed_eta_phi_DeepJet_p4(H1_b1);
  CLEAR_m_pt_ptRegressed_eta_phi_DeepJet_p4(H1_b2);
  CLEAR_m_pt_ptRegressed_eta_phi_DeepJet_p4(H2_b1);
  CLEAR_m_pt_ptRegressed_eta_phi_DeepJet_p4(H2_b2);

  HX_b1_genHflag = -999;
  HX_b2_genHflag = -999;
  H1_b1_genHflag = -999;
  H1_b2_genHflag = -999;
  H2_b1_genHflag = -999;
  H2_b2_genHflag = -999;

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

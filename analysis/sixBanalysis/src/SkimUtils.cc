#include "SkimUtils.h"

#include "Math/Vector4D.h"
typedef ROOT::Math::PtEtaPhiMVector p4_t;

#include <iostream>
#include <fstream>
#include <string>

using namespace std;

// helper: copies the pt/eta/phi/p4 branches from a candidate OBJ to the output tree
// NOTE: requires the matching of the names (and enforces it)
#define COPY_m_pt_eta_phi_p4(OBJ) \
    ot.OBJ ## _m   = ei. OBJ -> P4().M(); \
    ot.OBJ ## _pt  = ei. OBJ -> P4().Pt(); \
    ot.OBJ ## _eta = ei. OBJ -> P4().Eta(); \
    ot.OBJ ## _phi = ei. OBJ -> P4().Phi(); \
    ot.OBJ ## _p4  = ei. OBJ -> P4();

#define COPY_m_pt_ptRegressed_eta_phi_p4(OBJ) \
    ot.OBJ ## _m            = ei. OBJ -> P4().M(); \
    ot.OBJ ## _pt           = ei. OBJ -> P4().Pt(); \
    ot.OBJ ## _ptRegressed  = ei. OBJ -> P4Regressed().Pt(); \
    ot.OBJ ## _deepJet      = get_property(ei.OBJ.get(),Jet_btagDeepFlavB); \
    ot.OBJ ## _eta          = ei. OBJ -> P4().Eta(); \
    ot.OBJ ## _phi          = ei. OBJ -> P4().Phi(); \
    ot.OBJ ## _p4           = ei. OBJ -> P4();

//helperM same as above, but encloses the obj (a boost::optional is expected) in a if clause to check whether it is initialized
#define COPY_OPTIONAL_m_pt_eta_phi_p4(OBJ)	\
  if (ei.OBJ) {					\
    ot.OBJ ## _m   = ei. OBJ -> P4().M();	\
    ot.OBJ ## _pt  = ei. OBJ -> P4().Pt();	\
    ot.OBJ ## _eta = ei. OBJ -> P4().Eta();	\
    ot.OBJ ## _phi = ei. OBJ -> P4().Phi();	\
    ot.OBJ ## _p4  = ei. OBJ -> P4();		\
  }

#define COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_p4(OBJ)		\
  if (ei.OBJ) {							\
    ot.OBJ ## _m            = ei. OBJ -> P4().M();		\
    ot.OBJ ## _pt           = ei. OBJ -> P4().Pt();		\
    ot.OBJ ## _ptRegressed  = ei. OBJ -> P4Regressed().Pt();	\
    ot.OBJ ## _eta          = ei. OBJ -> P4().Eta();		\
    ot.OBJ ## _phi          = ei. OBJ -> P4().Phi();		\
    ot.OBJ ## _p4           = ei. OBJ -> P4();			\
  }

#define COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_DeepJet_p4(OBJ)		\
  if (ei.OBJ) {								\
    ot.OBJ ## _m            = ei. OBJ -> P4().M();			\
    ot.OBJ ## _pt           = ei. OBJ -> P4().Pt();			\
    ot.OBJ ## _ptRegressed  = ei. OBJ -> P4Regressed().Pt();		\
    ot.OBJ ## _eta          = ei. OBJ -> P4().Eta();			\
    ot.OBJ ## _phi          = ei. OBJ -> P4().Phi();			\
    ot.OBJ ## _DeepJet      = get_property( ei. OBJ .get(), Jet_btagDeepFlavB); \
    ot.OBJ ## _p4           = ei. OBJ -> P4();				\
  }

#define COPY_OPTIONAL_jet_list(OBJ)				\
  if (ei.OBJ ## _list) {					\
  for (Jet& jet : ei.OBJ ## _list.get()) {			\
    ot.OBJ ## _E.push_back( jet.get_E() );			\
    ot.OBJ ## _m.push_back( jet.get_m() );			\
    ot.OBJ ## _pt.push_back( jet.get_pt() );			\
    ot.OBJ ## _eta.push_back( jet.get_eta() );			\
    ot.OBJ ## _phi.push_back( jet.get_phi() );			\
    ot.OBJ ## _signalId.push_back( jet.get_signalId() );	\
    ot.OBJ ## _higgsIdx.push_back( jet.get_higgsIdx() );	\
    ot.OBJ ## _genIdx.push_back( jet.get_genIdx() );		\
    ot.OBJ ## _btag.push_back( jet.get_btag() );		\
    ot.OBJ ## _qgl.push_back( jet.get_qgl() );			\
    ot.OBJ ## _id.push_back( jet.get_id() );			\
    ot.OBJ ## _puid.push_back( jet.get_puid() );		\
    ot.OBJ ## _preselIdx.push_back( jet.get_preselIdx() );	\
  }								\
}

#define COPY_OPTIONAL_dijet_list(OBJ)				\
  if (ei.OBJ ## _list) {					\
  for (DiJet& dijet : ei.OBJ ## _list.get()) {			\
    ot.OBJ ## _E.push_back( dijet.E() );			\
    ot.OBJ ## _m.push_back( dijet.M() );			\
    ot.OBJ ## _pt.push_back( dijet.Pt() );			\
    ot.OBJ ## _eta.push_back( dijet.Eta() );			\
    ot.OBJ ## _phi.push_back( dijet.Phi() );			\
    ot.OBJ ## _dr.push_back( dijet.dR() );			\
    ot.OBJ ## _signalId.push_back( dijet.get_signalId() );	\
    ot.OBJ ## _2j_score.push_back( dijet.get_2j_score() );	\
  }								\
}

#define COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_p4(OBJ) \
    if (ei.OBJ) { \
    ot.OBJ ## _m            = ei. OBJ -> P4().M(); \
    ot.OBJ ## _pt           = ei. OBJ -> P4().Pt(); \
    ot.OBJ ## _ptRegressed  = ei. OBJ -> P4Regressed().Pt(); \
    ot.OBJ ## _deepJet      = get_property(ei.OBJ.get(),Jet_btagDeepFlavB); \
    ot.OBJ ## _eta          = ei. OBJ -> P4().Eta(); \
    ot.OBJ ## _phi          = ei. OBJ -> P4().Phi(); \
    ot.OBJ ## _p4           = ei. OBJ -> P4();\
    }
// --- - --- - --- - --- - --- - --- - --- - --- - --- - --- - --- - --- - 

int SkimUtils::appendFromFileList (TChain* chain, string filename)
{
  //cout << "=== inizio parser ===" << endl;
  std::ifstream infile(filename.c_str());
  std::string line;
  int nfiles = 0;
  while (std::getline(infile, line))
    {
      line = line.substr(0, line.find("#", 0)); // remove comments introduced by #
      while (line.find(" ") != std::string::npos) line = line.erase(line.find(" "), 1); // remove white spaces
      while (line.find("\n") != std::string::npos) line = line.erase(line.find("\n"), 1); // remove new line characters
      while (line.find("\r") != std::string::npos) line = line.erase(line.find("\r"), 1); // remove carriage return characters
      if (!line.empty()) // skip empty lines
        {
	  chain->Add(line.c_str());
	  ++nfiles;
        }
    }
  return nfiles;
}


void SkimUtils::fill_output_tree(OutputTree& ot, NanoAODTree& nat, EventInfo& ei)
{

  // set the variables for resonant analysis
  ot.Run      = *ei.Run;
  ot.LumiSec  = *ei.LumiSec;
  ot.Event    = *ei.Event;

  if(ei.n_other_pv)     ot.n_other_pv      = *ei.n_other_pv;
  if(ei.n_pu)           ot.n_pu            = *ei.n_pu;
  if(ei.n_true_int)     ot.n_true_int      = *ei.n_true_int;
  if(ei.rhofastjet_all) ot.rhofastjet_all  = *ei.rhofastjet_all;
  if(ei.lhe_ht)         ot.lhe_ht          = *ei.lhe_ht;
  if(ei.n_jet)          ot.n_jet           = *ei.n_jet;
  if(ei.n_total_jet)    ot.n_total_jet     = *ei.n_total_jet;
  if(ei.n_genjet)       ot.n_genjet        = *ei.n_genjet;
  if(ei.n_higgs)        ot.n_higgs         = *ei.n_higgs;

  if(ei.b_6j_score)     ot.b_6j_score      = *ei.b_6j_score;
  if(ei.b_3d_score)     ot.b_3d_score      = *ei.b_3d_score;

  COPY_OPTIONAL_jet_list(jet);
  COPY_OPTIONAL_jet_list(t6_jet);
  COPY_OPTIONAL_jet_list(nn_jet);

  COPY_OPTIONAL_dijet_list(t6_higgs);
  COPY_OPTIONAL_dijet_list(nn_higgs);

  if (ei.genjet_list) {
    for (GenJet& jet : ei.genjet_list.get()) {
      ot.genjet_E.push_back( jet.get_E() );	    
      ot.genjet_m.push_back( jet.get_m() );		
      ot.genjet_pt.push_back( jet.get_pt() );		
      ot.genjet_eta.push_back( jet.get_eta() );		
      ot.genjet_phi.push_back( jet.get_phi() );		
      ot.genjet_partonFlav.push_back( jet.get_partonFlav() );
      ot.genjet_hadronFlav.push_back( jet.get_hadronFlav() );
      ot.genjet_signalId.push_back( jet.get_signalId() );
      ot.genjet_recoIdx.push_back( jet.get_recoIdx() );
    }
  }

  // if (ei.t6_event_shapes) {
  //   ot.t6_sphericity = ei.t6_event_shapes.get().sphericity;
  //   ot.t6_sphericity_t = ei.t6_event_shapes.get().transverse_sphericity;
  //   ot.t6_aplanarity = ei.t6_event_shapes.get().aplanarity;
  // }
  
  // if (ei.nn_event_shapes) {
  //   ot.nn_sphericity = ei.nn_event_shapes.get().sphericity;
  //   ot.nn_sphericity_t = ei.nn_event_shapes.get().transverse_sphericity;
  //   ot.nn_aplanarity = ei.nn_event_shapes.get().aplanarity;
  // }

  if (ei.event_shapes) {
    ot.sphericity   = ei.event_shapes.get().sphericity;
    ot.sphericity_t = ei.event_shapes.get().transverse_sphericity;
    ot.aplanarity   = ei.event_shapes.get().aplanarity;
  }


  COPY_OPTIONAL_m_pt_eta_phi_p4(gen_X_fc);
  COPY_OPTIONAL_m_pt_eta_phi_p4(gen_X);
  COPY_OPTIONAL_m_pt_eta_phi_p4(gen_Y);
  COPY_OPTIONAL_m_pt_eta_phi_p4(gen_HX);
  COPY_OPTIONAL_m_pt_eta_phi_p4(gen_HY1);
  COPY_OPTIONAL_m_pt_eta_phi_p4(gen_HY2);

  COPY_OPTIONAL_m_pt_eta_phi_p4(gen_HX_b1);
  COPY_OPTIONAL_m_pt_eta_phi_p4(gen_HX_b2);
  COPY_OPTIONAL_m_pt_eta_phi_p4(gen_HY1_b1);
  COPY_OPTIONAL_m_pt_eta_phi_p4(gen_HY1_b2);
  COPY_OPTIONAL_m_pt_eta_phi_p4(gen_HY2_b1);
  COPY_OPTIONAL_m_pt_eta_phi_p4(gen_HY2_b2);

  COPY_OPTIONAL_m_pt_eta_phi_p4(gen_HX_b1_genjet);
  COPY_OPTIONAL_m_pt_eta_phi_p4(gen_HX_b2_genjet);
  COPY_OPTIONAL_m_pt_eta_phi_p4(gen_HY1_b1_genjet);
  COPY_OPTIONAL_m_pt_eta_phi_p4(gen_HY1_b2_genjet);
  COPY_OPTIONAL_m_pt_eta_phi_p4(gen_HY2_b1_genjet);
  COPY_OPTIONAL_m_pt_eta_phi_p4(gen_HY2_b2_genjet);

  COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_p4(gen_HX_b1_recojet);
  COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_p4(gen_HX_b2_recojet);
  COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_p4(gen_HY1_b1_recojet);
  COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_p4(gen_HY1_b2_recojet);
  COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_p4(gen_HY2_b1_recojet);
  COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_p4(gen_HY2_b2_recojet);
  if (ei.gen_bs_N_reco_match)        ot.gen_bs_N_reco_match        = *ei.gen_bs_N_reco_match;
  if (ei.gen_bs_N_reco_match_in_acc) ot.gen_bs_N_reco_match_in_acc = *ei.gen_bs_N_reco_match_in_acc;
  if (ei.gen_bs_match_recojet_minv)        ot.gen_bs_match_recojet_minv        = *ei.gen_bs_match_recojet_minv;
  if (ei.gen_bs_match_in_acc_recojet_minv) ot.gen_bs_match_in_acc_recojet_minv = *ei.gen_bs_match_in_acc_recojet_minv;

  COPY_OPTIONAL_m_pt_eta_phi_p4(X);
  COPY_OPTIONAL_m_pt_eta_phi_p4(Y);
  COPY_OPTIONAL_m_pt_eta_phi_p4(HX);
  COPY_OPTIONAL_m_pt_eta_phi_p4(HY1);
  COPY_OPTIONAL_m_pt_eta_phi_p4(HY2);

  COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_p4(HX_b1);
  COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_p4(HX_b2);
  COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_p4(HY1_b1);
  COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_p4(HY1_b2);
  COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_p4(HY2_b1);
  COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_p4(HY2_b2);

  if (ei.HX_b1_genHflag)  ot.HX_b1_genHflag  = *ei.HX_b1_genHflag;
  if (ei.HX_b2_genHflag)  ot.HX_b2_genHflag  = *ei.HX_b2_genHflag;
  if (ei.HY1_b1_genHflag) ot.HY1_b1_genHflag = *ei.HY1_b1_genHflag;
  if (ei.HY1_b2_genHflag) ot.HY1_b2_genHflag = *ei.HY1_b2_genHflag;
  if (ei.HY2_b1_genHflag) ot.HY2_b1_genHflag = *ei.HY2_b1_genHflag;
  if (ei.HY2_b2_genHflag) ot.HY2_b2_genHflag = *ei.HY2_b2_genHflag;

  if (ei.nsel_from_H) ot.nsel_from_H = *ei.nsel_from_H;

  COPY_OPTIONAL_m_pt_eta_phi_p4(mu_1);
  COPY_OPTIONAL_m_pt_eta_phi_p4(mu_2);
  COPY_OPTIONAL_m_pt_eta_phi_p4(ele_1);
  COPY_OPTIONAL_m_pt_eta_phi_p4(ele_2);

  ot.n_mu_loose  = *ei.n_mu_loose;
  ot.n_ele_loose = *ei.n_ele_loose;

  COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_DeepJet_p4(bjet1);
  COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_DeepJet_p4(bjet2);

  // must check validity of reader because this is not defined in data
  if (ei.bjet1 && nat.Jet_hadronFlavour.IsValid())
    ot.bjet1_hadflav = get_property(ei.bjet1.get(), Jet_hadronFlavour);

  if (ei.bjet2 && nat.Jet_hadronFlavour.IsValid())
    ot.bjet2_hadflav = get_property(ei.bjet2.get(), Jet_hadronFlavour);

  if (ei.btagSF_WP_M) ot.btagSF_WP_M = *ei.btagSF_WP_M;

  // fill the tree
  ot.fill();

}

void SkimUtils::init_gen_weights(OutputTree &ot, NormWeightTree &nwt)
{
  // create userfloats for systematics read from file directly
  auto& gen_weight   = nwt.get_gen_weight();
  auto& pu_weight    = nwt.get_pu_weight();
  auto& pdf_weight   = nwt.get_pdf_weight();
  auto& scale_weight = nwt.get_scale_weight();
  auto& ps_weight    = nwt.get_ps_weight();

  ot.declareUserFloatBranch(gen_weight.name, 1.0);
  for (auto n : gen_weight.syst_name)
    ot.declareUserFloatBranch(n, 1.0);

  ot.declareUserFloatBranch(pu_weight.name, 1.0);
  for (auto n : pu_weight.syst_name)
    ot.declareUserFloatBranch(n, 1.0);

  ot.declareUserFloatBranch(pdf_weight.name, 1.0);
  for (auto n : pdf_weight.syst_name)
    ot.declareUserFloatBranch(n, 1.0);

  ot.declareUserFloatBranch(scale_weight.name, 1.0);
  for (auto n : scale_weight.syst_name)
    ot.declareUserFloatBranch(n, 1.0);

  ot.declareUserFloatBranch(ps_weight.name, 1.0);
  for (auto n : ps_weight.syst_name)
    ot.declareUserFloatBranch(n, 1.0);
}

<<<<<<< HEAD
void SkimUtils::copy_gen_weights(OutputTree &ot, NormWeightTree &nwt)
{
  // copy the values and the structures for systematics
  auto& gen_weight   = nwt.get_gen_weight();
  auto& pu_weight    = nwt.get_pu_weight();
  auto& pdf_weight   = nwt.get_pdf_weight();
  auto& scale_weight = nwt.get_scale_weight();
  auto& ps_weight    = nwt.get_ps_weight();

  ot.userFloat(gen_weight.name) = gen_weight.w;
  for (uint iw = 0; iw < gen_weight.syst_name.size(); ++iw){
    auto n = gen_weight.syst_name.at(iw);
    ot.userFloat(n) = gen_weight.syst_val.at(iw);
  }

  ot.userFloat(pu_weight.name) = pu_weight.w;
  for (uint iw = 0; iw < pu_weight.syst_name.size(); ++iw){
    auto n = pu_weight.syst_name.at(iw);
    ot.userFloat(n) = pu_weight.syst_val.at(iw);
  }   

  ot.userFloat(pdf_weight.name) = pdf_weight.w;
  for (uint iw = 0; iw < pdf_weight.syst_name.size(); ++iw){
    auto n = pdf_weight.syst_name.at(iw);
    ot.userFloat(n) = pdf_weight.syst_val.at(iw);
  }

  ot.userFloat(scale_weight.name) = scale_weight.w;
  for (uint iw = 0; iw < scale_weight.syst_name.size(); ++iw){
    auto n = scale_weight.syst_name.at(iw);
    ot.userFloat(n) = scale_weight.syst_val.at(iw);
  }

  ot.userFloat(ps_weight.name) = ps_weight.w;
  for (uint iw = 0; iw < ps_weight.syst_name.size(); ++iw){
    auto n = ps_weight.syst_name.at(iw);
    ot.userFloat(n) = ps_weight.syst_val.at(iw);
  }
}
=======
    // COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_p4(H1_b1)
//     if (ei.H1_b1) ot.H1_b1_deepCSV = get_property(ei.H1_b1.get(),Jet_btagDeepB); 
//     if (ei.H1_b1) ot.H1_b1_bRegRes = get_property(ei.H1_b1.get(),Jet_bRegRes);
//     if (ei.H1_b1) ot.H1_b1_jetId   = get_property(ei.H1_b1.get(),Jet_jetId); 
//     if (ei.H1_b1) ot.H1_b1_puId    = get_property(ei.H1_b1.get(),Jet_puId);
//     if (ei.H1_b1) ot.H1_b1_qgl     = get_property(ei.H1_b1.get(),Jet_qgl);
//     COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_p4(H1_b2)
//     if (ei.H1_b2) ot.H1_b2_deepCSV = get_property(ei.H1_b2.get(),Jet_btagDeepB);
//     if (ei.H1_b2) ot.H1_b2_bRegRes = get_property(ei.H1_b2.get(),Jet_bRegRes);
//     if (ei.H1_b2) ot.H1_b2_jetId   = get_property(ei.H1_b2.get(),Jet_jetId); 
//     if (ei.H1_b2) ot.H1_b2_puId    = get_property(ei.H1_b2.get(),Jet_puId);
//     if (ei.H1_b2) ot.H1_b2_qgl     = get_property(ei.H1_b2.get(),Jet_qgl);
//     COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_p4(H2_b1)
//     if (ei.H2_b1) ot.H2_b1_deepCSV = get_property(ei.H2_b1.get(),Jet_btagDeepB);
//     if (ei.H2_b1) ot.H2_b1_bRegRes = get_property(ei.H2_b1.get(),Jet_bRegRes);
//     if (ei.H2_b1) ot.H2_b1_jetId   = get_property(ei.H2_b1.get(),Jet_jetId); 
//     if (ei.H2_b1) ot.H2_b1_puId    = get_property(ei.H2_b1.get(),Jet_puId);
//     if (ei.H2_b1) ot.H2_b1_qgl     = get_property(ei.H2_b1.get(),Jet_qgl);
//     COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_p4(H2_b2)
//     if (ei.H2_b2) ot.H2_b2_deepCSV = get_property(ei.H2_b2.get(),Jet_btagDeepB);
//     if (ei.H2_b2) ot.H2_b2_bRegRes = get_property(ei.H2_b2.get(),Jet_bRegRes);
//     if (ei.H2_b2) ot.H2_b2_jetId   = get_property(ei.H2_b2.get(),Jet_jetId); 
//     if (ei.H2_b2) ot.H2_b2_puId    = get_property(ei.H2_b2.get(),Jet_puId);
//     if (ei.H2_b2) ot.H2_b2_qgl     = get_property(ei.H2_b2.get(),Jet_qgl);

//     COPY_OPTIONAL_m_pt_eta_phi_p4(H1)
//     if(ei.H1_bb_DeltaR) ot.H1_bb_DeltaR  = *ei.H1_bb_DeltaR;
//     COPY_OPTIONAL_m_pt_eta_phi_p4(H2)
//     if(ei.H2_bb_DeltaR) ot.H2_bb_DeltaR  = *ei.H2_bb_DeltaR;
//     COPY_OPTIONAL_m_pt_eta_phi_p4(HH)
//     if(ei.HH_2DdeltaM) ot.HH_2DdeltaM  = *ei.HH_2DdeltaM;
//     if(ei.HH_m_kinFit) ot.HH_m_kinFit  = *ei.HH_m_kinFit;
 
//     //set the variables for TTEMU studies
//     COPY_OPTIONAL_m_pt_eta_phi_p4(H1unregressed)
//     COPY_OPTIONAL_m_pt_eta_phi_p4(H2unregressed)
//     COPY_OPTIONAL_m_pt_eta_phi_p4(HHunregressed)    

//     COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_p4(TT_b1)
//     if (ei.TT_b1) ot.TT_b1_deepCSV = get_property(ei.TT_b1.get(),Jet_btagDeepB);   
//     COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_p4(TT_b2)
//     if (ei.TT_b2) ot.TT_b2_deepCSV = get_property(ei.TT_b2.get(),Jet_btagDeepB);
//     COPY_OPTIONAL_m_pt_eta_phi_p4(TT_e)
//     COPY_OPTIONAL_m_pt_eta_phi_p4(TT_mu)
//     if(ei.TT_m) ot.TT_m  = *ei.TT_m;            
//     if(ei.TT_nPV) ot.TT_nPV  = *ei.TT_nPV;
//     if(ei.TT_nPVgood) ot.TT_nPVgood  = *ei.TT_nPVgood;
//     if(ei.TT_nJet) ot.TT_nJet  = *ei.TT_nJet;    
//     //set the variables for non-resonant analysis and studies
//     if(ei.EventCount) ot.EventCount = *ei.EventCount;    
//     if(ei.btaggerID) ot.btaggerID   = *ei.btaggerID;
//     if(ei.H1_b1_rawpt) ot.H1_b1_rawpt = *ei.H1_b1_rawpt;
//     if(ei.H1_b2_rawpt) ot.H1_b2_rawpt = *ei.H1_b2_rawpt;
//     if(ei.H2_b1_rawpt) ot.H2_b1_rawpt = *ei.H2_b1_rawpt;
//     if(ei.H2_b2_rawpt) ot.H2_b2_rawpt = *ei.H2_b2_rawpt;
//     if(ei.H1_b1_genJetIdx) ot.H1_b1_genJetIdx  = *ei.H1_b1_genJetIdx;
//     if(ei.H1_b2_genJetIdx) ot.H1_b2_genJetIdx  = *ei.H1_b2_genJetIdx;
//     if(ei.H2_b1_genJetIdx) ot.H2_b1_genJetIdx  = *ei.H2_b1_genJetIdx;
//     if(ei.H2_b2_genJetIdx) ot.H2_b2_genJetIdx  = *ei.H2_b2_genJetIdx;
//     if(ei.H1_b1_partonFlavour) ot.H1_b1_partonFlavour  = *ei.H1_b1_partonFlavour;
//     if(ei.H1_b2_partonFlavour) ot.H1_b2_partonFlavour  = *ei.H1_b2_partonFlavour;
//     if(ei.H2_b1_partonFlavour) ot.H2_b1_partonFlavour  = *ei.H2_b1_partonFlavour;
//     if(ei.H2_b2_partonFlavour) ot.H2_b2_partonFlavour  = *ei.H2_b2_partonFlavour;    
//     if(ei.H1_b1_hadronFlavour) ot.H1_b1_hadronFlavour  = *ei.H1_b1_hadronFlavour;
//     if(ei.H1_b2_hadronFlavour) ot.H1_b2_hadronFlavour  = *ei.H1_b2_hadronFlavour;
//     if(ei.H2_b1_hadronFlavour) ot.H2_b1_hadronFlavour  = *ei.H2_b1_hadronFlavour;
//     if(ei.H2_b2_hadronFlavour) ot.H2_b2_hadronFlavour  = *ei.H2_b2_hadronFlavour;
//     COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_p4(HH_b1)
//     if(ei.HH_b1)                ot.HH_b1_deepCSV  = get_property(ei.HH_b1.get(),Jet_btagDeepB);
//     if(ei.HH_b1)                ot.HH_b1_deepJet  = get_property(ei.HH_b1.get(),Jet_btagDeepFlavB);
//     if(ei.HH_b1)                ot.HH_b1_bRegRes  = get_property(ei.HH_b1.get(),Jet_bRegRes);
//     if(ei.HH_b1)                ot.HH_b1_qgl      = get_property(ei.HH_b1.get(),Jet_qgl);
//     if(ei.HH_b1) ot.HH_b1_jetId                   = get_property(ei.HH_b1.get(),Jet_jetId); 
//     if(ei.HH_b1) ot.HH_b1_puId                    = get_property(ei.HH_b1.get(),Jet_puId);
//     if(ei.HH_b1_rawpt) ot.HH_b1_rawpt   = *ei.HH_b1_rawpt;
//     if(ei.HH_b1_genJetIdx)        ot.HH_b1_genJetIdx = *ei.HH_b1_genJetIdx;
//     if(ei.HH_b1_partonFlavour)        ot.HH_b1_partonFlavour = *ei.HH_b1_partonFlavour;   
//     if(ei.HH_b1_hadronFlavour)        ot.HH_b1_hadronFlavour = *ei.HH_b1_hadronFlavour; 
//     COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_p4(HH_b2)
//     if(ei.HH_b2)                ot.HH_b2_deepCSV = get_property(ei.HH_b2.get(),Jet_btagDeepB);
//     if(ei.HH_b2)                ot.HH_b2_deepJet  = get_property(ei.HH_b2.get(),Jet_btagDeepFlavB);
//     if(ei.HH_b2)                ot.HH_b2_bRegRes = get_property(ei.HH_b2.get(),Jet_bRegRes);    
//     if(ei.HH_b2)                ot.HH_b2_qgl = get_property(ei.HH_b2.get(),Jet_qgl);
//     if(ei.HH_b2) ot.HH_b2_jetId   = get_property(ei.HH_b2.get(),Jet_jetId); 
//     if(ei.HH_b2) ot.HH_b2_puId    = get_property(ei.HH_b2.get(),Jet_puId);
//     if(ei.HH_b2_rawpt) ot.HH_b2_rawpt   = *ei.HH_b2_rawpt;
//     if(ei.HH_b2_genJetIdx)        ot.HH_b2_genJetIdx = *ei.HH_b2_genJetIdx;
//     if(ei.HH_b2_partonFlavour)        ot.HH_b2_partonFlavour = *ei.HH_b2_partonFlavour; 
//     if(ei.HH_b2_hadronFlavour)        ot.HH_b2_hadronFlavour = *ei.HH_b2_hadronFlavour; 
//     COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_p4(HH_b3)
//     if(ei.HH_b3)                ot.HH_b3_deepCSV = get_property(ei.HH_b3.get(),Jet_btagDeepB);
//     if(ei.HH_b3)                ot.HH_b3_deepJet = get_property(ei.HH_b3.get(),Jet_btagDeepFlavB);
//     if(ei.HH_b3)                ot.HH_b3_bRegRes = get_property(ei.HH_b3.get(),Jet_bRegRes);
//     if(ei.HH_b3)                ot.HH_b3_qgl = get_property(ei.HH_b3.get(),Jet_qgl);
//     if(ei.HH_b3) ot.HH_b3_jetId   = get_property(ei.HH_b3.get(),Jet_jetId); 
//     if(ei.HH_b3) ot.HH_b3_puId    = get_property(ei.HH_b3.get(),Jet_puId);
//     if(ei.HH_b3_rawpt) ot.HH_b3_rawpt   = *ei.HH_b3_rawpt;
//     if(ei.HH_b3_genJetIdx)                ot.HH_b3_genJetIdx = *ei.HH_b3_genJetIdx;
//     if(ei.HH_b3_partonFlavour)        ot.HH_b3_partonFlavour = *ei.HH_b3_partonFlavour;
//     if(ei.HH_b3_hadronFlavour)        ot.HH_b3_hadronFlavour = *ei.HH_b3_hadronFlavour;
//     COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_p4(HH_b4)
//     if(ei.HH_b4) ot.HH_b4_deepCSV = get_property(ei.HH_b4.get(),Jet_btagDeepB);
//     if(ei.HH_b4) ot.HH_b4_deepJet = get_property(ei.HH_b4.get(),Jet_btagDeepFlavB);
//     if(ei.HH_b4) ot.HH_b4_bRegRes = get_property(ei.HH_b4.get(),Jet_bRegRes);
//     if(ei.HH_b4)     ot.HH_b4_qgl = get_property(ei.HH_b4.get(),Jet_qgl);
//     if(ei.HH_b4) ot.HH_b4_jetId   = get_property(ei.HH_b4.get(),Jet_jetId); 
//     if(ei.HH_b4) ot.HH_b4_puId    = get_property(ei.HH_b4.get(),Jet_puId);
//     if(ei.HH_b4_rawpt) ot.HH_b4_rawpt   = *ei.HH_b4_rawpt;
//     if(ei.HH_b4_genJetIdx)                ot.HH_b4_genJetIdx = *ei.HH_b4_genJetIdx;    
//     if(ei.HH_b4_partonFlavour)        ot.HH_b4_partonFlavour = *ei.HH_b4_partonFlavour;
//     if(ei.HH_b4_hadronFlavour)        ot.HH_b4_hadronFlavour = *ei.HH_b4_hadronFlavour;
//     COPY_OPTIONAL_m_pt_eta_phi_p4(JJ_j1)
//     if(ei.JJ_j1)                ot.JJ_j1_deepCSV  = get_property(ei.JJ_j1.get(),Jet_btagDeepB);
//     if(ei.JJ_j1)                ot.JJ_j1_deepJet  = get_property(ei.JJ_j1.get(),Jet_btagDeepFlavB);
//     if(ei.JJ_j1)                ot.JJ_j1_qgl = get_property(ei.JJ_j1.get(),Jet_qgl);
//     if(ei.JJ_j1) ot.JJ_j1_jetId   = get_property(ei.JJ_j1.get(),Jet_jetId); 
//     if(ei.JJ_j1) ot.JJ_j1_puId    = get_property(ei.JJ_j1.get(),Jet_puId);
//     if(ei.JJ_j1_rawpt) ot.JJ_j1_rawpt   = *ei.JJ_j1_rawpt;
//     if(ei.JJ_j1_genJetIdx)                ot.JJ_j1_genJetIdx = *ei.JJ_j1_genJetIdx;
//     if(ei.JJ_j1_partonFlavour)        ot.JJ_j1_partonFlavour = *ei.JJ_j1_partonFlavour;
//     if(ei.JJ_j1_hadronFlavour)        ot.JJ_j1_hadronFlavour = *ei.JJ_j1_hadronFlavour;
//     if(ei.JJ_j1_location)        ot.JJ_j1_location = *ei.JJ_j1_location;
//     COPY_OPTIONAL_m_pt_eta_phi_p4(JJ_j2)
//     if(ei.JJ_j2)                ot.JJ_j2_deepCSV = get_property(ei.JJ_j2.get(),Jet_btagDeepB);
//     if(ei.JJ_j2)                ot.JJ_j2_deepJet = get_property(ei.JJ_j2.get(),Jet_btagDeepFlavB);
//     if(ei.JJ_j2)                ot.JJ_j2_qgl = get_property(ei.JJ_j2.get(),Jet_qgl);
//     if(ei.JJ_j2) ot.JJ_j2_jetId   = get_property(ei.JJ_j2.get(),Jet_jetId); 
//     if(ei.JJ_j2) ot.JJ_j2_puId    = get_property(ei.JJ_j2.get(),Jet_puId);
//     if(ei.JJ_j2_rawpt) ot.JJ_j2_rawpt   = *ei.JJ_j2_rawpt;
//     if(ei.JJ_j2_genJetIdx)                ot.JJ_j2_genJetIdx = *ei.JJ_j2_genJetIdx;      
//     if(ei.JJ_j2_partonFlavour)        ot.JJ_j2_partonFlavour = *ei.JJ_j2_partonFlavour;
//     if(ei.JJ_j2_hadronFlavour)        ot.JJ_j2_hadronFlavour = *ei.JJ_j2_hadronFlavour;
//     if(ei.JJ_j2_location)        ot.JJ_j2_location = *ei.JJ_j2_location;
//     COPY_OPTIONAL_m_pt_eta_phi_p4(JJ)
//     COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_p4(HH_btag_b1)
//     if(ei.HH_btag_b1)                ot.HH_btag_b1_bscore = *ei.HH_btag_b1_bscore;
//     if(ei.HH_btag_b1)                ot.HH_btag_b1_bres   = *ei.HH_btag_b1_bres;
//     COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_p4(HH_btag_b2)
//     if(ei.HH_btag_b2)                ot.HH_btag_b2_bscore = *ei.HH_btag_b2_bscore;
//     if(ei.HH_btag_b2)                ot.HH_btag_b2_bres   = *ei.HH_btag_b2_bres;
//     COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_p4(HH_btag_b3)
//     if(ei.HH_btag_b3)                ot.HH_btag_b3_bscore = *ei.HH_btag_b3_bscore;
//     if(ei.HH_btag_b3)                ot.HH_btag_b3_bres   = *ei.HH_btag_b3_bres;
//     COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_p4(HH_btag_b4)
//     if(ei.HH_btag_b4)                ot.HH_btag_b4_bscore = *ei.HH_btag_b4_bscore;
//     if(ei.HH_btag_b4)                ot.HH_btag_b4_bres   = *ei.HH_btag_b4_bres;
//     if( ei.b1b2_deltaR) ot.b1b2_deltaR = *ei.b1b2_deltaR; 
//     if( ei.b1b3_deltaR) ot.b1b3_deltaR = *ei.b1b3_deltaR; 
//     if( ei.b1b4_deltaR) ot.b1b4_deltaR = *ei.b1b4_deltaR; 
//     if( ei.b1j1_deltaR) ot.b1j1_deltaR = *ei.b1j1_deltaR; 
//     if( ei.b1j2_deltaR) ot.b1j2_deltaR = *ei.b1j2_deltaR; 
//     if( ei.b2b3_deltaR) ot.b2b3_deltaR = *ei.b2b3_deltaR; 
//     if( ei.b2b4_deltaR) ot.b2b4_deltaR = *ei.b2b4_deltaR; 
//     if( ei.b2j1_deltaR) ot.b2j1_deltaR = *ei.b2j1_deltaR; 
//     if( ei.b2j2_deltaR) ot.b2j2_deltaR = *ei.b2j2_deltaR; 
//     if( ei.b3b4_deltaR) ot.b3b4_deltaR = *ei.b3b4_deltaR; 
//     if( ei.b3j1_deltaR) ot.b3j1_deltaR = *ei.b3j1_deltaR; 
//     if( ei.b3j2_deltaR) ot.b3j2_deltaR = *ei.b3j2_deltaR; 
//     if( ei.b4j1_deltaR) ot.b4j1_deltaR = *ei.b4j1_deltaR; 
//     if( ei.b4j2_deltaR) ot.b4j2_deltaR = *ei.b4j2_deltaR; 
//     if( ei.j1j2_deltaR) ot.j1j2_deltaR = *ei.j1j2_deltaR; 
//     if( ei.h1h2_deltaR) ot.h1h2_deltaR = *ei.h1h2_deltaR; 
//     if( ei.h1j1_deltaR) ot.h1j1_deltaR = *ei.h1j1_deltaR; 
//     if( ei.h1j2_deltaR) ot.h1j2_deltaR = *ei.h1j2_deltaR; 
//     if( ei.h2j1_deltaR) ot.h2j1_deltaR = *ei.h2j1_deltaR; 
//     if( ei.h2j2_deltaR) ot.h2j2_deltaR = *ei.h2j2_deltaR; 
//     if( ei.h1jj_deltaR) ot.h1jj_deltaR = *ei.h1jj_deltaR; 
//     if( ei.h2jj_deltaR) ot.h2jj_deltaR = *ei.h2jj_deltaR; 
//     if( ei.hhj1_deltaR) ot.hhj1_deltaR = *ei.hhj1_deltaR; 
//     if( ei.hhj2_deltaR) ot.hhj2_deltaR = *ei.hhj2_deltaR; 
//     if( ei.hhjj_deltaR) ot.hhjj_deltaR = *ei.hhjj_deltaR;
//     if( ei.b1b2_deltaPhi) ot.b1b2_deltaPhi = *ei.b1b2_deltaPhi; 
//     if( ei.b1b3_deltaPhi) ot.b1b3_deltaPhi = *ei.b1b3_deltaPhi; 
//     if( ei.b1b4_deltaPhi) ot.b1b4_deltaPhi = *ei.b1b4_deltaPhi; 
//     if( ei.b1j1_deltaPhi) ot.b1j1_deltaPhi = *ei.b1j1_deltaPhi; 
//     if( ei.b1j2_deltaPhi) ot.b1j2_deltaPhi = *ei.b1j2_deltaPhi; 
//     if( ei.b2b3_deltaPhi) ot.b2b3_deltaPhi = *ei.b2b3_deltaPhi; 
//     if( ei.b2b4_deltaPhi) ot.b2b4_deltaPhi = *ei.b2b4_deltaPhi; 
//     if( ei.b2j1_deltaPhi) ot.b2j1_deltaPhi = *ei.b2j1_deltaPhi; 
//     if( ei.b2j2_deltaPhi) ot.b2j2_deltaPhi = *ei.b2j2_deltaPhi; 
//     if( ei.b3b4_deltaPhi) ot.b3b4_deltaPhi = *ei.b3b4_deltaPhi; 
//     if( ei.b3j1_deltaPhi) ot.b3j1_deltaPhi = *ei.b3j1_deltaPhi; 
//     if( ei.b3j2_deltaPhi) ot.b3j2_deltaPhi = *ei.b3j2_deltaPhi; 
//     if( ei.b4j1_deltaPhi) ot.b4j1_deltaPhi = *ei.b4j1_deltaPhi; 
//     if( ei.b4j2_deltaPhi) ot.b4j2_deltaPhi = *ei.b4j2_deltaPhi; 
//     if( ei.j1j2_deltaPhi) ot.j1j2_deltaPhi = *ei.j1j2_deltaPhi; 
//     if( ei.b1b2_deltaEta) ot.b1b2_deltaEta = *ei.b1b2_deltaEta; 
//     if( ei.b1b3_deltaEta) ot.b1b3_deltaEta = *ei.b1b3_deltaEta; 
//     if( ei.b1b4_deltaEta) ot.b1b4_deltaEta = *ei.b1b4_deltaEta; 
//     if( ei.b1j1_deltaEta) ot.b1j1_deltaEta = *ei.b1j1_deltaEta; 
//     if( ei.b1j2_deltaEta) ot.b1j2_deltaEta = *ei.b1j2_deltaEta; 
//     if( ei.b2b3_deltaEta) ot.b2b3_deltaEta = *ei.b2b3_deltaEta; 
//     if( ei.b2b4_deltaEta) ot.b2b4_deltaEta = *ei.b2b4_deltaEta; 
//     if( ei.b2j1_deltaEta) ot.b2j1_deltaEta = *ei.b2j1_deltaEta; 
//     if( ei.b2j2_deltaEta) ot.b2j2_deltaEta = *ei.b2j2_deltaEta; 
//     if( ei.b3b4_deltaEta) ot.b3b4_deltaEta = *ei.b3b4_deltaEta; 
//     if( ei.b3j1_deltaEta) ot.b3j1_deltaEta = *ei.b3j1_deltaEta; 
//     if( ei.b3j2_deltaEta) ot.b3j2_deltaEta = *ei.b3j2_deltaEta; 
//     if( ei.b4j1_deltaEta) ot.b4j1_deltaEta = *ei.b4j1_deltaEta; 
//     if( ei.b4j2_deltaEta) ot.b4j2_deltaEta = *ei.b4j2_deltaEta; 
//     if( ei.j1j2_deltaEta) ot.j1j2_deltaEta = *ei.j1j2_deltaEta; 
//     if( ei.h1h2_deltaPhi) ot.h1h2_deltaPhi = *ei.h1h2_deltaPhi; 
//     if( ei.h1j1_deltaPhi) ot.h1j1_deltaPhi = *ei.h1j1_deltaPhi; 
//     if( ei.h1j2_deltaPhi) ot.h1j2_deltaPhi = *ei.h1j2_deltaPhi; 
//     if( ei.h2j1_deltaPhi) ot.h2j1_deltaPhi = *ei.h2j1_deltaPhi; 
//     if( ei.h2j2_deltaPhi) ot.h2j2_deltaPhi = *ei.h2j2_deltaPhi; 
//     if( ei.h1jj_deltaPhi) ot.h1jj_deltaPhi = *ei.h1jj_deltaPhi; 
//     if( ei.h2jj_deltaPhi) ot.h2jj_deltaPhi = *ei.h2jj_deltaPhi; 
//     if( ei.hhj1_deltaPhi) ot.hhj1_deltaPhi = *ei.hhj1_deltaPhi; 
//     if( ei.hhj2_deltaPhi) ot.hhj2_deltaPhi = *ei.hhj2_deltaPhi; 
//     if( ei.hhjj_deltaPhi) ot.hhjj_deltaPhi = *ei.hhjj_deltaPhi; 
//     if( ei.h1h2_deltaEta) ot.h1h2_deltaEta = *ei.h1h2_deltaEta; 
//     if( ei.h1j1_deltaEta) ot.h1j1_deltaEta = *ei.h1j1_deltaEta; 
//     if( ei.h1j2_deltaEta) ot.h1j2_deltaEta = *ei.h1j2_deltaEta; 
//     if( ei.h2j1_deltaEta) ot.h2j1_deltaEta = *ei.h2j1_deltaEta; 
//     if( ei.h2j2_deltaEta) ot.h2j2_deltaEta = *ei.h2j2_deltaEta; 
//     if( ei.h1jj_deltaEta) ot.h1jj_deltaEta = *ei.h1jj_deltaEta; 
//     if( ei.h2jj_deltaEta) ot.h2jj_deltaEta = *ei.h2jj_deltaEta; 
//     if( ei.hhj1_deltaEta) ot.hhj1_deltaEta = *ei.hhj1_deltaEta; 
//     if( ei.hhj2_deltaEta) ot.hhj2_deltaEta = *ei.hhj2_deltaEta; 
//     if( ei.hhjj_deltaEta) ot.hhjj_deltaEta = *ei.hhjj_deltaEta;
//     if( ei.hhjj_pt)       ot.hhjj_pt       = *ei.hhjj_pt;
//     if(ei.VBFEvent) ot.VBFEvent  = *ei.VBFEvent;
//     if(ei.nBtag) ot.nBtag  = *ei.nBtag;
//     if(ei.VBFEventLocation) ot.VBFEventLocation  = *ei.VBFEventLocation;
//     if( ei.nJet_brl ) ot.nJet_brl = *ei.nJet_brl;
//     if( ei.nJet_edc ) ot.nJet_edc = *ei.nJet_edc;
//     if( ei.nJet_fwd ) ot.nJet_fwd = *ei.nJet_fwd;
//     if( ei.nJet_tot ) ot.nJet_tot = *ei.nJet_tot;
//     if(ei.nJet) ot.nJet = *ei.nJet;
//     if(ei.nPVgood) ot.nPVgood  = *ei.nPVgood;
//     if(ei.nJet_ec) ot.nJet_ec = *ei.nJet_ec;
//     if(ei.nJet_hf) ot.nJet_hf = *ei.nJet_hf;
//     if(ei.HT_PT30) ot.HT_PT30 = *ei.HT_PT30;    
//     if(ei.HT_PT40) ot.HT_PT40 = *ei.HT_PT40; 
//     if(ei.maxj1etaj2eta) ot.maxj1etaj2eta = *ei.maxj1etaj2eta;
//     if(ei.j1etaj2eta) ot.j1etaj2eta = *ei.j1etaj2eta;
//     if(ei.BDT1) ot.BDT1 = *ei.BDT1;
//     if(ei.BDT2) ot.BDT2 = *ei.BDT2;
//     if(ei.BDT3) ot.BDT3 = *ei.BDT3;
//     if(ei.BDT3cat1) ot.BDT3cat1 = *ei.BDT3cat1;
//     if(ei.BDT3cat2) ot.BDT3cat2 = *ei.BDT3cat2;
//     if(ei.abs_costh_H1_vbfcm   ) ot.abs_costh_H1_vbfcm   = *ei.abs_costh_H1_vbfcm   ;       
//     if(ei.abs_costh_H2_vbfcm   ) ot.abs_costh_H2_vbfcm   = *ei.abs_costh_H2_vbfcm   ;   
//     if(ei.abs_costh_HH_vbfcm   ) ot.abs_costh_HH_vbfcm   = *ei.abs_costh_HH_vbfcm   ;   
//     if(ei.abs_costh_JJ_vbfcm   ) ot.abs_costh_JJ_vbfcm   = *ei.abs_costh_JJ_vbfcm   ;   
//     if(ei.abs_costh_HH_b1_vbfcm) ot.abs_costh_HH_b1_vbfcm= *ei.abs_costh_HH_b1_vbfcm;    
//     if(ei.abs_costh_HH_b2_vbfcm) ot.abs_costh_HH_b2_vbfcm= *ei.abs_costh_HH_b2_vbfcm;
//     if(ei.abs_costh_HH_b3_vbfcm) ot.abs_costh_HH_b3_vbfcm= *ei.abs_costh_HH_b3_vbfcm;    
//     if(ei.abs_costh_HH_b4_vbfcm) ot.abs_costh_HH_b4_vbfcm= *ei.abs_costh_HH_b4_vbfcm;
//     if(ei.abs_costh_JJ_j1_vbfcm) ot.abs_costh_JJ_j1_vbfcm= *ei.abs_costh_JJ_j1_vbfcm;    
//     if(ei.abs_costh_JJ_j2_vbfcm) ot.abs_costh_JJ_j2_vbfcm= *ei.abs_costh_JJ_j2_vbfcm;
//     if(ei.abs_costh_HH_b1_ggfcm) ot.abs_costh_HH_b1_ggfcm= *ei.abs_costh_HH_b1_ggfcm;    
//     if(ei.abs_costh_HH_b2_ggfcm) ot.abs_costh_HH_b2_ggfcm= *ei.abs_costh_HH_b2_ggfcm;
//     if(ei.abs_costh_HH_b3_ggfcm) ot.abs_costh_HH_b3_ggfcm= *ei.abs_costh_HH_b3_ggfcm;    
//     if(ei.abs_costh_HH_b4_ggfcm) ot.abs_costh_HH_b4_ggfcm= *ei.abs_costh_HH_b4_ggfcm;
//     if(ei.abs_costh_H1_ggfcm   ) ot.abs_costh_H1_ggfcm   = *ei.abs_costh_H1_ggfcm   ;       
//     if(ei.abs_costh_H2_ggfcm   ) ot.abs_costh_H2_ggfcm   = *ei.abs_costh_H2_ggfcm   ; 
//     if(ei.abs_costh_H1_b1_h1cm ) ot.abs_costh_H1_b1_h1cm = *ei.abs_costh_H1_b1_h1cm ;       
//     if(ei.abs_costh_H1_b2_h1cm ) ot.abs_costh_H1_b2_h1cm = *ei.abs_costh_H1_b2_h1cm ; 
//     if(ei.abs_costh_H2_b1_h2cm ) ot.abs_costh_H2_b1_h2cm = *ei.abs_costh_H2_b1_h2cm ;       
//     if(ei.abs_costh_H2_b2_h2cm ) ot.abs_costh_H2_b2_h2cm = *ei.abs_costh_H2_b2_h2cm ; 
//     if(ei.abs_costh_JJ_j1_jjcm ) ot.abs_costh_JJ_j1_jjcm = *ei.abs_costh_JJ_j1_jjcm ;       
//     if(ei.abs_costh_JJ_j2_jjcm ) ot.abs_costh_JJ_j2_jjcm = *ei.abs_costh_JJ_j2_jjcm ; 
//     if(ei.sum_4b_pt )            ot.sum_4b_pt            = *ei.sum_4b_pt; 
//     if(ei.sum_3b_bscore )        ot.sum_3b_bscore        = *ei.sum_3b_bscore; 
//     if(ei.sum_3b_bres   )        ot.sum_3b_bres          = *ei.sum_3b_bres; 
//     if(ei.min_4b_deltaR   ) ot.min_4b_deltaR   = *ei.min_4b_deltaR  ;
//     if(ei.min_4b_deltaPhi ) ot.min_4b_deltaPhi = *ei.min_4b_deltaPhi;
//     if(ei.min_4b_deltaEta ) ot.min_4b_deltaEta = *ei.min_4b_deltaEta;
//     if(ei.max_4b_deltaR   ) ot.max_4b_deltaR   = *ei.max_4b_deltaR  ;
//     if(ei.max_4b_deltaPhi ) ot.max_4b_deltaPhi = *ei.max_4b_deltaPhi;
//     if(ei.max_4b_deltaEta ) ot.max_4b_deltaEta = *ei.max_4b_deltaEta;
//     if(ei.min_4b_cm_deltaR   ) ot.min_4b_cm_deltaR   = *ei.min_4b_cm_deltaR  ;
//     if(ei.min_4b_cm_deltaPhi ) ot.min_4b_cm_deltaPhi = *ei.min_4b_cm_deltaPhi;
//     if(ei.min_4b_cm_deltaEta ) ot.min_4b_cm_deltaEta = *ei.min_4b_cm_deltaEta;
//     if(ei.max_4b_cm_deltaR   ) ot.max_4b_cm_deltaR   = *ei.max_4b_cm_deltaR  ;
//     if(ei.max_4b_cm_deltaPhi ) ot.max_4b_cm_deltaPhi = *ei.max_4b_cm_deltaPhi;
//     if(ei.max_4b_cm_deltaEta ) ot.max_4b_cm_deltaEta = *ei.max_4b_cm_deltaEta;
//     if(ei.min_hbb_deltaR) ot.min_hbb_deltaR = *ei.min_hbb_deltaR;
//     if(ei.max_hbb_deltaR) ot.max_hbb_deltaR = *ei.max_hbb_deltaR;

//     COPY_OPTIONAL_m_pt_eta_phi_p4(H1rand)
//     COPY_OPTIONAL_m_pt_eta_phi_p4(H2rand)
//     if(ei.H1_bb_deltaR) ot.H1_bb_deltaR= *ei.H1_bb_deltaR;
//     if(ei.H2_bb_deltaR) ot.H2_bb_deltaR= *ei.H2_bb_deltaR;
//     if(ei.H1_bb_deltaPhi) ot.H1_bb_deltaPhi= *ei.H1_bb_deltaPhi;
//     if(ei.H2_bb_deltaPhi) ot.H2_bb_deltaPhi= *ei.H2_bb_deltaPhi;
//     if(ei.H1_bb_deltaEta) ot.H1_bb_deltaEta= *ei.H1_bb_deltaEta;
//     if(ei.H2_bb_deltaEta) ot.H2_bb_deltaEta= *ei.H2_bb_deltaEta;

//     if(ei.H1_b1_qid) ot.H1_b1_qid = *ei.H1_b1_qid;
//     if(ei.H1_b2_qid) ot.H1_b2_qid = *ei.H1_b2_qid;
//     if(ei.H2_b1_qid) ot.H2_b1_qid = *ei.H2_b1_qid;
//     if(ei.H2_b2_qid) ot.H2_b2_qid = *ei.H2_b2_qid;
//     if(ei.JJ_j1_qid) ot.JJ_j1_qid = *ei.JJ_j1_qid;
//     if(ei.JJ_j2_qid) ot.JJ_j2_qid = *ei.JJ_j2_qid;
//     if(ei.H1_b1_qual) ot.H1_b1_qual = *ei.H1_b1_qual;
//     if(ei.H1_b2_qual) ot.H1_b2_qual = *ei.H1_b2_qual;
//     if(ei.H2_b1_qual) ot.H2_b1_qual = *ei.H2_b1_qual;
//     if(ei.H2_b2_qual) ot.H2_b2_qual = *ei.H2_b2_qual;
//     if(ei.JJ_j1_qual) ot.JJ_j1_qual = *ei.JJ_j1_qual;
//     if(ei.JJ_j2_qual) ot.JJ_j2_qual = *ei.JJ_j2_qual;
//     if(ei.H1_qual) ot.H1_qual = *ei.H1_qual;
//     if(ei.H2_qual) ot.H2_qual = *ei.H2_qual;
//     if(ei.HH_qual) ot.HH_qual = *ei.HH_qual;
//     if(ei.JJ_qual) ot.JJ_qual = *ei.JJ_qual;
//     // gen info are not stored for all samples --> set only if initialized (macro checks if object is initialized, else does not set)
//     COPY_OPTIONAL_m_pt_eta_phi_p4(gen_H1)
//     COPY_OPTIONAL_m_pt_eta_phi_p4(gen_H2)
//     COPY_OPTIONAL_m_pt_eta_phi_p4(gen_H1_last)
//     COPY_OPTIONAL_m_pt_eta_phi_p4(gen_H2_last)

//     if (ei.gen_H1 && ei.gen_H2)
//     {
//         TLorentzVector p4_HH = ei.gen_H1->P4() + ei.gen_H2->P4();
//         ot.gen_mHH = p4_HH.M();
//     }

//     COPY_OPTIONAL_m_pt_eta_phi_p4(gen_H1_b1)
//     COPY_OPTIONAL_m_pt_eta_phi_p4(gen_H1_b2)
//     COPY_OPTIONAL_m_pt_eta_phi_p4(gen_H2_b1)
//     COPY_OPTIONAL_m_pt_eta_phi_p4(gen_H2_b2)
//     COPY_OPTIONAL_m_pt_eta_phi_p4(gen_q1_in)
//     COPY_OPTIONAL_m_pt_eta_phi_p4(gen_q2_in)
//     COPY_OPTIONAL_m_pt_eta_phi_p4(gen_q1_out)
//     COPY_OPTIONAL_m_pt_eta_phi_p4(gen_q2_out) 
    
//     if (ei.gen_H1_b1 && ei.gen_H1_b2 && ei.gen_H2_b1 && ei.gen_H2_b2)
//     {
//       float dR1 =  ei.gen_H1_b1->P4().DeltaR(ei.gen_H1_b2->P4());
//       float dR2 =  ei.gen_H1_b1->P4().DeltaR(ei.gen_H2_b1->P4());
//       float dR3 =  ei.gen_H1_b1->P4().DeltaR(ei.gen_H2_b2->P4());
//       float dR4 =  ei.gen_H1_b2->P4().DeltaR(ei.gen_H2_b1->P4());
//       float dR5 =  ei.gen_H1_b2->P4().DeltaR(ei.gen_H2_b2->P4());
//       float dR6 =  ei.gen_H2_b1->P4().DeltaR(ei.gen_H2_b2->P4());
//       ot.gen_min_4b_deltaR  = std::min({dR1,dR2,dR3,dR4,dR5,dR6});
//       ot.gen_max_4b_deltaR  = std::max({dR1,dR2,dR3,dR4,dR5,dR6});
//       ot.gen_min_hbb_deltaR = std::min({dR1,dR6});
//       ot.gen_max_hbb_deltaR = std::min({dR1,dR6});
//     }

//     if (ei.gen_q1_out && ei.gen_q2_out)
//     {
//         TLorentzVector p4_JJ = ei.gen_q1_out->P4() + ei.gen_q2_out->P4();
//         ot.gen_mJJ = p4_JJ.M();
//         ot.gen_etapairsign = (ei.gen_q1_out->P4().Eta()*ei.gen_q2_out->P4().Eta())/abs(ei.gen_q1_out->P4().Eta()*ei.gen_q2_out->P4().Eta()) ;
//         ot.gen_deltaEtaJJ  = abs( ei.gen_q1_out->P4().Eta() - ei.gen_q2_out->P4().Eta() );
//     }    

//     if(ei.gen_H1_b1_jetidx)  ot.gen_H1_b1_jetidx =  *ei.gen_H1_b1_jetidx;
//     if(ei.gen_H1_b2_jetidx)  ot.gen_H1_b2_jetidx =  *ei.gen_H1_b2_jetidx;
//     if(ei.gen_H2_b1_jetidx)  ot.gen_H2_b1_jetidx =  *ei.gen_H2_b1_jetidx;
//     if(ei.gen_H2_b2_jetidx)  ot.gen_H2_b2_jetidx =  *ei.gen_H2_b2_jetidx;
//     if(ei.gen_q1_out_jetidx) ot.gen_q1_out_jetidx = *ei.gen_q1_out_jetidx; 
//     if(ei.gen_q2_out_jetidx) ot.gen_q2_out_jetidx = *ei.gen_q2_out_jetidx;
//     if(ei.gen_H1_b1_jetmatched)  ot.gen_H1_b1_jetmatched =  *ei.gen_H1_b1_jetmatched;
//     if(ei.gen_H1_b2_jetmatched)  ot.gen_H1_b2_jetmatched =  *ei.gen_H1_b2_jetmatched;
//     if(ei.gen_H2_b1_jetmatched)  ot.gen_H2_b1_jetmatched =  *ei.gen_H2_b1_jetmatched;
//     if(ei.gen_H2_b2_jetmatched)  ot.gen_H2_b2_jetmatched =  *ei.gen_H2_b2_jetmatched;
//     if(ei.gen_q1_out_jetmatched) ot.gen_q1_out_jetmatched = *ei.gen_q1_out_jetmatched; 
//     if(ei.gen_q2_out_jetmatched) ot.gen_q2_out_jetmatched = *ei.gen_q2_out_jetmatched;
//     if(ei.gen_HH_qual) ot.gen_HH_qual = *ei.gen_HH_qual;
//     if(ei.gen_qq_qual) ot.gen_qq_qual = *ei.gen_qq_qual;

//     //XYH stuff
//     if(ei.gen_H1_b1_matchedflag) ot.gen_H1_b1_matchedflag  = *ei.gen_H1_b1_matchedflag;
//     if(ei.gen_H1_b2_matchedflag) ot.gen_H1_b2_matchedflag  = *ei.gen_H1_b2_matchedflag;
//     if(ei.gen_H2_b1_matchedflag) ot.gen_H2_b1_matchedflag  = *ei.gen_H2_b1_matchedflag;
//     if(ei.gen_H2_b2_matchedflag) ot.gen_H2_b2_matchedflag = *ei.gen_H2_b2_matchedflag;
//     if(ei.recoJetMatchedToGenJet1) ot.recoJetMatchedToGenJet1 = *ei.recoJetMatchedToGenJet1;
//     if(ei.recoJetMatchedToGenJet2) ot.recoJetMatchedToGenJet2 = *ei.recoJetMatchedToGenJet2;
//     if(ei.recoJetMatchedToGenJet3) ot.recoJetMatchedToGenJet3 = *ei.recoJetMatchedToGenJet3;
//     if(ei.recoJetMatchedToGenJet4) ot.recoJetMatchedToGenJet4 = *ei.recoJetMatchedToGenJet4;

//     // fill the tree
//     ot.fill();
>>>>>>> ae2ad916f162dd3fc5729fffb6628d530478ef2c

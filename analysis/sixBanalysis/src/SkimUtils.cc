#include "SkimUtils.h"

#include "Math/Vector4D.h"
typedef ROOT::Math::PtEtaPhiMVector p4_t;

#include <iostream>
#include <fstream>
#include <string>

using namespace std;

// helper: copies the pt/eta/phi/p4 branches from a candidate OBJ to the output tree
// NOTE: requires the matching of the names (and enforces it)
#define COPY_m_pt_eta_phi_p4(OBJ)		\
  ot.OBJ ## _m   = ei. OBJ -> P4().M();		\
  ot.OBJ ## _pt  = ei. OBJ -> P4().Pt();	\
  ot.OBJ ## _eta = ei. OBJ -> P4().Eta();	\
  ot.OBJ ## _phi = ei. OBJ -> P4().Phi();	\
  ot.OBJ ## _p4  = ei. OBJ -> P4();

#define COPY_m_pt_ptRegressed_eta_phi_p4(OBJ)			\
  ot.OBJ ## _m            = ei. OBJ -> P4().M();		\
  ot.OBJ ## _pt           = ei. OBJ -> P4().Pt();		\
  ot.OBJ ## _ptRegressed  = ei. OBJ -> P4Regressed().Pt();	\
  ot.OBJ ## _eta          = ei. OBJ -> P4().Eta();		\
  ot.OBJ ## _phi          = ei. OBJ -> P4().Phi();		\
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
  if(ei.n_nn_higgs)     ot.n_nn_higgs      = *ei.n_nn_higgs;

  if(ei.b_6j_score)     ot.b_6j_score      = *ei.b_6j_score;
  if(ei.b_3h_score)     ot.b_3h_score      = *ei.b_3h_score;

  if (ei.jet_list) {
    for (Jet& jet : ei.jet_list.get()) {
      ot.jet_E.push_back( jet.get_E() );	    
      ot.jet_m.push_back( jet.get_m() );		
      ot.jet_pt.push_back( jet.get_pt() );
      ot.jet_eta.push_back( jet.get_eta() );		
      ot.jet_phi.push_back( jet.get_phi() );		
      // ot.jet_partonFlav.push_back( jet.get_partonFlav() );
      // ot.jet_hadronFlav.push_back( jet.get_hadronFlav() );
      ot.jet_signalId.push_back( jet.get_signalId() );
      ot.jet_higgsId.push_back( jet.get_higgsId() );
      ot.jet_nn_higgsId.push_back( jet.get_nn_higgsId() );
      ot.jet_genIdx.push_back( jet.get_genIdx() );
      ot.jet_btag.push_back( jet.get_btag() );
      ot.jet_qgl.push_back( jet.get_qgl() );
      ot.jet_id.push_back( jet.get_id() );
      ot.jet_puid.push_back( jet.get_puid() );
    }
  }

  if (ei.higgs_list) {
    for (DiJet& higgs : ei.higgs_list.get()) {
      ot.higgs_E.push_back( higgs.E() );
      ot.higgs_m.push_back( higgs.M() );
      ot.higgs_pt.push_back( higgs.Pt() );
      ot.higgs_eta.push_back( higgs.Eta() );
      ot.higgs_phi.push_back( higgs.Phi() );
      ot.higgs_signalId.push_back( higgs.get_signalId() );
    }
  }
	
  if (ei.nn_higgs_list) {
    for (DiJet& nn_higgs : ei.nn_higgs_list.get()) {
      ot.nn_higgs_E.push_back( nn_higgs.E() );
      ot.nn_higgs_m.push_back( nn_higgs.M() );
      ot.nn_higgs_pt.push_back( nn_higgs.Pt() );
      ot.nn_higgs_eta.push_back( nn_higgs.Eta() );
      ot.nn_higgs_phi.push_back( nn_higgs.Phi() );
      ot.nn_higgs_signalId.push_back( nn_higgs.get_signalId() );
      ot.nn_higgs_2j_score.push_back( nn_higgs.get_2j_score() );
    }
  }

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

  if (ei.event_shapes) {
    ot.sphericity = ei.event_shapes.get().sphericity;
    ot.sphericity_t = ei.event_shapes.get().transverse_sphericity;
    ot.aplanarity = ei.event_shapes.get().aplanarity;
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

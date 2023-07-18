#include "SkimUtils.h"

#include "Math/Vector4D.h"
typedef ROOT::Math::PtEtaPhiMVector p4_t;

#include <iostream>
#include <fstream>
#include <string>

using namespace std;

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
  if(ei.PFHT)           ot.PFHT            = *ei.PFHT;
  if(ei.lhe_ht)         ot.lhe_ht          = *ei.lhe_ht;
  if(ei.n_jet)          ot.n_jet           = *ei.n_jet;
  if(ei.n_total_jet)    ot.n_total_jet     = *ei.n_total_jet;
  if(ei.n_genjet)       ot.n_genjet        = *ei.n_genjet;
  if(ei.n_higgs)        ot.n_higgs         = *ei.n_higgs;
  if(ei.n_fatjet)       ot.n_fatjet        = *ei.n_fatjet;
  if(ei.n_genfatjet)    ot.n_genfatjet     = *ei.n_genfatjet;
  if(ei.n_ele)          ot.n_ele           = *ei.n_ele;
  if(ei.n_muon)         ot.n_muon          = *ei.n_muon;
  
  if(ei.b_6j_score)     ot.b_6j_score      = *ei.b_6j_score;
  if(ei.b_3d_score)     ot.b_3d_score      = *ei.b_3d_score;

  ot.ele.FillOptional(ei.ele_list);
  ot.muon.FillOptional(ei.muon_list);

  ot.jet.FillOptional(ei.jet_list);
  ot.fatjet.FillOptional(ei.fatjet_list);

  ot.genpb.FillOptional(ei.genpb_list);
  ot.genjet.FillOptional(ei.genjet_list);
  ot.genfatjet.FillOptional(ei.genfatjet_list);

  if (ei.event_shapes) {
    ot.sphericity   = ei.event_shapes.get().sphericity;
    ot.sphericity_t = ei.event_shapes.get().transverse_sphericity;
    ot.aplanarity   = ei.event_shapes.get().aplanarity;
  }

  ot.gen_H1_fc.FillOptional(ei.gen_H1_fc);
  ot.gen_H2_fc.FillOptional(ei.gen_H2_fc);
  ot.gen_H1_b1_genfatjet.FillOptional(ei.gen_H1_b1_genfatjet);
  ot.gen_H1_b2_genfatjet.FillOptional(ei.gen_H1_b2_genfatjet);
  ot.gen_H2_b1_genfatjet.FillOptional(ei.gen_H2_b1_genfatjet);
  ot.gen_H2_b2_genfatjet.FillOptional(ei.gen_H2_b2_genfatjet);
  ot.gen_H1_b1_recofatjet.FillOptional(ei.gen_H1_b1_recofatjet);
  ot.gen_H1_b2_recofatjet.FillOptional(ei.gen_H1_b2_recofatjet);
  ot.gen_H2_b1_recofatjet.FillOptional(ei.gen_H2_b1_recofatjet);
  ot.gen_H2_b2_recofatjet.FillOptional(ei.gen_H2_b2_recofatjet);
  
  ot.gen_X_fc.FillOptional(ei.gen_X_fc);
  ot.gen_X.FillOptional(ei.gen_X);
  
  // Start Gen 6B Objects
  ot.gen_Y.FillOptional(ei.gen_Y);
  ot.gen_HX.FillOptional(ei.gen_HX);
  ot.gen_H1.FillOptional(ei.gen_H1);
  ot.gen_H2.FillOptional(ei.gen_H2);

  ot.gen_HX_b1.FillOptional(ei.gen_HX_b1);
  ot.gen_HX_b2.FillOptional(ei.gen_HX_b2);
  ot.gen_H1_b1.FillOptional(ei.gen_H1_b1);
  ot.gen_H1_b2.FillOptional(ei.gen_H1_b2);
  ot.gen_H2_b1.FillOptional(ei.gen_H2_b1);
  ot.gen_H2_b2.FillOptional(ei.gen_H2_b2);

   ot.gen_HX_b1_genjet.FillOptional(ei.gen_HX_b1_genjet);
   ot.gen_HX_b2_genjet.FillOptional(ei.gen_HX_b2_genjet);
   ot.gen_H1_b1_genjet.FillOptional(ei.gen_H1_b1_genjet);
   ot.gen_H1_b2_genjet.FillOptional(ei.gen_H1_b2_genjet);
   ot.gen_H2_b1_genjet.FillOptional(ei.gen_H2_b1_genjet);
   ot.gen_H2_b2_genjet.FillOptional(ei.gen_H2_b2_genjet);

   ot.gen_HX_b1_recojet.FillOptional(ei.gen_HX_b1_recojet);
   ot.gen_HX_b2_recojet.FillOptional(ei.gen_HX_b2_recojet);
   ot.gen_H1_b1_recojet.FillOptional(ei.gen_H1_b1_recojet);
   ot.gen_H1_b2_recojet.FillOptional(ei.gen_H1_b2_recojet);
   ot.gen_H2_b1_recojet.FillOptional(ei.gen_H2_b1_recojet);
   ot.gen_H2_b2_recojet.FillOptional(ei.gen_H2_b2_recojet);
  // End Gen 6B Objects

  // Start Gen 8B Objects
  ot.gen_Y1.FillOptional(ei.gen_Y1);
  ot.gen_Y2.FillOptional(ei.gen_Y2);
  ot.gen_H1Y1.FillOptional(ei.gen_H1Y1);
  ot.gen_H2Y1.FillOptional(ei.gen_H2Y1);
  ot.gen_H1Y2.FillOptional(ei.gen_H1Y2);
  ot.gen_H2Y2.FillOptional(ei.gen_H2Y2);

  ot.gen_H1Y1_b1.FillOptional(ei.gen_H1Y1_b1);
  ot.gen_H1Y1_b2.FillOptional(ei.gen_H1Y1_b2);
  ot.gen_H2Y1_b1.FillOptional(ei.gen_H2Y1_b1);
  ot.gen_H2Y1_b2.FillOptional(ei.gen_H2Y1_b2);
  ot.gen_H1Y2_b1.FillOptional(ei.gen_H1Y2_b1);
  ot.gen_H1Y2_b2.FillOptional(ei.gen_H1Y2_b2);
  ot.gen_H2Y2_b1.FillOptional(ei.gen_H2Y2_b1);
  ot.gen_H2Y2_b2.FillOptional(ei.gen_H2Y2_b2);
  
  ot.gen_H1Y1_b1_genjet.FillOptional(ei.gen_H1Y1_b1_genjet);
  ot.gen_H1Y1_b2_genjet.FillOptional(ei.gen_H1Y1_b2_genjet);
  ot.gen_H2Y1_b1_genjet.FillOptional(ei.gen_H2Y1_b1_genjet);
  ot.gen_H2Y1_b2_genjet.FillOptional(ei.gen_H2Y1_b2_genjet);
  ot.gen_H1Y2_b1_genjet.FillOptional(ei.gen_H1Y2_b1_genjet);
  ot.gen_H1Y2_b2_genjet.FillOptional(ei.gen_H1Y2_b2_genjet);
  ot.gen_H2Y2_b1_genjet.FillOptional(ei.gen_H2Y2_b1_genjet);
  ot.gen_H2Y2_b2_genjet.FillOptional(ei.gen_H2Y2_b2_genjet);

  ot.gen_H1Y1_b1_recojet.FillOptional(ei.gen_H1Y1_b1_recojet);
  ot.gen_H1Y1_b2_recojet.FillOptional(ei.gen_H1Y1_b2_recojet);
  ot.gen_H2Y1_b1_recojet.FillOptional(ei.gen_H2Y1_b1_recojet);
  ot.gen_H2Y1_b2_recojet.FillOptional(ei.gen_H2Y1_b2_recojet);
  ot.gen_H1Y2_b1_recojet.FillOptional(ei.gen_H1Y2_b1_recojet);
  ot.gen_H1Y2_b2_recojet.FillOptional(ei.gen_H1Y2_b2_recojet);
  ot.gen_H2Y2_b1_recojet.FillOptional(ei.gen_H2Y2_b1_recojet);
  ot.gen_H2Y2_b2_recojet.FillOptional(ei.gen_H2Y2_b2_recojet);
  // End Gen 8B Objects

  if (ei.gen_bs_N_reco_match)        ot.gen_bs_N_reco_match        = *ei.gen_bs_N_reco_match;
  if (ei.gen_bs_N_reco_match_in_acc) ot.gen_bs_N_reco_match_in_acc = *ei.gen_bs_N_reco_match_in_acc;
  if (ei.gen_bs_match_recojet_minv)        ot.gen_bs_match_recojet_minv        = *ei.gen_bs_match_recojet_minv;
  if (ei.gen_bs_match_in_acc_recojet_minv) ot.gen_bs_match_in_acc_recojet_minv = *ei.gen_bs_match_in_acc_recojet_minv;

  ot.X.FillOptional(ei.X);
  // Start Reco 6B Objects
  ot.Y.FillOptional(ei.Y);
  ot.HX.FillOptional(ei.HX);
  ot.H1.FillOptional(ei.H1);
  ot.H2.FillOptional(ei.H2);

   ot.HX_b1.FillOptional(ei.HX_b1);
   ot.HX_b2.FillOptional(ei.HX_b2);
   ot.H1_b1.FillOptional(ei.H1_b1);
   ot.H1_b2.FillOptional(ei.H1_b2);
   ot.H2_b1.FillOptional(ei.H2_b1);
   ot.H2_b2.FillOptional(ei.H2_b2);

  if (ei.HX_b1_genHflag)  ot.HX_b1_genHflag  = *ei.HX_b1_genHflag;
  if (ei.HX_b2_genHflag)  ot.HX_b2_genHflag  = *ei.HX_b2_genHflag;
  if (ei.H1_b1_genHflag) ot.H1_b1_genHflag = *ei.H1_b1_genHflag;
  if (ei.H1_b2_genHflag) ot.H1_b2_genHflag = *ei.H1_b2_genHflag;
  if (ei.H2_b1_genHflag) ot.H2_b1_genHflag = *ei.H2_b1_genHflag;
  if (ei.H2_b2_genHflag) ot.H2_b2_genHflag = *ei.H2_b2_genHflag;
  // End Reco 6B Objects

  // Start Reco 8B Objects
  ot.Y1.FillOptional(ei.Y1);
  ot.Y2.FillOptional(ei.Y2);
  ot.H1Y1.FillOptional(ei.H1Y1);
  ot.H2Y1.FillOptional(ei.H2Y1);
  ot.H1Y2.FillOptional(ei.H1Y2);
  ot.H2Y2.FillOptional(ei.H2Y2);

  ot.H1Y1_b1.FillOptional(ei.H1Y1_b1);
  ot.H1Y1_b2.FillOptional(ei.H1Y1_b2);
  ot.H2Y1_b1.FillOptional(ei.H2Y1_b1);
  ot.H2Y1_b2.FillOptional(ei.H2Y1_b2);
  ot.H1Y2_b1.FillOptional(ei.H1Y2_b1);
  ot.H1Y2_b2.FillOptional(ei.H1Y2_b2);
  ot.H2Y2_b1.FillOptional(ei.H2Y2_b1);
  ot.H2Y2_b2.FillOptional(ei.H2Y2_b2);

  if (ei.n_loose_btag) ot.n_loose_btag = *ei.n_loose_btag;
  if (ei.n_medium_btag) ot.n_medium_btag = *ei.n_medium_btag;
  if (ei.n_tight_btag) ot.n_tight_btag = *ei.n_tight_btag;
  if (ei.btagavg) ot.btagavg = *ei.btagavg;
  // End Reco 8B Objects

  if (ei.nfound_all) ot.nfound_all = *ei.nfound_all;
  if (ei.nfound_all_h) ot.nfound_all_h = *ei.nfound_all_h;
  if (ei.nfound_presel) ot.nfound_presel = *ei.nfound_presel;
  if (ei.nfound_presel_h) ot.nfound_presel_h = *ei.nfound_presel_h;
  if (ei.nfound_select) ot.nfound_select = *ei.nfound_select;
  if (ei.nfound_select_h) ot.nfound_select_h = *ei.nfound_select_h;
  if (ei.nfound_paired_h) ot.nfound_paired_h = *ei.nfound_paired_h;
  if (ei.nfound_select_y) ot.nfound_select_y = *ei.nfound_select_y;
  if (ei.nfound_paired_y) ot.nfound_paired_y = *ei.nfound_paired_y;

  //COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_DeepJet_p4(bjet1);
  //COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_DeepJet_p4(bjet2);

  // must check validity of reader because this is not defined in data
  //if (ei.bjet1 && nat.Jet_hadronFlavour.IsValid())
  //  ot.bjet1_hadflav = get_property(ei.bjet1.get(), Jet_hadronFlavour);

  //if (ei.bjet2 && nat.Jet_hadronFlavour.IsValid())
  //  ot.bjet2_hadflav = get_property(ei.bjet2.get(), Jet_hadronFlavour);

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

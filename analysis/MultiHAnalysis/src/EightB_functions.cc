#include "EightB_functions.h"
#include "Math/VectorUtil.h"
#include "Math/Vector3D.h"
#include "Math/Functions.h"

#include "BuildClassifierInput.h"

#include "DebugUtils.h"

#include <iostream>
#include <tuple>
#include <algorithm>
#include <limits>

#include "Electron.h"
#include "Muon.h"

using namespace std;

void EightB_functions::initialize_params_from_cfg(CfgParser& config)
{
  

  // preselections
  pmap.insert_param<bool>("presel","apply", config.readBoolOpt("presel::apply"));
  pmap.insert_param<std::vector<double> >("presel", "pt_min", config.readDoubleListOpt("presel::pt_min"));
  pmap.insert_param<double>("presel", "eta_max", config.readDoubleOpt("presel::eta_max"));
  pmap.insert_param<int>   ("presel", "pf_id",   config.readIntOpt("presel::pf_id"));
  pmap.insert_param<int>   ("presel", "pu_id",   config.readIntOpt("presel::pu_id"));
  
  // eightb jet choice
  pmap.insert_param<string>("configurations", "eightbJetChoice", config.readStringOpt("configurations::eightbJetChoice"));
  
  // Pair 4H first or 2Y first
  pmap.insert_param<bool>("configurations", "pair4Hfirst", config.readBoolOpt("configurations::pair4Hfirst"));

  // HHHH pairing
  pmap.insert_param<string>("configurations", "jetPairsChoice", config.readStringOpt("configurations::jetPairsChoice"));

  // YY pairing
  pmap.insert_param<string>("configurations", "YYChoice", config.readStringOpt("configurations::YYChoice"));

  // H done with regressed pT
  pmap.insert_param<bool>("configurations", "useRegressedPtForHp4", config.readBoolOpt("configurations::useRegressedPtForHp4"));

  
  if (pmap.get_param<string> ("configurations", "jetPairsChoice") == "gnn_dijet") {
      pmap.insert_param<string> ("GNN", "model_path", config.readStringOpt("GNN::model_path"));
      pmap.insert_param<string> ("GNN", "output", config.readStringOpt("GNN::output"));
  }
  
  if (pmap.get_param<string> ("configurations", "eightbJetChoice") == "gnn_jet") {
      pmap.insert_param<string> ("GNN", "model_path", config.readStringOpt("GNN::model_path"));
  }
}

void EightB_functions::initialize_functions(TFile& outputFile)
{
  if (pmap.get_param<string>("configurations", "jetPairsChoice") == "gnn_dijet") {
    cout << "[INFO] ... Loading GNN: " << pmap.get_param<string>("GNN", "model_path") << endl;
    // gnn_classifier_ = std::unique_ptr<TorchUtils::GeoModel> (new TorchUtils::GeoModel(pmap.get_param<string>("GNN", "model_path")));
    onnx_classifier_ =
        std::unique_ptr<EvalONNX>(new EvalONNX("particle_net", pmap.get_param<string>("GNN", "model_path")));
  }

  if (pmap.get_param<string>("configurations", "eightbJetChoice") == "gnn_jet")
  {
    cout << "[INFO] ... Loading GNN: " << pmap.get_param<string>("GNN", "model_path") << endl;
    // gnn_classifier_ = std::unique_ptr<TorchUtils::GeoModel> (new TorchUtils::GeoModel(pmap.get_param<string>("GNN", "model_path")));
    onnx_classifier_ =
        std::unique_ptr<EvalONNX>(new EvalONNX("particle_net", pmap.get_param<string>("GNN", "model_path")));
  }
}

bool EightB_functions::is_blinded(NanoAODTree& nat, EventInfo& ei, bool is_data) 
{
  bool blind = true;
  //  if (ei.n_medium_btag)
  //  blind = blind & ei.n_medium_btag.get() >= pmap.get_param<int>("blind","n_medium_btag");
  //  if (ei.quadh_score)
  //  blind = blind & ei.quadh_score.get() >= pmap.get_param<double>("blind","quadh_score");
  return blind;
}

void EightB_functions::select_gen_particles(NanoAODTree& nat, EventInfo& ei)
{
  for (uint igp = 0; igp < *(nat.nGenPart); ++igp)
  {
    GenPart gp(igp, &nat);
    int apdgid = abs(get_property(gp, GenPart_pdgId));

    // X
    if (apdgid == 45)
    {
      if (gp.isFirstCopy())
        ei.gen_X_fc = gp;
      else if (gp.isLastCopy())
        ei.gen_X = gp;
    }

    // Y
    if (apdgid == 35 && gp.isLastCopy())
    {
      assign_to_uninit(gp, {&ei.gen_Y1, &ei.gen_Y2});
    }

    // H
    if (apdgid == 25 && gp.isLastCopy())
    {
      int moth_idx = get_property(gp, GenPart_genPartIdxMother);
      if (moth_idx >= 0)
      {
        GenPart mother(moth_idx, &nat);
        int amothpdgid = abs(get_property(mother, GenPart_pdgId));

        if (amothpdgid == 35)
        {
          if (ei.gen_Y1 && moth_idx == ei.gen_Y1->getIdx())
            assign_to_uninit(gp, {&ei.gen_H1Y1, &ei.gen_H2Y1});
          if (ei.gen_Y2 && moth_idx == ei.gen_Y2->getIdx())
            assign_to_uninit(gp, {&ei.gen_H1Y2, &ei.gen_H2Y2});
        }
      }
    }

    // b
    if (apdgid == 5 && gp.isFirstCopy())
    {
      int moth_idx = get_property(gp, GenPart_genPartIdxMother);
      if (moth_idx >= 0)
      {
        GenPart mother(moth_idx, &nat);
        int amothpdgid = abs(get_property(mother, GenPart_pdgId));
        // in the LHE the mother always comes before the daughters, so it is guaranteed to have been found already
        if (amothpdgid == 25)
        {
          if (ei.gen_H1Y1 && moth_idx == ei.gen_H1Y1->getIdx())
            assign_to_uninit(gp, {&ei.gen_H1Y1_b1, &ei.gen_H1Y1_b2});
            
          if (ei.gen_H2Y1 && moth_idx == ei.gen_H2Y1->getIdx())
            assign_to_uninit(gp, {&ei.gen_H2Y1_b1, &ei.gen_H2Y1_b2});

          if (ei.gen_H1Y2 && moth_idx == ei.gen_H1Y2->getIdx())
            assign_to_uninit(gp, {&ei.gen_H1Y2_b1, &ei.gen_H1Y2_b2});
            
          if (ei.gen_H2Y2 && moth_idx == ei.gen_H2Y2->getIdx())
            assign_to_uninit(gp, {&ei.gen_H2Y2_b1, &ei.gen_H2Y2_b2});
        }
      }
    }
  }

    // reorder objects according to pt
  if (ei.gen_Y1->P4().Pt() < ei.gen_Y2->P4().Pt()) 
  {
    std::swap(ei.gen_Y1, ei.gen_Y2);
    std::swap(ei.gen_H1Y1, ei.gen_H1Y2);
    std::swap(ei.gen_H2Y1, ei.gen_H2Y2);

    std::swap(ei.gen_H1Y1_b1, ei.gen_H1Y2_b1);
    std::swap(ei.gen_H1Y1_b2, ei.gen_H1Y2_b2);
    std::swap(ei.gen_H2Y1_b1, ei.gen_H2Y2_b1);
    std::swap(ei.gen_H2Y1_b2, ei.gen_H2Y2_b2);
  }

  if (ei.gen_H1Y1->P4().Pt() < ei.gen_H2Y1->P4().Pt())
  {
    std::swap(ei.gen_H1Y1, ei.gen_H2Y1);
    std::swap(ei.gen_H1Y1_b1, ei.gen_H2Y1_b1);
    std::swap(ei.gen_H1Y1_b2, ei.gen_H2Y1_b2);
  }

  if (ei.gen_H1Y2->P4().Pt() < ei.gen_H2Y2->P4().Pt())
  {
    std::swap(ei.gen_H1Y2, ei.gen_H2Y2);
    std::swap(ei.gen_H1Y2_b1, ei.gen_H2Y2_b1);
    std::swap(ei.gen_H1Y2_b2, ei.gen_H2Y2_b2);
  }

  if (ei.gen_H1Y1_b1->P4().Pt() < ei.gen_H1Y1_b2->P4().Pt())
    std::swap(ei.gen_H1Y1_b1, ei.gen_H1Y1_b2);
  if (ei.gen_H2Y1_b1->P4().Pt() < ei.gen_H2Y1_b2->P4().Pt())
    std::swap(ei.gen_H2Y1_b1, ei.gen_H2Y1_b2);
  if (ei.gen_H1Y2_b1->P4().Pt() < ei.gen_H1Y2_b2->P4().Pt())
    std::swap(ei.gen_H1Y2_b1, ei.gen_H1Y2_b2);
  if (ei.gen_H2Y2_b1->P4().Pt() < ei.gen_H2Y2_b2->P4().Pt())
    std::swap(ei.gen_H2Y2_b1, ei.gen_H2Y2_b2);

  return;
}

// match the selected gen b to gen jets
void EightB_functions::match_genbs_to_genjets(NanoAODTree& nat, EventInfo& ei, bool ensure_unique)
{
  const double dR_match = 0.4;

  std::vector<GenPart *> bs_to_match = {
      ei.gen_H1Y1_b1.get_ptr(),
      ei.gen_H1Y1_b2.get_ptr(),

      ei.gen_H2Y1_b1.get_ptr(),
      ei.gen_H2Y1_b2.get_ptr(),

      ei.gen_H1Y2_b1.get_ptr(),
      ei.gen_H1Y2_b2.get_ptr(),

      ei.gen_H2Y2_b1.get_ptr(),
      ei.gen_H2Y2_b2.get_ptr()};

  
  std::vector<GenJet> genjets;
  for (unsigned int igj = 0; igj < *(nat.nGenJet); ++igj)
    {
      GenJet gj (igj, &nat);
      genjets.push_back(gj);
    }

  std::vector<GenPart*> matched_quarks;
  std::vector<GenJet> matched_genjets;
  GetMatchedPairs(dR_match, bs_to_match, genjets, matched_quarks, matched_genjets);

  for (unsigned int im=0; im<matched_quarks.size(); im++)
  {
    GenPart* b = matched_quarks.at(im);
    GenJet   j = matched_genjets.at(im);

    int bIdx = b->getIdx();
    if (bIdx == ei.gen_H1Y1_b1.get_ptr()->getIdx())
      ei.gen_H1Y1_b1_genjet = GenJet(j.getIdx(), &nat);
    if (bIdx == ei.gen_H1Y1_b2.get_ptr()->getIdx())
      ei.gen_H1Y1_b2_genjet = GenJet(j.getIdx(), &nat);

    if (bIdx == ei.gen_H2Y1_b1.get_ptr()->getIdx())
      ei.gen_H2Y1_b1_genjet = GenJet(j.getIdx(), &nat);
    if (bIdx == ei.gen_H2Y1_b2.get_ptr()->getIdx())
      ei.gen_H2Y1_b2_genjet = GenJet(j.getIdx(), &nat);

    if (bIdx == ei.gen_H1Y2_b1.get_ptr()->getIdx())
      ei.gen_H1Y2_b1_genjet = GenJet(j.getIdx(), &nat);
    if (bIdx == ei.gen_H1Y2_b2.get_ptr()->getIdx())
      ei.gen_H1Y2_b2_genjet = GenJet(j.getIdx(), &nat);

    if (bIdx == ei.gen_H2Y2_b1.get_ptr()->getIdx())
      ei.gen_H2Y2_b1_genjet = GenJet(j.getIdx(), &nat);
    if (bIdx == ei.gen_H2Y2_b2.get_ptr()->getIdx())
      ei.gen_H2Y2_b2_genjet = GenJet(j.getIdx(), &nat);
  }

  return;
}

void EightB_functions::match_genbs_genjets_to_reco(NanoAODTree& nat, EventInfo& ei)
{
  int ij_gen_H1Y1_b1_genjet  = (ei.gen_H1Y1_b1_genjet  ? find_jet_from_genjet(nat, *ei.gen_H1Y1_b1_genjet)  : -1); 
  int ij_gen_H1Y1_b2_genjet  = (ei.gen_H1Y1_b2_genjet  ? find_jet_from_genjet(nat, *ei.gen_H1Y1_b2_genjet)  : -1); 
  int ij_gen_H2Y1_b1_genjet  = (ei.gen_H2Y1_b1_genjet  ? find_jet_from_genjet(nat, *ei.gen_H2Y1_b1_genjet)  : -1); 
  int ij_gen_H2Y1_b2_genjet  = (ei.gen_H2Y1_b2_genjet  ? find_jet_from_genjet(nat, *ei.gen_H2Y1_b2_genjet)  : -1); 
  int ij_gen_H1Y2_b1_genjet  = (ei.gen_H1Y2_b1_genjet  ? find_jet_from_genjet(nat, *ei.gen_H1Y2_b1_genjet)  : -1); 
  int ij_gen_H1Y2_b2_genjet  = (ei.gen_H1Y2_b2_genjet  ? find_jet_from_genjet(nat, *ei.gen_H1Y2_b2_genjet)  : -1); 
  int ij_gen_H2Y2_b1_genjet  = (ei.gen_H2Y2_b1_genjet  ? find_jet_from_genjet(nat, *ei.gen_H2Y2_b1_genjet)  : -1); 
  int ij_gen_H2Y2_b2_genjet  = (ei.gen_H2Y2_b2_genjet  ? find_jet_from_genjet(nat, *ei.gen_H2Y2_b2_genjet)  : -1); 

  if (ij_gen_H1Y1_b1_genjet >= 0)  ei.gen_H1Y1_b1_recojet  = Jet(ij_gen_H1Y1_b1_genjet,  &nat);
  if (ij_gen_H1Y1_b2_genjet >= 0)  ei.gen_H1Y1_b2_recojet  = Jet(ij_gen_H1Y1_b2_genjet,  &nat);
  if (ij_gen_H2Y1_b1_genjet >= 0)  ei.gen_H2Y1_b1_recojet  = Jet(ij_gen_H2Y1_b1_genjet,  &nat);
  if (ij_gen_H2Y1_b2_genjet >= 0)  ei.gen_H2Y1_b2_recojet  = Jet(ij_gen_H2Y1_b2_genjet,  &nat);
  
  if (ij_gen_H1Y2_b1_genjet >= 0)  ei.gen_H1Y2_b1_recojet  = Jet(ij_gen_H1Y2_b1_genjet,  &nat);
  if (ij_gen_H1Y2_b2_genjet >= 0)  ei.gen_H1Y2_b2_recojet  = Jet(ij_gen_H1Y2_b2_genjet,  &nat);
  if (ij_gen_H2Y2_b1_genjet >= 0)  ei.gen_H2Y2_b1_recojet  = Jet(ij_gen_H2Y2_b1_genjet,  &nat);
  if (ij_gen_H2Y2_b2_genjet >= 0)  ei.gen_H2Y2_b2_recojet  = Jet(ij_gen_H2Y2_b2_genjet,  &nat);

  // select unique occurences in vector
  // note : PAT tools already ensure that match is unique
  // https://github.com/cms-sw/cmssw/blob/master/PhysicsTools/PatAlgos/python/mcMatchLayer0/jetMatch_cfi.py
  // so the check below is redundant

  // std::vector<int> imatchs;
  // if (ij_gen_H1Y1_b1_genjet >= 0)  imatchs.push_back(ij_gen_H1Y1_b1_genjet);
  // if (ij_gen_H1Y1_b2_genjet >= 0)  imatchs.push_back(ij_gen_H1Y1_b2_genjet);
  // if (ij_gen_HY1_b1_genjet >= 0) imatchs.push_back(ij_gen_HY1_b1_genjet);
  // if (ij_gen_HY1_b2_genjet >= 0) imatchs.push_back(ij_gen_HY1_b2_genjet);
  // if (ij_gen_HY2_b1_genjet >= 0) imatchs.push_back(ij_gen_HY2_b1_genjet);
  // if (ij_gen_HY2_b2_genjet >= 0) imatchs.push_back(ij_gen_HY2_b2_genjet);

  // sort(imatchs.begin(), imatchs.end());
  // imatchs.erase(unique (imatchs.begin(), imatchs.end()), imatchs.end());
  // ei.gen_bs_N_reco_match = imatchs.size(); // number of different reco jets that are matched to gen jets

  int nmatched = 0;
  if (ij_gen_H1Y1_b1_genjet >= 0)  nmatched += 1;
  if (ij_gen_H1Y1_b2_genjet >= 0)  nmatched += 1;
  if (ij_gen_H2Y1_b1_genjet >= 0)  nmatched += 1;
  if (ij_gen_H2Y1_b2_genjet >= 0)  nmatched += 1;
  if (ij_gen_H1Y2_b1_genjet >= 0)  nmatched += 1;
  if (ij_gen_H1Y2_b2_genjet >= 0)  nmatched += 1;
  if (ij_gen_H2Y2_b1_genjet >= 0)  nmatched += 1;
  if (ij_gen_H2Y2_b2_genjet >= 0)  nmatched += 1;
  ei.gen_bs_N_reco_match = nmatched;

  // same as above, but apply acceptance cuts on the matched jets
  int nmatched_acc = 0;
  if (ei.gen_H1Y1_b1_recojet  && ei.gen_H1Y1_b1_recojet->P4().Pt()  > 20 && std::abs(ei.gen_H1Y1_b1_recojet->P4().Eta())  < 4.8) nmatched_acc += 1;
  if (ei.gen_H1Y1_b2_recojet  && ei.gen_H1Y1_b2_recojet->P4().Pt()  > 20 && std::abs(ei.gen_H1Y1_b2_recojet->P4().Eta())  < 4.8) nmatched_acc += 1;
  if (ei.gen_H2Y1_b1_recojet  && ei.gen_H2Y1_b1_recojet->P4().Pt()  > 20 && std::abs(ei.gen_H2Y1_b1_recojet->P4().Eta())  < 4.8) nmatched_acc += 1;
  if (ei.gen_H2Y1_b2_recojet  && ei.gen_H2Y1_b2_recojet->P4().Pt()  > 20 && std::abs(ei.gen_H2Y1_b2_recojet->P4().Eta())  < 4.8) nmatched_acc += 1;
  if (ei.gen_H1Y2_b1_recojet  && ei.gen_H1Y2_b1_recojet->P4().Pt()  > 20 && std::abs(ei.gen_H1Y2_b1_recojet->P4().Eta())  < 4.8) nmatched_acc += 1;
  if (ei.gen_H1Y2_b2_recojet  && ei.gen_H1Y2_b2_recojet->P4().Pt()  > 20 && std::abs(ei.gen_H1Y2_b2_recojet->P4().Eta())  < 4.8) nmatched_acc += 1;
  if (ei.gen_H2Y2_b1_recojet  && ei.gen_H2Y2_b1_recojet->P4().Pt()  > 20 && std::abs(ei.gen_H2Y2_b1_recojet->P4().Eta())  < 4.8) nmatched_acc += 1;
  if (ei.gen_H2Y2_b2_recojet  && ei.gen_H2Y2_b2_recojet->P4().Pt()  > 20 && std::abs(ei.gen_H2Y2_b2_recojet->P4().Eta())  < 4.8) nmatched_acc += 1;
  ei.gen_bs_N_reco_match_in_acc = nmatched_acc;

  // now compute p4 sums to make the invariant mass of X - FIXME: can add more inv masses for the various cases
  p4_t p4_sum_matched (0,0,0,0);
  if (ei.gen_H1Y1_b1_recojet) p4_sum_matched  += ei.gen_H1Y1_b1_recojet->P4();
  if (ei.gen_H1Y1_b2_recojet) p4_sum_matched  += ei.gen_H1Y1_b2_recojet->P4();
  if (ei.gen_H2Y1_b1_recojet) p4_sum_matched  += ei.gen_H2Y1_b1_recojet->P4();
  if (ei.gen_H2Y1_b2_recojet) p4_sum_matched  += ei.gen_H2Y1_b2_recojet->P4();
  if (ei.gen_H1Y2_b1_recojet) p4_sum_matched  += ei.gen_H1Y2_b1_recojet->P4();
  if (ei.gen_H1Y2_b2_recojet) p4_sum_matched  += ei.gen_H1Y2_b2_recojet->P4();
  if (ei.gen_H2Y2_b1_recojet) p4_sum_matched  += ei.gen_H2Y2_b1_recojet->P4();
  if (ei.gen_H2Y2_b2_recojet) p4_sum_matched  += ei.gen_H2Y2_b2_recojet->P4();
  ei.gen_bs_match_recojet_minv = p4_sum_matched.M();

  p4_t p4_sum_matched_acc (0,0,0,0);
  if (ei.gen_H1Y1_b1_recojet  && ei.gen_H1Y1_b1_recojet->P4().Pt()  > 20 && std::abs(ei.gen_H1Y1_b1_recojet->P4().Eta())  < 4.8) p4_sum_matched_acc += ei.gen_H1Y1_b1_recojet->P4();
  if (ei.gen_H1Y1_b2_recojet  && ei.gen_H1Y1_b2_recojet->P4().Pt()  > 20 && std::abs(ei.gen_H1Y1_b2_recojet->P4().Eta())  < 4.8) p4_sum_matched_acc += ei.gen_H1Y1_b2_recojet->P4();
  if (ei.gen_H2Y1_b1_recojet  && ei.gen_H2Y1_b1_recojet->P4().Pt()  > 20 && std::abs(ei.gen_H2Y1_b1_recojet->P4().Eta())  < 4.8) p4_sum_matched_acc += ei.gen_H2Y1_b1_recojet->P4();
  if (ei.gen_H2Y1_b2_recojet  && ei.gen_H2Y1_b2_recojet->P4().Pt()  > 20 && std::abs(ei.gen_H2Y1_b2_recojet->P4().Eta())  < 4.8) p4_sum_matched_acc += ei.gen_H2Y1_b2_recojet->P4();
  if (ei.gen_H1Y2_b1_recojet  && ei.gen_H1Y2_b1_recojet->P4().Pt()  > 20 && std::abs(ei.gen_H1Y2_b1_recojet->P4().Eta())  < 4.8) p4_sum_matched_acc += ei.gen_H1Y2_b1_recojet->P4();
  if (ei.gen_H1Y2_b2_recojet  && ei.gen_H1Y2_b2_recojet->P4().Pt()  > 20 && std::abs(ei.gen_H1Y2_b2_recojet->P4().Eta())  < 4.8) p4_sum_matched_acc += ei.gen_H1Y2_b2_recojet->P4();
  if (ei.gen_H2Y2_b1_recojet  && ei.gen_H2Y2_b1_recojet->P4().Pt()  > 20 && std::abs(ei.gen_H2Y2_b1_recojet->P4().Eta())  < 4.8) p4_sum_matched_acc += ei.gen_H2Y2_b1_recojet->P4();
  if (ei.gen_H2Y2_b2_recojet  && ei.gen_H2Y2_b2_recojet->P4().Pt()  > 20 && std::abs(ei.gen_H2Y2_b2_recojet->P4().Eta())  < 4.8) p4_sum_matched_acc += ei.gen_H2Y2_b2_recojet->P4();
  ei.gen_bs_match_in_acc_recojet_minv = p4_sum_matched_acc.M();
}

int EightB_functions::get_jet_genmatch_flag (NanoAODTree& nat, EventInfo& ei, const Jet& jet)
{
    int ijet = jet.getIdx();
    // if ( (ei.gen_H1Y1_b1_recojet && ijet == ei.gen_H1Y1_b1_recojet->getIdx())   || (ei.gen_H1Y1_b2_recojet && ijet == ei.gen_H1Y1_b2_recojet->getIdx()) )
    //     return 0; 
    // if ( (ei.gen_H2Y1_b1_recojet && ijet == ei.gen_H2Y1_b1_recojet->getIdx())   || (ei.gen_H2Y1_b2_recojet && ijet == ei.gen_H2Y1_b2_recojet->getIdx()) )
    //     return 1; 
    // if ( (ei.gen_H1Y2_b1_recojet && ijet == ei.gen_H1Y2_b1_recojet->getIdx())   || (ei.gen_H1Y2_b2_recojet && ijet == ei.gen_H1Y2_b2_recojet->getIdx()) )
    //     return 2; 
    // if ( (ei.gen_H2Y2_b1_recojet && ijet == ei.gen_H2Y2_b1_recojet->getIdx())   || (ei.gen_H2Y2_b2_recojet && ijet == ei.gen_H2Y2_b2_recojet->getIdx()) )
    //     return 3; 

    if ((ei.gen_H1Y1_b1_recojet && ijet == ei.gen_H1Y1_b1_recojet->getIdx()))
      return 0;
    if ((ei.gen_H1Y1_b2_recojet && ijet == ei.gen_H1Y1_b2_recojet->getIdx()))
      return 1;
    if ((ei.gen_H2Y1_b1_recojet && ijet == ei.gen_H2Y1_b1_recojet->getIdx()))
      return 2;
    if ((ei.gen_H2Y1_b2_recojet && ijet == ei.gen_H2Y1_b2_recojet->getIdx()))
      return 3;
    if ((ei.gen_H1Y2_b1_recojet && ijet == ei.gen_H1Y2_b1_recojet->getIdx()))
      return 4;
    if ((ei.gen_H1Y2_b2_recojet && ijet == ei.gen_H1Y2_b2_recojet->getIdx()))
      return 5;
    if ((ei.gen_H2Y2_b1_recojet && ijet == ei.gen_H2Y2_b1_recojet->getIdx()))
      return 6;
    if ((ei.gen_H2Y2_b2_recojet && ijet == ei.gen_H2Y2_b2_recojet->getIdx()))
      return 7;

    return -1;
}

void EightB_functions::compute_seljets_genmatch_flags(NanoAODTree& nat, EventInfo& ei)
{
    // flags per jet
    ei.H1Y1_b1_genHflag  = get_jet_genmatch_flag(nat, ei, *ei.H1Y1_b1);
    ei.H1Y1_b2_genHflag  = get_jet_genmatch_flag(nat, ei, *ei.H1Y1_b2);
    ei.H2Y1_b1_genHflag  = get_jet_genmatch_flag(nat, ei, *ei.H2Y1_b1);
    ei.H2Y1_b2_genHflag  = get_jet_genmatch_flag(nat, ei, *ei.H2Y1_b2);
    ei.H1Y2_b1_genHflag  = get_jet_genmatch_flag(nat, ei, *ei.H1Y2_b1);
    ei.H1Y2_b2_genHflag  = get_jet_genmatch_flag(nat, ei, *ei.H1Y2_b2);
    ei.H2Y2_b1_genHflag  = get_jet_genmatch_flag(nat, ei, *ei.H2Y2_b1);
    ei.H2Y2_b2_genHflag  = get_jet_genmatch_flag(nat, ei, *ei.H2Y2_b2);

    vector<int> flags = {ei.H1Y1_b1_genHflag.get(),
                         ei.H1Y1_b2_genHflag.get(),
                         ei.H2Y1_b1_genHflag.get(),
                         ei.H2Y1_b2_genHflag.get(),
                         ei.H1Y2_b1_genHflag.get(),
                         ei.H1Y2_b2_genHflag.get(),
                         ei.H2Y2_b1_genHflag.get(),
                         ei.H2Y2_b2_genHflag.get()};

    // flags per event
    int nfound_select = 0;
    int nfound_select_h = 0;
    int nfound_paired_h = 0;

    int nfound_select_y = 0;
    int nfound_paired_y = 0;

    for (int i = 0; i < 8; i++) {
      if (flags[i] > -1) {
        nfound_select++;
        for (int j = i + 1; j < 8; j++) {
          if ( (flags[i]+2)/2 == (flags[j]+2)/2 ) {
            nfound_select_h++;

            if (i == 0 || i == 2 || i == 4 || i == 6)
              nfound_paired_h += (j - i < 2);
          }
          
          if ( (flags[i]+4)/4 == (flags[j]+4)/4 ) {
            nfound_select_y++;

            if (i == 0 || i == 4)
              nfound_paired_y += (j - i < 4);
          }
        }
      }
    }

    //   if (ei.H1Y1_b1_genHflag > -1 && ei.H1Y1_b1_genHflag == ei.H1Y1_b2_genHflag)
    //     nfound_paired_h += 1;
    // if (ei.H2Y1_b1_genHflag > -1 && ei.H2Y1_b1_genHflag == ei.H2Y1_b2_genHflag)  nfound_paired_h += 1;
    // if (ei.H1Y2_b1_genHflag > -1 && ei.H1Y2_b1_genHflag == ei.H1Y2_b2_genHflag)  nfound_paired_h += 1;
    // if (ei.H2Y2_b1_genHflag > -1 && ei.H2Y2_b1_genHflag == ei.H2Y2_b2_genHflag)  nfound_paired_h += 1;

    ei.nfound_select = nfound_select;
    ei.nfound_select_h = nfound_select_h;
    ei.nfound_paired_h = nfound_paired_h;  // number of selected jets that are from H
    ei.nfound_select_y = nfound_select_y/6;
    ei.nfound_paired_y = nfound_paired_y/3;
}

void EightB_functions::compute_seljets_btagmulti(NanoAODTree& nat, EventInfo& ei)
{
    // btag per jet

    vector<float> btags = {ei.H1Y1_b1.get().get_btag(),
                         ei.H1Y1_b2.get().get_btag(),
                         ei.H2Y1_b1.get().get_btag(),
                         ei.H2Y1_b2.get().get_btag(),
                         ei.H1Y2_b1.get().get_btag(),
                         ei.H1Y2_b2.get().get_btag(),
                         ei.H2Y2_b1.get().get_btag(),
                         ei.H2Y2_b2.get().get_btag()};

    vector<int> btagmulti = {0, 0, 0};
    float btagsum = 0.0;

    for (float btag : btags) {
      btagsum += btag;
      for (unsigned int i = 0; i < btag_WPs.size(); i++) {
        if (btag > btag_WPs[i]) {
          btagmulti[i]++;
        }
      }
    }
    btagsum /= (float)btags.size();

    ei.btagavg = btagsum;
    ei.n_loose_btag = btagmulti[0];
    ei.n_medium_btag = btagmulti[1];
    ei.n_tight_btag = btagmulti[2];
}

////////////////////////////////////////////////////////////////////
////////////////////// EightB jet selections//////////////////////////
////////////////////////////////////////////////////////////////////

std::vector<Jet> EightB_functions::select_jets(NanoAODTree& nat, EventInfo& ei, const std::vector<Jet>& in_jets)
{
  std::string sel_type = pmap.get_param<std::string>("configurations", "eightbJetChoice");
  
  if (sel_type == "maxbtag")
    return select_eightb_jets_maxbtag(nat, ei, in_jets);

  if (sel_type == "gnn_jet")
    return select_eightb_jets_gnn(nat, ei, in_jets);

  if (sel_type == "none")
  {
    vector<Jet> jets = in_jets;
    return jets;
  }

  else
    throw std::runtime_error(std::string("EightB_functions::select_jets : eightbJetChoice ") + sel_type + std::string("not understood"));
}


std::vector<Jet> EightB_functions::select_eightb_jets_maxbtag(NanoAODTree& nat, EventInfo& ei, const std::vector<Jet>& in_jets)
{
    std::vector<Jet> jets = btag_sort_jets(nat,ei,in_jets);

    int n_out = std::min<int>(jets.size(), 8);
    jets.resize(n_out);



    // for (auto& jet : jets)
    //     std::cout << jet.P4().Pt() << " " << get_property (jet, Jet_btagDeepFlavB) << std::endl;
    // std::cout << std::endl << std::endl;
    return pt_sort_jets(nat, ei, jets);
}

std::vector<Jet> EightB_functions::select_eightb_jets_gnn(NanoAODTree& nat,
                                                          EventInfo& ei,
                                                          const std::vector<Jet>& in_jets) {
  vector<Jet> jets = pt_sort_jets(nat, ei, in_jets);
  vector<DiJet> dijets = make_dijets(nat, ei, jets);

  map<string, vector<float>> features = buildClassifierInput::build_gnn_classifier_input(jets, dijets);

  vector<float> jet_pred = onnx_classifier_->evaluate(features);
  jet_pred.resize(jets.size());

  for (unsigned int i = 0 ; i < jets.size(); i++)
  {
    jets[i].set_param("score", jet_pred[i]);
  }

  ei.jet_list = jets;

  std::sort(jets.begin(), jets.end(), [](Jet& j1, Jet& j2) {
    return j1.get_param("score", 0) > j2.get_param("score", 0); });
    
  int n_out = std::min<int>(jets.size(), 8);
  jets.resize(n_out);

  return jets;
}

void EightB_functions::pair_jets(NanoAODTree& nat, EventInfo& ei, const std::vector<Jet>& in_jets)
{
    //TODO implement D_HHHH method
  // H4_tuple reco_Hs;
  // std::string pairAlgo = pmap.get_param<std::string>("configurations", "jetPairsChoice");

  // if (debug_) loop_timer->click("Pairing Jets");
  // if (pairAlgo == "passthrough")
  //   reco_Hs = pair_4H_passthrough(nat, ei, in_jets);
  // if (pairAlgo == "min_mass_spread")
  //   reco_Hs = pair_4H_min_mass_spread(nat, ei, in_jets);
  // if (pairAlgo == "gnn_dijet")
  //   reco_Hs = pair_4H_gnn(nat, ei, in_jets);

  // if (debug_) loop_timer->click("Pairing Higgs");
  // YY_tuple reco_YYs;
  // std::string YYAlgo = pmap.get_param<std::string>("configurations", "YYChoice");
  // if (YYAlgo == "passthrough")
  //   reco_YYs = pair_YY_passthrough(nat, ei, reco_Hs);
  // if (YYAlgo == "min_mass_spread")
  //   reco_YYs = pair_YY_min_mass_spread(nat, ei, reco_Hs);

    bool pair4Hfirst = pmap.get_param<bool>("configurations", "pair4Hfirst");

    YY_tuple reco_YYs;

    if (pair4Hfirst)
        reco_YYs = pair_4H_2Y(nat, ei, in_jets);
    else
        reco_YYs = pair_2Y_4H(nat, ei, in_jets);

    if (debug_)
      loop_timer->click("Reordering Resonances");

    CompositeCandidate& H1Y1 = static_cast<CompositeCandidate&>(std::get<0>(reco_YYs).getComponent1());
    CompositeCandidate& H2Y1 = static_cast<CompositeCandidate&>(std::get<0>(reco_YYs).getComponent2());
    CompositeCandidate& H1Y2 = static_cast<CompositeCandidate&>(std::get<1>(reco_YYs).getComponent1());
    CompositeCandidate& H2Y2 = static_cast<CompositeCandidate&>(std::get<1>(reco_YYs).getComponent2());

    // rebuild p4 with regressed pT if required
    if (pmap.get_param<bool>("configurations", "useRegressedPtForHp4")) {
      H1Y1.rebuildP4UsingRegressedPt(true, true);
      H2Y1.rebuildP4UsingRegressedPt(true, true);
      H1Y2.rebuildP4UsingRegressedPt(true, true);
      H2Y2.rebuildP4UsingRegressedPt(true, true);
  }

  if (H1Y1.getComponent1().P4().Pt() < H1Y1.getComponent2().P4().Pt())
    H1Y1.swapComponents();

  if (H2Y1.getComponent1().P4().Pt() < H2Y1.getComponent2().P4().Pt())
    H2Y1.swapComponents();

  if (H1Y2.getComponent1().P4().Pt() < H1Y2.getComponent2().P4().Pt())
    H1Y2.swapComponents();

  if (H2Y2.getComponent1().P4().Pt() < H2Y2.getComponent2().P4().Pt())
    H2Y2.swapComponents();

  if (H1Y1.P4().Pt() < H2Y1.P4().Pt())
    std::swap(H1Y1, H2Y1);

  if (H1Y2.P4().Pt() < H2Y2.P4().Pt())
    std::swap(H1Y2, H2Y2);

  CompositeCandidate Y1(H1Y1, H2Y1);
  CompositeCandidate Y2(H1Y2, H2Y2);

  if (Y1.P4().Pt() < Y2.P4().Pt())
    std::swap(Y1, Y2);

  CompositeCandidate X(Y1, Y2);

  ei.X = X;
  ei.Y1= Y1;
  ei.Y2= Y2;

  ei.H1Y1 = H1Y1;
  ei.H2Y1 = H2Y1;
  ei.H1Y2 = H1Y2;
  ei.H2Y2 = H2Y2;

  ei.H1Y1_b1  = static_cast<Jet&>(H1Y1.getComponent1());
  ei.H1Y1_b2  = static_cast<Jet&>(H1Y1.getComponent2());
  ei.H2Y1_b1  = static_cast<Jet&>(H2Y1.getComponent1());
  ei.H2Y1_b2  = static_cast<Jet&>(H2Y1.getComponent2());
  ei.H1Y2_b1  = static_cast<Jet&>(H1Y2.getComponent1());
  ei.H1Y2_b2  = static_cast<Jet&>(H1Y2.getComponent2());
  ei.H2Y2_b1  = static_cast<Jet&>(H2Y2.getComponent1());
  ei.H2Y2_b2  = static_cast<Jet&>(H2Y2.getComponent2());

  if (debug_) 
  {
    vector<Jet> selected_jets = {
        ei.H1Y1_b1.get(),
        ei.H1Y1_b2.get(),
        ei.H2Y1_b1.get(),
        ei.H2Y1_b2.get(),
        ei.H1Y2_b1.get(),
        ei.H1Y2_b2.get(),
        ei.H2Y2_b1.get(),
        ei.H2Y2_b2.get(),
    };
    dumpObjColl(selected_jets, "==== SELECTED JETS ====");

    vector<CompositeCandidate> selected_higgs = {
        ei.H1Y1.get(),
        ei.H2Y1.get(),
        ei.H1Y2.get(),
        ei.H2Y2.get(),
    };
    dumpObjColl(selected_higgs, "==== PAIRED HIGGS ====");

    vector<CompositeCandidate> selected_y = {
      ei.Y1.get(),
      ei.Y2.get(),
    };
    dumpObjColl(selected_y, "==== PAIRED Y ====");
  }
}


YY_tuple EightB_functions::pair_4H_2Y(NanoAODTree &nat, EventInfo &ei, const std::vector<Jet> &in_jets)
{
  if (debug_) loop_timer->click("Pairing Jets");

  H4_tuple reco_Hs;
  std::string pairAlgo = pmap.get_param<std::string>("configurations", "jetPairsChoice");
  if (pairAlgo == "passthrough")
    reco_Hs = pair_4H_passthrough(nat, ei, in_jets);
  if (pairAlgo == "min_mass_spread")
    reco_Hs = pair_4H_min_mass_spread(nat, ei, in_jets);
  if (pairAlgo == "gnn_dijet")
    reco_Hs = pair_4H_gnn(nat, ei, in_jets);

  if (debug_) loop_timer->click("Pairing Higgs");

  YY_tuple reco_YYs;
  std::string YYAlgo = pmap.get_param<std::string>("configurations", "YYChoice");
  if (YYAlgo == "passthrough")
    reco_YYs = pair_YY_passthrough(nat, ei, reco_Hs);
  if (YYAlgo == "min_mass_spread")
    reco_YYs = pair_YY_min_mass_spread(nat, ei, reco_Hs);

  return reco_YYs;
}

H4_tuple EightB_functions::pair_4H_passthrough (NanoAODTree &nat, EventInfo& ei, const std::vector<Jet>& jets)
{
  if (jets.size() != 8)
    throw std::runtime_error("The jet pairing -passthrough- function requires 8 jets");

  CompositeCandidate H1Y1  (jets.at(0), jets.at(1));
  CompositeCandidate H2Y1 (jets.at(2), jets.at(3));
  CompositeCandidate H1Y2 (jets.at(4), jets.at(5));
  CompositeCandidate H2Y2 (jets.at(6), jets.at(7));

  return std::make_tuple(H1Y1, H2Y1, H1Y2,H2Y2);
}

H4_tuple EightB_functions::pair_4H_min_mass_spread(NanoAODTree &nat, EventInfo &ei, const std::vector<Jet> &jets)
{
  if (jets.size() != 8)
    throw std::runtime_error("The jet pairing -passthrough- function requires 8 jets");

  if (debug_) loop_timer->click("Dijet Min Mass Spread Pairing");

  // 8 jets grouped into 4 groups of 2
  if (quadH_jet_groups.size() == 0)
  {
    vector<int> groups = {2, 2, 2, 2};
    quadH_jet_groups = combinations(8, groups);
  }

  map<int, CompositeCandidate> dijetMap;
  std::hash<std::string> str_hash;
  auto pair_hash = [str_hash](vector<int> pair) { return str_hash(to_string(pair[0]) + to_string(pair[1])); };

  vector<float> m_asyms;
  for (vector<vector<int>> group : quadH_jet_groups) {
    vector<float> group_m;
    for (vector<int> pair : group) {
      int hash = pair_hash(pair);
      if ( dijetMap.count(hash) == 0 )
      {
        dijetMap[hash] = CompositeCandidate(jets.at(pair[0]), jets.at(pair[1]));
        dijetMap[hash].rebuildP4UsingRegressedPt(true, true);
      }
      group_m.push_back(dijetMap[hash].P4().M());
    }
    std::sort(group_m.begin(), group_m.end(), [](float m1, float m2) { return m1 < m2; });
    float m_asym = (group_m[3] - group_m[0]) / (group_m[3] + group_m[0]);
    // float m_asym = (group_m[3] - group_m[0]);
    m_asyms.push_back(m_asym);
  }
  int argmin = std::distance(m_asyms.begin(), std::min_element(m_asyms.begin(), m_asyms.end()));
  vector<vector<int>> best_group = quadH_jet_groups[argmin];

  CompositeCandidate H1Y1 = dijetMap[pair_hash(best_group[0])];
  CompositeCandidate H2Y1 = dijetMap[pair_hash(best_group[1])];
  CompositeCandidate H1Y2 = dijetMap[pair_hash(best_group[2])];
  CompositeCandidate H2Y2 = dijetMap[pair_hash(best_group[3])];

  // vector<vector<int>> dijet_pairings = combinations(8, 2);
  // std::vector<CompositeCandidate> dijets(dijet_pairings.size());
  // std::vector<float> dijet_m(dijet_pairings.size());
  // for (unsigned int i = 0; i < dijet_pairings.size(); i++)
  // {
  //   int j0 = dijet_pairings[i][0];
  //   int j1 = dijet_pairings[i][1];
  //   dijets[i] = CompositeCandidate(jets.at(j0), jets.at(j1));
  //   dijets[i].rebuildP4UsingRegressedPt(true, true);
  //   dijet_m[i] = dijets[i].P4().M();
  // }

  // std::vector<int> min_quadH_pair(4);
  // float min_mass_spread = std::numeric_limits<float>::max();
  // for (unsigned int i = 0; i < quadH_pairings.size(); i++)
  // {
  //   std::vector<int> quadH_pair = quadH_pairings[i];
  //   std::sort(quadH_pair.begin(), quadH_pair.end(), [dijet_m](int &h1, int &h2)
  //             { return dijet_m[h1] > dijet_m[h2]; });
  //   float mass_spread = fabs(dijet_m[quadH_pair[0]] - dijet_m[quadH_pair[3]]);
  //   if (mass_spread < min_mass_spread)
  //   {
  //     min_quadH_pair = quadH_pair;
  //     min_mass_spread = mass_spread;
  //   }
  // }

  // CompositeCandidate H1Y1 = dijets[min_quadH_pair[0]];
  // CompositeCandidate H2Y1 = dijets[min_quadH_pair[1]];
  // CompositeCandidate H1Y2 = dijets[min_quadH_pair[2]];
  // CompositeCandidate H2Y2 = dijets[min_quadH_pair[3]];

  return std::make_tuple(H1Y1, H2Y1, H1Y2, H2Y2);
}


H4_tuple EightB_functions::pair_4H_gnn (NanoAODTree &nat, EventInfo& ei, const std::vector<Jet>& in_jets)
{
  // std::string gnn_output = pmap.get_param<std::string>("GNN", "output");
  string gnn_output = "quadh";
  if (gnn_output == "quadh")
    return pair_4H_gnn_quadh(nat, ei, in_jets);
  return pair_4H_gnn_dijet(nat, ei, in_jets);
}

H4_tuple EightB_functions::pair_4H_gnn_dijet (NanoAODTree &nat, EventInfo& ei, const std::vector<Jet>& in_jets)
{
  vector<Jet> jets = in_jets;
  vector<DiJet> dijets = make_dijets(nat, ei, in_jets);
  map<string, vector<float>> features = buildClassifierInput::build_gnn_classifier_input(jets, dijets);

  if (debug_)
    loop_timer->click("Prepared GNN Features");

  // TODO: implement using ONNX 
  // tuple<vector<float>, vector<float>> pred = gnn_classifier_->evaluate(node_x, edge_index, edge_attr);
  vector<float> pair_pred = onnx_classifier_->evaluate(features);
  pair_pred.resize(dijets.size());


  if (debug_)
    loop_timer->click("Evaluated GNN");


  for (unsigned int i = 0; i < dijets.size(); i++)
  {
    dijets[i].set_param("score", pair_pred[i]);
  }

  ei.dijet_list = dijets;

  std::sort(dijets.begin(), dijets.end(), [](DiJet& d1, DiJet& d2)
            { return d1.get_param("score", 0) > d2.get_param("score", 0); });

  vector<Jet> selected_jets;
  vector<int> selected_idxs;
  vector<float> higgs_score;
  for (DiJet &d : dijets)
  {
    int x_i = d.get_j1Idx();
    int x_j = d.get_j2Idx();

    if (!(x_i < x_j))
      continue;

    Jet &j1 = jets[x_i];
    Jet &j2 = jets[x_j];

    // Make sure we haven't used these jets yet
    if (std::find(selected_idxs.begin(), selected_idxs.end(), x_i) != selected_idxs.end() ||
        std::find(selected_idxs.begin(), selected_idxs.end(), x_j) != selected_idxs.end())
      continue;
      
    selected_idxs.push_back(x_i);
    selected_idxs.push_back(x_j);

    higgs_score.push_back(d.get_param("score", 0));
    selected_jets.push_back(j1);
    selected_jets.push_back(j2);
  }
  if (debug_)
    loop_timer->click("Selected GNN Pair");

  CompositeCandidate H1Y1 (selected_jets.at(0), selected_jets.at(1));
  CompositeCandidate H2Y1 (selected_jets.at(2), selected_jets.at(3));
  CompositeCandidate H1Y2 (selected_jets.at(4), selected_jets.at(5));
  CompositeCandidate H2Y2 (selected_jets.at(6), selected_jets.at(7));

  H1Y1.set_param("score", higgs_score.at(0));
  H2Y1.set_param("score", higgs_score.at(1));
  H1Y2.set_param("score", higgs_score.at(2));
  H2Y2.set_param("score", higgs_score.at(3));

  return std::make_tuple(H1Y1, H2Y1, H1Y2,H2Y2);
}

H4_tuple EightB_functions::pair_4H_gnn_quadh (NanoAODTree &nat, EventInfo& ei, const std::vector<Jet>& in_jets)
{
  // 8 jets grouped into 4 groups of 2
  if (quadH_jet_groups.size() == 0)
  {
    vector<int> groups = {2, 2, 2, 2};
    quadH_jet_groups = combinations(8, groups);
  }

  vector<Jet> jets = in_jets;
  vector<DiJet> dijets = make_dijets(nat, ei, in_jets);
  map<string, vector<float>> features = buildClassifierInput::build_gnn_classifier_input(jets, dijets);

  if (debug_)
    loop_timer->click("Prepared GNN Features");

  // TODO: implement using ONNX 
  // tuple<vector<float>, vector<float>> pred = gnn_classifier_->evaluate(node_x, edge_index, edge_attr);
  bool is_binary = false;
  vector<float> pred = onnx_classifier_->evaluate(features, is_binary);

  if (debug_)
    loop_timer->click("Evaluated GNN");

  
  int argmax = std::distance(pred.begin(), std::max_element(pred.begin(), pred.end()));
  vector<vector<int>> best_group = quadH_jet_groups[argmax];

  vector<Jet> selected_jets;
  for (vector<int> pair : best_group) {
    for (int i : pair) {
      selected_jets.push_back(jets[i]);
    }
  }

  if (debug_)
    loop_timer->click("Selected GNN Pair");

  CompositeCandidate H1Y1 (selected_jets.at(0), selected_jets.at(1));
  CompositeCandidate H2Y1 (selected_jets.at(2), selected_jets.at(3));
  CompositeCandidate H1Y2 (selected_jets.at(4), selected_jets.at(5));
  CompositeCandidate H2Y2 (selected_jets.at(6), selected_jets.at(7));

  ei.quadh_score = pred[argmax];

  return std::make_tuple(H1Y1, H2Y1, H1Y2,H2Y2);
}

YY_tuple EightB_functions::pair_YY_passthrough(NanoAODTree &nat, EventInfo &ei, const H4_tuple &reco_Hs)
{
  CompositeCandidate Y1(std::get<0>(reco_Hs), std::get<1>(reco_Hs));
  CompositeCandidate Y2(std::get<2>(reco_Hs), std::get<3>(reco_Hs));

  return std::make_tuple(Y1, Y2);
}

YY_tuple EightB_functions::pair_YY_min_mass_spread(NanoAODTree &nat, EventInfo &ei, const H4_tuple &reco_Hs)
{
  if (debug_) loop_timer->click("Dihiggs Min Mass Spread Pairing");
  std::vector<CompositeCandidate> higgs = {std::get<0>(reco_Hs), std::get<1>(reco_Hs), std::get<2>(reco_Hs), std::get<3>(reco_Hs)};

  
  // 4 higgs grouped into 2 groups of 2
  if (diY_higgs_groups.size() == 0)
  {
    vector<int> groups = {2, 2};
    diY_higgs_groups = combinations(4, groups);
  }

  map<int, CompositeCandidate> dihiggsMap;
  std::hash<std::string> str_hash;
  auto pair_hash = [str_hash](vector<int> pair) { return str_hash(to_string(pair[0]) + to_string(pair[1])); };

  vector<float> m_asyms;
  for (vector<vector<int>> group : diY_higgs_groups) {
    vector<float> group_m;
    for (vector<int> pair : group) {
      int hash = pair_hash(pair);
      if ( dihiggsMap.count(hash) == 0 )
      {
        dihiggsMap[hash] = CompositeCandidate(higgs.at(pair[0]), higgs.at(pair[1]));
      }
      group_m.push_back(dihiggsMap[hash].P4().M());
    }
    std::sort(group_m.begin(), group_m.end(), [](float m1, float m2) { return m1 < m2; });
    float m_asym = (group_m[1] - group_m[0]) / (group_m[1] + group_m[0]);
    // float m_asym = (group_m[3] - group_m[0]);
    m_asyms.push_back(m_asym);
  }
  int argmin = std::distance(m_asyms.begin(), std::min_element(m_asyms.begin(), m_asyms.end()));
  vector<vector<int>> best_group = diY_higgs_groups[argmin];

  CompositeCandidate Y1 = dihiggsMap[pair_hash(best_group[0])];
  CompositeCandidate Y2 = dihiggsMap[pair_hash(best_group[1])];
  return std::make_tuple(Y1, Y2);
}


YY_tuple EightB_functions::pair_2Y_4H(NanoAODTree &nat, EventInfo &ei, const std::vector<Jet> &in_jets)
{
  YY_tuple reco_YYs;
  std::string YYAlgo = pmap.get_param<std::string>("configurations", "YYChoice");
  // if (YYAlgo == "passthrough")
  //   reco_YYs = pair_YY_passthrough(nat, ei, in_jets);
  if (YYAlgo == "min_mass_spread")
    reco_YYs = pair_YY_min_mass_spread(nat, ei, in_jets);

  H4_tuple reco_Hs;
  std::string pairAlgo = pmap.get_param<std::string>("configurations", "jetPairsChoice");
  if (pairAlgo == "passthrough")
  {
    
  }
  if (pairAlgo == "min_mass_spread")
    reco_YYs = pair_4H_min_mass_spread(nat, ei, reco_YYs);

  if (debug_) loop_timer->click("Pairing Higgs");

  return reco_YYs;
}

YY_tuple EightB_functions::pair_YY_min_mass_spread(NanoAODTree &nat, EventInfo &ei, const std::vector<Jet>& jets)
{
  if (jets.size() != 8)
    throw std::runtime_error("The jet pairing -passthrough- function requires 8 jets");

  if (debug_) loop_timer->click("4-Jet Min Mass Spread Pairing");
  
  // 8 jets grouped into 2 groups of 4
  if (diY_jet_groups.size() == 0)
  {
    vector<int> groups = {4, 4};
    diY_jet_groups = combinations(8, groups);
  }

  map<int, CompositeCandidate> dihiggsMap;

  std::hash<std::string> str_hash;
  auto pair_hash = [str_hash](vector<int> pair) {
    return str_hash(to_string(pair[0]) + to_string(pair[1]) + to_string(pair[2]) + to_string(pair[3]));
  };

  vector<float> m_asyms;
  for (vector<vector<int>> group : diY_jet_groups) {
    vector<float> group_m;
    for (vector<int> pair : group) {
      int hash = pair_hash(pair);
      if ( dihiggsMap.count(hash) == 0 )
      {
        CompositeCandidate h1 = CompositeCandidate(jets.at(pair[0]), jets.at(pair[1]));
        CompositeCandidate h2 = CompositeCandidate(jets.at(pair[2]), jets.at(pair[3]));
        h1.rebuildP4UsingRegressedPt(true, true);
        h2.rebuildP4UsingRegressedPt(true, true);
        dihiggsMap[hash] = CompositeCandidate(h1, h2);
      }
      group_m.push_back(dihiggsMap[hash].P4().M());
    }
    std::sort(group_m.begin(), group_m.end(), [](float m1, float m2) { return m1 < m2; });
    float m_asym = (group_m[1] - group_m[0]) / (group_m[1] + group_m[0]);
    // float m_asym = (group_m[3] - group_m[0]);
    m_asyms.push_back(m_asym);
  }
  int argmin = std::distance(m_asyms.begin(), std::min_element(m_asyms.begin(), m_asyms.end()));
  vector<vector<int>> best_group = diY_jet_groups[argmin];

  CompositeCandidate Y1 = dihiggsMap[pair_hash(best_group[0])];
  CompositeCandidate Y2 = dihiggsMap[pair_hash(best_group[1])];

  return std::make_tuple(Y1, Y2);
}

YY_tuple EightB_functions::pair_4H_min_mass_spread(NanoAODTree &nat, EventInfo &ei, const YY_tuple &reco_YYs)
{
  if (debug_) loop_timer->click("Dijet Min Mass Spread Pairing");

  // 4 higgs grouped into 2 groups of 2
  if (diH_y_groups.size() == 0)
  {
    vector<int> groups = {2, 2};
    diH_y_groups = combinations(4, groups);
  }


  CompositeCandidate& H1Y1_ = static_cast<CompositeCandidate&>(std::get<0>(reco_YYs).getComponent1());
  CompositeCandidate& H2Y1_ = static_cast<CompositeCandidate&>(std::get<0>(reco_YYs).getComponent2());
  CompositeCandidate& H1Y2_ = static_cast<CompositeCandidate&>(std::get<1>(reco_YYs).getComponent1());
  CompositeCandidate& H2Y2_ = static_cast<CompositeCandidate&>(std::get<1>(reco_YYs).getComponent2());

  vector<vector<Jet>> jets = {{
                                  static_cast<Jet&>(H1Y1_.getComponent1()),
                                  static_cast<Jet&>(H1Y1_.getComponent2()),
                                  static_cast<Jet&>(H2Y1_.getComponent1()),
                                  static_cast<Jet&>(H2Y1_.getComponent2()),
                              },
                              {
                                  static_cast<Jet&>(H1Y2_.getComponent1()),
                                  static_cast<Jet&>(H1Y2_.getComponent2()),
                                  static_cast<Jet&>(H2Y2_.getComponent1()),
                                  static_cast<Jet&>(H2Y2_.getComponent2()),
                              }};

  map<int, CompositeCandidate> dijetMap;
  std::hash<std::string> str_hash;

  vector<vector<int>> best_group;
  auto pair_hash = [str_hash](int y, vector<int> pair) { return str_hash(to_string(y)+to_string(pair[0]) + to_string(pair[1])); };

  for (int y = 0; y < 2; y++) {
    vector<float> m_asyms;
    for (vector<vector<int>> group : diH_y_groups) {
      vector<float> group_m;
      for (vector<int> &pair : group) {
        int hash = pair_hash(y, pair);
        if (dijetMap.count(hash) == 0) {
          dijetMap[hash] = CompositeCandidate(jets[y].at(pair[0]), jets[y].at(pair[1]));
          dijetMap[hash].rebuildP4UsingRegressedPt(true, true);
        }
        group_m.push_back(dijetMap[hash].P4().M());
      }
      std::sort(group_m.begin(), group_m.end(), [](float m1, float m2) { return m1 < m2; });
      float m_asym = (group_m[1] - group_m[0]) / (group_m[1] + group_m[0]);
      // float m_asym = (group_m[3] - group_m[0]);
      m_asyms.push_back(m_asym);
    }
    int argmin = std::distance(m_asyms.begin(), std::min_element(m_asyms.begin(), m_asyms.end()));
    vector<vector<int>> best_group_ = diH_y_groups[argmin];
    best_group.insert(best_group.end(), best_group_.begin(), best_group_.end());
  }

  CompositeCandidate H1Y1 = dijetMap[pair_hash(0, best_group[0])];
  CompositeCandidate H2Y1 = dijetMap[pair_hash(0, best_group[1])];
  CompositeCandidate H1Y2 = dijetMap[pair_hash(1, best_group[2])];
  CompositeCandidate H2Y2 = dijetMap[pair_hash(1, best_group[3])];

  CompositeCandidate Y1(H1Y1, H2Y1);
  CompositeCandidate Y2(H1Y2, H2Y2);

  return std::make_tuple(Y1, Y2);
}

int EightB_functions::n_gjmatched_in_jetcoll(NanoAODTree& nat, EventInfo& ei, const std::vector<Jet>& in_jets)
{
  std::vector<int> matched_jets;
  if (ei.gen_H1Y1_b1_recojet)  matched_jets.push_back(ei.gen_H1Y1_b1_recojet->getIdx());
  if (ei.gen_H1Y1_b2_recojet)  matched_jets.push_back(ei.gen_H1Y1_b2_recojet->getIdx());
  if (ei.gen_H2Y1_b1_recojet)  matched_jets.push_back(ei.gen_H2Y1_b1_recojet->getIdx());
  if (ei.gen_H2Y1_b2_recojet)  matched_jets.push_back(ei.gen_H2Y1_b2_recojet->getIdx());
  if (ei.gen_H1Y2_b1_recojet)  matched_jets.push_back(ei.gen_H1Y2_b1_recojet->getIdx());
  if (ei.gen_H1Y2_b2_recojet)  matched_jets.push_back(ei.gen_H1Y2_b2_recojet->getIdx());
  if (ei.gen_H2Y2_b1_recojet)  matched_jets.push_back(ei.gen_H2Y2_b1_recojet->getIdx());
  if (ei.gen_H2Y2_b2_recojet)  matched_jets.push_back(ei.gen_H2Y2_b2_recojet->getIdx());

  std::vector<int> reco_js (in_jets.size());
  for (unsigned int ij = 0; ij < in_jets.size(); ++ij)
    reco_js.at(ij) = in_jets.at(ij).getIdx();

  int nfound = 0;
  for (int imj : matched_jets){
    if (std::find(reco_js.begin(), reco_js.end(), imj) != reco_js.end())
      nfound += 1;
  }

  return nfound;
}

int EightB_functions::n_ghmatched_in_jetcoll(NanoAODTree& nat, EventInfo& ei, const std::vector<Jet>& in_jets)
{
  std::vector<int> matched_jets(8,-1);
  if (ei.gen_H1Y1_b1_recojet)  matched_jets[0] = ei.gen_H1Y1_b1_recojet->getIdx();
  if (ei.gen_H1Y1_b2_recojet)  matched_jets[1] = ei.gen_H1Y1_b2_recojet->getIdx();
  if (ei.gen_H2Y1_b1_recojet)  matched_jets[2] = ei.gen_H2Y1_b1_recojet->getIdx();
  if (ei.gen_H2Y1_b2_recojet)  matched_jets[3] = ei.gen_H2Y1_b2_recojet->getIdx();
  if (ei.gen_H1Y2_b1_recojet)  matched_jets[4] = ei.gen_H1Y2_b1_recojet->getIdx();
  if (ei.gen_H1Y2_b2_recojet)  matched_jets[5] = ei.gen_H1Y2_b2_recojet->getIdx();
  if (ei.gen_H2Y2_b1_recojet)  matched_jets[6] = ei.gen_H2Y2_b1_recojet->getIdx();
  if (ei.gen_H2Y2_b2_recojet)  matched_jets[7] = ei.gen_H2Y2_b2_recojet->getIdx();

  std::vector<int> reco_js(in_jets.size());
  for (unsigned int ij = 0; ij < in_jets.size(); ++ij)
    reco_js.at(ij) = in_jets.at(ij).getIdx();

  int nfound = 0;
  for (unsigned int ih = 0; ih < 4; ++ih)
  {
    bool paired = true;
    for (unsigned int ij = 0; ij < 2; ++ij)
    {
      paired = paired & (std::find(reco_js.begin(), reco_js.end(), matched_jets[2 * ih + ij]) != reco_js.end());
    }
    if (paired)
      nfound += 1;
  }

  return nfound;
}

void EightB_functions::match_signal_genjets(NanoAODTree &nat, EventInfo& ei, std::vector<GenJet> &in_jets)
{
  std::vector<int> matched_jets(8, -1);
  if (ei.gen_H1Y1_b1_genjet)
    matched_jets[0] = ei.gen_H1Y1_b1_genjet->getIdx();
  if (ei.gen_H1Y1_b2_genjet)
    matched_jets[1] = ei.gen_H1Y1_b2_genjet->getIdx();
  if (ei.gen_H2Y1_b1_genjet)
    matched_jets[2] = ei.gen_H2Y1_b1_genjet->getIdx();
  if (ei.gen_H2Y1_b2_genjet)
    matched_jets[3] = ei.gen_H2Y1_b2_genjet->getIdx();
  if (ei.gen_H1Y2_b1_genjet)
    matched_jets[4] = ei.gen_H1Y2_b1_genjet->getIdx();
  if (ei.gen_H1Y2_b2_genjet)
    matched_jets[5] = ei.gen_H1Y2_b2_genjet->getIdx();
  if (ei.gen_H2Y2_b1_genjet)
    matched_jets[6] = ei.gen_H2Y2_b1_genjet->getIdx();
  if (ei.gen_H2Y2_b2_genjet)
    matched_jets[7] = ei.gen_H2Y2_b2_genjet->getIdx();

  for (GenJet &gj : in_jets)
  {
    int gj_idx = gj.getIdx();
    if (gj_idx == -1)
      continue;

    for (int id = 0; id < 8; id++)
    {
      if (matched_jets[id] == gj_idx)
      {
        gj.set_signalId(id);
      }
    }
  }
}

void EightB_functions::match_signal_recojets(NanoAODTree &nat, EventInfo& ei, std::vector<Jet> &in_jets)
{
  std::vector<int> matched_jets(8, -1);
  if (ei.gen_H1Y1_b1_recojet)
    matched_jets[0] = ei.gen_H1Y1_b1_recojet->getIdx();
  if (ei.gen_H1Y1_b2_recojet)
    matched_jets[1] = ei.gen_H1Y1_b2_recojet->getIdx();
  if (ei.gen_H2Y1_b1_recojet)
    matched_jets[2] = ei.gen_H2Y1_b1_recojet->getIdx();
  if (ei.gen_H2Y1_b2_recojet)
    matched_jets[3] = ei.gen_H2Y1_b2_recojet->getIdx();
  if (ei.gen_H1Y2_b1_recojet)
    matched_jets[4] = ei.gen_H1Y2_b1_recojet->getIdx();
  if (ei.gen_H1Y2_b2_recojet)
    matched_jets[5] = ei.gen_H1Y2_b2_recojet->getIdx();
  if (ei.gen_H2Y2_b1_recojet)
    matched_jets[6] = ei.gen_H2Y2_b1_recojet->getIdx();
  if (ei.gen_H2Y2_b2_recojet)
    matched_jets[7] = ei.gen_H2Y2_b2_recojet->getIdx();

  for (Jet &j : in_jets)
  {
    int j_idx = j.getIdx();
    if (j_idx == -1)
      continue;

    for (int id = 0; id < 8; id++)
    {
      if (matched_jets[id] == j_idx)
      {
        j.set_signalId(id);
      }
    }
  }
}

 #include "EightB_functions.h"
#include "Math/VectorUtil.h"
#include "Math/Vector3D.h"
#include "Math/Functions.h"

#include "BuildClassifierInput.h"

// #include "DebugUtils.h"

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
  pmap.insert_param<double>("presel", "pt_min",  config.readDoubleOpt("presel::pt_min"));
  pmap.insert_param<double>("presel", "eta_max", config.readDoubleOpt("presel::eta_max"));
  pmap.insert_param<int>   ("presel", "pf_id",   config.readIntOpt("presel::pf_id"));
  pmap.insert_param<int>   ("presel", "pu_id",   config.readIntOpt("presel::pu_id"));
  
  // eightb jet choice
  pmap.insert_param<string>("configurations", "eightbJetChoice", config.readStringOpt("configurations::eightbJetChoice"));
  
  // HHHH pairing
  pmap.insert_param<string>("configurations", "jetPairsChoice", config.readStringOpt("configurations::jetPairsChoice"));

  // YY pairing
  pmap.insert_param<string>("configurations", "YYChoice", config.readStringOpt("configurations::YYChoice"));

  // H done with regressed pT
  pmap.insert_param<bool>("configurations", "useRegressedPtForHp4", config.readBoolOpt("configurations::useRegressedPtForHp4"));
}

void EightB_functions::initialize_functions(TFile& outputFile)
{
 
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

  std::vector<int> genjet_idxs;

  std::vector<GenJet> genjets;
  for (unsigned int igj = 0; igj < *(nat.nGenJet); ++igj)
  {
    GenJet gj(igj, &nat);
    genjets.push_back(gj);
  }

  for (GenPart *b : bs_to_match)
  {
    std::vector<std::tuple<double, int, int>> matched_gj; // dR, idx in nanoAOD, idx in local coll
    for (unsigned int igj = 0; igj < genjets.size(); ++igj)
    {
      GenJet &gj = genjets.at(igj);
      double dR = ROOT::Math::VectorUtil::DeltaR(b->P4(), gj.P4());
      if (dR < dR_match)
        matched_gj.push_back(std::make_tuple(dR, gj.getIdx(), igj)); // save the idx in the nanoAOD collection to rebuild this after
    }

    if (matched_gj.size() > 0)
    {
      std::sort(matched_gj.begin(), matched_gj.end());
      auto best_match = matched_gj.at(0);
      genjet_idxs.push_back(std::get<1>(best_match));
      if (ensure_unique) // genjet already used, remove it from the input list
        genjets.erase(genjets.begin() + std::get<2>(best_match));
    }
    else
      genjet_idxs.push_back(-1);
  }

  // matched done, store in ei - use the map built above in bs_to_match to know the correspondence position <-> meaning
  if (genjet_idxs.at(0) >= 0)
    ei.gen_H1Y1_b1_genjet = GenJet(genjet_idxs.at(0), &nat);
  if (genjet_idxs.at(1) >= 0)
    ei.gen_H1Y1_b2_genjet = GenJet(genjet_idxs.at(1), &nat);

  if (genjet_idxs.at(2) >= 0)
    ei.gen_H2Y1_b1_genjet = GenJet(genjet_idxs.at(2), &nat);
  if (genjet_idxs.at(3) >= 0)
    ei.gen_H2Y1_b2_genjet = GenJet(genjet_idxs.at(3), &nat);

  if (genjet_idxs.at(4) >= 0)
    ei.gen_H1Y2_b1_genjet = GenJet(genjet_idxs.at(4), &nat);
  if (genjet_idxs.at(5) >= 0)
    ei.gen_H1Y2_b2_genjet = GenJet(genjet_idxs.at(5), &nat);

  if (genjet_idxs.at(6) >= 0)
    ei.gen_H2Y2_b1_genjet = GenJet(genjet_idxs.at(6), &nat);
  if (genjet_idxs.at(7) >= 0)
    ei.gen_H2Y2_b2_genjet = GenJet(genjet_idxs.at(7), &nat);

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
    if ( (ei.gen_H1Y1_b1_recojet && ijet == ei.gen_H1Y1_b1_recojet->getIdx())   || (ei.gen_H1Y1_b2_recojet && ijet == ei.gen_H1Y1_b2_recojet->getIdx()) )
        return 0; 
    if ( (ei.gen_H2Y1_b1_recojet && ijet == ei.gen_H2Y1_b1_recojet->getIdx())   || (ei.gen_H2Y1_b2_recojet && ijet == ei.gen_H2Y1_b2_recojet->getIdx()) )
        return 1; 
    if ( (ei.gen_H1Y2_b1_recojet && ijet == ei.gen_H1Y2_b1_recojet->getIdx())   || (ei.gen_H1Y2_b2_recojet && ijet == ei.gen_H1Y2_b2_recojet->getIdx()) )
        return 2; 
    if ( (ei.gen_H2Y2_b1_recojet && ijet == ei.gen_H2Y2_b1_recojet->getIdx())   || (ei.gen_H2Y2_b2_recojet && ijet == ei.gen_H2Y2_b2_recojet->getIdx()) )
        return 3; 
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

    // flags per event
    int nfound_paired_h = 0;

    if (ei.H1Y1_b1_genHflag > -1 && ei.H1Y1_b1_genHflag == ei.H1Y1_b2_genHflag)  nfound_paired_h += 1;
    if (ei.H2Y1_b1_genHflag > -1 && ei.H2Y1_b1_genHflag == ei.H2Y1_b2_genHflag)  nfound_paired_h += 1;
    if (ei.H1Y2_b1_genHflag > -1 && ei.H1Y2_b1_genHflag == ei.H1Y2_b2_genHflag)  nfound_paired_h += 1;
    if (ei.H2Y2_b1_genHflag > -1 && ei.H2Y2_b1_genHflag == ei.H2Y2_b2_genHflag)  nfound_paired_h += 1;
    ei.nfound_paired_h = nfound_paired_h; // number of selected jets that are from H
}

////////////////////////////////////////////////////////////////////
////////////////////// EightB jet selections//////////////////////////
////////////////////////////////////////////////////////////////////

std::vector<Jet> EightB_functions::select_jets(NanoAODTree& nat, EventInfo& ei, const std::vector<Jet>& in_jets)
{
  std::string sel_type = pmap.get_param<std::string>("configurations", "eightbJetChoice");
  
  if (sel_type == "maxbtag")
    return select_eightb_jets_maxbtag(nat, ei, in_jets);
    
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

    return jets;
}


void EightB_functions::pair_jets(NanoAODTree& nat, EventInfo& ei, const std::vector<Jet>& in_jets)
{
    //TODO implement D_HHHH method
    
  std::tuple<CompositeCandidate, CompositeCandidate, CompositeCandidate, CompositeCandidate> reco_Hs;
  std::string pairAlgo = pmap.get_param<std::string>("configurations", "jetPairsChoice");

  
  if (pairAlgo == "passthrough")
    reco_Hs = pair_4H_passthrough(nat, ei, in_jets);
  if (pairAlgo == "min_mass_spread")
    reco_Hs = pair_4H_min_mass_spread(nat, ei, in_jets);

  std::tuple<CompositeCandidate, CompositeCandidate> reco_YYs;
  std::string YYAlgo = pmap.get_param<std::string>("configurations", "YYChoice");
  if (YYAlgo == "passthrough")
    reco_YYs = pair_YY_passthrough(nat, ei, reco_Hs);
  if (YYAlgo == "min_mass_spread")
    reco_YYs = pair_YY_min_mass_spread(nat, ei, reco_Hs);

  

  CompositeCandidate &H1Y1 = static_cast<CompositeCandidate &>(std::get<0>(reco_YYs).getComponent1());
  CompositeCandidate &H2Y1 = static_cast<CompositeCandidate &>(std::get<0>(reco_YYs).getComponent2());
  CompositeCandidate &H1Y2 = static_cast<CompositeCandidate &>(std::get<1>(reco_YYs).getComponent1());
  CompositeCandidate &H2Y2 = static_cast<CompositeCandidate &>(std::get<1>(reco_YYs).getComponent2());

  // rebuild p4 with regressed pT if required
  if (pmap.get_param<bool>("configurations", "useRegressedPtForHp4")){
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
}

std::tuple<CompositeCandidate, CompositeCandidate, CompositeCandidate, CompositeCandidate> EightB_functions::pair_4H_passthrough (NanoAODTree &nat, EventInfo& ei, const std::vector<Jet>& jets)
{
  if (jets.size() != 8)
    throw std::runtime_error("The jet pairing -passthrough- function requires 8 jets");

  CompositeCandidate H1Y1  (jets.at(0), jets.at(1));
  CompositeCandidate H2Y1 (jets.at(2), jets.at(3));
  CompositeCandidate H1Y2 (jets.at(4), jets.at(5));
  CompositeCandidate H2Y2 (jets.at(6), jets.at(7));

  return std::make_tuple(H1Y1, H2Y1, H1Y2,H2Y2);
}

std::tuple<CompositeCandidate, CompositeCandidate, CompositeCandidate, CompositeCandidate> EightB_functions::pair_4H_min_mass_spread(NanoAODTree &nat, EventInfo &ei, const std::vector<Jet> &jets)
{
  if (jets.size() != 8)
    throw std::runtime_error("The jet pairing -passthrough- function requires 8 jets");

  std::vector<CompositeCandidate> dijets(dijet_pairings.size());
  for (unsigned int i = 0; i < dijet_pairings.size(); i++)
  {
    int j0 = dijet_pairings[i][0];
    int j1 = dijet_pairings[i][1];
    dijets[i] = CompositeCandidate(jets.at(j0), jets.at(j1));
    dijets[i].rebuildP4UsingRegressedPt(true, true);
  }

  std::vector<int> min_quadH_pair(4);
  float min_mass_spread = std::numeric_limits<float>::max();
  for (unsigned int i = 0; i < quadH_pairings.size(); i++)
  {
    std::vector<int> quadH_pair = quadH_pairings[i];
    std::sort(quadH_pair.begin(), quadH_pair.end(), [dijets](int &h1, int &h2)
              { return dijets[h1].P4().M() > dijets[h2].P4().M(); });
    float mass_spread = fabs(dijets[quadH_pair[0]].P4().M() - dijets[quadH_pair[3]].P4().M());
    if (mass_spread < min_mass_spread)
    {
      min_quadH_pair = quadH_pair;
      min_mass_spread = mass_spread;
    }
  }

  CompositeCandidate H1Y1 = dijets[min_quadH_pair[0]];
  CompositeCandidate H2Y1 = dijets[min_quadH_pair[1]];
  CompositeCandidate H1Y2 = dijets[min_quadH_pair[2]];
  CompositeCandidate H2Y2 = dijets[min_quadH_pair[3]];


  return std::make_tuple(H1Y1, H2Y1, H1Y2, H2Y2);
}

std::tuple<CompositeCandidate, CompositeCandidate> EightB_functions::pair_YY_passthrough(NanoAODTree &nat, EventInfo &ei, const std::tuple<CompositeCandidate, CompositeCandidate, CompositeCandidate, CompositeCandidate> &reco_Hs)
{
  CompositeCandidate Y1(std::get<0>(reco_Hs), std::get<1>(reco_Hs));
  CompositeCandidate Y2(std::get<2>(reco_Hs), std::get<3>(reco_Hs));

  return std::make_tuple(Y1, Y2);
}

std::tuple<CompositeCandidate, CompositeCandidate> EightB_functions::pair_YY_min_mass_spread(NanoAODTree &nat, EventInfo &ei, const std::tuple<CompositeCandidate, CompositeCandidate, CompositeCandidate, CompositeCandidate> &reco_Hs)
{
  std::vector<CompositeCandidate> higgs = {std::get<0>(reco_Hs), std::get<1>(reco_Hs), std::get<2>(reco_Hs), std::get<3>(reco_Hs)};
  std::vector<CompositeCandidate> dihiggs(dihiggs_pairings.size());
  for (unsigned int i = 0; i < dihiggs_pairings.size(); i++)
  {
    int h0 = dihiggs_pairings[i][0];
    int h1 = dihiggs_pairings[i][1];
    dihiggs[i] = CompositeCandidate(higgs[h0],higgs[h1]);
  }

  std::vector<int> min_diY_pair(2);
  float min_mass_spread = std::numeric_limits<float>::max();
  for (unsigned int i = 0; i < diY_pairings.size(); i++)
  {
    std::vector<int> diY_pair = diY_pairings[i];
    std::sort(diY_pair.begin(), diY_pair.end(), [dihiggs](int &y1, int &y2)
              { return dihiggs[y1].P4().M() > dihiggs[y2].P4().M(); });
    float mass_spread = fabs(dihiggs[diY_pair[0]].P4().M() - dihiggs[diY_pair[1]].P4().M());
    if (mass_spread < min_mass_spread)
    {
      min_diY_pair = diY_pair;
      min_mass_spread = mass_spread;
    }
  }

  CompositeCandidate Y1 = dihiggs[min_diY_pair[0]];
  CompositeCandidate Y2 = dihiggs[min_diY_pair[1]];
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
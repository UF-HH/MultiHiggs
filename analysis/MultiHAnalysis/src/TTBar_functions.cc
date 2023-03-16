#include "TTBar_functions.h"
#include "Math/VectorUtil.h"
#include "Math/Vector3D.h"
#include "Math/Functions.h"

#include "BuildClassifierInput.h"

// #include "DebugUtils.h"

#include <iostream>
#include <tuple>
#include <algorithm>

#include "Electron.h"
#include "Muon.h"

using namespace std;

std::vector<Jet> TTBar_functions::select_jets(NanoAODTree &nat, EventInfo &ei, const std::vector<Jet> &in_jets)
{
  std::vector<Jet> jets = in_jets;

  jets.resize(6);
  // stable_sort(jets.begin(), jets.end(), [](const Jet& a, const Jet& b) -> bool {
  //   return ( get_property (a, Jet_btagDeepFlavB) > get_property (b, Jet_btagDeepFlavB) ); }
  //   ); // sort jet by deepjet score (highest to lowest)

  // if (jets.size() < 2)
  //   return jets;
  // ei.bjet1 = jets.at(0);
  // ei.bjet2 = jets.at(0);
  // if (ei.bjet1->P4().Pt() < ei.bjet2->P4().Pt()) // sort by pt
  //   std::swap(ei.bjet1, ei.bjet2);

  return jets;

  // int n_out = std::min<int>(jets.size(), 6);
  // jets.resize(n_out);

  // for (auto& jet : jets)
  //     std::cout << jet.P4().Pt() << " " << get_property (jet, Jet_btagDeepFlavB) << std::endl;
  // std::cout << std::endl << std::endl;

  // return jets;

}

void TTBar_functions::select_gen_particles(NanoAODTree& nat, EventInfo& ei) {
  for (uint igp = 0; igp < *(nat.nGenPart); ++igp) {
    GenPart gp(igp, &nat);
    int apdgid = abs(get_property(gp, GenPart_pdgId));
    // top
    if (abs(apdgid) == 6 && gp.isLastCopy()) {
      if (0) {
        std::cout << "Found Top" << std::endl;
      }
      assign_to_uninit(gp, {&ei.gen_t1, &ei.gen_t2});
    }

    // W
    if (abs(apdgid) == 24 && gp.isFirstCopy()) {
      int moth_idx = get_property(gp, GenPart_genPartIdxMother);
      if (moth_idx >= 0) {
        GenPart mother(moth_idx, &nat);
        int amothpdgid = abs(get_property(mother, GenPart_pdgId));

        if (abs(amothpdgid) == 6) {
          if (0) {
            std::cout << "Found Top --> W" << std::endl;
          }
          if (ei.gen_t1 && moth_idx == ei.gen_t1->getIdx()) {
            if (0) {
              std::cout << "Found t1 --> W" << std::endl;
            }
            ei.gen_t1_w = gp;
          }
          if (ei.gen_t2 && moth_idx == ei.gen_t2->getIdx()){
            if (0) {
              std::cout << "Found t2 --> W" << std::endl;
            }
            ei.gen_t2_w = gp;
          }
        }
      }
    }

    // b
    if (abs(apdgid) == 5 && gp.isFirstCopy()) {
      int moth_idx = get_property(gp, GenPart_genPartIdxMother);
      if (moth_idx >= 0) {
        GenPart mother(moth_idx, &nat);
        int amothpdgid = abs(get_property(mother, GenPart_pdgId));

        if (abs(amothpdgid) == 6) {
          if (0) {
            std::cout << "Found Top --> b" << std::endl;
          }
          if (ei.gen_t1 && moth_idx == ei.gen_t1->getIdx()) {
            if (0) {
              std::cout << "Found t1 --> b" << std::endl;
            }
            ei.gen_t1_b = gp;
          }
          if (ei.gen_t2 && moth_idx == ei.gen_t2->getIdx()) {
            if (0) {
              std::cout << "Found t2 --> b" << std::endl;
            }
            ei.gen_t2_b = gp;
          }
        }
      }
    }

    // udscb
    if (abs(apdgid) >= 1 && abs(apdgid) <= 5 && gp.isFirstCopy()) {
      int moth_idx = get_property(gp, GenPart_genPartIdxMother);

      GenPart mother;
      if (moth_idx >= 0) {
        mother = GenPart(moth_idx, &nat);

        while ( !mother.isFirstCopy() && moth_idx >= 0 ) {
          moth_idx = get_property(mother, GenPart_genPartIdxMother);
          if (moth_idx < 0)
            break;
          mother = GenPart(moth_idx, &nat);
        }
      }
      if (moth_idx >= 0) {

        int amothpdgid = abs(get_property(mother, GenPart_pdgId));

        if (abs(amothpdgid) == 24) {
          if (0) {
            std::cout << "Found Top --> W --> j" << std::endl;
          }
          if (ei.gen_t1_w && moth_idx == ei.gen_t1_w->getIdx()){
            if (0) {
              std::cout << "Found t1 --> W --> j" << std::endl;
            }
            assign_to_uninit(gp, {&ei.gen_t1_w_j1, &ei.gen_t1_w_j2});
          }
          if (ei.gen_t2_w && moth_idx == ei.gen_t2_w->getIdx()){
            if (0) {
              std::cout << "Found t2 --> W --> j" << std::endl;
            }
            assign_to_uninit(gp, {&ei.gen_t2_w_j1, &ei.gen_t2_w_j2});
          }
        }
      }
    }
  }
  // reorder objects according to pt

  if (ei.gen_t1->P4().Pt() < ei.gen_t2->P4().Pt()) {
    std::swap(ei.gen_t1, ei.gen_t2);

    std::swap(ei.gen_t1_b, ei.gen_t2_b);
    std::swap(ei.gen_t1_w, ei.gen_t2_w);
    std::swap(ei.gen_t1_w_j1, ei.gen_t2_w_j1);
    std::swap(ei.gen_t1_w_j2, ei.gen_t2_w_j2);
  }

  if (ei.gen_t1_w_j1->P4().Pt() < ei.gen_t1_w_j2->P4().Pt()) {
    std::swap(ei.gen_t1_w_j1, ei.gen_t1_w_j2);
  }

  if (ei.gen_t2_w_j1->P4().Pt() < ei.gen_t2_w_j2->P4().Pt()) {
    std::swap(ei.gen_t2_w_j1, ei.gen_t2_w_j2);
  }

  return;
}

// match the selected gen b to gen jets
void TTBar_functions::match_genbs_to_genjets(NanoAODTree& nat, EventInfo& ei, bool ensure_unique)
{
  const double dR_match = 0.4;

  std::vector<GenPart*> bs_to_match = {
      ei.gen_t1_b.get_ptr(),
      ei.gen_t1_w_j1.get_ptr(),
      ei.gen_t1_w_j2.get_ptr(),

      ei.gen_t2_b.get_ptr(),
      ei.gen_t2_w_j1.get_ptr(),
      ei.gen_t2_w_j2.get_ptr(),
  };

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
    if (bIdx == ei.gen_t1_b.get_ptr()->getIdx())
      ei.gen_t1_b_genjet = GenJet(j.getIdx(), &nat);
    if (bIdx == ei.gen_t1_w_j1.get_ptr()->getIdx())
      ei.gen_t1_w_j1_genjet = GenJet(j.getIdx(), &nat);
    if (bIdx == ei.gen_t1_w_j2.get_ptr()->getIdx())
      ei.gen_t1_w_j2_genjet = GenJet(j.getIdx(), &nat);

    if (bIdx == ei.gen_t2_b.get_ptr()->getIdx())
      ei.gen_t2_b_genjet = GenJet(j.getIdx(), &nat);
    if (bIdx == ei.gen_t2_w_j1.get_ptr()->getIdx())
      ei.gen_t2_w_j1_genjet = GenJet(j.getIdx(), &nat);
    if (bIdx == ei.gen_t2_w_j2.get_ptr()->getIdx())
      ei.gen_t2_w_j2_genjet = GenJet(j.getIdx(), &nat);
  }

  return;
}

void TTBar_functions::match_genbs_genjets_to_reco(NanoAODTree& nat, EventInfo& ei)
{
  int ij_gen_t1_b_genjet  = (ei.gen_t1_b_genjet  ? find_jet_from_genjet(nat, *ei.gen_t1_b_genjet)  : -1); 
  int ij_gen_t1_w_j1_genjet  = (ei.gen_t1_w_j1_genjet  ? find_jet_from_genjet(nat, *ei.gen_t1_w_j1_genjet)  : -1); 
  int ij_gen_t1_w_j2_genjet  = (ei.gen_t1_w_j2_genjet  ? find_jet_from_genjet(nat, *ei.gen_t1_w_j2_genjet)  : -1); 
  int ij_gen_t2_b_genjet  = (ei.gen_t2_b_genjet  ? find_jet_from_genjet(nat, *ei.gen_t2_b_genjet)  : -1); 
  int ij_gen_t2_w_j1_genjet  = (ei.gen_t2_w_j1_genjet  ? find_jet_from_genjet(nat, *ei.gen_t2_w_j1_genjet)  : -1); 
  int ij_gen_t2_w_j2_genjet  = (ei.gen_t2_w_j2_genjet  ? find_jet_from_genjet(nat, *ei.gen_t2_w_j2_genjet)  : -1); 

  if (ij_gen_t1_b_genjet >= 0)  ei.gen_t1_b_recojet  = Jet(ij_gen_t1_b_genjet,  &nat);
  if (ij_gen_t1_w_j1_genjet >= 0)  ei.gen_t1_w_j1_recojet  = Jet(ij_gen_t1_w_j1_genjet,  &nat);
  if (ij_gen_t1_w_j2_genjet >= 0)  ei.gen_t1_w_j2_recojet  = Jet(ij_gen_t1_w_j2_genjet,  &nat);
  if (ij_gen_t2_b_genjet >= 0)  ei.gen_t2_b_recojet  = Jet(ij_gen_t2_b_genjet,  &nat);
  
  if (ij_gen_t2_w_j1_genjet >= 0)  ei.gen_t2_w_j1_recojet  = Jet(ij_gen_t2_w_j1_genjet,  &nat);
  if (ij_gen_t2_w_j2_genjet >= 0)  ei.gen_t2_w_j2_recojet  = Jet(ij_gen_t2_w_j2_genjet,  &nat);

  // select unique occurences in vector
  // note : PAT tools already ensure that match is unique
  // https://github.com/cms-sw/cmssw/blob/master/PhysicsTools/PatAlgos/python/mcMatchLayer0/jetMatch_cfi.py
  // so the check below is redundant

  // std::vector<int> imatchs;
  // if (ij_gen_t1_b_genjet >= 0)  imatchs.push_back(ij_gen_t1_b_genjet);
  // if (ij_gen_t1_w_j1_genjet >= 0)  imatchs.push_back(ij_gen_t1_w_j1_genjet);
  // if (ij_gen_HY1_b1_genjet >= 0) imatchs.push_back(ij_gen_HY1_b1_genjet);
  // if (ij_gen_HY1_b2_genjet >= 0) imatchs.push_back(ij_gen_HY1_b2_genjet);
  // if (ij_gen_HY2_b1_genjet >= 0) imatchs.push_back(ij_gen_HY2_b1_genjet);
  // if (ij_gen_HY2_b2_genjet >= 0) imatchs.push_back(ij_gen_HY2_b2_genjet);

  // sort(imatchs.begin(), imatchs.end());
  // imatchs.erase(unique (imatchs.begin(), imatchs.end()), imatchs.end());
  // ei.gen_bs_N_reco_match = imatchs.size(); // number of different reco jets that are matched to gen jets

  int nmatched = 0;
  if (ij_gen_t1_b_genjet >= 0)  nmatched += 1;
  if (ij_gen_t1_w_j1_genjet >= 0)  nmatched += 1;
  if (ij_gen_t1_w_j2_genjet >= 0)  nmatched += 1;
  if (ij_gen_t2_b_genjet >= 0)  nmatched += 1;
  if (ij_gen_t2_w_j1_genjet >= 0)  nmatched += 1;
  if (ij_gen_t2_w_j2_genjet >= 0)  nmatched += 1;
  ei.gen_bs_N_reco_match = nmatched;

  // same as above, but apply acceptance cuts on the matched jets
  int nmatched_acc = 0;
  if (ei.gen_t1_b_recojet  && ei.gen_t1_b_recojet->P4().Pt()  > 20 && std::abs(ei.gen_t1_b_recojet->P4().Eta())  < 4.8) nmatched_acc += 1;
  if (ei.gen_t1_w_j1_recojet  && ei.gen_t1_w_j1_recojet->P4().Pt()  > 20 && std::abs(ei.gen_t1_w_j1_recojet->P4().Eta())  < 4.8) nmatched_acc += 1;
  if (ei.gen_t1_w_j2_recojet  && ei.gen_t1_w_j2_recojet->P4().Pt()  > 20 && std::abs(ei.gen_t1_w_j2_recojet->P4().Eta())  < 4.8) nmatched_acc += 1;
  if (ei.gen_t2_b_recojet  && ei.gen_t2_b_recojet->P4().Pt()  > 20 && std::abs(ei.gen_t2_b_recojet->P4().Eta())  < 4.8) nmatched_acc += 1;
  if (ei.gen_t2_w_j1_recojet  && ei.gen_t2_w_j1_recojet->P4().Pt()  > 20 && std::abs(ei.gen_t2_w_j1_recojet->P4().Eta())  < 4.8) nmatched_acc += 1;
  if (ei.gen_t2_w_j2_recojet  && ei.gen_t2_w_j2_recojet->P4().Pt()  > 20 && std::abs(ei.gen_t2_w_j2_recojet->P4().Eta())  < 4.8) nmatched_acc += 1;
  ei.gen_bs_N_reco_match_in_acc = nmatched_acc;

  // now compute p4 sums to make the invariant mass of X - FIXME: can add more inv masses for the various cases
  p4_t p4_sum_matched (0,0,0,0);
  if (ei.gen_t1_b_recojet) p4_sum_matched  += ei.gen_t1_b_recojet->P4();
  if (ei.gen_t1_w_j1_recojet) p4_sum_matched  += ei.gen_t1_w_j1_recojet->P4();
  if (ei.gen_t1_w_j2_recojet) p4_sum_matched  += ei.gen_t1_w_j2_recojet->P4();
  if (ei.gen_t2_b_recojet) p4_sum_matched  += ei.gen_t2_b_recojet->P4();
  if (ei.gen_t2_w_j1_recojet) p4_sum_matched  += ei.gen_t2_w_j1_recojet->P4();
  if (ei.gen_t2_w_j2_recojet) p4_sum_matched  += ei.gen_t2_w_j2_recojet->P4();
  ei.gen_bs_match_recojet_minv = p4_sum_matched.M();

  p4_t p4_sum_matched_acc (0,0,0,0);
  if (ei.gen_t1_b_recojet  && ei.gen_t1_b_recojet->P4().Pt()  > 20 && std::abs(ei.gen_t1_b_recojet->P4().Eta())  < 4.8) p4_sum_matched_acc += ei.gen_t1_b_recojet->P4();
  if (ei.gen_t1_w_j1_recojet  && ei.gen_t1_w_j1_recojet->P4().Pt()  > 20 && std::abs(ei.gen_t1_w_j1_recojet->P4().Eta())  < 4.8) p4_sum_matched_acc += ei.gen_t1_w_j1_recojet->P4();
  if (ei.gen_t1_w_j2_recojet  && ei.gen_t1_w_j2_recojet->P4().Pt()  > 20 && std::abs(ei.gen_t1_w_j2_recojet->P4().Eta())  < 4.8) p4_sum_matched_acc += ei.gen_t1_w_j2_recojet->P4();
  if (ei.gen_t2_b_recojet  && ei.gen_t2_b_recojet->P4().Pt()  > 20 && std::abs(ei.gen_t2_b_recojet->P4().Eta())  < 4.8) p4_sum_matched_acc += ei.gen_t2_b_recojet->P4();
  if (ei.gen_t2_w_j1_recojet  && ei.gen_t2_w_j1_recojet->P4().Pt()  > 20 && std::abs(ei.gen_t2_w_j1_recojet->P4().Eta())  < 4.8) p4_sum_matched_acc += ei.gen_t2_w_j1_recojet->P4();
  if (ei.gen_t2_w_j2_recojet  && ei.gen_t2_w_j2_recojet->P4().Pt()  > 20 && std::abs(ei.gen_t2_w_j2_recojet->P4().Eta())  < 4.8) p4_sum_matched_acc += ei.gen_t2_w_j2_recojet->P4();
  ei.gen_bs_match_in_acc_recojet_minv = p4_sum_matched_acc.M();
}


void TTBar_functions::match_signal_genjets(NanoAODTree &nat, EventInfo& ei, std::vector<GenJet> &in_jets)
{
  std::vector<int> matched_jets(6, -1);
  if (ei.gen_t1_b_genjet)
    matched_jets[0] = ei.gen_t1_b_genjet->getIdx();
  if (ei.gen_t1_w_j1_genjet)
    matched_jets[1] = ei.gen_t1_w_j1_genjet->getIdx();
  if (ei.gen_t1_w_j2_genjet)
    matched_jets[2] = ei.gen_t1_w_j2_genjet->getIdx();
  if (ei.gen_t2_b_genjet)
    matched_jets[3] = ei.gen_t2_b_genjet->getIdx();
  if (ei.gen_t2_w_j1_genjet)
    matched_jets[4] = ei.gen_t2_w_j1_genjet->getIdx();
  if (ei.gen_t2_w_j2_genjet)
    matched_jets[5] = ei.gen_t2_w_j2_genjet->getIdx();

  for (GenJet &gj : in_jets)
  {
    int gj_idx = gj.getIdx();
    if (gj_idx == -1)
      continue;

    for (int id = 0; id < 6; id++)
    {
      if (matched_jets[id] == gj_idx)
      {
        gj.set_signalId(id);
      }
    }
  }
}


void TTBar_functions::match_signal_recojets(NanoAODTree &nat, EventInfo& ei, std::vector<Jet> &in_jets)
{
  std::vector<int> matched_jets(6, -1);
  if (ei.gen_t1_b_recojet)
    matched_jets[0] = ei.gen_t1_b_recojet->getIdx();
  if (ei.gen_t1_w_j1_recojet)
    matched_jets[1] = ei.gen_t1_w_j1_recojet->getIdx();
  if (ei.gen_t1_w_j2_recojet)
    matched_jets[2] = ei.gen_t1_w_j2_recojet->getIdx();
  if (ei.gen_t2_b_recojet)
    matched_jets[3] = ei.gen_t2_b_recojet->getIdx();
  if (ei.gen_t2_w_j1_recojet)
    matched_jets[4] = ei.gen_t2_w_j1_recojet->getIdx();
  if (ei.gen_t2_w_j2_recojet)
    matched_jets[5] = ei.gen_t2_w_j2_recojet->getIdx();

  for (Jet &j : in_jets)
  {
    int j_idx = j.getIdx();
    if (j_idx == -1)
      continue;

    for (int id = 0; id < 6; id++)
    {
      if (matched_jets[id] == j_idx)
      {
        j.set_signalId(id);
      }
    }
  }
}


int TTBar_functions::n_gjmatched_in_jetcoll(NanoAODTree& nat, EventInfo& ei, const std::vector<Jet>& in_jets)
{
  std::vector<int> matched_jets;
  if (ei.gen_t1_b_recojet)  matched_jets.push_back(ei.gen_t1_b_recojet->getIdx());
  if (ei.gen_t1_w_j1_recojet)  matched_jets.push_back(ei.gen_t1_w_j1_recojet->getIdx());
  if (ei.gen_t1_w_j2_recojet)  matched_jets.push_back(ei.gen_t1_w_j2_recojet->getIdx());
  if (ei.gen_t2_b_recojet)  matched_jets.push_back(ei.gen_t2_b_recojet->getIdx());
  if (ei.gen_t2_w_j1_recojet)  matched_jets.push_back(ei.gen_t2_w_j1_recojet->getIdx());
  if (ei.gen_t2_w_j2_recojet)  matched_jets.push_back(ei.gen_t2_w_j2_recojet->getIdx());

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


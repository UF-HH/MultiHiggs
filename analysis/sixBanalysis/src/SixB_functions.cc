#include "SixB_functions.h"
#include "Math/VectorUtil.h"
#include "Math/Vector3D.h"
#include "Math/Functions.h"

#include <iostream>
#include <tuple>
#include <algorithm>

#include "Electron.h"
#include "Muon.h"

void SixB_functions::copy_event_info(NanoAODTree& nat, EventInfo& ei, bool is_mc)
{
  ei.Run     = *(nat.run);
  ei.LumiSec = *(nat.luminosityBlock);
  ei.Event   = *(nat.event);

  ei.n_other_pv                    = *(nat.nOtherPV);
  ei.rhofastjet_all                = *(nat.fixedGridRhoFastjetAll);
  ei.n_total_jet                   = *(nat.nJet);

  // mc-only
  if (is_mc){
    ei.n_pu       = *(nat.Pileup_nPU);
    ei.n_true_int = *(nat.Pileup_nTrueInt);
    ei.n_genjet   = *(nat.nGenJet);
    ei.lhe_ht     = *(nat.LHE_HT);
  }
}

void SixB_functions::select_gen_particles(NanoAODTree& nat, EventInfo& ei)
{
  for (uint igp = 0; igp < *(nat.nGenPart); ++igp)
    {
      GenPart gp (igp, &nat);
      int apdgid = abs(get_property(gp, GenPart_pdgId));
        
      // X
      if (apdgid == 45) {
	if (gp.isFirstCopy())
	  ei.gen_X_fc = gp;
	else if (gp.isLastCopy())
	  ei.gen_X = gp;
      }

      // Y
      if (apdgid == 35 && gp.isLastCopy())
	ei.gen_Y = gp;

      // H
      if (apdgid == 25 && gp.isLastCopy()) {
	GenPart mother (get_property(gp, GenPart_genPartIdxMother), &nat);
	int amothpdgid = abs(get_property(mother, GenPart_pdgId));
	if (amothpdgid == 45)
	  ei.gen_HX = gp;
	else if (amothpdgid == 35)
	  assign_to_uninit(gp, {&ei.gen_HY1, &ei.gen_HY2} );
      }

      // b
      if (apdgid == 5 && gp.isFirstCopy()) {
	int moth_idx = get_property(gp, GenPart_genPartIdxMother);
	if (moth_idx >= 0) {
	  GenPart mother (moth_idx, &nat);
	  int amothpdgid = abs(get_property(mother, GenPart_pdgId));
	  // in the LHE the mother always comes before the daughters, so it is guaranteed to have been found already
	  if (amothpdgid == 25){
	    if (ei.gen_HX && moth_idx == ei.gen_HX->getIdx())
	      assign_to_uninit(gp, {&ei.gen_HX_b1, &ei.gen_HX_b2} );
	    if (ei.gen_HY1 && moth_idx == ei.gen_HY1->getIdx())
	      assign_to_uninit(gp, {&ei.gen_HY1_b1, &ei.gen_HY1_b2} );
	    if (ei.gen_HY2 && moth_idx == ei.gen_HY2->getIdx())
	      assign_to_uninit(gp, {&ei.gen_HY2_b1, &ei.gen_HY2_b2} );
	  }
	}
      }
    }

  // reorder objects according to pt
  if (ei.gen_HY1->P4().Pt() < ei.gen_HY2->P4().Pt()){
    std::swap(ei.gen_HY1,    ei.gen_HY2);
    std::swap(ei.gen_HY1_b1, ei.gen_HY2_b1);
    std::swap(ei.gen_HY1_b2, ei.gen_HY2_b2);
  }

  if (ei.gen_HX_b1->P4().Pt() < ei.gen_HX_b2->P4().Pt())
    std::swap(ei.gen_HX_b1, ei.gen_HX_b2);
  if (ei.gen_HY1_b1->P4().Pt() < ei.gen_HY1_b2->P4().Pt())
    std::swap(ei.gen_HY1_b1, ei.gen_HY1_b2);
  if (ei.gen_HY2_b1->P4().Pt() < ei.gen_HY2_b2->P4().Pt())
    std::swap(ei.gen_HY2_b1, ei.gen_HY2_b2);

  return;
}


// match the selected gen b to gen jets
void SixB_functions::match_genbs_to_genjets(NanoAODTree& nat, EventInfo& ei, bool ensure_unique)
{
  const double dR_match = 0.4;

  std::vector<GenPart*> bs_to_match = {
    ei.gen_HX_b1.get_ptr(),
    ei.gen_HX_b2.get_ptr(),
    ei.gen_HY1_b1.get_ptr(),
    ei.gen_HY1_b2.get_ptr(),
    ei.gen_HY2_b1.get_ptr(),
    ei.gen_HY2_b2.get_ptr()
  };

  std::vector<int> genjet_idxs;

  std::vector<GenJet> genjets;
  for (unsigned int igj = 0; igj < *(nat.nGenJet); ++igj){
    GenJet gj (igj, &nat);
    genjets.push_back(gj);
  }

  for (GenPart* b : bs_to_match){
    std::vector<std::tuple<double, int, int>> matched_gj; // dR, idx in nanoAOD, idx in local coll
    for (unsigned int igj = 0; igj < genjets.size(); ++igj){
      GenJet& gj = genjets.at(igj);
      double dR = ROOT::Math::VectorUtil::DeltaR(b->P4(), gj.P4());
      if (dR < dR_match)
	matched_gj.push_back(std::make_tuple(dR, gj.getIdx(), igj)); // save the idx in the nanoAOD collection to rebuild this after 
									  }
        
    if (matched_gj.size() > 0){
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
  if (genjet_idxs.at(0) >= 0) ei.gen_HX_b1_genjet  = GenJet(genjet_idxs.at(0), &nat);
  if (genjet_idxs.at(1) >= 0) ei.gen_HX_b2_genjet  = GenJet(genjet_idxs.at(1), &nat);
  if (genjet_idxs.at(2) >= 0) ei.gen_HY1_b1_genjet = GenJet(genjet_idxs.at(2), &nat);
  if (genjet_idxs.at(3) >= 0) ei.gen_HY1_b2_genjet = GenJet(genjet_idxs.at(3), &nat);
  if (genjet_idxs.at(4) >= 0) ei.gen_HY2_b1_genjet = GenJet(genjet_idxs.at(4), &nat);
  if (genjet_idxs.at(5) >= 0) ei.gen_HY2_b2_genjet = GenJet(genjet_idxs.at(5), &nat);

  return;
}

void SixB_functions::match_genbs_genjets_to_reco(NanoAODTree& nat, EventInfo& ei)
{
  int ij_gen_HX_b1_genjet  = (ei.gen_HX_b1_genjet  ? find_jet_from_genjet(nat, *ei.gen_HX_b1_genjet)  : -1); 
  int ij_gen_HX_b2_genjet  = (ei.gen_HX_b2_genjet  ? find_jet_from_genjet(nat, *ei.gen_HX_b2_genjet)  : -1); 
  int ij_gen_HY1_b1_genjet = (ei.gen_HY1_b1_genjet ? find_jet_from_genjet(nat, *ei.gen_HY1_b1_genjet) : -1); 
  int ij_gen_HY1_b2_genjet = (ei.gen_HY1_b2_genjet ? find_jet_from_genjet(nat, *ei.gen_HY1_b2_genjet) : -1); 
  int ij_gen_HY2_b1_genjet = (ei.gen_HY2_b1_genjet ? find_jet_from_genjet(nat, *ei.gen_HY2_b1_genjet) : -1); 
  int ij_gen_HY2_b2_genjet = (ei.gen_HY2_b2_genjet ? find_jet_from_genjet(nat, *ei.gen_HY2_b2_genjet) : -1); 

  if (ij_gen_HX_b1_genjet >= 0)  ei.gen_HX_b1_recojet  = Jet(ij_gen_HX_b1_genjet,  &nat);
  if (ij_gen_HX_b2_genjet >= 0)  ei.gen_HX_b2_recojet  = Jet(ij_gen_HX_b2_genjet,  &nat);
  if (ij_gen_HY1_b1_genjet >= 0) ei.gen_HY1_b1_recojet = Jet(ij_gen_HY1_b1_genjet, &nat);
  if (ij_gen_HY1_b2_genjet >= 0) ei.gen_HY1_b2_recojet = Jet(ij_gen_HY1_b2_genjet, &nat);
  if (ij_gen_HY2_b1_genjet >= 0) ei.gen_HY2_b1_recojet = Jet(ij_gen_HY2_b1_genjet, &nat);
  if (ij_gen_HY2_b2_genjet >= 0) ei.gen_HY2_b2_recojet = Jet(ij_gen_HY2_b2_genjet, &nat);

  // select unique occurences in vector
  // note : PAT tools already ensure that match is unique
  // https://github.com/cms-sw/cmssw/blob/master/PhysicsTools/PatAlgos/python/mcMatchLayer0/jetMatch_cfi.py
  // so the check below is redundant

  // std::vector<int> imatchs;
  // if (ij_gen_HX_b1_genjet >= 0)  imatchs.push_back(ij_gen_HX_b1_genjet);
  // if (ij_gen_HX_b2_genjet >= 0)  imatchs.push_back(ij_gen_HX_b2_genjet);
  // if (ij_gen_HY1_b1_genjet >= 0) imatchs.push_back(ij_gen_HY1_b1_genjet);
  // if (ij_gen_HY1_b2_genjet >= 0) imatchs.push_back(ij_gen_HY1_b2_genjet);
  // if (ij_gen_HY2_b1_genjet >= 0) imatchs.push_back(ij_gen_HY2_b1_genjet);
  // if (ij_gen_HY2_b2_genjet >= 0) imatchs.push_back(ij_gen_HY2_b2_genjet);

  // sort(imatchs.begin(), imatchs.end());
  // imatchs.erase(unique (imatchs.begin(), imatchs.end()), imatchs.end());
  // ei.gen_bs_N_reco_match = imatchs.size(); // number of different reco jets that are matched to gen jets

  int nmatched = 0;
  if (ij_gen_HX_b1_genjet >= 0)  nmatched += 1;
  if (ij_gen_HX_b2_genjet >= 0)  nmatched += 1;
  if (ij_gen_HY1_b1_genjet >= 0) nmatched += 1;
  if (ij_gen_HY1_b2_genjet >= 0) nmatched += 1;
  if (ij_gen_HY2_b1_genjet >= 0) nmatched += 1;
  if (ij_gen_HY2_b2_genjet >= 0) nmatched += 1;
  ei.gen_bs_N_reco_match = nmatched;

  // same as above, but apply acceptance cuts on the matched jets
  int nmatched_acc = 0;
  if (ei.gen_HX_b1_recojet  && ei.gen_HX_b1_recojet->P4().Pt()  > 20 && std::abs(ei.gen_HX_b1_recojet->P4().Eta())  < 4.8) nmatched_acc += 1;
  if (ei.gen_HX_b2_recojet  && ei.gen_HX_b2_recojet->P4().Pt()  > 20 && std::abs(ei.gen_HX_b2_recojet->P4().Eta())  < 4.8) nmatched_acc += 1;
  if (ei.gen_HY1_b1_recojet && ei.gen_HY1_b1_recojet->P4().Pt() > 20 && std::abs(ei.gen_HY1_b1_recojet->P4().Eta()) < 4.8) nmatched_acc += 1;
  if (ei.gen_HY1_b2_recojet && ei.gen_HY1_b2_recojet->P4().Pt() > 20 && std::abs(ei.gen_HY1_b2_recojet->P4().Eta()) < 4.8) nmatched_acc += 1;
  if (ei.gen_HY2_b1_recojet && ei.gen_HY2_b1_recojet->P4().Pt() > 20 && std::abs(ei.gen_HY2_b1_recojet->P4().Eta()) < 4.8) nmatched_acc += 1;
  if (ei.gen_HY2_b2_recojet && ei.gen_HY2_b2_recojet->P4().Pt() > 20 && std::abs(ei.gen_HY2_b2_recojet->P4().Eta()) < 4.8) nmatched_acc += 1;
  ei.gen_bs_N_reco_match_in_acc = nmatched_acc;

  // now compute p4 sums to make the invariant mass of X - FIXME: can add more inv masses for the various cases
  p4_t p4_sum_matched (0,0,0,0);
  if (ei.gen_HX_b1_recojet) p4_sum_matched  += ei.gen_HX_b1_recojet->P4();
  if (ei.gen_HX_b2_recojet) p4_sum_matched  += ei.gen_HX_b2_recojet->P4();
  if (ei.gen_HY1_b1_recojet) p4_sum_matched += ei.gen_HY1_b1_recojet->P4();
  if (ei.gen_HY1_b2_recojet) p4_sum_matched += ei.gen_HY1_b2_recojet->P4();
  if (ei.gen_HY2_b1_recojet) p4_sum_matched += ei.gen_HY2_b1_recojet->P4();
  if (ei.gen_HY2_b2_recojet) p4_sum_matched += ei.gen_HY2_b2_recojet->P4();
  ei.gen_bs_match_recojet_minv = p4_sum_matched.M();

  p4_t p4_sum_matched_acc (0,0,0,0);
  if (ei.gen_HX_b1_recojet  && ei.gen_HX_b1_recojet->P4().Pt()  > 20 && std::abs(ei.gen_HX_b1_recojet->P4().Eta())  < 4.8) p4_sum_matched_acc += ei.gen_HX_b1_recojet->P4();
  if (ei.gen_HX_b2_recojet  && ei.gen_HX_b2_recojet->P4().Pt()  > 20 && std::abs(ei.gen_HX_b2_recojet->P4().Eta())  < 4.8) p4_sum_matched_acc += ei.gen_HX_b2_recojet->P4();
  if (ei.gen_HY1_b1_recojet && ei.gen_HY1_b1_recojet->P4().Pt() > 20 && std::abs(ei.gen_HY1_b1_recojet->P4().Eta()) < 4.8) p4_sum_matched_acc += ei.gen_HY1_b1_recojet->P4();
  if (ei.gen_HY1_b2_recojet && ei.gen_HY1_b2_recojet->P4().Pt() > 20 && std::abs(ei.gen_HY1_b2_recojet->P4().Eta()) < 4.8) p4_sum_matched_acc += ei.gen_HY1_b2_recojet->P4();
  if (ei.gen_HY2_b1_recojet && ei.gen_HY2_b1_recojet->P4().Pt() > 20 && std::abs(ei.gen_HY2_b1_recojet->P4().Eta()) < 4.8) p4_sum_matched_acc += ei.gen_HY2_b1_recojet->P4();
  if (ei.gen_HY2_b2_recojet && ei.gen_HY2_b2_recojet->P4().Pt() > 20 && std::abs(ei.gen_HY2_b2_recojet->P4().Eta()) < 4.8) p4_sum_matched_acc += ei.gen_HY2_b2_recojet->P4();
  ei.gen_bs_match_in_acc_recojet_minv = p4_sum_matched_acc.M();
}

int SixB_functions::find_jet_from_genjet (NanoAODTree& nat, const GenJet& gj)
{
  const int gjidx = gj.getIdx();
  for (unsigned int ij = 0; ij < *(nat.nJet); ++ij){
    Jet jet (ij, &nat);
    int igj = get_property(jet, Jet_genJetIdx);
    if (igj == gjidx)
      return ij;
  }
  return -1;
}

void SixB_functions::match_genjets_to_reco(std::vector<GenJet>& genjets,std::vector<Jet>& recojets)
{
  
  for (unsigned int ireco = 0; ireco < recojets.size(); ireco++)
    {
      Jet& jet = recojets.at(ireco);
      int gen_match = -1;
      for (unsigned int igen = 0; igen < genjets.size(); igen++)
	{
	  GenJet& genjet = genjets.at(igen);
			
	  if (genjet.getIdx() == get_property(jet,Jet_genJetIdx))
	    {
	      gen_match = igen;
	      break;
	    }
      
	}
      if (gen_match != -1) {
	recojets.at(ireco).set_genIdx(gen_match);
	genjets.at(gen_match).set_recoIdx(ireco);
      }
    }
}

std::vector<GenJet> SixB_functions::get_all_genjets(NanoAODTree& nat)
{
  std::vector<GenJet> jets;
  jets.reserve(*(nat.nGenJet));
    
  for (unsigned int ij = 0; ij < *(nat.nGenJet); ++ij){
    GenJet jet (ij, &nat);
    jets.emplace_back(jet);
  }
  return jets;
}

std::vector<Jet> SixB_functions::get_all_jets(NanoAODTree& nat)
{
  std::vector<Jet> jets;
  jets.reserve(*(nat.nJet));
    
  for (unsigned int ij = 0; ij < *(nat.nJet); ++ij){
    Jet jet (ij, &nat);
    jets.emplace_back(jet);
  }
  return jets;
}

std::vector<Jet> SixB_functions::preselect_jets(NanoAODTree& nat, const std::vector<Jet>& in_jets)
{
  // FIXME: make these selections configurable
  const double pt_min  = 20.;
  const double eta_max = 2.5;
  // const double btag_min = btag_WPs.at(0);
  const int    pf_id   = 1;
  const int    pu_id   = 1;

  std::vector<Jet> out_jets;
  out_jets.reserve(in_jets.size());

  for (unsigned int ij = 0; ij < in_jets.size(); ++ij)
    {
      const Jet& jet = in_jets.at(ij);
      if (jet.get_pt()            <= pt_min)  continue;
      if (std::abs(jet.get_eta()) >= eta_max) continue;
      // if (jet.get_btag() <= btag_min) continue;
      if (!checkBit(jet.get_id(), pf_id)) continue;
      if (!checkBit(jet.get_puid(),  pu_id)) continue;

      out_jets.emplace_back(jet);
    }

  return out_jets;
}

std::vector<Jet> SixB_functions::select_sixb_jets(NanoAODTree& nat, const std::vector<Jet>& in_jets)
{
  std::vector<Jet> jets = in_jets;
  stable_sort(jets.begin(), jets.end(), [](const Jet& a, const Jet& b) -> bool {
    return ( get_property (a, Jet_btagDeepFlavB) > get_property (b, Jet_btagDeepFlavB) ); }
    ); // sort jet by deepjet score (highest to lowest)

  int n_out = std::min<int>(jets.size(), 6);
  jets.resize(n_out);

  // for (auto& jet : jets)
  //     std::cout << jet.P4().Pt() << " " << get_property (jet, Jet_btagDeepFlavB) << std::endl;
  // std::cout << std::endl << std::endl;

  return jets;
}

std::vector<Jet> SixB_functions::select_ttbar_jets(NanoAODTree &nat, EventInfo &ei, const std::vector<Jet> &in_jets)
{
  std::vector<Jet> jets = in_jets;
  stable_sort(jets.begin(), jets.end(), [](const Jet& a, const Jet& b) -> bool {
    return ( get_property (a, Jet_btagDeepFlavB) > get_property (b, Jet_btagDeepFlavB) ); }
    ); // sort jet by deepjet score (highest to lowest)

  if (jets.size() < 2)
    return jets;
  ei.bjet1 = jets.at(0);
  ei.bjet2 = jets.at(1);
  if (ei.bjet1->P4().Pt() < ei.bjet2->P4().Pt()) // sort by pt
    std::swap(ei.bjet1, ei.bjet2);

  return jets;

  // int n_out = std::min<int>(jets.size(), 6);
  // jets.resize(n_out);

  // for (auto& jet : jets)
  //     std::cout << jet.P4().Pt() << " " << get_property (jet, Jet_btagDeepFlavB) << std::endl;
  // std::cout << std::endl << std::endl;

  // return jets;

}


std::vector<int> SixB_functions::match_local_idx(std::vector<Jet>& subset,std::vector<Jet>& supset)
{
  std::vector<int> local_idxs;
	
  for (unsigned int i = 0; i < subset.size(); i++)
    {
      const Jet& obj = subset.at(i);
      int local_idx = -1;
      for (unsigned int j = 0; j < supset.size(); j++)
	{
	  const Jet& com = supset.at(j);
	  if ( obj.getIdx() == com.getIdx() ) {
	    local_idx = j;
	    break;
	  }
	}
      local_idxs.push_back(local_idx);
    }
  return local_idxs;
}

void SixB_functions::btag_bias_pt_sort(std::vector<Jet>& in_jets)
{
  std::sort(in_jets.begin(),in_jets.end(),[](Jet& j1,Jet& j2){ return j1.get_btag()>j2.get_btag(); });

  auto loose_it = std::find_if(in_jets.rbegin(),in_jets.rend(),[this](Jet& j){ return j.get_btag()>this->btag_WPs[0]; });
  auto medium_it= std::find_if(in_jets.rbegin(),in_jets.rend(),[this](Jet& j){ return j.get_btag()>this->btag_WPs[1]; });
  auto tight_it = std::find_if(in_jets.rbegin(),in_jets.rend(),[this](Jet& j){ return j.get_btag()>this->btag_WPs[2]; });

  auto pt_sort = [](Jet& j1,Jet& j2) { return j1.get_pt()>j2.get_pt(); };

  int tight_idx = std::distance(in_jets.begin(),tight_it.base())-1;
  int medium_idx = std::distance(in_jets.begin(),medium_it.base())-1;
  int loose_idx = std::distance(in_jets.begin(),loose_it.base())-1;

  std::vector<int> wp_idxs = {tight_idx,medium_idx,loose_idx};
  auto start = in_jets.begin();
  for (int wp_idx : wp_idxs)
    {
      if (wp_idx != -1 && start != in_jets.end()) {
	auto end = in_jets.begin() + wp_idx + 1;
	std::sort(start,end,pt_sort);
	start = end;
      }
    }
}

void SixB_functions::pt_sort(std::vector<Jet>& in_jets)
{
  std::sort(in_jets.begin(),in_jets.end(),[](Jet& j1,Jet& j2){ return j1.get_pt()>j2.get_pt(); });
}

bool SixB_functions::pass_jet_cut(Cutflow& cutflow,const std::vector<double> pt_cuts,const std::vector<int> btagWP_cuts,const std::vector<Jet> &in_jets)
{
  std::vector<std::string> wplabels = {"loose","medium","tight"};
	
  unsigned int ncuts = pt_cuts.size();

  if ( in_jets.size() < ncuts ) return false;
	
  for (unsigned int icut = 0; icut < ncuts; icut++)
    {
      const Jet& ijet = in_jets[icut];

      double pt = pt_cuts[icut];
      int btag_wp = btagWP_cuts[icut];

      if ( ijet.get_pt() <= pt || ijet.get_btag() <= btag_WPs[btag_wp] )
	return false;
		
      cutflow.add( "jet" + std::to_string(icut) + "_pt" + std::to_string( (int)pt ) + "_" + wplabels[btag_wp]  );
    }
  return true;
}

std::vector<DiJet> pair_best_higgs_method(std::vector<Jet>& in_jets)
{
  std::vector<DiJet> higgs_list;
	
  for (unsigned int i = 0; i < in_jets.size(); i++)
    {
      if (higgs_list.size() == 3) break;
		
      Jet& j1 = in_jets[i];
      if (j1.get_higgsId() != -1) continue;

      std::vector<std::pair<int,DiJet>> dijet_pairs;
      for (unsigned int k = i+1; k < in_jets.size(); k++)
	{
	  Jet& j2 = in_jets[k];
	  if (j2.get_higgsId() != -1) continue;
			
	  DiJet dijet(j1,j2);
	  dijet_pairs.push_back( std::make_pair(k,dijet) );
	}
      if (dijet_pairs.size() == 0) continue;
      std::sort(dijet_pairs.begin(),dijet_pairs.end(),[](auto di1,auto di2){ return fabs(di1.second.M()-125)<fabs(di2.second.M()-125); });
		
      int pair_idx = dijet_pairs[0].first;
      DiJet& higgs_p4 = dijet_pairs[0].second;
      Jet& j2 = in_jets[pair_idx];
				  
      j1.set_nn_higgsId( higgs_list.size() );
      j2.set_nn_higgsId( higgs_list.size() );
      higgs_list.push_back(higgs_p4);
    }
  return higgs_list;
}


std::vector<DiJet> SixB_functions::get_tri_higgs_D_HHH(std::vector<Jet>& in_jets)
{

  // Optimial 3D Line to select most signal like higgs
  const float phi = 0.77;
  const float theta = 0.98;
  const ROOT::Math::Polar3DVectorF r_vec(1,theta,phi);
	
  std::vector<DiJet> dijets;
  for (const std::vector<int> ijets : dijet_pairings)
    { 
      int ij1 = ijets[0]; int ij2 = ijets[1];
      DiJet dijet(in_jets[ij1],in_jets[ij2]);
      dijets.push_back( dijet );
    }
	
  std::vector< std::pair<float,int> > triH_d_hhh;
  for (unsigned int i = 0; i < triH_pairings.size(); i++)
    {
      std::vector<DiJet> tri_dijet_sys;
      for (int id : triH_pairings[i]) tri_dijet_sys.push_back( dijets[id] );
      std::sort(tri_dijet_sys.begin(),tri_dijet_sys.end(),[](DiJet& dj1,DiJet& dj2){ return dj1.Pt()>dj2.Pt(); });
		
      ROOT::Math::XYZVectorF m_vec(tri_dijet_sys[0].M(),tri_dijet_sys[1].M(),tri_dijet_sys[2].M());
      float d_hhh = m_vec.Cross(r_vec).R();
      triH_d_hhh.push_back( std::make_pair(d_hhh,i) );
    }

  // Choose the closest triH vector to the r_vec line
  std::sort(triH_d_hhh.begin(),triH_d_hhh.end(),[](std::pair<float,int> h1,std::pair<float,int> h2){ return h1.first<h2.first; });

  int itriH = triH_d_hhh[0].second;
  std::vector<int> idijets = triH_pairings[itriH];

  // Order dijets by highest Pt
  std::sort(idijets.begin(),idijets.end(),[dijets](int id1,int id2){ return dijets[id1].Pt() > dijets[id2].Pt(); });
  std::vector<DiJet> higgs_list;
	
  for (unsigned int i = 0; i < idijets.size(); i++)
    {
      int id = idijets[i];
      for (int ij : dijet_pairings[id])
	{
	  Jet& jet = in_jets[ij];
	  jet.set_higgsId(i);
	}
		
      DiJet dijet = dijets[id];

      higgs_list.push_back(dijet);
    }
	
  return higgs_list;
}

std::vector<std::vector<int>> get_6jet_index_combos(int n,int r=6)
{
  std::vector<std::vector<int>> index_combos;
	
  std::vector<bool> v(n);
  std::fill(v.end() - r, v.end(), true);
	
  do {
    std::vector<int> combo;
    for (int i = 0; i < n; ++i) {
      if (v[i]) {
	combo.push_back(i);
      }
    }
    index_combos.push_back(combo);
  } while (std::next_permutation(v.begin(), v.end()));
  return index_combos;
}

std::vector<float> build_6jet_classifier_input(const std::vector<Jet>& in_jets,std::vector<int>& indices)
{
  std::vector<float> input_array;
	
  std::vector<std::vector<float>> input_matrix;
  std::sort(indices.begin(),indices.end(),[in_jets](int i1,int i2){ return in_jets[i1].get_pt()>in_jets[i2].get_pt(); });

  int nvar = 5;
  for (int i = 0; i < nvar; i++) input_matrix.push_back(std::vector<float>());
	
  p4_t com = in_jets[indices[0]].P4Regressed() + in_jets[indices[1]].P4Regressed() + in_jets[indices[2]].P4Regressed() + in_jets[indices[3]].P4Regressed() + in_jets[indices[4]].P4Regressed() + in_jets[indices[5]].P4Regressed();

  for (int ij : indices)
    {
      input_matrix[0].push_back( in_jets[ij].get_pt() );
      input_matrix[1].push_back( in_jets[ij].get_eta() );
      input_matrix[2].push_back( in_jets[ij].get_phi() );
      input_matrix[3].push_back( in_jets[ij].get_btag() );
      input_matrix[4].push_back( (in_jets[ij].P4Regressed() - com).Pt() );
    }

  for ( std::vector<float> input : input_matrix ) input_array.insert(input_array.end(),input.begin(),input.end());

  return input_array;
}

std::vector<Jet> SixB_functions::get_6jet_NN(EventInfo& ei,std::vector<Jet>& in_jets,EvalNN& n_6j_classifier)
{
  std::vector<Jet> b_jets;
	
  std::vector<std::vector<int>> index_combos = get_6jet_index_combos(in_jets.size());
	
  std::vector< std::pair<float,std::vector<int>> > n_6j_scores;
  for (std::vector<int> combo : index_combos)
    {
      std::vector<float> input = build_6jet_classifier_input(in_jets,combo);
      float score = n_6j_classifier.evaluate(input)[0];
      n_6j_scores.push_back( std::make_pair(-score,combo) );
    }
  std::sort(n_6j_scores.begin(),n_6j_scores.end());
  float b_6j_score = -n_6j_scores[0].first;
  std::vector<int> b_index_combo = n_6j_scores[0].second;

  ei.b_6j_score = b_6j_score;
	
  for (int ij : b_index_combo) b_jets.push_back( in_jets[ij] );
	
  return b_jets;
}


std::vector<float> build_2jet_classifier_input(const std::vector<Jet>& in_jets,std::vector<int>& indices)
{
  std::vector<float> input_array;
	
  std::vector<std::vector<float>> input_matrix;
  
  std::sort(indices.begin(),indices.end(),[in_jets](int i1,int i2){ return in_jets[i1].get_pt()>in_jets[i2].get_pt(); });

  int nvar = 5;
  for (int i = 0; i < nvar; i++) input_matrix.push_back(std::vector<float>());

  for (int ij : indices)
    {
      input_matrix[0].push_back( in_jets[ij].get_pt() );
      input_matrix[1].push_back( in_jets[ij].get_eta() );
      input_matrix[2].push_back( in_jets[ij].get_phi() );
      input_matrix[3].push_back( in_jets[ij].get_btag() );
    }

  float dr = ROOT::Math::VectorUtil::DeltaR( in_jets[indices[0]].P4Regressed(),in_jets[indices[1]].P4Regressed() );
  input_matrix[4].push_back( dr );

  for ( std::vector<float> input : input_matrix ) input_array.insert(input_array.end(),input.begin(),input.end());

  return input_array;
}


std::vector<DiJet> SixB_functions::get_2jet_NN(EventInfo& ei,std::vector<Jet>& in_jets,std::vector<Jet>& sup_jets,EvalNN& n_2j_classifier)
{
  std::vector<int> sup_index = match_local_idx(in_jets,sup_jets);
	
  std::vector<DiJet> b_dijets;
	
  std::vector<float> n_2j_scores;
  for (std::vector<int> combo : dijet_pairings)
    {
      std::vector<float> input = build_2jet_classifier_input(in_jets,combo);
      float score = n_2j_classifier.evaluate(input)[0];
      n_2j_scores.push_back(score);
    }

  std::vector< std::pair<float,std::vector<int>> > triH_scores;
  for (std::vector<int> combo : triH_pairings)
    {
      float score = 0;
      for (int i : combo) score += n_2j_scores[i]*n_2j_scores[i];
      score = sqrt(score/3);
      triH_scores.push_back( std::make_pair(-score,combo) );
    }
  std::sort(triH_scores.begin(),triH_scores.end());
  std::vector<int> b_index_combo = triH_scores[0].second;
  
  float b_3h_score = -triH_scores[0].first;
  std::vector<float> b_2j_scores;
  for (int i : b_index_combo) b_2j_scores.push_back(n_2j_scores[i]);

  ei.b_3h_score = b_3h_score;

  for (int ih = 0; ih < 3; ih++)
    {
      int id = b_index_combo[ih];
      std::vector<int> ijs = dijet_pairings[id];
      Jet& j1 = sup_jets[ sup_index[ijs[0]] ]; Jet& j2 = sup_jets[ sup_index[ijs[1]] ];

      j1.set_nn_higgsId(ih);
      j2.set_nn_higgsId(ih);
		
      DiJet dijet(j1,j2);

      dijet.set_2j_score(n_2j_scores[id]);
      b_dijets.push_back(dijet);
    }
  std::sort(b_dijets.begin(),b_dijets.end(),[](DiJet& d1,DiJet& d2){ return d1.Pt()>d2.Pt(); });
	
  return b_dijets;
}

std::vector<DiJet> SixB_functions::get_tri_higgs_NN(EventInfo& ei,std::vector<Jet>& in_jets,EvalNN& n_6j_classifier,EvalNN& n_2j_classifier)
{
  std::vector<DiJet> higgs_list;

  std::vector<Jet> b_jets = get_6jet_NN(ei,in_jets,n_6j_classifier);
  higgs_list = get_2jet_NN(ei,b_jets,in_jets,n_2j_classifier);
	
  return higgs_list;
}


bool SixB_functions::pass_higgs_cr(const std::vector<DiJet>& in_dijets)
{
  //
	
  float higgs_mass = 125;
  float mass_sideband = 30;
	
  for (DiJet dijet : in_dijets)
    if ( fabs(dijet.M() - higgs_mass) <= mass_sideband )
      return false;
	
  return true;
}


void SixB_functions::pair_jets(NanoAODTree& nat, EventInfo& ei, const std::vector<Jet>& in_jets)
{
  // FIXME: here a switch for the pairing algo
  const std::string pairAlgo = "passthrough";

  // call the desired algo - expected interface is input jets -> output 3 composite candidate HX, HY1. HY2
  // the order of HY1, HY2 and of the jets does not matter - they will be reordered after

  std::tuple<CompositeCandidate, CompositeCandidate, CompositeCandidate> reco_Hs;
  if (pairAlgo == "passthrough")
    reco_Hs = pair_passthrough(in_jets);

  // reorder objects
  CompositeCandidate HX  = std::get<0>(reco_Hs);
  CompositeCandidate HY1 = std::get<1>(reco_Hs);
  CompositeCandidate HY2 = std::get<2>(reco_Hs);

  if (HY1.P4().Pt() < HY2.P4().Pt())
    std::swap(HY1, HY2);

  if (HX.getComponent1().P4().Pt() < HX.getComponent2().P4().Pt())
    HX.swapComponents();

  if (HY1.getComponent1().P4().Pt() < HY1.getComponent2().P4().Pt())
    HY1.swapComponents();

  if (HY2.getComponent1().P4().Pt() < HY2.getComponent2().P4().Pt())
    HY2.swapComponents();

  CompositeCandidate Y(HY1, HY2);
  CompositeCandidate X(Y, HX);

  ei.X = X;
  ei.Y = Y;

  ei.HX  = HX;
  ei.HY1 = HY1;
  ei.HY2 = HY2;

  ei.HX_b1  = static_cast<Jet&>(HX.getComponent1());
  ei.HX_b2  = static_cast<Jet&>(HX.getComponent2());
    
  ei.HY1_b1 = static_cast<Jet&>(HY1.getComponent1());
  ei.HY1_b2 = static_cast<Jet&>(HY1.getComponent2());
    
  ei.HY2_b1 = static_cast<Jet&>(HY2.getComponent1());
  ei.HY2_b2 = static_cast<Jet&>(HY2.getComponent2());

}

std::tuple<CompositeCandidate, CompositeCandidate, CompositeCandidate> SixB_functions::pair_passthrough (std::vector<Jet> jets)
{
  if (jets.size() != 6)
    throw std::runtime_error("The jet pairing -passthrough- function requires 6 jets");

  CompositeCandidate HX  (jets.at(0), jets.at(1));
  CompositeCandidate HY1 (jets.at(2), jets.at(3));
  CompositeCandidate HY2 (jets.at(4), jets.at(5));

  return std::make_tuple(HX, HY1, HY2);
}

int SixB_functions::n_gjmatched_in_jetcoll(NanoAODTree& nat, EventInfo& ei, const std::vector<Jet>& in_jets)
{
  std::vector<int> matched_jets;
  if (ei.gen_HX_b1_recojet)  matched_jets.push_back(ei.gen_HX_b1_recojet->getIdx());
  if (ei.gen_HX_b2_recojet)  matched_jets.push_back(ei.gen_HX_b2_recojet->getIdx());
  if (ei.gen_HY1_b1_recojet) matched_jets.push_back(ei.gen_HY1_b1_recojet->getIdx());
  if (ei.gen_HY1_b2_recojet) matched_jets.push_back(ei.gen_HY1_b2_recojet->getIdx());
  if (ei.gen_HY2_b1_recojet) matched_jets.push_back(ei.gen_HY2_b1_recojet->getIdx());
  if (ei.gen_HY2_b2_recojet) matched_jets.push_back(ei.gen_HY2_b2_recojet->getIdx());

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

void SixB_functions::match_signal_genjets(EventInfo& ei, std::vector<GenJet>& in_jets)
{
  std::vector<int> matched_jets = {-1,-1,-1,-1,-1,-1};
  if (ei.gen_HX_b1_genjet)  matched_jets[0] = ei.gen_HX_b1_genjet->getIdx();
  if (ei.gen_HX_b2_genjet)  matched_jets[1] = ei.gen_HX_b2_genjet->getIdx();
  if (ei.gen_HY1_b1_genjet) matched_jets[2] = ei.gen_HY1_b1_genjet->getIdx();
  if (ei.gen_HY1_b2_genjet) matched_jets[3] = ei.gen_HY1_b2_genjet->getIdx();
  if (ei.gen_HY2_b1_genjet) matched_jets[4] = ei.gen_HY2_b1_genjet->getIdx();
  if (ei.gen_HY2_b2_genjet) matched_jets[5] = ei.gen_HY2_b2_genjet->getIdx();

  for (GenJet& gj : in_jets)
    {
      int gj_idx = gj.getIdx();
      if (gj_idx == -1) continue;
		
      for (int id = 0; id < 6; id++)
	{
	  if (matched_jets[id] == gj_idx)
	    {
	      gj.set_signalId(id);
	    }
	}
    }
}

void SixB_functions::match_signal_recojets(EventInfo& ei,std::vector<Jet>& in_jets)
{
  std::vector<int> matched_jets = {-1,-1,-1,-1,-1,-1};
  if (ei.gen_HX_b1_recojet)  matched_jets[0] = ei.gen_HX_b1_recojet->getIdx();
  if (ei.gen_HX_b2_recojet)  matched_jets[1] = ei.gen_HX_b2_recojet->getIdx();
  if (ei.gen_HY1_b1_recojet) matched_jets[2] = ei.gen_HY1_b1_recojet->getIdx();
  if (ei.gen_HY1_b2_recojet) matched_jets[3] = ei.gen_HY1_b2_recojet->getIdx();
  if (ei.gen_HY2_b1_recojet) matched_jets[4] = ei.gen_HY2_b1_recojet->getIdx();
  if (ei.gen_HY2_b2_recojet) matched_jets[5] = ei.gen_HY2_b2_recojet->getIdx();

  for (Jet& j : in_jets)
    {
      int j_idx = j.getIdx();
      if (j_idx == -1) continue;
		
      for (int id = 0; id < 6; id++)
	{
	  if (matched_jets[id] == j_idx)
	    {
	      j.set_signalId(id);
	    }
	}
    }
}

void SixB_functions::select_leptons(NanoAODTree &nat, EventInfo &ei)
{
  std::vector<Electron> electrons;
  std::vector<Muon> muons;

  for (unsigned int ie = 0; ie < *(nat.nElectron); ++ie){
    Electron ele (ie, &nat);
    electrons.emplace_back(ele);
  }

  for (unsigned int imu = 0; imu < *(nat.nMuon); ++imu){
    Muon mu(imu, &nat);
    muons.emplace_back(mu);
  }

  // apply preselections
  std::vector<Electron> loose_electrons;
  std::vector<Muon> loose_muons;

  // std::vector<Electron> tight_electrons;
  // std::vector<Muon> tight_muons;

  for (auto& el : electrons){

    float dxy    = get_property(el, Electron_dxy);
    float dz     = get_property(el, Electron_dz);
    float eta    = get_property(el, Electron_eta);
    float pt     = get_property(el, Electron_pt);
    bool ID_WPL  = get_property(el, Electron_mvaFall17V2Iso_WPL); 
    // bool ID_WP90 = get_property(el, Electron_mvaFall17V2Iso_WP90);
    // bool ID_WP80 = get_property(el, Electron_mvaFall17V2Iso_WP80);
    float iso    = get_property(el, Electron_pfRelIso03_all);

    // note: hardcoded selections can be made configurable from cfg if needed
    const float e_pt_min  = 15;
    const float e_eta_max = 2.5;
    const float e_iso_max = 0.15;
        
    const float e_dxy_max_barr = 0.05;
    const float e_dxy_max_endc = 0.10;
    const float e_dz_max_barr  = 0.10;
    const float e_dz_max_endc  = 0.20;

    bool is_barrel = abs(eta) < 1.479;
    bool pass_dxy  = (is_barrel ? dxy < e_dxy_max_barr : dxy < e_dxy_max_endc);
    bool pass_dz   = (is_barrel ? dz  < e_dz_max_barr  : dz  < e_dz_max_endc);

    // loose electrons for veto
    if (pt > e_pt_min        &&
	abs(eta) < e_eta_max &&
	iso < e_iso_max      &&
	pass_dxy             &&
	pass_dz              &&
	ID_WPL)
      loose_electrons.emplace_back(el);
  }

  for (auto& mu : muons){

    float dxy    = get_property(mu, Muon_dxy);
    float dz     = get_property(mu, Muon_dz);
    float eta    = get_property(mu, Muon_eta);
    float pt     = get_property(mu, Muon_pt);
    bool ID_WPL  = get_property(mu, Muon_looseId);
    // bool ID_WPM = get_property(mu, Muon_mediumId);
    // bool ID_WPT = get_property(mu, Muon_tightId);
    float iso    = get_property(mu, Muon_pfRelIso04_all);

    // note: hardcoded selections can be made configurable from cfg if needed
    const float mu_pt_min  = 10;
    const float mu_eta_max = 2.4;
    const float mu_iso_max = 0.15;
        
    const float mu_dxy_max_barr = 0.05;
    const float mu_dxy_max_endc = 0.10;
    const float mu_dz_max_barr  = 0.10;
    const float mu_dz_max_endc  = 0.20;

    bool is_barrel = abs(eta) < 1.2;
    bool pass_dxy  = (is_barrel ? dxy < mu_dxy_max_barr : dxy < mu_dxy_max_endc);
    bool pass_dz   = (is_barrel ? dz  < mu_dz_max_barr  : dz  < mu_dz_max_endc);

    // loose muons for veto
    if (pt > mu_pt_min        &&
	abs(eta) < mu_eta_max &&
	iso < mu_iso_max      &&
	pass_dxy              &&
	pass_dz               &&
	ID_WPL)
      loose_muons.emplace_back(mu);
  }

  // copy needed info to the EventInfo
  if (loose_muons.size() > 0) ei.mu_1 = loose_muons.at(0);
  if (loose_muons.size() > 1) ei.mu_2 = loose_muons.at(1);
  if (loose_electrons.size() > 0) ei.ele_1 = loose_electrons.at(0);
  if (loose_electrons.size() > 1) ei.ele_2 = loose_electrons.at(1);

  ei.n_mu_loose  = loose_muons.size();
  ei.n_ele_loose = loose_electrons.size();
  // ei.n_mu_tight  = tight_muons.size();
  // ei.n_ele_tight = tight_electrons.size();
}

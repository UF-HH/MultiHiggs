#include "Skim_functions.h"
#include "Math/VectorUtil.h"
#include "Math/Vector3D.h"
#include "Math/Functions.h"

// #include "DebugUtils.h"

#include <iostream>
#include <tuple>
#include <algorithm>

#include "Electron.h"
#include "Muon.h"

#include "TFile.h"
#include "TH2F.h"

using namespace std;

void Skim_functions::initialize_params_from_cfg(CfgParser &config)
{
  /**
   * @brief Initialize configuration for skim
   * Default sets preselection requirements from config
   * 
   */
  // preselections
  pmap.insert_param<bool>("presel", "apply", config.readBoolOpt("presel::apply"));
  pmap.insert_param<std::vector<double> >("presel", "pt_min", config.readDoubleListOpt("presel::pt_min"));
  pmap.insert_param<double>("presel", "eta_max", config.readDoubleOpt("presel::eta_max"));
  pmap.insert_param<int>("presel", "pf_id", config.readIntOpt("presel::pf_id"));
  pmap.insert_param<int>("presel", "pu_id", config.readIntOpt("presel::pu_id"));
}

void Skim_functions::copy_event_info(NanoAODTree &nat, EventInfo &ei, bool is_mc)
{
  /**
   * @brief Copy general event info to EventInfo
   * 
   */
  ei.Run = *(nat.run);
  ei.LumiSec = *(nat.luminosityBlock);
  ei.Event = *(nat.event);

  ei.n_other_pv = *(nat.nOtherPV);
  ei.rhofastjet_all = *(nat.fixedGridRhoFastjetAll);
  ei.n_total_jet = *(nat.nJet);

  // mc-only
  if (is_mc)
  {
    ei.n_pu = *(nat.Pileup_nPU);
    ei.n_true_int = *(nat.Pileup_nTrueInt);
    ei.n_genjet = *(nat.nGenJet);
    ei.lhe_ht = *(nat.LHE_HT);
  }
}

int Skim_functions::find_fatjet_from_genfatjet(NanoAODTree &nat, const GenJetAK8 &gj)
{
  /**
   * @brief Returns the index of the reco fatjet this gen fatjet is matched to
   *
   */
  const int gjidx = gj.getIdx();
  for (unsigned int ij = 0; ij < *(nat.nFatJet); ++ij)
    {
      FatJet fatjet(ij, &nat);
      int igj = get_property(fatjet, FatJet_genJetAK8Idx);
      if (0) std::cout << "Fat-jet with index="<<ij<<"  is related to gen-jet AK8 with index ="<<igj<<"    ("<<gjidx<<")"<<std::endl;
      if (igj == gjidx) return ij;
    }
  return -1;
}

int Skim_functions::find_jet_from_genjet(NanoAODTree &nat, const GenJet &gj)
{
  /**
   * @brief Returns the index of the recojet this genjet is matched to
   * 
   */
  const int gjidx = gj.getIdx();
  for (unsigned int ij = 0; ij < *(nat.nJet); ++ij)
  {
    Jet jet(ij, &nat);
    int igj = get_property(jet, Jet_genJetIdx);
    if (igj == gjidx)
      return ij;
  }
  return -1;
}

std::vector<SubGenJetAK8> Skim_functions::get_all_subgenjets(NanoAODTree &nat)
{
  /**
   * @brief Returns list of all gen subjets of AK8 in the event
   *
   */
  std::vector<SubGenJetAK8> subjets;
  subjets.reserve(*(nat.nSubGenJetAK8));
  for (unsigned int ij = 0; ij < *(nat.nSubGenJetAK8); ++ij)
    {
      SubGenJetAK8 subjet(ij, &nat);
      subjets.emplace_back(subjet);
    }
  return subjets;
}

std::vector<GenJetAK8> Skim_functions::get_all_genfatjets(NanoAODTree &nat)
{
  /**
   * @brief Returns list of all gen-fatjets in the event
   *
   */
  std::vector<GenJetAK8> fatjets;
  fatjets.reserve(*(nat.nGenJetAK8));
  for (unsigned int ij = 0; ij < *(nat.nGenJetAK8); ++ij)
    {
      GenJetAK8 fatjet(ij, &nat);
      fatjets.emplace_back(fatjet);
    }
  return fatjets;
}

std::vector<GenJet> Skim_functions::get_all_genjets(NanoAODTree &nat)
{
  /**
   * @brief Returns list of all genjets in the event
   * 
   */
  std::vector<GenJet> jets;
  jets.reserve(*(nat.nGenJet));

  for (unsigned int ij = 0; ij < *(nat.nGenJet); ++ij)
  {
    GenJet jet(ij, &nat);
    jets.emplace_back(jet);
  }
  return jets;
}

std::vector<FatJet> Skim_functions::get_all_fatjets(NanoAODTree &nat)
{
  /**
   * @brief Returns list of all reco fat-jets in the event
   *
   */
  std::vector<FatJet> fatjets;
  fatjets.reserve(*(nat.nFatJet));
  for (unsigned int ij = 0; ij < *(nat.nFatJet); ++ij)
    {
      FatJet fatjet(ij, &nat);
      fatjets.emplace_back(fatjet);
    }
  return fatjets;
}

std::vector<Jet> Skim_functions::get_all_jets(NanoAODTree &nat)
{
  /**
   * @brief Returns list of all recojets in the event
   * 
   */
  std::vector<Jet> jets;
  jets.reserve(*(nat.nJet));

  for (unsigned int ij = 0; ij < *(nat.nJet); ++ij)
  {
    Jet jet(ij, &nat);
    jets.emplace_back(jet);
  }
  return jets;
}

std::vector<Jet> Skim_functions::preselect_jets(NanoAODTree &nat, EventInfo& ei, const std::vector<Jet> &in_jets)
{
  /**
   * @brief Selects jets from in_jets according to preselections defined in config
   * 
   * @return skimmed jet list
   */
  const bool apply = pmap.get_param<bool>("presel","apply");
  if (!apply) return in_jets;
  
  const std::vector<double> pt_cuts = pmap.get_param<std::vector<double> >("presel", "pt_min");
  const double eta_max = pmap.get_param<double>("presel", "eta_max");
  const int pf_id = pmap.get_param<int>("presel", "pf_id");
  const int pu_id = pmap.get_param<int>("presel", "pu_id");
  
  std::vector<Jet> out_jets;
  out_jets.reserve(in_jets.size());
  
  unsigned int ptCut_index = 0;
  
  // Jets need to be sorted by pT in descending order before applying different pT cuts
  std::vector<Jet> jets_sortedInPt = pt_sort_jets(nat, ei, in_jets);
  
  for (unsigned int ij=0; ij<jets_sortedInPt.size(); ++ij)
    {
      const Jet &jet = jets_sortedInPt.at(ij);
      
      if (0) std::cout << " jet "<<ij<<"  pt="<<jet.P4().Pt()<<"   pt cut ="<<pt_cuts.at(ptCut_index)<<std::endl;
      
      if (jet.P4().Pt() <= pt_cuts.at(ptCut_index))
	continue;
      if (std::abs(jet.P4().Eta()) >= eta_max)
	continue;
      if (!checkBit(jet.get_id(), pf_id))
	continue;
      if (jet.P4().Pt() < 50 && !checkBit(jet.get_puid(), pu_id))
	continue; // PU ID only applies to jet with pT < 50 GeV
      
      out_jets.emplace_back(jet);
      
      // Increment cut index only
      if (ptCut_index < pt_cuts.size()-1) ptCut_index++;
    }
  return out_jets;
}

std::vector<Jet> Skim_functions::btag_sort_jets(NanoAODTree &nat, EventInfo& ei, const std::vector<Jet> &in_jets)
{
  std::vector<Jet> jets = in_jets;
  std::sort(jets.begin(),jets.end(),[](Jet& j1,Jet& j2){ return j1.get_btag()>j2.get_btag(); });
  return jets;
}

std::vector<Jet> Skim_functions::pt_sort_jets(NanoAODTree &nat, EventInfo& ei, const std::vector<Jet> &in_jets)
{
  std::vector<Jet> jets = in_jets;
  std::sort(jets.begin(),jets.end(),[](Jet& j1,Jet& j2){ return j1.get_pt()>j2.get_pt(); });
  return jets;
}

std::vector<Jet> Skim_functions::bias_pt_sort_jets(NanoAODTree &nat, EventInfo& ei, const std::vector<Jet> &in_jets)
{
  std::vector<Jet> jets = in_jets;
  
  // For debugging
  if (0)
    {
      std::cout << "Input jet collection should be sorted by pT (only) in descending order"<<std::endl;
      for (unsigned int ij=0; ij<in_jets.size(); ij++)
	{
	  const Jet j = in_jets.at(ij);
	  std::cout<<" jet "<< ij <<"  pt = "<< j.get_pt() <<"   b-disc="<< j.get_btag()<<std::endl;
	}
    }
  
  // Sort jets by their b-tagging score in descending order
  std::sort(jets.begin(),jets.end(),[](Jet& j1,Jet& j2){ return j1.get_btag()>j2.get_btag(); });
  
  // For debugging
  if (0)
    {
      std::cout << "Jets are now sorted by b-tagging score (only) in descending order"<<std::endl;
      for (unsigned int ij=0; ij<jets.size(); ij++)
	{
	  std::cout << "  jet "<<ij<<"  pt = "<<jets.at(ij).get_pt()<<"   b-disc="<<jets.at(ij).get_btag()<<std::endl;
	}
    }
  
  auto fail_it  = std::find_if(jets.rbegin(),jets.rend(),[this](Jet& j){ return j.get_btag()<this->btag_WPs[0]; });
  auto loose_it = std::find_if(jets.rbegin(),jets.rend(),[this](Jet& j){ return j.get_btag()>this->btag_WPs[0]; });
  auto medium_it= std::find_if(jets.rbegin(),jets.rend(),[this](Jet& j){ return j.get_btag()>this->btag_WPs[1]; });
  auto tight_it = std::find_if(jets.rbegin(),jets.rend(),[this](Jet& j){ return j.get_btag()>this->btag_WPs[2]; });
  
  auto pt_sort = [](Jet& j1,Jet& j2) { return j1.get_pt()>j2.get_pt(); };

  int tight_idx  = std::distance(jets.begin(),tight_it.base())-1;
  int medium_idx = std::distance(jets.begin(),medium_it.base())-1;
  int loose_idx  = std::distance(jets.begin(),loose_it.base())-1;
  int fail_idx   = std::distance(jets.begin(),fail_it.base())-1;
  
  std::vector<int> wp_idxs = {tight_idx,medium_idx,loose_idx, fail_idx};
  auto start = jets.begin();
  for (int wp_idx : wp_idxs)
    {
      if (wp_idx != -1 && start != jets.end())
	{
	  auto end = jets.begin() + wp_idx + 1;
	  std::sort(start, end, pt_sort);
	  start = end;
	}
    }
  
  // For debugging
  if (0)
    {
      std::cout << "Sorted by b-tagging score in descending order and then by pT within each group (Tight, Medium, Loose, Fail), again in descending order:"<<std::endl;
      for (unsigned int ij=0; ij<jets.size(); ij++)
        {
	  std::cout << "  jet "<<ij<<"  pt = "<<jets.at(ij).get_pt()<<"   b-disc="<<jets.at(ij).get_btag()<<std::endl;
        }
    }
  return jets;
}

std::vector<DiJet> Skim_functions::make_dijets(NanoAODTree &nat, EventInfo &ei, const std::vector<Jet> &in_jets)
{
  /**
   * @brief Make all dijets in list of jets
   * 
   */

  std::vector<DiJet> dijets;
  for (unsigned int i = 0; i < in_jets.size(); i++)
  {
    const Jet j1 = in_jets[i];
    for (unsigned int j = i+1; j < in_jets.size(); j++)
    {
      const Jet j2 = in_jets[j];
      DiJet dijet(j1, j2);
      dijet.rebuildP4UsingRegressedPt(true, true);
      dijet.set_jIdx(i, j);

      dijets.push_back(dijet);
    }
  }

  return dijets;
}

void Skim_functions::compute_event_shapes(NanoAODTree &nat, EventInfo& ei, const std::vector<Jet> &in_jets)
{
  /**
   * @brief Computes event shapes for jets in in_jets, and saves them to EVentInfo
   * 
   */
  EventShapeCalculator esc(in_jets);
  EventShapes event_shapes = esc.get_sphericity_shapes();
  ei.event_shapes = event_shapes;
}

std::vector<int> Skim_functions::match_local_idx(std::vector<Jet>& subset,std::vector<Jet>& supset)
{
  /**
   * @brief Returns a list of the subset jet index in the supset jet list
   * 
   */
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

std::vector<GenPart> Skim_functions::select_b_quarks(NanoAODTree &nat, EventInfo &ei)
{
  /*
   * @brief: Return all final state b-quarks
   */
  std::vector<GenPart> bQuarks;
  for (uint igp = 0; igp < *(nat.nGenPart); ++igp)
    {
      GenPart gp(igp, &nat);
      int apdgid = abs(get_property(gp, GenPart_pdgId));
      // b quarks
      if ((apdgid == 5) && gp.isLastCopy())
	{
	  bQuarks.push_back(gp);
	}
    }
  return bQuarks;
}

void Skim_functions::GetMatchedPairs(const double dR_match, std::vector<GenPart*>& quarks, std::vector<GenJetAK8>& genfatjets,
				     std::vector<GenPart*>& matched_quarks, std::vector<GenJetAK8>& matched_genfatjets)
{
  /*
   * @brief Recursively search for the quark-genfatjet pairs based on the minimum dR
   * dR_match: the dR cut to be used in the matching, typically 0.8 for AK8 gen-jets
   * quarks: the vector of quarks you want to match
   * genfatjets: the vector of gen-fatjets to be used in the matching.
   * matched_quarks: the (initially empty) vector of matched quarks
   * matched_genfatjets: the (initially empty) vector of matched gen-fatjets
   */
  unsigned int counter = -1;
  double minDR = 9999.9;
  unsigned int minDR_jetIndex = -1;
  unsigned int minDR_particleIndex = -1;
  for (auto& p: quarks)
    {
      counter++;
      for (unsigned int igj=0; igj<genfatjets.size(); ++igj)
	{
	  double dR = ROOT::Math::VectorUtil::DeltaR(p->P4(), genfatjets.at(igj).P4());
	  if (dR > dR_match) continue;
	  if (dR < minDR)
	    {
	      minDR = dR;
              minDR_jetIndex = igj;
              minDR_particleIndex = counter;
            }
        }
    }

  if (minDR < dR_match)
    {
      // For debugging
      if (0)
        {
          unsigned int quark_uniqueIdx = quarks.at(minDR_particleIndex)->getIdx();
          unsigned int genfatjet_uniqueIdx = genfatjets.at(minDR_jetIndex).getIdx();
	  std::cout << "  DR(quark="<<quark_uniqueIdx<<", gen-fatjet="<<genfatjet_uniqueIdx<<") = "<<minDR<<std::endl;
        }
      matched_genfatjets.push_back(genfatjets.at(minDR_jetIndex));
      matched_quarks.push_back(quarks.at(minDR_particleIndex));

      // Temporary quarks vector:
      std::vector<GenPart*> quarks_to_match_temp;
      unsigned int counter = -1;
      for (auto& p: quarks)
        {
          counter++;
          if (counter == minDR_particleIndex) continue;
          quarks_to_match_temp.push_back(p);
        }
      GetMatchedPairs(dR_match, quarks_to_match_temp, genfatjets, matched_quarks, matched_genfatjets);
    }
  else return;
}

void Skim_functions::GetMatchedPairs(const double dR_match, std::vector<GenPart*>& quarks, std::vector<GenJet>& genjets,
                                     std::vector<GenPart*>& matched_quarks, std::vector<GenJet>& matched_genjets)
{
  /*
   * @brief Recursively search for the quark-genjet pairs based on the minimum dR
   * dR_match: the dR cut to be used in the matching
   * quarks: the vector of quarks you want to match
   * genjets: the vector of gen-jets to be used in the matching
   * matched_quarks: the (initially empty) vector of matched quarks
   * matched_genjets: the (initially empty) vector of matched gen-jets
   */
  unsigned int counter = -1;
  double minDR = 9999.9;
  unsigned int minDR_jetIndex = -1;
  unsigned int minDR_particleIndex = -1;
  for (auto& p: quarks)
    {
      counter++;
      for (unsigned int igj=0; igj<genjets.size(); ++igj)
        {
          double dR = ROOT::Math::VectorUtil::DeltaR(p->P4(), genjets.at(igj).P4());
	  if (dR > dR_match) continue;
          if (dR < minDR)
            {
	      minDR = dR;
              minDR_jetIndex = igj;
              minDR_particleIndex = counter;
            }
        }
    }

  if (minDR < dR_match)
    {
      // For debugging
      if (0)
        {
          unsigned int quark_uniqueIdx = quarks.at(minDR_particleIndex)->getIdx();
          unsigned int genjet_uniqueIdx = genjets.at(minDR_jetIndex).getIdx();
	  std::cout << "  DR(quark="<<quark_uniqueIdx<<", gen-jet="<<genjet_uniqueIdx<<") = "<<minDR<<std::endl;
        }
      matched_genjets.push_back(genjets.at(minDR_jetIndex));
      matched_quarks.push_back(quarks.at(minDR_particleIndex));

      // Temporary quarks vector:
      std::vector<GenPart*> quarks_to_match_temp;
      unsigned int counter = -1;
      for (auto& p: quarks)
        {
          counter++;
          if (counter == minDR_particleIndex) continue;
          quarks_to_match_temp.push_back(p);
        }

      // Temporary genjets vector:
      std::vector<GenJet> genjets_to_match_temp;
      for (unsigned int igj=0; igj<genjets.size(); ++igj)
        {
          if (igj == minDR_jetIndex) continue;
          genjets_to_match_temp.push_back(genjets.at(igj));
        }

      GetMatchedPairs(dR_match, quarks_to_match_temp, genjets_to_match_temp, matched_quarks, matched_genjets);
    }
  else return;
}

void Skim_functions::match_genjets_to_reco(NanoAODTree &nat, EventInfo& ei, std::vector<GenJet>& genjets,std::vector<Jet>& recojets)
{
  for (unsigned int ireco = 0; ireco < recojets.size(); ireco++)
  {
    Jet &jet = recojets.at(ireco);
    int gen_match = -1;
    for (unsigned int igen = 0; igen < genjets.size(); igen++)
    {
      GenJet &genjet = genjets.at(igen);

      if (genjet.getIdx() == get_property(jet, Jet_genJetIdx))
      {
        gen_match = igen;
        break;
      }
    }
    if (gen_match != -1)
    {
      recojets.at(ireco).set_genIdx(gen_match);
      genjets.at(gen_match).set_recoIdx(ireco);
    }
  }
}

std::vector<Muon> Skim_functions::select_muons(CfgParser &config, NanoAODTree &nat, EventInfo &ei)
{
  /**
   * @brief Selects muons in the event
   * 
   */
  float muonPtCut  = config.readFloatOpt("configurations::muonPtCut");
  float muonEtaCut = config.readFloatOpt("configurations::muonEtaCut"); 
  string muonID         = config.readStringOpt("configurations::muonID");
  string muonIsoCutName = config.readStringOpt("configurations::muonIsoCut");
  float muonIsoCutValue;
  
  if (muonIsoCutName == "vLoose")       muonIsoCutValue = 0.4;
  else if (muonIsoCutName == "Loose")   muonIsoCutValue = 0.25; // eff. ~98%
  else if (muonIsoCutName == "Medium")  muonIsoCutValue = 0.20;
  else if (muonIsoCutName == "Tight")   muonIsoCutValue = 0.15; // eff. ~95%
  else if (muonIsoCutName == "vTight")  muonIsoCutValue = 0.10;
  else if (muonIsoCutName == "vvTight") muonIsoCutValue = 0.05;
  else muonIsoCutValue = 9999.9;
    
  std::vector<Muon> muons;
  for (unsigned int imu=0; imu < *(nat.nMuon); ++imu)
    {
      Muon mu(imu, &nat);
      muons.emplace_back(mu);
    }
  
  std::vector<Muon> selected_muons;
  for (auto &mu : muons)
    {
      float pt  = get_property(mu, Muon_pt);
      float eta = get_property(mu, Muon_eta);
      
      // Apply pt & eta cuts
      if (pt < muonPtCut) continue;
      if (std::abs(eta) > muonEtaCut) continue;
      
      // Apply isolation cut
      // PF-based combined relative isolation with Delta & Beta corrections for PU mitigation, uses a DR cone of 0.4
      // Link: https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideMuonSelection#Particle_Flow_isolation
      float iso = get_property(mu, Muon_pfRelIso04_all); 
      if (iso > muonIsoCutValue) continue;
      
      bool ID_WPL = get_property(mu, Muon_looseId);
      bool ID_WPM = get_property(mu, Muon_mediumId);
      bool ID_WPT = get_property(mu, Muon_tightId);
      
      // Apply ID requirement (to be used
      if (muonID == "Loose")
	{
	  if (!ID_WPL) continue;
	}
      else if (muonID == "Medium")
	{
	  if (!ID_WPM) continue;
	}
      else if (muonID == "Tight")
	{
	  if (!ID_WPT) continue;
	}
      
      float dxy = get_property(mu, Muon_dxy);
      float dz  = get_property(mu, Muon_dz);
      
      // note: hardcoded selections can be made configurable from cfg if needed
      const float mu_dxy_max_barr = 0.05;
      const float mu_dxy_max_endc = 0.10;
      const float mu_dz_max_barr = 0.10;
      const float mu_dz_max_endc = 0.20;
      
      bool is_barrel = abs(eta) < 1.2;
      bool pass_dxy = (is_barrel ? dxy < mu_dxy_max_barr : dxy < mu_dxy_max_endc);
      bool pass_dz = (is_barrel ? dz < mu_dz_max_barr : dz < mu_dz_max_endc);
      
      if (!pass_dxy) continue;
      if (!pass_dz) continue;
      
      selected_muons.emplace_back(mu);
    }
  return selected_muons;  
}


std::vector<Electron> Skim_functions::select_electrons(CfgParser &config, NanoAODTree &nat, EventInfo &ei)
{
  float elePtCut  = config.readFloatOpt("configurations::elePtCut");
  float eleEtaCut = config.readFloatOpt("configurations::eleEtaCut");
  string eleID = config.readStringOpt("configurations::eleID");
  float eleIsoCut = config.readFloatOpt("configurations::eleIsoCut");
  
  std::vector<Electron> electrons;
  for (unsigned int ie = 0; ie < *(nat.nElectron); ++ie)
    {
      Electron ele(ie, &nat);
      electrons.emplace_back(ele);
    }
  
  std::vector<Electron> selected_electrons;
  for (auto &el : electrons)
    {
      float pt = get_property(el, Electron_pt);
      float eta = get_property(el, Electron_eta);
      
      // Apply pT and eta cuts
      if (pt < elePtCut) continue;
      if (std::abs(eta) > eleEtaCut) continue;
      
      // Apply isolation cut
      float iso = get_property(el, Electron_pfRelIso03_all);
      if (iso > eleIsoCut) continue;
      
      float dxy = get_property(el, Electron_dxy);
      float dz  = get_property(el, Electron_dz);
      
      bool ID_WPL = get_property(el, Electron_mvaFall17V2Iso_WPL);
      bool ID_WP90 = get_property(el, Electron_mvaFall17V2Iso_WP90);
      bool ID_WP80 = get_property(el, Electron_mvaFall17V2Iso_WP80);
      
      if (eleID == "Loose")
	{
	  if (!ID_WPL) continue;
	}
      else if (eleID == "90")
	{
	  if (!ID_WP90) continue;
	}
      else if (eleID == "80")
	{
	  if (!ID_WP80) continue;
	}
      
      // note: hardcoded selections can be made configurable from cfg if needed
      const float e_dxy_max_barr = 0.05;
      const float e_dxy_max_endc = 0.10;
      const float e_dz_max_barr = 0.10;
      const float e_dz_max_endc = 0.20;
      
      bool is_barrel = abs(eta) < 1.479;
      bool pass_dxy = (is_barrel ? dxy < e_dxy_max_barr : dxy < e_dxy_max_endc);
      bool pass_dz = (is_barrel ? dz < e_dz_max_barr : dz < e_dz_max_endc);
      
      if (!pass_dxy) continue;
      if (!pass_dz) continue;
      
      selected_electrons.emplace_back(el);
    }
  return selected_electrons;
}

double Skim_functions::getPFHT(NanoAODTree& nat, EventInfo& ei)
{
  double sumPFHT = 0.0;
  for (unsigned int ij = 0; ij < *(nat.nJet); ++ij)
    {
      Jet jet(ij, &nat);
      if (jet.P4().Pt() < 30) continue;
      if (std::abs(jet.P4().Eta()) > 2.5) continue;
      sumPFHT+=jet.P4().Pt();
    }
  return sumPFHT;
}

bool Skim_functions::checkHEMissue(EventInfo& ei, const std::vector<Jet> &jets)
{
  for (unsigned int ij=0; ij<jets.size(); ij++)
    {
      bool eta_check = (-3.0 < jets.at(ij).P4().Eta() && jets.at(ij).P4().Eta() < -1.3);
      bool phi_check = (-1.57 < jets.at(ij).P4().Phi() && jets.at(ij).P4().Phi() < -0.78);
      bool pt_check = jets.at(ij).P4().Pt() > 30;

      if (eta_check && phi_check && pt_check)
        {
          // ei.HEMWeight = 0.352;
          return true;
        }
    }
  return false;
}

void Skim_functions::get_puid_sf(EventInfo& ei, const std::vector<Jet> &jets, string puid_sf_file, string year)
{
  // See https://twiki.cern.ch/twiki/bin/view/CMS/PileupJetID#Efficiencies_and_data_MC_scale_f, which recommends using the method 1a in https://twiki.cern.ch/twiki/bin/view/CMS/BTagSFMethods#1a_Event_reweighting_using_scale

  const int pu_id = pmap.get_param<int>("presel", "pu_id");
  // double puid_weight = 1.0;
  // double puid_weight_up = 1.0;
  // double puid_weight_down = 1.0;

  double mc_prob = 1.0;

  double data_prob = 1.0;
  double data_prob_up = 1.0;
  double data_prob_down = 1.0;
  
  TFile f(puid_sf_file.c_str());
  string puid_eff_title = "h2_eff_mcUL" + year + "_T";
  TH2F *puid_eff = (TH2F*)f.Get(puid_eff_title.c_str());
  string puid_sf_title = "h2_eff_sfUL" + year + "_T";
  TH2F *puid_sf = (TH2F*)f.Get(puid_sf_title.c_str());
  string puid_sf_unc_title = "h2_eff_sfUL" + year + "_T_Systuncty";
  TH2F *puid_sf_unc = (TH2F*)f.Get(puid_sf_unc_title.c_str());
  
  for (unsigned int ij=0; ij<jets.size(); ij++)
  {
    Jet jet = jets.at(ij);

    if (jet.P4().Pt() >= 50) {continue;}
    if (get_property(jet, Jet_genJetIdx) == -1) {continue;}
 
    double pt = jet.P4().Pt();
    double eta = jet.P4().Eta();

    if (abs(eta) >= 5.0) {eta = 4.9999;}
    if (pt < 20) {pt = 20;}

    int bin = puid_sf->FindBin(pt, eta);
    float eff = puid_eff->GetBinContent(bin);
    float sf = puid_sf->GetBinContent(bin);
    float sf_up = sf + puid_sf_unc->GetBinContent(bin);
    float sf_down = sf - puid_sf_unc->GetBinContent(bin);

    if (checkBit(jet.get_puid(), pu_id))
    {
      mc_prob *= eff;
      data_prob *= sf*eff;
      data_prob_up *= sf_up*eff;
      data_prob_down *= sf_down*eff;
    }
    else if (!checkBit(jet.get_puid(), pu_id)) {
      mc_prob *= (1 - eff);
      data_prob *= (1 - sf*eff);
      data_prob_up *= (1 - sf_up*eff);
      data_prob_down *= (1 - sf_down*eff);
    }
  }

  double puid_weight = data_prob/mc_prob;
  double puid_weight_up = data_prob_up/mc_prob;
  double puid_weight_down = data_prob_down/mc_prob;

  if (puid_weight_up > 5) {puid_weight_up = 5;}

  ei.PUIDWeight = puid_weight;
  ei.PUIDWeight_up = puid_weight_up;
  ei.PUIDWeight_down = puid_weight_down;
}
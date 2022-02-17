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

using namespace std;

void Skim_functions::initialize_params_from_cfg(CfgParser &config)
{
  /**
   * @brief Initialize configuration for skim
   * Default sets preselection requirements from config
   * 
   */
  // preselections
  pmap.insert_param<bool>("presel","apply", config.readBoolOpt("presel::apply"));
  pmap.insert_param<double>("presel", "pt_min", config.readDoubleOpt("presel::pt_min"));
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

std::vector<Jet> Skim_functions::preselect_jets(NanoAODTree &nat, const std::vector<Jet> &in_jets)
{
  /**
   * @brief Selects jets from in_jets according to preselections defined in config
   * 
   * @return skimmed jet list
   */
  const bool apply = pmap.get_param<bool>("presel","apply");
  if (!apply) return in_jets;
  
  const double pt_min = pmap.get_param<double>("presel", "pt_min");
  const double eta_max = pmap.get_param<double>("presel", "eta_max");
  // const double btag_min = btag_WPs.at(0);
  const int pf_id = pmap.get_param<int>("presel", "pf_id");
  const int pu_id = pmap.get_param<int>("presel", "pu_id");

  std::vector<Jet> out_jets;
  out_jets.reserve(in_jets.size());

  for (unsigned int ij = 0; ij < in_jets.size(); ++ij)
  {
    const Jet &jet = in_jets.at(ij);
    if (jet.P4().Pt() <= pt_min)
      continue;
    if (std::abs(jet.P4().Eta()) >= eta_max)
      continue;
    // if (jet.get_btag() <= btag_min) continue;
    if (!checkBit(jet.get_id(), pf_id))
      continue;
    if (jet.P4().Pt() < 50 && !checkBit(jet.get_puid(), pu_id))
      continue; // PU ID only applies to jet with pT < 50 GeV

    out_jets.emplace_back(jet);
  }

  return out_jets;
}

std::vector<Jet> Skim_functions::btag_sort_jets(NanoAODTree &nat, EventInfo& ei, const std::vector<Jet> &in_jets)
{
  std::vector<Jet> jets = in_jets;
  std::sort(jets.begin(),jets.end(),[](Jet& j1,Jet& j2){ return j1.get_btag()>j2.get_btag(); });
  return jets;
}

std::vector<Jet> Skim_functions::bias_pt_sort_jets (NanoAODTree &nat, EventInfo& ei, const std::vector<Jet> &in_jets)
{
  std::vector<Jet> jets = in_jets;
  std::sort(jets.begin(),jets.end(),[](Jet& j1,Jet& j2){ return j1.get_btag()>j2.get_btag(); });

  auto loose_it = std::find_if(jets.rbegin(),jets.rend(),[this](Jet& j){ return j.get_btag()>this->btag_WPs[0]; });
  auto medium_it= std::find_if(jets.rbegin(),jets.rend(),[this](Jet& j){ return j.get_btag()>this->btag_WPs[1]; });
  auto tight_it = std::find_if(jets.rbegin(),jets.rend(),[this](Jet& j){ return j.get_btag()>this->btag_WPs[2]; });

  auto pt_sort = [](Jet& j1,Jet& j2) { return j1.get_pt()>j2.get_pt(); };

  int tight_idx  = std::distance(jets.begin(),tight_it.base())-1;
  int medium_idx = std::distance(jets.begin(),medium_it.base())-1;
  int loose_idx  = std::distance(jets.begin(),loose_it.base())-1;

  std::vector<int> wp_idxs = {tight_idx,medium_idx,loose_idx};
  auto start = jets.begin();
  for (int wp_idx : wp_idxs)
  {
    if (wp_idx != -1 && start != jets.end()) {
	    auto end = jets.begin() + wp_idx + 1;
	    std::sort(start,end,pt_sort);
	    start = end;
    }
  }
  return jets;
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

void Skim_functions::select_leptons(NanoAODTree &nat, EventInfo &ei)
{
  /**
   * @brief Selects leptons in the event
   * 
   */
  std::vector<Electron> electrons;
  std::vector<Muon> muons;

  for (unsigned int ie = 0; ie < *(nat.nElectron); ++ie)
  {
    Electron ele(ie, &nat);
    electrons.emplace_back(ele);
  }

  for (unsigned int imu = 0; imu < *(nat.nMuon); ++imu)
  {
    Muon mu(imu, &nat);
    muons.emplace_back(mu);
  }

  // apply preselections
  std::vector<Electron> loose_electrons;
  std::vector<Muon> loose_muons;

  // std::vector<Electron> tight_electrons;
  // std::vector<Muon> tight_muons;

  for (auto &el : electrons)
  {

    float dxy = get_property(el, Electron_dxy);
    float dz = get_property(el, Electron_dz);
    float eta = get_property(el, Electron_eta);
    float pt = get_property(el, Electron_pt);
    bool ID_WPL = get_property(el, Electron_mvaFall17V2Iso_WPL);
    // bool ID_WP90 = get_property(el, Electron_mvaFall17V2Iso_WP90);
    // bool ID_WP80 = get_property(el, Electron_mvaFall17V2Iso_WP80);
    float iso = get_property(el, Electron_pfRelIso03_all);

    // note: hardcoded selections can be made configurable from cfg if needed
    const float e_pt_min = 15;
    const float e_eta_max = 2.5;
    const float e_iso_max = 0.15;

    const float e_dxy_max_barr = 0.05;
    const float e_dxy_max_endc = 0.10;
    const float e_dz_max_barr = 0.10;
    const float e_dz_max_endc = 0.20;

    bool is_barrel = abs(eta) < 1.479;
    bool pass_dxy = (is_barrel ? dxy < e_dxy_max_barr : dxy < e_dxy_max_endc);
    bool pass_dz = (is_barrel ? dz < e_dz_max_barr : dz < e_dz_max_endc);

    // loose electrons for veto
    if (pt > e_pt_min &&
        abs(eta) < e_eta_max &&
        iso < e_iso_max &&
        pass_dxy &&
        pass_dz &&
        ID_WPL)
      loose_electrons.emplace_back(el);
  }

  for (auto &mu : muons)
  {

    float dxy = get_property(mu, Muon_dxy);
    float dz = get_property(mu, Muon_dz);
    float eta = get_property(mu, Muon_eta);
    float pt = get_property(mu, Muon_pt);
    bool ID_WPL = get_property(mu, Muon_looseId);
    // bool ID_WPM = get_property(mu, Muon_mediumId);
    // bool ID_WPT = get_property(mu, Muon_tightId);
    float iso = get_property(mu, Muon_pfRelIso04_all);

    // note: hardcoded selections can be made configurable from cfg if needed
    const float mu_pt_min = 10;
    const float mu_eta_max = 2.4;
    const float mu_iso_max = 0.15;

    const float mu_dxy_max_barr = 0.05;
    const float mu_dxy_max_endc = 0.10;
    const float mu_dz_max_barr = 0.10;
    const float mu_dz_max_endc = 0.20;

    bool is_barrel = abs(eta) < 1.2;
    bool pass_dxy = (is_barrel ? dxy < mu_dxy_max_barr : dxy < mu_dxy_max_endc);
    bool pass_dz = (is_barrel ? dz < mu_dz_max_barr : dz < mu_dz_max_endc);

    // loose muons for veto
    if (pt > mu_pt_min &&
        abs(eta) < mu_eta_max &&
        iso < mu_iso_max &&
        pass_dxy &&
        pass_dz &&
        ID_WPL)
      loose_muons.emplace_back(mu);
  }

  // copy needed info to the EventInfo
  if (loose_muons.size() > 0)
    ei.mu_1 = loose_muons.at(0);
  if (loose_muons.size() > 1)
    ei.mu_2 = loose_muons.at(1);
  if (loose_electrons.size() > 0)
    ei.ele_1 = loose_electrons.at(0);
  if (loose_electrons.size() > 1)
    ei.ele_2 = loose_electrons.at(1);

  ei.n_mu_loose = loose_muons.size();
  ei.n_ele_loose = loose_electrons.size();
  // ei.n_mu_tight  = tight_muons.size();
  // ei.n_ele_tight = tight_electrons.size();
}
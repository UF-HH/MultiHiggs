#include "FourB_functions.h"
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

void FourB_functions::initialize_params_from_cfg(CfgParser& config)
{
  // preselections
  pmap.insert_param<bool>("presel", "apply", config.readBoolOpt("presel::apply"));
  pmap.insert_param<std::vector<double> >("presel", "pt_min", config.readDoubleListOpt("presel::pt_min"));
  pmap.insert_param<double>("presel", "eta_max", config.readDoubleOpt("presel::eta_max"));
  pmap.insert_param<int>   ("presel", "pf_id",   config.readIntOpt("presel::pf_id"));
  pmap.insert_param<int>   ("presel", "pu_id",   config.readIntOpt("presel::pu_id"));
  
  // Selection on jets (pT, b-tagging)
  pmap.insert_param<bool>("select_jets", "applyJetCuts", config.readBoolOpt("select_jets::applyJetCuts"));
  pmap.insert_param<int>("select_jets", "applyJetPtCutsTo", config.readIntOpt("select_jets::applyJetPtCutsTo"));
  pmap.insert_param<int>("select_jets", "applyJetBTagCutsTo", config.readIntOpt("select_jets::applyJetBTagCutsTo"));
  pmap.insert_param<vector<int> >("select_jets", "btagWP_cuts", config.readIntListOpt("select_jets::btagWP_cuts"));
  pmap.insert_param<vector<double> >("select_jets", "pt_cuts", config.readDoubleListOpt("select_jets::pt_cuts"));
}

void FourB_functions::initialize_functions(TFile& outputFile)
{}

void FourB_functions::select_gen_particles(NanoAODTree& nat, EventInfo& ei)
{
  std::vector<GenPart> HiggsBosons_FirstCopy;
  std::vector<GenPart> HiggsBosons_LastCopy;
  std::vector<GenPart> BQuarks_FirstCopy;
  
  for (uint igp = 0; igp < *(nat.nGenPart); ++igp)
    {
      GenPart gp(igp, &nat);
      
      int pdgID  = abs(get_property(gp, GenPart_pdgId));
      int status = get_property(gp, GenPart_status);
      bool isLastCopy  = gp.isLastCopy();
      bool isFirstCopy = gp.isFirstCopy();
      
      // Higgs boson
      if (pdgID == 25)
	{
	  if (isFirstCopy) HiggsBosons_FirstCopy.push_back(gp);
	  else if (isLastCopy) HiggsBosons_LastCopy.push_back(gp);
	}
      // Bottom quarks
      else if (pdgID == 5 && isFirstCopy)
	{
	  // Keep only the outgoing b-quarks
	  if (status == 23)
	    {
	      BQuarks_FirstCopy.push_back(gp);
	    }
	}
    }
  
  assert(HiggsBosons_FirstCopy.size() == 2);
  if (HiggsBosons_FirstCopy.at(0).P4().Pt() > HiggsBosons_FirstCopy.at(1).P4().Pt())
    {
      ei.gen_H1_fc = HiggsBosons_FirstCopy.at(0);
      ei.gen_H2_fc = HiggsBosons_FirstCopy.at(1);
    }
  else
    {
      ei.gen_H1_fc = HiggsBosons_FirstCopy.at(1);
      ei.gen_H2_fc = HiggsBosons_FirstCopy.at(0);
    }
  
  assert(HiggsBosons_LastCopy.size() == 2);
  if (HiggsBosons_LastCopy.at(0).P4().Pt() > HiggsBosons_LastCopy.at(1).P4().Pt())
    {
      ei.gen_H1 = HiggsBosons_LastCopy.at(0);
      ei.gen_H2 = HiggsBosons_LastCopy.at(1);
    }
  else
    {
      ei.gen_H1 = HiggsBosons_LastCopy.at(1);
      ei.gen_H2 = HiggsBosons_LastCopy.at(0);
    }
  
  assert(BQuarks_FirstCopy.size() == 4);
  
  std::vector<GenPart> bQuarksFromH1;
  std::vector<GenPart> bQuarksFromH2;
  for (unsigned int b=0; b<BQuarks_FirstCopy.size(); b++)
    {
      GenPart bQ = BQuarks_FirstCopy.at(b);
      GenPart mother(get_property(bQ, GenPart_genPartIdxMother), &nat);
      int motherIdx = mother.getIdx();
      
      if (motherIdx == ei.gen_H1->getIdx())
	{
	  bQuarksFromH1.push_back(bQ);
	}
      else if (motherIdx == ei.gen_H2->getIdx())
	{
	  bQuarksFromH2.push_back(bQ);
	}
      else
	{
	  std::cout << "b-quark has a non-Higgs mother with ID ="<<get_property(mother, GenPart_pdgId)<<std::endl;
	}
    }
  assert(bQuarksFromH1.size() == 2);
  assert(bQuarksFromH2.size() == 2);
  if (bQuarksFromH1.at(0).P4().Pt() > bQuarksFromH1.at(1).P4().Pt())
    {
      ei.gen_H1_b1 = bQuarksFromH1.at(0);
      ei.gen_H1_b2 = bQuarksFromH1.at(1);
    }
  else
    {
      ei.gen_H1_b1 = bQuarksFromH1.at(1);
      ei.gen_H1_b2 = bQuarksFromH1.at(0);
    }
  
  if (bQuarksFromH2.at(0).P4().Pt() > bQuarksFromH2.at(1).P4().Pt())
    {
      ei.gen_H2_b1 = bQuarksFromH2.at(0);
      ei.gen_H2_b2 = bQuarksFromH2.at(1);
    }
  else
    {
      ei.gen_H2_b1 = bQuarksFromH2.at(1);
      ei.gen_H2_b2 = bQuarksFromH2.at(0);
    }
  return;
}

// Match the selected gen b to gen fatjets (AK8)
void FourB_functions::match_genbs_to_genfatjets(NanoAODTree &nat, EventInfo &ei, bool ensure_unique)
{
  const double dR_match = 0.8;
  std::vector<GenPart*> bs_to_match = {
    ei.gen_H1_b1.get_ptr(),
    ei.gen_H1_b2.get_ptr(),
    ei.gen_H2_b1.get_ptr(),
    ei.gen_H2_b2.get_ptr()
  };
  
  std::vector<GenJetAK8> genfatjets;
  for (unsigned int igj = 0; igj < *(nat.nGenJetAK8); ++igj)
    {
      GenJetAK8 gj(igj, &nat);
      genfatjets.push_back(gj);
    }
  
  std::vector<GenPart*> matched_quarks;
  std::vector<GenJetAK8> matched_genfatjets;
  GetMatchedPairs(dR_match, bs_to_match, genfatjets, matched_quarks, matched_genfatjets);
  
  for (unsigned int im=0; im<matched_quarks.size(); im++)
    {
      GenPart* b  = matched_quarks.at(im);
      GenJetAK8 j = matched_genfatjets.at(im);
      
      int bIdx = b->getIdx();
      if (bIdx == ei.gen_H1_b1.get_ptr()->getIdx())
        {
          ei.gen_H1_b1_genfatjet = GenJetAK8(j.getIdx(), &nat);
          if (0) std::cout << "H1_b1 ("<<ei.gen_H1_b1.get_ptr()->getIdx()<<") matched with gen fatjet ="<<j.getIdx()<<std::endl;
        }
      else if (bIdx == ei.gen_H1_b2.get_ptr()->getIdx())
        {
          ei.gen_H1_b2_genfatjet = GenJetAK8(j.getIdx(), &nat);
          if (0) std::cout << "H1_b2 ("<<ei.gen_H1_b2.get_ptr()->getIdx()<<") matched with gen fatjet ="<<j.getIdx()<<std::endl;
        }
      else if (bIdx == ei.gen_H2_b1.get_ptr()->getIdx())
        {
          ei.gen_H2_b1_genfatjet = GenJetAK8(j.getIdx(), &nat);
          if (0) std::cout << "H2_b1 ("<<ei.gen_H2_b1.get_ptr()->getIdx()<<") matched with gen fatjet ="<<j.getIdx()<<std::endl;
        }
      else if (bIdx == ei.gen_H2_b2.get_ptr()->getIdx())
        {
          ei.gen_H2_b2_genfatjet = GenJetAK8(j.getIdx(), &nat);
          if (0) std::cout << "H2_b2 ("<<ei.gen_H2_b2.get_ptr()->getIdx()<<") matched with gen fatjet ="<<j.getIdx()<<std::endl;
        }
    } // Closes loop over matched quarks
}

// Match the selected gen b to gen jets (AK4)
void FourB_functions::match_genbs_to_genjets(NanoAODTree& nat, EventInfo& ei, bool ensure_unique)
{
  const double dR_match = 0.4;
  std::vector<GenPart*> bs_to_match = {
    ei.gen_H1_b1.get_ptr(),
    ei.gen_H1_b2.get_ptr(),
    ei.gen_H2_b1.get_ptr(),
    ei.gen_H2_b2.get_ptr()
  };
  
  // For debugging 
  if (0)
    {
      std::cout << "H1_b1 index: "<<ei.gen_H1_b1.get_ptr()->getIdx()<<std::endl;
      std::cout << "H1_b2 index: "<<ei.gen_H1_b2.get_ptr()->getIdx()<<std::endl;
      std::cout << "H2_b1 index: "<<ei.gen_H2_b1.get_ptr()->getIdx()<<std::endl;
      std::cout << "H2_b2 index: "<<ei.gen_H2_b2.get_ptr()->getIdx()<<std::endl;
    }

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
      if (bIdx == ei.gen_H1_b1.get_ptr()->getIdx())
        {
          ei.gen_H1_b1_genjet = GenJet(j.getIdx(), &nat);
          if (0) std::cout << "H1_b1 ("<<ei.gen_H1_b1.get_ptr()->getIdx()<<") matched with genjet ="<<j.getIdx()<<std::endl;
        }
      else if (bIdx == ei.gen_H1_b2.get_ptr()->getIdx())
        {
          ei.gen_H1_b2_genjet = GenJet(j.getIdx(), &nat);
          if (0) std::cout << "H1_b2 ("<<ei.gen_H1_b2.get_ptr()->getIdx()<<") matched with genjet ="<<j.getIdx()<<std::endl;
        }
      else if (bIdx == ei.gen_H2_b1.get_ptr()->getIdx())
        {
          ei.gen_H2_b1_genjet = GenJet(j.getIdx(), &nat);
          if (0) std::cout << "H2_b1 ("<<ei.gen_H2_b1.get_ptr()->getIdx()<<") matched with genjet ="<<j.getIdx()<<std::endl;
        }
      else if (bIdx == ei.gen_H2_b2.get_ptr()->getIdx())
        {
          ei.gen_H2_b2_genjet = GenJet(j.getIdx(), &nat);
          if (0) std::cout << "H2_b2 ("<<ei.gen_H2_b2.get_ptr()->getIdx()<<") matched with genjet ="<<j.getIdx()<<std::endl;
        }
    }
  return;
}

void FourB_functions::match_genbs_genjets_to_reco(NanoAODTree& nat, EventInfo& ei)
{
  int ij_gen_H1_b1_genjet = (ei.gen_H1_b1_genjet ? find_jet_from_genjet(nat, *ei.gen_H1_b1_genjet) : -1);
  int ij_gen_H1_b2_genjet = (ei.gen_H1_b2_genjet ? find_jet_from_genjet(nat, *ei.gen_H1_b2_genjet) : -1);
  int ij_gen_H2_b1_genjet = (ei.gen_H2_b1_genjet ? find_jet_from_genjet(nat, *ei.gen_H2_b1_genjet) : -1);
  int ij_gen_H2_b2_genjet = (ei.gen_H2_b2_genjet ? find_jet_from_genjet(nat, *ei.gen_H2_b2_genjet) : -1);
  
  if (ij_gen_H1_b1_genjet >= 0) ei.gen_H1_b1_recojet = Jet(ij_gen_H1_b1_genjet, &nat);
  if (ij_gen_H1_b2_genjet >= 0) ei.gen_H1_b2_recojet = Jet(ij_gen_H1_b2_genjet, &nat);
  if (ij_gen_H2_b1_genjet >= 0) ei.gen_H2_b1_recojet = Jet(ij_gen_H2_b1_genjet, &nat);
  if (ij_gen_H2_b2_genjet >= 0) ei.gen_H2_b2_recojet = Jet(ij_gen_H2_b2_genjet, &nat);
  return;
}

void FourB_functions::match_genbs_genfatjets_to_reco(NanoAODTree& nat, EventInfo& ei)
{
  int ij_gen_H1_b1_genfatjet = (ei.gen_H1_b1_genfatjet ? find_fatjet_from_genfatjet(nat, *ei.gen_H1_b1_genfatjet) : -1);
  int ij_gen_H1_b2_genfatjet = (ei.gen_H1_b2_genfatjet ? find_fatjet_from_genfatjet(nat, *ei.gen_H1_b2_genfatjet) : -1);
  int ij_gen_H2_b1_genfatjet = (ei.gen_H2_b1_genfatjet ? find_fatjet_from_genfatjet(nat, *ei.gen_H2_b1_genfatjet) : -1);
  int ij_gen_H2_b2_genfatjet = (ei.gen_H2_b2_genfatjet ? find_fatjet_from_genfatjet(nat, *ei.gen_H2_b2_genfatjet) : -1);
  
  if (ij_gen_H1_b1_genfatjet >= 0) ei.gen_H1_b1_recofatjet = FatJet(ij_gen_H1_b1_genfatjet, &nat);
  if (ij_gen_H1_b2_genfatjet >= 0) ei.gen_H1_b2_recofatjet = FatJet(ij_gen_H1_b2_genfatjet, &nat);
  if (ij_gen_H2_b1_genfatjet >= 0) ei.gen_H2_b1_recofatjet = FatJet(ij_gen_H2_b1_genfatjet, &nat);
  if (ij_gen_H2_b2_genfatjet >= 0) ei.gen_H2_b2_recofatjet = FatJet(ij_gen_H2_b2_genfatjet, &nat);
  return;
}

int FourB_functions::n_gjmatched_in_jetcoll(NanoAODTree& nat, EventInfo& ei, const std::vector<Jet>& in_jets)
{
  std::vector<int> matched_jets;
  if (ei.gen_H1_b1_recojet) matched_jets.push_back(ei.gen_H1_b1_recojet->getIdx());
  if (ei.gen_H1_b2_recojet) matched_jets.push_back(ei.gen_H1_b2_recojet->getIdx());
  if (ei.gen_H2_b1_recojet) matched_jets.push_back(ei.gen_H2_b1_recojet->getIdx());
  if (ei.gen_H2_b2_recojet) matched_jets.push_back(ei.gen_H2_b2_recojet->getIdx());
  
  std::vector<int> reco_js (in_jets.size());
  for (unsigned int ij=0; ij<in_jets.size(); ++ij)
    {
      reco_js.at(ij) = in_jets.at(ij).getIdx();
    }
  int nfound = 0;
  for (int imj : matched_jets)
    {
      if (std::find(reco_js.begin(), reco_js.end(), imj) != reco_js.end())
        nfound += 1;
    }
  return nfound;
}

int FourB_functions::n_ghmatched_in_jetcoll(NanoAODTree& nat, EventInfo& ei, const std::vector<Jet>& in_jets)
{
  std::vector<int> matched_jets(4,-1);
  if (ei.gen_H1_b1_recojet) matched_jets[0] = ei.gen_H1_b1_recojet->getIdx();
  if (ei.gen_H1_b2_recojet) matched_jets[1] = ei.gen_H1_b2_recojet->getIdx();
  if (ei.gen_H2_b1_recojet) matched_jets[2] = ei.gen_H2_b1_recojet->getIdx();
  if (ei.gen_H2_b2_recojet) matched_jets[3] = ei.gen_H2_b2_recojet->getIdx();
  
  std::vector<int> reco_js(in_jets.size());
  for (unsigned int ij = 0; ij < in_jets.size(); ++ij)
    reco_js.at(ij) = in_jets.at(ij).getIdx();
  
  int nfound = 0;
  // Loop over Higgses
  for (unsigned int ih = 0; ih<2; ++ih)
    {
      bool paired = false;
      // Loop over jets
      for (unsigned int ij = 0; ij<2; ++ij)
	{
	  paired = (std::find(reco_js.begin(), reco_js.end(), matched_jets[2 * ih + ij]) != reco_js.end());
	}
      if (paired) nfound += 1;
    }
  return nfound;
}

void FourB_functions::match_signal_genjets(NanoAODTree &nat, EventInfo& ei, std::vector<GenJet> &in_jets)
{
  std::vector<int> matched_jets(4, -1);
  if (ei.gen_H1_b1_genjet) matched_jets[0] = ei.gen_H1_b1_genjet->getIdx();
  if (ei.gen_H1_b2_genjet) matched_jets[1] = ei.gen_H1_b2_genjet->getIdx();
  if (ei.gen_H2_b1_genjet) matched_jets[2] = ei.gen_H2_b1_genjet->getIdx();
  if (ei.gen_H2_b2_genjet) matched_jets[3] = ei.gen_H2_b2_genjet->getIdx();
  
  for (GenJet &gj : in_jets)
    {
      int gj_idx = gj.getIdx();
      if (gj_idx == -1)
	continue;

      for (int id = 0; id < 4; id++)
	{
	  if (matched_jets[id] == gj_idx)
	    {
	      gj.set_signalId(id);
	    }
	}
    }
}

void FourB_functions::match_signal_recojets(NanoAODTree &nat, EventInfo &ei, std::vector<Jet> &in_jets)
{
  std::vector<int> matched_jets(4, -1);
  if (ei.gen_H1_b1_recojet) matched_jets[0] = ei.gen_H1_b1_recojet->getIdx();
  if (ei.gen_H1_b2_recojet) matched_jets[1] = ei.gen_H1_b2_recojet->getIdx();
  if (ei.gen_H2_b1_recojet) matched_jets[2] = ei.gen_H2_b1_recojet->getIdx();
  if (ei.gen_H2_b2_recojet) matched_jets[3] = ei.gen_H2_b2_recojet->getIdx();
  
  for (Jet &j : in_jets)
    {
      int j_idx = j.getIdx();
      if (j_idx == -1)
	continue;

      for (int id = 0; id < 4; id++)
	{
	  if (matched_jets[id] == j_idx)
	    {
	      j.set_signalId(id);
	    }
	}
    }
}

std::vector<Jet> FourB_functions::select_jets(NanoAODTree& nat, EventInfo& ei, const std::vector<Jet>& in_jets)
{
  // Sort jets by pT
  std::vector<Jet> jets_sortedInPt = pt_sort_jets(nat, ei, in_jets);
  if (0) // For debugging
    {
      for (unsigned int ij=0; ij<jets_sortedInPt.size(); ij++)
	{
	  std::cout << " jet "<<ij<<"   pT="<<jets_sortedInPt.at(ij).get_pt()<<"   b-disc.="<<jets_sortedInPt.at(ij).get_btag()<<std::endl;
	}
    }
  
  bool apply_cuts = pmap.get_param<bool>("select_jets", "applyJetCuts");
  if (apply_cuts)
    {
      bool pass_cuts = true;
      const int applyJetPtCutsTo    = pmap.get_param<int>("select_jets", "applyJetPtCutsTo");
      const int applyJetBTagCutsTo  = pmap.get_param<int>("select_jets", "applyJetBTagCutsTo");
      const std::vector<double> pt_cuts  = pmap.get_param<std::vector<double> >("select_jets", "pt_cuts");
      const std::vector<int> btagWP_cuts = pmap.get_param<std::vector<int>>("select_jets", "btagWP_cuts");
      
      // Sanity checks
      if (pt_cuts.size() > applyJetPtCutsTo)
	{
	  throw std::runtime_error("Number of pT cuts required larger than the number of jets mentioned in config (applyJetPtCutsTo). Fixme.");
	}
      if (btagWP_cuts.size() > applyJetBTagCutsTo)
	{
	  throw std::runtime_error("Number of b-tagging cuts required larger than the number of jets mentioned in config (applyJetBTagCutsTo). Fixme.");
	}
      
      // Apply pT cuts
      unsigned int ptCut_index = 0;
      for (unsigned int ij=0; ij<jets_sortedInPt.size(); ++ij)
	{
	  const Jet &jet = jets_sortedInPt.at(ij);
	  if (ij > applyJetPtCutsTo-1) break;
	  if (0) std::cout << " jet "<<ij<<"  pt="<<jet.P4().Pt()<<"   pt cut ="<<pt_cuts.at(ptCut_index)<<std::endl;
	  
	  if (jet.P4().Pt() <= pt_cuts.at(ptCut_index))
	    {
	      pass_cuts = false;
	      break;
	    }
	  if (ptCut_index < pt_cuts.size()-1)
	    {
	      ptCut_index++;
	    }
	}
      
      // Sort jets by ParticleNet b-tagging
      std::vector<Jet> jets_sortedInBTag;
      for (unsigned int ij=0; ij<jets_sortedInPt.size(); ++ij)
        {
          const Jet &jet = jets_sortedInPt.at(ij);
	  jets_sortedInBTag.push_back(jet);
	}
      stable_sort(jets_sortedInBTag.begin(), jets_sortedInBTag.end(), [](const Jet & a, const Jet & b) -> bool{return(get_property(a, Jet_btagPNetBvsAll) > get_property(b, Jet_btagPNetBvsAll)); });
      for (unsigned int ij=0; ij<jets_sortedInBTag.size(); ++ij)
	{
	  const Jet &jet = jets_sortedInBTag.at(ij);
	  //if (0) std::cout << " jet ="<<ij<<"   PNet BvsAll = "<<get_property(jet, Jet_btagPNetBvsAll)<<std::endl;
	}
      
      // If cuts are not satisfied, resize jet selection to zero
      if (!pass_cuts)
	{
	  jets_sortedInPt.resize(0);
	}
    } // Closes if for pT and b-tagging cuts
  return jets_sortedInPt;
}


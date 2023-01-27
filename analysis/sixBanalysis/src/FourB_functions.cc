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

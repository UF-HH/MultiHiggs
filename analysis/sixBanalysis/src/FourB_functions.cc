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
  
  std::cout << "\nselect_gen_particles"<<std::endl;
  for (uint igp = 0; igp < *(nat.nGenPart); ++igp)
    {
      GenPart gp(igp, &nat);
      
      int pdgID  = abs(get_property(gp, GenPart_pdgId));
      int status = get_property(gp, GenPart_status);
      bool isLastCopy  = gp.isLastCopy();
      bool isFirstCopy = gp.isFirstCopy();
      
      std::cout << "igp ="<<igp<<"   ID="<<pdgID<<"   status="<<status<<"  last="<<isLastCopy<<"  first="<<isFirstCopy<<std::endl;
      //GenPart mother(get_property(gp, GenPart_genPartIdxMother), &nat);
            
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
  
  std::cout << "Size of b-quarks vector ="<<BQuarks_FirstCopy.size()<<std::endl;
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

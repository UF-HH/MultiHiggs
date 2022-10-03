#include "TrgEff_functions.h"
#include "Math/VectorUtil.h"
#include "Math/Vector3D.h"
#include "Math/Functions.h"

#include <iostream>
#include <tuple>
#include <algorithm>

#include "Muon.h"

using namespace std;

void TrgEff_functions::initialize_params_from_cfg(CfgParser& config)
{
  // preselections
  pmap.insert_param<bool>("presel", "apply", config.readBoolOpt("presel::apply"));
  pmap.insert_param<std::vector<double> >("presel", "pt_min", config.readDoubleListOpt("presel::pt_min"));
  pmap.insert_param<double>("presel", "eta_max", config.readDoubleOpt("presel::eta_max"));
  pmap.insert_param<int>   ("presel", "pf_id",   config.readIntOpt("presel::pf_id"));
  pmap.insert_param<int>   ("presel", "pu_id",   config.readIntOpt("presel::pu_id"));
  
  // parse specific parameters for various functions
  pmap.insert_param<bool>          ("bias_pt_sort", "applyJetCuts", config.readBoolOpt("bias_pt_sort::applyJetCuts"));
  pmap.insert_param<vector<int>>   ("bias_pt_sort", "btagWP_cuts",  config.readIntListOpt("bias_pt_sort::btagWP_cuts"));
  pmap.insert_param<std::vector<double> >("bias_pt_sort", "pt_cuts", config.readDoubleListOpt("bias_pt_sort::pt_cuts"));
}

std::vector<Jet> TrgEff_functions::select_jets(NanoAODTree &nat, EventInfo& ei, const std::vector<Jet> &in_jets)
{
  return select_jets_bias_pt_sort(nat, ei, in_jets);
}

std::vector<Jet> TrgEff_functions::select_jets_bias_pt_sort(NanoAODTree &nat, EventInfo& ei, const std::vector<Jet> &in_jets)
{
  std::vector<Jet> jets = bias_pt_sort_jets(nat, ei, in_jets);
  bool apply_cuts = pmap.get_param<bool>("bias_pt_sort", "applyJetCuts");
  
  if (apply_cuts)
    {
      bool pass_cuts = true;
      std::vector<int>    btagWP_cuts = pmap.get_param<std::vector<int>>("bias_pt_sort", "btagWP_cuts");
      
      unsigned int ncuts = btagWP_cuts.size();
      
      for (unsigned int icut=0; icut<ncuts; icut++)
	{
	  const Jet& j = jets[icut];
	  int  btagWP  = btagWP_cuts[icut];
	  
	  if (j.get_btag() <= btag_WPs[btagWP])
	    {
	      pass_cuts = false;
	      break;
	    }
	}
      if (!pass_cuts) jets.resize(0);
    }
  return jets;
}

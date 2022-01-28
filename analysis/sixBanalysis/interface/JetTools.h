#ifndef JETFUNCTIONS_H
#define JETFUNCTIONS_H

/**
 ** class  : Jet_functions
 ** author : L. Cadamuro (UF)
 ** date   : 16/10/2020
 ** brief  : Functions for generic handling of jets (scale, smear, etc..)
 **/

#include "Jet.h"
#include "NanoAODTree.h"
#include <vector>
#include "TRandom3.h"

// from CMSSW libraries
#include "JetMETCorrections/Modules/interface/JetResolution.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"

class JetTools{
    
public:
  void init_jec_shift(std::string JECFileName, std::string syst_name);

  void init_smear(std::string JERScaleFactorFile, std::string JERResolutionFile, int random_seed);

  std::vector<Jet> jec_shift_jets(NanoAODTree& nat, const std::vector<Jet>& input_jets, bool direction_is_up);

  std::vector<Jet> smear_jets(NanoAODTree& nat, const std::vector<Jet>& input_jets,
			      Variation jer_var = Variation::NOMINAL, Variation breg_jer_var = Variation::NOMINAL);

private:
  std::unique_ptr<JetCorrectorParameters>   jcp_;
  std::unique_ptr<JetCorrectionUncertainty> jcu_;

  std::unique_ptr<JME::JetResolutionScaleFactor> jetResolutionScaleFactor_;
  std::unique_ptr<JME::JetResolution>            jetResolution_;
  TRandom3 rndm_generator_;

};

#endif // JETFUNCTIONS_H

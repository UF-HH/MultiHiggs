#ifndef TRGEFF_FUNCTIONS_H
#define TRGEFF_FUNCTIONS_H

#include "Skim_functions.h"

class TrgEff_functions : public Skim_functions{
  
public:

  ////////////////////////////////////////////////////
  /// Start methods to be overidden

  void Print() override{
    cout << "[INFO] ... Using TrgEff_functions" << endl; 
  }

  ////////////////////////////////////////////////////
  /// parameter initialization
  ////////////////////////////////////////////////////

  /**
   * @brief Initialize param values for skim as defined in config file 
   * This method can be overriden to define skim specific values
   * Default defines preselection cuts
   * @param cfgr .cfg config file
   */
  void initialize_params_from_cfg(CfgParser &cfgr) override;
  
  std::vector<Jet> select_jets(NanoAODTree &nat, EventInfo& ei, const std::vector<Jet> &in_jets);
  std::vector<Jet> select_jets_bias_pt_sort(NanoAODTree &nat, EventInfo& ei, const std::vector<Jet> &in_jets);
  
  //private:
  
  // NN evaluators for DNN
  //std::unique_ptr<EvalNN> n_2j_classifier_;
  //std::unique_ptr<EvalNN> n_6j_classifier_;
};

#endif //TRGEFF_FUNCTIONS_H

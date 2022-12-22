#ifndef FOURB_FUNCTIONS_H
#define FOURB_FUNCTIONS_H

#include "Skim_functions.h"

class FourB_functions : public Skim_functions{
    
public:

  ////////////////////////////////////////////////////
  /// Start methods to be overidden

  void Print() override{
    cout << "[INFO] ... Using FourB_functions" << endl; 
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

  /**
   * @brief Initialize functions for skim as defined in config file
   * This method should be overriden 
   * @param outputFile .root output file
   */
  void initialize_functions(TFile &outputFile) override;


  ////////////////////////////////////////////////////
  /// gen objects functions
  ////////////////////////////////////////////////////
  /**
   * @brief Select important gen particles and save them to ei
   * This method should be overriden 
   * @param nat NanoAODTree being processed
   * @param ei EventInfo class to store values
   */
  void select_gen_particles(NanoAODTree &nat, EventInfo &ei) override;
  

private:

};

#endif

#ifndef TTBar_FUNCTIONS_H
#define TTBar_FUNCTIONS_H

#include "Skim_functions.h"

class TTBar_functions : public Skim_functions{
    
public:
  ////////////////////////////////////////////////////
  /// Start methods to be overidden

  void Print() override{
    cout << "[INFO] ... Using TTBar_functions" << endl; 
  }

  // select up to six jet candidates out of the input jets - configurable to run various selection algos
  /**
   * @brief Select jet candidates - configureable to run various selection algos defined in config
   * This method should be overriden 
   * @param nat NanoAODTree being processed
   * @param ei EventInfo class to store values
   * @param in_jets List of jets to select from
   * @return std::vector<Jet> of selected jets
   */
  std::vector<Jet> select_jets(NanoAODTree &nat, EventInfo &ei, const std::vector<Jet> &in_jets) override;


};
#endif //TTBar_FUNCTIONS_H

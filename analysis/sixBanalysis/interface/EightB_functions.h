#ifndef EIGHTB_FUNCTIONS_H
#define EIGHTB_FUNCTIONS_H

#include "Skim_functions.h"

class EightB_functions : public Skim_functions{
    
public:

  ////////////////////////////////////////////////////
  /// Start methods to be overidden

  void Print() override{
    cout << "[INFO] ... Using EightB_functions" << endl; 
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

  /**
   * @brief Match selected gen bs to gen jets
   * This method should be overriden 
   * @param nat NanoAODTree being processed
   * @param ei EventInfo class to store values
   * @param ensure_unique if true, ensures that a gen jet is not matched to two different partons
  // otherwise it will match to the closest parton found
   */
  void match_genbs_to_genjets(NanoAODTree &nat, EventInfo &ei, bool ensure_unique = true) override;

  /**
   * @brief Match genjets associacted to a gen b quark to a reco jet
   * This method should be overriden 
   * @param nat NanoAODTree being processed
   * @param ei EventInfo class to store values
   */
  void match_genbs_genjets_to_reco(NanoAODTree &nat, EventInfo &ei) override;

  /**
   * @brief Match signal objects to reco in_jets collection and saving ID to signalId
   * This method should be overriden 
   * @param nat NanoAODTree being processed
   * @param ei EventInfo class to store values
   * @param in_jets Reco Jet collection to match with
   */
  void match_signal_recojets(NanoAODTree &nat, EventInfo &ei, std::vector<Jet> &in_jets) override;

  /**
   * @brief Match signal objects to gen in_jets collection and saving ID to signalId
   * This method should be overriden 
   * @param nat NanoAODTree being processed
   * @param ei EventInfo class to store values
   * @param in_jets Gen Jet collection to match with
   */
  void match_signal_genjets(NanoAODTree &nat, EventInfo &ei, std::vector<GenJet> &in_jets) override;

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

  std::vector<Jet> select_eightb_jets_maxbtag        (NanoAODTree& nat, EventInfo& ei, const std::vector<Jet>& in_jets); // by b tag (highest first)

  ////////////////////////////////////////////////////
  /// Higgs pairing functions
  ////////////////////////////////////////////////////

  /**
   * @brief Pair jet candidates - configurable to run various pairing algos
   * This method should be overriden
   * @param nat NanoAODTree being processed
   * @param ei EventInfo class to store values
   * @param in_jets List of jets to pair 
   */
  void pair_jets(NanoAODTree &nat, EventInfo &ei, const std::vector<Jet> &in_jets) override;

  std::tuple<CompositeCandidate, CompositeCandidate, CompositeCandidate, CompositeCandidate> pair_passthrough (NanoAODTree &nat, EventInfo& ei, const std::vector<Jet>& jets);

  ////////////////////////////////////////////////////
  /// other jet utilities
  ////////////////////////////////////////////////////

  /**
   * @brief Count how many valid genjets in the ei are in the in_jets collection
   * This method should be overriden
   * @param nat NanoAODTree being processed
   * @param ei EventInfo class to store values
   * @param in_jets List of jets to to compare
   * @return int Number of valid genjets in in_jets
   */
  int n_gjmatched_in_jetcoll(NanoAODTree &nat, EventInfo &ei, const std::vector<Jet> &in_jets) override;

  /**
   * @brief Count how many valid gen higgs in the ei are in the in_jets collection
   * This method should be overriden
   * @param nat NanoAODTree being processed
   * @param ei EventInfo class to store values
   * @param in_jets List of jets to to compare
   * @return int Number of valid gen higgs in in_jets
   */
  int n_ghmatched_in_jetcoll(NanoAODTree &nat, EventInfo &ei, const std::vector<Jet> &in_jets) override;

  // add match flags to the selected jets (from which H are the selected jets?)
  /**
   * @brief Returns ID of the gen higgs this jet is from
   * This method should be overriden
   * @param nat NanoAODTree being processed
   * @param ei EventInfo class to store values
   * @param jet 
   * @return int ID of the gen higgs this jet is from
   * -1: none, 0: H1Y1, 1: H2Y1, 2: H1Y2, 3 H2Y2
   */
  int get_jet_genmatch_flag(NanoAODTree &nat, EventInfo &ei, const Jet &jet) override; // -1: other, 0: HX, 1: HY1, 2: HY2

  /**
   * @brief Get the ID of the gen higgs each selected jet in ei, stores in ei
   * 
   * @param nat NanoAODTree being processed
   * @param ei EventInfo class to store values
   */
  void compute_seljets_genmatch_flags(NanoAODTree &nat, EventInfo &ei) override;

};
#endif //EIGHTB_FUNCTIONS_H

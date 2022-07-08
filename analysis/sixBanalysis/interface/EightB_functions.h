#ifndef EIGHTB_FUNCTIONS_H
#define EIGHTB_FUNCTIONS_H

#include "Skim_functions.h"

// #include "cpp_geometric.h"

#include "EvalONNX.h"

typedef std::tuple<CompositeCandidate, CompositeCandidate, CompositeCandidate, CompositeCandidate> H4_tuple;
typedef std::tuple<CompositeCandidate, CompositeCandidate> YY_tuple;

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

  std::vector<Jet> select_eightb_jets_gnn(NanoAODTree &nat, EventInfo &ei, const std::vector<Jet> &in_jets);

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

  H4_tuple pair_4H_passthrough (NanoAODTree &nat, EventInfo& ei, const std::vector<Jet>& jets);
  H4_tuple pair_4H_min_mass_spread (NanoAODTree &nat, EventInfo& ei, const std::vector<Jet>& jets);
  H4_tuple pair_4H_gnn(NanoAODTree &nat, EventInfo &ei, const std::vector<Jet> &in_jets);

  YY_tuple pair_YY_passthrough(NanoAODTree &nat, EventInfo &ei, const H4_tuple &reco_Hs);
  YY_tuple pair_YY_min_mass_spread(NanoAODTree &nat, EventInfo &ei, const H4_tuple &reco_Hs);

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

private:
  // std::unique_ptr<TorchUtils::GeoModel> gnn_classifier_;
  std::unique_ptr<EvalONNX> onnx_classifier_;

  std::vector<std::vector<int>> dijet_pairings = {
      {0, 1}, {0, 2}, {0, 3}, {0, 4}, {0, 5}, {0, 6}, {0, 7}, {1, 2}, {1, 3}, {1, 4}, {1, 5}, {1, 6}, {1, 7}, {2, 3}, {2, 4}, {2, 5}, {2, 6}, {2, 7}, {3, 4}, {3, 5}, {3, 6}, {3, 7}, {4, 5}, {4, 6}, {4, 7}, {5, 6}, {5, 7}, {6, 7}};

  std::vector<std::vector<int>> quadH_pairings = {
      {0, 13, 22, 27}, {0, 13, 23, 26}, {0, 13, 24, 25}, {0, 14, 19, 27}, {0, 14, 20, 26}, {0, 14, 21, 25}, {0, 15, 18, 27}, {0, 15, 20, 24}, {0, 15, 21, 23}, {0, 16, 18, 26}, {0, 16, 19, 24}, {0, 16, 21, 22}, {0, 17, 18, 25}, {0, 17, 19, 23}, {0, 17, 20, 22}, {1, 8, 22, 27}, {1, 8, 23, 26}, {1, 8, 24, 25}, {1, 9, 19, 27}, {1, 9, 20, 26}, {1, 9, 21, 25}, {1, 10, 18, 27}, {1, 10, 20, 24}, {1, 10, 21, 23}, {1, 11, 18, 26}, {1, 11, 19, 24}, {1, 11, 21, 22}, {1, 12, 18, 25}, {1, 12, 19, 23}, {1, 12, 20, 22}, {2, 7, 22, 27}, {2, 7, 23, 26}, {2, 7, 24, 25}, {2, 9, 15, 27}, {2, 9, 16, 26}, {2, 9, 17, 25}, {2, 10, 14, 27}, {2, 10, 16, 24}, {2, 10, 17, 23}, {2, 11, 14, 26}, {2, 11, 15, 24}, {2, 11, 17, 22}, {2, 12, 14, 25}, {2, 12, 15, 23}, {2, 12, 16, 22}, {3, 7, 19, 27}, {3, 7, 20, 26}, {3, 7, 21, 25}, {3, 8, 15, 27}, {3, 8, 16, 26}, {3, 8, 17, 25}, {3, 10, 13, 27}, {3, 10, 16, 21}, {3, 10, 17, 20}, {3, 11, 13, 26}, {3, 11, 15, 21}, {3, 11, 17, 19}, {3, 12, 13, 25}, {3, 12, 15, 20}, {3, 12, 16, 19}, {4, 7, 18, 27}, {4, 7, 20, 24}, {4, 7, 21, 23}, {4, 8, 14, 27}, {4, 8, 16, 24}, {4, 8, 17, 23}, {4, 9, 13, 27}, {4, 9, 16, 21}, {4, 9, 17, 20}, {4, 11, 13, 24}, {4, 11, 14, 21}, {4, 11, 17, 18}, {4, 12, 13, 23}, {4, 12, 14, 20}, {4, 12, 16, 18}, {5, 7, 18, 26}, {5, 7, 19, 24}, {5, 7, 21, 22}, {5, 8, 14, 26}, {5, 8, 15, 24}, {5, 8, 17, 22}, {5, 9, 13, 26}, {5, 9, 15, 21}, {5, 9, 17, 19}, {5, 10, 13, 24}, {5, 10, 14, 21}, {5, 10, 17, 18}, {5, 12, 13, 22}, {5, 12, 14, 19}, {5, 12, 15, 18}, {6, 7, 18, 25}, {6, 7, 19, 23}, {6, 7, 20, 22}, {6, 8, 14, 25}, {6, 8, 15, 23}, {6, 8, 16, 22}, {6, 9, 13, 25}, {6, 9, 15, 20}, {6, 9, 16, 19}, {6, 10, 13, 23}, {6, 10, 14, 20}, {6, 10, 16, 18}, {6, 11, 13, 22}, {6, 11, 14, 19}, {6, 11, 15, 18}};

  std::vector<std::vector<int>> dihiggs_pairings = {
      {0, 1}, {0, 2}, {0, 3}, {1, 2}, {1, 3}, {2, 3}};

  std::vector<std::vector<int>> diY_pairings = {
      {0, 5}, {1, 4}, {2, 3}};
};
#endif //EIGHTB_FUNCTIONS_H

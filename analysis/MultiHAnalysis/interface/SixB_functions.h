#ifndef SIXB_FUNCTIONS_H
#define SIXB_FUNCTIONS_H

#include "Skim_functions.h"
#include "EvalNN.h"

class SixB_functions : public Skim_functions{
    
public:

  ////////////////////////////////////////////////////
  /// Start methods to be overidden

  void Print() override{
    cout << "[INFO] ... Using SixB_functions" << endl; 
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
   * @param nat NanoAODTree being processed
   * @param ei EventInfo class to store values
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
   */
  int get_jet_genmatch_flag(NanoAODTree &nat, EventInfo &ei, const Jet &jet) override; // -1: other, 0: HX, 1: HY1, 2: HY2

  /**
   * @brief Get the ID of the gen higgs each selected jet in ei, stores in ei
   * 
   * @param nat NanoAODTree being processed
   * @param ei EventInfo class to store values
   */
  void compute_seljets_genmatch_flags(NanoAODTree &nat, EventInfo &ei) override;

  ////////////////////////////////////////////////////
  /// parameter initialization
  ////////////////////////////////////////////////////

  // just pair jets as in their initial order ABCDEF -> (AB)(CD)(ED) - for debug
  std::tuple<CompositeCandidate, CompositeCandidate, CompositeCandidate> pair_passthrough (NanoAODTree& nat, EventInfo& ei, const std::vector<Jet>& jets);

  // closest to a 3D diagonal a la HH->4b resonant  
  std::tuple<CompositeCandidate, CompositeCandidate, CompositeCandidate> pair_mH (NanoAODTree& nat, EventInfo& ei, const std::vector<Jet>& in_jets);

  // closest to a 3D diagonal a la HH->4b nonresonant  
  std::tuple<CompositeCandidate, CompositeCandidate, CompositeCandidate> pair_D_HHH (NanoAODTree& nat, EventInfo& ei, const std::vector<Jet>& in_jets);
  std::tuple<CompositeCandidate, CompositeCandidate, CompositeCandidate> pair_D_HHH (NanoAODTree& nat, EventInfo& ei, const std::vector<Jet>& in_jets, const int fitCorrection);

  // use the 2jet DNN
  std::tuple<CompositeCandidate, CompositeCandidate, CompositeCandidate> pair_2jet_DNN (NanoAODTree& nat, EventInfo& ei, const std::vector<Jet>& in_jets);

  // build the pairs leading to the min mass difference across them
  std::tuple<CompositeCandidate, CompositeCandidate, CompositeCandidate> pair_min_diag_distance (NanoAODTree& nat, EventInfo& ei, std::vector<Jet> jets);


  ////////////////////////////////////////////////////
  /// HYX reconstruction functions
  ////////////////////////////////////////////////////
  std::tuple<CompositeCandidate, CompositeCandidate, CompositeCandidate> select_XYH_leadJetInX (
    NanoAODTree& nat, EventInfo& ei, std::tuple<CompositeCandidate, CompositeCandidate, CompositeCandidate> reco_Hs);

  // sort jets with btag bias pt ordering
  // void btag_bias_pt_sort(std::vector<Jet>& in_jets);

  // sort jets with pt regressed ordering
  // void pt_sort(std::vector<Jet>& in_jets);

  // pass event if jet collection passes input pt and btag cuts
  // bool pass_jet_cut(Cutflow& cutflow, const std::vector<double> pt_cuts,const std::vector<int> btagWP_cuts,const std::vector<Jet> &in_jets);

  // create vector of all higgs resonances 
  // std::vector<DiJet> get_tri_higgs_D_HHH(std::vector<Jet>& in_jets);

  // std::vector<Jet> get_6jet_top(std::vector<Jet>& in_jets);
  // std::vector<Jet> get_6jet_NN(EventInfo& ei,std::vector<Jet>& in_jets,EvalNN& n_6j_classifier);

  
  // std::vector<DiJet> get_2jet_NN(EventInfo& ei,std::vector<Jet>& in_jets,EvalNN& n_2j_classifier);
  std::vector<DiJet> get_3dijet_NN(EventInfo& ei,std::vector<Jet>& in_jets,EvalNN& n_3d_classifier);
  // std::vector<DiJet> get_tri_higgs_NN(EventInfo& ei,std::vector<Jet>& in_jets,EvalNN& n_6j_classifier,EvalNN& n_2j_classifier);

  // passes event if all dijets mass is greater than 30 from higgs mass
  bool pass_higgs_cr(const std::vector<DiJet>& in_dijets);

  //////////// functions for the jet selection
  // std::vector<Jet> select_sixb_jets_btag_order     (NanoAODTree &nat, EventInfo& ei, const std::vector<Jet> &in_jets); // by b tag (highest first)
  std::vector<Jet> selectJetsForPairing            (NanoAODTree &nat, EventInfo& ei, const std::vector<Jet> &in_jets); // by the b tag groups + pt within but apply cuts on sorted by pT b-jets
  std::vector<Jet> select_sixb_jets_bias_pt_sort   (NanoAODTree &nat, EventInfo& ei, const std::vector<Jet> &in_jets); // by the b tag groups + pt within
  std::vector<Jet> select_sixb_jets_pt_sort        (NanoAODTree &nat, EventInfo& ei, const std::vector<Jet> &in_jets); // by pt (highest first)
  std::vector<Jet> select_sixb_jets_6jet_DNN       (NanoAODTree &nat, EventInfo& ei, const std::vector<Jet> &in_jets); // use the 6 jet classifier
  std::vector<Jet> select_sixb_jets_maxbtag        (NanoAODTree& nat, EventInfo& ei, const std::vector<Jet>& in_jets); // by b tag (highest first)
  std::vector<Jet> select_sixb_jets_maxbtag_highpT (NanoAODTree& nat, EventInfo& ei, const std::vector<Jet>& in_jets, int nleadbtag);
        

private:
	
  // NN evaluators for DNN
  std::unique_ptr<EvalNN> n_2j_classifier_;
  std::unique_ptr<EvalNN> n_6j_classifier_;

  // All the different dijet pairs for 6 jets
  const std::vector<std::vector<int>> dijet_pairings = {
    {0, 1},{0, 2},{0, 3},{0, 4},{0, 5},
    {1, 2},{1, 3},{1, 4},{1, 5},
    {2, 3},{2, 4},{2, 5},
    {3, 4},{3, 5},
    {4, 5}
  };
	
  // All the different 3 higgs pairs for 3 dijets of 6 jets
  const std::vector<std::vector<int>> triH_pairings = {
    {0,  9, 14},
    {0, 10, 13},
    {0, 11, 12},
    {1,  6, 14},
    {1,  7, 13},
    {1,  8, 12},
    {2,  5, 14},
    {2,  7, 11},
    {2,  8, 10},
    {3,  5, 13},
    {3,  6, 11},
    {3,  8,  9},
    {4,  5, 12},
    {4,  6, 10},
    {4,  7,  9}
  };
};

#endif //SIXB_FUNCTIONS_H

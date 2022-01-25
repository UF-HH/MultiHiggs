#ifndef SIXB_FUNCTIONS_H
#define SIXB_FUNCTIONS_H

#include "NanoAODTree.h"
#include "EventInfo.h"
#include "Cutflow.h"

#include "Jet.h"
#include "GenJet.h"
#include "GenPart.h"
#include "CompositeCandidate.h"
#include "DiJet.h"

#include "CfgParser.h"

#include "EvalNN.h"

#include "ParamsMap.h"

#include <any>
#include <unordered_map>
#include <string>

class SixB_functions{
    
public:
  ////////////////////////////////////////////////////
  /// parameter initialization
  ////////////////////////////////////////////////////

  // read all the info needed by the six functions from the config - to be done once before the event loop starts
  void initialize_params_from_cfg_sixbskim(CfgParser& cfgr);
  void initialize_params_from_cfg_ttbarskim(CfgParser& cfgr);
  
  // using the internally stored parameters, initialize the function methods
  void initialize_functions_sixbskim(TFile& outputFile);

  void set_debug(bool debug) {debug_ = debug;}

  ////////////////////////////////////////////////////
  /// gen objects functions
  ////////////////////////////////////////////////////

  // copy general event-level into to ei
  void copy_event_info(NanoAODTree& nat, EventInfo& ei, bool is_mc);
        
  // select the gen-level six b candidates (bs, bosons)
  void select_gen_particles(NanoAODTree& nat, EventInfo& ei);

  // match the selected gen b to gen jets
  // if ensure_unique = true, ensures that a gen jet is not matched to two different partons
  // otherwise it will match to the closest parton found
  void match_genbs_to_genjets(NanoAODTree& nat, EventInfo& ei, bool ensure_unique = true);

  // match the genjets associated to the 6 gen b quarks to reco jets
  void match_genbs_genjets_to_reco(NanoAODTree& nat, EventInfo& ei);

  // void match_genjets_to_reco(std::vector<GenJet>& genjets,std::vector<Jet>& recojets); // EDITED FOR CODE REVIEW - FIXME

  ////////////////////////////////////////////////////
  /// jet selection functions
  ////////////////////////////////////////////////////

  // create a vector with all jets in the event
  std::vector<GenJet> get_all_genjets(NanoAODTree& nat);
	
  // create a vector with all jets in the event
  std::vector<Jet> get_all_jets(NanoAODTree& nat);

  // create a vector with all preselected jets in the event (minimal pt/eta/id requirements)
  std::vector<Jet> preselect_jets(NanoAODTree& nat, const std::vector<Jet>& in_jets);

  // select up to six jet candidates out of the input jets - configurable to run various selection algos
  std::vector<Jet> select_sixb_jets(NanoAODTree& nat, EventInfo& ei, const std::vector<Jet>& in_jets);

  // two most b tagged jets for ttbar events
  std::vector<Jet> select_ttbar_jets(NanoAODTree &nat, EventInfo& ei, const std::vector<Jet> &in_jets);


  ////////////////////////////////////////////////////
  /// Higgs pairing functions
  ////////////////////////////////////////////////////

  // pair the jets and assign them into the 6b candidates - will be stored in the EventInfo. The algorithm is configured as a string in the parameters
  // specific functions for pairing must return 3 CompositeCandidate, and they are re-ordered in the pair_jets function
  void pair_jets(NanoAODTree& nat, EventInfo& ei, const std::vector<Jet>& in_jets);

  // just pair jets as in their initial order ABCDEF -> (AB)(CD)(ED) - for debug
  std::tuple<CompositeCandidate, CompositeCandidate, CompositeCandidate> pair_passthrough (NanoAODTree& nat, EventInfo& ei, const std::vector<Jet>& jets);

  // closest to a 3D diagonal a la HH->4b nonresonant  
  std::tuple<CompositeCandidate, CompositeCandidate, CompositeCandidate> pair_D_HHH (NanoAODTree& nat, EventInfo& ei, const std::vector<Jet>& in_jets);

  // use the 2jet DNN
  std::tuple<CompositeCandidate, CompositeCandidate, CompositeCandidate> pair_2jet_DNN (NanoAODTree& nat, EventInfo& ei, const std::vector<Jet>& in_jets);

  // build the pairs leading to the min mass difference across them
  std::tuple<CompositeCandidate, CompositeCandidate, CompositeCandidate> pair_min_diag_distance (NanoAODTree& nat, EventInfo& ei, std::vector<Jet> jets);


  ////////////////////////////////////////////////////
  /// HYX reconstruction functions
  ////////////////////////////////////////////////////
  std::tuple<CompositeCandidate, CompositeCandidate, CompositeCandidate> select_XYH_leadJetInX (
    NanoAODTree& nat, EventInfo& ei, std::tuple<CompositeCandidate, CompositeCandidate, CompositeCandidate> reco_Hs);

  // get the local idx in the supset for each jet in the subset
  std::vector<int> match_local_idx(std::vector<Jet>& subset,std::vector<Jet>& supset);
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
  std::vector<Jet> select_sixb_jets_bias_pt_sort   (NanoAODTree &nat, EventInfo& ei, const std::vector<Jet> &in_jets); // by the b tag groups + pt within
  std::vector<Jet> select_sixb_jets_pt_sort        (NanoAODTree &nat, EventInfo& ei, const std::vector<Jet> &in_jets); // by pt (highest first)
  std::vector<Jet> select_sixb_jets_6jet_DNN       (NanoAODTree &nat, EventInfo& ei, const std::vector<Jet> &in_jets); // use the 6 jet classifier
  std::vector<Jet> select_sixb_jets_maxbtag        (NanoAODTree& nat, EventInfo& ei, const std::vector<Jet>& in_jets); // by b tag (highest first)
  std::vector<Jet> select_sixb_jets_maxbtag_highpT (NanoAODTree& nat, EventInfo& ei, const std::vector<Jet>& in_jets, int nleadbtag);


  // reorder the collection of the input jets according to the bias pt sort order (b tag groups + pt order inside each group) - used by select_sixb_jets_bias_pt_sort
  std::vector<Jet> bias_pt_sort_jets (NanoAODTree &nat, EventInfo& ei, const std::vector<Jet> &in_jets);

  ////////////////////////////////////////////////////
  /// compute high-level properties
  ////////////////////////////////////////////////////

  void compute_event_shapes(NanoAODTree &nat, EventInfo& ei, const std::vector<Jet> &in_jets);

  ////////////////////////////////////////////////////
  /// other jet utilities
  ////////////////////////////////////////////////////

  // counts how many valid gen higgs are in the in_dijets collection
  int n_gjmatched_in_dijetcoll(const std::vector<DiJet>& in_dijets);

  // counts how many of the valid genjets in the ei (matched to b quarks) are in the in_jets collection
  int n_gjmatched_in_jetcoll(NanoAODTree& nat, EventInfo& ei, const std::vector<Jet>& in_jets);
  
  // counts how many of the valid gen higgs in the ei (matched to b quarks) are in the in_jets collection
  int n_ghmatched_in_jetcoll(NanoAODTree& nat, EventInfo& ei, const std::vector<Jet>& in_jets);

  // add match flags to the selected jets (from which H are the selected jets?)
  int get_jet_genmatch_flag (NanoAODTree& nat, EventInfo& ei, const Jet& jet); // -1: other, 0: HX, 1: HY1, 2: HY2
  void compute_seljets_genmatch_flags(NanoAODTree& nat, EventInfo& ei);

  // match signal to genjets
  // void match_signal_genjets(EventInfo& ei, std::vector<GenJet>& in_jets); // EDITED FOR CODE REVIEW - FIXME

  // match signal to recojets
  // void match_signal_recojets(EventInfo& ei, std::vector<Jet>& in_jets); // EDITED FOR CODE REVIEW - FIXME

  ////////////////////////////////////////////////////
  /// non-jet functions
  ////////////////////////////////////////////////////

  void select_leptons(NanoAODTree& nat, EventInfo& ei);

  void set_btag_WPs(std::vector<double> btag_wps) { btag_WPs = btag_wps; }

  ////////////////////////////////////////////////////
  /// parameter handling
  ////////////////////////////////////////////////////

  ParamsMap pmap;

  // template <typename T>
  // void insert_param (std::string name, T value);

  // template <typename T>
  // T get_param (std::string name);

  // bool has_param (std::string name) {
  //   return (params_.find(name) != params_.end());
  // }

private:

  std::vector<double> btag_WPs;

  bool debug_ = false;
	
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
	
  // loops on targets, and assigns value to the first element of target that is found to be uninitialized
  // returns false if none could be assigned, else return true
  // if throw = true, throws an error if none could be assigned
  template <typename T>
  bool assign_to_uninit(T value, std::initializer_list<boost::optional<T>*> targets, bool do_throw = true);

  template <typename T>
  bool checkBit(T value, int bitpos) {T unit = 1; return value & (unit << bitpos);}

  // finds the index of the jet that was matched in nanoAOD to the input genjet
  int find_jet_from_genjet (NanoAODTree& nat, const GenJet& gj);
};


template <typename T>
bool SixB_functions::assign_to_uninit(T value, std::initializer_list<boost::optional<T>*> targets, bool do_throw)
{
  for (boost::optional<T>* tar : targets) {
    if (!(*tar)) {
      *tar = value;
      return true;
    }
  }
  if (do_throw)
    throw std::runtime_error("could not assign to uninit");
  return false;
}

// template <typename T>
// void SixB_functions::insert_param (std::string name, T value)
// {
//   if (has_param(name)){
//     std::string msg = std::string("SixB_functions : parameter ") + name + std::string(" already exists");
//     throw std::runtime_error(msg);
//   }
//   params_[name] = value;
// }

// template <typename T>
// T SixB_functions::get_param (std::string name)
// {
//   T ret = std::any_cast<T>(params_[name]);
//   return ret;
// }

#endif //SIXB_FUNCTIONS_H

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

#include "EvalNN.h"

class SixB_functions{
    
public:

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
	
  void match_genjets_to_reco(std::vector<GenJet>& genjets,std::vector<Jet>& recojets);

  ////////////////////////////////////////////////////
  /// jet selection functions
  ////////////////////////////////////////////////////

  // create a vector with all jets in the event
  std::vector<GenJet> get_all_genjets(NanoAODTree& nat);
	
  // create a vector with all jets in the event
  std::vector<Jet> get_all_jets(NanoAODTree& nat);

  // create a vector with all preselected jets in the event
  std::vector<Jet> preselect_jets(NanoAODTree& nat, const std::vector<Jet>& in_jets);

  // select up to six jet candidates out of the input jets
  std::vector<Jet> select_sixb_jets(NanoAODTree& nat, const std::vector<Jet>& in_jets);

  // two most b tagged jets for ttbar events
  std::vector<Jet> select_ttbar_jets(NanoAODTree &nat, EventInfo& ei, const std::vector<Jet> &in_jets);

  // pair the jets and assign them into the 6b candidates - will be stored in the EventInfo
  void pair_jets(NanoAODTree& nat, EventInfo& ei, const std::vector<Jet>& in_jets);

  // get the local idx in the supset for each jet in the subset
  std::vector<int> match_local_idx(std::vector<Jet>& subset,std::vector<Jet>& supset);

  // sort jets with btag bias pt ordering
  void btag_bias_pt_sort(std::vector<Jet>& in_jets);

  // sort jets with pt regressed ordering
  void pt_sort(std::vector<Jet>& in_jets);

  // pass event if jet collection passes input pt and btag cuts
  bool pass_jet_cut(Cutflow& cutflow, const std::vector<double> pt_cuts,const std::vector<int> btagWP_cuts,const std::vector<Jet> &in_jets);

  // create vector of all higgs resonances 
  std::vector<DiJet> get_tri_higgs_D_HHH(std::vector<Jet>& in_jets);

  std::vector<Jet> get_6jet_NN(EventInfo& ei,std::vector<Jet>& in_jets,EvalNN& n_6j_classifier);
  std::vector<DiJet> get_2jet_NN(EventInfo& ei,std::vector<Jet>& in_jets,std::vector<Jet>& sup_jets,EvalNN& n_2j_classifier);
  std::vector<DiJet> get_tri_higgs_NN(EventInfo& ei,std::vector<Jet>& in_jets,EvalNN& n_6j_classifier,EvalNN& n_2j_classifier);

  // passes event if all dijets mass is greater than 30 from higgs mass
  bool pass_higgs_cr(const std::vector<DiJet>& in_dijets);

  ////////////////////////////////////////////////////
  /// other jet utilities
  ////////////////////////////////////////////////////

  // counts how many of the valid genjets in the ei (matched to b quarks) are in the in_jets collection
  int n_gjmatched_in_jetcoll(NanoAODTree& nat, EventInfo& ei, const std::vector<Jet>& in_jets);
	
  // match signal to genjets
  void match_signal_genjets(EventInfo& ei, std::vector<GenJet>& in_jets);
	
  // match signal to recojets
  void match_signal_recojets(EventInfo& ei, std::vector<Jet>& in_jets);

  ////////////////////////////////////////////////////
  /// non-jet functions
  ////////////////////////////////////////////////////

  void select_leptons(NanoAODTree& nat, EventInfo& ei);

  void set_btag_WPs(std::vector<double> btag_wps) { btag_WPs = btag_wps; }
private:

  std::vector<double> btag_WPs;
	
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

  ////////////////////////////////////////////////////
  /// jet pairing functions
  ////////////////////////////////////////////////////

  // just pair jets as they are incoming - for debug
  std::tuple<CompositeCandidate, CompositeCandidate, CompositeCandidate> pair_passthrough (std::vector<Jet> jets);


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

#endif //SIXB_FUNCTIONS_H

#ifndef SKIM_FUNCTIONS_H
#define SKIM_FUNCTIONS_H

#include "DirectionalCut.h"
#include "NanoAODTree.h"
#include "EventInfo.h"
#include "Cutflow.h"

#include "Electron.h"
#include "Muon.h"
#include "Jet.h"
#include "FatJet.h"
#include "GenJet.h"
#include "GenJetAK8.h"
#include "SubGenJetAK8.h"
#include "GenPart.h"
#include "CompositeCandidate.h"
#include "DiJet.h"
#include "Timer.h"

#include "CfgParser.h"

#include "ParamsMap.h"

#include <any>
#include <unordered_map>
#include <string>
#include <iostream>

using namespace std;

  /**
   * @brief Template class for storing general event methods and virtual methods to be overidden for skim specific things
   * Any class with the virtual keyword can be and should be overriden in a child class
   * 
   */
class Skim_functions
{

public:

  ////////////////////////////////////////////////////
  /// Common Methods
  
  void set_debug(bool debug) { debug_ = debug; }
  void set_timer(Timer* timer) { loop_timer = timer; }
  
  /**
   * @brief Copy general event info to ei
   * 
   * @param nat NanoAODTree being processed
   * @param ei EventInfo class to store values
   * @param is_mc Flag to store MC specific values
   */
  void copy_event_info(NanoAODTree &nat, EventInfo &ei, bool is_mc);

  virtual bool is_blinded(NanoAODTree &nat, EventInfo &ei, bool is_data) { return false;  };

  ////////////////////////////////////////////////////
  /// jet selection functions
  ////////////////////////////////////////////////////

  // create a vector with all jets in the event
  std::vector<GenJet> get_all_genjets(NanoAODTree &nat);
  
  // create a vector with all gen subjets of fatjets in the event
  std::vector<SubGenJetAK8> get_all_subgenjets(NanoAODTree &nat);
  
  // create a vector with all gen fatjets in the event
  std::vector<GenJetAK8> get_all_genfatjets(NanoAODTree &nat);
  
  // create a vector with all fatjets in the event
  std::vector<FatJet> get_all_fatjets(NanoAODTree &nat);
  
  // create a vector with all jets in the event
  std::vector<Jet> get_all_jets(NanoAODTree &nat);

  // create a vector with all preselected jets in the event (minimal pt/eta/id requirements)
  std::vector<Jet> preselect_jets(NanoAODTree &nat, EventInfo& ei, const std::vector<Jet> &in_jets);

  std::vector<Jet> btag_sort_jets(NanoAODTree &nat, EventInfo& ei, const std::vector<Jet> &in_jets);

  std::vector<Jet> pt_sort_jets(NanoAODTree &nat, EventInfo& ei, const std::vector<Jet> &in_jets);
  
  // reorder the collection of the input jets according to the bias pt sort order (b tag groups + pt order inside each group) - used by select_sixb_jets_bias_pt_sort
  std::vector<Jet> bias_pt_sort_jets (NanoAODTree &nat, EventInfo& ei, const std::vector<Jet> &in_jets);

  
  ////////////////////////////////////////////////////
  /// compute high-level properties
  ////////////////////////////////////////////////////

  void compute_event_shapes(NanoAODTree &nat, EventInfo &ei, const std::vector<Jet> &in_jets);
  
  // get the local idx in the supset for each jet in the subset
  std::vector<int> match_local_idx(std::vector<Jet>& subset,std::vector<Jet>& supset);
  
  void GetMatchedPairs(const double dR_match, std::vector<GenPart*>& quarks, std::vector<GenJet>& genjets,
                       std::vector<GenPart*>& matched_quarks, std::vector<GenJet>& matched_genjets);
  
  void GetMatchedPairs(const double dR_match, std::vector<GenPart*>& quarks, std::vector<GenJetAK8>& genfatjets,
		       std::vector<GenPart*>& matched_quarks, std::vector<GenJetAK8>& matched_genfatjets);
  
  void match_genjets_to_reco(NanoAODTree &nat, EventInfo& ei,std::vector<GenJet>& in_gen,std::vector<Jet>& in_reco);
  
  double getPFHT(NanoAODTree& nat, EventInfo& ei);

  ////////////////////////////////////////////////////
  /// non-jet functions
  ////////////////////////////////////////////////////
  
  std::vector<Electron> select_electrons(CfgParser &config, NanoAODTree &nat, EventInfo &ei);
  std::vector<Muon> select_muons(CfgParser &config, NanoAODTree &nat, EventInfo &ei);
  
  void set_btag_WPs(std::vector<double> btag_wps) { btag_WPs = btag_wps; }

  bool checkHEMissue(EventInfo& ei, const std::vector<Jet> &jets);

  void get_puid_sf(EventInfo& ei, const std::vector<Jet> &jets, string puid_sf_file, string year);
  
  ////////////////////////////////////////////////////
  /// parameter handling
  ////////////////////////////////////////////////////

  ParamsMap pmap;

  ////////////////////////////////////////////////////
  /// Start virtual methods to be overidden

  virtual void Print() {
    cout << "[INFO] ... Using Skim_functions" << endl; 
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
  virtual void initialize_params_from_cfg(CfgParser &cfgr);

  /**
   * @brief Initialize functions for skim as defined in config file
   * This method should be overriden 
   * @param outputFile .root output file
   */
  virtual void initialize_functions(TFile &outputFile) {};

  ////////////////////////////////////////////////////
  /// gen objects functions
  ////////////////////////////////////////////////////
  /**
   * @brief Select all gen b-quarks
   */
  std::vector<GenPart> select_b_quarks(NanoAODTree &nat, EventInfo &ei);

  /**
   * @brief Select important gen particles and save them to ei
   * This method should be overriden 
   * @param nat NanoAODTree being processed
   * @param ei EventInfo class to store values
   */
  virtual void select_gen_particles(NanoAODTree &nat, EventInfo &ei) {};

  /**
   * @brief Match selected gen bs to gen jets
   * This method should be overriden 
   * @param nat NanoAODTree being processed
   * @param ei EventInfo class to store values
   * @param ensure_unique if true, ensures that a gen jet is not matched to two different partons
  // otherwise it will match to the closest parton found
   */
  virtual void match_genbs_to_genjets(NanoAODTree &nat, EventInfo &ei, bool ensure_unique = true) {};
  
  /**
   * @brief Match selected gen bs to gen fatjets
   * This method should be overriden
   * @param nat NanoAODTree being processed 
   * @param ei EventInfo class to store values 
   * @param ensure_unique if true, ensures that a gen fatjet is not matched to two different partons
   // otherwise it will match to the closest parton found 
   */
  virtual void match_genbs_to_genfatjets(NanoAODTree &nat, EventInfo &ei, bool ensure_unique = true) {};
  
  /**
   * @brief Match genjets associacted to a gen b quark to a reco jet
   * This method should be overriden 
   * @param nat NanoAODTree being processed
   * @param ei EventInfo class to store values
   */
  virtual void match_genbs_genjets_to_reco(NanoAODTree &nat, EventInfo &ei) {};
  
  /**
   * @brief Match genfatjets associated to a gen b quark to a reco fatjet
   * This method should be overriden
   * @param nat NanoAODTree being processed
   * @param ei EventInfo class to store values
   */
  virtual void match_genbs_genfatjets_to_reco(NanoAODTree &nat, EventInfo &ei) {};

  /**
   * @brief Match signal objects to reco in_jets collection and saving ID to signalId
   * This method should be overriden 
   * @param nat NanoAODTree being processed
   * @param ei EventInfo class to store values
   * @param in_jets Reco Jet collection to match with
   */
  virtual void match_signal_recojets(NanoAODTree &nat, EventInfo &ei, std::vector<Jet> &in_jets) {};

  /**
   * @brief Match signal objects to gen in_jets collection and saving ID to signalId
   * This method should be overriden 
   * @param nat NanoAODTree being processed
   * @param ei EventInfo class to store values
   * @param in_jets Gen Jet collection to match with
   */
  virtual void match_signal_genjets(NanoAODTree &nat, EventInfo &ei, std::vector<GenJet> &in_jets){};

  // select up to six jet candidates out of the input jets - configurable to run various selection algos
  /**
   * @brief Select jet candidates - configureable to run various selection algos defined in config
   * This method should be overriden 
   * @param nat NanoAODTree being processed
   * @param ei EventInfo class to store values
   * @param in_jets List of jets to select from
   * @return std::vector<Jet> of selected jets
   */
  virtual std::vector<Jet> select_jets(NanoAODTree &nat, EventInfo &ei, const std::vector<Jet> &in_jets) { return in_jets; };

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
  virtual void pair_jets(NanoAODTree &nat, EventInfo &ei, const std::vector<Jet> &in_jets) {};

  /**
   * @brief Calculate all di-jet pairings for input list of jets
   * 
   * @param nat  NanoAODTree being processed
   * @param ei  EventInfo class to store values
   * @param in_jets  List of jets to pair
   * @return std::vector<DiJet> of dijets 
   */
  std::vector<DiJet> make_dijets(NanoAODTree &nat, EventInfo &ei, const std::vector<Jet> &in_jets);

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
  virtual int n_gjmatched_in_jetcoll(NanoAODTree &nat, EventInfo &ei, const std::vector<Jet> &in_jets) { return 0; };

  /**
   * @brief Count how many valid gen higgs in the ei are in the in_jets collection
   * This method should be overriden
   * @param nat NanoAODTree being processed
   * @param ei EventInfo class to store values
   * @param in_jets List of jets to to compare
   * @return int Number of valid gen higgs in in_jets
   */
  virtual int n_ghmatched_in_jetcoll(NanoAODTree &nat, EventInfo &ei, const std::vector<Jet> &in_jets) { return 0; };

  // add match flags to the selected jets (from which H are the selected jets?)
  /**
   * @brief Returns ID of the gen higgs this jet is from
   * This method should be overriden
   * @param nat NanoAODTree being processed
   * @param ei EventInfo class to store values
   * @param jet 
   * @return int ID of the gen higgs this jet is from
   */
  virtual int get_jet_genmatch_flag(NanoAODTree &nat, EventInfo &ei, const Jet &jet) { return 0; }; // -1: other, 0: HX, 1: HY1, 2: HY2

  /**
   * @brief Get the ID of the gen higgs each selected jet in ei, stores in ei
   * 
   * @param nat NanoAODTree being processed
   * @param ei EventInfo class to store values
   */
  virtual void compute_seljets_genmatch_flags(NanoAODTree &nat, EventInfo &ei) {};

  virtual void compute_seljets_btagmulti(NanoAODTree &nat, EventInfo &ei){};

protected:
  std::vector<double> btag_WPs;

  bool debug_ = false;
  Timer* loop_timer;

  // loops on targets, and assigns value to the first element of target that is found to be uninitialized
  // returns false if none could be assigned, else return true
  // if throw = true, throws an error if none could be assigned
  template <typename T>
  bool assign_to_uninit(T value, std::initializer_list<boost::optional<T> *> targets, bool do_throw = true);

  template <typename T>
  bool checkBit(T value, int bitpos)
  {
    T unit = 1;
    return value & (unit << bitpos);
  }
  
  // finds the index of the fatjet that was matched in NanoAOD to the input gen fatjet
  int find_fatjet_from_genfatjet(NanoAODTree &nat, const GenJetAK8 &gj);
  
  // finds the index of the jet that was matched in nanoAOD to the input genjet
  int find_jet_from_genjet(NanoAODTree &nat, const GenJet &gj);
};

template <typename T>
bool Skim_functions::assign_to_uninit(T value, std::initializer_list<boost::optional<T> *> targets, bool do_throw)
{
  for (boost::optional<T> *tar : targets)
  {
    if (!(*tar))
    {
      *tar = value;
      return true;
    }
  }
  if (do_throw)
    throw std::runtime_error("could not assign to uninit");
  return false;
}


// template <typename T>
// void Skim_functions::insert_param (std::string name, T value)
// {
//   if (has_param(name)){
//     std::string msg = std::string("Skim_functions : parameter ") + name + std::string(" already exists");
//     throw std::runtime_error(msg);
//   }
//   params_[name] = value;
// }

// template <typename T>
// T Skim_functions::get_param (std::string name)
// {
//   T ret = std::any_cast<T>(params_[name]);
//   return ret;
// }

#endif // SKIM_FUNCTIONS_H

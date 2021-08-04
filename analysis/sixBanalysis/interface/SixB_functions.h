#ifndef SIXB_FUNCTIONS_H
#define SIXB_FUNCTIONS_H

#include "NanoAODTree.h"
#include "EventInfo.h"

#include "Jet.h"
#include "GenJet.h"
#include "GenPart.h"
#include "CompositeCandidate.h"

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

	// pass event if jet collection passes input pt and btag cuts
	bool pass_jet_cut(const std::vector<double> pt_cuts,const std::vector<int> btagWP_cuts,const std::vector<Jet> &in_jets);

	// create vector of all higgs resonances 
	std::vector<p4_t> get_all_higgs_pairs(std::vector<Jet>& in_jets);

	// passes event if all dijets mass is greater than 30 from higgs mass
	bool pass_higgs_cr(const std::vector<p4_t>& in_dijets);

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

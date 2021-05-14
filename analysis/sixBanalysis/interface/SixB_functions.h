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
        void copy_event_info(NanoAODTree& nat, EventInfo& ei);
        
        // select the gen-level six b candidates (bs, bosons)
        void select_gen_particles(NanoAODTree& nat, EventInfo& ei);

        // match the selected gen b to gen jets
        // if ensure_unique = true, ensures that a gen jet is not matched to two different partons
        // otherwise it will match to the closest parton found
        void match_genbs_to_genjets(NanoAODTree& nat, EventInfo& ei, bool ensure_unique = true);

        // match the genjets associated to the 6 gen b quarks to reco jets
        void match_genbs_genjets_to_reco(NanoAODTree& nat, EventInfo& ei);

        ////////////////////////////////////////////////////
        /// jet selection functions
        ////////////////////////////////////////////////////

        int njets_preselections (const std::vector<Jet>& in_jets);

        // create a vector with all jets in the event
        std::vector<Jet> get_all_jets(NanoAODTree& nat);
        std::vector<float> get_all_jet_pt(const std::vector<Jet>& in_jets);
        std::vector<float> get_all_jet_eta(const std::vector<Jet>& in_jets);
        std::vector<float> get_all_jet_phi(const std::vector<Jet>& in_jets);
        std::vector<float> get_all_jet_mass(const std::vector<Jet>& in_jets);
        std::vector<float> get_all_jet_btag(const std::vector<Jet>& in_jets);

        // create a vector with all jets in the event
        std::vector<Jet> preselect_jets(NanoAODTree& nat, const std::vector<Jet>& in_jets);

        // select up to six jet candidates out of the input jets
        std::vector<Jet> select_sixb_jets(NanoAODTree& nat, const std::vector<Jet>& in_jets);

        // pair the jets and assign them into the 6b candidates - will be stored in the EventInfo
        void pair_jets(NanoAODTree& nat, EventInfo& ei, const std::vector<Jet>& in_jets);

        ////////////////////////////////////////////////////
        /// other jet utilities
        ////////////////////////////////////////////////////

        // counts how many of the valid genjets in the ei (matched to b quarks) are in the in_jets collection
        int n_gjmatched_in_jetcoll(NanoAODTree& nat, EventInfo& ei, const std::vector<Jet>& in_jets);


    private:
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
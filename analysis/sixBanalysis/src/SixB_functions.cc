#include "SixB_functions.h"
#include "Math/VectorUtil.h"

#include <iostream>
#include <tuple>

#include "Electron.h"
#include "Muon.h"

using namespace std;

void SixB_functions::copy_event_info(NanoAODTree& nat, EventInfo& ei, bool is_mc)
{
    ei.Run     = *(nat.run);
    ei.LumiSec = *(nat.luminosityBlock);
    ei.Event   = *(nat.event);

    ei.n_other_pv                    = *(nat.nOtherPV);
    ei.rhofastjet_all                = *(nat.fixedGridRhoFastjetAll);

    // mc-only
    if (is_mc){
        ei.n_pu       = *(nat.Pileup_nPU);
        ei.n_true_int = *(nat.Pileup_nTrueInt);
    }
}

void SixB_functions::select_gen_particles(NanoAODTree& nat, EventInfo& ei)
{
    for (uint igp = 0; igp < *(nat.nGenPart); ++igp)
    {
        GenPart gp (igp, &nat);
        int apdgid = abs(get_property(gp, GenPart_pdgId));
        
        // X
        if (apdgid == 45) {
            if (gp.isFirstCopy())
                ei.gen_X_fc = gp;
            else if (gp.isLastCopy())
                ei.gen_X = gp;
        }

        // Y
        if (apdgid == 35 && gp.isLastCopy())
            ei.gen_Y = gp;

        // H
        if (apdgid == 25 && gp.isLastCopy()) {
            GenPart mother (get_property(gp, GenPart_genPartIdxMother), &nat);
            int amothpdgid = abs(get_property(mother, GenPart_pdgId));
            if (amothpdgid == 45)
                ei.gen_HX = gp;
            else if (amothpdgid == 35)
                assign_to_uninit(gp, {&ei.gen_HY1, &ei.gen_HY2} );
        }

        // b
        if (apdgid == 5 && gp.isFirstCopy()) {
            int moth_idx = get_property(gp, GenPart_genPartIdxMother);
            if (moth_idx >= 0) {
                GenPart mother (moth_idx, &nat);
                int amothpdgid = abs(get_property(mother, GenPart_pdgId));
                // in the LHE the mother always comes before the daughters, so it is guaranteed to have been found already
                if (amothpdgid == 25){
                    if (ei.gen_HX && moth_idx == ei.gen_HX->getIdx())
                        assign_to_uninit(gp, {&ei.gen_HX_b1, &ei.gen_HX_b2} );
                    if (ei.gen_HY1 && moth_idx == ei.gen_HY1->getIdx())
                        assign_to_uninit(gp, {&ei.gen_HY1_b1, &ei.gen_HY1_b2} );
                    if (ei.gen_HY2 && moth_idx == ei.gen_HY2->getIdx())
                        assign_to_uninit(gp, {&ei.gen_HY2_b1, &ei.gen_HY2_b2} );
                }
            }
        }
    }

    // reorder objects according to pt
    if (ei.gen_HY1->P4().Pt() < ei.gen_HY2->P4().Pt()){
        std::swap(ei.gen_HY1,    ei.gen_HY2);
        std::swap(ei.gen_HY1_b1, ei.gen_HY2_b1);
        std::swap(ei.gen_HY1_b2, ei.gen_HY2_b2);
    }

    if (ei.gen_HX_b1->P4().Pt() < ei.gen_HX_b2->P4().Pt())
        std::swap(ei.gen_HX_b1, ei.gen_HX_b2);
    if (ei.gen_HY1_b1->P4().Pt() < ei.gen_HY1_b2->P4().Pt())
        std::swap(ei.gen_HY1_b1, ei.gen_HY1_b2);
    if (ei.gen_HY2_b1->P4().Pt() < ei.gen_HY2_b2->P4().Pt())
        std::swap(ei.gen_HY2_b1, ei.gen_HY2_b2);

    return;
}


// match the selected gen b to gen jets
void SixB_functions::match_genbs_to_genjets(NanoAODTree& nat, EventInfo& ei, bool ensure_unique)
{
    const double dR_match = 0.4;

    std::vector<GenPart*> bs_to_match = {
        ei.gen_HX_b1.get_ptr(),
        ei.gen_HX_b2.get_ptr(),
        ei.gen_HY1_b1.get_ptr(),
        ei.gen_HY1_b2.get_ptr(),
        ei.gen_HY2_b1.get_ptr(),
        ei.gen_HY2_b2.get_ptr()
    };

    std::vector<int> genjet_idxs;

    std::vector<GenJet> genjets;
    for (unsigned int igj = 0; igj < *(nat.nGenJet); ++igj){
        GenJet gj (igj, &nat);
        genjets.push_back(gj);
    }

    for (GenPart* b : bs_to_match){
        std::vector<std::tuple<double, int, int>> matched_gj; // dR, idx in nanoAOD, idx in local coll
        for (unsigned int igj = 0; igj < genjets.size(); ++igj){
            GenJet& gj = genjets.at(igj);
            double dR = ROOT::Math::VectorUtil::DeltaR(b->P4(), gj.P4());
            if (dR < dR_match)
                matched_gj.push_back(std::make_tuple(dR, gj.getIdx(), igj)); // save the idx in the nanoAOD collection to rebuild this after 
        }
        
        if (matched_gj.size() > 0){
            std::sort(matched_gj.begin(), matched_gj.end());
            auto best_match = matched_gj.at(0);
            genjet_idxs.push_back(std::get<1>(best_match));
            if (ensure_unique) // genjet already used, remove it from the input list
               genjets.erase(genjets.begin() + std::get<2>(best_match)); 
        }
        else
            genjet_idxs.push_back(-1);
    }

    // matched done, store in ei - use the map built above in bs_to_match to know the correspondence position <-> meaning
    if (genjet_idxs.at(0) >= 0) ei.gen_HX_b1_genjet  = GenJet(genjet_idxs.at(0), &nat);
    if (genjet_idxs.at(1) >= 0) ei.gen_HX_b2_genjet  = GenJet(genjet_idxs.at(1), &nat);
    if (genjet_idxs.at(2) >= 0) ei.gen_HY1_b1_genjet = GenJet(genjet_idxs.at(2), &nat);
    if (genjet_idxs.at(3) >= 0) ei.gen_HY1_b2_genjet = GenJet(genjet_idxs.at(3), &nat);
    if (genjet_idxs.at(4) >= 0) ei.gen_HY2_b1_genjet = GenJet(genjet_idxs.at(4), &nat);
    if (genjet_idxs.at(5) >= 0) ei.gen_HY2_b2_genjet = GenJet(genjet_idxs.at(5), &nat);

    return;
}

void SixB_functions::match_genbs_genjets_to_reco(NanoAODTree& nat, EventInfo& ei)
{
    int ij_gen_HX_b1_genjet  = (ei.gen_HX_b1_genjet  ? find_jet_from_genjet(nat, *ei.gen_HX_b1_genjet)  : -1); 
    int ij_gen_HX_b2_genjet  = (ei.gen_HX_b2_genjet  ? find_jet_from_genjet(nat, *ei.gen_HX_b2_genjet)  : -1); 
    int ij_gen_HY1_b1_genjet = (ei.gen_HY1_b1_genjet ? find_jet_from_genjet(nat, *ei.gen_HY1_b1_genjet) : -1); 
    int ij_gen_HY1_b2_genjet = (ei.gen_HY1_b2_genjet ? find_jet_from_genjet(nat, *ei.gen_HY1_b2_genjet) : -1); 
    int ij_gen_HY2_b1_genjet = (ei.gen_HY2_b1_genjet ? find_jet_from_genjet(nat, *ei.gen_HY2_b1_genjet) : -1); 
    int ij_gen_HY2_b2_genjet = (ei.gen_HY2_b2_genjet ? find_jet_from_genjet(nat, *ei.gen_HY2_b2_genjet) : -1); 

    if (ij_gen_HX_b1_genjet >= 0)  ei.gen_HX_b1_recojet  = Jet(ij_gen_HX_b1_genjet,  &nat);
    if (ij_gen_HX_b2_genjet >= 0)  ei.gen_HX_b2_recojet  = Jet(ij_gen_HX_b2_genjet,  &nat);
    if (ij_gen_HY1_b1_genjet >= 0) ei.gen_HY1_b1_recojet = Jet(ij_gen_HY1_b1_genjet, &nat);
    if (ij_gen_HY1_b2_genjet >= 0) ei.gen_HY1_b2_recojet = Jet(ij_gen_HY1_b2_genjet, &nat);
    if (ij_gen_HY2_b1_genjet >= 0) ei.gen_HY2_b1_recojet = Jet(ij_gen_HY2_b1_genjet, &nat);
    if (ij_gen_HY2_b2_genjet >= 0) ei.gen_HY2_b2_recojet = Jet(ij_gen_HY2_b2_genjet, &nat);

    // select unique occurences in vector
    // note : PAT tools already ensure that match is unique
    // https://github.com/cms-sw/cmssw/blob/master/PhysicsTools/PatAlgos/python/mcMatchLayer0/jetMatch_cfi.py
    // so the check below is redundant

    // std::vector<int> imatchs;
    // if (ij_gen_HX_b1_genjet >= 0)  imatchs.push_back(ij_gen_HX_b1_genjet);
    // if (ij_gen_HX_b2_genjet >= 0)  imatchs.push_back(ij_gen_HX_b2_genjet);
    // if (ij_gen_HY1_b1_genjet >= 0) imatchs.push_back(ij_gen_HY1_b1_genjet);
    // if (ij_gen_HY1_b2_genjet >= 0) imatchs.push_back(ij_gen_HY1_b2_genjet);
    // if (ij_gen_HY2_b1_genjet >= 0) imatchs.push_back(ij_gen_HY2_b1_genjet);
    // if (ij_gen_HY2_b2_genjet >= 0) imatchs.push_back(ij_gen_HY2_b2_genjet);

    // sort(imatchs.begin(), imatchs.end());
    // imatchs.erase(unique (imatchs.begin(), imatchs.end()), imatchs.end());
    // ei.gen_bs_N_reco_match = imatchs.size(); // number of different reco jets that are matched to gen jets

    int nmatched = 0;
    if (ij_gen_HX_b1_genjet >= 0)  nmatched += 1;
    if (ij_gen_HX_b2_genjet >= 0)  nmatched += 1;
    if (ij_gen_HY1_b1_genjet >= 0) nmatched += 1;
    if (ij_gen_HY1_b2_genjet >= 0) nmatched += 1;
    if (ij_gen_HY2_b1_genjet >= 0) nmatched += 1;
    if (ij_gen_HY2_b2_genjet >= 0) nmatched += 1;
    ei.gen_bs_N_reco_match = nmatched;

    // same as above, but apply acceptance cuts on the matched jets
    int nmatched_acc = 0;
    if (ei.gen_HX_b1_recojet  && ei.gen_HX_b1_recojet->P4().Pt()  > 20 && std::abs(ei.gen_HX_b1_recojet->P4().Eta())  < 4.8) nmatched_acc += 1;
    if (ei.gen_HX_b2_recojet  && ei.gen_HX_b2_recojet->P4().Pt()  > 20 && std::abs(ei.gen_HX_b2_recojet->P4().Eta())  < 4.8) nmatched_acc += 1;
    if (ei.gen_HY1_b1_recojet && ei.gen_HY1_b1_recojet->P4().Pt() > 20 && std::abs(ei.gen_HY1_b1_recojet->P4().Eta()) < 4.8) nmatched_acc += 1;
    if (ei.gen_HY1_b2_recojet && ei.gen_HY1_b2_recojet->P4().Pt() > 20 && std::abs(ei.gen_HY1_b2_recojet->P4().Eta()) < 4.8) nmatched_acc += 1;
    if (ei.gen_HY2_b1_recojet && ei.gen_HY2_b1_recojet->P4().Pt() > 20 && std::abs(ei.gen_HY2_b1_recojet->P4().Eta()) < 4.8) nmatched_acc += 1;
    if (ei.gen_HY2_b2_recojet && ei.gen_HY2_b2_recojet->P4().Pt() > 20 && std::abs(ei.gen_HY2_b2_recojet->P4().Eta()) < 4.8) nmatched_acc += 1;
    ei.gen_bs_N_reco_match_in_acc = nmatched_acc;

    // now compute p4 sums to make the invariant mass of X - FIXME: can add more inv masses for the various cases
    p4_t p4_sum_matched (0,0,0,0);
    if (ei.gen_HX_b1_recojet) p4_sum_matched  += ei.gen_HX_b1_recojet->P4();
    if (ei.gen_HX_b2_recojet) p4_sum_matched  += ei.gen_HX_b2_recojet->P4();
    if (ei.gen_HY1_b1_recojet) p4_sum_matched += ei.gen_HY1_b1_recojet->P4();
    if (ei.gen_HY1_b2_recojet) p4_sum_matched += ei.gen_HY1_b2_recojet->P4();
    if (ei.gen_HY2_b1_recojet) p4_sum_matched += ei.gen_HY2_b1_recojet->P4();
    if (ei.gen_HY2_b2_recojet) p4_sum_matched += ei.gen_HY2_b2_recojet->P4();
    ei.gen_bs_match_recojet_minv = p4_sum_matched.M();

    p4_t p4_sum_matched_acc (0,0,0,0);
    if (ei.gen_HX_b1_recojet  && ei.gen_HX_b1_recojet->P4().Pt()  > 20 && std::abs(ei.gen_HX_b1_recojet->P4().Eta())  < 4.8) p4_sum_matched_acc += ei.gen_HX_b1_recojet->P4();
    if (ei.gen_HX_b2_recojet  && ei.gen_HX_b2_recojet->P4().Pt()  > 20 && std::abs(ei.gen_HX_b2_recojet->P4().Eta())  < 4.8) p4_sum_matched_acc += ei.gen_HX_b2_recojet->P4();
    if (ei.gen_HY1_b1_recojet && ei.gen_HY1_b1_recojet->P4().Pt() > 20 && std::abs(ei.gen_HY1_b1_recojet->P4().Eta()) < 4.8) p4_sum_matched_acc += ei.gen_HY1_b1_recojet->P4();
    if (ei.gen_HY1_b2_recojet && ei.gen_HY1_b2_recojet->P4().Pt() > 20 && std::abs(ei.gen_HY1_b2_recojet->P4().Eta()) < 4.8) p4_sum_matched_acc += ei.gen_HY1_b2_recojet->P4();
    if (ei.gen_HY2_b1_recojet && ei.gen_HY2_b1_recojet->P4().Pt() > 20 && std::abs(ei.gen_HY2_b1_recojet->P4().Eta()) < 4.8) p4_sum_matched_acc += ei.gen_HY2_b1_recojet->P4();
    if (ei.gen_HY2_b2_recojet && ei.gen_HY2_b2_recojet->P4().Pt() > 20 && std::abs(ei.gen_HY2_b2_recojet->P4().Eta()) < 4.8) p4_sum_matched_acc += ei.gen_HY2_b2_recojet->P4();
    ei.gen_bs_match_in_acc_recojet_minv = p4_sum_matched_acc.M();
}

int SixB_functions::get_jet_genmatch_flag (NanoAODTree& nat, EventInfo& ei, const Jet& jet)
{
    int ijet = jet.getIdx();
    if ( (ei.gen_HX_b1_recojet && ijet == ei.gen_HX_b1_recojet->getIdx())   || (ei.gen_HX_b2_recojet && ijet == ei.gen_HX_b2_recojet->getIdx()) )
        return 0; 
    if ( (ei.gen_HY1_b1_recojet && ijet == ei.gen_HY1_b1_recojet->getIdx()) || (ei.gen_HY1_b2_recojet && ijet == ei.gen_HY1_b2_recojet->getIdx()) )
        return 1; 
    if ( (ei.gen_HY2_b1_recojet && ijet == ei.gen_HY2_b1_recojet->getIdx()) || (ei.gen_HY2_b2_recojet && ijet == ei.gen_HY2_b2_recojet->getIdx()) )
        return 2; 
    return -1;
}

void SixB_functions::compute_seljets_genmatch_flags(NanoAODTree& nat, EventInfo& ei)
{
    // flags per jet
    ei.HX_b1_genHflag  = get_jet_genmatch_flag(nat, ei, *ei.HX_b1);
    ei.HX_b2_genHflag  = get_jet_genmatch_flag(nat, ei, *ei.HX_b2);
    ei.HY1_b1_genHflag = get_jet_genmatch_flag(nat, ei, *ei.HY1_b1);
    ei.HY1_b2_genHflag = get_jet_genmatch_flag(nat, ei, *ei.HY1_b2);
    ei.HY2_b1_genHflag = get_jet_genmatch_flag(nat, ei, *ei.HY2_b1);
    ei.HY2_b2_genHflag = get_jet_genmatch_flag(nat, ei, *ei.HY2_b2);

    // flags per event
    int nsel_from_H = 0;
    if (ei.HX_b1_genHflag > -1)  nsel_from_H += 1;
    if (ei.HX_b2_genHflag > -1)  nsel_from_H += 1;
    if (ei.HY1_b1_genHflag > -1) nsel_from_H += 1;
    if (ei.HY1_b2_genHflag > -1) nsel_from_H += 1;
    if (ei.HY2_b1_genHflag > -1) nsel_from_H += 1;
    if (ei.HY2_b2_genHflag > -1) nsel_from_H += 1;
    ei.nsel_from_H = nsel_from_H; // number of selected jets that are from H
}

int SixB_functions::find_jet_from_genjet (NanoAODTree& nat, const GenJet& gj)
{
    const int gjidx = gj.getIdx();
    for (unsigned int ij = 0; ij < *(nat.nJet); ++ij){
        Jet jet (ij, &nat);
        int igj = get_property(jet, Jet_genJetIdx);
        if (igj == gjidx)
            return ij;
    }
    return -1;
}

int SixB_functions::njets_preselections (const std::vector<Jet>& in_jets)
{
    const double pt_min  = 30.;
    const double eta_max = 2.4;
    int count = 0;
    for (unsigned int ij = 0; ij < in_jets.size(); ++ij){
        const Jet& jet = in_jets.at(ij);
        if (jet.P4().Pt()            <= pt_min)  continue;
        if (std::abs(jet.P4().Eta()) >= eta_max) continue;
        count++;
    }
    return count;
}

std::vector<Jet> SixB_functions::get_all_jets(NanoAODTree& nat)
{
    std::vector<Jet> jets;
    jets.reserve(*(nat.nJet));
    
    for (unsigned int ij = 0; ij < *(nat.nJet); ++ij){
        Jet jet (ij, &nat);
        jets.emplace_back(jet);
    }
    return jets;
}

std::vector<float> SixB_functions::get_all_jet_pt(const std::vector<Jet>& in_jets)
{
    std::vector<float> jets;
    jets.reserve(in_jets.size());

    const double pt_min  = 30.;
    const double eta_max = 2.4;
    
    for (unsigned int ij = 0; ij < in_jets.size(); ++ij){
        const Jet& jet = in_jets.at(ij);
        if (jet.P4().Pt()            <= pt_min)  continue;
        if (std::abs(jet.P4().Eta()) >= eta_max) continue;
        jets.emplace_back(jet.P4().Pt());
    }

    return jets;
}


std::vector<int> SixB_functions::get_all_jet_genidx(EventInfo& ei, const std::vector<Jet>& in_jets)
{
    std::vector<int> jets;
    jets.reserve(in_jets.size());

    int id1 = -1;
    int id2 = -1;
    int id3 = -1;
    int id4 = -1;
    int id5 = -1;
    int id6 = -1;

    if (ei.gen_HX_b1_recojet) {id1 = ei.gen_HX_b1_recojet->getIdx();}
    if (ei.gen_HX_b2_recojet) {id2 = ei.gen_HX_b2_recojet->getIdx();}
    if (ei.gen_HY1_b1_recojet) {id3 = ei.gen_HY1_b1_recojet->getIdx();}
    if (ei.gen_HY1_b2_recojet) {id4 = ei.gen_HY1_b2_recojet->getIdx();}
    if (ei.gen_HY2_b1_recojet) {id5 = ei.gen_HY2_b1_recojet->getIdx();}
    if (ei.gen_HY2_b2_recojet) {id6 = ei.gen_HY2_b2_recojet->getIdx();}

    const double pt_min  = 30.;
    const double eta_max = 2.4;
    
    for (unsigned int ij = 0; ij < in_jets.size(); ++ij){
        const Jet& jet = in_jets.at(ij);
        if (jet.P4().Pt()            <= pt_min)  continue;
        if (std::abs(jet.P4().Eta()) >= eta_max) continue;

        // std::cout << jet.getIdx() << std::endl;

        if (id1 == jet.getIdx()) {jets.emplace_back(0);}
        else if (id2 == jet.getIdx()) {jets.emplace_back(1);}
        else if (id3 == jet.getIdx()) {jets.emplace_back(2);}
        else if (id4 == jet.getIdx()) {jets.emplace_back(3);}
        else if (id5 == jet.getIdx()) {jets.emplace_back(4);}
        else if (id6 == jet.getIdx()) {jets.emplace_back(5);}
        else {jets.emplace_back(-1);}
    }

    return jets;
}


std::vector<float> SixB_functions::get_all_jet_eta(const std::vector<Jet>& in_jets)
{
    std::vector<float> jets;
    jets.reserve(in_jets.size());

    const double pt_min  = 30.;
    const double eta_max = 2.4;
    
    for (unsigned int ij = 0; ij < in_jets.size(); ++ij){
        const Jet& jet = in_jets.at(ij);
        if (jet.P4().Pt()            <= pt_min)  continue;
        if (std::abs(jet.P4().Eta()) >= eta_max) continue;
        jets.emplace_back(jet.P4().Eta());
    }
    return jets;
}

std::vector<float> SixB_functions::get_all_jet_phi(const std::vector<Jet>& in_jets)
{
    std::vector<float> jets;
    jets.reserve(in_jets.size());

    const double pt_min  = 30.;
    const double eta_max = 2.4;
    
    for (unsigned int ij = 0; ij < in_jets.size(); ++ij){
        const Jet& jet = in_jets.at(ij);
        if (jet.P4().Pt()            <= pt_min)  continue;
        if (std::abs(jet.P4().Eta()) >= eta_max) continue;
        jets.emplace_back(jet.P4().Phi());
    }
    return jets;
}

std::vector<float> SixB_functions::get_all_jet_mass(const std::vector<Jet>& in_jets)
{
    std::vector<float> jets;
    jets.reserve(in_jets.size());

    const double pt_min  = 30.;
    const double eta_max = 2.4;
    
    for (unsigned int ij = 0; ij < in_jets.size(); ++ij){
        const Jet& jet = in_jets.at(ij);
        if (jet.P4().Pt()            <= pt_min)  continue;
        if (std::abs(jet.P4().Eta()) >= eta_max) continue;
        jets.emplace_back(jet.P4().M());
    }
    return jets;
}

std::vector<float> SixB_functions::get_all_jet_btag(const std::vector<Jet>& in_jets)
{
    std::vector<float> jets;
    jets.reserve(in_jets.size());

    const double pt_min  = 30.;
    const double eta_max = 2.4;
    
    for (unsigned int ij = 0; ij < in_jets.size(); ++ij){
        const Jet& jet = in_jets.at(ij);
        if (jet.P4().Pt()            <= pt_min)  continue;
        if (std::abs(jet.P4().Eta()) >= eta_max) continue;
        float btag = get_property (jet, Jet_btagDeepFlavB);
        jets.emplace_back(btag);
    }
    return jets;
}

std::vector<float> SixB_functions::get_all_jet_qgl(const std::vector<Jet>& in_jets)
{
    std::vector<float> jets;
    jets.reserve(in_jets.size());

    const double pt_min  = 30.;
    const double eta_max = 2.4;
    
    for (unsigned int ij = 0; ij < in_jets.size(); ++ij){
        const Jet& jet = in_jets.at(ij);
        if (jet.P4().Pt()            <= pt_min)  continue;
        if (std::abs(jet.P4().Eta()) >= eta_max) continue;
        float qgl = get_property (jet, Jet_qgl);
        jets.emplace_back(qgl);
    }
    return jets;
}

std::vector<int> SixB_functions::get_all_jet_partonFlavour(const std::vector<Jet>& in_jets)
{
    std::vector<int> jets;
    jets.reserve(in_jets.size());

    const double pt_min  = 30.;
    const double eta_max = 2.4;
    
    for (unsigned int ij = 0; ij < in_jets.size(); ++ij){
        const Jet& jet = in_jets.at(ij);
        if (jet.P4().Pt()            <= pt_min)  continue;
        if (std::abs(jet.P4().Eta()) >= eta_max) continue;
        int partonFlavour = get_property (jet, Jet_partonFlavour);
        jets.emplace_back(partonFlavour);
    }
    return jets;
}

std::vector<int> SixB_functions::get_all_jet_hadronFlavour(const std::vector<Jet>& in_jets)
{
    std::vector<int> jets;
    jets.reserve(in_jets.size());

    const double pt_min  = 30.;
    const double eta_max = 2.4;
    
    for (unsigned int ij = 0; ij < in_jets.size(); ++ij){
        const Jet& jet = in_jets.at(ij);
        if (jet.P4().Pt()            <= pt_min)  continue;
        if (std::abs(jet.P4().Eta()) >= eta_max) continue;
        int hadronFlavour = get_property (jet, Jet_hadronFlavour);
        jets.emplace_back(hadronFlavour);
    }
    return jets;
}

std::vector<Jet> SixB_functions::preselect_jets(NanoAODTree& nat, const std::vector<Jet>& in_jets)
{
    // FIXME: make these selections configurable
    const double pt_min  = 30.;
    const double eta_max = 2.4;
    const int    pf_id   = 1;
    const int    pu_id   = 1;

    std::vector<Jet> out_jets;
    out_jets.reserve(in_jets.size());

    for (unsigned int ij = 0; ij < in_jets.size(); ++ij)
    {
        const Jet& jet = in_jets.at(ij);
        if (jet.P4().Pt()            <= pt_min)  continue;
        if (std::abs(jet.P4().Eta()) >= eta_max) continue;
        if (!checkBit(get_property(jet, Jet_jetId), pf_id)) continue;
        if (!checkBit(get_property(jet, Jet_puId),  pu_id)) continue;

        out_jets.emplace_back(jet);
    }

    return out_jets;
}

std::vector<Jet> SixB_functions::select_sixb_jets(NanoAODTree& nat, const std::vector<Jet>& in_jets)
{
    const std::string algo = "maxbtag"; // FIXME: make configurable from cfg

    if (algo == "maxbtag"){
        return select_sixb_jets_maxbtag(nat, in_jets);
    }

    else if (algo == "5btag_maxpt"){
        return select_sixb_jets_maxbtag_highpT(nat, in_jets, 5);
    }

    else if (algo == "4btag_maxpt"){
        return select_sixb_jets_maxbtag_highpT(nat, in_jets, 4);
    }

    throw std::runtime_error("jet sel algo not recognized");
}

std::vector<Jet> SixB_functions::select_sixb_jets_maxbtag(NanoAODTree& nat, const std::vector<Jet>& in_jets)
{
    std::vector<Jet> jets = in_jets;
    stable_sort(jets.begin(), jets.end(), [](const Jet& a, const Jet& b) -> bool {
            return ( get_property (a, Jet_btagDeepFlavB) > get_property (b, Jet_btagDeepFlavB) ); }
    ); // sort jet by deepjet score (highest to lowest)

    int n_out = std::min<int>(jets.size(), 6);
    jets.resize(n_out);

    // for (auto& jet : jets)
    //     std::cout << jet.P4().Pt() << " " << get_property (jet, Jet_btagDeepFlavB) << std::endl;
    // std::cout << std::endl << std::endl;

    return jets;
}

std::vector<Jet> SixB_functions::select_sixb_jets_maxbtag_highpT(NanoAODTree& nat, const std::vector<Jet>& in_jets, int nleadbtag)
{
    std::vector<Jet> jets = in_jets;
    stable_sort(jets.begin(), jets.end(), [](const Jet& a, const Jet& b) -> bool {
            return ( get_property (a, Jet_btagDeepFlavB) > get_property (b, Jet_btagDeepFlavB) ); }
    ); // sort jet by deepjet score (highest to lowest)

    int n_out_btag = std::min<int>(jets.size(), nleadbtag);
    std::vector<Jet> out_jets (jets.begin(), jets.begin()+n_out_btag); // copy the first N btag jets to the out vector

    std::vector<Jet>(jets.begin()+n_out_btag,jets.end()).swap(jets); // put into "jets" the remaining elements

    stable_sort(jets.begin(), jets.end(), [](const Jet& a, const Jet& b) -> bool {
            return ( a.P4().Pt() > b.P4().Pt() ); }
    ); // sort jet by pT (highest to lowest)

    int n_to_add = std::min<int>(jets.size(), 6-nleadbtag); // add at most 6-nleadbtag elements (if they are available)
    out_jets.insert(out_jets.end(), jets.begin(), jets.begin()+n_to_add);

    // std::cout << "   ---> IN JETS" << std::endl;
    // for (auto& jet : in_jets)
    //     std::cout << jet.P4().Pt() << " " << get_property (jet, Jet_btagDeepFlavB) << std::endl;
    // std::cout << std::endl << std::endl;

    // std::cout << "   ---> OUT JETS" << std::endl;
    // for (auto& jet : out_jets)
    //     std::cout << jet.P4().Pt() << " " << get_property (jet, Jet_btagDeepFlavB) << std::endl;
    // std::cout << std::endl << "-------------------------" << std::endl;

    return out_jets;
}


std::vector<Jet> SixB_functions::select_ttbar_jets(NanoAODTree &nat, EventInfo &ei, const std::vector<Jet> &in_jets)
{
    std::vector<Jet> jets = in_jets;
    stable_sort(jets.begin(), jets.end(), [](const Jet& a, const Jet& b) -> bool {
            return ( get_property (a, Jet_btagDeepFlavB) > get_property (b, Jet_btagDeepFlavB) ); }
    ); // sort jet by deepjet score (highest to lowest)

    if (jets.size() < 2)
        return jets;
    ei.bjet1 = jets.at(0);
    ei.bjet2 = jets.at(1);
    if (ei.bjet1->P4().Pt() < ei.bjet2->P4().Pt()) // sort by pt
        std::swap(ei.bjet1, ei.bjet2);

    return jets;

    // int n_out = std::min<int>(jets.size(), 6);
    // jets.resize(n_out);

    // for (auto& jet : jets)
    //     std::cout << jet.P4().Pt() << " " << get_property (jet, Jet_btagDeepFlavB) << std::endl;
    // std::cout << std::endl << std::endl;

    // return jets;

}


void SixB_functions::pair_jets(NanoAODTree& nat, EventInfo& ei, const std::vector<Jet>& in_jets)
{
    // FIXME: here a switch for the pairing algo - to be made configurable from the cfg file
    const std::string pairAlgo = "min_diag_distance";

    // call the desired algo - expected interface is input jets -> output 3 composite candidate HX, HY1. HY2
    // the order of HY1, HY2 and of the jets does not matter - they will be reordered after

    std::tuple<CompositeCandidate, CompositeCandidate, CompositeCandidate> reco_Hs;
    if (pairAlgo == "passthrough")
        reco_Hs = pair_passthrough(in_jets);

    if (pairAlgo == "min_diag_distance")
        reco_Hs = pair_min_diag_distance(in_jets);

    // reorder objects
    CompositeCandidate HX  = std::get<0>(reco_Hs);
    CompositeCandidate HY1 = std::get<1>(reco_Hs);
    CompositeCandidate HY2 = std::get<2>(reco_Hs);

    if (HY1.P4().Pt() < HY2.P4().Pt())
        std::swap(HY1, HY2);

    if (HX.getComponent1().P4().Pt() < HX.getComponent2().P4().Pt())
        HX.swapComponents();

    if (HY1.getComponent1().P4().Pt() < HY1.getComponent2().P4().Pt())
        HY1.swapComponents();

    if (HY2.getComponent1().P4().Pt() < HY2.getComponent2().P4().Pt())
        HY2.swapComponents();

    CompositeCandidate Y(HY1, HY2);
    CompositeCandidate X(Y, HX);

    ei.X = X;
    ei.Y = Y;

    ei.HX  = HX;
    ei.HY1 = HY1;
    ei.HY2 = HY2;

    ei.HX_b1  = static_cast<Jet&>(HX.getComponent1());
    ei.HX_b2  = static_cast<Jet&>(HX.getComponent2());
    
    ei.HY1_b1 = static_cast<Jet&>(HY1.getComponent1());
    ei.HY1_b2 = static_cast<Jet&>(HY1.getComponent2());
    
    ei.HY2_b1 = static_cast<Jet&>(HY2.getComponent1());
    ei.HY2_b2 = static_cast<Jet&>(HY2.getComponent2());

}

std::tuple<CompositeCandidate, CompositeCandidate, CompositeCandidate> SixB_functions::pair_passthrough (std::vector<Jet> jets)
{
    if (jets.size() != 6)
        throw std::runtime_error("The jet pairing -passthrough- function requires 6 jets");

    CompositeCandidate HX  (jets.at(0), jets.at(1));
    CompositeCandidate HY1 (jets.at(2), jets.at(3));
    CompositeCandidate HY2 (jets.at(4), jets.at(5));

    return std::make_tuple(HX, HY1, HY2);
}

std::tuple<CompositeCandidate, CompositeCandidate, CompositeCandidate> SixB_functions::pair_min_diag_distance (std::vector<Jet> jets)
{
    if (jets.size() != 6)
        throw std::runtime_error("The jet pairing -min_diag_distance- function requires 6 jets");

    const bool use_pt_regressed = true;

    // 6 jets -> 15 possible pairings given by:
    // (0, 1), (2, 3), (4, 5)
    // (0, 1), (2, 4), (3, 5)
    // (0, 1), (2, 5), (3, 4)
    // (0, 2), (1, 3), (4, 5)
    // (0, 2), (1, 4), (3, 5)
    // (0, 2), (1, 5), (3, 4)
    // (0, 3), (1, 2), (4, 5)
    // (0, 3), (1, 4), (2, 5)
    // (0, 3), (1, 5), (2, 4)
    // (0, 4), (1, 2), (3, 5)
    // (0, 4), (1, 3), (2, 5)
    // (0, 4), (1, 5), (2, 3)
    // (0, 5), (1, 2), (3, 4)
    // (0, 5), (1, 3), (2, 4)
    // (0, 5), (1, 4), (2, 3)

    typedef std::array<unsigned int, 6> idx_t; // {p0.0, p0.1, p1.0, p1.1, p2.0, p2.1}
    typedef std::array<idx_t, 15> idx_list_t; // idx_t x 15
    typedef std::array<CompositeCandidate, 3> pair_triplet_t;
    // not super elegant, but the list of all possible 15 pairs is the one below
    const idx_list_t idxs = {{
        {0, 1,    2, 3,    4, 5},
        {0, 1,    2, 4,    3, 5},
        {0, 1,    2, 5,    3, 4},
        {0, 2,    1, 3,    4, 5},
        {0, 2,    1, 4,    3, 5},
        {0, 2,    1, 5,    3, 4},
        {0, 3,    1, 2,    4, 5},
        {0, 3,    1, 4,    2, 5},
        {0, 3,    1, 5,    2, 4},
        {0, 4,    1, 2,    3, 5},
        {0, 4,    1, 3,    2, 5},
        {0, 4,    1, 5,    2, 3},
        {0, 5,    1, 2,    3, 4},
        {0, 5,    1, 3,    2, 4},
        {0, 5,    1, 4,    2, 3}
    }};

    // cout << "--- debug idx to build" << endl;
    // for (unsigned int i = 0; i < 15; ++i){
    //     for (unsigned int j = 0; j < 6; ++j){
    //         cout << idxs[i][j] << " ";
    //     }
    //     cout << endl;
    // }

    std::array<pair_triplet_t, 15> pairs;
    for (unsigned int ip = 0; ip < 15; ++ip){

        const idx_t& tidx = idxs.at(ip);
        CompositeCandidate hA (jets.at(tidx.at(0)), jets.at(tidx.at(1)) );
        CompositeCandidate hB (jets.at(tidx.at(2)), jets.at(tidx.at(3)) );
        CompositeCandidate hC (jets.at(tidx.at(4)), jets.at(tidx.at(5)) );

        if (use_pt_regressed){
            hA.rebuildP4UsingRegressedPt(true, true);
            hB.rebuildP4UsingRegressedPt(true, true);
            hC.rebuildP4UsingRegressedPt(true, true);
        }

        pairs.at(ip) = {hA, hB, hC};
    }

    struct vec3d {
        double x;
        double y;
        double z;
    };

    // compute the distance from the 3D "diagonal"
    // FIXME: can order pairs by H pT and define a diagonal that is not passing at 125/125/125 (take into account responses a la)
    const vec3d diag = {1./sqrt(3), 1./sqrt(3), 1./sqrt(3)};

    std::vector<std::pair<double, int>> mdiff_idx;
    for (unsigned int ip = 0; ip < 15; ++ip){

        // vector from origin (0,0,0) to this 3d mass point
        // FIXME: check if this uses standard p4 or regressed p4
        vec3d masspoint = {pairs.at(ip).at(0).P4().M(), pairs.at(ip).at(1).P4().M(), pairs.at(ip).at(2).P4().M()};
        
        // compute projection on diagonal - note: diagonal has a norm of 1 already
        double dotprod = masspoint.x*diag.x + masspoint.y*diag.y + masspoint.z*diag.z;

        // get the projected point
        vec3d proj {dotprod*diag.x, dotprod*diag.y, dotprod*diag.z};

        // distance of projection from masspoint
        double dx = proj.x - masspoint.x;
        double dy = proj.y - masspoint.y;
        double dz = proj.z - masspoint.z;
        double d = sqrt(dx*dx + dy*dy + dz*dz);
        mdiff_idx.push_back (make_pair(d, ip));   
    }

    // -------------------------------------------------------------

    // // sort to take the closest pair and return it
    // std::sort(mdiff_idx.begin(), mdiff_idx.end());
    // int best_idx = mdiff_idx.at(0).second;

    // -------------------------------------------------------------

    // take all pairs with a distance from the first value within the resolution 30 GeV - FIXME: tune value
    // then boost to the 6 jet ref frame and get the pair giving the largest sum(ptH)
    const double thresh_mdiff = 30.;
    std::sort(mdiff_idx.begin(), mdiff_idx.end());
    std::vector<std::pair<double, int>> mdiff_idx_afterthresh;
    for (unsigned int ip = 0; ip < 15; ++ip){
        double mdiff = mdiff_idx.at(ip).first - mdiff_idx.at(0).first;
        if (mdiff < thresh_mdiff){
            mdiff_idx_afterthresh.push_back(mdiff_idx.at(ip));
        }
    }

    int best_idx = -1;
    
    if (mdiff_idx_afterthresh.size() == 1){ // by construction size is >= 1 always since 1st pair is compared with itself
        best_idx = mdiff_idx_afterthresh.at(0).second;
    }
    
    else { // only for pairs thus selected, pick up the one with the highest sum(p H)
        std::vector<std::pair<double, int>> psum_idx_afterthresh;
        for (unsigned int ip = 0; ip < mdiff_idx_afterthresh.size(); ++ip){
            
            int ipair = mdiff_idx_afterthresh.at(ip).second;
            pair_triplet_t tr = pairs.at(ipair); // retrieve this triplet
            CompositeCandidate hA = tr.at(0);
            CompositeCandidate hB = tr.at(1);
            CompositeCandidate hC = tr.at(2);

            p4_t vsum (0,0,0,0);
            vsum += hA.P4();
            vsum += hB.P4();
            vsum += hC.P4();
            auto boost_vctr = vsum.BoostToCM();
            ROOT::Math::Boost boost(boost_vctr);

            // p4_t vsum_cm  = boost(vsum);
            p4_t hA_p4_cm = boost(hA.P4());
            p4_t hB_p4_cm = boost(hB.P4());
            p4_t hC_p4_cm = boost(hC.P4());
            // cout << " XCHECK: " << vsum_cm.Pt() << "  x/y/z" << vsum_cm.Px() << " " << vsum_cm.Py() << " " << vsum_cm.Pz() << " || " << vsum_cm.P() << "  " << hA.P4().Pt() << " --> " << hA_p4_cm.Pt() << endl;
            double psum = hA_p4_cm.P() + hB_p4_cm.P() + hC_p4_cm.P();
            psum_idx_afterthresh.push_back(make_pair(psum, ipair));
        }
        std::sort(psum_idx_afterthresh.begin(), psum_idx_afterthresh.end());
        best_idx = psum_idx_afterthresh.back().second; // take the one with the highest pT sum
    }
    
    // -------------------------------------------------------------

    std::tuple<CompositeCandidate, CompositeCandidate, CompositeCandidate> result = make_tuple(pairs.at(best_idx).at(0), pairs.at(best_idx).at(1), pairs.at(best_idx).at(2));

    // FIXME: need to attribute correctly who is HX, H1, H2

    return result;
}



int SixB_functions::n_gjmatched_in_jetcoll(NanoAODTree& nat, EventInfo& ei, const std::vector<Jet>& in_jets)
{
    std::vector<int> matched_jets;
    if (ei.gen_HX_b1_recojet)  matched_jets.push_back(ei.gen_HX_b1_recojet->getIdx());
    if (ei.gen_HX_b2_recojet)  matched_jets.push_back(ei.gen_HX_b2_recojet->getIdx());
    if (ei.gen_HY1_b1_recojet) matched_jets.push_back(ei.gen_HY1_b1_recojet->getIdx());
    if (ei.gen_HY1_b2_recojet) matched_jets.push_back(ei.gen_HY1_b2_recojet->getIdx());
    if (ei.gen_HY2_b1_recojet) matched_jets.push_back(ei.gen_HY2_b1_recojet->getIdx());
    if (ei.gen_HY2_b2_recojet) matched_jets.push_back(ei.gen_HY2_b2_recojet->getIdx());

    std::vector<int> reco_js (in_jets.size());
    for (unsigned int ij = 0; ij < in_jets.size(); ++ij)
        reco_js.at(ij) = in_jets.at(ij).getIdx();

    int nfound = 0;
    for (int imj : matched_jets){
        if (std::find(reco_js.begin(), reco_js.end(), imj) != reco_js.end())
            nfound += 1;
    }

    return nfound;
}

void SixB_functions::select_leptons(NanoAODTree &nat, EventInfo &ei)
{
    std::vector<Electron> electrons;
    std::vector<Muon> muons;

    for (unsigned int ie = 0; ie < *(nat.nElectron); ++ie){
        Electron ele (ie, &nat);
        electrons.emplace_back(ele);
    }

    for (unsigned int imu = 0; imu < *(nat.nMuon); ++imu){
        Muon mu(imu, &nat);
        muons.emplace_back(mu);
    }

    // apply preselections
    std::vector<Electron> loose_electrons;
    std::vector<Muon> loose_muons;

    // std::vector<Electron> tight_electrons;
    // std::vector<Muon> tight_muons;

    for (auto& el : electrons){

        float dxy    = get_property(el, Electron_dxy);
        float dz     = get_property(el, Electron_dz);
        float eta    = get_property(el, Electron_eta);
        float pt     = get_property(el, Electron_pt);
        bool ID_WPL  = get_property(el, Electron_mvaFall17V2Iso_WPL); 
        // bool ID_WP90 = get_property(el, Electron_mvaFall17V2Iso_WP90);
        // bool ID_WP80 = get_property(el, Electron_mvaFall17V2Iso_WP80);
        float iso    = get_property(el, Electron_pfRelIso03_all);

        // note: hardcoded selections can be made configurable from cfg if needed
        const float e_pt_min  = 15;
        const float e_eta_max = 2.5;
        const float e_iso_max = 0.15;
        
        const float e_dxy_max_barr = 0.05;
        const float e_dxy_max_endc = 0.10;
        const float e_dz_max_barr  = 0.10;
        const float e_dz_max_endc  = 0.20;

        bool is_barrel = abs(eta) < 1.479;
        bool pass_dxy  = (is_barrel ? dxy < e_dxy_max_barr : dxy < e_dxy_max_endc);
        bool pass_dz   = (is_barrel ? dz  < e_dz_max_barr  : dz  < e_dz_max_endc);

        // loose electrons for veto
        if (pt > e_pt_min        &&
            abs(eta) < e_eta_max &&
            iso < e_iso_max      &&
            pass_dxy             &&
            pass_dz              &&
            ID_WPL)
            loose_electrons.emplace_back(el);
    }

    for (auto& mu : muons){

        float dxy    = get_property(mu, Muon_dxy);
        float dz     = get_property(mu, Muon_dz);
        float eta    = get_property(mu, Muon_eta);
        float pt     = get_property(mu, Muon_pt);
        bool ID_WPL  = get_property(mu, Muon_looseId);
        // bool ID_WPM = get_property(mu, Muon_mediumId);
        // bool ID_WPT = get_property(mu, Muon_tightId);
        float iso    = get_property(mu, Muon_pfRelIso04_all);

        // note: hardcoded selections can be made configurable from cfg if needed
        const float mu_pt_min  = 10;
        const float mu_eta_max = 2.4;
        const float mu_iso_max = 0.15;
        
        const float mu_dxy_max_barr = 0.05;
        const float mu_dxy_max_endc = 0.10;
        const float mu_dz_max_barr  = 0.10;
        const float mu_dz_max_endc  = 0.20;

        bool is_barrel = abs(eta) < 1.2;
        bool pass_dxy  = (is_barrel ? dxy < mu_dxy_max_barr : dxy < mu_dxy_max_endc);
        bool pass_dz   = (is_barrel ? dz  < mu_dz_max_barr  : dz  < mu_dz_max_endc);

        // loose muons for veto
        if (pt > mu_pt_min        &&
            abs(eta) < mu_eta_max &&
            iso < mu_iso_max      &&
            pass_dxy              &&
            pass_dz               &&
            ID_WPL)
            loose_muons.emplace_back(mu);
    }

    // copy needed info to the EventInfo
    if (loose_muons.size() > 0) ei.mu_1 = loose_muons.at(0);
    if (loose_muons.size() > 1) ei.mu_2 = loose_muons.at(1);
    if (loose_electrons.size() > 0) ei.ele_1 = loose_electrons.at(0);
    if (loose_electrons.size() > 1) ei.ele_2 = loose_electrons.at(1);

    ei.n_mu_loose  = loose_muons.size();
    ei.n_ele_loose = loose_electrons.size();
    // ei.n_mu_tight  = tight_muons.size();
    // ei.n_ele_tight = tight_electrons.size();
}
#include "SixB_functions.h"
#include "Math/VectorUtil.h"

#include <iostream>
#include <tuple>

void SixB_functions::copy_event_info(NanoAODTree& nat, EventInfo& ei)
{
    ei.Run     = *(nat.run);
    ei.LumiSec = *(nat.luminosityBlock);
    ei.Event   = *(nat.event);
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

void SixB_functions::pair_jets(NanoAODTree& nat, EventInfo& ei, const std::vector<Jet>& in_jets)
{
    // FIXME: here a switch for the pairing algo
    const std::string pairAlgo = "passthrough";

    // call the desired algo - expected interface is input jets -> output 3 composite candidate HX, HY1. HY2
    // the order of HY1, HY2 and of the jets does not matter - they will be reordered after

    std::tuple<CompositeCandidate, CompositeCandidate, CompositeCandidate> reco_Hs;
    if (pairAlgo == "passthrough")
        reco_Hs = pair_passthrough(in_jets);

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

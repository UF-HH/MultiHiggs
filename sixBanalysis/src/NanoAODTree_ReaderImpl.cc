#include "NanoAODTree_ReaderImpl.h"

bool NanoAODTree_ReaderImpl::Next()
{
    bool next = fReader.Next();
    if (!next) return next; // it's the end
    
    int t_tmp = fReader.GetTree()->GetTreeNumber();

    if (t_tmp != old_tree_nr_) // marks a chain transition
    {
        Long64_t entry = fReader.GetCurrentEntry();
        fReader.Restart();
        for (auto& rd : trg_reader_.getRefToReadersPtrVector())
            rd->Verify(fReader.GetTree());
        //Stuff for XYH  
        for (auto& customBranch : fCustomBranchMap)
            customBranch.second->Verify(fReader.GetTree());
        //Stuff for XYH
        fReader.SetEntry(entry);
        old_tree_nr_ = t_tmp;
    }

    /*
    // do the initialization of the branches that can differ between different samples, e.g. data vs MC
    // (no gen info in the former)
    // no need to check at any tree transition but only at the first event readout
    if (!proc_first_ev_) // this is the start of the tree
    {
        proc_first_ev_ = true;
        // if (!is_data_) // enable the MC branches
        // {
        Electron_genPartIdx         .Verify(fReader.GetTree());
        Electron_genPartFlav        .Verify(fReader.GetTree());
        nGenJetAK8                  .Verify(fReader.GetTree());
        GenJetAK8_eta               .Verify(fReader.GetTree());
        GenJetAK8_mass              .Verify(fReader.GetTree());
        GenJetAK8_phi               .Verify(fReader.GetTree());
        GenJetAK8_pt                .Verify(fReader.GetTree());
        nGenJet                     .Verify(fReader.GetTree());
        GenJet_eta                  .Verify(fReader.GetTree());
        GenJet_mass                 .Verify(fReader.GetTree());
        GenJet_phi                  .Verify(fReader.GetTree());
        GenJet_pt                   .Verify(fReader.GetTree());
        nGenPart                    .Verify(fReader.GetTree());
        GenPart_eta                 .Verify(fReader.GetTree());
        GenPart_mass                .Verify(fReader.GetTree());
        GenPart_phi                 .Verify(fReader.GetTree());
        GenPart_pt                  .Verify(fReader.GetTree());
        GenPart_genPartIdxMother    .Verify(fReader.GetTree());
        GenPart_pdgId               .Verify(fReader.GetTree());
        GenPart_status              .Verify(fReader.GetTree());
        GenPart_statusFlags         .Verify(fReader.GetTree());
        Generator_x1                .Verify(fReader.GetTree());
        Generator_x2                .Verify(fReader.GetTree());
        nGenVisTau                  .Verify(fReader.GetTree());
        GenVisTau_eta               .Verify(fReader.GetTree());
        GenVisTau_mass              .Verify(fReader.GetTree());
        GenVisTau_phi               .Verify(fReader.GetTree());
        GenVisTau_pt                .Verify(fReader.GetTree());
        GenVisTau_charge            .Verify(fReader.GetTree());
        GenVisTau_genPartIdxMother  .Verify(fReader.GetTree());
        GenVisTau_status            .Verify(fReader.GetTree());
        genWeight                   .Verify(fReader.GetTree());
        LHEWeight_originalXWGTUP    .Verify(fReader.GetTree());
        nLHEPdfWeight               .Verify(fReader.GetTree());
        LHEPdfWeight                .Verify(fReader.GetTree());
        nLHEScaleWeight             .Verify(fReader.GetTree());
        LHEScaleWeight              .Verify(fReader.GetTree());
        Jet_genJetIdx               .Verify(fReader.GetTree());
        Jet_hadronFlavour           .Verify(fReader.GetTree());
        Jet_partonFlavour           .Verify(fReader.GetTree());
        GenMET_phi                  .Verify(fReader.GetTree());
        GenMET_pt                   .Verify(fReader.GetTree());
        Pileup_nPU                  .Verify(fReader.GetTree());
        Pileup_nTrueInt             .Verify(fReader.GetTree());
        nGenDressedLepton           .Verify(fReader.GetTree());
        GenDressedLepton_eta        .Verify(fReader.GetTree());
        GenDressedLepton_mass       .Verify(fReader.GetTree());
        GenDressedLepton_phi        .Verify(fReader.GetTree());
        GenDressedLepton_pt         .Verify(fReader.GetTree());
        GenDressedLepton_pdgId      .Verify(fReader.GetTree());
        genTtbarId                  .Verify(fReader.GetTree());
        GenJetAK8_partonFlavour     .Verify(fReader.GetTree());
        GenJetAK8_hadronFlavour     .Verify(fReader.GetTree());
        GenJet_partonFlavour        .Verify(fReader.GetTree());
        GenJet_hadronFlavour        .Verify(fReader.GetTree());
        Muon_genPartIdx             .Verify(fReader.GetTree());
        Muon_genPartFlav            .Verify(fReader.GetTree());
        Photon_genPartIdx           .Verify(fReader.GetTree());
        Photon_genPartFlav          .Verify(fReader.GetTree());
        Tau_genPartIdx              .Verify(fReader.GetTree());
        Tau_genPartFlav             .Verify(fReader.GetTree());
        MET_fiducialGenPhi          .Verify(fReader.GetTree());
        MET_fiducialGenPt           .Verify(fReader.GetTree());
        // }
    }
    */

    return next;
}
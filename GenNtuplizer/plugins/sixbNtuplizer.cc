#ifndef SIXBNTUPLIZER_H
#define SIXBNTUPLIZER_H

// -*- C++ -*-
//
// Package:    sixB/GenNtuplizer
// Class:      sixbNtuplizer
//
/**\class sixbNtuplizer sixbNtuplizer.cc sixB/GenNtuplizer/plugins/sixbNtuplizer.cc

 Description: ntuplizer for the six b gen studies

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Luca Cadamuro
//         Created:  Fri, 18 Sep 2020 15:45:38 GMT
//
//


// system include files
#include <memory>
#include <utility>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/HepMCCandidate/interface/GenStatusFlags.h"
#include "DataFormats/JetReco/interface/GenJet.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/Math/interface/deltaR.h"

#include "TTree.h"

using namespace reco;

//
// class declaration
//

// If the analyzer does not use TFileService, please remove
// the template argument to the base class so the class inherits
// from  edm::one::EDAnalyzer<>
// This will improve performance in multithreaded jobs.


class sixbNtuplizer : public edm::one::EDAnalyzer<edm::one::SharedResources>  {
   public:
      explicit sixbNtuplizer(const edm::ParameterSet&);
      ~sixbNtuplizer();

      // static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);
      typedef std::vector< GenParticle >  GenParticleCollection;
      typedef std::vector< GenJet >       GenJetCollection;

   private:
      virtual void beginJob() override;
      virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;

      void reset();

      // these functions set the variables for H1, H2, H2, X, Y, with the associated b decays
      void save_X_vars(const GenParticle* cand);
      void save_Y_vars(const GenParticle* cand);
      void save_HX_vars(const GenParticle* cand, std::vector<const GenJet*> genjets);
      void save_HY_vars(const GenParticle* cand1, const GenParticle* cand2, std::vector<const GenJet*> genjets);

      int find_genjet_idx(const Candidate* gp, std::vector<const GenJet*>& genjets);

      // std::pair<GenParticle*, GenParticle*> find_first_last (const GenParticle& gp);
      const Candidate* find_last (const GenParticle& gp);

      // ----------member data ---------------------------
      edm::EDGetTokenT<GenParticleCollection> genPartToken_;
      edm::EDGetTokenT<GenJetCollection>      genJetToken_;
      edm::EDGetTokenT<GenJetCollection>      genJetWithNuToken_;
      
      //
      // static data member definitions
      //
      TTree *tree_;

      std::vector<float> gen_jet_pt_;
      std::vector<float> gen_jet_eta_;
      std::vector<float> gen_jet_phi_;
      std::vector<float> gen_jet_m_;
      // std::vector<int>   gen_jet_charge_;

      std::vector<float> gen_jet_wnu_pt_;
      std::vector<float> gen_jet_wnu_eta_;
      std::vector<float> gen_jet_wnu_phi_;
      std::vector<float> gen_jet_wnu_m_;
      std::vector<int>   gen_jet_wnu_charge_;

      // first copies
      float gen_fc_X_pt_;
      float gen_fc_X_eta_;
      float gen_fc_X_phi_;
      float gen_fc_X_m_;

      float gen_fc_Y_pt_;
      float gen_fc_Y_eta_;
      float gen_fc_Y_phi_;
      float gen_fc_Y_m_;

      float gen_fc_HX_pt_;
      float gen_fc_HX_eta_;
      float gen_fc_HX_phi_;
      float gen_fc_HX_m_;

      float gen_fc_HY1_pt_;
      float gen_fc_HY1_eta_;
      float gen_fc_HY1_phi_;
      float gen_fc_HY1_m_;

      float gen_fc_HY2_pt_;
      float gen_fc_HY2_eta_;
      float gen_fc_HY2_phi_;
      float gen_fc_HY2_m_;


      // last copies
      float gen_lc_X_pt_;
      float gen_lc_X_eta_;
      float gen_lc_X_phi_;
      float gen_lc_X_m_;

      float gen_lc_Y_pt_;
      float gen_lc_Y_eta_;
      float gen_lc_Y_phi_;
      float gen_lc_Y_m_;

      float gen_lc_HX_pt_;
      float gen_lc_HX_eta_;
      float gen_lc_HX_phi_;
      float gen_lc_HX_m_;

      float gen_lc_HY1_pt_;
      float gen_lc_HY1_eta_;
      float gen_lc_HY1_phi_;
      float gen_lc_HY1_m_;

      float gen_lc_HY2_pt_;
      float gen_lc_HY2_eta_;
      float gen_lc_HY2_phi_;
      float gen_lc_HY2_m_;

      // b quarks from Higgs decays
      float gen_HX_b1_pt_;
      float gen_HX_b1_eta_;
      float gen_HX_b1_phi_;
      float gen_HX_b1_m_;
      int   gen_HX_b1_genjetIdx_;

      float gen_HX_b2_pt_;
      float gen_HX_b2_eta_;
      float gen_HX_b2_phi_;
      float gen_HX_b2_m_;
      int   gen_HX_b2_genjetIdx_;

      float gen_HY1_b1_pt_;
      float gen_HY1_b1_eta_;
      float gen_HY1_b1_phi_;
      float gen_HY1_b1_m_;
      int   gen_HY1_b1_genjetIdx_;

      float gen_HY1_b2_pt_;
      float gen_HY1_b2_eta_;
      float gen_HY1_b2_phi_;
      float gen_HY1_b2_m_;
      int   gen_HY1_b2_genjetIdx_;

      float gen_HY2_b1_pt_;
      float gen_HY2_b1_eta_;
      float gen_HY2_b1_phi_;
      float gen_HY2_b1_m_;
      int   gen_HY2_b1_genjetIdx_;

      float gen_HY2_b2_pt_;
      float gen_HY2_b2_eta_;
      float gen_HY2_b2_phi_;
      float gen_HY2_b2_m_;
      int   gen_HY2_b2_genjetIdx_;
};

//
// constructors and destructor
//
sixbNtuplizer::sixbNtuplizer(const edm::ParameterSet& iConfig)
 :
  genPartToken_       (consumes<GenParticleCollection> (iConfig.getParameter<edm::InputTag>("GenParticles"))),
  genJetToken_        (consumes<GenJetCollection>      (iConfig.getParameter<edm::InputTag>("GenJets"))),
  genJetWithNuToken_  (consumes<GenJetCollection>      (iConfig.getParameter<edm::InputTag>("GenJetsWithNu")))

{
}

int sixbNtuplizer::find_genjet_idx(const Candidate* gp, std::vector<const GenJet*>& genjets)
{
  int idx = -1;
  std::vector<std::pair<float,int>> dr_imatched;
  for (uint igj = 0; igj < genjets.size(); ++igj)
  {
    const GenJet* gj = genjets.at(igj);
    float dr = deltaR(*gj, *gp);
    if (dr < 0.4) {
      dr_imatched.push_back(std::make_pair(dr, igj));
    }
  }

  if (dr_imatched.size() > 0) {
    sort(dr_imatched.begin(), dr_imatched.end());
    idx = dr_imatched.at(0).second;
  }

  return idx;
}

void sixbNtuplizer::save_X_vars(const GenParticle* cand)
{
  const Candidate* last = find_last(*cand);
  
  gen_fc_X_pt_  = cand->pt();
  gen_fc_X_eta_ = cand->eta();
  gen_fc_X_phi_ = cand->phi();
  gen_fc_X_m_   = cand->mass();

  gen_lc_X_pt_  = last->pt();
  gen_lc_X_eta_ = last->eta();
  gen_lc_X_phi_ = last->phi();
  gen_lc_X_m_   = last->mass();
}

void sixbNtuplizer::save_Y_vars(const GenParticle* cand)
{
  const Candidate* last = find_last(*cand);
  
  gen_fc_Y_pt_  = cand->pt();
  gen_fc_Y_eta_ = cand->eta();
  gen_fc_Y_phi_ = cand->phi();
  gen_fc_Y_m_   = cand->mass();

  gen_lc_Y_pt_  = last->pt();
  gen_lc_Y_eta_ = last->eta();
  gen_lc_Y_phi_ = last->phi();
  gen_lc_Y_m_   = last->mass();
}

void sixbNtuplizer::save_HX_vars(const GenParticle* cand, std::vector<const GenJet*> genjets)
{
  const Candidate* last = find_last(*cand);

  gen_fc_HX_pt_  = cand->pt();
  gen_fc_HX_eta_ = cand->eta();
  gen_fc_HX_phi_ = cand->phi();
  gen_fc_HX_m_   = cand->mass();

  gen_lc_HX_pt_  = last->pt();
  gen_lc_HX_eta_ = last->eta();
  gen_lc_HX_phi_ = last->phi();
  gen_lc_HX_m_   = last->mass();

  // now b quarks
  int ndau = last->numberOfDaughters();
  if (ndau != 2)
    throw cms::Exception("sixBgenContent") << "HX last cand has not 2 daughters but " << ndau << "\n";

  const Candidate* b1 = last->daughter(0);
  const Candidate* b2 = last->daughter(1);

  // sort by pt
  if (b2->pt() > b1->pt())
    std::swap(b1, b2);

  gen_HX_b1_pt_        = b1->pt();
  gen_HX_b1_eta_       = b1->eta();
  gen_HX_b1_phi_       = b1->phi();
  gen_HX_b1_m_         = b1->mass();
  gen_HX_b1_genjetIdx_ = find_genjet_idx(b1, genjets);

  gen_HX_b2_pt_        = b2->pt();
  gen_HX_b2_eta_       = b2->eta();
  gen_HX_b2_phi_       = b2->phi();
  gen_HX_b2_m_         = b2->mass();
  gen_HX_b2_genjetIdx_ = find_genjet_idx(b2, genjets);
}


void sixbNtuplizer::save_HY_vars(const GenParticle* cand1, const GenParticle* cand2, std::vector<const GenJet*> genjets)
{
  if (cand2->pt() > cand1->pt())
    std::swap(cand1, cand2);

  const Candidate* last1 = find_last(*cand1);
  const Candidate* last2 = find_last(*cand2);

  gen_fc_HY1_pt_  = cand1->pt();
  gen_fc_HY1_eta_ = cand1->eta();
  gen_fc_HY1_phi_ = cand1->phi();
  gen_fc_HY1_m_   = cand1->mass();

  gen_lc_HY1_pt_  = last1->pt();
  gen_lc_HY1_eta_ = last1->eta();
  gen_lc_HY1_phi_ = last1->phi();
  gen_lc_HY1_m_   = last1->mass();

  gen_fc_HY2_pt_  = cand2->pt();
  gen_fc_HY2_eta_ = cand2->eta();
  gen_fc_HY2_phi_ = cand2->phi();
  gen_fc_HY2_m_   = cand2->mass();

  gen_lc_HY2_pt_  = last2->pt();
  gen_lc_HY2_eta_ = last2->eta();
  gen_lc_HY2_phi_ = last2->phi();
  gen_lc_HY2_m_   = last2->mass();


  // now b quarks
  int ndau1 = last1->numberOfDaughters();
  if (ndau1 != 2)
    throw cms::Exception("sixBgenContent") << "HY1 last cand has not 2 daughters but " << ndau1 << "\n";

  int ndau2 = last1->numberOfDaughters();
  if (ndau2 != 2)
    throw cms::Exception("sixBgenContent") << "HY1 last cand has not 2 daughters but " << ndau2 << "\n";

  const Candidate* H1_b1 = last1->daughter(0);
  const Candidate* H1_b2 = last1->daughter(1);

  const Candidate* H2_b1 = last2->daughter(0);
  const Candidate* H2_b2 = last2->daughter(1);

  // sort by pt
  if (H1_b2->pt() > H1_b1->pt())
    std::swap(H1_b1, H1_b2);

  // sort by pt
  if (H2_b2->pt() > H2_b1->pt())
    std::swap(H2_b1, H2_b2);

  // leading H from Y
  gen_HY1_b1_pt_          = H1_b1->pt();
  gen_HY1_b1_eta_         = H1_b1->eta();
  gen_HY1_b1_phi_         = H1_b1->phi();
  gen_HY1_b1_m_           = H1_b1->mass();
  gen_HY1_b1_genjetIdx_   = find_genjet_idx(H1_b1, genjets);

  gen_HY1_b2_pt_          = H1_b2->pt();
  gen_HY1_b2_eta_         = H1_b2->eta();
  gen_HY1_b2_phi_         = H1_b2->phi();
  gen_HY1_b2_m_           = H1_b2->mass();
  gen_HY1_b2_genjetIdx_   = find_genjet_idx(H1_b2, genjets);

  // subleading H from Y
  gen_HY2_b1_pt_          = H2_b1->pt();
  gen_HY2_b1_eta_         = H2_b1->eta();
  gen_HY2_b1_phi_         = H2_b1->phi();
  gen_HY2_b1_m_           = H2_b1->mass();
  gen_HY2_b1_genjetIdx_   = find_genjet_idx(H2_b1, genjets);

  gen_HY2_b2_pt_          = H2_b2->pt();
  gen_HY2_b2_eta_         = H2_b2->eta();
  gen_HY2_b2_phi_         = H2_b2->phi();
  gen_HY2_b2_m_           = H2_b2->mass();
  gen_HY2_b2_genjetIdx_   = find_genjet_idx(H2_b2, genjets);
}


// std::pair<GenParticle*, GenParticle*> find_first_last (const GenParticle& gp)
// {
//   int pdgId = gp.pdgId();

//   // find mother - up to the chain until moth idx is != from this one
//   GenParticle* first = &gp;
//   while (true)
//   {
//     if (first->mother(0)->pdgId() != pdgId)
//       break; // this is the last particle
//     else
//       first = first->mother(0);
//   }

//   GenParticle* last = &gp;
//   while (true)
//   {
//     if (last->daughter(0)->pdgId() != pdgId)
//       break; // this is the last particle
//     else
//       last = last->daughter(0);
//   }

//   return std::make_pair(first, last);
// }

const Candidate* sixbNtuplizer::find_last (const GenParticle& gp)
{
  int pdgId = gp.pdgId();

  const Candidate* last = &gp;
  while (true)
  {
    if (last->daughter(0)->pdgId() != pdgId)
      break; // this is the last particle
    else
      last = last->daughter(0);
  }

  return last;
}

void sixbNtuplizer::reset()
{
  gen_jet_pt_.clear();
  gen_jet_eta_.clear();
  gen_jet_phi_.clear();
  gen_jet_m_.clear();
  // gen_jet_charge_.clear();

  gen_jet_wnu_pt_.clear();
  gen_jet_wnu_eta_.clear();
  gen_jet_wnu_phi_.clear();
  gen_jet_wnu_m_.clear();
  gen_jet_wnu_charge_.clear();

  // first copies
  gen_fc_X_pt_    = -1;
  gen_fc_X_eta_   = -1;
  gen_fc_X_phi_   = -1;
  gen_fc_X_m_     = -1;

  gen_fc_Y_pt_    = -1;
  gen_fc_Y_eta_   = -1;
  gen_fc_Y_phi_   = -1;
  gen_fc_Y_m_     = -1;

  gen_fc_HX_pt_   = -1;
  gen_fc_HX_eta_  = -1;
  gen_fc_HX_phi_  = -1;
  gen_fc_HX_m_    = -1;

  gen_fc_HY1_pt_  = -1;
  gen_fc_HY1_eta_ = -1;
  gen_fc_HY1_phi_ = -1;
  gen_fc_HY1_m_   = -1;

  gen_fc_HY2_pt_  = -1;
  gen_fc_HY2_eta_ = -1;
  gen_fc_HY2_phi_ = -1;
  gen_fc_HY2_m_   = -1;


  // last copies
  gen_lc_X_pt_    = -1;
  gen_lc_X_eta_   = -1;
  gen_lc_X_phi_   = -1;
  gen_lc_X_m_     = -1;

  gen_lc_Y_pt_    = -1;
  gen_lc_Y_eta_   = -1;
  gen_lc_Y_phi_   = -1;
  gen_lc_Y_m_     = -1;

  gen_lc_HX_pt_   = -1;
  gen_lc_HX_eta_  = -1;
  gen_lc_HX_phi_  = -1;
  gen_lc_HX_m_    = -1;

  gen_lc_HY1_pt_  = -1;
  gen_lc_HY1_eta_ = -1;
  gen_lc_HY1_phi_ = -1;
  gen_lc_HY1_m_   = -1;

  gen_lc_HY2_pt_  = -1;
  gen_lc_HY2_eta_ = -1;
  gen_lc_HY2_phi_ = -1;
  gen_lc_HY2_m_   = -1;

  // b quarks from Higgs decays
  gen_HX_b1_pt_            = -1;
  gen_HX_b1_eta_           = -1;
  gen_HX_b1_phi_           = -1;
  gen_HX_b1_m_             = -1;
  gen_HX_b1_genjetIdx_     = -1;

  gen_HX_b2_pt_            = -1;
  gen_HX_b2_eta_           = -1;
  gen_HX_b2_phi_           = -1;
  gen_HX_b2_m_             = -1;
  gen_HX_b2_genjetIdx_     = -1;

  gen_HY1_b1_pt_           = -1;
  gen_HY1_b1_eta_          = -1;
  gen_HY1_b1_phi_          = -1;
  gen_HY1_b1_m_            = -1;
  gen_HY1_b1_genjetIdx_    = -1;

  gen_HY1_b2_pt_           = -1;
  gen_HY1_b2_eta_          = -1;
  gen_HY1_b2_phi_          = -1;
  gen_HY1_b2_m_            = -1;
  gen_HY1_b2_genjetIdx_    = -1;

  gen_HY2_b1_pt_           = -1;
  gen_HY2_b1_eta_          = -1;
  gen_HY2_b1_phi_          = -1;
  gen_HY2_b1_m_            = -1;
  gen_HY2_b1_genjetIdx_    = -1;

  gen_HY2_b2_pt_           = -1;
  gen_HY2_b2_eta_          = -1;
  gen_HY2_b2_phi_          = -1;
  gen_HY2_b2_m_            = -1;
  gen_HY2_b2_genjetIdx_    = -1;
}



sixbNtuplizer::~sixbNtuplizer()
{

   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void sixbNtuplizer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  using namespace edm;

  reset(); // clear vectors

  // gen jets -------------------------------------------------

  Handle<GenJetCollection> genjets;
  iEvent.getByToken(genJetToken_, genjets);
  std::vector<const GenJet*> sel_genjets;
  for(GenJetCollection::const_iterator gj = genjets->begin(); gj != genjets->end(); ++gj) {
    if (gj->pt() < 10)
      continue;
    sel_genjets.push_back(&(*gj));
  }

  for (auto* gj : sel_genjets)
  {
    gen_jet_pt_  .push_back(gj->pt());
    gen_jet_eta_ .push_back(gj->eta());
    gen_jet_phi_ .push_back(gj->phi());
    gen_jet_m_   .push_back(gj->mass());
  }

  // gen jets w/o neutrinos -------------------------------------------------

  Handle<GenJetCollection> genjetswithnu;
  iEvent.getByToken(genJetWithNuToken_, genjetswithnu);
  std::vector<const GenJet*> sel_genjetswithnu;
  for(GenJetCollection::const_iterator gjwn = genjetswithnu->begin(); gjwn != genjetswithnu->end(); ++gjwn) {
    if (gjwn->pt() < 10)
      continue;
    sel_genjetswithnu.push_back(&(*gjwn));
  }

  for (auto* gjwn : sel_genjetswithnu)
  {
    gen_jet_wnu_pt_  .push_back(gjwn->pt());
    gen_jet_wnu_eta_ .push_back(gjwn->eta());
    gen_jet_wnu_phi_ .push_back(gjwn->phi());
    gen_jet_wnu_m_   .push_back(gjwn->mass());
  }

  // gen level particles -------------------------------------------------

  Handle<GenParticleCollection> genparts;
  iEvent.getByToken(genPartToken_, genparts);

  std::vector<const GenParticle*> hs_bosons;
  for(GenParticleCollection::const_iterator gp = genparts->begin(); gp != genparts->end(); ++gp) {
    int apdgid = abs(gp->pdgId());
    if (apdgid != 25 && apdgid != 35 && apdgid != 45) // only keep and higgses
      continue;
    
    const reco::GenStatusFlags& fl = gp->statusFlags();
    if (!fl.isFirstCopy())
      continue;

    hs_bosons.push_back(&(*gp));
  }

  // there should be exactly 1 X, 1 Y, 3 H => tot 5
  if (hs_bosons.size() != 5) {
    std::cout << ".... dumping gen particles ID found" << std::endl;
    for (auto* gp : hs_bosons)
      std::cout << gp->pdgId() << std::endl;
    throw cms::Exception("sixBgenContent") << "I could not find 5 boson candidates but " << hs_bosons.size() << "\n";
  }

  const GenParticle* pX = nullptr;
  const GenParticle* pY = nullptr;
  const GenParticle* pHX = nullptr;
  const GenParticle* pHY1 = nullptr;
  const GenParticle* pHY2 = nullptr;

  for (auto* gp : hs_bosons)
  {
    int apdgid = abs(gp->pdgId());
    if (apdgid == 45)
      pX = gp;
    else if (apdgid == 35)
      pY = gp;
    else if (apdgid == 25){
      int mapdgid = abs(gp->mother(0)->pdgId());
      if (mapdgid == 45)
        pHX = gp;
      else if (mapdgid == 35)
        (!pHY1 ? pHY1 : pHY2) = gp;
      else
        throw cms::Exception("sixBgenContent") << "Looks like this Higgs boson has an unknown mother, id is " << mapdgid << "\n";    
    }
    else
      throw cms::Exception("sixBgenContent") << "Looks like this is not a boson, id is " << apdgid << "\n";

  }

  save_X_vars(pX);
  save_Y_vars(pY);
  save_HX_vars(pHX, sel_genjets);
  save_HY_vars(pHY1, pHY2, sel_genjets);

  tree_->Fill();

}


// ------------ method called once each job just before starting event loop  ------------
void
sixbNtuplizer::beginJob()
{
  edm::Service<TFileService> fs;
  tree_ = fs -> make<TTree>("sixBtree", "sixBtree");

  tree_->Branch("gen_jet_pt",     &gen_jet_pt_);
  tree_->Branch("gen_jet_eta",    &gen_jet_eta_);
  tree_->Branch("gen_jet_phi",    &gen_jet_phi_);
  tree_->Branch("gen_jet_m",      &gen_jet_m_);
  // tree_->Branch("gen_jet_charge", &gen_jet_charge_);

  tree_->Branch("gen_jet_wnu_pt",     &gen_jet_wnu_pt_);
  tree_->Branch("gen_jet_wnu_eta",    &gen_jet_wnu_eta_);
  tree_->Branch("gen_jet_wnu_phi",    &gen_jet_wnu_phi_);
  tree_->Branch("gen_jet_wnu_m",      &gen_jet_wnu_m_);
  // tree_->Branch("gen_jet_wnu_charge", &gen_jet_wnu_charge_);

  // first copies
  tree_->Branch("gen_fc_X_pt",    &gen_fc_X_pt_);
  tree_->Branch("gen_fc_X_eta",   &gen_fc_X_eta_);
  tree_->Branch("gen_fc_X_phi",   &gen_fc_X_phi_);
  tree_->Branch("gen_fc_X_m",     &gen_fc_X_m_);

  tree_->Branch("gen_fc_Y_pt",    &gen_fc_Y_pt_);
  tree_->Branch("gen_fc_Y_eta",   &gen_fc_Y_eta_);
  tree_->Branch("gen_fc_Y_phi",   &gen_fc_Y_phi_);
  tree_->Branch("gen_fc_Y_m",     &gen_fc_Y_m_);

  tree_->Branch("gen_fc_HX_pt",   &gen_fc_HX_pt_);
  tree_->Branch("gen_fc_HX_eta",  &gen_fc_HX_eta_);
  tree_->Branch("gen_fc_HX_phi",  &gen_fc_HX_phi_);
  tree_->Branch("gen_fc_HX_m",    &gen_fc_HX_m_);

  tree_->Branch("gen_fc_HY1_pt",  &gen_fc_HY1_pt_);
  tree_->Branch("gen_fc_HY1_eta", &gen_fc_HY1_eta_);
  tree_->Branch("gen_fc_HY1_phi", &gen_fc_HY1_phi_);
  tree_->Branch("gen_fc_HY1_m",   &gen_fc_HY1_m_);

  tree_->Branch("gen_fc_HY2_pt",  &gen_fc_HY2_pt_);
  tree_->Branch("gen_fc_HY2_eta", &gen_fc_HY2_eta_);
  tree_->Branch("gen_fc_HY2_phi", &gen_fc_HY2_phi_);
  tree_->Branch("gen_fc_HY2_m",   &gen_fc_HY2_m_);


  // last copies
  tree_->Branch("gen_lc_X_pt",    &gen_lc_X_pt_);
  tree_->Branch("gen_lc_X_eta",   &gen_lc_X_eta_);
  tree_->Branch("gen_lc_X_phi",   &gen_lc_X_phi_);
  tree_->Branch("gen_lc_X_m",     &gen_lc_X_m_);

  tree_->Branch("gen_lc_Y_pt",    &gen_lc_Y_pt_);
  tree_->Branch("gen_lc_Y_eta",   &gen_lc_Y_eta_);
  tree_->Branch("gen_lc_Y_phi",   &gen_lc_Y_phi_);
  tree_->Branch("gen_lc_Y_m",     &gen_lc_Y_m_);

  tree_->Branch("gen_lc_HX_pt",   &gen_lc_HX_pt_);
  tree_->Branch("gen_lc_HX_eta",  &gen_lc_HX_eta_);
  tree_->Branch("gen_lc_HX_phi",  &gen_lc_HX_phi_);
  tree_->Branch("gen_lc_HX_m",    &gen_lc_HX_m_);

  tree_->Branch("gen_lc_HY1_pt",  &gen_lc_HY1_pt_);
  tree_->Branch("gen_lc_HY1_eta", &gen_lc_HY1_eta_);
  tree_->Branch("gen_lc_HY1_phi", &gen_lc_HY1_phi_);
  tree_->Branch("gen_lc_HY1_m",   &gen_lc_HY1_m_);

  tree_->Branch("gen_lc_HY2_pt",  &gen_lc_HY2_pt_);
  tree_->Branch("gen_lc_HY2_eta", &gen_lc_HY2_eta_);
  tree_->Branch("gen_lc_HY2_phi", &gen_lc_HY2_phi_);
  tree_->Branch("gen_lc_HY2_m",   &gen_lc_HY2_m_);

  // b quarks from Higgs decays
  tree_->Branch("gen_HX_b1_pt",           &gen_HX_b1_pt_);
  tree_->Branch("gen_HX_b1_eta",          &gen_HX_b1_eta_);
  tree_->Branch("gen_HX_b1_phi",          &gen_HX_b1_phi_);
  tree_->Branch("gen_HX_b1_m",            &gen_HX_b1_m_);
  tree_->Branch("gen_HX_b1_genjetIdx",    &gen_HX_b1_genjetIdx_);

  tree_->Branch("gen_HX_b2_pt",           &gen_HX_b2_pt_);
  tree_->Branch("gen_HX_b2_eta",          &gen_HX_b2_eta_);
  tree_->Branch("gen_HX_b2_phi",          &gen_HX_b2_phi_);
  tree_->Branch("gen_HX_b2_m",            &gen_HX_b2_m_);
  tree_->Branch("gen_HX_b2_genjetIdx",    &gen_HX_b2_genjetIdx_);

  tree_->Branch("gen_HY1_b1_pt",          &gen_HY1_b1_pt_);
  tree_->Branch("gen_HY1_b1_eta",         &gen_HY1_b1_eta_);
  tree_->Branch("gen_HY1_b1_phi",         &gen_HY1_b1_phi_);
  tree_->Branch("gen_HY1_b1_m",           &gen_HY1_b1_m_);
  tree_->Branch("gen_HY1_b1_genjetIdx",   &gen_HY1_b1_genjetIdx_);

  tree_->Branch("gen_HY1_b2_pt",          &gen_HY1_b2_pt_);
  tree_->Branch("gen_HY1_b2_eta",         &gen_HY1_b2_eta_);
  tree_->Branch("gen_HY1_b2_phi",         &gen_HY1_b2_phi_);
  tree_->Branch("gen_HY1_b2_m",           &gen_HY1_b2_m_);
  tree_->Branch("gen_HY1_b2_genjetIdx",   &gen_HY1_b2_genjetIdx_);

  tree_->Branch("gen_HY2_b1_pt",          &gen_HY2_b1_pt_);
  tree_->Branch("gen_HY2_b1_eta",         &gen_HY2_b1_eta_);
  tree_->Branch("gen_HY2_b1_phi",         &gen_HY2_b1_phi_);
  tree_->Branch("gen_HY2_b1_m",           &gen_HY2_b1_m_);
  tree_->Branch("gen_HY2_b1_genjetIdx",   &gen_HY2_b1_genjetIdx_);

  tree_->Branch("gen_HY2_b2_pt",          &gen_HY2_b2_pt_);
  tree_->Branch("gen_HY2_b2_eta",         &gen_HY2_b2_eta_);
  tree_->Branch("gen_HY2_b2_phi",         &gen_HY2_b2_phi_);
  tree_->Branch("gen_HY2_b2_m",           &gen_HY2_b2_m_);
  tree_->Branch("gen_HY2_b2_genjetIdx",   &gen_HY2_b2_genjetIdx_);
}

// ------------ method called once each job just after ending the event loop  ------------
void
sixbNtuplizer::endJob()
{
}

// // ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
// void
// sixbNtuplizer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
//   //The following says we do not know what parameters are allowed so do no validation
//   // Please change this to state exactly what you do use, even if it is no parameters
//   edm::ParameterSetDescription desc;
//   desc.setUnknown();
//   descriptions.addDefault(desc);

//   //Specify that only 'tracks' is allowed
//   //To use, remove the default given above and uncomment below
//   //ParameterSetDescription desc;
//   //desc.addUntracked<edm::InputTag>("tracks","ctfWithMaterialTracks");
//   //descriptions.addDefault(desc);
// }

//define this as a plug-in
DEFINE_FWK_MODULE(sixbNtuplizer);

#endif //SIXBNTUPLIZER_H
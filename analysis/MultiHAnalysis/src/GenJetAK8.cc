#include "GenJetAK8.h"

#include "BuildP4.h"

void GenJetAK8::buildP4()
{
  p4_.BUILDP4(GenJetAK8, nat_);
}

void GenJetAK8ListCollection::Register(TString tag, std::unique_ptr<TTree>& tree_, std::map<std::string, bool>& branch_switches_) {
  branch_switches = branch_switches_;
  
  CHECK_BRANCH(E);
  CHECK_BRANCH(m);
  CHECK_BRANCH(pt);
  CHECK_BRANCH(eta);
  CHECK_BRANCH(phi);
  CHECK_BRANCH(signalId);
  CHECK_BRANCH(recoIdx);
  CHECK_BRANCH(hadronFlav);
  CHECK_BRANCH(partonFlav);
  CHECK_BRANCH(nsubjets);
  CHECK_BRANCH(subjet1_pt);
  CHECK_BRANCH(subjet1_m);
  CHECK_BRANCH(subjet1_eta);
  CHECK_BRANCH(subjet1_phi);
  CHECK_BRANCH(subjet2_pt);
  CHECK_BRANCH(subjet2_m);
  CHECK_BRANCH(subjet2_eta);
  CHECK_BRANCH(subjet2_phi);
}

void GenJetAK8ListCollection::Clear() {
  E.clear();
  m.clear();
  pt.clear();
  eta.clear();
  phi.clear();
  signalId.clear();
  recoIdx.clear();
  partonFlav.clear();
  hadronFlav.clear();
  nsubjets.clear();
  subjet1_pt.clear();
  subjet1_m.clear();
  subjet1_eta.clear();
  subjet1_phi.clear();
  subjet2_pt.clear();
  subjet2_m.clear();
  subjet2_eta.clear();
  subjet2_phi.clear();
}

void GenJetAK8ListCollection::Fill(const std::vector<GenJetAK8>& genjetak8s) {

  for (const GenJetAK8& fatjet : genjetak8s) {
      E.push_back( fatjet.get_E() );
      m.push_back( fatjet.get_m() );
      pt.push_back( fatjet.get_pt() );
      eta.push_back( fatjet.get_eta() );
      phi.push_back( fatjet.get_phi() );
      signalId.push_back( fatjet.get_signalId() );
      recoIdx.push_back( fatjet.get_recoIdx() );
      hadronFlav.push_back( fatjet.get_hadronFlav() );
      partonFlav.push_back( fatjet.get_partonFlav() );
      nsubjets.push_back( fatjet.get_nsubjets() );
      subjet1_pt.push_back( fatjet.get_subjet1_pt() );
      subjet1_eta.push_back( fatjet.get_subjet1_eta() );
      subjet1_phi.push_back( fatjet.get_subjet1_phi() );
      subjet1_m.push_back( fatjet.get_subjet1_mass() );
      subjet2_pt.push_back( fatjet.get_subjet2_pt() );
      subjet2_eta.push_back( fatjet.get_subjet2_eta() );
      subjet2_phi.push_back( fatjet.get_subjet2_phi() );
      subjet2_m.push_back(fatjet.get_subjet2_mass() );             
  }
}

void GenJetAK8Collection::Register(TString tag, std::unique_ptr<TTree>& tree_, std::map<std::string, bool>& branch_switches_) {
  branch_switches = branch_switches_;
  
  CHECK_BRANCH(E);
  CHECK_BRANCH(m);
  CHECK_BRANCH(pt);
  CHECK_BRANCH(eta);
  CHECK_BRANCH(phi);
  CHECK_BRANCH(signalId);
  CHECK_BRANCH(recoIdx);
  CHECK_BRANCH(hadronFlav);
  CHECK_BRANCH(partonFlav);
  CHECK_BRANCH(nsubjets);
  CHECK_BRANCH(subjet1_pt);
  CHECK_BRANCH(subjet1_m);
  CHECK_BRANCH(subjet1_eta);
  CHECK_BRANCH(subjet1_phi);
  CHECK_BRANCH(subjet2_pt);
  CHECK_BRANCH(subjet2_m);
  CHECK_BRANCH(subjet2_eta);
  CHECK_BRANCH(subjet2_phi);
}

void GenJetAK8Collection::Clear() {
  E = -999;
  m = -999;
  pt = -999;
  eta = -999;
  phi = -999;
  signalId = -999;
  recoIdx = -999;
  partonFlav = -999;
  hadronFlav = -999;
  nsubjets = -999;
  subjet1_pt = -999;
  subjet1_m = -999;
  subjet1_eta = -999;
  subjet1_phi = -999;
  subjet2_pt = -999;
  subjet2_m = -999;
  subjet2_eta = -999;
  subjet2_phi = -999;
}

void GenJetAK8Collection::Fill(const GenJetAK8& fatjet) {
    E = fatjet.get_E() ;
    m = fatjet.get_m() ;
    pt = fatjet.get_pt() ;
    eta = fatjet.get_eta() ;
    phi = fatjet.get_phi() ;
    signalId = fatjet.get_signalId() ;
    recoIdx = fatjet.get_recoIdx() ;
    hadronFlav = fatjet.get_hadronFlav() ;
    partonFlav = fatjet.get_partonFlav() ;
    nsubjets = fatjet.get_nsubjets() ;
    subjet1_pt = fatjet.get_subjet1_pt() ;
    subjet1_eta = fatjet.get_subjet1_eta() ;
    subjet1_phi = fatjet.get_subjet1_phi() ;
    subjet1_m = fatjet.get_subjet1_mass() ;
    subjet2_pt = fatjet.get_subjet2_pt() ;
    subjet2_eta = fatjet.get_subjet2_eta() ;
    subjet2_phi = fatjet.get_subjet2_phi() ;
    subjet2_m =fatjet.get_subjet2_mass() ;             
}

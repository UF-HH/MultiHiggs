#include "GenJet.h"

#include "BuildP4.h"

void GenJet::buildP4()
{
  p4_.BUILDP4(GenJet, nat_);
}



void GenJetListCollection::Register(TString tag, std::unique_ptr<TTree>& tree_, std::map<std::string, bool>& branch_switches_) {
  branch_switches = branch_switches_;
  
  CHECK_BRANCH(E);
  CHECK_BRANCH(m);
  CHECK_BRANCH(pt);
  CHECK_BRANCH(eta);
  CHECK_BRANCH(phi);
  CHECK_BRANCH(partonFlav);
  CHECK_BRANCH(hadronFlav);
  CHECK_BRANCH(signalId);
  CHECK_BRANCH(recoIdx);
}

void GenJetListCollection::Clear() {
  E.clear();
  m.clear();
  pt.clear();
  eta.clear();
  phi.clear();
  partonFlav.clear();
  hadronFlav.clear();
  signalId.clear();
  recoIdx.clear();
}

void GenJetListCollection::Fill(const std::vector<GenJet>& genjets) {
  for (const GenJet& jet : genjets) {
    E.push_back(jet.get_E());
    m.push_back(jet.get_m());
    pt.push_back(jet.get_pt());
    eta.push_back(jet.get_eta());
    phi.push_back(jet.get_phi());
    partonFlav.push_back( jet.get_partonFlav() );
    hadronFlav.push_back( jet.get_hadronFlav() );
    signalId.push_back( jet.get_signalId() );
    recoIdx.push_back( jet.get_recoIdx() );
  }
}


void GenJetCollection::Register(TString tag, std::unique_ptr<TTree>& tree_, std::map<std::string, bool>& branch_switches_) {
  branch_switches = branch_switches_;
  
  CHECK_BRANCH(E);
  CHECK_BRANCH(m);
  CHECK_BRANCH(pt);
  CHECK_BRANCH(eta);
  CHECK_BRANCH(phi);
  CHECK_BRANCH(partonFlav);
  CHECK_BRANCH(hadronFlav);
  CHECK_BRANCH(signalId);
}

void GenJetCollection::Clear() {
  E = -999;
  m = -999;
  pt = -999;
  eta = -999;
  phi = -999;
  partonFlav = -999;
  hadronFlav = -999;
  signalId = -999;
}

void GenJetCollection::Fill(const GenJet& jet) {
  E = jet.get_E();
  m = jet.get_m();
  pt = jet.get_pt();
  eta = jet.get_eta();
  phi = jet.get_phi();
  partonFlav =  jet.get_partonFlav();
  hadronFlav =  jet.get_hadronFlav();
  signalId =  jet.get_signalId();
}

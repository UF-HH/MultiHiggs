#include "Jet.h"
#include "GenJet.h"
#include "GenPart.h"
#include <iostream>
#include "BuildP4.h"

void Jet::buildP4() { p4_.BUILDP4(Jet, nat_); }

float Jet::getBregCorr() {
  //Determine the corr factor
  float corr = get_property((*this), Jet_bRegCorr);
  float res = get_property((*this), Jet_bRegRes);
  //The condition below needs to check in every NANOAOD release.
  //It is not implemmented in NANOAODv5. A similar condition for bRegRes is implemented on the OfflineProducerHelper as "Get_bRegRes"
  if (!((corr > 0.1) && (corr < 2) && (res > 0.005) && (res < 0.9))) {
    corr = 1.;
  } else if (get_property((*this), Jet_pt) < 20) {
    corr = 1.;
  }
  // else //Do nothing, use the NANOAOD correction value

  return corr;
}

float Jet::getBregRes() {
  //Determine the corr factor
  float corr = get_property((*this), Jet_bRegCorr);
  float res = get_property((*this), Jet_bRegRes);
  //The condition below needs to check in every NANOAOD release.  It is not implemmented in NANOAODv5.
  if (!((corr > 0.1) && (corr < 2) && (res > 0.005) && (res < 0.9))) {
    res = 0.2;
  } else if (get_property((*this), Jet_pt) < 20) {
    res = 0.2;
  }
  // else //Do nothing, use the NANOAOD correction value

  return res;
}

void Jet::buildP4Regressed() {
  if (p4_.Pt() == 0.)
    this->buildP4();

  //Apply regression
  float corr = getBregCorr();
  p4Regressed_ = corr * p4_;
}

void JetListCollection::Register(TString tag, std::unique_ptr<TTree>& tree_, std::map<std::string, bool>& branch_switches_) {
  branch_switches = branch_switches_;

  CHECK_BRANCH(E);
  CHECK_BRANCH(m);
  CHECK_BRANCH(mRegressed);
  CHECK_BRANCH(pt);
  CHECK_BRANCH(ptRegressed);
  CHECK_BRANCH(eta);
  CHECK_BRANCH(phi);
  CHECK_BRANCH(signalId);
  CHECK_BRANCH(btag);
  CHECK_BRANCH(qgl);
  CHECK_BRANCH(chEmEF);
  CHECK_BRANCH(chHEF);
  CHECK_BRANCH(neEmEF);
  CHECK_BRANCH(neHEF);
  CHECK_BRANCH(nConstituents);
  CHECK_BRANCH(id);
  CHECK_BRANCH(puid);

  if ( is_enabled("gen_brs") ) {
    CHECK_BRANCH(partonFlav);
    CHECK_BRANCH(hadronFlav);
  }
}

void JetListCollection::Clear() {
  E.clear();
  m.clear();
  mRegressed.clear();
  pt.clear();
  ptRegressed.clear();
  eta.clear();
  phi.clear();
  partonFlav.clear();
  hadronFlav.clear();
  signalId.clear();
  higgsIdx.clear();
  genIdx.clear();
  btag.clear();
  qgl.clear();
  chEmEF.clear();
  chHEF.clear();
  neEmEF.clear();
  neHEF.clear();
  nConstituents.clear();
  id.clear();
  puid.clear();
}

void JetListCollection::Fill(const std::vector<Jet>& jets) {
  bool gen_brs = is_enabled("gen_brs");

  for (const Jet& jet : jets) {
    E.push_back(jet.get_E());
    m.push_back(jet.get_m());
    mRegressed.push_back(jet.get_mRegressed());
    pt.push_back(jet.get_pt());
    ptRegressed.push_back(jet.get_ptRegressed());
    eta.push_back(jet.get_eta());
    phi.push_back(jet.get_phi());
    signalId.push_back(jet.get_signalId());
    higgsIdx.push_back(jet.get_higgsIdx());
    genIdx.push_back(jet.get_genIdx());

    if (gen_brs) {
      partonFlav.push_back(jet.get_partonFlav());
      hadronFlav.push_back(jet.get_hadronFlav());
    }

    btag.push_back(jet.get_btag());
    qgl.push_back(jet.get_qgl());
    chEmEF.push_back(jet.get_chEmEF());
    chHEF.push_back(jet.get_chHEF());
    neEmEF.push_back(jet.get_neEmEF());
    neHEF.push_back(jet.get_neHEF());
    nConstituents.push_back(jet.get_nConstituents());
    id.push_back(jet.get_id());
    puid.push_back(jet.get_puid());
  }
}

void JetCollection::Register(TString tag, std::unique_ptr<TTree>& tree_, std::map<std::string, bool>& branch_switches_) {
  branch_switches = branch_switches_;

  CHECK_BRANCH(E);
  CHECK_BRANCH(m);
  CHECK_BRANCH(mRegressed);
  CHECK_BRANCH(pt);
  CHECK_BRANCH(ptRegressed);
  CHECK_BRANCH(eta);
  CHECK_BRANCH(phi);
  CHECK_BRANCH(signalId);
  CHECK_BRANCH(btag);
  CHECK_BRANCH(qgl);
  CHECK_BRANCH(chEmEF);
  CHECK_BRANCH(chHEF);
  CHECK_BRANCH(neEmEF);
  CHECK_BRANCH(neHEF);
  CHECK_BRANCH(nConstituents);
  CHECK_BRANCH(id);
  CHECK_BRANCH(puid);

  if ( is_enabled("gen_brs") ) {
    CHECK_BRANCH(partonFlav);
    CHECK_BRANCH(hadronFlav);
  }
}

void JetCollection::Clear() {
  E = -999;
  m = -999;
  mRegressed = -999;
  pt = -999;
  ptRegressed = -999;
  eta = -999;
  phi = -999;
  partonFlav = -999;
  hadronFlav = -999;
  signalId = -999;
  btag = -999;
  qgl = -999;
  chEmEF = -999;
  chHEF = -999;
  neEmEF = -999;
  neHEF = -999;
  nConstituents = -999;
  id = -999;
  puid = -999;
}

void JetCollection::Fill(const Jet& jet) {
  bool gen_brs = is_enabled("gen_brs");
  
  E = jet.get_E();
  m = jet.get_m();
  mRegressed = jet.get_mRegressed();
  pt = jet.get_pt();
  ptRegressed = jet.get_ptRegressed();
  eta = jet.get_eta();
  phi = jet.get_phi();
  signalId = jet.get_signalId();

  if (gen_brs) {
    partonFlav = jet.get_partonFlav();
    hadronFlav = jet.get_hadronFlav();
  }

  btag = jet.get_btag();
  qgl = jet.get_qgl();
  chEmEF = jet.get_chEmEF();
  chHEF = jet.get_chHEF();
  neEmEF = jet.get_neEmEF();
  neHEF = jet.get_neHEF();
  nConstituents = jet.get_nConstituents();
  id = jet.get_id();
  puid = jet.get_puid();
}
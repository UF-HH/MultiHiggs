#include "FatJet.h"
#include <iostream>
#include "BuildP4.h"

void FatJet::buildP4() { p4_.BUILDP4(FatJet, nat_); }

void FatJetListCollection::Register(TString tag,
                                    std::unique_ptr<TTree>& tree_,
                                    std::map<std::string, bool>& branch_switches_) {
  branch_switches = branch_switches_;

  CHECK_BRANCH(pt);
  CHECK_BRANCH(eta);
  CHECK_BRANCH(phi);
  CHECK_BRANCH(m);
  CHECK_BRANCH(mSD_UnCorrected);
  CHECK_BRANCH(area);
  CHECK_BRANCH(n2b1);
  CHECK_BRANCH(n3b1);
  CHECK_BRANCH(rawFactor);
  CHECK_BRANCH(tau1);
  CHECK_BRANCH(tau2);
  CHECK_BRANCH(tau3);
  CHECK_BRANCH(tau4);
  CHECK_BRANCH(jetId);
  CHECK_BRANCH(genJetAK8Idx);
  CHECK_BRANCH(hadronFlavour);
  CHECK_BRANCH(nBHadrons);
  CHECK_BRANCH(nCHadrons);

  if (is_enabled("run3_brs", false)) {
    CHECK_BRANCH(nPFCand);
    CHECK_BRANCH(PNetQCDb);
    CHECK_BRANCH(PNetQCDbb);
    CHECK_BRANCH(PNetQCDc);
    CHECK_BRANCH(PNetQCDcc);
    CHECK_BRANCH(PNetQCDothers);
    CHECK_BRANCH(PNetXbb);
    CHECK_BRANCH(PNetXcc);
    CHECK_BRANCH(PNetXqq);
    CHECK_BRANCH(deepTagMD_H4q);
    CHECK_BRANCH(deepTagMD_Hbb);
    CHECK_BRANCH(deepTagMD_T);
    CHECK_BRANCH(deepTagMD_W);
    CHECK_BRANCH(deepTagMD_Z);
    CHECK_BRANCH(deepTagMD_bbvsL);
    CHECK_BRANCH(deepTagMD_ccvsL);
    CHECK_BRANCH(deepTag_QCD);
    CHECK_BRANCH(deepTag_QCDothers);
    CHECK_BRANCH(deepTag_W);
    CHECK_BRANCH(deepTag_Z);
    CHECK_BRANCH(nsubjets);
    CHECK_BRANCH(subjet1_pt);
    CHECK_BRANCH(subjet1_eta);
    CHECK_BRANCH(subjet1_phi);
    CHECK_BRANCH(subjet1_m);
    CHECK_BRANCH(subjet2_btagDeepB);
    CHECK_BRANCH(subjet2_pt);
    CHECK_BRANCH(subjet2_eta);
    CHECK_BRANCH(subjet2_phi);
    CHECK_BRANCH(subjet2_m);
    CHECK_BRANCH(subjet2_btagDeepB);
  }
}

void FatJetListCollection::Clear() {
  pt.clear();
  eta.clear();
  phi.clear();
  m.clear();
  mSD_UnCorrected.clear();
  area.clear();
  n2b1.clear();
  n3b1.clear();
  rawFactor.clear();
  tau1.clear();
  tau2.clear();
  tau3.clear();
  tau4.clear();
  jetId.clear();
  genJetAK8Idx.clear();
  hadronFlavour.clear();
  nBHadrons.clear();
  nCHadrons.clear();
  nPFCand.clear();
  PNetQCDb.clear();
  PNetQCDbb.clear();
  PNetQCDc.clear();
  PNetQCDcc.clear();
  PNetQCDothers.clear();
  PNetXbb.clear();
  PNetXcc.clear();
  PNetXqq.clear();
  deepTagMD_H4q.clear();
  deepTagMD_Hbb.clear();
  deepTagMD_T.clear();
  deepTagMD_W.clear();
  deepTagMD_Z.clear();
  deepTagMD_bbvsL.clear();
  deepTagMD_ccvsL.clear();
  deepTag_QCD.clear();
  deepTag_QCDothers.clear();
  deepTag_W.clear();
  deepTag_Z.clear();
  nsubjets.clear();
  subjet1_pt.clear();
  subjet1_eta.clear();
  subjet1_phi.clear();
  subjet1_m.clear();
  subjet1_btagDeepB.clear();
  subjet2_pt.clear();
  subjet2_eta.clear();
  subjet2_phi.clear();
  subjet2_m.clear();
  subjet2_btagDeepB.clear();
}

void FatJetListCollection::Fill(const std::vector<FatJet>& fatjets) {
  for (const FatJet& fatjet : fatjets) {
    pt.push_back(fatjet.get_pt());
    eta.push_back(fatjet.get_eta());
    phi.push_back(fatjet.get_phi());
    m.push_back(fatjet.get_mass());
    mSD_UnCorrected.push_back(fatjet.get_massSD_UnCorrected());
    area.push_back(fatjet.get_area());
    n2b1.push_back(fatjet.get_n2b1());
    n3b1.push_back(fatjet.get_n3b1());
    rawFactor.push_back(fatjet.get_rawFactor());
    tau1.push_back(fatjet.get_tau1());
    tau2.push_back(fatjet.get_tau2());
    tau3.push_back(fatjet.get_tau3());
    tau4.push_back(fatjet.get_tau4());
    jetId.push_back(fatjet.get_jetId());
    genJetAK8Idx.push_back(fatjet.get_genJetAK8Idx());
    hadronFlavour.push_back(fatjet.get_hadronFlavour());
    nBHadrons.push_back(fatjet.get_nBHadrons());
    nCHadrons.push_back(fatjet.get_nCHadrons());

    if (is_enabled("run3_brs", false)) {
      nPFCand.push_back(fatjet.get_nPFCand());
      PNetQCDb.push_back(fatjet.get_PNetQCDb());
      PNetQCDbb.push_back(fatjet.get_PNetQCDbb());
      PNetQCDc.push_back(fatjet.get_PNetQCDc());
      PNetQCDcc.push_back(fatjet.get_PNetQCDcc());
      PNetQCDothers.push_back(fatjet.get_PNetQCDothers());
      PNetXbb.push_back(fatjet.get_PNetXbb());
      PNetXcc.push_back(fatjet.get_PNetXcc());
      PNetXqq.push_back(fatjet.get_PNetXqq());
      deepTagMD_H4q.push_back(fatjet.get_deepTagMD_H4q());
      deepTagMD_Hbb.push_back(fatjet.get_deepTagMD_Hbb());
      deepTagMD_T.push_back(fatjet.get_deepTagMD_T());
      deepTagMD_W.push_back(fatjet.get_deepTagMD_W());
      deepTagMD_Z.push_back(fatjet.get_deepTagMD_Z());
      deepTagMD_bbvsL.push_back(fatjet.get_deepTagMD_bbvsL());
      deepTagMD_ccvsL.push_back(fatjet.get_deepTagMD_ccvsL());
      deepTag_QCD.push_back(fatjet.get_deepTag_QCD());
      deepTag_QCDothers.push_back(fatjet.get_deepTag_QCDothers());
      deepTag_W.push_back(fatjet.get_deepTag_W());
      deepTag_Z.push_back(fatjet.get_deepTag_Z());
      nsubjets.push_back(fatjet.get_subjets().size());
      subjet1_pt.push_back(fatjet.get_subjet1_pt());
      subjet1_eta.push_back(fatjet.get_subjet1_eta());
      subjet1_phi.push_back(fatjet.get_subjet1_phi());
      subjet1_m.push_back(fatjet.get_subjet1_mass());
      subjet1_btagDeepB.push_back(fatjet.get_subjet1_btagDeepB());
      subjet2_pt.push_back(fatjet.get_subjet2_pt());
      subjet2_eta.push_back(fatjet.get_subjet2_eta());
      subjet2_phi.push_back(fatjet.get_subjet2_phi());
      subjet2_m.push_back(fatjet.get_subjet2_mass());
      subjet2_btagDeepB.push_back(fatjet.get_subjet2_btagDeepB());
    }
  }
}

void FatJetCollection::Register(TString tag,
                                std::unique_ptr<TTree>& tree_,
                                std::map<std::string, bool>& branch_switches_) {
  branch_switches = branch_switches_;

  CHECK_BRANCH(pt);
  CHECK_BRANCH(eta);
  CHECK_BRANCH(phi);
  CHECK_BRANCH(m);
  CHECK_BRANCH(mSD_UnCorrected);
  CHECK_BRANCH(area);
  CHECK_BRANCH(n2b1);
  CHECK_BRANCH(n3b1);
  CHECK_BRANCH(rawFactor);
  CHECK_BRANCH(tau1);
  CHECK_BRANCH(tau2);
  CHECK_BRANCH(tau3);
  CHECK_BRANCH(tau4);
  CHECK_BRANCH(jetId);
  CHECK_BRANCH(genJetAK8Idx);
  CHECK_BRANCH(hadronFlavour);
  CHECK_BRANCH(nBHadrons);
  CHECK_BRANCH(nCHadrons);

  if (is_enabled("run3_brs", false)) {
    CHECK_BRANCH(nPFCand);
    CHECK_BRANCH(PNetQCDb);
    CHECK_BRANCH(PNetQCDbb);
    CHECK_BRANCH(PNetQCDc);
    CHECK_BRANCH(PNetQCDcc);
    CHECK_BRANCH(PNetQCDothers);
    CHECK_BRANCH(PNetXbb);
    CHECK_BRANCH(PNetXcc);
    CHECK_BRANCH(PNetXqq);
    CHECK_BRANCH(deepTagMD_H4q);
    CHECK_BRANCH(deepTagMD_Hbb);
    CHECK_BRANCH(deepTagMD_T);
    CHECK_BRANCH(deepTagMD_W);
    CHECK_BRANCH(deepTagMD_Z);
    CHECK_BRANCH(deepTagMD_bbvsL);
    CHECK_BRANCH(deepTagMD_ccvsL);
    CHECK_BRANCH(deepTag_QCD);
    CHECK_BRANCH(deepTag_QCDothers);
    CHECK_BRANCH(deepTag_W);
    CHECK_BRANCH(deepTag_Z);
    CHECK_BRANCH(nsubjets);
    CHECK_BRANCH(subjet1_pt);
    CHECK_BRANCH(subjet1_eta);
    CHECK_BRANCH(subjet1_phi);
    CHECK_BRANCH(subjet1_m);
    CHECK_BRANCH(subjet2_btagDeepB);
    CHECK_BRANCH(subjet2_pt);
    CHECK_BRANCH(subjet2_eta);
    CHECK_BRANCH(subjet2_phi);
    CHECK_BRANCH(subjet2_m);
    CHECK_BRANCH(subjet2_btagDeepB);
  }
}

void FatJetCollection::Clear() {
  pt = -999;
  eta = -999;
  phi = -999;
  m = -999;
  mSD_UnCorrected = -999;
  area = -999;
  n2b1 = -999;
  n3b1 = -999;
  rawFactor = -999;
  tau1 = -999;
  tau2 = -999;
  tau3 = -999;
  tau4 = -999;
  jetId = -999;
  genJetAK8Idx = -999;
  hadronFlavour = -999;
  nBHadrons = -999;
  nCHadrons = -999;
  nPFCand = -999;
  PNetQCDb = -999;
  PNetQCDbb = -999;
  PNetQCDc = -999;
  PNetQCDcc = -999;
  PNetQCDothers = -999;
  PNetXbb = -999;
  PNetXcc = -999;
  PNetXqq = -999;
  deepTagMD_H4q = -999;
  deepTagMD_Hbb = -999;
  deepTagMD_T = -999;
  deepTagMD_W = -999;
  deepTagMD_Z = -999;
  deepTagMD_bbvsL = -999;
  deepTagMD_ccvsL = -999;
  deepTag_QCD = -999;
  deepTag_QCDothers = -999;
  deepTag_W = -999;
  deepTag_Z = -999;
  nsubjets = -999;
  subjet1_pt = -999;
  subjet1_eta = -999;
  subjet1_phi = -999;
  subjet1_m = -999;
  subjet1_btagDeepB = -999;
  subjet2_pt = -999;
  subjet2_eta = -999;
  subjet2_phi = -999;
  subjet2_m = -999;
  subjet2_btagDeepB = -999;
}

void FatJetCollection::Fill(const FatJet& fatjet) {
  pt = fatjet.get_pt();
  eta = fatjet.get_eta();
  phi = fatjet.get_phi();
  m = fatjet.get_mass();
  mSD_UnCorrected = fatjet.get_massSD_UnCorrected();
  area = fatjet.get_area();
  n2b1 = fatjet.get_n2b1();
  n3b1 = fatjet.get_n3b1();
  rawFactor = fatjet.get_rawFactor();
  tau1 = fatjet.get_tau1();
  tau2 = fatjet.get_tau2();
  tau3 = fatjet.get_tau3();
  tau4 = fatjet.get_tau4();
  jetId = fatjet.get_jetId();
  genJetAK8Idx = fatjet.get_genJetAK8Idx();
  hadronFlavour = fatjet.get_hadronFlavour();
  nBHadrons = fatjet.get_nBHadrons();
  nCHadrons = fatjet.get_nCHadrons();

  if (is_enabled("run3_brs", false)) {
    nPFCand = fatjet.get_nPFCand();
    PNetQCDb = fatjet.get_PNetQCDb();
    PNetQCDbb = fatjet.get_PNetQCDbb();
    PNetQCDc = fatjet.get_PNetQCDc();
    PNetQCDcc = fatjet.get_PNetQCDcc();
    PNetQCDothers = fatjet.get_PNetQCDothers();
    PNetXbb = fatjet.get_PNetXbb();
    PNetXcc = fatjet.get_PNetXcc();
    PNetXqq = fatjet.get_PNetXqq();
    deepTagMD_H4q = fatjet.get_deepTagMD_H4q();
    deepTagMD_Hbb = fatjet.get_deepTagMD_Hbb();
    deepTagMD_T = fatjet.get_deepTagMD_T();
    deepTagMD_W = fatjet.get_deepTagMD_W();
    deepTagMD_Z = fatjet.get_deepTagMD_Z();
    deepTagMD_bbvsL = fatjet.get_deepTagMD_bbvsL();
    deepTagMD_ccvsL = fatjet.get_deepTagMD_ccvsL();
    deepTag_QCD = fatjet.get_deepTag_QCD();
    deepTag_QCDothers = fatjet.get_deepTag_QCDothers();
    deepTag_W = fatjet.get_deepTag_W();
    deepTag_Z = fatjet.get_deepTag_Z();
    nsubjets = fatjet.get_subjets().size();
    subjet1_pt = fatjet.get_subjet1_pt();
    subjet1_eta = fatjet.get_subjet1_eta();
    subjet1_phi = fatjet.get_subjet1_phi();
    subjet1_m = fatjet.get_subjet1_mass();
    subjet1_btagDeepB = fatjet.get_subjet1_btagDeepB();
    subjet2_pt = fatjet.get_subjet2_pt();
    subjet2_eta = fatjet.get_subjet2_eta();
    subjet2_phi = fatjet.get_subjet2_phi();
    subjet2_m = fatjet.get_subjet2_mass();
    subjet2_btagDeepB = fatjet.get_subjet2_btagDeepB();
  }
}

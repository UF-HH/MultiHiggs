#ifndef FATJET_H
#define FATJET_H

#include "Candidate.h"
#include "SubJet.h"

class FatJet : public Candidate
{
public:
  FatJet () : Candidate(){typeId_=6;}
  FatJet (int idx, NanoAODTree* nat) : Candidate(idx, nat){
    typeId_=6;
    buildP4(); 
  }
  ~FatJet(){};
  std::unique_ptr<Candidate> clone() const override{
    FatJet *clonedFatJet = new FatJet(this->getIdx(), this->getNanoAODTree());
    clonedFatJet->setP4(this->P4());
    clonedFatJet->params = this->params;
    return std::unique_ptr<FatJet>(clonedFatJet);
  }
  int signalId = -1;
  void set_signalId(int id) { signalId = id; }

  int higgsIdx = -1;
  void set_higgsIdx(int id) { higgsIdx = id; }
	
  int genIdx = -1;
  void set_genIdx(int idx) { genIdx = idx; }

  int preselIdx = -1;
  void set_preselIdx(int idx) { preselIdx = idx; }
  
  float get_pt() const { return get_property((*this), FatJet_pt); }
  float get_eta() const { return get_property((*this), FatJet_eta); }
  float get_mass() const { return get_property((*this), FatJet_mass); }
  float get_massSD_UnCorrected() const { return get_property((*this), FatJet_msoftdrop); }
  float get_n2b1() const { return get_property((*this), FatJet_n2b1); }
  float get_n3b1() const { return get_property((*this), FatJet_n3b1); }
  float get_phi() const { return get_property((*this), FatJet_phi); }
  float get_rawFactor() const { return get_property((*this), FatJet_rawFactor); }
  float get_tau1() const { return get_property((*this), FatJet_tau1); }
  float get_tau2() const { return get_property((*this), FatJet_tau2); }
  float get_tau3() const { return get_property((*this), FatJet_tau3); }
  float get_tau4() const { return get_property((*this), FatJet_tau4); }
  int get_jetId() const { return get_property((*this), FatJet_jetId); }
  int get_subJetIdx1() const { return get_property((*this), FatJet_subJetIdx1); }
  int get_subJetIdx2() const { return get_property((*this), FatJet_subJetIdx2); }
  int get_genJetAK8Idx() const { return get_property((*this), FatJet_genJetAK8Idx); }
  int get_hadronFlavour() const { return get_property((*this), FatJet_hadronFlavour); }
  int get_nBHadrons() const { return get_property((*this), FatJet_nBHadrons); }
  int get_nCHadrons() const { return get_property((*this), FatJet_nCHadrons); }
  int get_nPFCand() const { return get_property((*this), FatJet_nPFCand); }
  float get_area() const { return get_property((*this), FatJet_area); }
  
  // Particle Net taggers:
  float get_PNetQCDb() const { return get_property((*this), FatJet_ParticleNetMD_probQCDb); }
  float get_PNetQCDbb() const { return get_property((*this), FatJet_ParticleNetMD_probQCDbb); }
  float get_PNetQCDc() const { return get_property((*this), FatJet_ParticleNetMD_probQCDc); }
  float get_PNetQCDcc() const { return get_property((*this), FatJet_ParticleNetMD_probQCDcc); }
  float get_PNetQCDothers() const { return get_property((*this), FatJet_ParticleNetMD_probQCDothers); }
  float get_PNetXbb() const { return get_property((*this), FatJet_ParticleNetMD_probXbb); }
  float get_PNetXcc() const { return get_property((*this), FatJet_ParticleNetMD_probXcc); }
  float get_PNetXqq() const { return get_property((*this), FatJet_ParticleNetMD_probXqq); }
  
  float get_deepTagMD_H4q() const { return get_property((*this), FatJet_deepTagMD_H4qvsQCD); }
  float get_deepTagMD_Hbb() const { return get_property((*this), FatJet_deepTagMD_HbbvsQCD); }
  float get_deepTagMD_T() const { return get_property((*this), FatJet_deepTagMD_TvsQCD); }
  float get_deepTagMD_W() const { return get_property((*this), FatJet_deepTagMD_WvsQCD); }
  float get_deepTagMD_Z() const { return get_property((*this), FatJet_deepTagMD_ZvsQCD); }
  float get_deepTagMD_bbvsL() const { return get_property((*this), FatJet_deepTagMD_bbvsLight); }
  float get_deepTagMD_ccvsL() const { return get_property((*this), FatJet_deepTagMD_ccvsLight); }
  
  float get_deepTag_QCD() const { return get_property((*this), FatJet_deepTag_QCD); }
  float get_deepTag_QCDothers() const { return get_property((*this), FatJet_deepTag_QCDothers); }
  
  float get_deepTag_W() const { return get_property((*this), FatJet_deepTag_WvsQCD); }
  float get_deepTag_Z() const { return get_property((*this), FatJet_deepTag_ZvsQCD); }
  
  std::vector<SubJet> get_subjets() const
    {
      std::vector<SubJet> subjets;
      if (get_property((*this), FatJet_subJetIdx1) != -1)
	{
	  SubJet subjet1(get_property((*this), FatJet_subJetIdx1), this->getNanoAODTree());
	  subjets.push_back(subjet1);
	  
	  if (get_property((*this), FatJet_subJetIdx2) != -1)
	    {
	      SubJet subjet2(get_property((*this), FatJet_subJetIdx2), this->getNanoAODTree());
	      subjets.push_back(subjet2);
	    }
	}
      return subjets;
    }
  
  float get_subjet1_pt() const {
    if (get_property((*this), FatJet_subJetIdx1) != -1)
      {
	SubJet subjet(get_property((*this), FatJet_subJetIdx1), this->getNanoAODTree());
	return subjet.get_pt();
      }
    else return -99.0;
  }
  float get_subjet1_eta() const {
    if (get_property((*this), FatJet_subJetIdx1) != -1)
      {
	SubJet subjet(get_property((*this), FatJet_subJetIdx1), this->getNanoAODTree());
	return subjet.get_eta();
      }
    else return -99.0;
  }
  float get_subjet1_phi() const {
    if (get_property((*this), FatJet_subJetIdx1) != -1)
      {
	SubJet subjet(get_property((*this), FatJet_subJetIdx1), this->getNanoAODTree());
	return subjet.get_phi();
      }
    else return -99.0;
  }
  float get_subjet1_mass() const {
    if (get_property((*this), FatJet_subJetIdx1) != -1)
      {
	SubJet subjet(get_property((*this), FatJet_subJetIdx1), this->getNanoAODTree());
	return subjet.get_mass();
      }
    else return -99.0;
  }
  float get_subjet1_btagDeepB() const {
    if (get_property((*this), FatJet_subJetIdx1) != -1)
      {
	SubJet subjet(get_property((*this), FatJet_subJetIdx1), this->getNanoAODTree());
	return subjet.get_btagDeepB();
      }
    else return -99.0;
  }
  float get_subjet2_pt() const {
    if (get_property((*this), FatJet_subJetIdx2) != -1)
      {
	SubJet subjet(get_property((*this), FatJet_subJetIdx2), this->getNanoAODTree());
	return subjet.get_pt();
      }
    else return -99.0;
  }
  float get_subjet2_eta() const {
    if (get_property((*this), FatJet_subJetIdx2) != -1)
      {
	SubJet subjet(get_property((*this), FatJet_subJetIdx2), this->getNanoAODTree());
	return subjet.get_eta();
      }
    else return -99.0;
  }
  float get_subjet2_phi() const {
    if (get_property((*this), FatJet_subJetIdx2) != -1)
      {
	SubJet subjet(get_property((*this), FatJet_subJetIdx2), this->getNanoAODTree());
	return subjet.get_phi();
      }
    else return -99.0;
  }
  float get_subjet2_mass() const {
    if (get_property((*this), FatJet_subJetIdx2) != -1)
      {
	SubJet subjet(get_property((*this), FatJet_subJetIdx2), this->getNanoAODTree());
	return subjet.get_mass();
      }
    else return -99.0;
  }
  float get_subjet2_btagDeepB() const {
    if (get_property((*this), FatJet_subJetIdx2) != -1)
      {
	SubJet subjet(get_property((*this), FatJet_subJetIdx2), this->getNanoAODTree());
	return subjet.get_btagDeepB();
      }
    else return -99.0;
  }
  
private:
  void buildP4() override; 
  
  
};

#endif
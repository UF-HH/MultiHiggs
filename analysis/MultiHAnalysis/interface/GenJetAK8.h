#ifndef GENJETAK8_H
#define GENJETAK8_H

#include "Candidate.h"
#include "SubGenJetAK8.h"

class GenJetAK8 : public Candidate
{
public:
  GenJetAK8 () : Candidate(){}
  GenJetAK8 (int idx, NanoAODTree* nat) : Candidate(idx, nat){buildP4();}
  ~GenJetAK8(){};
  std::unique_ptr<Candidate> clone() const {
    GenJetAK8 *clonedGenJetAK8 = new GenJetAK8(this->getIdx(), this->getNanoAODTree());
    clonedGenJetAK8->setP4(this->P4());
    return std::unique_ptr<GenJetAK8> (clonedGenJetAK8);
  }

  int signalId = -1;
  void set_signalId(int id) { signalId = id; }

  int recoIdx = -1;
  void set_recoIdx(int idx) { recoIdx = idx; }
  
  float get_E() const        { return this->P4().E(); }
  float get_m() const        { return this->P4().M(); }
  float get_pt() const       { return this->P4().Pt(); }
  float get_eta() const      { return this->P4().Eta(); }
  float get_phi() const      { return this->P4().Phi(); }
  int get_signalId() const   { return signalId; }
  int get_recoIdx() const    { return recoIdx; }
  int get_hadronFlav() const { return get_property((*this), GenJetAK8_hadronFlavour); }
  int get_partonFlav() const { return get_property((*this), GenJetAK8_partonFlavour); }
  
  std::vector<SubGenJetAK8> get_subjets() const
    {
      float fatjet_phi = get_property((*this), GenJetAK8_phi);
      float fatjet_eta = get_property((*this), GenJetAK8_eta);
      std::vector<SubGenJetAK8> subjets;
      for (unsigned int i=0; i<*(this->getNanoAODTree()->nSubGenJetAK8); i++)
	{
	  SubGenJetAK8 subjet(i, this->getNanoAODTree());
	  float dPhi = TMath::Abs(TMath::Abs(TMath::Abs(subjet.get_phi() - fatjet_phi) - TMath::Pi())-TMath::Pi());
	  float dEta = subjet.get_eta() - fatjet_eta;
	  float dR2 = dPhi*dPhi + dEta*dEta;
	  float dR  = std::sqrt(dR2);
	  if (dR < 0.8) subjets.push_back(subjet);
	}
      return subjets;
    }
  
  int get_nsubjets() const {
    return this->get_subjets().size();
  }
  
  float get_subjet1_pt() const {
    if (this->get_subjets().size() > 0) return this->get_subjets().at(0).get_pt();
    else return -99.9;
  }
  
  float get_subjet1_eta() const {
    if (this->get_nsubjets() > 0)
      return this->get_subjets().at(0).get_eta();
    else return -99.9;
  }
  
  float get_subjet1_mass() const {
    if (this->get_nsubjets() > 0)
      return this->get_subjets().at(0).get_mass();
    else return -99.9;
  }
  
  float get_subjet1_phi() const {
    if (this->get_nsubjets() > 0)
      return this->get_subjets().at(0).get_phi();
    else return -99.9;
  }
  
  float get_subjet2_pt() const {
    if (this->get_nsubjets() > 1)
      return this->get_subjets().at(1).get_pt();
    else return -99.9;
  }
  
  float get_subjet2_eta() const {
    if (this->get_nsubjets() > 1)
      return this->get_subjets().at(1).get_eta();
    else return -99.9;
  }
  
  float get_subjet2_mass() const {
    if (this->get_nsubjets() > 1)
      return this->get_subjets().at(1).get_mass();
    else return -99.9;
  }
  
  float get_subjet2_phi() const {
    if (this->get_nsubjets() > 1)
      return this->get_subjets().at(1).get_phi();
    else return -99.9;
  }
    
 private:
  void buildP4(); 
};

#endif
#ifndef SUBGENJETAK8_H
#define SUBGENJETAK8_H

#include "Candidate.h"

class SubGenJetAK8 : public Candidate
{
public:
  SubGenJetAK8 () : Candidate(){}
  SubGenJetAK8 (int idx, NanoAODTree* nat) : Candidate(idx, nat){buildP4();}
  ~SubGenJetAK8(){};
  std::unique_ptr<Candidate> clone() const {
    SubGenJetAK8 *clonedSubGenJetAK8 = new SubGenJetAK8(this->getIdx(), this->getNanoAODTree());
    clonedSubGenJetAK8->setP4(this->P4());
    return std::unique_ptr<SubGenJetAK8> (clonedSubGenJetAK8);
  }
  
  float get_eta() const { return get_property((*this), SubGenJetAK8_eta); }
  float get_mass() const { return get_property((*this), SubGenJetAK8_mass); }
  float get_pt() const { return get_property((*this), SubGenJetAK8_pt); }
  float get_phi() const { return get_property((*this), SubGenJetAK8_phi); }
  
private:
  void buildP4(); 
};

#endif

#ifndef SUBJET_H
#define SUBJET_H

#include "Candidate.h"

class SubJet : public Candidate
{
 public:
  SubJet () : Candidate(){typeId_=6;}
  SubJet (int idx, NanoAODTree* nat) : Candidate(idx, nat){
    typeId_=6;
    buildP4();
  }
  ~SubJet(){};
  std::unique_ptr<Candidate> clone() const override{
    SubJet *clonedSubJet = new SubJet(this->getIdx(), this->getNanoAODTree());
    clonedSubJet->setP4(this->P4());
    clonedSubJet->params = this->params;
    return std::unique_ptr<SubJet>(clonedSubJet);
  }
  
  float get_pt() const { return get_property((*this), SubJet_pt); }
  float get_phi() const { return get_property((*this), SubJet_phi); }
  float get_eta() const { return get_property((*this), SubJet_eta); }
  float get_mass() const { return get_property((*this), SubJet_mass); }
  float get_n2b1() const { return get_property((*this), SubJet_n2b1); }
  float get_n3b1() const { return get_property((*this), SubJet_n3b1); }
  float get_tau1() const { return get_property((*this), SubJet_tau1); }
  float get_tau2() const { return get_property((*this), SubJet_tau2); }
  float get_tau3() const { return get_property((*this), SubJet_tau3); }
  float get_tau4() const { return get_property((*this), SubJet_tau4); }
  float get_btagDeepB() const { return get_property((*this), SubJet_btagDeepB); }

 private:
  void buildP4() override;
};

#endif

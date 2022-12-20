#ifndef GENJETAK8_H
#define GENJETAK8_H

#include "Candidate.h"

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

private:
  void buildP4(); 
};

#endif

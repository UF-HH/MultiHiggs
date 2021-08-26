#ifndef GENJET_H
#define GENJET_H

#include "Candidate.h"

class GenJet : public Candidate
{
public:
  GenJet () : Candidate(){}
  GenJet (int idx, NanoAODTree* nat) : Candidate(idx, nat){buildP4();}
  ~GenJet(){};
  std::unique_ptr<Candidate> clone() const {
    GenJet *clonedGenJet = new GenJet(this->getIdx(), this->getNanoAODTree());
    clonedGenJet->setP4(this->P4());
    return std::unique_ptr<GenJet> (clonedGenJet);
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
  int get_partonFlav() const { return get_property ((*this), Jet_partonFlavour); }
  int get_hadronFlav() const { return get_property ((*this), Jet_hadronFlavour); }
  int get_signalId() const   { return signalId; }
  int get_recoIdx() const    { return recoIdx; }
private:
  void buildP4(); 
};

#endif

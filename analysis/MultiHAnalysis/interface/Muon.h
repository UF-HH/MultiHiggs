#ifndef MUON_H
#define MUON_H

#include "Candidate.h"

class Muon : public Candidate
{
public:
  Muon () : Candidate(){typeId_=13;}
  Muon (int idx, NanoAODTree* nat) : Candidate(idx, nat){typeId_=13; buildP4();}
  ~Muon(){};
  std::unique_ptr<Candidate> clone() const override{
    Muon *clonedMuon = new Muon(this->getIdx(), this->getNanoAODTree());
    clonedMuon->setP4(this->P4());
    return std::unique_ptr<Muon> (clonedMuon);
  }

  float get_E() const { return this->P4().E(); }
  float get_m() const { return this->P4().M(); }
  float get_pt() const { return this->P4().Pt(); }
  float get_eta() const { return this->P4().Eta(); }
  float get_phi() const { return this->P4().Phi(); }
  float get_dxy() const { return get_property((*this), Muon_dxy); }
  float get_dz() const { return get_property((*this), Muon_dz); }
  float get_charge() const { return get_property((*this), Muon_charge); }
  float get_pfRelIso04_all() const { return get_property((*this), Muon_pfRelIso04_all); }
  bool get_looseId() const { return get_property((*this), Muon_looseId); }
  bool get_mediumId() const { return get_property((*this), Muon_mediumId); }
  bool get_tightId() const { return get_property((*this), Muon_tightId); }
  
private:
  void buildP4() override; 
};

#endif

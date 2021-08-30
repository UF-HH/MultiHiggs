#ifndef JET_H
#define JET_H

#include "Candidate.h"

class Jet : public Candidate
{
public:
  Jet () : Candidate(){typeId_=1;}
  Jet (int idx, NanoAODTree* nat) : Candidate(idx, nat){
    typeId_=1;
    buildP4Regressed();
    buildP4(); 
  }
  ~Jet(){};
  std::unique_ptr<Candidate> clone() const override{
    Jet *clonedJet = new Jet(this->getIdx(), this->getNanoAODTree());
    clonedJet->setP4Regressed(this->P4Regressed());
    clonedJet->setP4(this->P4());
    return std::unique_ptr<Jet> (clonedJet);
  }
  float getBregCorr();
  float getBregRes();
  p4_t P4Regressed() const      {return p4Regressed_;}
  void setP4Regressed( p4_t p4Regressed) {p4Regressed_ = p4Regressed;}
        
  p4_t p4Regressed_;
  void buildP4Regressed();

  int signalId = -1;
  void set_signalId(int id) { signalId = id; }

  int higgsIdx = -1;
  void set_higgsIdx(int id) { higgsIdx = id; }
	
  int genIdx = -1;
  void set_genIdx(int idx) { genIdx = idx; }

  int preselIdx = -1;
  void set_preselIdx(int idx) { preselIdx = idx; }

	
  float get_E() const        { return this->P4().E(); }
  float get_m() const        { return this->P4().M(); }
  float get_pt() const       { return this->P4Regressed().Pt(); }
  float get_eta() const      { return this->P4().Eta(); }
  float get_phi() const      { return this->P4().Phi(); }
  int get_partonFlav() const { return get_property ((*this), Jet_partonFlavour); }
  int get_hadronFlav() const { return get_property ((*this), Jet_hadronFlavour); }
  int get_signalId() const   { return signalId; }
  int get_higgsIdx() const    { return higgsIdx; }
  int get_genIdx() const     { return genIdx; }
  float get_btag() const     { return get_property ((*this), Jet_btagDeepFlavB); }
  float get_qgl() const      { return get_property ((*this), Jet_qgl); }
  int get_id() const         { return get_property ((*this),Jet_jetId); }
  int get_puid() const       { return get_property ((*this), Jet_puId); }
  int get_preselIdx() const  { return preselIdx; }
private:
  void buildP4() override; 

};

#endif

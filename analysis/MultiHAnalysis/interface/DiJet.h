#ifndef DIJET_H
#define DIJET_H

#include "Jet.h"
#include "CompositeCandidate.h"

class DiJet : public CompositeCandidate
{
public:
  DiJet(const Jet& j1,const Jet& j2);

  void set_jIdx(int j1Idx, int j2Idx) { 
    j1Idx_ = j1Idx;
    j2Idx_ = j2Idx;
  };

  int get_signalId() const   { return signalId; }
  float Pt() const           { return this->P4().Pt(); }
  float Eta() const          { return this->P4().Eta(); }
  float Phi() const          { return this->P4().Phi(); }
  float M() const            { return this->P4().M(); }
  float E() const            { return this->P4().E(); }
  float dR() const           { return dr_; }
  int get_j1Idx() const { return j1Idx_; }
  int get_j2Idx() const { return j2Idx_; }

private:
  int signalId = -1;
  float dr_ = -1;
  int j1Idx_ = -1;
  int j2Idx_ = -1;
};

#endif

#ifndef COMPOSITECANDIDATE_H
#define COMPOSITECANDIDATE_H

/*
** class  : CompositeCandidate
** author : L. Cadamuro (UF)
** date   : 23/01/2018
** brief  : an object composed by a pair of Candidates
** note   : the candidate stores the combined P4 and keep reference of its components
**        : this reference is in the form of the two idx of the components, plus the two components themselves
**        : The CompositeCandidate own completely the two components and any copy operation also creates two new components
**        : This should not cause a problem as the == comparison between to Candidates is based on their index
**        : but be careful in case you want to compare the pointers
*/

#include "Math/Vector4D.h"
typedef ROOT::Math::PtEtaPhiMVector p4_t;

#include "Candidate.h"
#include <utility>

class CompositeCandidate : public Candidate
{
public:
  CompositeCandidate() : Candidate(),cand1_(), cand2_() {typeId_=-1; p4_.SetCoordinates(0,0,0,0); isComposite_=true;}
  CompositeCandidate(const Candidate& c1, const Candidate& c2) : Candidate() {typeId_=-1; setComponents(c1,c2); isComposite_=true;}

  ~CompositeCandidate(){};
  CompositeCandidate(const CompositeCandidate& rhs); // copy ctor
  CompositeCandidate& operator = (const CompositeCandidate& rhs);        // assignment
        
  void setComponents(const Candidate& c1, const Candidate& c2);

  Candidate& getComponent1 () const {
    return (*cand1_);
  }
  Candidate& getComponent2 () const {
    return (*cand2_);
  }

  bool sharesComponentWith (const CompositeCandidate& cc) const;
  bool isValid() {return (cand1_ && cand2_);}
  std::unique_ptr<Candidate> clone() const override{
    std::unique_ptr<CompositeCandidate> CompositeCandidateClone(new CompositeCandidate(this->getComponent1(), this->getComponent2()));
    CompositeCandidateClone->setP4(this->P4()); //In case the P4 had been re-evaluated
    CompositeCandidateClone->params = this->params;
    return CompositeCandidateClone;
  }
  void rebuildP4UsingRegressedPt(bool usePtRegressedCandidate1, bool usePtRegressedCandidate2);

  void swapComponents() {
    std::swap(cand1_, cand2_);
  }

protected:
  void buildP4() override {p4_ = cand1_->P4() + cand2_->P4();}; 
  std::unique_ptr<Candidate> cand1_;
  std::unique_ptr<Candidate> cand2_;
};

struct CompositeCandidateCollection : public BranchCollection<CompositeCandidate> {
  float m;           
  float pt;          
  float eta;         
  float phi;         

  DEF_BRANCH_COLLECTION(CompositeCandidateCollection);
  void Register(TString tag, std::unique_ptr<TTree>& tree_, std::map<std::string, bool>& branch_switches_) override {
    branch_switches = branch_switches_;

    CHECK_BRANCH(m);
    CHECK_BRANCH(pt);
    CHECK_BRANCH(eta);
    CHECK_BRANCH(phi);
  }
  void Clear() override {
    m = -999;
    pt = -999;
    eta = -999;
    phi = -999;
  }
  void Fill(const CompositeCandidate& cand) override {
    m = cand.P4().M();
    pt = cand.P4().Pt();
    eta = cand.P4().Eta();
    phi = cand.P4().Phi();
  }
};

#endif

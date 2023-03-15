#ifndef CANDIDATE_H
#define CANDIDATE_H

/*
** class  : Candidate
** author : L. Cadamuro (UF)
** date   : 30/12/2017
** brief  : lightweight class representing a general physics object in nanoAOD.
**          Each object has an index (in its respective parent vector collection) and a p4 built from it
** note   : the macro get_property simulates an introspection by giving access to a user defined object property
**          through an access from the NanoAODTree
**          The #define ensures it is automatically propagated to all codes using Candidate or its derived
*/

#include "Math/Vector4D.h"
typedef ROOT::Math::PtEtaPhiMVector p4_t;

#include "NanoAODTree.h"
#include <memory>
#include <iostream>
#include "TLorentzVector.h"
#include "BranchCollection.h"

#define get_property(OBJ, NAME) (OBJ.isValid() ?  OBJ.getNanoAODTree() -> NAME .At(OBJ.getIdx()) : throw std::runtime_error("get property " #NAME " from invalid object"))

class Candidate
{
public:
  Candidate(){nat_ = nullptr; idx_ = -1; isComposite_=false;} // creates an invalid Candidate
  Candidate(int idx, NanoAODTree* nat){idx_ = idx; nat_ = nat; isComposite_=false; parentIdxVector_.emplace_back(idx);} // standard ctor to be used for NanoAODTree inspection
  ~Candidate(){};
        
  p4_t P4() const      {return p4_;}
  void setP4(p4_t p4) {p4_ = p4;}
  bool getIsComposite() const {return isComposite_;}
        
  int getIdx() const {
    if(isComposite_) throw std::runtime_error("Composite particles do not have id");
    return idx_;
  }

  std::vector<int> getIdxParents() const 
  {
    if(!isComposite_) throw std::runtime_error("Non composite particles do not have parent ids");
    return parentIdxVector_;
  }

  NanoAODTree* getNanoAODTree() const {return nat_;}
        
  bool isValid() const {return idx_ >= 0;}
  virtual std::unique_ptr<Candidate> clone() const = 0;
  int getCandidateTypeId() const {return typeId_;};

  void set_param(std::string key, float value) { params[key] = value; }
  float get_param(std::string key, float value) const
  {
    if (!has_param(key))
      return value;
    // std::cout << "[WARNING] " << key << " not found in Candidate params." << std::endl;
    return params.at(key);
  }
  bool has_param(std::string key) const { return params.find(key) != params.end(); }

protected:
  virtual void buildP4() = 0;
  int idx_;
  std::vector<int> parentIdxVector_;

  p4_t p4_;
  NanoAODTree* nat_;
  bool isComposite_;
  int typeId_; //11 = Electron , 22 = Photon , 13 = Muon, 15 = Tau, 1 = Jet, 6 = FatJet, 2 = MET, -1 = GenParticle, -10 = CompositeCandidate
  std::map<std::string, float> params;
};

struct CandidateCollection : public BranchCollection<Candidate> {
  float m;           
  float pt;          
  float eta;         
  float phi;         

  DEF_BRANCH_COLLECTION(CandidateCollection);
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
  void Fill(const Candidate& cand) override {
    m = cand.P4().M();
    pt = cand.P4().Pt();
    eta = cand.P4().Eta();
    phi = cand.P4().Phi();
  }
};

#endif

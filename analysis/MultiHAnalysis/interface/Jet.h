#ifndef JET_H
#define JET_H

#include "Candidate.h"
#include "BranchCollection.h"

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
    clonedJet->params = this->params;
    return std::unique_ptr<Jet>(clonedJet);
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

  float get_E() const { return this->P4().E(); }
  float get_m() const { return this->P4().M(); }
  float get_mRegressed() const { return this->P4Regressed().M(); }
  float get_pt() const { return this->P4().Pt(); }
  float get_ptRegressed() const { return this->P4Regressed().Pt(); }
  float get_eta() const { return this->P4().Eta(); }
  float get_phi() const { return this->P4().Phi(); }
  int get_partonFlav() const {
    // return 0;
    return get_property((*this), Jet_partonFlavour);
  }
  int get_hadronFlav() const {
    // return 0;
    return get_property((*this), Jet_hadronFlavour);
  }
  int get_signalId() const { return signalId; }
  int get_higgsIdx() const { return higgsIdx; }
  int get_genIdx() const { return genIdx; }
  float get_btag() const { return get_property((*this), Jet_btagDeepFlavB); }
  float get_PNetBvsAll() const { return get_property((*this), Jet_btagPNetBvsAll); }
  float get_qgl() const { return get_property((*this), Jet_qgl); }
  float get_chEmEF() const { return get_property((*this), Jet_chEmEF); }      
  float get_chHEF() const { return get_property((*this), Jet_chHEF); }       
  float get_neEmEF() const { return get_property((*this), Jet_neEmEF); }      
  float get_neHEF() const { return get_property((*this), Jet_neHEF); }       
  int get_nConstituents() const { return get_property((*this), Jet_nConstituents); } 
  int get_id() const { return get_property((*this), Jet_jetId); }
  int get_puid() const { return get_property((*this), Jet_puId); }
  int get_preselIdx() const { return preselIdx; }

private:
  void buildP4() override; 

};

struct JetListCollection : public BranchCollection<std::vector<Jet>> {
  std::vector<float> E;           
  std::vector<float> m;           
  std::vector<float> mRegressed;  
  std::vector<float> pt;          
  std::vector<float> ptRegressed; 
  std::vector<float> eta;         
  std::vector<float> phi;         
  std::vector<int> partonFlav;    
  std::vector<int> hadronFlav;    
  std::vector<int> signalId;      
  std::vector<int> higgsIdx;      
  std::vector<int> genIdx;        
  std::vector<float> btag;        
  std::vector<float> qgl;         
  std::vector<float> chEmEF;      
  std::vector<float> chHEF;       
  std::vector<float> neEmEF;      
  std::vector<float> neHEF;       
  std::vector<int> nConstituents; 
  std::vector<int> id;            
  std::vector<int> puid;

  DEF_BRANCH_COLLECTION(JetListCollection);
  void Register(TString tag, std::unique_ptr<TTree>& tree_, std::map<std::string, bool>& branch_switches_) override;
  void Clear() override;
  void Fill(const std::vector<Jet>& jets) override;
};

struct JetCollection : public BranchCollection<Jet> {
  float E;           
  float m;           
  float mRegressed;  
  float pt;          
  float ptRegressed; 
  float eta;         
  float phi;         
  int partonFlav;    
  int hadronFlav;    
  int signalId;      
  float btag;        
  float qgl;         
  float chEmEF;      
  float chHEF;       
  float neEmEF;      
  float neHEF;       
  int nConstituents; 
  int id;            
  int puid;

  DEF_BRANCH_COLLECTION(JetCollection);
  void Register(TString tag, std::unique_ptr<TTree>& tree_, std::map<std::string, bool>& branch_switches_) override;
  void Clear() override;
  void Fill(const Jet& jet) override;
};

#endif

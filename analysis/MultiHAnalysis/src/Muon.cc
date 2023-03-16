#include "Muon.h"

#include "BuildP4.h"

void Muon::buildP4()
{
  p4_.BUILDP4(Muon, nat_);
}

void MuonListCollection::Register(TString tag, std::unique_ptr<TTree>& tree_, std::map<std::string, bool>& branch_switches_) {
  branch_switches = branch_switches_;
  
  CHECK_BRANCH(E);                           
  CHECK_BRANCH(m);                           
  CHECK_BRANCH(pt);                         
  CHECK_BRANCH(eta);                       
  CHECK_BRANCH(phi);                       
  CHECK_BRANCH(dxy);                       
  CHECK_BRANCH(dz);                        
  CHECK_BRANCH(charge);                 
  CHECK_BRANCH(pfRelIso04_all); 
  CHECK_BRANCH(looseId);               
  CHECK_BRANCH(mediumId);             
  CHECK_BRANCH(tightId);
}

void MuonListCollection::Clear() {
  E.clear();              
  m.clear();	
  pt.clear();             
  eta.clear();            
  phi.clear();            
  dxy.clear();            
  dz.clear();             
  charge.clear();         
  pfRelIso04_all.clear(); 
  looseId.clear();        
  mediumId.clear();       
  tightId.clear();
}

void MuonListCollection::Fill(const std::vector<Muon>& muons) {

  for (const Muon& muon : muons) {
      E.push_back(muon.get_E());                           
      m.push_back(muon.get_m());		            
      pt.push_back(muon.get_pt());	                    
      eta.push_back(muon.get_eta());		            
      phi.push_back(muon.get_phi());			    
      dxy.push_back(muon.get_dxy());			    
      dz.push_back(muon.get_dz());			    
      charge.push_back(muon.get_charge());	            
      pfRelIso04_all.push_back(muon.get_pfRelIso04_all()); 
      looseId.push_back(muon.get_looseId());		    
      mediumId.push_back(muon.get_mediumId());             
      tightId.push_back(muon.get_tightId());               
  }
}

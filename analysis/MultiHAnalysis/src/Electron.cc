#include "Electron.h"

#include "BuildP4.h"

void Electron::buildP4()
{
  p4_.BUILDP4(Electron, nat_);
}
void ElectronListCollection::Register(TString tag, std::unique_ptr<TTree>& tree_, std::map<std::string, bool>& branch_switches_) {
  branch_switches = branch_switches_;
  
  CHECK_BRANCH(E);                           
  CHECK_BRANCH(m);                           
  CHECK_BRANCH(pt);                         
  CHECK_BRANCH(eta);                       
  CHECK_BRANCH(phi);                       
  CHECK_BRANCH(dxy);                       
  CHECK_BRANCH(dz);                        
  CHECK_BRANCH(charge);                 
  CHECK_BRANCH(pfRelIso03_all);           
  CHECK_BRANCH(mvaFall17V2Iso_WPL);   
  CHECK_BRANCH(mvaFall17V2Iso_WP90); 
  CHECK_BRANCH(mvaFall17V2Iso_WP80); 
}

void ElectronListCollection::Clear() {
  E.clear();              
  m.clear();              
  pt.clear();             
  eta.clear();            
  phi.clear();            
  dxy.clear();            
  dz.clear();             
  charge.clear();         
  pfRelIso03_all.clear(); 
  mvaFall17V2Iso_WPL.clear();  
  mvaFall17V2Iso_WP90.clear(); 
  mvaFall17V2Iso_WP80.clear();
}

void ElectronListCollection::Fill(const std::vector<Electron>& electrons) {

  for (const Electron& ele : electrons) {
        E.push_back(ele.get_E());                          
        m.push_back(ele.get_m());			    
        pt.push_back(ele.get_pt());			  
        eta.push_back(ele.get_eta());            
        phi.push_back(ele.get_phi());                      
        dxy.push_back(ele.get_dxy());                      
        dz.push_back(ele.get_dz());                        
        charge.push_back(ele.get_charge());                
        pfRelIso03_all.push_back(ele.get_pfRelIso03_all());           
        mvaFall17V2Iso_WPL.push_back(ele.get_mvaFall17V2Iso_WPL());   
        mvaFall17V2Iso_WP90.push_back(ele.get_mvaFall17V2Iso_WP90()); 
        mvaFall17V2Iso_WP80.push_back(ele.get_mvaFall17V2Iso_WP80()); 
  }
}

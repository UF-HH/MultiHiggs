#include "Jet.h"
#include "GenJet.h"
#include "GenPart.h"
#include <iostream>
#include "BuildP4.h"

void Jet::buildP4(){
  p4_.BUILDP4(Jet, nat_);
}

float Jet::getBregCorr()
{
  //Determine the corr factor
  float corr = get_property((*this),Jet_bRegCorr);
  float res  = get_property((*this),Jet_bRegRes);
  //The condition below needs to check in every NANOAOD release. 
    //It is not implemmented in NANOAODv5. A similar condition for bRegRes is implemented on the OfflineProducerHelper as "Get_bRegRes"
  if (  !( (corr>0.1) && (corr<2) && (res>0.005) && (res<0.9) ) ) {
    corr = 1.;
  }
  else if( get_property((*this),Jet_pt) < 20 ){
    corr = 1.;
  }
  // else //Do nothing, use the NANOAOD correction value

  return corr;
}

float Jet::getBregRes()
{
  //Determine the corr factor
  float corr = get_property((*this),Jet_bRegCorr);
  float res  = get_property((*this),Jet_bRegRes);
  //The condition below needs to check in every NANOAOD release.  It is not implemmented in NANOAODv5.
  if (  !( (corr>0.1) && (corr<2) && (res>0.005) && (res<0.9) ) ) {
    res = 0.2;
  }
  else if( get_property((*this),Jet_pt) < 20 ){
    res = 0.2;
  }
  // else //Do nothing, use the NANOAOD correction value

  return res;
}

void Jet::buildP4Regressed()
{
  if(p4_.Pt()==0.) this->buildP4();
 
  //Apply regression
  float corr = getBregCorr();
  p4Regressed_ = corr * p4_;
}

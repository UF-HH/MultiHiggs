#include "GenPart.h"
#include "BuildP4.h"

#include <iostream>

// all masses in GeV, from PDG 2017
// FIXME: should I use Madgraph/PYTHIA settings ?
const std::map<int, float> GenPart::gen_mass_ = {
    // charged leptons
    {11 , 0.5109989461e-3}, // e
    {13 , 105.6583745e-3},  // mu
    {15 , 1776.86e-3},      // tau
    // neutrinos
    {12 , 0},               // nu_e
    {14 , 0},               // nu_mu
    {16 , 0},               // nu_tau
    // quarks
    {1 , 4.7e-3},           // d
    {2 , 2.2e-3},           // u
    {3 , 1.28},             // s
    {4 , 96.e-3},           // c
    {5 , 4.18},             // b
    // vector bosons
    {21 , 0},               // gluon
    {22 , 0}                // photon
};

void GenPart::buildP4()
{
    // NOTE: some care is required here, because particles with mass < 10 do not have the mass stored
    // so I need to look up a pdgId vector

    auto aPdgId = abs(get_property((*this), GenPart_pdgId));
    auto mass   = get_property((*this), GenPart_pdgId);
    if (mass != 0){
        p4_.BUILDP4(GenPart, nat_);    
    }
    else{
        if (gen_mass_.find(aPdgId) != gen_mass_.end())
            p4_.BUILDP4_MASS(GenPart, nat_, gen_mass_.at(aPdgId));
        else{
            std::cout << " ** GenPart :: buildP4 :: WARNING: no mass info specified for particle of pdgId " << aPdgId << " , using 0" << std::endl;
            p4_.BUILDP4_MASS(GenPart, nat_, 0.0);
        }
    }
}
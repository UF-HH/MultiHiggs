#ifndef EVENTINFO_H
#define EVENTINFO_H

/**
** class  : EventInfo
** author : L. Cadamuro (UF)
** date   : 10/01/2018
** brief  : Struct that contains all the inforrmation elaborated during the skim
**          (e.g., which jets are selected, whic triggers fire etc...)
**          each object is wrapped in a boost::optional class so that it can be autmatically unitialized
**/

#include <boost/optional.hpp>

#include "CompositeCandidate.h"
#include "Jet.h"
// #include "Muon.h"
// #include "Electron.h"
#include "GenPart.h"
#include "GenJet.h"

struct EventInfo{

    boost::optional<unsigned int>           Run;
    boost::optional<unsigned int>           LumiSec;
    boost::optional<unsigned long long int> Event;
    boost::optional<unsigned int>           njet;

    boost::optional<GenPart>  gen_X_fc; // first copy at LHE
    boost::optional<GenPart>  gen_X;
    boost::optional<GenPart>  gen_Y;
    boost::optional<GenPart>  gen_HX;    // H from the X->YH process
    boost::optional<GenPart>  gen_HY1;   // H from the X->YH, Y->HH process
    boost::optional<GenPart>  gen_HY2;   // H from the X->YH, Y->HH process

    boost::optional<GenPart>  gen_HX_b1;
    boost::optional<GenPart>  gen_HX_b2;
    boost::optional<GenPart>  gen_HY1_b1;
    boost::optional<GenPart>  gen_HY1_b2;
    boost::optional<GenPart>  gen_HY2_b1;
    boost::optional<GenPart>  gen_HY2_b2;

    boost::optional<GenJet> gen_HX_b1_genjet; // genjets matched to the 6 b
    boost::optional<GenJet> gen_HX_b2_genjet;
    boost::optional<GenJet> gen_HY1_b1_genjet;
    boost::optional<GenJet> gen_HY1_b2_genjet;
    boost::optional<GenJet> gen_HY2_b1_genjet;
    boost::optional<GenJet> gen_HY2_b2_genjet;

    boost::optional<Jet> gen_HX_b1_recojet; // recojets matched to the 6 b
    boost::optional<Jet> gen_HX_b2_recojet;
    boost::optional<Jet> gen_HY1_b1_recojet;
    boost::optional<Jet> gen_HY1_b2_recojet;
    boost::optional<Jet> gen_HY2_b1_recojet;
    boost::optional<Jet> gen_HY2_b2_recojet;
    boost::optional<int> gen_bs_N_reco_match;
    boost::optional<int> gen_bs_N_reco_match_in_acc; // counts how many different jets are the ones above (== fully resolved event)
    boost::optional<double> gen_bs_match_recojet_minv; // inv mass of the matched jets
    boost::optional<double> gen_bs_match_in_acc_recojet_minv;

    boost::optional<CompositeCandidate> X;
    boost::optional<CompositeCandidate> Y;
    boost::optional<CompositeCandidate> HX;
    boost::optional<CompositeCandidate> HY1;
    boost::optional<CompositeCandidate> HY2;

    boost::optional<Jet> HX_b1;
    boost::optional<Jet> HX_b2;
    boost::optional<Jet> HY1_b1;
    boost::optional<Jet> HY1_b2;
    boost::optional<Jet> HY2_b1;
    boost::optional<Jet> HY2_b2;

    std::vector<float> jet_pt;
    std::vector<float> jet_eta;
    std::vector<float> jet_phi;
    std::vector<float> jet_m;
    std::vector<float> jet_btag;

};

#endif
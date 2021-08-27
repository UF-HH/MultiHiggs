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
#include "Muon.h"
#include "Electron.h"
#include "GenPart.h"
#include "GenJet.h"
#include "DiJet.h"
#include "EventShapeCalculator.h"

struct EventInfo{

  boost::optional<unsigned int>           Run;
  boost::optional<unsigned int>           LumiSec;
  boost::optional<unsigned long long int> Event;

  boost::optional<int>    n_other_pv;
  boost::optional<int>    n_pu;
  boost::optional<double> n_true_int;
  boost::optional<double> rhofastjet_all;
  boost::optional<double> lhe_ht;

  boost::optional<int>    n_total_jet;
  boost::optional<int>    n_jet;
  boost::optional<int>    n_genjet;
  boost::optional<int>    n_higgs;
  boost::optional<int>    n_nn_higgs;

  boost::optional<float>  b_6j_score;
  boost::optional<std::vector<float>> b_2j_scores;
  boost::optional<float>  b_3h_score;

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

  boost::optional< std::vector<GenJet> > genjet_list;
  boost::optional< std::vector<Jet> > jet_list;
  boost::optional< std::vector<DiJet> > higgs_list;
  boost::optional< std::vector<DiJet> > nn_higgs_list;

  boost::optional<EventShapes> event_shapes;

  // for ttbar skims
  boost::optional<Jet> bjet1;
  boost::optional<Jet> bjet2;

  // info on leptons in the event
  boost::optional<Muon> mu_1;
  boost::optional<Muon> mu_2;
  boost::optional<Electron> ele_1;
  boost::optional<Electron> ele_2;
  boost::optional<int> n_mu_loose;
  boost::optional<int> n_ele_loose;
  // boost::optional<int> n_mu_tight;
  // boost::optional<int> n_ele_tight;

  // scale factors
  boost::optional<double> btagSF_WP_M;
};

#endif

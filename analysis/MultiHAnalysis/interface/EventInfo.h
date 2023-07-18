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
#include "FatJet.h"
#include "SubJet.h"
#include "Muon.h"
#include "Electron.h"
#include "GenPart.h"
#include "GenJet.h"
#include "GenJetAK8.h"
#include "SubGenJetAK8.h"
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
  boost::optional<double> PFHT;
  boost::optional<double> lhe_ht;

  boost::optional<int>    n_total_jet;
  boost::optional<int>    n_jet;
  boost::optional<int>    n_genjet;
  boost::optional<int>    n_higgs;
  boost::optional<int>    n_genfatjet;
  boost::optional<int>    n_fatjet;
  boost::optional<int>    n_ele;
  boost::optional<int>    n_muon;
  
  boost::optional<float>  b_6j_score;
  boost::optional<float>  b_3d_score;

  boost::optional<GenPart>  gen_H1_fc;
  boost::optional<GenPart>  gen_H2_fc;
  boost::optional<GenJetAK8> gen_H1_b1_genfatjet;
  boost::optional<GenJetAK8> gen_H1_b2_genfatjet;
  boost::optional<GenJetAK8> gen_H2_b1_genfatjet;
  boost::optional<GenJetAK8> gen_H2_b2_genfatjet;
  boost::optional<FatJet> gen_H1_b1_recofatjet;
  boost::optional<FatJet> gen_H1_b2_recofatjet;
  boost::optional<FatJet> gen_H2_b1_recofatjet;
  boost::optional<FatJet> gen_H2_b2_recofatjet;
  
  boost::optional<GenPart>  gen_X_fc; // first copy at LHE
  boost::optional<GenPart>  gen_X;

  // Start Gen 6B Objects
  boost::optional<GenPart>  gen_Y;
  boost::optional<GenPart>  gen_HX;    // H from the X->YH process
  boost::optional<GenPart>  gen_H1;   // H from the X->YH, Y->HH process
  boost::optional<GenPart>  gen_H2;   // H from the X->YH, Y->HH process

  boost::optional<GenPart>  gen_HX_b1;
  boost::optional<GenPart>  gen_HX_b2;
  boost::optional<GenPart>  gen_H1_b1;
  boost::optional<GenPart>  gen_H1_b2;
  boost::optional<GenPart>  gen_H2_b1;
  boost::optional<GenPart>  gen_H2_b2;

  boost::optional<GenJet> gen_HX_b1_genjet; // genjets matched to the 6 b
  boost::optional<GenJet> gen_HX_b2_genjet;
  boost::optional<GenJet> gen_H1_b1_genjet;
  boost::optional<GenJet> gen_H1_b2_genjet;
  boost::optional<GenJet> gen_H2_b1_genjet;
  boost::optional<GenJet> gen_H2_b2_genjet;

  boost::optional<Jet> gen_HX_b1_recojet; // recojets matched to the 6 b
  boost::optional<Jet> gen_HX_b2_recojet;
  boost::optional<Jet> gen_H1_b1_recojet;
  boost::optional<Jet> gen_H1_b2_recojet;
  boost::optional<Jet> gen_H2_b1_recojet;
  boost::optional<Jet> gen_H2_b2_recojet;
  // End Gen 6B Objects

  boost::optional<int> gen_bs_N_reco_match;
  boost::optional<int> gen_bs_N_reco_match_in_acc; // counts how many different jets are the ones above (== fully resolved event)
  boost::optional<double> gen_bs_match_recojet_minv; // inv mass of the matched jets
  boost::optional<double> gen_bs_match_in_acc_recojet_minv;

  // Start Gen 8B Objects
  boost::optional<GenPart>  gen_Y1;
  boost::optional<GenPart>  gen_Y2;
  boost::optional<GenPart>  gen_H1Y1;    // H from the X->YY, Y->HH process
  boost::optional<GenPart>  gen_H2Y1;    // H from the X->YY, Y->HH process
  boost::optional<GenPart>  gen_H1Y2;    // H from the X->YY, Y->HH process
  boost::optional<GenPart>  gen_H2Y2;    // H from the X->YY, Y->HH process

  boost::optional<GenPart>  gen_H1Y1_b1;
  boost::optional<GenPart>  gen_H1Y1_b2;
  boost::optional<GenPart>  gen_H2Y1_b1;
  boost::optional<GenPart>  gen_H2Y1_b2;
  boost::optional<GenPart>  gen_H1Y2_b1;
  boost::optional<GenPart>  gen_H1Y2_b2;
  boost::optional<GenPart>  gen_H2Y2_b1;
  boost::optional<GenPart>  gen_H2Y2_b2;


  boost::optional<GenJet>  gen_H1Y1_b1_genjet; // genjets matched to the 8 b
  boost::optional<GenJet>  gen_H1Y1_b2_genjet;
  boost::optional<GenJet>  gen_H2Y1_b1_genjet;
  boost::optional<GenJet>  gen_H2Y1_b2_genjet;
  boost::optional<GenJet>  gen_H1Y2_b1_genjet;
  boost::optional<GenJet>  gen_H1Y2_b2_genjet;
  boost::optional<GenJet>  gen_H2Y2_b1_genjet;
  boost::optional<GenJet>  gen_H2Y2_b2_genjet;


  boost::optional<Jet>  gen_H1Y1_b1_recojet; // recojets matched to the 8 b
  boost::optional<Jet>  gen_H1Y1_b2_recojet;
  boost::optional<Jet>  gen_H2Y1_b1_recojet;
  boost::optional<Jet>  gen_H2Y1_b2_recojet;
  boost::optional<Jet>  gen_H1Y2_b1_recojet;
  boost::optional<Jet>  gen_H1Y2_b2_recojet;
  boost::optional<Jet>  gen_H2Y2_b1_recojet;
  boost::optional<Jet>  gen_H2Y2_b2_recojet;
  // End Gen 8B Objects

  // Start Reco 6B Objects
  boost::optional<CompositeCandidate> X;
  boost::optional<CompositeCandidate> Y;
  boost::optional<CompositeCandidate> HX;
  boost::optional<CompositeCandidate> H1;
  boost::optional<CompositeCandidate> H2;

  boost::optional<Jet> HX_b1;
  boost::optional<Jet> HX_b2;
  boost::optional<Jet> H1_b1;
  boost::optional<Jet> H1_b2;
  boost::optional<Jet> H2_b1;
  boost::optional<Jet> H2_b2;

  boost::optional<int> HX_b1_genHflag;
  boost::optional<int> HX_b2_genHflag;
  boost::optional<int> H1_b1_genHflag;
  boost::optional<int> H1_b2_genHflag;
  boost::optional<int> H2_b1_genHflag;
  boost::optional<int> H2_b2_genHflag;
  // End Reco 6B Objects

  // Start Reco 8B Objects
  boost::optional<CompositeCandidate> Y1;
  boost::optional<CompositeCandidate> Y2;
  boost::optional<CompositeCandidate> H1Y1;
  boost::optional<CompositeCandidate> H2Y1;
  boost::optional<CompositeCandidate> H1Y2;
  boost::optional<CompositeCandidate> H2Y2;

  boost::optional<float> H1Y1_score;
  boost::optional<float> H2Y1_score;
  boost::optional<float> H1Y2_score;
  boost::optional<float> H2Y2_score;

  boost::optional<Jet> H1Y1_b1;
  boost::optional<Jet> H1Y1_b2;
  boost::optional<Jet> H2Y1_b1;
  boost::optional<Jet> H2Y1_b2;
  boost::optional<Jet> H1Y2_b1;
  boost::optional<Jet> H1Y2_b2;
  boost::optional<Jet> H2Y2_b1;
  boost::optional<Jet> H2Y2_b2;

  boost::optional<int> H1Y1_b1_genHflag;
  boost::optional<int> H1Y1_b2_genHflag;
  boost::optional<int> H2Y1_b1_genHflag;
  boost::optional<int> H2Y1_b2_genHflag;
  boost::optional<int> H1Y2_b1_genHflag;
  boost::optional<int> H1Y2_b2_genHflag;
  boost::optional<int> H2Y2_b1_genHflag;
  boost::optional<int> H2Y2_b2_genHflag;

  boost::optional<float> H1Y1_b1_score;
  boost::optional<float> H1Y1_b2_score;
  boost::optional<float> H2Y1_b1_score;
  boost::optional<float> H2Y1_b2_score;
  boost::optional<float> H1Y2_b1_score;
  boost::optional<float> H1Y2_b2_score;
  boost::optional<float> H2Y2_b1_score;
  boost::optional<float> H2Y2_b2_score;

  boost::optional<int> n_loose_btag;
  boost::optional<int> n_medium_btag;
  boost::optional<int> n_tight_btag;
  boost::optional<float> btagavg;
  
  boost::optional<float> quadh_score;
  
  // End Reco 8B Objects
  boost::optional< std::vector<Electron> > ele_list;
  boost::optional< std::vector<Muon> > muon_list;
  boost::optional< std::vector<GenPart> > genpb_list;
  boost::optional< std::vector<GenJet> > genjet_list;
  boost::optional< std::vector<Jet> > jet_list;
  boost::optional< std::vector<GenJetAK8> > genfatjet_list;
  boost::optional< std::vector<FatJet> > fatjet_list;
  boost::optional<std::vector<DiJet>> dijet_list;

  boost::optional<EventShapes> event_shapes;

  boost::optional<int> nfound_all;
  boost::optional<int> nfound_all_h;
  boost::optional<int> nfound_presel;
  boost::optional<int> nfound_presel_h;
  boost::optional<int> nfound_select;
  boost::optional<int> nfound_select_h;
  boost::optional<int> nfound_paired_h;
  boost::optional<int> nfound_select_y;
  boost::optional<int> nfound_paired_y;

  // for ttbar skims
  boost::optional<GenPart> gen_t1;
  boost::optional<GenPart> gen_t1_b;
  boost::optional<GenPart> gen_t1_w;
  boost::optional<GenPart> gen_t1_w_j1;
  boost::optional<GenPart> gen_t1_w_j2;


  boost::optional<GenPart> gen_t2;
  boost::optional<GenPart> gen_t2_b;
  boost::optional<GenPart> gen_t2_w;
  boost::optional<GenPart> gen_t2_w_j1;
  boost::optional<GenPart> gen_t2_w_j2;

  boost::optional<GenJet> gen_t1_b_genjet;
  boost::optional<GenJet> gen_t1_w_j1_genjet;
  boost::optional<GenJet> gen_t1_w_j2_genjet;

  boost::optional<GenJet> gen_t2_b_genjet;
  boost::optional<GenJet> gen_t2_w_j1_genjet;
  boost::optional<GenJet> gen_t2_w_j2_genjet;

  boost::optional<Jet> gen_t1_b_recojet;
  boost::optional<Jet> gen_t1_w_j1_recojet;
  boost::optional<Jet> gen_t1_w_j2_recojet;

  boost::optional<Jet> gen_t2_b_recojet;
  boost::optional<Jet> gen_t2_w_j1_recojet;
  boost::optional<Jet> gen_t2_w_j2_recojet;

  boost::optional<Jet> bjet1;
  boost::optional<Jet> bjet2;

  // scale factors
  boost::optional<double> btagSF_WP_M;
};

#endif

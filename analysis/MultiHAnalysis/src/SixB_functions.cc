#include "SixB_functions.h"
#include "Math/VectorUtil.h"
#include "Math/Vector3D.h"
#include "Math/Functions.h"

#include "BuildClassifierInput.h"

// #include "DebugUtils.h"

#include <iostream>
#include <tuple>
#include <algorithm>

#include "Electron.h"
#include "Muon.h"

using namespace std;

void SixB_functions::initialize_params_from_cfg(CfgParser& config)
{
  // preselections
  pmap.insert_param<bool>("presel", "apply", config.readBoolOpt("presel::apply"));
  pmap.insert_param<std::vector<double> >("presel", "pt_min", config.readDoubleListOpt("presel::pt_min"));
  pmap.insert_param<double>("presel", "eta_max", config.readDoubleOpt("presel::eta_max"));
  pmap.insert_param<int>   ("presel", "pf_id",   config.readIntOpt("presel::pf_id"));
  pmap.insert_param<int>   ("presel", "pu_id",   config.readIntOpt("presel::pu_id"));

  // six jet choice
  pmap.insert_param<string>("configurations", "sixbJetChoice", config.readStringOpt("configurations::sixbJetChoice"));

  // HHH pairing
  pmap.insert_param<string>("configurations", "jetPairsChoice", config.readStringOpt("configurations::jetPairsChoice"));

  // HHH pairing
  pmap.insert_param<string>("configurations", "XYHChoice", config.readStringOpt("configurations::XYHChoice"));

  // H done with regressed pT
  pmap.insert_param<bool>("configurations", "useRegressedPtForHp4", config.readBoolOpt("configurations::useRegressedPtForHp4"));

  // parse specific parameters for various functions
  if (pmap.get_param<string> ("configurations", "sixbJetChoice") == "bias_pt_sort" || pmap.get_param<string> ("configurations", "sixbJetChoice") == "btag_sortedpt_cuts")
    {
      pmap.insert_param<bool>          ("bias_pt_sort", "applyJetCuts", config.readBoolOpt("bias_pt_sort::applyJetCuts"));
      pmap.insert_param<vector<int> >   ("bias_pt_sort", "btagWP_cuts",  config.readIntListOpt("bias_pt_sort::btagWP_cuts"));
      pmap.insert_param<std::vector<double >>("bias_pt_sort", "pt_cuts", config.readDoubleListOpt("bias_pt_sort::pt_cuts"));
      pmap.insert_param<double>("bias_pt_sort", "htCut", config.readDoubleOpt("bias_pt_sort::htCut"));
    }

  if (pmap.get_param<string> ("configurations", "sixbJetChoice") == "6jet_DNN") {
      pmap.insert_param<string> ("6jet_DNN", "model_path", config.readStringOpt("6jet_DNN::model_path"));
  }

  if (pmap.get_param<string> ("configurations", "jetPairsChoice") == "2jet_DNN") {
      pmap.insert_param<string> ("2jet_DNN", "model_path", config.readStringOpt("2jet_DNN::model_path"));
  }

  if (pmap.get_param<string>("configurations", "XYHChoice") == "leadJetInX") {
    pmap.insert_param<bool> ("leadJetInX", "useRegressedPt", config.readBoolOpt("leadJetInX::useRegressedPt"));
  }
}

void SixB_functions::initialize_functions(TFile& outputFile)
{
  if (pmap.get_param<string> ("configurations", "sixbJetChoice") == "6jet_DNN") {
    cout << "[INFO] ... Loading 6 Jet Classifier: " << pmap.get_param<string>("6jet_DNN", "model_path") << endl;
    n_6j_classifier_ = std::unique_ptr<EvalNN> (new EvalNN("n_6j_classifier", pmap.get_param<string>("6jet_DNN", "model_path")));
    n_6j_classifier_->write(outputFile);
  }

  if (pmap.get_param<string> ("configurations", "jetPairsChoice") == "2jet_DNN") {
    cout << "[INFO] ... Loading 2 Jet Classifier: " << pmap.get_param<string>("2jet_DNN", "model_path") << endl;
    n_2j_classifier_ = std::unique_ptr<EvalNN> (new EvalNN("n_2j_classifier", pmap.get_param<string>("2jet_DNN", "model_path")));
    n_2j_classifier_->write(outputFile);
  }

}

void SixB_functions::select_gen_particles(NanoAODTree& nat, EventInfo& ei)
{
  for (uint igp = 0; igp < *(nat.nGenPart); ++igp)
    {
      GenPart gp (igp, &nat);
      int apdgid = abs(get_property(gp, GenPart_pdgId));
        
      // X
      if (apdgid == 45) {
	if (gp.isFirstCopy())
	  ei.gen_X_fc = gp;
	else if (gp.isLastCopy())
	  ei.gen_X = gp;
      }

      // Y
      if (apdgid == 35 && gp.isLastCopy())
	ei.gen_Y = gp;

      // H
      if (apdgid == 25 && gp.isLastCopy()) {
	GenPart mother (get_property(gp, GenPart_genPartIdxMother), &nat);
	int amothpdgid = abs(get_property(mother, GenPart_pdgId));
	if (amothpdgid == 45)
	  ei.gen_HX = gp;
	else if (amothpdgid == 35)
	  assign_to_uninit(gp, {&ei.gen_H1, &ei.gen_H2} );
      }

      // b
      if (apdgid == 5 && gp.isFirstCopy()) {
	int moth_idx = get_property(gp, GenPart_genPartIdxMother);
	if (moth_idx >= 0) {
	  GenPart mother (moth_idx, &nat);
	  int amothpdgid = abs(get_property(mother, GenPart_pdgId));
	  // in the LHE the mother always comes before the daughters, so it is guaranteed to have been found already
	  if (amothpdgid == 25){
	    if (ei.gen_HX && moth_idx == ei.gen_HX->getIdx())
	      assign_to_uninit(gp, {&ei.gen_HX_b1, &ei.gen_HX_b2} );
	    if (ei.gen_H1 && moth_idx == ei.gen_H1->getIdx())
	      assign_to_uninit(gp, {&ei.gen_H1_b1, &ei.gen_H1_b2} );
	    if (ei.gen_H2 && moth_idx == ei.gen_H2->getIdx())
	      assign_to_uninit(gp, {&ei.gen_H2_b1, &ei.gen_H2_b2} );
	  }
	}
      }
    }

  // reorder objects according to pt
  if (ei.gen_H1->P4().Pt() < ei.gen_H2->P4().Pt()){
    std::swap(ei.gen_H1,    ei.gen_H2);
    std::swap(ei.gen_H1_b1, ei.gen_H2_b1);
    std::swap(ei.gen_H1_b2, ei.gen_H2_b2);
  }

  if (ei.gen_HX_b1->P4().Pt() < ei.gen_HX_b2->P4().Pt())
    std::swap(ei.gen_HX_b1, ei.gen_HX_b2);
  if (ei.gen_H1_b1->P4().Pt() < ei.gen_H1_b2->P4().Pt())
    std::swap(ei.gen_H1_b1, ei.gen_H1_b2);
  if (ei.gen_H2_b1->P4().Pt() < ei.gen_H2_b2->P4().Pt())
    std::swap(ei.gen_H2_b1, ei.gen_H2_b2);

  return;
}
// match the selected gen b to gen jets
void SixB_functions::match_genbs_to_genjets(NanoAODTree& nat, EventInfo& ei, bool ensure_unique)
{
  const double dR_match = 0.4;

  std::vector<GenPart*> bs_to_match = {
    ei.gen_HX_b1.get_ptr(),
    ei.gen_HX_b2.get_ptr(),
    ei.gen_H1_b1.get_ptr(),
    ei.gen_H1_b2.get_ptr(),
    ei.gen_H2_b1.get_ptr(),
    ei.gen_H2_b2.get_ptr()
  };

  // For debugging
  if (0)
    {
      std::cout << "HX_b1 index:  "<<ei.gen_HX_b1.get_ptr()->getIdx()<<std::endl;
      std::cout << "HX_b2 index:  "<<ei.gen_HX_b2.get_ptr()->getIdx()<<std::endl;
      std::cout << "H1_b1 index: "<<ei.gen_H1_b1.get_ptr()->getIdx()<<std::endl;
      std::cout << "H1_b2 index: "<<ei.gen_H1_b2.get_ptr()->getIdx()<<std::endl;
      std::cout << "H2_b1 index: "<<ei.gen_H2_b1.get_ptr()->getIdx()<<std::endl;
      std::cout << "H2_b2 index: "<<ei.gen_H2_b2.get_ptr()->getIdx()<<std::endl;
    }

  std::vector<GenJet> genjets;
  for (unsigned int igj = 0; igj < *(nat.nGenJet); ++igj)
    {
      GenJet gj (igj, &nat);
      genjets.push_back(gj);
    }

  std::vector<GenPart*> matched_quarks;
  std::vector<GenJet> matched_genjets;
  GetMatchedPairs(dR_match, bs_to_match, genjets, matched_quarks, matched_genjets);

  for (unsigned int im=0; im<matched_quarks.size(); im++)
    {
      GenPart* b = matched_quarks.at(im);
      GenJet   j = matched_genjets.at(im);

      int bIdx = b->getIdx();
      if (bIdx == ei.gen_HX_b1.get_ptr()->getIdx())
        {
          ei.gen_HX_b1_genjet = GenJet(j.getIdx(), &nat);
          if (0) std::cout << "HX_b1 ("<<ei.gen_HX_b1.get_ptr()->getIdx()<<") matched with genjet ="<<j.getIdx()<<std::endl;
        }
      else if (bIdx == ei.gen_HX_b2.get_ptr()->getIdx())
        {
          ei.gen_HX_b2_genjet = GenJet(j.getIdx(), &nat);
          if (0) std::cout << "HX_b2 ("<<ei.gen_HX_b2.get_ptr()->getIdx()<<") matched with genjet ="<<j.getIdx()<<std::endl;
        }
      else if (bIdx == ei.gen_H1_b1.get_ptr()->getIdx())
        {
          ei.gen_H1_b1_genjet = GenJet(j.getIdx(), &nat);
          if (0) std::cout << "H1_b1 ("<<ei.gen_H1_b1.get_ptr()->getIdx()<<") matched with genjet ="<<j.getIdx()<<std::endl;
        }
      else if (bIdx == ei.gen_H1_b2.get_ptr()->getIdx())
        {
          ei.gen_H1_b2_genjet = GenJet(j.getIdx(), &nat);
          if (0) std::cout << "H1_b2 ("<<ei.gen_H1_b2.get_ptr()->getIdx()<<") matched with genjet ="<<j.getIdx()<<std::endl;
        }
      else if (bIdx == ei.gen_H2_b1.get_ptr()->getIdx())
        {
          ei.gen_H2_b1_genjet = GenJet(j.getIdx(), &nat);
          if (0) std::cout << "H2_b1 ("<<ei.gen_H2_b1.get_ptr()->getIdx()<<") matched with genjet ="<<j.getIdx()<<std::endl;
        }
      else if (bIdx == ei.gen_H2_b2.get_ptr()->getIdx())
        {
          ei.gen_H2_b2_genjet = GenJet(j.getIdx(), &nat);
          if (0) std::cout << "H2_b2 ("<<ei.gen_H2_b2.get_ptr()->getIdx()<<") matched with genjet ="<<j.getIdx()<<std::endl;
        }
    }
  return;
}

void SixB_functions::match_genbs_genjets_to_reco(NanoAODTree& nat, EventInfo& ei)
{
  int ij_gen_HX_b1_genjet  = (ei.gen_HX_b1_genjet  ? find_jet_from_genjet(nat, *ei.gen_HX_b1_genjet)  : -1); 
  int ij_gen_HX_b2_genjet  = (ei.gen_HX_b2_genjet  ? find_jet_from_genjet(nat, *ei.gen_HX_b2_genjet)  : -1); 
  int ij_gen_H1_b1_genjet = (ei.gen_H1_b1_genjet ? find_jet_from_genjet(nat, *ei.gen_H1_b1_genjet) : -1); 
  int ij_gen_H1_b2_genjet = (ei.gen_H1_b2_genjet ? find_jet_from_genjet(nat, *ei.gen_H1_b2_genjet) : -1); 
  int ij_gen_H2_b1_genjet = (ei.gen_H2_b1_genjet ? find_jet_from_genjet(nat, *ei.gen_H2_b1_genjet) : -1); 
  int ij_gen_H2_b2_genjet = (ei.gen_H2_b2_genjet ? find_jet_from_genjet(nat, *ei.gen_H2_b2_genjet) : -1); 

  if (ij_gen_HX_b1_genjet >= 0)  ei.gen_HX_b1_recojet  = Jet(ij_gen_HX_b1_genjet,  &nat);
  if (ij_gen_HX_b2_genjet >= 0)  ei.gen_HX_b2_recojet  = Jet(ij_gen_HX_b2_genjet,  &nat);
  if (ij_gen_H1_b1_genjet >= 0) ei.gen_H1_b1_recojet = Jet(ij_gen_H1_b1_genjet, &nat);
  if (ij_gen_H1_b2_genjet >= 0) ei.gen_H1_b2_recojet = Jet(ij_gen_H1_b2_genjet, &nat);
  if (ij_gen_H2_b1_genjet >= 0) ei.gen_H2_b1_recojet = Jet(ij_gen_H2_b1_genjet, &nat);
  if (ij_gen_H2_b2_genjet >= 0) ei.gen_H2_b2_recojet = Jet(ij_gen_H2_b2_genjet, &nat);

  // select unique occurences in vector
  // note : PAT tools already ensure that match is unique
  // https://github.com/cms-sw/cmssw/blob/master/PhysicsTools/PatAlgos/python/mcMatchLayer0/jetMatch_cfi.py
  // so the check below is redundant

  // std::vector<int> imatchs;
  // if (ij_gen_HX_b1_genjet >= 0)  imatchs.push_back(ij_gen_HX_b1_genjet);
  // if (ij_gen_HX_b2_genjet >= 0)  imatchs.push_back(ij_gen_HX_b2_genjet);
  // if (ij_gen_H1_b1_genjet >= 0) imatchs.push_back(ij_gen_H1_b1_genjet);
  // if (ij_gen_H1_b2_genjet >= 0) imatchs.push_back(ij_gen_H1_b2_genjet);
  // if (ij_gen_H2_b1_genjet >= 0) imatchs.push_back(ij_gen_H2_b1_genjet);
  // if (ij_gen_H2_b2_genjet >= 0) imatchs.push_back(ij_gen_H2_b2_genjet);

  // sort(imatchs.begin(), imatchs.end());
  // imatchs.erase(unique (imatchs.begin(), imatchs.end()), imatchs.end());
  // ei.gen_bs_N_reco_match = imatchs.size(); // number of different reco jets that are matched to gen jets

  int nmatched = 0;
  if (ij_gen_HX_b1_genjet >= 0)  nmatched += 1;
  if (ij_gen_HX_b2_genjet >= 0)  nmatched += 1;
  if (ij_gen_H1_b1_genjet >= 0) nmatched += 1;
  if (ij_gen_H1_b2_genjet >= 0) nmatched += 1;
  if (ij_gen_H2_b1_genjet >= 0) nmatched += 1;
  if (ij_gen_H2_b2_genjet >= 0) nmatched += 1;
  ei.gen_bs_N_reco_match = nmatched;

  // same as above, but apply acceptance cuts on the matched jets
  int nmatched_acc = 0;
  if (ei.gen_HX_b1_recojet && ei.gen_HX_b1_recojet->P4().Pt() > 20 && std::abs(ei.gen_HX_b1_recojet->P4().Eta()) < 4.8) nmatched_acc += 1;
  if (ei.gen_HX_b2_recojet && ei.gen_HX_b2_recojet->P4().Pt() > 20 && std::abs(ei.gen_HX_b2_recojet->P4().Eta()) < 4.8) nmatched_acc += 1;
  if (ei.gen_H1_b1_recojet && ei.gen_H1_b1_recojet->P4().Pt() > 20 && std::abs(ei.gen_H1_b1_recojet->P4().Eta()) < 4.8) nmatched_acc += 1;
  if (ei.gen_H1_b2_recojet && ei.gen_H1_b2_recojet->P4().Pt() > 20 && std::abs(ei.gen_H1_b2_recojet->P4().Eta()) < 4.8) nmatched_acc += 1;
  if (ei.gen_H2_b1_recojet && ei.gen_H2_b1_recojet->P4().Pt() > 20 && std::abs(ei.gen_H2_b1_recojet->P4().Eta()) < 4.8) nmatched_acc += 1;
  if (ei.gen_H2_b2_recojet && ei.gen_H2_b2_recojet->P4().Pt() > 20 && std::abs(ei.gen_H2_b2_recojet->P4().Eta()) < 4.8) nmatched_acc += 1;
  ei.gen_bs_N_reco_match_in_acc = nmatched_acc;

  // now compute p4 sums to make the invariant mass of X - FIXME: can add more inv masses for the various cases
  p4_t p4_sum_matched (0,0,0,0);
  if (ei.gen_HX_b1_recojet) p4_sum_matched += ei.gen_HX_b1_recojet->P4();
  if (ei.gen_HX_b2_recojet) p4_sum_matched += ei.gen_HX_b2_recojet->P4();
  if (ei.gen_H1_b1_recojet) p4_sum_matched += ei.gen_H1_b1_recojet->P4();
  if (ei.gen_H1_b2_recojet) p4_sum_matched += ei.gen_H1_b2_recojet->P4();
  if (ei.gen_H2_b1_recojet) p4_sum_matched += ei.gen_H2_b1_recojet->P4();
  if (ei.gen_H2_b2_recojet) p4_sum_matched += ei.gen_H2_b2_recojet->P4();
  ei.gen_bs_match_recojet_minv = p4_sum_matched.M();

  p4_t p4_sum_matched_acc (0,0,0,0);
  if (ei.gen_HX_b1_recojet && ei.gen_HX_b1_recojet->P4().Pt() > 20 && std::abs(ei.gen_HX_b1_recojet->P4().Eta())  < 4.8) p4_sum_matched_acc += ei.gen_HX_b1_recojet->P4();
  if (ei.gen_HX_b2_recojet && ei.gen_HX_b2_recojet->P4().Pt() > 20 && std::abs(ei.gen_HX_b2_recojet->P4().Eta())  < 4.8) p4_sum_matched_acc += ei.gen_HX_b2_recojet->P4();
  if (ei.gen_H1_b1_recojet && ei.gen_H1_b1_recojet->P4().Pt() > 20 && std::abs(ei.gen_H1_b1_recojet->P4().Eta()) < 4.8) p4_sum_matched_acc += ei.gen_H1_b1_recojet->P4();
  if (ei.gen_H1_b2_recojet && ei.gen_H1_b2_recojet->P4().Pt() > 20 && std::abs(ei.gen_H1_b2_recojet->P4().Eta()) < 4.8) p4_sum_matched_acc += ei.gen_H1_b2_recojet->P4();
  if (ei.gen_H2_b1_recojet && ei.gen_H2_b1_recojet->P4().Pt() > 20 && std::abs(ei.gen_H2_b1_recojet->P4().Eta()) < 4.8) p4_sum_matched_acc += ei.gen_H2_b1_recojet->P4();
  if (ei.gen_H2_b2_recojet && ei.gen_H2_b2_recojet->P4().Pt() > 20 && std::abs(ei.gen_H2_b2_recojet->P4().Eta()) < 4.8) p4_sum_matched_acc += ei.gen_H2_b2_recojet->P4();
  ei.gen_bs_match_in_acc_recojet_minv = p4_sum_matched_acc.M();
}

int SixB_functions::get_jet_genmatch_flag (NanoAODTree& nat, EventInfo& ei, const Jet& jet)
{
    int ijet = jet.getIdx();
    if ( (ei.gen_HX_b1_recojet && ijet == ei.gen_HX_b1_recojet->getIdx())   || (ei.gen_HX_b2_recojet && ijet == ei.gen_HX_b2_recojet->getIdx()) )
        return 0; 
    if ( (ei.gen_H1_b1_recojet && ijet == ei.gen_H1_b1_recojet->getIdx()) || (ei.gen_H1_b2_recojet && ijet == ei.gen_H1_b2_recojet->getIdx()) )
        return 1; 
    if ( (ei.gen_H2_b1_recojet && ijet == ei.gen_H2_b1_recojet->getIdx()) || (ei.gen_H2_b2_recojet && ijet == ei.gen_H2_b2_recojet->getIdx()) )
        return 2; 
    return -1;
}

void SixB_functions::compute_seljets_genmatch_flags(NanoAODTree& nat, EventInfo& ei)
{
    // flags per jet
    ei.HX_b1_genHflag = get_jet_genmatch_flag(nat, ei, *ei.HX_b1);
    ei.HX_b2_genHflag = get_jet_genmatch_flag(nat, ei, *ei.HX_b2);
    ei.H1_b1_genHflag = get_jet_genmatch_flag(nat, ei, *ei.H1_b1);
    ei.H1_b2_genHflag = get_jet_genmatch_flag(nat, ei, *ei.H1_b2);
    ei.H2_b1_genHflag = get_jet_genmatch_flag(nat, ei, *ei.H2_b1);
    ei.H2_b2_genHflag = get_jet_genmatch_flag(nat, ei, *ei.H2_b2);

    // flags per event
    int nfound_paired_h = 0;

    if (ei.HX_b1_genHflag > -1 && ei.HX_b1_genHflag == ei.HX_b2_genHflag)  nfound_paired_h += 1;
    if (ei.H1_b1_genHflag > -1 && ei.H1_b1_genHflag == ei.H1_b2_genHflag) nfound_paired_h += 1;
    if (ei.H2_b1_genHflag > -1 && ei.H2_b1_genHflag == ei.H2_b2_genHflag) nfound_paired_h += 1;
    ei.nfound_paired_h = nfound_paired_h; // number of selected jets that are from H
}


std::vector<Jet> SixB_functions::select_jets(NanoAODTree& nat, EventInfo& ei, const std::vector<Jet>& in_jets)
{
  std::string sel_type = pmap.get_param<std::string>("configurations", "sixbJetChoice");
  
  // if (sel_type == "btag_order")
  //   return select_sixb_jets_btag_order(nat, ei, in_jets);
  
  if (sel_type == "bias_pt_sort")
    return select_sixb_jets_bias_pt_sort(nat, ei, in_jets);
  
  else if (sel_type == "btag_sortedpt_cuts")
    return selectJetsForPairing(nat, ei, in_jets);
  
  else if (sel_type == "pt_sort")
    return select_sixb_jets_pt_sort(nat, ei, in_jets);
  
  else if (sel_type == "6jet_DNN")
    return select_sixb_jets_6jet_DNN(nat, ei, in_jets);

  else if (sel_type == "maxbtag")
    return select_sixb_jets_maxbtag(nat, ei, in_jets);

  else if (sel_type == "5btag_maxpt")
      return select_sixb_jets_maxbtag_highpT(nat, ei, in_jets, 5);

  else if (sel_type == "4btag_maxpt")
    return select_sixb_jets_maxbtag_highpT(nat, ei, in_jets, 4);

  else
    throw std::runtime_error(std::string("SixB_functions::select_sixb_jets : sixbJetChoice ") + sel_type + std::string("not understood"));
}

std::vector<Jet> SixB_functions::select_sixb_jets_bias_pt_sort(NanoAODTree &nat, EventInfo& ei, const std::vector<Jet> &in_jets)
{
  /*
    input jet collection is in_jets : sorted in pT (only) jets
    
    This function sorts the input jet collection, first by the b-tagging score in descending order, and groups the jets into:
    Tight, Medium, Loose and Fail categories. Within these four categories, the jets are sorted again by their pT in descending order.
  */
  
  if (0) // For debugging
    {
      std::cout << "SixB_functions::select_sixb_jets_bias_pt_sort:   input jet collection (should be ordered in pT only):" << std::endl;
      for (unsigned int ij=0; ij<in_jets.size(); ij++)
      {
        std::cout << " jet "<<ij<<"   pT="<<in_jets.at(ij).get_pt()<<"   b-disc.="<<in_jets.at(ij).get_btag()<<std::endl;
      }
    }
  
  // Sort jets by their b-tagging score in descending order
  std::vector<Jet> jets = bias_pt_sort_jets(nat, ei, in_jets);
  
  if (0) // For debugging
    {
      std::cout << "SixB_functions::select_sixb_jets_bias_pt_sort:  jet collection after sorting by b-tagging score and then pT within each group:"<<std::endl;
      for (unsigned int ij=0; ij<jets.size(); ij++)
	{
	  std::cout << " jet "<<ij<<"   pT="<<jets.at(ij).get_pt()<<"   b-disc.="<<jets.at(ij).get_btag()<<std::endl;
	}
    }
  
  // Select the first 6 jets for the pairing
  unsigned int n_out = std::min<int>(jets.size(), 6);
  jets.resize(n_out);
  
  bool apply_cuts = pmap.get_param<bool>("bias_pt_sort", "applyJetCuts");
  if (apply_cuts)
    {
      bool pass_cuts = true;
      
      std::vector<double> pt_cuts     = pmap.get_param<std::vector<double>>("bias_pt_sort", "pt_cuts");
      std::vector<int>    btagWP_cuts = pmap.get_param<std::vector<int>>("bias_pt_sort", "btagWP_cuts");
      
      unsigned int ncuts = pt_cuts.size();
      if (jets.size() < ncuts)
      {
        pass_cuts = false;
      }
      else
      {
        for (unsigned int icut = 0; icut < ncuts; icut++)
          {
            const Jet& ijet = jets[icut];
            double pt   = pt_cuts[icut];
            int btag_wp = btagWP_cuts[icut];
            if ( ijet.get_pt() <= pt || ijet.get_btag() <= btag_WPs[btag_wp] )
        {
          // if (debug_){
          //   cout << "==> the jet nr " << icut << " fails cuts, jet dumped below" << endl;
          //   cout << getObjDescr(ijet) << endl;
          // }
          pass_cuts = false;
          break;
        }
          }
      }
      if (!pass_cuts)
	jets.resize(0); // empty this vector if cuts were not passed
    }
  
  if (0) // For debugging
    {
      std::cout << "SixB_functions: final collection of jets"<<std::endl;
      for (unsigned int ij=0; ij<jets.size(); ij++)
	{
	  std::cout << " jet "<<ij<<"   pT="<<jets.at(ij).get_pt()<<"   b-disc.="<<jets.at(ij).get_btag()<<std::endl;
	}
    }
  return jets;  
}

std::vector<Jet> SixB_functions::selectJetsForPairing(NanoAODTree &nat, EventInfo& ei, const std::vector<Jet> &in_jets)
{
  /*
    input jet collection is in_jets : sorted in pT (only) jets
    
    This function sorts the input jet collection, first by the b-tagging score in descending order, and groups the jets into:
    Tight, Medium, Loose and Fail categories. Within these four categories, the jets are sorted again by their pT in descending order.
  */
  if (0) // For debugging
    {
      std::cout << "SixB_functions::selectJetsForPairing:   input jet collection (should be ordered in pT only):"<<std::endl;
      for (unsigned int ij=0; ij<in_jets.size(); ij++)
	{
	  std::cout << " jet "<<ij<<"   pT="<<in_jets.at(ij).get_pt()<<"   b-disc.="<<in_jets.at(ij).get_btag()<<std::endl;
	}
    }
  
  if (0) std::cout << "Sort jets by their b-tagging score in descending order"<<std::endl;
  // Sort jets by their b-tagging score in descending order
  std::vector<Jet> jets = bias_pt_sort_jets(nat, ei, in_jets);
  
  if (0) // For debugging
    {
      std::cout << "SixB_functions::selectJetsForPairing:  jet collection after sorting by b-tagging score and then pT within each group:"<<std::endl;
      for (unsigned int ij=0; ij<jets.size(); ij++)
        {
          std::cout << " jet "<<ij<<"   pT="<<jets.at(ij).get_pt()<<"   b-disc.="<<jets.at(ij).get_btag()<<std::endl;
        }
    }
  
  // Select the first 6 jets for the pairing
  if (0) std::cout << "Select the first 6 jets for the pairing"<<std::endl;
  unsigned int n_out = std::min<int>(jets.size(), 6);
  jets.resize(n_out);
  
  bool apply_cuts = pmap.get_param<bool>("bias_pt_sort", "applyJetCuts");
  if (apply_cuts)
    {
      bool pass_cuts = true;
      
      if (0) std::cout << "Apply b-tagging cuts on the selected jets"<<std::endl;
      std::vector<int> btagWP_cuts = pmap.get_param<std::vector<int>>("bias_pt_sort", "btagWP_cuts");
      if (btagWP_cuts.size() > n_out)
	{
	  throw std::runtime_error("Number of cuts required larger than the jet collection size! Fix me.");
	}

    double ht_cut = pmap.get_param<double>("bias_pt_sort", "htCut");
    if (ei.PFHT < ht_cut) {
      pass_cuts = false;
    }
      
      for (unsigned int icut=0; icut<btagWP_cuts.size(); icut++)
	{
	  const Jet& j = jets.at(icut);
	  int btag_wp  = btagWP_cuts.at(icut);
	  if (j.get_btag() <= btag_WPs[btag_wp])
	    {
	      pass_cuts = false; 
	      break;
	    }
	}
      
      if (0) std::cout << "Apply pT cuts on the selected jets"<<std::endl;
      const std::vector<double> pt_cuts = pmap.get_param<std::vector<double> >("bias_pt_sort", "pt_cuts");
      if (pt_cuts.size() > n_out)
	{
	  throw std::runtime_error("Number of pT cuts required larger thatn the jet collection size! Fix me.");
	}
      
      unsigned int ptCut_index = 0;
      // Jets need to be sorted by pT in descending order before applying different pT cuts
      std::vector<Jet> jets_sortedInPt = pt_sort_jets(nat, ei, jets);
      for (unsigned int ij=0; ij<jets_sortedInPt.size(); ++ij)
	{
	  const Jet &jet = jets_sortedInPt.at(ij);
	  
	  if (0) std::cout << " jet "<<ij<<"  pt="<<jet.P4().Pt()<<"   pt cut ="<<pt_cuts.at(ptCut_index)<<std::endl;
	  
	  if (jet.P4().Pt() <= pt_cuts.at(ptCut_index))
	    {
	      pass_cuts = false;
	      break;
	    }
	  if (ptCut_index < pt_cuts.size()-1) ptCut_index++;
	}
      
      if (!pass_cuts)
	{
	  jets.resize(0);
	}
    }
  // std::sort(jets.begin(),jets.end(),[](Jet& j1,Jet& j2){ return j1.get_btag()>j2.get_btag(); });
  stable_sort(jets.begin(), jets.end(), [](const Jet& a, const Jet& b) -> bool {
          return ( get_property (a, Jet_btagDeepFlavB) > get_property (b, Jet_btagDeepFlavB) ); }
  ); // sort jet by deepjet score (highest to lowest)
  return jets;
}

std::vector<Jet> SixB_functions::select_sixb_jets_pt_sort(NanoAODTree &nat, EventInfo& ei, const std::vector<Jet> &in_jets)
{
  std::vector<Jet> jets = in_jets;
  std::sort(jets.begin(),jets.end(),[](Jet& j1,Jet& j2){ return j1.get_pt()>j2.get_pt(); });

  int n_out = std::min<int>(jets.size(), 6);
  jets.resize(n_out); // take top 6

  return jets;  
}

std::vector<Jet> SixB_functions::select_sixb_jets_6jet_DNN (NanoAODTree &nat, EventInfo& ei, const std::vector<Jet> &in_jets)
{
    // std::vector<Jet> jets = in_jets;
    // FIXME: make sorting configurable from cfg
    std::vector<Jet> jets = bias_pt_sort_jets(nat, ei, in_jets);

    std::vector<std::vector<int>> index_combos = buildClassifierInput::get_6jet_index_combos(jets.size());
    if (debug_){
      cout << "select_sixb_jets_6jet_DNN : DEBUG : combo jet list" << endl; 
      for (auto combo : index_combos) cout << combo << endl; // parammap overloads << for vector so can print
    }
    std::vector< std::pair<float,std::vector<int>> > n_6j_scores;

    for (std::vector<int> combo : index_combos)
    {
      std::vector<float> input = buildClassifierInput::build_6jet_classifier_input(jets,combo);
      float score = n_6j_classifier_->evaluate(input)[0];
      if (debug_){
        // cout << "select_sixb_jets_6jet_DNN : DEBUG : input list and score below" << endl; 
        cout << "select_sixb_jets_6jet_DNN : DEBUG : inputs to DNN" << input << endl;
        cout << "select_sixb_jets_6jet_DNN : DEBUG : --> score " << score << endl;
      }
      n_6j_scores.push_back( std::make_pair(-score,combo) );
    }
    std::sort(n_6j_scores.begin(),n_6j_scores.end());
    float b_6j_score = -n_6j_scores[0].first;
    std::vector<int> b_index_combo = n_6j_scores[0].second;

    if (debug_) cout << "select_sixb_jets_6jet_DNN : DEBUG : b_index_combo : " << b_index_combo << endl;

    ei.b_6j_score = b_6j_score;
    std::vector<Jet> b_jets;
    for (int ij : b_index_combo)
    {
      Jet& j = jets[ij];
      // j.set_preselIdx(ij);
      b_jets.push_back( j );
    }
    return b_jets;
}

std::vector<Jet> SixB_functions::select_sixb_jets_maxbtag(NanoAODTree& nat, EventInfo& ei, const std::vector<Jet>& in_jets)
{   
  std::vector<Jet> jets = in_jets;
  stable_sort(jets.begin(), jets.end(), [](const Jet& a, const Jet& b) -> bool {
          return ( get_property (a, Jet_btagDeepFlavB) > get_property (b, Jet_btagDeepFlavB) ); }
  ); // sort jet by deepjet score (highest to lowest)

  int n_out = std::min<int>(jets.size(), 6);
  jets.resize(n_out);

  return jets;
}

std::vector<Jet> SixB_functions::select_sixb_jets_maxbtag_highpT(NanoAODTree& nat, EventInfo& ei, const std::vector<Jet>& in_jets, int nleadbtag)
{
    std::vector<Jet> jets = in_jets;
    stable_sort(jets.begin(), jets.end(), [](const Jet& a, const Jet& b) -> bool {
            return ( get_property (a, Jet_btagDeepFlavB) > get_property (b, Jet_btagDeepFlavB) ); }
    ); // sort jet by deepjet score (highest to lowest)

    int n_out_btag = std::min<int>(jets.size(), nleadbtag);
    std::vector<Jet> out_jets (jets.begin(), jets.begin()+n_out_btag); // copy the first N btag jets to the out vector

    std::vector<Jet>(jets.begin()+n_out_btag,jets.end()).swap(jets); // put into "jets" the remaining elements

    stable_sort(jets.begin(), jets.end(), [](const Jet& a, const Jet& b) -> bool {
            return ( a.P4().Pt() > b.P4().Pt() ); }
    ); // sort jet by pT (highest to lowest)

    int n_to_add = std::min<int>(jets.size(), 6-nleadbtag); // add at most 6-nleadbtag elements (if they are available)
    out_jets.insert(out_jets.end(), jets.begin(), jets.begin()+n_to_add);

    // std::cout << "   ---> IN JETS" << std::endl;
    // for (auto& jet : in_jets)
    //     std::cout << jet.P4().Pt() << " " << get_property (jet, Jet_btagDeepFlavB) << std::endl;
    // std::cout << std::endl << std::endl;

    // std::cout << "   ---> OUT JETS" << std::endl;
    // for (auto& jet : out_jets)
    //     std::cout << jet.P4().Pt() << " " << get_property (jet, Jet_btagDeepFlavB) << std::endl;
    // std::cout << std::endl << "-------------------------" << std::endl;

    return out_jets;
}


// bool SixB_functions::pass_jet_cut(Cutflow& cutflow,const std::vector<double> pt_cuts,const std::vector<int> btagWP_cuts,const std::vector<Jet> &in_jets)
// {
//   std::vector<std::string> wplabels = {"loose","medium","tight"};
  
//   unsigned int ncuts = pt_cuts.size();

//   if ( in_jets.size() < ncuts ) return false;

//   for (unsigned int icut = 0; icut < ncuts; icut++)
//   {
//     const Jet& ijet = in_jets[icut];

//     double pt = pt_cuts[icut];
//     int btag_wp = btagWP_cuts[icut];

//     if ( ijet.get_ptRegressed() <= pt || ijet.get_btag() <= btag_WPs[btag_wp] )
//       return false;

//     cutflow.add( "jet" + std::to_string(icut) + "_pt" + std::to_string( (int)pt ) + "_" + wplabels[btag_wp]  );
//   }
//   return true;
// }


// std::vector<Jet> SixB_functions::get_all_jets(NanoAODTree& nat)
// {
//   std::vector<DiJet> higgs_list;
	
//   for (unsigned int i = 0; i < in_jets.size(); i++)
//     {
//       if (higgs_list.size() == 3) break;
		
//       Jet& j1 = in_jets[i];
//       if (j1.get_higgsIdx() != -1) continue;

//       std::vector<std::pair<int,DiJet>> dijet_pairs;
//       for (unsigned int k = i+1; k < in_jets.size(); k++)
// 	{
// 	  Jet& j2 = in_jets[k];
// 	  if (j2.get_higgsIdx() != -1) continue;
			
// 	  DiJet dijet(j1,j2);
// 	  dijet_pairs.push_back( std::make_pair(k,dijet) );
// 	}
//       if (dijet_pairs.size() == 0) continue;
//       std::sort(dijet_pairs.begin(),dijet_pairs.end(),[](auto di1,auto di2){ return fabs(di1.second.M()-125)<fabs(di2.second.M()-125); });
		
//       int pair_idx = dijet_pairs[0].first;
//       DiJet& higgs_p4 = dijet_pairs[0].second;
//       Jet& j2 = in_jets[pair_idx];
				  
//       j1.set_higgsIdx( higgs_list.size() );
//       j2.set_higgsIdx( higgs_list.size() );
//       higgs_list.push_back(higgs_p4);
//     }
//   return higgs_list;
// }

// std::vector<DiJet> SixB_functions::get_tri_higgs_D_HHH(std::vector<Jet>& in_jets)
// {

//   // Optimial 3D Line to select most signal like higgs
//   const float phi = 0.77;
//   const float theta = 0.98;
//   const ROOT::Math::Polar3DVectorF r_vec(1,theta,phi);
	
//   std::vector<DiJet> dijets;
//   for (const std::vector<int> ijets : dijet_pairings)
//     { 
//       int ij1 = ijets[0]; int ij2 = ijets[1];
//       DiJet dijet(in_jets[ij1],in_jets[ij2]);
//       dijets.push_back( dijet );
//     }
	
//   std::vector< std::pair<float,int> > triH_d_hhh;
//   for (unsigned int i = 0; i < triH_pairings.size(); i++)
//     {
//       std::vector<DiJet> tri_dijet_sys;
//       for (int id : triH_pairings[i]) tri_dijet_sys.push_back( dijets[id] );
//       std::sort(tri_dijet_sys.begin(),tri_dijet_sys.end(),[](DiJet& dj1,DiJet& dj2){ return dj1.Pt()>dj2.Pt(); });
		
//       ROOT::Math::XYZVectorF m_vec(tri_dijet_sys[0].M(),tri_dijet_sys[1].M(),tri_dijet_sys[2].M());
//       float d_hhh = m_vec.Cross(r_vec).R();
//       triH_d_hhh.push_back( std::make_pair(d_hhh,i) );
//     }

//   // Choose the closest triH vector to the r_vec line
//   std::sort(triH_d_hhh.begin(),triH_d_hhh.end(),[](std::pair<float,int> h1,std::pair<float,int> h2){ return h1.first<h2.first; });

//   int itriH = triH_d_hhh[0].second;
//   std::vector<int> idijets = triH_pairings[itriH];

//   // Order dijets by highest Pt
//   std::sort(idijets.begin(),idijets.end(),[dijets](int id1,int id2){ return dijets[id1].Pt() > dijets[id2].Pt(); });
//   std::vector<DiJet> higgs_list;
	
//   for (unsigned int i = 0; i < idijets.size(); i++)
//     {
//       int id = idijets[i];
//       for (int ij : dijet_pairings[id])
// 	{
// 	  Jet& jet = in_jets[ij];
// 	  jet.set_higgsIdx(i);
// 	}
		
//       DiJet dijet = dijets[id];

//       higgs_list.push_back(dijet);
//     }
	
//   return higgs_list;
// }

// std::vector<Jet> SixB_functions::get_6jet_top(std::vector<Jet>& in_jets)
// {
//   std::vector<Jet> b_jets;
//   for (int i = 0; i < 6; i++)
//     {
//       Jet& j = in_jets[i];
//       j.set_preselIdx(i);
//       b_jets.push_back(j);
//     }
//   return b_jets;
// }

// std::vector<Jet> SixB_functions::get_6jet_NN(EventInfo& ei,std::vector<Jet>& in_jets,EvalNN& n_6j_classifier)
// {
//   std::vector<Jet> b_jets;
	
//   std::vector<std::vector<int>> index_combos = get_6jet_index_combos(in_jets.size());
	
//   std::vector< std::pair<float,std::vector<int>> > n_6j_scores;
//   for (std::vector<int> combo : index_combos)
//     {
//       std::vector<float> input = build_6jet_classifier_input(in_jets,combo);
//       float score = n_6j_classifier.evaluate(input)[0];
//       n_6j_scores.push_back( std::make_pair(-score,combo) );
//     }
//   std::sort(n_6j_scores.begin(),n_6j_scores.end());
//   float b_6j_score = -n_6j_scores[0].first;
//   std::vector<int> b_index_combo = n_6j_scores[0].second;
  
//   ei.b_6j_score = b_6j_score;
  
//   for (int ij : b_index_combo)
//     {
//       Jet& j = in_jets[ij];
//       j.set_preselIdx(ij);
//       b_jets.push_back( j );
//     }
	
//   return b_jets;
// }


// std::vector<DiJet> SixB_functions::get_2jet_NN(EventInfo& ei,std::vector<Jet>& in_jets,EvalNN& n_2j_classifier)
// {
//   std::vector<DiJet> b_dijets;
	
//   std::vector<float> n_2j_scores;
//   for (std::vector<int> combo : dijet_pairings)
//     {
//       std::vector<float> input = buildClassifierInput::build_2jet_classifier_input(in_jets,combo);
//       float score = n_2j_classifier.evaluate(input)[0];
//       n_2j_scores.push_back(score);
//     }

//   std::vector< std::pair<float,std::vector<int>> > triH_scores;
//   for (std::vector<int> combo : triH_pairings)
//     {
//       float score = 0;
//       for (int i : combo) score += n_2j_scores[i]*n_2j_scores[i];
//       score = sqrt(score/3);
//       triH_scores.push_back( std::make_pair(-score,combo) );
//     }
//   std::sort(triH_scores.begin(),triH_scores.end());
//   std::vector<int> b_index_combo = triH_scores[0].second;
  
//   float b_3d_score = -triH_scores[0].first;
//   std::vector<float> b_2j_scores;
//   for (int i : b_index_combo) b_2j_scores.push_back(n_2j_scores[i]);

//   ei.b_3d_score = b_3d_score;

//   for (int ih = 0; ih < 3; ih++)
//     {
//       int id = b_index_combo[ih];
//       std::vector<int> ijs = dijet_pairings[id];
//       Jet& j1 = in_jets[ ijs[0] ]; Jet& j2 = in_jets[ ijs[1] ];

//       j1.set_higgsIdx(ih);
//       j2.set_higgsIdx(ih);
		
//       DiJet dijet(j1,j2);

//       dijet.set_2j_score(n_2j_scores[id]);
//       b_dijets.push_back(dijet);
//     }
//   std::sort(b_dijets.begin(),b_dijets.end(),[](DiJet& d1,DiJet& d2){ return d1.Pt()>d2.Pt(); });
	
//   return b_dijets;
// }

std::vector<DiJet> SixB_functions::get_3dijet_NN(EventInfo& ei,std::vector<Jet>& in_jets,EvalNN& n_3d_classifier)
{
  std::vector<DiJet> b_dijets;

  std::vector< std::pair<float,std::vector<int>> > triH_scores;
  for (std::vector<int> combo : triH_pairings)
    {
      std::vector<int> jet_combo;
      for (int id : combo) jet_combo.insert(jet_combo.end(),dijet_pairings[id].begin(),dijet_pairings[id].end());

      std::vector<float> input = buildClassifierInput::build_3dijet_classifier_input(in_jets,jet_combo);
      float score = n_3d_classifier.evaluate(input)[0];
      triH_scores.push_back( std::make_pair(-score,combo) );
    }
  std::sort(triH_scores.begin(),triH_scores.end());
  std::vector<int> b_index_combo = triH_scores[0].second;
  
  float b_3d_score = -triH_scores[0].first;
  ei.b_3d_score = b_3d_score;

  for (int ih = 0; ih < 3; ih++)
    {
      int id = b_index_combo[ih];
      std::vector<int> ijs = dijet_pairings[id];
      Jet& j1 = in_jets[ ijs[0] ]; Jet& j2 = in_jets[ ijs[1] ];

      j1.set_higgsIdx(ih);
      j2.set_higgsIdx(ih);
		
      DiJet dijet(j1,j2);
      b_dijets.push_back(dijet);
    }
  std::sort(b_dijets.begin(),b_dijets.end(),[](DiJet& d1,DiJet& d2){ return d1.Pt()>d2.Pt(); });
	
  return b_dijets;
}

// std::vector<DiJet> SixB_functions::get_tri_higgs_NN(EventInfo& ei,std::vector<Jet>& in_jets,EvalNN& n_6j_classifier,EvalNN& n_2j_classifier)
// {
//   std::vector<DiJet> higgs_list;

//   std::vector<Jet> b_jets = get_6jet_NN(ei,in_jets,n_6j_classifier);
//   higgs_list = get_2jet_NN(ei,b_jets,n_2j_classifier);
	
//   return higgs_list;
// }


bool SixB_functions::pass_higgs_cr(const std::vector<DiJet>& in_dijets)
{
  //
	
  float higgs_mass = 125;
  float mass_sideband = 30;
	
  for (DiJet dijet : in_dijets)
    if ( fabs(dijet.M() - higgs_mass) <= mass_sideband )
      return false;
	
  return true;
}


void SixB_functions::pair_jets(NanoAODTree& nat, EventInfo& ei, const std::vector<Jet>& in_jets)
{
  std::tuple<CompositeCandidate, CompositeCandidate, CompositeCandidate> reco_Hs;

  // call the desired algo - expected interface is input jets -> output 3 composite candidate HX, H1. H2
  // the order of H1, H2 and of the jets does not matter - they will be reordered after

  std::string pairAlgo = pmap.get_param<std::string>("configurations", "jetPairsChoice");
  if (pairAlgo == "passthrough")
    reco_Hs = pair_passthrough(nat, ei, in_jets);
  // else if (pairAlgo == "m_H")
    // reco_Hs = pair_mH(nat, ei, in_jets);
  else if (pairAlgo == "D_HHH")
    reco_Hs = pair_D_HHH(nat, ei, in_jets);
  else if (pairAlgo == "D_HHH_corr") {
    int fitCorrection = std::stoi(pmap.get_param<std::string>("configurations", "fitCorrection"));
    reco_Hs = pair_D_HHH(nat, ei, in_jets, fitCorrection);
  }
  else if (pairAlgo == "2jet_DNN")
    reco_Hs = pair_2jet_DNN(nat, ei, in_jets);
  else if (pairAlgo == "min_diag_distance")
        reco_Hs = pair_min_diag_distance(nat, ei, in_jets);


  std::tuple<CompositeCandidate, CompositeCandidate, CompositeCandidate> reco_HX_HY_HY;

  std::string XYHAlgo = pmap.get_param<std::string>("configurations", "XYHChoice");
  if (XYHAlgo == "passthrough")
    reco_HX_HY_HY = reco_Hs;
  else if (XYHAlgo == "leadJetInX")
    reco_HX_HY_HY = select_XYH_leadJetInX(nat, ei, reco_Hs);

  // call the al

  // reorder objects
  CompositeCandidate HX  = std::get<0>(reco_HX_HY_HY);
  CompositeCandidate H1 = std::get<1>(reco_HX_HY_HY);
  CompositeCandidate H2 = std::get<2>(reco_HX_HY_HY);

  // rebuild p4 with regressed pT if required
  if (pmap.get_param<bool>("configurations", "useRegressedPtForHp4")){
    HX.rebuildP4UsingRegressedPt(true, true);
    H1.rebuildP4UsingRegressedPt(true, true);
    H2.rebuildP4UsingRegressedPt(true, true);
  }

  if (H1.P4().Pt() < H2.P4().Pt())
    std::swap(H1, H2);

  if (HX.getComponent1().P4().Pt() < HX.getComponent2().P4().Pt())
    HX.swapComponents();

  if (H1.getComponent1().P4().Pt() < H1.getComponent2().P4().Pt())
    H1.swapComponents();

  if (H2.getComponent1().P4().Pt() < H2.getComponent2().P4().Pt())
    H2.swapComponents();

  CompositeCandidate Y(H1, H2);
  CompositeCandidate X(Y, HX);

  ei.X = X;
  ei.Y = Y;

  ei.HX = HX;
  ei.H1 = H1;
  ei.H2 = H2;

  ei.HX_b1 = static_cast<Jet&>(HX.getComponent1());
  ei.HX_b2 = static_cast<Jet&>(HX.getComponent2());
    
  ei.H1_b1 = static_cast<Jet&>(H1.getComponent1());
  ei.H1_b2 = static_cast<Jet&>(H1.getComponent2());
    
  ei.H2_b1 = static_cast<Jet&>(H2.getComponent1());
  ei.H2_b2 = static_cast<Jet&>(H2.getComponent2());

}

std::tuple<CompositeCandidate, CompositeCandidate, CompositeCandidate> SixB_functions::pair_passthrough (NanoAODTree &nat, EventInfo& ei, const std::vector<Jet>& jets)
{
  if (jets.size() != 6)
    throw std::runtime_error("The jet pairing -passthrough- function requires 6 jets");

  CompositeCandidate HX (jets.at(0), jets.at(1));
  CompositeCandidate H1 (jets.at(2), jets.at(3));
  CompositeCandidate H2 (jets.at(4), jets.at(5));

  return std::make_tuple(HX, H1, H2);
}

std::tuple<CompositeCandidate, CompositeCandidate, CompositeCandidate> SixB_functions::pair_D_HHH(NanoAODTree &nat, EventInfo& ei, const std::vector<Jet>& in_jets)
{
  // Optimial 3D Line to select most signal like higgs
  const float phi = 0.77;
  const float theta = 0.98;
  const ROOT::Math::Polar3DVectorF r_vec(1,theta,phi);

  // NOTE: p4 is constructed using unregressed pT
  // to update if it needs to use the regressed pT by calling CompositeCandiadte.rebuildP4UsingRegressedPt

  std::vector<CompositeCandidate> dijets;
  for (const std::vector<int> ijets : dijet_pairings)
  { 
    int ij1 = ijets[0]; int ij2 = ijets[1];
    CompositeCandidate dijet(in_jets[ij1],in_jets[ij2]);
    dijets.push_back( dijet );
  }
  
  
  std::vector< std::pair<float,int> > triH_d_hhh;
  for (unsigned int i = 0; i < triH_pairings.size(); i++)
    {
      std::vector<CompositeCandidate> tri_dijet_sys;
      for (int id : triH_pairings[i]) tri_dijet_sys.push_back( dijets[id] );

      std::sort(tri_dijet_sys.begin(),tri_dijet_sys.end(),[](CompositeCandidate& dj1,CompositeCandidate& dj2){ return dj1.P4().Pt()>dj2.P4().Pt(); });
        
      ROOT::Math::XYZVectorF m_vec(tri_dijet_sys[0].P4().M(),tri_dijet_sys[1].P4().M(),tri_dijet_sys[2].P4().M());
      float d_hhh = m_vec.Cross(r_vec).R();
      triH_d_hhh.push_back( std::make_pair(d_hhh,i) );
    }


  // Choose the closest triH vector to the r_vec line
  std::sort(triH_d_hhh.begin(),triH_d_hhh.end(),[](std::pair<float,int> h1,std::pair<float,int> h2){ return h1.first<h2.first; });

  int itriH = triH_d_hhh[0].second;
  std::vector<int> idijets = triH_pairings[itriH];


  // Order dijets by highest Pt
  std::sort(idijets.begin(),idijets.end(),[dijets](int id1,int id2){ return dijets[id1].P4().Pt() > dijets[id2].P4().Pt(); });

  std::tuple<CompositeCandidate, CompositeCandidate, CompositeCandidate> higgs_cands = std::make_tuple(dijets[idijets[0]], dijets[idijets[1]], dijets[idijets[2]]);


  return higgs_cands;

  // std::vector<CompositeCandidate> higgs_list;
    
  // for (unsigned int i = 0; i < idijets.size(); i++)
  //   {
  //     int id = idijets[i];
  //     for (int ij : dijet_pairings[id])
  //     {
  //       Jet& jet = in_jets[ij];
  //       jet.set_higgsIdx(i);
  //     }
        
  //     DiJet dijet = dijets[id];

  //     higgs_list.push_back(dijet);
  //   }
    
  // return higgs_list;  
}

std::tuple<CompositeCandidate, CompositeCandidate, CompositeCandidate> SixB_functions::pair_D_HHH (NanoAODTree &nat, EventInfo& ei, const std::vector<Jet>& in_jets, const int fitCorrection)
{
  // Optimial 3D Line to select most signal like higgs
  const float phi = 0.77;
  const float theta = 0.98;
  const ROOT::Math::Polar3DVectorF r_vec(1,theta,phi);

  // NOTE: p4 is constructed using unregressed pT
  // to update if it needs to use the regressed pT by calling CompositeCandiadte.rebuildP4UsingRegressedPt

  std::vector<CompositeCandidate> dijets;
  for (const std::vector<int> ijets : dijet_pairings)
  { 
    int ij1 = ijets[0]; int ij2 = ijets[1];
    CompositeCandidate dijet(in_jets[ij1],in_jets[ij2]);
    dijet.rebuildP4UsingRegressedPt(true, true);
    dijets.push_back( dijet );
  }


  std::vector< std::pair<float,int> > triH_d_hhh;
  for (unsigned int i = 0; i < triH_pairings.size(); i++)
    {
      std::vector<CompositeCandidate> tri_dijet_sys;
      for (int id : triH_pairings[i]) tri_dijet_sys.push_back( dijets[id] );

      std::sort(tri_dijet_sys.begin(),tri_dijet_sys.end(),[](CompositeCandidate& dj1,CompositeCandidate& dj2){ return dj1.P4().Pt()>dj2.P4().Pt(); });
        
      ROOT::Math::XYZVectorF m_vec(tri_dijet_sys[0].P4().M(),tri_dijet_sys[1].P4().M(),tri_dijet_sys[2].P4().M());
      float d_hhh = m_vec.Cross(r_vec).R();
      triH_d_hhh.push_back( std::make_pair(d_hhh,i) );
    }

  // Choose the closest triH vector to the r_vec line
  std::sort(triH_d_hhh.begin(),triH_d_hhh.end(),[](std::pair<float,int> h1,std::pair<float,int> h2){ return h1.first<h2.first; });

  float min_d_hhh = triH_d_hhh[0].first;
  float next_min_d_hhh = triH_d_hhh[1].first;
  float Delta_d_hhh = next_min_d_hhh - min_d_hhh;

  int itriH;
  // if minimum d_hhh is significantly smaller than the next to minimum d_hhh, select the min
  // otherwise, maximize the pT in the 6-jet CM frame
  if (Delta_d_hhh > 30) {
    itriH = triH_d_hhh[0].second;
  }
  else {
    // check which pairings maximize the pT in the 6-jet CM frame
    // FIX ME
    itriH = triH_d_hhh[0].second; // not correct, just a placeholder
  }

  std::vector<int> idijets = triH_pairings[itriH];

  // Order dijets by highest Pt
  std::sort(idijets.begin(),idijets.end(),[dijets](int id1,int id2){ return dijets[id1].P4().Pt() > dijets[id2].P4().Pt(); });

  std::tuple<CompositeCandidate, CompositeCandidate, CompositeCandidate> higgs_cands = std::make_tuple(dijets[idijets[0]], dijets[idijets[1]], dijets[idijets[2]]);
  return higgs_cands;
}

std::tuple<CompositeCandidate, CompositeCandidate, CompositeCandidate> SixB_functions::pair_min_diag_distance (NanoAODTree &nat, EventInfo& ei, std::vector<Jet> jets)
{
  if (jets.size() != 6)
      throw std::runtime_error("The jet pairing -min_diag_distance- function requires 6 jets");

  const bool use_pt_regressed = true;

  // 6 jets -> 15 possible pairings given by:
  // (0, 1), (2, 3), (4, 5)
  // (0, 1), (2, 4), (3, 5)
  // (0, 1), (2, 5), (3, 4)
  // (0, 2), (1, 3), (4, 5)
  // (0, 2), (1, 4), (3, 5)
  // (0, 2), (1, 5), (3, 4)
  // (0, 3), (1, 2), (4, 5)
  // (0, 3), (1, 4), (2, 5)
  // (0, 3), (1, 5), (2, 4)
  // (0, 4), (1, 2), (3, 5)
  // (0, 4), (1, 3), (2, 5)
  // (0, 4), (1, 5), (2, 3)
  // (0, 5), (1, 2), (3, 4)
  // (0, 5), (1, 3), (2, 4)
  // (0, 5), (1, 4), (2, 3)

  typedef std::array<unsigned int, 6> idx_t; // {p0.0, p0.1, p1.0, p1.1, p2.0, p2.1}
  typedef std::array<idx_t, 15> idx_list_t; // idx_t x 15
  typedef std::array<CompositeCandidate, 3> pair_triplet_t;
  // not super elegant, but the list of all possible 15 pairs is the one below
  const idx_list_t idxs = {{
      {0, 1,    2, 3,    4, 5},
      {0, 1,    2, 4,    3, 5},
      {0, 1,    2, 5,    3, 4},
      {0, 2,    1, 3,    4, 5},
      {0, 2,    1, 4,    3, 5},
      {0, 2,    1, 5,    3, 4},
      {0, 3,    1, 2,    4, 5},
      {0, 3,    1, 4,    2, 5},
      {0, 3,    1, 5,    2, 4},
      {0, 4,    1, 2,    3, 5},
      {0, 4,    1, 3,    2, 5},
      {0, 4,    1, 5,    2, 3},
      {0, 5,    1, 2,    3, 4},
      {0, 5,    1, 3,    2, 4},
      {0, 5,    1, 4,    2, 3}
  }};

  // cout << "--- debug idx to build" << endl;
  // for (unsigned int i = 0; i < 15; ++i){
  //     for (unsigned int j = 0; j < 6; ++j){
  //         cout << idxs[i][j] << " ";
  //     }
  //     cout << endl;
  // }

  std::array<pair_triplet_t, 15> pairs;
  for (unsigned int ip = 0; ip < 15; ++ip){

      const idx_t& tidx = idxs.at(ip);
      CompositeCandidate hA (jets.at(tidx.at(0)), jets.at(tidx.at(1)) );
      CompositeCandidate hB (jets.at(tidx.at(2)), jets.at(tidx.at(3)) );
      CompositeCandidate hC (jets.at(tidx.at(4)), jets.at(tidx.at(5)) );

      if (use_pt_regressed){
          hA.rebuildP4UsingRegressedPt(true, true);
          hB.rebuildP4UsingRegressedPt(true, true);
          hC.rebuildP4UsingRegressedPt(true, true);
      }

      pairs.at(ip) = {hA, hB, hC};
  }

  struct vec3d {
      double x;
      double y;
      double z;
  };

  // compute the distance from the 3D "diagonal"
  // FIXME: can order pairs by H pT and define a diagonal that is not passing at 125/125/125 (take into account responses a la)
  const vec3d diag = {1./sqrt(3), 1./sqrt(3), 1./sqrt(3)};

  std::vector<std::pair<double, int>> mdiff_idx;
  for (unsigned int ip = 0; ip < 15; ++ip){

      // vector from origin (0,0,0) to this 3d mass point
      // FIXME: check if this uses standard p4 or regressed p4
      vec3d masspoint = {pairs.at(ip).at(0).P4().M(), pairs.at(ip).at(1).P4().M(), pairs.at(ip).at(2).P4().M()};
      
      // compute projection on diagonal - note: diagonal has a norm of 1 already
      double dotprod = masspoint.x*diag.x + masspoint.y*diag.y + masspoint.z*diag.z;

      // get the projected point
      vec3d proj {dotprod*diag.x, dotprod*diag.y, dotprod*diag.z};

      // distance of projection from masspoint
      double dx = proj.x - masspoint.x;
      double dy = proj.y - masspoint.y;
      double dz = proj.z - masspoint.z;
      double d = sqrt(dx*dx + dy*dy + dz*dz);
      mdiff_idx.push_back (make_pair(d, ip));   
  }

  // -------------------------------------------------------------

  // // sort to take the closest pair and return it
  // std::sort(mdiff_idx.begin(), mdiff_idx.end());
  // int best_idx = mdiff_idx.at(0).second;

  // -------------------------------------------------------------

  // take all pairs with a distance from the first value within the resolution 30 GeV - FIXME: tune value
  // then boost to the 6 jet ref frame and get the pair giving the largest sum(ptH)
  const double thresh_mdiff = 30.;
  std::sort(mdiff_idx.begin(), mdiff_idx.end());
  std::vector<std::pair<double, int>> mdiff_idx_afterthresh;
  for (unsigned int ip = 0; ip < 15; ++ip){
      double mdiff = mdiff_idx.at(ip).first - mdiff_idx.at(0).first;
      if (mdiff < thresh_mdiff){
          mdiff_idx_afterthresh.push_back(mdiff_idx.at(ip));
      }
  }

  int best_idx = -1;
  
  if (mdiff_idx_afterthresh.size() == 1){ // by construction size is >= 1 always since 1st pair is compared with itself
      best_idx = mdiff_idx_afterthresh.at(0).second;
  }
  
  else { // only for pairs thus selected, pick up the one with the highest sum(p H)
      std::vector<std::pair<double, int>> psum_idx_afterthresh;
      for (unsigned int ip = 0; ip < mdiff_idx_afterthresh.size(); ++ip){
          
          int ipair = mdiff_idx_afterthresh.at(ip).second;
          pair_triplet_t tr = pairs.at(ipair); // retrieve this triplet
          CompositeCandidate hA = tr.at(0);
          CompositeCandidate hB = tr.at(1);
          CompositeCandidate hC = tr.at(2);

          p4_t vsum (0,0,0,0);
          vsum += hA.P4();
          vsum += hB.P4();
          vsum += hC.P4();
          auto boost_vctr = vsum.BoostToCM();
          ROOT::Math::Boost boost(boost_vctr);

          // p4_t vsum_cm  = boost(vsum);
          p4_t hA_p4_cm = boost(hA.P4());
          p4_t hB_p4_cm = boost(hB.P4());
          p4_t hC_p4_cm = boost(hC.P4());
          // cout << " XCHECK: " << vsum_cm.Pt() << "  x/y/z" << vsum_cm.Px() << " " << vsum_cm.Py() << " " << vsum_cm.Pz() << " || " << vsum_cm.P() << "  " << hA.P4().Pt() << " --> " << hA_p4_cm.Pt() << endl;
          double psum = hA_p4_cm.P() + hB_p4_cm.P() + hC_p4_cm.P();
          psum_idx_afterthresh.push_back(make_pair(psum, ipair));
      }
      std::sort(psum_idx_afterthresh.begin(), psum_idx_afterthresh.end());
      best_idx = psum_idx_afterthresh.back().second; // take the one with the highest pT sum
  }
  
  // -------------------------------------------------------------

  std::tuple<CompositeCandidate, CompositeCandidate, CompositeCandidate> result = make_tuple(pairs.at(best_idx).at(0), pairs.at(best_idx).at(1), pairs.at(best_idx).at(2));

  // FIXME: need to attribute correctly who is HX, H1, H2

  return result;
}

std::tuple<CompositeCandidate, CompositeCandidate, CompositeCandidate> SixB_functions::pair_2jet_DNN (NanoAODTree &nat, EventInfo& ei, const std::vector<Jet>& in_jets)
{

  std::vector<Jet> jets = in_jets;
  
  std::vector<float> n_2j_scores;

  for (std::vector<int> combo : dijet_pairings)
  {
    std::vector<float> input = buildClassifierInput::build_2jet_classifier_input(jets,combo);
    float score = n_2j_classifier_->evaluate(input)[0];
    n_2j_scores.push_back(score);
  }

  std::vector< std::pair<float,std::vector<int>> > triH_scores;
  for (std::vector<int> combo : triH_pairings)
  {
    float score = 0;
    for (int i : combo) score += n_2j_scores[i]*n_2j_scores[i];
    score = sqrt(score/3);
    triH_scores.push_back( std::make_pair(-score,combo) );
  }
  std::sort(triH_scores.begin(),triH_scores.end());
  std::vector<int> b_index_combo = triH_scores[0].second;

  float b_3d_score = -triH_scores[0].first;
  std::vector<float> b_2j_scores;
  for (int i : b_index_combo) b_2j_scores.push_back(n_2j_scores[i]);

  ei.b_3d_score = b_3d_score;

  std::vector<CompositeCandidate> b_dijets_vec;
  for (int ih = 0; ih < 3; ih++)
  {
    int id = b_index_combo[ih];
    std::vector<int> ijs = dijet_pairings[id];
    Jet& j1 = jets[ ijs[0] ]; Jet& j2 = jets[ ijs[1] ];

    // j1.set_higgsIdx(ih);
    // j2.set_higgsIdx(ih);

    CompositeCandidate dijet(j1,j2);

    // dijet.set_2j_score(n_2j_scores[id]);
    b_dijets_vec.push_back(dijet);
  }

  std::tuple<CompositeCandidate, CompositeCandidate, CompositeCandidate> b_dijets = make_tuple(b_dijets_vec.at(0), b_dijets_vec.at(1), b_dijets_vec.at(2));

  // skip sorting, since anyway this is redone in the parent function to assign elements and H to the ei
  // std::sort(b_dijets.begin(),b_dijets.end(),[](DiJet& d1,DiJet& d2){ return d1.Pt()>d2.Pt(); });

  return b_dijets;
}



std::tuple<CompositeCandidate, CompositeCandidate, CompositeCandidate> SixB_functions::select_XYH_leadJetInX (
  NanoAODTree& nat, EventInfo& ei, std::tuple<CompositeCandidate, CompositeCandidate, CompositeCandidate> reco_Hs)
{
  std::array<CompositeCandidate, 3> reco_Hs_arr = {
    std::get<0>(reco_Hs),
    std::get<1>(reco_Hs),
    std::get<2>(reco_Hs)
  };

  std::vector<std::pair<double, int>> leadPt(3);

  if (pmap.get_param<bool>("leadJetInX", "useRegressedPt")){
    leadPt.at(0) = make_pair(std::max(dynamic_cast<Jet&>(reco_Hs_arr.at(0).getComponent1()).P4().Pt(), dynamic_cast<Jet&>(reco_Hs_arr.at(0).getComponent2()).P4().Pt()), 0);
    leadPt.at(1) = make_pair(std::max(dynamic_cast<Jet&>(reco_Hs_arr.at(1).getComponent1()).P4().Pt(), dynamic_cast<Jet&>(reco_Hs_arr.at(1).getComponent2()).P4().Pt()), 1);
    leadPt.at(2) = make_pair(std::max(dynamic_cast<Jet&>(reco_Hs_arr.at(2).getComponent1()).P4().Pt(), dynamic_cast<Jet&>(reco_Hs_arr.at(2).getComponent2()).P4().Pt()), 2);    
  }
  
  else {
    leadPt.at(0) = make_pair(std::max(reco_Hs_arr.at(0).getComponent1().P4().Pt(), reco_Hs_arr.at(0).getComponent2().P4().Pt()), 0);
    leadPt.at(1) = make_pair(std::max(reco_Hs_arr.at(1).getComponent1().P4().Pt(), reco_Hs_arr.at(1).getComponent2().P4().Pt()), 1);
    leadPt.at(2) = make_pair(std::max(reco_Hs_arr.at(2).getComponent1().P4().Pt(), reco_Hs_arr.at(2).getComponent2().P4().Pt()), 2);
  }

  sort(leadPt.begin(), leadPt.end());
  
  std::tuple<CompositeCandidate, CompositeCandidate, CompositeCandidate> ret_tuple = make_tuple(
    reco_Hs_arr.at(leadPt.at(2).second),
    reco_Hs_arr.at(leadPt.at(1).second),
    reco_Hs_arr.at(leadPt.at(0).second)
  );

  return ret_tuple;
}

int SixB_functions::n_gjmatched_in_jetcoll(NanoAODTree& nat, EventInfo& ei, const std::vector<Jet>& in_jets)
{
  std::vector<int> matched_jets;
  if (ei.gen_HX_b1_recojet)  matched_jets.push_back(ei.gen_HX_b1_recojet->getIdx());
  if (ei.gen_HX_b2_recojet)  matched_jets.push_back(ei.gen_HX_b2_recojet->getIdx());
  if (ei.gen_H1_b1_recojet) matched_jets.push_back(ei.gen_H1_b1_recojet->getIdx());
  if (ei.gen_H1_b2_recojet) matched_jets.push_back(ei.gen_H1_b2_recojet->getIdx());
  if (ei.gen_H2_b1_recojet) matched_jets.push_back(ei.gen_H2_b1_recojet->getIdx());
  if (ei.gen_H2_b2_recojet) matched_jets.push_back(ei.gen_H2_b2_recojet->getIdx());

  std::vector<int> reco_js (in_jets.size());
  for (unsigned int ij=0; ij<in_jets.size(); ++ij)
    {
      reco_js.at(ij) = in_jets.at(ij).getIdx();
    }
  
  int nfound = 0;
  for (int imj : matched_jets)
    {
      if (std::find(reco_js.begin(), reco_js.end(), imj) != reco_js.end())
	nfound += 1;
    }
  
  return nfound;
}

int SixB_functions::n_ghmatched_in_jetcoll(NanoAODTree& nat, EventInfo& ei, const std::vector<Jet>& in_jets)
{
  std::vector<int> matched_jets(6,-1);
  if (ei.gen_HX_b1_recojet)  matched_jets[0] = ei.gen_HX_b1_recojet->getIdx();
  if (ei.gen_HX_b2_recojet)  matched_jets[1] = ei.gen_HX_b2_recojet->getIdx();
  if (ei.gen_H1_b1_recojet) matched_jets[2] = ei.gen_H1_b1_recojet->getIdx();
  if (ei.gen_H1_b2_recojet) matched_jets[3] = ei.gen_H1_b2_recojet->getIdx();
  if (ei.gen_H2_b1_recojet) matched_jets[4] = ei.gen_H2_b1_recojet->getIdx();
  if (ei.gen_H2_b2_recojet) matched_jets[5] = ei.gen_H2_b2_recojet->getIdx();

  std::vector<int> reco_js(in_jets.size());
  for (unsigned int ij = 0; ij < in_jets.size(); ++ij)
    reco_js.at(ij) = in_jets.at(ij).getIdx();

  int nfound = 0;
  for (unsigned int ih = 0; ih < 3; ++ih)
  {
    bool paired = true;
    for (unsigned int ij = 0; ij < 2; ++ij)
    {
      paired = paired & (std::find(reco_js.begin(), reco_js.end(), matched_jets[2 * ih + ij]) != reco_js.end());
    }
    if (paired)
      nfound += 1;
  }

  return nfound;
}

void SixB_functions::match_signal_genjets(NanoAODTree &nat, EventInfo& ei, std::vector<GenJet> &in_jets)
{
  std::vector<int> matched_jets(6, -1);
  if (ei.gen_HX_b1_genjet)
    matched_jets[0] = ei.gen_HX_b1_genjet->getIdx();
  if (ei.gen_HX_b2_genjet)
    matched_jets[1] = ei.gen_HX_b2_genjet->getIdx();
  if (ei.gen_H1_b1_genjet)
    matched_jets[2] = ei.gen_H1_b1_genjet->getIdx();
  if (ei.gen_H1_b2_genjet)
    matched_jets[3] = ei.gen_H1_b2_genjet->getIdx();
  if (ei.gen_H2_b1_genjet)
    matched_jets[4] = ei.gen_H2_b1_genjet->getIdx();
  if (ei.gen_H2_b2_genjet)
    matched_jets[5] = ei.gen_H2_b2_genjet->getIdx();

  for (GenJet &gj : in_jets)
  {
    int gj_idx = gj.getIdx();
    if (gj_idx == -1)
      continue;

    for (int id = 0; id < 6; id++)
    {
      if (matched_jets[id] == gj_idx)
      {
        gj.set_signalId(id);
      }
    }
  }
}

void SixB_functions::match_signal_recojets(NanoAODTree &nat, EventInfo& ei, std::vector<Jet> &in_jets)
{
  std::vector<int> matched_jets(6, -1);
  if (ei.gen_HX_b1_recojet)
    matched_jets[0] = ei.gen_HX_b1_recojet->getIdx();
  if (ei.gen_HX_b2_recojet)
    matched_jets[1] = ei.gen_HX_b2_recojet->getIdx();
  if (ei.gen_H1_b1_recojet)
    matched_jets[2] = ei.gen_H1_b1_recojet->getIdx();
  if (ei.gen_H1_b2_recojet)
    matched_jets[3] = ei.gen_H1_b2_recojet->getIdx();
  if (ei.gen_H2_b1_recojet)
    matched_jets[4] = ei.gen_H2_b1_recojet->getIdx();
  if (ei.gen_H2_b2_recojet)
    matched_jets[5] = ei.gen_H2_b2_recojet->getIdx();

  for (Jet &j : in_jets)
  {
    int j_idx = j.getIdx();
    if (j_idx == -1)
      continue;

    for (int id = 0; id < 6; id++)
    {
      if (matched_jets[id] == j_idx)
      {
        j.set_signalId(id);
      }
    }
  }
}

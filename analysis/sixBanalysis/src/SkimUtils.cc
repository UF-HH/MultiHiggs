#include "SkimUtils.h"

#include "Math/Vector4D.h"
typedef ROOT::Math::PtEtaPhiMVector p4_t;

#include <iostream>
#include <fstream>
#include <string>

using namespace std;

// helper: copies the pt/eta/phi/p4 branches from a candidate OBJ to the output tree
// NOTE: requires the matching of the names (and enforces it)
#define COPY_m_pt_eta_phi_p4(OBJ)    \
  ot.OBJ##_m = ei.OBJ->P4().M();     \
  ot.OBJ##_pt = ei.OBJ->P4().Pt();   \
  ot.OBJ##_eta = ei.OBJ->P4().Eta(); \
  ot.OBJ##_phi = ei.OBJ->P4().Phi(); \
  ot.OBJ##_p4 = ei.OBJ->P4();

#define COPY_m_pt_ptRegressed_eta_phi_p4(OBJ)        \
  ot.OBJ##_m = ei.OBJ->P4().M();                     \
  ot.OBJ##_mRegressed = ei.OBJ->P4Regressed().M();   \
  ot.OBJ##_pt = ei.OBJ->P4().Pt();                   \
  ot.OBJ##_ptRegressed = ei.OBJ->P4Regressed().Pt(); \
  ot.OBJ##_eta = ei.OBJ->P4().Eta();                 \
  ot.OBJ##_phi = ei.OBJ->P4().Phi();                 \
  ot.OBJ##_p4 = ei.OBJ->P4();

// helperM same as above, but encloses the obj (a boost::optional is expected) in a if clause to check whether it is initialized
#define COPY_OPTIONAL_m_pt_eta_phi_p4(OBJ) \
  if (ei.OBJ)                              \
  {                                        \
    ot.OBJ##_m = ei.OBJ->P4().M();         \
    ot.OBJ##_pt = ei.OBJ->P4().Pt();       \
    ot.OBJ##_eta = ei.OBJ->P4().Eta();     \
    ot.OBJ##_phi = ei.OBJ->P4().Phi();     \
    ot.OBJ##_p4 = ei.OBJ->P4();            \
  }

#define COPY_OPTIONAL_m_pt_eta_phi_score_p4(OBJ) \
  if (ei.OBJ)                                    \
  {                                              \
    ot.OBJ##_m = ei.OBJ->P4().M();               \
    ot.OBJ##_pt = ei.OBJ->P4().Pt();             \
    ot.OBJ##_eta = ei.OBJ->P4().Eta();           \
    ot.OBJ##_phi = ei.OBJ->P4().Phi();           \
    ot.OBJ##_score = ei.OBJ->get_param("score", 0); \
    ot.OBJ##_p4 = ei.OBJ->P4();                  \
  }

#define COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_p4(OBJ) \
  if (ei.OBJ)                                          \
  {                                                    \
    ot.OBJ##_m = ei.OBJ->P4().M();                     \
    ot.OBJ##_mRegressed = ei.OBJ->P4Regressed().M();   \
    ot.OBJ##_pt = ei.OBJ->P4().Pt();                   \
    ot.OBJ##_ptRegressed = ei.OBJ->P4Regressed().Pt(); \
    ot.OBJ##_eta = ei.OBJ->P4().Eta();                 \
    ot.OBJ##_phi = ei.OBJ->P4().Phi();                 \
    ot.OBJ##_p4 = ei.OBJ->P4();                        \
  }

#define COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_DeepJet_p4(OBJ)     \
  if (ei.OBJ)                                                      \
  {                                                                \
    ot.OBJ##_m = ei.OBJ->P4().M();                                 \
    ot.OBJ##_mRegressed = ei.OBJ->P4Regressed().M();               \
    ot.OBJ##_pt = ei.OBJ->P4().Pt();                               \
    ot.OBJ##_ptRegressed = ei.OBJ->P4Regressed().Pt();             \
    ot.OBJ##_eta = ei.OBJ->P4().Eta();                             \
    ot.OBJ##_phi = ei.OBJ->P4().Phi();                             \
    ot.OBJ##_btag = get_property(ei.OBJ.get(), Jet_btagDeepFlavB); \
    ot.OBJ##_p4 = ei.OBJ->P4();                                    \
  }

#define COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_DeepJet_score_p4(OBJ) \
  if (ei.OBJ)                                                        \
  {                                                                  \
    ot.OBJ##_m = ei.OBJ->P4().M();                                   \
    ot.OBJ##_mRegressed = ei.OBJ->P4Regressed().M();                 \
    ot.OBJ##_pt = ei.OBJ->P4().Pt();                                 \
    ot.OBJ##_ptRegressed = ei.OBJ->P4Regressed().Pt();               \
    ot.OBJ##_eta = ei.OBJ->P4().Eta();                               \
    ot.OBJ##_phi = ei.OBJ->P4().Phi();                               \
    ot.OBJ##_btag = get_property(ei.OBJ.get(), Jet_btagDeepFlavB);   \
    ot.OBJ##_score = ei.OBJ->get_param("score", 0);                     \
    ot.OBJ##_p4 = ei.OBJ->P4();                                      \
  }

#define COPY_OPTIONAL_ele_list(OBJ)                                  \
  if (ei.OBJ##_list) {                                               \
      for (Electron & ele : ei.OBJ##_list.get()) {		     \
        ot.OBJ##_E.push_back(ele.get_E());                          \
	ot.OBJ##_m.push_back(ele.get_m());			     \
	ot.OBJ##_pt.push_back(ele.get_pt());			     \
        ot.OBJ##_eta.push_back(ele.get_eta());                       \
        ot.OBJ##_phi.push_back(ele.get_phi());                       \
        ot.OBJ##_dxy.push_back(ele.get_dxy());                       \
        ot.OBJ##_dz.push_back(ele.get_dz());                         \
        ot.OBJ##_charge.push_back(ele.get_charge());                 \
        ot.OBJ##_pfRelIso03_all.push_back(ele.get_pfRelIso03_all());            \
        ot.OBJ##_mvaFall17V2Iso_WPL.push_back(ele.get_mvaFall17V2Iso_WPL());    \
        ot.OBJ##_mvaFall17V2Iso_WP90.push_back(ele.get_mvaFall17V2Iso_WP90());  \
        ot.OBJ##_mvaFall17V2Iso_WP80.push_back(ele.get_mvaFall17V2Iso_WP80());  \
      }								        	\
  }

#define COPY_OPTIONAL_muon_list(OBJ)                                \
  if (ei.OBJ##_list) {                                              \
    for (Muon & muon : ei.OBJ##_list.get()) {			    \
      ot.OBJ##_E.push_back(muon.get_E());                           \
      ot.OBJ##_m.push_back(muon.get_m());		            \
      ot.OBJ##_pt.push_back(muon.get_pt());	                    \
      ot.OBJ##_eta.push_back(muon.get_eta());		            \
      ot.OBJ##_phi.push_back(muon.get_phi());			    \
      ot.OBJ##_dxy.push_back(muon.get_dxy());			    \
      ot.OBJ##_dz.push_back(muon.get_dz());			    \
      ot.OBJ##_charge.push_back(muon.get_charge());	            \
      ot.OBJ##_pfRelIso04_all.push_back(muon.get_pfRelIso04_all()); \
      ot.OBJ##_looseId.push_back(muon.get_looseId());		    \
      ot.OBJ##_mediumId.push_back(muon.get_mediumId());             \
      ot.OBJ##_tightId.push_back(muon.get_tightId());               \
    }                                                               \
}

#define COPY_OPTIONAL_fatjet_list(OBJ)		                    \
  if (ei.OBJ##_list) {				                    \
    for (FatJet & fatjet : ei.OBJ##_list.get()) {		    \
      ot.OBJ##_pt.push_back(fatjet.get_pt());			    \
      ot.OBJ##_eta.push_back(fatjet.get_eta());		            \
      ot.OBJ##_phi.push_back(fatjet.get_phi());		            \
      ot.OBJ##_m.push_back(fatjet.get_mass());		            \
      ot.OBJ##_mSD_UnCorrected.push_back(fatjet.get_massSD_UnCorrected());	\
      ot.OBJ##_area.push_back(fatjet.get_area());		    \
      ot.OBJ##_n2b1.push_back(fatjet.get_n2b1());		    \
      ot.OBJ##_n3b1.push_back(fatjet.get_n3b1());		    \
      ot.OBJ##_rawFactor.push_back(fatjet.get_rawFactor());	    \
      ot.OBJ##_tau1.push_back(fatjet.get_tau1());		    \
      ot.OBJ##_tau2.push_back(fatjet.get_tau2());		    \
      ot.OBJ##_tau3.push_back(fatjet.get_tau3());		    \
      ot.OBJ##_tau4.push_back(fatjet.get_tau4());		    \
      ot.OBJ##_jetId.push_back(fatjet.get_jetId());		    \
      ot.OBJ##_genJetAK8Idx.push_back(fatjet.get_genJetAK8Idx());  \
      ot.OBJ##_hadronFlavour.push_back(fatjet.get_hadronFlavour());  \
      ot.OBJ##_nBHadrons.push_back(fatjet.get_nBHadrons());	       \
      ot.OBJ##_nCHadrons.push_back(fatjet.get_nCHadrons());	       \
      ot.OBJ##_nPFCand.push_back(fatjet.get_nPFCand());	       \
      ot.OBJ##_PNetQCDb.push_back(fatjet.get_PNetQCDb());	    \
      ot.OBJ##_PNetQCDbb.push_back(fatjet.get_PNetQCDbb());	    \
      ot.OBJ##_PNetQCDc.push_back(fatjet.get_PNetQCDc());	    \
      ot.OBJ##_PNetQCDcc.push_back(fatjet.get_PNetQCDcc());	    \
      ot.OBJ##_PNetQCDothers.push_back(fatjet.get_PNetQCDothers()); \
      ot.OBJ##_PNetXbb.push_back(fatjet.get_PNetXbb());		    \
      ot.OBJ##_PNetXcc.push_back(fatjet.get_PNetXcc());		    \
      ot.OBJ##_PNetXqq.push_back(fatjet.get_PNetXqq());		    \
      ot.OBJ##_deepTagMD_H4q.push_back(fatjet.get_deepTagMD_H4q()); \
      ot.OBJ##_deepTagMD_Hbb.push_back(fatjet.get_deepTagMD_Hbb()); \
      ot.OBJ##_deepTagMD_T.push_back(fatjet.get_deepTagMD_T());	    \
      ot.OBJ##_deepTagMD_W.push_back(fatjet.get_deepTagMD_W());	    \
      ot.OBJ##_deepTagMD_Z.push_back(fatjet.get_deepTagMD_Z());	    \
      ot.OBJ##_deepTagMD_bbvsL.push_back(fatjet.get_deepTagMD_bbvsL());     \
      ot.OBJ##_deepTagMD_ccvsL.push_back(fatjet.get_deepTagMD_ccvsL());     \
      ot.OBJ##_deepTag_QCD.push_back(fatjet.get_deepTag_QCD());	            \
      ot.OBJ##_deepTag_QCDothers.push_back(fatjet.get_deepTag_QCDothers()); \
      ot.OBJ##_deepTag_W.push_back(fatjet.get_deepTag_W());	            \
      ot.OBJ##_deepTag_Z.push_back(fatjet.get_deepTag_Z());		    \
      ot.OBJ##_nsubjets.push_back(fatjet.get_subjets().size());	\
      ot.OBJ##_subjet1_pt.push_back(fatjet.get_subjet1_pt());	\
      ot.OBJ##_subjet1_eta.push_back(fatjet.get_subjet1_eta());             \
      ot.OBJ##_subjet1_phi.push_back(fatjet.get_subjet1_phi());	            \
      ot.OBJ##_subjet1_m.push_back(fatjet.get_subjet1_mass());              \
      ot.OBJ##_subjet1_btagDeepB.push_back(fatjet.get_subjet1_btagDeepB()); \
      ot.OBJ##_subjet2_pt.push_back(fatjet.get_subjet2_pt());		    \
      ot.OBJ##_subjet2_eta.push_back(fatjet.get_subjet2_eta());             \
      ot.OBJ##_subjet2_phi.push_back(fatjet.get_subjet2_phi());             \
      ot.OBJ##_subjet2_m.push_back(fatjet.get_subjet2_mass());              \
      ot.OBJ##_subjet2_btagDeepB.push_back(fatjet.get_subjet2_btagDeepB()); \
    }									    \
  }

#define COPY_OPTIONAL_jet_list(OBJ)                              \
  if (ei.OBJ##_list) {                                           \
    for (Jet & jet : ei.OBJ##_list.get()) {                      \
      ot.OBJ##_E.push_back(jet.get_E());                         \
      ot.OBJ##_m.push_back(jet.get_m());                         \
      ot.OBJ##_mRegressed.push_back(jet.get_mRegressed());       \
      ot.OBJ##_pt.push_back(jet.get_pt());                       \
      ot.OBJ##_ptRegressed.push_back(jet.get_ptRegressed());     \
      ot.OBJ##_eta.push_back(jet.get_eta());                     \
      ot.OBJ##_phi.push_back(jet.get_phi());                     \
      ot.OBJ##_signalId.push_back(jet.get_signalId());           \
      ot.OBJ##_higgsIdx.push_back(jet.get_higgsIdx());           \
      ot.OBJ##_genIdx.push_back(jet.get_genIdx());               \
      ot.OBJ##_btag.push_back(jet.get_btag());                   \
      ot.OBJ##_qgl.push_back(jet.get_qgl());                     \
      ot.OBJ##_chEmEF.push_back(jet.get_chEmEF());               \
      ot.OBJ##_chHEF.push_back(jet.get_chHEF());                 \
      ot.OBJ##_neEmEF.push_back(jet.get_neEmEF());               \
      ot.OBJ##_neHEF.push_back(jet.get_neHEF());                 \
      ot.OBJ##_nConstituents.push_back(jet.get_nConstituents()); \
      ot.OBJ##_id.push_back(jet.get_id());                       \
      ot.OBJ##_puid.push_back(jet.get_puid());                   \
    }                                                            \
  }

#define COPY_OPTIONAL_dijet_list(OBJ)                    \
  if (ei.OBJ##_list)                                     \
  {                                                      \
    for (DiJet & dijet : ei.OBJ##_list.get())            \
    {                                                    \
      ot.OBJ##_E.push_back(dijet.E());                   \
      ot.OBJ##_m.push_back(dijet.M());                   \
      ot.OBJ##_pt.push_back(dijet.Pt());                 \
      ot.OBJ##_eta.push_back(dijet.Eta());               \
      ot.OBJ##_phi.push_back(dijet.Phi());               \
      ot.OBJ##_dr.push_back(dijet.dR());                 \
      ot.OBJ##_signalId.push_back(dijet.get_signalId()); \
      ot.OBJ##_2j_score.push_back(dijet.get_2j_score()); \
    }                                                    \
  }

// --- - --- - --- - --- - --- - --- - --- - --- - --- - --- - --- - --- - 

int SkimUtils::appendFromFileList (TChain* chain, string filename)
{
  //cout << "=== inizio parser ===" << endl;
  std::ifstream infile(filename.c_str());
  std::string line;
  int nfiles = 0;
  while (std::getline(infile, line))
    {
      line = line.substr(0, line.find("#", 0)); // remove comments introduced by #
      while (line.find(" ") != std::string::npos) line = line.erase(line.find(" "), 1); // remove white spaces
      while (line.find("\n") != std::string::npos) line = line.erase(line.find("\n"), 1); // remove new line characters
      while (line.find("\r") != std::string::npos) line = line.erase(line.find("\r"), 1); // remove carriage return characters
      if (!line.empty()) // skip empty lines
        {
	  chain->Add(line.c_str());
	  ++nfiles;
        }
    }
  return nfiles;
}


void SkimUtils::fill_output_tree(OutputTree& ot, NanoAODTree& nat, EventInfo& ei)
{

  // set the variables for resonant analysis
  ot.Run      = *ei.Run;
  ot.LumiSec  = *ei.LumiSec;
  ot.Event    = *ei.Event;

  if(ei.n_other_pv)     ot.n_other_pv      = *ei.n_other_pv;
  if(ei.n_pu)           ot.n_pu            = *ei.n_pu;
  if(ei.n_true_int)     ot.n_true_int      = *ei.n_true_int;
  if(ei.rhofastjet_all) ot.rhofastjet_all  = *ei.rhofastjet_all;
  if(ei.lhe_ht)         ot.lhe_ht          = *ei.lhe_ht;
  if(ei.n_jet)          ot.n_jet           = *ei.n_jet;
  if(ei.n_total_jet)    ot.n_total_jet     = *ei.n_total_jet;
  if(ei.n_genjet)       ot.n_genjet        = *ei.n_genjet;
  if(ei.n_higgs)        ot.n_higgs         = *ei.n_higgs;
  if(ei.n_fatjet)       ot.n_fatjet        = *ei.n_fatjet;
  if(ei.n_genfatjet)    ot.n_genfatjet     = *ei.n_genfatjet;
  if(ei.n_ele)          ot.n_ele           = *ei.n_ele;
  if(ei.n_muon)         ot.n_muon          = *ei.n_muon;
  
  if(ei.b_6j_score)     ot.b_6j_score      = *ei.b_6j_score;
  if(ei.b_3d_score)     ot.b_3d_score      = *ei.b_3d_score;

  COPY_OPTIONAL_ele_list(ele);
  COPY_OPTIONAL_muon_list(muon);
  COPY_OPTIONAL_jet_list(jet);
  COPY_OPTIONAL_fatjet_list(fatjet);

  if (ei.genjet_list) {
    for (GenJet& jet : ei.genjet_list.get()) {
      ot.genjet_E.push_back( jet.get_E() );	    
      ot.genjet_m.push_back( jet.get_m() );		
      ot.genjet_pt.push_back( jet.get_pt() );		
      ot.genjet_eta.push_back( jet.get_eta() );		
      ot.genjet_phi.push_back( jet.get_phi() );		
      ot.genjet_partonFlav.push_back( jet.get_partonFlav() );
      ot.genjet_hadronFlav.push_back( jet.get_hadronFlav() );
      ot.genjet_signalId.push_back( jet.get_signalId() );
      ot.genjet_recoIdx.push_back( jet.get_recoIdx() );
    }
  }
  
  if (ei.genfatjet_list) {
    for (GenJetAK8& fatjet : ei.genfatjet_list.get()) {
      ot.genfatjet_E.push_back( fatjet.get_E() );
      ot.genfatjet_m.push_back( fatjet.get_m() );
      ot.genfatjet_pt.push_back( fatjet.get_pt() );
      ot.genfatjet_eta.push_back( fatjet.get_eta() );
      ot.genfatjet_phi.push_back( fatjet.get_phi() );
      ot.genfatjet_signalId.push_back( fatjet.get_signalId() );
      ot.genfatjet_recoIdx.push_back( fatjet.get_recoIdx() );
      ot.genfatjet_hadronFlav.push_back( fatjet.get_hadronFlav() );
      ot.genfatjet_partonFlav.push_back( fatjet.get_partonFlav() );
    }
  }

  if (ei.event_shapes) {
    ot.sphericity   = ei.event_shapes.get().sphericity;
    ot.sphericity_t = ei.event_shapes.get().transverse_sphericity;
    ot.aplanarity   = ei.event_shapes.get().aplanarity;
  }

  if (ei.dijet_list) {

    ot.n_dijet = ei.dijet_list.get().size();
    for (DiJet &dijet : ei.dijet_list.get())
    {
      ot.dijet_m.push_back(dijet.M());                   
      ot.dijet_pt.push_back(dijet.Pt());                 
      ot.dijet_eta.push_back(dijet.Eta());               
      ot.dijet_phi.push_back(dijet.Phi());               
      ot.dijet_dr.push_back(dijet.dR());
      ot.dijet_score.push_back(dijet.get_param("score", 0));
      ot.dijet_signalId.push_back(dijet.get_signalId());
      ot.dijet_j1Idx.push_back(dijet.get_j1Idx());
      ot.dijet_j2Idx.push_back(dijet.get_j2Idx());
    }
  }


  COPY_OPTIONAL_m_pt_eta_phi_p4(gen_X_fc);
  COPY_OPTIONAL_m_pt_eta_phi_p4(gen_X);
  
  // Start Gen 6B Objects
  COPY_OPTIONAL_m_pt_eta_phi_p4(gen_Y);
  COPY_OPTIONAL_m_pt_eta_phi_p4(gen_HX);
  COPY_OPTIONAL_m_pt_eta_phi_p4(gen_H1);
  COPY_OPTIONAL_m_pt_eta_phi_p4(gen_H2);

  COPY_OPTIONAL_m_pt_eta_phi_p4(gen_HX_b1);
  COPY_OPTIONAL_m_pt_eta_phi_p4(gen_HX_b2);
  COPY_OPTIONAL_m_pt_eta_phi_p4(gen_H1_b1);
  COPY_OPTIONAL_m_pt_eta_phi_p4(gen_H1_b2);
  COPY_OPTIONAL_m_pt_eta_phi_p4(gen_H2_b1);
  COPY_OPTIONAL_m_pt_eta_phi_p4(gen_H2_b2);

  COPY_OPTIONAL_m_pt_eta_phi_p4(gen_HX_b1_genjet);
  COPY_OPTIONAL_m_pt_eta_phi_p4(gen_HX_b2_genjet);
  COPY_OPTIONAL_m_pt_eta_phi_p4(gen_H1_b1_genjet);
  COPY_OPTIONAL_m_pt_eta_phi_p4(gen_H1_b2_genjet);
  COPY_OPTIONAL_m_pt_eta_phi_p4(gen_H2_b1_genjet);
  COPY_OPTIONAL_m_pt_eta_phi_p4(gen_H2_b2_genjet);

  COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_p4(gen_HX_b1_recojet);
  COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_p4(gen_HX_b2_recojet);
  COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_p4(gen_H1_b1_recojet);
  COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_p4(gen_H1_b2_recojet);
  COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_p4(gen_H2_b1_recojet);
  COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_p4(gen_H2_b2_recojet);
  // End Gen 6B Objects

  // Start Gen 8B Objects
  COPY_OPTIONAL_m_pt_eta_phi_p4(gen_Y1);
  COPY_OPTIONAL_m_pt_eta_phi_p4(gen_Y2);
  COPY_OPTIONAL_m_pt_eta_phi_p4(gen_H1Y1);
  COPY_OPTIONAL_m_pt_eta_phi_p4(gen_H2Y1);
  COPY_OPTIONAL_m_pt_eta_phi_p4(gen_H1Y2);
  COPY_OPTIONAL_m_pt_eta_phi_p4(gen_H2Y2);

  COPY_OPTIONAL_m_pt_eta_phi_p4(gen_H1Y1_b1);
  COPY_OPTIONAL_m_pt_eta_phi_p4(gen_H1Y1_b2);
  COPY_OPTIONAL_m_pt_eta_phi_p4(gen_H2Y1_b1);
  COPY_OPTIONAL_m_pt_eta_phi_p4(gen_H2Y1_b2);
  COPY_OPTIONAL_m_pt_eta_phi_p4(gen_H1Y2_b1);
  COPY_OPTIONAL_m_pt_eta_phi_p4(gen_H1Y2_b2);
  COPY_OPTIONAL_m_pt_eta_phi_p4(gen_H2Y2_b1);
  COPY_OPTIONAL_m_pt_eta_phi_p4(gen_H2Y2_b2);
  
  COPY_OPTIONAL_m_pt_eta_phi_p4(gen_H1Y1_b1_genjet);
  COPY_OPTIONAL_m_pt_eta_phi_p4(gen_H1Y1_b2_genjet);
  COPY_OPTIONAL_m_pt_eta_phi_p4(gen_H2Y1_b1_genjet);
  COPY_OPTIONAL_m_pt_eta_phi_p4(gen_H2Y1_b2_genjet);
  COPY_OPTIONAL_m_pt_eta_phi_p4(gen_H1Y2_b1_genjet);
  COPY_OPTIONAL_m_pt_eta_phi_p4(gen_H1Y2_b2_genjet);
  COPY_OPTIONAL_m_pt_eta_phi_p4(gen_H2Y2_b1_genjet);
  COPY_OPTIONAL_m_pt_eta_phi_p4(gen_H2Y2_b2_genjet);

  COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_DeepJet_p4(gen_H1Y1_b1_recojet);
  COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_DeepJet_p4(gen_H1Y1_b2_recojet);
  COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_DeepJet_p4(gen_H2Y1_b1_recojet);
  COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_DeepJet_p4(gen_H2Y1_b2_recojet);
  COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_DeepJet_p4(gen_H1Y2_b1_recojet);
  COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_DeepJet_p4(gen_H1Y2_b2_recojet);
  COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_DeepJet_p4(gen_H2Y2_b1_recojet);
  COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_DeepJet_p4(gen_H2Y2_b2_recojet);
  // End Gen 8B Objects

  if (ei.gen_bs_N_reco_match)        ot.gen_bs_N_reco_match        = *ei.gen_bs_N_reco_match;
  if (ei.gen_bs_N_reco_match_in_acc) ot.gen_bs_N_reco_match_in_acc = *ei.gen_bs_N_reco_match_in_acc;
  if (ei.gen_bs_match_recojet_minv)        ot.gen_bs_match_recojet_minv        = *ei.gen_bs_match_recojet_minv;
  if (ei.gen_bs_match_in_acc_recojet_minv) ot.gen_bs_match_in_acc_recojet_minv = *ei.gen_bs_match_in_acc_recojet_minv;

  COPY_OPTIONAL_m_pt_eta_phi_p4(X);
  // Start Reco 6B Objects
  COPY_OPTIONAL_m_pt_eta_phi_p4(Y);
  COPY_OPTIONAL_m_pt_eta_phi_p4(HX);
  COPY_OPTIONAL_m_pt_eta_phi_p4(H1);
  COPY_OPTIONAL_m_pt_eta_phi_p4(H2);

  COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_DeepJet_p4(HX_b1);
  COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_DeepJet_p4(HX_b2);
  COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_DeepJet_p4(H1_b1);
  COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_DeepJet_p4(H1_b2);
  COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_DeepJet_p4(H2_b1);
  COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_DeepJet_p4(H2_b2);

  if (ei.HX_b1_genHflag)  ot.HX_b1_genHflag  = *ei.HX_b1_genHflag;
  if (ei.HX_b2_genHflag)  ot.HX_b2_genHflag  = *ei.HX_b2_genHflag;
  if (ei.H1_b1_genHflag) ot.H1_b1_genHflag = *ei.H1_b1_genHflag;
  if (ei.H1_b2_genHflag) ot.H1_b2_genHflag = *ei.H1_b2_genHflag;
  if (ei.H2_b1_genHflag) ot.H2_b1_genHflag = *ei.H2_b1_genHflag;
  if (ei.H2_b2_genHflag) ot.H2_b2_genHflag = *ei.H2_b2_genHflag;
  // End Reco 6B Objects

  // Start Reco 8B Objects
  COPY_OPTIONAL_m_pt_eta_phi_p4(Y1);
  COPY_OPTIONAL_m_pt_eta_phi_p4(Y2);
  COPY_OPTIONAL_m_pt_eta_phi_score_p4(H1Y1);
  COPY_OPTIONAL_m_pt_eta_phi_score_p4(H2Y1);
  COPY_OPTIONAL_m_pt_eta_phi_score_p4(H1Y2);
  COPY_OPTIONAL_m_pt_eta_phi_score_p4(H2Y2);

  COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_DeepJet_score_p4(H1Y1_b1);
  COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_DeepJet_score_p4(H1Y1_b2);
  COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_DeepJet_score_p4(H2Y1_b1);
  COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_DeepJet_score_p4(H2Y1_b2);
  COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_DeepJet_score_p4(H1Y2_b1);
  COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_DeepJet_score_p4(H1Y2_b2);
  COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_DeepJet_score_p4(H2Y2_b1);
  COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_DeepJet_score_p4(H2Y2_b2);

  if (ei.H1Y1_b1_genHflag)  ot.H1Y1_b1_genHflag  = *ei.H1Y1_b1_genHflag;
  if (ei.H1Y1_b2_genHflag)  ot.H1Y1_b2_genHflag  = *ei.H1Y1_b2_genHflag;
  if (ei.H2Y1_b1_genHflag)  ot.H2Y1_b1_genHflag  = *ei.H2Y1_b1_genHflag;
  if (ei.H2Y1_b2_genHflag)  ot.H2Y1_b2_genHflag  = *ei.H2Y1_b2_genHflag;
  if (ei.H1Y2_b1_genHflag)  ot.H1Y2_b1_genHflag  = *ei.H1Y2_b1_genHflag;
  if (ei.H1Y2_b2_genHflag)  ot.H1Y2_b2_genHflag  = *ei.H1Y2_b2_genHflag;
  if (ei.H2Y2_b1_genHflag)  ot.H2Y2_b1_genHflag  = *ei.H2Y2_b1_genHflag;
  if (ei.H2Y2_b2_genHflag)  ot.H2Y2_b2_genHflag  = *ei.H2Y2_b2_genHflag;

  if (ei.n_loose_btag) ot.n_loose_btag = *ei.n_loose_btag;
  if (ei.n_medium_btag) ot.n_medium_btag = *ei.n_medium_btag;
  if (ei.n_tight_btag) ot.n_tight_btag = *ei.n_tight_btag;
  if (ei.btagavg) ot.btagavg = *ei.btagavg;

  if (ei.quadh_score) ot.quadh_score = *ei.quadh_score;
  // End Reco 8B Objects

  if (ei.nfound_all) ot.nfound_all = *ei.nfound_all;
  if (ei.nfound_all_h) ot.nfound_all_h = *ei.nfound_all_h;
  if (ei.nfound_presel) ot.nfound_presel = *ei.nfound_presel;
  if (ei.nfound_presel_h) ot.nfound_presel_h = *ei.nfound_presel_h;
  if (ei.nfound_select) ot.nfound_select = *ei.nfound_select;
  if (ei.nfound_select_h) ot.nfound_select_h = *ei.nfound_select_h;
  if (ei.nfound_paired_h) ot.nfound_paired_h = *ei.nfound_paired_h;
  if (ei.nfound_select_y) ot.nfound_select_y = *ei.nfound_select_y;
  if (ei.nfound_paired_y) ot.nfound_paired_y = *ei.nfound_paired_y;

  //COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_DeepJet_p4(bjet1);
  //COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_DeepJet_p4(bjet2);

  // must check validity of reader because this is not defined in data
  //if (ei.bjet1 && nat.Jet_hadronFlavour.IsValid())
  //  ot.bjet1_hadflav = get_property(ei.bjet1.get(), Jet_hadronFlavour);

  //if (ei.bjet2 && nat.Jet_hadronFlavour.IsValid())
  //  ot.bjet2_hadflav = get_property(ei.bjet2.get(), Jet_hadronFlavour);

  if (ei.btagSF_WP_M) ot.btagSF_WP_M = *ei.btagSF_WP_M;

  // fill the tree
  ot.fill();

}

void SkimUtils::init_gen_weights(OutputTree &ot, NormWeightTree &nwt)
{
  // create userfloats for systematics read from file directly
  auto& gen_weight   = nwt.get_gen_weight();
  auto& pu_weight    = nwt.get_pu_weight();
  auto& pdf_weight   = nwt.get_pdf_weight();
  auto& scale_weight = nwt.get_scale_weight();
  auto& ps_weight    = nwt.get_ps_weight();

  ot.declareUserFloatBranch(gen_weight.name, 1.0);
  for (auto n : gen_weight.syst_name)
    ot.declareUserFloatBranch(n, 1.0);

  ot.declareUserFloatBranch(pu_weight.name, 1.0);
  for (auto n : pu_weight.syst_name)
    ot.declareUserFloatBranch(n, 1.0);

  ot.declareUserFloatBranch(pdf_weight.name, 1.0);
  for (auto n : pdf_weight.syst_name)
    ot.declareUserFloatBranch(n, 1.0);

  ot.declareUserFloatBranch(scale_weight.name, 1.0);
  for (auto n : scale_weight.syst_name)
    ot.declareUserFloatBranch(n, 1.0);

  ot.declareUserFloatBranch(ps_weight.name, 1.0);
  for (auto n : ps_weight.syst_name)
    ot.declareUserFloatBranch(n, 1.0);
}

void SkimUtils::copy_gen_weights(OutputTree &ot, NormWeightTree &nwt)
{
  // copy the values and the structures for systematics
  auto& gen_weight   = nwt.get_gen_weight();
  auto& pu_weight    = nwt.get_pu_weight();
  auto& pdf_weight   = nwt.get_pdf_weight();
  auto& scale_weight = nwt.get_scale_weight();
  auto& ps_weight    = nwt.get_ps_weight();

  ot.userFloat(gen_weight.name) = gen_weight.w;
  for (uint iw = 0; iw < gen_weight.syst_name.size(); ++iw){
    auto n = gen_weight.syst_name.at(iw);
    ot.userFloat(n) = gen_weight.syst_val.at(iw);
  }

  ot.userFloat(pu_weight.name) = pu_weight.w;
  for (uint iw = 0; iw < pu_weight.syst_name.size(); ++iw){
    auto n = pu_weight.syst_name.at(iw);
    ot.userFloat(n) = pu_weight.syst_val.at(iw);
  }   

  ot.userFloat(pdf_weight.name) = pdf_weight.w;
  for (uint iw = 0; iw < pdf_weight.syst_name.size(); ++iw){
    auto n = pdf_weight.syst_name.at(iw);
    ot.userFloat(n) = pdf_weight.syst_val.at(iw);
  }

  ot.userFloat(scale_weight.name) = scale_weight.w;
  for (uint iw = 0; iw < scale_weight.syst_name.size(); ++iw){
    auto n = scale_weight.syst_name.at(iw);
    ot.userFloat(n) = scale_weight.syst_val.at(iw);
  }

  ot.userFloat(ps_weight.name) = ps_weight.w;
  for (uint iw = 0; iw < ps_weight.syst_name.size(); ++iw){
    auto n = ps_weight.syst_name.at(iw);
    ot.userFloat(n) = ps_weight.syst_val.at(iw);
  }
}

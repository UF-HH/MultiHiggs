#include "BtagSF.h"
#include <iostream>

using namespace std;

// void BtagSF::init_reader(std::string tagger, std::string SFfile, std::vector<std::string> udsg_c_b_meas)
void BtagSF::init_reader(std::string tagger, std::string SFfile)
{
  cout << "[INFO] ... BtagSF : loading for tagger " << tagger << " from " << SFfile << endl;
  BTagCalibration btagCalibration(tagger, SFfile);

  // WP_meas_[btagFlav::udsg] = udsg_c_b_meas.at(btagFlav::udsg);
  // WP_meas_[btagFlav::c]    = udsg_c_b_meas.at(btagFlav::c);
  // WP_meas_[btagFlav::b]    = udsg_c_b_meas.at(btagFlav::b);
  // cout << "[INFO] ... BtagSF : for udsg/c/b loading measurements: " << WP_meas_[btagFlav::udsg] << "/" << WP_meas_[btagFlav::c] << "/" << WP_meas_[btagFlav::b] << endl;

  // btcr_[btagWP::loose]  = std::unique_ptr<BTagCalibrationReader> (new BTagCalibrationReader(BTagEntry::OP_LOOSE,  "central", {"up", "down"}));
  // btcr_[btagWP::medium] = std::unique_ptr<BTagCalibrationReader> (new BTagCalibrationReader(BTagEntry::OP_MEDIUM, "central", {"up", "down"}));
  // btcr_[btagWP::tight]  = std::unique_ptr<BTagCalibrationReader> (new BTagCalibrationReader(BTagEntry::OP_TIGHT,  "central", {"up", "down"}));

  btcr_[btagWP::loose]  = std::unique_ptr<BTagCalibrationReader> (new BTagCalibrationReader(BTagEntry::OP_LOOSE,  "central", {"up", "down"}));
  btcr_[btagWP::medium] = std::unique_ptr<BTagCalibrationReader> (new BTagCalibrationReader(BTagEntry::OP_MEDIUM, "central", {"up", "down"}));
  btcr_[btagWP::tight]  = std::unique_ptr<BTagCalibrationReader> (new BTagCalibrationReader(BTagEntry::OP_TIGHT,  "central", {"up", "down"}));
  
  btcr_[btagWP::loose]->load(btagCalibration, BTagEntry::FLAV_UDSG, "incl");
  btcr_[btagWP::loose]->load(btagCalibration, BTagEntry::FLAV_C   , "comb");
  btcr_[btagWP::loose]->load(btagCalibration, BTagEntry::FLAV_B   , "comb");

  btcr_[btagWP::medium]->load(btagCalibration, BTagEntry::FLAV_UDSG, "incl");
  btcr_[btagWP::medium]->load(btagCalibration, BTagEntry::FLAV_C   , "comb");
  btcr_[btagWP::medium]->load(btagCalibration, BTagEntry::FLAV_B   , "comb");

  btcr_[btagWP::tight]->load(btagCalibration, BTagEntry::FLAV_UDSG, "incl");
  btcr_[btagWP::tight]->load(btagCalibration, BTagEntry::FLAV_C   , "comb");
  btcr_[btagWP::tight]->load(btagCalibration, BTagEntry::FLAV_B   , "comb");

  // btcr_[btagWP::loose]->load(btagCalibration, BTagEntry::FLAV_UDSG, WP_meas_[btagFlav::udsg]);
  // btcr_[btagWP::loose]->load(btagCalibration, BTagEntry::FLAV_C   , WP_meas_[btagFlav::c]);
  // btcr_[btagWP::loose]->load(btagCalibration, BTagEntry::FLAV_B   , WP_meas_[btagFlav::b]);

  // btcr_[btagWP::medium]->load(btagCalibration, BTagEntry::FLAV_UDSG, WP_meas_[btagFlav::udsg]);
  // btcr_[btagWP::medium]->load(btagCalibration, BTagEntry::FLAV_C   , WP_meas_[btagFlav::c]);
  // btcr_[btagWP::medium]->load(btagCalibration, BTagEntry::FLAV_B   , WP_meas_[btagFlav::b]);

  // btcr_[btagWP::tight]->load(btagCalibration, BTagEntry::FLAV_UDSG, WP_meas_[btagFlav::udsg]);
  // btcr_[btagWP::tight]->load(btagCalibration, BTagEntry::FLAV_C   , WP_meas_[btagFlav::c]);
  // btcr_[btagWP::tight]->load(btagCalibration, BTagEntry::FLAV_B   , WP_meas_[btagFlav::b]);
}

void BtagSF::set_WPs(double WP_L, double WP_M, double WP_T)
{
  WP_[btagWP::loose]  = WP_L;
  WP_[btagWP::medium] = WP_M;
  WP_[btagWP::tight]  = WP_T;   
  cout << "[INFO] ... BtagSF : WP used are (L/M/T) : " << WP_[btagWP::loose] << "/" << WP_[btagWP::medium] << "/" << WP_[btagWP::tight] << endl;
}

// FIXME: Needs to be corrected based on: https://twiki.cern.ch/twiki/bin/viewauth/CMS/BTagSFMethods#1a_Event_reweighting_using_scale

// FIXME: systematics can be sped up by reducing the number of event loops (just do one loop and precompute all systematics)
// void BtagSF::get_SF_allJetsPassWP (const std::vector<Jet>& jets, btagWP WP, std::string syst = "", bool syst_up = true)
double BtagSF::get_SF_allJetsPassWP(const std::vector<Jet>& jets, btagWP WP)
{
  double SF = 1.0;
  for (const auto& jet : jets)
    {
      int jetFlavour = abs(get_property(jet, Jet_hadronFlavour));
      
      BTagEntry::JetFlavor jf = BTagEntry::FLAV_UDSG;
      if (jetFlavour == 5)
	jf = BTagEntry::FLAV_B;
      else if (jetFlavour == 4)
	jf = BTagEntry::FLAV_C;
      
      std::cout << "btag SF (central) ="<<btcr_[WP] -> eval_auto_bounds("central", jf, jet.P4().Eta(), jet.P4().Pt())<<std::endl;
      std::cout << "btag SF (up)      ="<<btcr_[WP] -> eval_auto_bounds("up", jf, jet.P4().Eta(), jet.P4().Pt())<<std::endl;
      std::cout << "btag SF (down)    ="<<btcr_[WP] -> eval_auto_bounds("down", jf, jet.P4().Eta(), jet.P4().Pt())<<std::endl;
      
      double thisSF = btcr_[WP] -> eval_auto_bounds("central", jf, jet.P4().Eta(), jet.P4().Pt());
      SF *= thisSF;
    }
  return SF;
}

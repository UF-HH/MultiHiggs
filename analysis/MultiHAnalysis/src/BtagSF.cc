#include "BtagSF.h"
#include <iostream>

using namespace std;

// void BtagSF::init_reader(std::string tagger, std::string SFfile, std::vector<std::string> udsg_c_b_meas)
void BtagSF::init_reader(std::string tagger, std::string SFfile, OutputTree& ot)
{
  cout << "[INFO] ... BtagSF : loading for tagger " << tagger << " from " << SFfile << endl;
  BTagCalibration btagCalibration(tagger, SFfile);

  bool wp_found = SFfile.find("wp") != string::npos;
  reshaping_found = SFfile.find("reshaping") != string::npos;


  if (wp_found)
  {
    cout << "[INFO] Using working point scale factor file" << endl;

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
  }
  else if (reshaping_found)
  {
    cout << "[INFO] Using reshaping scale factor file" << endl;

  // // Added by Suzanne on 10/16/2023 for reshaping
  btag_sf_reshaping_full_list_.push_back("central");
  for (string sfunc : btag_sf_reshaping_unc_sources_)
  {
      for (string dir : {"up", "down"})
      {
          string uncname = dir;
          uncname += string("_");
          uncname += sfunc;
          btag_sf_reshaping_full_list_.push_back(uncname);
      }
  }
  for (string sfname : btag_sf_reshaping_full_list_)
  {
    string sfbrname = "bSFshape_";
    sfbrname += sfname;
    ot.declareUserFloatBranch(sfbrname, 1.0);
  }
  btcr_[btagWP::shape]  = std::unique_ptr<BTagCalibrationReader> (new BTagCalibrationReader(BTagEntry::OP_RESHAPING, "central", btag_sf_reshaping_full_list_));
  btcr_[btagWP::shape]->load(btagCalibration,  BTagEntry::FLAV_B,    "iterativefit");
  btcr_[btagWP::shape]->load(btagCalibration,  BTagEntry::FLAV_C,    "iterativefit");
  btcr_[btagWP::shape]->load(btagCalibration,  BTagEntry::FLAV_UDSG, "iterativefit");
  }
  else {
    std::cerr << "ERROR in BtagSF: "
	      << "Filename does not contain 'wp' or 'reshaping'! : " << SFfile << endl;
    throw std::exception();
  }

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

void BtagSF::compute_reshaping_sf(const std::vector<Jet> &jets, NanoAODTree& nat, OutputTree& ot)
{
  for (uint isf = 0; isf < btag_sf_reshaping_full_list_.size(); ++isf)
    {
        // cout << ".. btag_sf_reshaping_full_list_[" << isf << "]" << endl;
        string sfname = btag_sf_reshaping_full_list_.at(isf);

        double bSF = 1.0;
        for (const auto& jet : jets)
        {
            int jetFlavour = abs(get_property(jet, Jet_hadronFlavour));
            
            BTagEntry::JetFlavor jf = BTagEntry::FLAV_UDSG;
            if (jetFlavour == 5)
                jf = BTagEntry::FLAV_B;
            else if (jetFlavour == 4)
                jf = BTagEntry::FLAV_C;

            double b_score = get_property(jet, Jet_btagDeepFlavB);

            double aeta = std::abs(jet.P4().Eta());
            double pt   = jet.P4().Pt();

            double w = btcr_[btagWP::shape]->eval_auto_bounds(sfname, jf, aeta, pt, b_score);

            // if (jetFlavour == 4)
              // cout << "Hadron flavor is 4, " << sfname << " = " << w << endl;
            
            // 0 is the default value for a missing line in the .csv file (e.g., an uncertainty available only for one flavour but not the others)
            // but there is not a way to check if the value was available or the default was returned
            // (who developed this horrible tool?)
            // in that case, replace the syst-varied SF with the nominal one for this jet
            if (b_score >= 0 && w == 0)
                w = btcr_[btagWP::shape]->eval_auto_bounds("central", jf, aeta, pt, b_score);

            bSF *= w; // the SF is the product over the preselected jets - IMPORTANT : must be before cuts on b tag! (because it is a reshape)
        }

        // save in output
        string sfbrname = "bSFshape_";
        sfbrname += sfname;
        // cout << "sfbrname = " << sfbrname << endl;
        // cout << "bSF = " << bSF << endl;
        ot.userFloat(sfbrname) = bSF;

        // cout << ".. branch saved to OT" << endl;
        
        
        // ot.userFloat(sfbrname) = bSF; // the product of the 4 b tag SF (*before* cuts) is my weight

        // store partial sum
        // btag_sf_reshaping_full_list_sumw_.at(isf) += (bSF * event_weight); // to ensure normalisation I store bSF times weight
        // btag_sf_reshaping_full_list_sumw_.at(isf) += bSF;
    }
    // btag_sf_reshaping_sumw_denom_ += event_weight;
}
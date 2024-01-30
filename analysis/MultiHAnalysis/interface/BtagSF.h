#ifndef BTAGSF_H
#define BTAGSF_H

#include <memory>
#include <vector>
#include <tuple>
#include <string>
#include "BTagCalibrationStandalone.h"
#include "Jet.h"
#include "OutputTree.h"

class BtagSF{
    
public:
  enum btagWP {
    loose  = 0,
    medium = 1,
    tight  = 2,
    shape  = 3,
    N_WP   = 4,
  };

  enum btagFlav {
    udsg    = 0,
    c       = 1,
    b       = 2,
    N_FLAV  = 3,
  };

  const std::vector<std::string> btag_sf_reshaping_unc_sources_ = {"jes", "jesAbsolute", "jesBBEC1", "jesEC2", "jesFlavorQCD", "jesHF", "jesRelativeBal", "jesRelativeSample", "hf", "lf", "lfstats1", "lfstats2", "hfstats1", "hfstats2"}; // x {up, down} in the code
  std::vector<std::string> btag_sf_reshaping_full_list_;
  std::vector<double> btag_sf_reshaping_full_list_sumw_;

  BtagSF(){};
  ~BtagSF(){};

  // void init_reader(std::string tagger, std::string SFfile, std::vector<std::string> udsg_c_b_meas = {"incl", "comb", "comb"});
  void init_reader(std::string tagger, std::string SFfile, OutputTree& ot);
  void set_WPs(double WP_L, double WP_M, double WP_T);
  double get_WP(btagWP WP) {return WP_[WP];}

  // get the SF for all jets in jets passing the specified WP (== product of the SFs)
  // if non-emtpy syst, the SF is calculated with the measurement "syst" shifted up/down if syst_up
  // void get_SF_allJetsPassWP (const std::vector<Jet>& jets, btagWP WP, std::string syst = "", bool syst_up = true);
  double get_SF_allJetsPassWP (const std::vector<Jet>& jets, btagWP WP);
  void compute_reshaping_sf(const std::vector<Jet> &jets, NanoAODTree& nat, OutputTree &ot);

  bool reshaping_found;

private:
  // every WP must have its reader
  // std::unique_ptr<BTagCalibrationReader> btcr_L_;
  // std::unique_ptr<BTagCalibrationReader> btcr_M_;
  // std::unique_ptr<BTagCalibrationReader> btcr_T_;

  // double WP_L_;
  // double WP_M_;
  // double WP_T_;

  std::unique_ptr<BTagCalibrationReader> btcr_[btagWP::N_WP];
  double WP_[btagWP::N_WP];
  // std::unordered_map<std::string, std::vector<btagFlav>> WP_meas_to_flavs_; // maps the name of the measurement to the b flavours that use it
};

#endif

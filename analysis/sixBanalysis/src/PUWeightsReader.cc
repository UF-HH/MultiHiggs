#include "PUWeightsReader.h"
#include "TFile.h"
#include "TH1D.h"
#include <algorithm>
#include <iostream>

void PUWeightsReader::init_data(std::string filename, std::string name_PU_w, std::string name_PU_w_up, std::string name_PU_w_do)
{
  TFile* fIn = TFile::Open(filename.c_str());
  TH1* h_w    = (TH1*) fIn->Get(name_PU_w.c_str());
  TH1* h_w_up = (TH1*) fIn->Get(name_PU_w_up.c_str());
  TH1* h_w_do = (TH1*) fIn->Get(name_PU_w_do.c_str());

  // binning is read from nominal - user *must* make sure the 3 histograms are coherent
  for (int i = 1; i <= h_w->GetNbinsX(); ++i)
    {
      double edge = h_w    -> GetBinLowEdge(i);
      double w    = h_w    -> GetBinContent(i);
      double w_up = h_w_up -> GetBinContent(i);
      double w_do = h_w_do -> GetBinContent(i);
      bin_edges_.push_back(edge);
      PU_w_.push_back(w);
      PU_w_up_.push_back(w_up);
      PU_w_do_.push_back(w_do);
    }
  // finally, add last edge (Nweights = Nedges-1)
  bin_edges_.push_back(h_w->GetBinContent(h_w->GetNbinsX()+1));
  fIn->Close();
}

int PUWeightsReader::find_bin(double val)
{
  auto it = std::upper_bound(bin_edges_.begin(), bin_edges_.end(), val);
  if (it == bin_edges_.begin())
    return 0; // underflow
  if (it == bin_edges_.end())
    return bin_edges_.size()-2; // overflow - remember: -2 because Nbins = nedges-1 
				     return distance(bin_edges_.begin(), it) -1;
}

std::tuple<double, double, double> PUWeightsReader::get_weight(double PU)
{
  if (bin_edges_.size() < 2){ // one needs at least 2 bins edges (= 1 single bin)
    std::cout << "[ERROR] : PUWeightsReader : PU corrections were not initialised, edge size is " << bin_edges_.size() << std::endl;
    throw std::runtime_error("PUWeightsReader : checking weights when values not initialised");
  }

  int ibin = find_bin(PU);
  double w = PU_w_.at(ibin);
  double w_up = PU_w_up_.at(ibin);
  double w_do = PU_w_do_.at(ibin);
  return std::make_tuple(w, w_up, w_do);
}

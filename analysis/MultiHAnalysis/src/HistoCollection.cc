#include "HistoCollection.h"

using namespace std;

void Histogram::Fill(float value, NormWeightTree& nwt) {
  float genWeight = nwt.get_gen_weight().w;
  if (genWeight == 0)
    genWeight = 1;
  TH1D::Fill(value, genWeight);
}

Histogram& HistoCollection::get(TString name, TString title, int nbins, double xlow, double xhi) {
  if (histos.find(name) == histos.end()) {
    histos[name] = Histogram(name, title, nbins, xlow, xhi);
  }
  return histos[name];
}

void HistoCollection::write(TFile& output) {
  output.cd();
  for (auto const& [key, histo] : histos) {
    histo.Write();
  }
}
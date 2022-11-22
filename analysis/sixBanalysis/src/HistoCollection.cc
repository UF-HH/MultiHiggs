#include "HistoCollection.h"

using namespace std;

TH1D& HistoCollection::get(TString name, TString title, int nbins, double xlow, double xhi) 
{ 
  if (histos.find(name) == histos.end())  {
    histos[name] = TH1D(name, title, nbins, xlow, xhi);
  }
  return histos[name];
}

void HistoCollection::write(TFile& output)
{
  output.cd();
  for (auto const& [key, histo] : histos)
  {
    histo.Write();
  }
}
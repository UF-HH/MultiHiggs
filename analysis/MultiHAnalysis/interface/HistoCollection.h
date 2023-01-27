#ifndef HISTOCOLLECTION_H
#define HISTOCOLLECTION_H

#include <iostream>
#include <string>
#include <iomanip>
#include <any>
#include <chrono>
#include <map>

#include "TFile.h"
#include "TROOT.h"
#include "TH1F.h"
#include "TString.h"
#include "NormWeightTree.h"

struct Histogram : public TH1D {
  Histogram() : TH1D(){};
  Histogram(TString name, TString title, int nbins, double xlow, double xhi) : TH1D(name, title, nbins, xlow, xhi){};
  void Fill(float value, NormWeightTree& nwt);
};

class HistoCollection {
public:
  HistoCollection(){};
  Histogram& get(TString name, TString title, int nbins, double xlow, double xhi);
  void write(TFile& output);

private:
  std::map<TString, Histogram> histos;
};

#endif  // HISTOCOLLECTION_H
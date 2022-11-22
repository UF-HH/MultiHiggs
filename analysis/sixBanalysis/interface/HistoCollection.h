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

class HistoCollection {
public:
  HistoCollection() {};
  TH1D& get(TString name, TString title, int nbins, double xlow, double xhi);
  void write(TFile& output);

private:
  std::map<TString, TH1D> histos;
};

#endif // HISTOCOLLECTION_H
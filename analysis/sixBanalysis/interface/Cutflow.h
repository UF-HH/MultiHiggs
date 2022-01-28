#ifndef CUTFLOW_H
#define CUTFLOW_H

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

class Cutflow {
public:
  Cutflow(TString name="h_cutflow",TString title="Selection Cutflow");
  void add(TString entry,float value=1);
  void write(TFile& output);
private:
  TString _name;
  TString _title;
  std::vector<TString>    _entries;
  std::map<TString,float> _cutflow;
};

#endif // CUTFLOW_H

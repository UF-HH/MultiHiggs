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

#include "Cutflow.h"

Cutflow::Cutflow(TString name,TString title)
{
  _name = name;
  _title = title;
}

void Cutflow::add(TString entry,float value)
{
  if (_cutflow.count(entry) == 0) {
    _entries.push_back(entry);
    _cutflow[entry] = 0;
  }
  _cutflow[entry] += value;
}

void Cutflow::write(TFile& output)
{
  output.cd();
  unsigned int nentries = _entries.size();
  TH1F cutflow(_name,_title,nentries,0,nentries);
  for (unsigned int i = 0; i < nentries; i++)
    {
      TString entry = _entries[i];
      float value = _cutflow[entry];

      cutflow.SetBinContent(i+1,value);
      cutflow.GetXaxis()->SetBinLabel(i+1,entry);
    }

  cutflow.Write();
}

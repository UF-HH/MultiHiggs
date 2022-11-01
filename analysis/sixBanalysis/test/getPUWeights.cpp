/*
DESCRIPTION:
Calculates the PU weights for each MC sample passed as input and stores the weights in a ROOT file under weights.

USAGE:
./bin/getPUWeights.exe --realPU weights/Collision18PileupHistogram.root --input inputFiles/2016ResonantDiHiggs4BDataSets/MCSignal_BulkGravTohhTohbbhbb_narrow_M-1000_13TeV-madgraph.txt

LAST USED:

*/
#include <iostream>
#include <string>
#include <iomanip>
#include <boost/program_options.hpp>
namespace po = boost::program_options;

#include "SkimUtils.h"
namespace su = SkimUtils;

#include "TFile.h"
#include "TH1.h"

using namespace std;

int main(int argc, char** argv)
{
  po::options_description desc("Skim options");
  desc.add_options()
    ("help", "produce help message")
    ("realPU", po::value<string>()->required(), "File containing real PU distribution")
    ("input" , po::value<string>()->required(), "input file with MC file list")
    // optional
    ("output", po::value<string>(), "output file with weight histogram, if not specified weights/<input>_PUweights.root")
    ;
  
  po::variables_map opts;
  try {
    po::store(parse_command_line(argc, argv, desc, po::command_line_style::unix_style ^ po::command_line_style::allow_short), opts);
    if (opts.count("help")) {
      cout << desc << "\n";
      return 1;
    }
    po::notify(opts);
  }    
  catch (po::error& e) {
    cerr << "** [ERROR] " << e.what() << endl;
    return 1;
  }
  
  TChain ch("Events");
  int nFiles = su::appendFromFileList(&ch, opts["input"].as<string>());
  
  if (nFiles == 0){
    cerr << "** [ERROR] The input file list contains no files, aborting" << endl;
    return 1;
  }
  cout << "[INFO] ... file list contains " << nFiles << " files" << endl;
  cout << "[INFO] ... creating tree reader" << endl;
  
  //weights for PU
  TFile *realPUFile  = new TFile(opts["realPU"].as<string>().data());
  TH1D* realPU       = (TH1D*) realPUFile->Get("pileup");
  TH1D* realPU_up    = (TH1D*) realPUFile->Get("pileup_up");
  TH1D* realPU_down  = (TH1D*) realPUFile->Get("pileup_down");    
  
  TH1D* puWeight     = (TH1D*) realPU->Clone("PUweights");
  TH1D* puWeight_up  = (TH1D*) realPU_up->Clone("PUweights_up");
  TH1D* puWeight_down= (TH1D*) realPU_down->Clone("PUweights_down");
  
  int nBins     = puWeight->GetNbinsX();
  double binMin = puWeight->GetBinLowEdge(1);
  double binMax = puWeight->GetBinLowEdge(nBins+1);
  
  puWeight     ->Scale(1./puWeight->Integral());
  puWeight_up  ->Scale(1.0/puWeight_up->Integral());
  puWeight_down->Scale(1.0/puWeight_down->Integral());
  
  TH1D *samplePU = new TH1D("samplePU","samplePU", nBins, binMin, binMax);
  
  ch.Draw("Pileup_nTrueInt>>samplePU");
  
  samplePU->Scale(1./samplePU->Integral());
  samplePU->SetDirectory(0);
  
  puWeight->Divide(samplePU);
  puWeight->SetDirectory(0);
  
  //weights for PU up
  puWeight_up->Divide(samplePU);
  puWeight_up->SetDirectory(0);
  
  //weights for PU down
  puWeight_down->Divide(samplePU);
  puWeight_down->SetDirectory(0);
  
  // Close the collision data file
  realPUFile->Close();
  
  std::string outputFileName;
  if(opts.count("output")) outputFileName = opts["output"].as<string>();
  else
    {
      outputFileName = opts["input"].as<string>();
      std::size_t begin = outputFileName.rfind("/");
      if(begin >= outputFileName.length()) begin = 0; //not found
      std::size_t end = outputFileName.rfind(".");
      if(end >= outputFileName.length())
        {
	  cerr << "input file should have an extension!" << endl;
	  return 1;
        }
      outputFileName = outputFileName.substr(begin, end-begin);
      outputFileName = "weights/" + outputFileName + "_PUweights.root";
    }
  
  TFile *outputFile = new TFile(outputFileName.data(),"RECREATE");
  puWeight->Write();
  puWeight_up->Write();
  puWeight_down->Write();
  outputFile->Close();
  
  cout << "[INFO] ... weights saved in " << outputFileName << endl;
  return 1;
}


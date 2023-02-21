#include <iostream>
#include <string>
#include <iomanip>
#include <any>
#include <numeric>
#include <algorithm>

#include <glob.h>

#include <boost/program_options.hpp>
namespace po = boost::program_options;

#include "CfgParser.h"
#include "NanoAODTree.h"
#include "EventInfo.h"
#include "JetTools.h"

#include "SkimUtils.h"
namespace su = SkimUtils;

// #include "OutputTree.h"
#include "jsonLumiFilter.h"

#include "TFile.h"
#include "TROOT.h"
#include "TH1F.h"
#include "TH2D.h"
#include <TTreeReader.h>
#include <TTreeReaderValue.h>
#include <TTreeReaderArray.h>
#include "TEfficiency.h"

using namespace std;


std::vector<string> wplabels = {"total","loose", "medium", "tight"};

std::vector<std::string> split_by_delimiter(std::string input, std::string delimiter) {
  std::vector<std::string> tokens;
  if (input == "")
    return tokens;
  size_t pos = 0;
  while ((pos = input.find(delimiter)) != std::string::npos) {
    tokens.push_back(input.substr(0, pos));
    input.erase(0, pos + delimiter.length());
  }
  tokens.push_back(input);  // last part splitted
  return tokens;
}

std::vector<std::string> glob(const std::string& pattern) {
    // glob struct resides on the stack
    glob_t glob_result;
    memset(&glob_result, 0, sizeof(glob_result));

    // do the glob operation
    int return_value = glob(pattern.c_str(), GLOB_TILDE, NULL, &glob_result);
    if(return_value != 0) {
        globfree(&glob_result);
        stringstream ss;
        ss << "glob() failed with return_value " << return_value << endl;
        throw std::runtime_error(ss.str());
    }

    // collect all the filenames into a std::list<std::string>
    vector<string> filenames;
    for(size_t i = 0; i < glob_result.gl_pathc; ++i) {
        filenames.push_back(string(glob_result.gl_pathv[i]));
    }

    // cleanup
    globfree(&glob_result);

    // done
    return filenames;
}

struct Histos {
    TH1D* h_n_jet;
    TH1D* h_ht_jet;
    TH1D* h_jet_btag;
    TH1D* h_jet_pt;
    TH1D* h_jet_eta;
    TH2D* h_jet_pt_eta;

    Histos(){};
    Histos(TString tag) {
        h_n_jet = new TH1D(tag + "_n_jet", tag + " N jet;N jet;", 15, 0, 15);
        h_ht_jet = new TH1D(tag + "_ht_jet", tag + " Ht jet;Ht jet [GeV];", 30, 100, 1500.0);
        h_jet_btag = new TH1D(tag + "_jet_btag", tag + " jet deepJet;jet deepJet;", 30, 0.0, 1.0);
        h_jet_pt = new TH1D(tag + "_jet_pt", tag + " jet pt;jet pt [GeV];", 30, 20.0, 500.0);
        h_jet_eta = new TH1D(tag + "_jet_eta", tag + " jet #eta;jet #eta;", 30, -2.5, 2.5);
        h_jet_pt_eta =
            new TH2D(tag + "_jet_pt_eta", tag + " jet pt;jet pt [GeV];jet #eta", 30, 20.0, 500.0, 30, -2.5, 2.5);

        h_n_jet->Sumw2();
        h_ht_jet->Sumw2();
        h_jet_btag->Sumw2();
        h_jet_pt->Sumw2();
        h_jet_eta->Sumw2();
        h_jet_pt_eta->Sumw2();
    }

    void Fill(float pt, float eta, float btag, float weight = 1) {
        h_jet_btag->Fill(btag, weight);
        h_jet_pt->Fill(pt, weight);
        h_jet_eta->Fill(eta, weight);
        h_jet_pt_eta->Fill(pt, eta, weight);
    }

    void Write() {
        h_n_jet->Write();
        h_ht_jet->Write();
        h_jet_btag->Write();
        h_jet_pt->Write();
        h_jet_eta->Write();
        h_jet_pt_eta->Write();
    }
};

struct Efficiency {
  TEfficiency* eff_jet_btag;
  TEfficiency* eff_jet_pt;
  TEfficiency* eff_jet_eta;
  TEfficiency* eff_jet_pt_eta;

  Efficiency() {};
  Efficiency(TString tag) {
    eff_jet_btag =   new TEfficiency(tag + "_jet_btag", tag + " jet deepJet;jet deepJet;", 30, 0., 1.0);
    eff_jet_pt =     new TEfficiency(tag + "_jet_pt", tag + " jet pt;jet pt [GeV];", 30, 20.0, 500.0);
    eff_jet_eta =    new TEfficiency(tag + "_jet_eta", tag + " jet #eta;jet #eta;", 30, -2.5, 2.5);
    eff_jet_pt_eta = new TEfficiency(tag + "_jet_pt_eta", tag + " jet pt;jet pt [GeV];jet #eta", 30, 20.0, 500.0, 30, -2.5, 2.5);

    eff_jet_btag->SetStatisticOption(TEfficiency::kFNormal);
    eff_jet_pt->SetStatisticOption(TEfficiency::kFNormal);
    eff_jet_eta->SetStatisticOption(TEfficiency::kFNormal);
    eff_jet_pt_eta->SetStatisticOption(TEfficiency::kFNormal);
  }

  void Fill(Histos& passed, Histos& total) {
    eff_jet_btag->SetPassedHistogram( *passed.h_jet_btag, "f" );
    eff_jet_btag->SetTotalHistogram( *total.h_jet_btag, "f" );

    eff_jet_pt->SetPassedHistogram( *passed.h_jet_pt, "f" );
    eff_jet_pt->SetTotalHistogram( *total.h_jet_pt, "f" );
    
    eff_jet_eta->SetPassedHistogram( *passed.h_jet_eta, "f" );
    eff_jet_eta->SetTotalHistogram( *total.h_jet_eta, "f" );
    
    eff_jet_pt_eta->SetPassedHistogram( *passed.h_jet_pt_eta, "f" );
    eff_jet_pt_eta->SetTotalHistogram( *total.h_jet_pt_eta, "f" );
  }

  void Write() {
    eff_jet_btag->Write();
    eff_jet_pt->Write();
    eff_jet_eta->Write();
    eff_jet_pt_eta->Write();
  }
};

struct SelectConfig {
  int maxjets = -1;
  string jet_value = "none";
  std::vector<float> ptcuts;

  SelectConfig(CfgParser& config) {
    if ( !config.hasOpt("select::maxjets") )
      return;

    maxjets = config.readIntOpt("select", "maxjets");
    std::cout << "\033[1;34m Selecting max jets   : \033[0m" << maxjets << std::endl;

    if ( config.hasOpt("select", "value") ) {
      jet_value = config.readStringOpt("select", "value");
    std::cout << "\033[1;34m Selecting top jets : \033[0m" << jet_value << std::endl;
    }
    
    if (config.hasOpt("select", "ptcuts")) {
      ptcuts = config.readFloatListOpt("select", "ptcuts");
    std::cout << "\033[1;34m Selecting jet pt cuts : \033[0m";
    for (float pt : ptcuts)
    {
    std::cout << " " << pt;
    }
    std::cout << std::endl;
    }
  }
};

std::vector<int> get_selected_jets(const int njets)
{
  std::vector<int> jets(njets);
  iota(jets.begin(), jets.end(), 0);
  return jets;
}

std::vector<int> get_selected_jets_max(const int njets, const TTreeReaderArray<float>& jet_value)
{
  std::vector<int> jets = get_selected_jets( jet_value.GetSize() );

  stable_sort(jets.begin(), jets.end(), [&jet_value](int i1, int i2) { return jet_value[i1] > jet_value[i2]; });
  jets.resize(njets);

  return jets;
}

bool pass_pt_cut(std::vector<int> jets, std::vector<float> ptcuts, const TTreeReaderArray<float>& jet_pt)
{
  if (ptcuts.size() == 0)
    return true;

  stable_sort(jets.begin(), jets.end(), [&jet_pt](int i1, int i2) { return jet_pt[i1] > jet_pt[i2]; });

  int njets = min(jets.size(), ptcuts.size());
  for (int i = 0; i < njets; i++)
  {
    int ijet = jets[i];
    if ( jet_pt[ijet] < ptcuts[i] ) {
      return false;
    }
  }
  return true;
}

/**
 * @brief  Class for reading TFiles produced by the skim_ntuple.cpp script
 * 
 * 
 */
struct SkimFile {
  string name;
  string filepath;
  float xsec;

  float norm = 1;

  TChain* ch;

  SkimFile(string name_, string filepath_, float xsec_) : name(name_), filepath(filepath_), xsec(xsec_) {
      std::cout << "[INFO] ... loading " << name << " with ";
      std::vector<string> filelist = glob(filepath);
      std::cout << filelist.size() << " file(s) at " << xsec << " pb" << std::endl;

      TString treename = "sixBtree";

      int n_files_openned = 0;
      float total_events = 0;
      ch = new TChain(treename);
      for (string file : filelist) {
      TString tfname(file);

      TFile* tf = TFile::Open(tfname);

      if (tf->IsZombie())
        continue;

      if ( !tf->GetListOfKeys()->Contains("h_cutflow") )
        continue;

      TH1D* cutflow = (TH1D*)tf->Get("h_cutflow");
      total_events += cutflow->GetBinContent(1);

      if ( !tf->GetListOfKeys()->Contains(treename) )
        continue;

      ch->AddFile(tfname);
      n_files_openned++;
    }

    if (n_files_openned != filelist.size()) {
    std::cout << "[WARNING] ...  only able to open " << name << " with " << n_files_openned << " of " << filelist.size() << " file(s)" << std::endl;
    }

    norm = xsec / total_events;
  }

  /**
   * @brief Loop through events in TTrees and fill histograms for efficiency measurements
   * 
   * @param btag_wps vector of DeepJet btag working points to use for efficiency
   * @param histos map of histograms to fill for each working point and hadron flavor
   */
  void process(const std::vector<float> btag_wps, const SelectConfig& select_cfg, std::map<string, Histos>& histos) {
    TTreeReader reader(ch);

    TTreeReaderValue<float> genWeight(reader,      "genWeight");
    TTreeReaderArray<float> jet_pt(reader,         "jet_pt");
    TTreeReaderArray<float> jet_eta(reader,        "jet_eta");
    TTreeReaderArray<float> jet_btag(reader,       "jet_btag");
    TTreeReaderArray<int>   jet_hadronFlav(reader, "jet_hadronFlav");
    TTreeReaderArray<int>   jet_partonFlav(reader, "jet_partonFlav");

    int ievent = 0;
    int total_events = ch->GetEntries();
    int steps = (int) (0.1 * total_events);
    if ( steps < 1 )
      steps = 1;

    while (reader.Next()) {
      if ( ievent % steps == 0 ) {
        float progress = ((float)ievent) / ((float)total_events);
        progress = ceil(1000 * progress) / 10;
        std::cout << "\r[INFO] ... processesing " << name << " : " << progress << "%";
        std::cout.flush();
      }
      ievent++;

      std::map<string, int> njetMap;
      std::map<string, float> htjetMap;
      for (string wp : wplabels) {
        njetMap[wp] = 0;
        njetMap[wp + "_hf0"] = 0;
        njetMap[wp + "_hf4"] = 0;
        njetMap[wp + "_hf5"] = 0;

        htjetMap[wp] = 0;
        htjetMap[wp + "_hf0"] = 0;
        htjetMap[wp + "_hf4"] = 0;
        htjetMap[wp + "_hf5"] = 0;
      }

      int njets = jet_pt.GetSize();
      float weight = norm*(*genWeight);

      // Set the maximum number of jets to use ( -1 uses all available )
      int maxjets = select_cfg.maxjets;
      if (maxjets == -1)
        maxjets = njets;

      // Restrict the jets to the top in a specified value
      std::vector<int> jets;
      if (select_cfg.jet_value == "btag")
        jets = get_selected_jets_max(maxjets, jet_btag);
      if (select_cfg.jet_value == "pt")
        jets = get_selected_jets_max(maxjets, jet_pt);
      else
        jets = get_selected_jets(maxjets);

      if (! pass_pt_cut(jets, select_cfg.ptcuts, jet_pt) )
        continue;

      for (int ijet : jets) {
        float btag = jet_btag[ijet];
        float pt = jet_pt[ijet];
        float eta = jet_eta[ijet];
        int hf = jet_hadronFlav[ijet];
        int pf = abs(jet_partonFlav[ijet]);

        for (int wp = 0; wp < 4; wp++) {
          bool passed = btag > btag_wps[wp];
          if (!passed)
            continue;

          string label = wplabels[wp];

          htjetMap[label] += pt;
          histos[label].Fill(pt, eta, btag, weight);
          njetMap[label]++;

          if (hf == 5) {  // b
            histos[label + "_hf5"].Fill(pt, eta, btag, weight);
            njetMap[label + "_hf5"]++;
            htjetMap[label + "_hf5"] += pt;
          } else if (hf == 4) {  // c
            histos[label + "_hf4"].Fill(pt, eta, btag, weight);
            njetMap[label + "_hf4"]++;
            htjetMap[label + "_hf4"] += pt;
          } else {  // guds
            histos[label + "_hf0"].Fill(pt, eta, btag, weight);
            njetMap[label + "_hf0"]++;
            htjetMap[label + "_hf0"] += pt;
          }

          // if (pf == 5) {  // b
          //   histos[label + "_pf5"].Fill(pt, eta, weight);
          // } else if (pf == 4) {  // c
          //   histos[label + "_pf4"].Fill(pt, eta, weight);
          // } else if (pf == 21) {  // g
          //   histos[label + "_pf21"].Fill(pt, eta, weight);
          // } else {  // uds
          //   histos[label + "_pf0"].Fill(pt, eta, weight);
          // }
        }
      }

      for (auto [key, n] : njetMap) {
        histos[key].h_ht_jet->Fill(htjetMap[key], weight);
        histos[key].h_n_jet->Fill(n, weight);
      }
    }
    std::cout << "\r[DONE] ... processesing " << name << " :  100%";
    std::cout.flush();
    std::cout << std::endl;
  }
};

/**
 * @brief run the SkimFile::process method on all files provided. Initializes all needed histograms and places them in the provided TDirectory
 * 
 * @param files vector of SkimFiles to process into histograms
 * @param tdir TDirectory to place histograms into 
 * @param btag_wps vector of DeepJet btag working points
 * @param histos map of histograms to save processed histograms to
 */
void process(std::vector<SkimFile>& files, TDirectory* tdir, std::vector<float> btag_wps, const SelectConfig& select_cfg, std::map<string, Histos>& histos) {
  tdir->cd();

  histos["total"] = Histos("total");
  histos["total_hf0"] = Histos("total_hf0");
  histos["total_hf4"] = Histos("total_hf4");
  histos["total_hf5"] = Histos("total_hf5");

  histos["loose"] = Histos("loose");
  histos["loose_hf0"] = Histos("loose_hf0");
  histos["loose_hf4"] = Histos("loose_hf4");
  histos["loose_hf5"] = Histos("loose_hf5");
  // histos["loose_pf21"]= Histos("loose_pf21");
  // histos["loose_pf0"] = Histos("loose_pf0");
  // histos["loose_pf4"] = Histos("loose_pf4");
  // histos["loose_pf5"] = Histos("loose_pf5");
  
  histos["medium"] = Histos("medium");
  histos["medium_hf0"] = Histos("medium_hf0");
  histos["medium_hf4"] = Histos("medium_hf4");
  histos["medium_hf5"] = Histos("medium_hf5");
  // histos["medium_pf21"]= Histos("medium_pf21");
  // histos["medium_pf0"] = Histos("medium_pf0");
  // histos["medium_pf4"] = Histos("medium_pf4");
  // histos["medium_pf5"] = Histos("medium_pf5");
  
  histos["tight"] = Histos("tight");
  histos["tight_hf0"] = Histos("tight_hf0");
  histos["tight_hf4"] = Histos("tight_hf4");
  histos["tight_hf5"] = Histos("tight_hf5");
  // histos["tight_pf21"]= Histos("tight_pf21");
  // histos["tight_pf0"] = Histos("tight_pf0");
  // histos["tight_pf4"] = Histos("tight_pf4");
  // histos["tight_pf5"] = Histos("tight_pf5");

  for ( SkimFile& f : files ) {
    f.process(btag_wps, select_cfg, histos);
  }

  for (auto [key, histo] : histos) {
    histo.Write();
  }
}

/**
 * @brief Calculate efficiency for the working point and hadronFlav 
 * 
 * @param histos map containing histograms for calculating efficiency
 * @param wp loose, medium, or, tight working point
 * @param hadronFlav hf0 -> guds, hf4 -> c, hf5 -> b
 */
void calculate_efficiency(std::map<string, Histos>& histos, string wp, string hadronFlav) {
  std::cout << "[INFO] ... calculating efficiency " << wp << " for " << hadronFlav << std::endl;

  Histos passed = histos[wp + "_" + hadronFlav];
  Histos total  = histos["total_" + hadronFlav];
  Efficiency eff(wp + "_" + hadronFlav);
  eff.Fill(passed, total);
  eff.Write();
}

//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
// MAIN
//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
int main(int argc, char** argv) { 
  std::cout << "\n\033[1;33m skim_btageff: \033[0m" << std::endl; 

    // Declare command line options
  po::options_description desc("Skim options");
  desc.add_options()
    ("help", "produce help message")
    // required
    ("cfg"   , po::value<string>()->required(), "skim config")
    ("out"   , po::value<string>()->required(), "output root file")
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
  
  ////////////////////////////////////////////////////////////////////////
  // Read config and other cmd line options for skims
  ////////////////////////////////////////////////////////////////////////
  CfgParser config;
  if (!config.init(opts["cfg"].as<string>())) return 1;
  std::cout << "\n\033[1;34m Config          : \033[0m" << opts["cfg"].as<string>() <<std::endl;

  const string year  = config.readStringOpt("parameters::year");
  std::cout << "\033[1;34m Year            : \033[0m"<< year <<std::endl;

  const std::vector<float> btag_wps = config.readFloatListOpt("parameters::bTagWPDef");
  std::cout << "\033[1;34m DeepJet WP      : \033[0m"<< btag_wps[0] << " " << btag_wps[1] << " " << btag_wps[2] <<std::endl;

  const string xsec_file = config.readStringOpt("parameters::xsec");
  CfgParser xsec_cfg;
  if (!xsec_cfg.init(xsec_file)) return 1;
  std::cout << "\033[1;34m MC Xsec Config  : \033[0m" << xsec_file << std::endl;

  const string basepath = config.readStringOpt("parameters::path");
  std::cout << "\033[1;34m File Base Path   : \033[0m" << basepath << std::endl;

  SelectConfig select_cfg(config);

  ////////////////////////////////////////////////////////////////////////
  // Loading MC files from skim_ntuple.cpp
  ////////////////////////////////////////////////////////////////////////

  std::vector<SkimFile> qcd_files;
  for ( string sample : config.readListOfOpts("qcd") ) {
    SkimFile f(sample, basepath + config.readStringOpt("qcd", sample), xsec_cfg.readFloatOpt("2018", sample));
    qcd_files.push_back(f);
  }

  std::vector<SkimFile> ttbar_files;
  for ( string sample : config.readListOfOpts("ttbar") ) {
    SkimFile f(sample, basepath + config.readStringOpt("ttbar", sample), xsec_cfg.readFloatOpt("2018", sample));
    ttbar_files.push_back(f);
  }


  ////////////////////////////////////////////////////////////////////////
  // Process events from QCD and TTBar
  ////////////////////////////////////////////////////////////////////////
  const string outfile = opts["out"].as<string>();
  TFile output(outfile.c_str(), "recreate");
  
  output.cd();
  auto qcd_dir = output.mkdir("qcd/");
  std::map<string, Histos> qcd_histos;
  process(qcd_files, qcd_dir, btag_wps, select_cfg, qcd_histos);

  output.cd();
  auto ttbar_dir = output.mkdir("ttbar/");
  std::map<string, Histos> ttbar_histos;
  process(ttbar_files, ttbar_dir, btag_wps, select_cfg, ttbar_histos);

  ////////////////////////////////////////////////////////////////////////
  // Calculate Efficiencies 
  ////////////////////////////////////////////////////////////////////////
  output.cd();
  auto eff_dir = output.mkdir("eff/");
  eff_dir->cd();
  for (string wp : wplabels) {
    calculate_efficiency(qcd_histos, wp, "hf0");
    calculate_efficiency(ttbar_histos, wp, "hf4");
    calculate_efficiency(ttbar_histos, wp, "hf5");

    // calculate_efficiency(qcd_histos, wp, "pf21");
    // calculate_efficiency(qcd_histos, wp, "pf0");
    // calculate_efficiency(ttbar_histos, wp, "pf4");
    // calculate_efficiency(ttbar_histos, wp, "pf5");
  }

}
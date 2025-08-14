#!/usr/bin/env python3
'''
DESCRIPTION:
Compares data and simulation distributions

./compareTrgEff.py --year 2018
'''
import os
import numpy as np
import math
import ROOT
import array

from argparse import ArgumentParser
ROOT.gROOT.SetBatch(True)
ROOT.ROOT.EnableImplicitMT()
ROOT.ROOT.EnableThreadSafety()

ROOT.PyConfig.IgnoreCommandLineOptions = True

lumi_dict = {2015: 19.52, 2016: 16.81, 2017: 41.48, 2018: 59.83, 2021: 7.98, 2022: 26.67, 2023: 17.65, 2020: 9.45}

year_labels = {"2022": "2022 EE",
               "2021": "2022 pre-EE",
               "2023": "2023 pre-BPix",
               "2020": "2023 BPix",
               "2018": "2018",
}
energy_dict = {2015: "13",
               2016: "13",
               2017: "13",
               2018: "13",
               2021: "13.6",
               2022: "13.6",
               2023: "13.6",
               2020: "13.6",
               }

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def main(args):
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    year_files = {
        "2018": {"data": "data/trigger/2018/TriggerEfficiency_Fit_2018_wMatching.root",
                 "mc": "data/trigger/2018/TriggerEfficiency_Fit_2018_wMatching.root"},
        }


    print("\033[94m {}\033[00m" .format("\nProcessing year : %s" % (args.year)))
    
    f_data = ROOT.TFile(year_files[args.year]["data"], "READ")
    f_mc   = ROOT.TFile(year_files[args.year]["mc"], "READ")

    filters = ["L1filterHT",
               "QuadCentralJet30",
               "CaloQuadJet30HT320",
               "BTagCaloDeepCSVp17Double",
               "PFCentralJetLooseIDQuad30",
               "1PFCentralJetLooseID75",
               "2PFCentralJetLooseID60",
               "3PFCentralJetLooseID45",
               "4PFCentralJetLooseID40",
               "PFCentralJetsLooseIDQuad30HT330",
               "BTagPFDeepCSV4p5Triple"
               ]

    titles = {
        "L1filterHT" : r"Sum p_{T} [GeV]",
        "QuadCentralJet30" : r"p_{T}^{4} [GeV]",
        "CaloQuadJet30HT320" : "PF #sum p_{T} with p_{T}>30 GeV [GeV]",
        "BTagCaloDeepCSVp17Double" : r"DeepFlavB^{1}",
        "PFCentralJetLooseIDQuad30" : r"p_{T}^{4} [GeV]",
        "1PFCentralJetLooseID75" : r"p_{T}^{1} [GeV]",
        "2PFCentralJetLooseID60" : r"p_{T}^{2} [GeV]",
        "3PFCentralJetLooseID45" : r"p_{T}^{3} [GeV]",
        "4PFCentralJetLooseID40" : r"p_{T}^{4} [GeV]",
        "PFCentralJetsLooseIDQuad30HT330" : "PF #sum p_{T} with p_{T}>30 GeV [GeV]",
        "BTagPFDeepCSV4p5Triple" : r"PF DeepFlavB^{1}"
    }

    for fil in filters:
        # Canvas and general style options
        ROOT.gStyle.SetOptStat(0)
        ROOT.gStyle.SetTextFont(42)
        d = ROOT.TCanvas("", "", 600, 600)
        
        legend = ROOT.TLegend(0.60, 0.32, 0.88, 0.58)
        legend.SetFillColor(0)
        legend.SetBorderSize(0)
        legend.SetTextSize(0.028)
        
        ROOT.SetOwnership(d, False)
        d.SetLeftMargin(0.15)
        
        h_data_nominal = f_data.Get("SingleMuon__Efficiency_%s" % (fil)).Clone("data")
        h_mc = f_mc.Get("TTbar__Efficiency_%s" % (fil)).Clone("mc")
        
        h_data_nominal.SetLineColor(ROOT.kBlack)
        h_data_nominal.SetLineWidth(3)
        h_data_nominal.GetYaxis().SetTitleOffset(1.3)
        h_data_nominal.SetTitle(fr";{titles[fil]};Efficiency")
        h_data_nominal.SetMinimum(0.0)
        h_data_nominal.SetMaximum(1.05)
        
        h_mc.SetLineColor(ROOT.kBlue)
        h_mc.SetLineWidth(3)
        
        h_data_nominal.Draw()
        h_mc.Draw("same")
        
        # Create ratios
        
        d.Modified()
        d.Update()
        
        legend.AddEntry(h_data_nominal, "Data")
        legend.AddEntry(h_mc, "Simulation")
        legend.Draw("same")
        
        cms_label = ROOT.TLatex()
        cms_label.SetTextSize(0.04)
        cms_label.DrawLatexNDC(0.14, 0.915, "#bf{CMS}")
        
        prel_label = ROOT.TLatex()
        prel_label.SetTextSize(0.04)
        prel_label.DrawLatexNDC(0.22, 0.915, "#it{Preliminary}")
    
        header = ROOT.TLatex()
        header.SetTextSize(0.04)
        header.DrawLatexNDC(0.64, 0.915, "%s (13 TeV)" % year_labels[args.year])
        
        d.Modified()
        d.Update()
        
        savename = "TrgEff_DataVsMC_%s_%s" % (args.year, fil)
        d.SaveAs(savename+".pdf")
        d.SaveAs(savename+".png")
    return

if __name__ == "__main__":

    # Default values
    YEAR = "2018"
    parser = ArgumentParser(description="Plot sfs")
    parser.add_argument("--year", dest="year", action="store", default=YEAR, help="Process year")
    args = parser.parse_args()
    main(args)

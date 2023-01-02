#!/usr/bin/env python3
'''
DESCRIPTION


'''
#===================================
# Import modules
#===================================
import ROOT
import os
import sys
import time
import datetime
import math
import socket
import getpass
from argparse import ArgumentParser

# Enable ROOT's implicit multi-threading
ROOT.gROOT.SetBatch(True)

def getPublicPath(convertToURL=False):
    
    if "fnal" in socket.gethostname().lower():
        urlDir  = "http://home.fnal.gov/~%s/" % (getpass.getuser())
        baseDir = "/publicweb/%s/%s/" % (getpass.getuser()[0], getpass.getuser())
    elif "cern.ch" in socket.gethostname().lower():
        urlDir  = "https://cmsdoc.cern.ch/~%s/" % (getpass.getuser())
        baseDir = "/afs/cern.ch/user/%s/%s/public/html" % (getpass.getuser()[0], getpass.getuser())
    else:
        raise Exception("Cannot determine URL path for host %s" % (socket.gethostname()))
        
    if not os.path.isdir(baseDir):
        raise Exception("Invalid path. The public directory '%s' does not exist! Something went wrong.." % (baseDir))
        
    if convertToURL:
        return urlDir
    else:
        return baseDir
        
def GetLabel(sample):
    labels = {}
    labels["GluGluToHHTo4B_node_cHHH0"] = "HH#rightarrow 4b cHHH0"
    labels["GluGluToHHTo4B_node_cHHH1"] = "HH#rightarrow 4b cHHH1"
    labels["GluGluToHHTo4B_node_cHHH2p45"] = "HH#rightarrow 4b cHHH2p45"
    labels["GluGluToHHTo4B_node_cHHH5"] = "HH#rightarrow 4b cHHH5"
    return labels[sample]

def GetOpts(hname):
    
    opts = {"xlabel" : "", "xmin": 0.0, "xmax": 2000.0, "ymaxfactor": 1.10}
    
    if "delta" in hname.lower() or "eta" in hname.lower():
        opts["ymaxfactor"] = 1.30
        
    if "phi" in hname:
        opts["xmin"] = -3.0
        opts["xmax"] = 3.0
    elif "eta" in hname:
        opts["xmin"] = -4.0
        opts["xmax"] = 4.0
    elif "b2_pt" in hname:
        opts["xmin"] = 0.0
        opts["xmax"] = 400
        
        if "resolved" in hname.lower():
            opts["xmax"] = 300
    elif "b1_pt" in hname:
        opts["xmin"] = 0.0
        opts["xmax"] = 700
        if "resolved" in hname.lower():
            opts["xmax"] = 500
    elif "H1_pt" in hname or "H2_pt" in hname:
        opts["xmin"] = 0.0
        opts["xmax"] = 1000
        if "resolved" in hname.lower():
            opts["xmax"] = 600
        
    elif "NFatJets" in hname:
        opts["xmin"] = 0.0
        opts["xmax"] = 6
    elif "DeltaPhi" in hname:
        opts["xmin"] = 0.0
        opts["xmax"] = 3.4
    else:
        pass


    if "hSemiresolved_H1Boosted_H2resolved_GenFatJet_H1_pt" in hname or "hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_pt" in hname or "hSemiresolved_H2Boosted_H1resolved_GenFatJet_H2_pt" in hname or "hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_pt" in hname:
        opts["xmax"] = 1000
        opts["ymaxfactor"] = 1.25
    if "nsubjets" in hname:
        opts["ymaxfactor"] = 1.3

    return opts

def AddPreliminaryText():
    # Setting up preliminary text
    tex = ROOT.TLatex(0.,0., 'Simulation Preliminary');
    tex.SetNDC();
    tex.SetX(0.22);
    tex.SetY(0.92);
    tex.SetTextFont(53);
    tex.SetTextSize(28);
    tex.SetLineWidth(2)
    return tex

def AddCMSText():
    # Settign up cms text
    texcms = ROOT.TLatex(0.,0., 'CMS');
    texcms.SetNDC();
    texcms.SetTextAlign(31);
    texcms.SetX(0.21);
    texcms.SetY(0.92);
    texcms.SetTextFont(63);
    texcms.SetLineWidth(2);
    texcms.SetTextSize(30);
    return texcms


def PrintSummary():
    
    # Create a table for samples
    samples = []
    msgAlign = "{:<3} {:<60}"
    header   = msgAlign.format("#", "Sample name")
    hLine    = "="*len(header)
    samples.append("")
    samples.append(hLine)
    samples.append(header)
    samples.append(hLine)

    # Create a table for selections
    selections = []
    selAlign = "{:<3} {:<15}"
    header   = selAlign.format("#", "Selections")
    hLine    = "="*len(header)
    selections.append("")
    selections.append(hLine)
    selections.append(header)
    selections.append(hLine)
    
    # Initialize selection counter
    j = 0
    s = []
    sel = []
    
    # Loop over ROOT directories
    for i, key in enumerate(ROOT.gDirectory.GetListOfKeys()):
        kname    = key.GetName()
        isFolder = key.IsFolder()
        if (isFolder):
            s.append(kname)
            samples.append(msgAlign.format(i, kname))
        else:
            pass
            
        title = key.GetTitle()
        print(title)
        if isFolder:
            print(title)
            selection = title.split("/")[-1]
            sel.append(selection)
            
    for l in samples:
        print(l)
        
    sel = set(sel)
    for m, isel in enumerate(sel):
        selections.append(msgAlign.format(m, isel))

    for l in selections:
        print(l)
    
    print("\n")
    return s, sel


def main(args):
    
    f = ROOT.TFile.Open("histogramsForHHTo4b.root", "READ")
    
    if not args.verbose:
        ROOT.gErrorIgnoreLevel = ROOT.kWarning

    samples, selections = PrintSummary()
    
    labels = {"Resolved"     : "resolved",
              "Semiresolved" : "semi-resolved",
              "Boosted"      : "boosted"}
    
    colors = {"Resolved"     : ROOT.kBlue,
              "Semiresolved" : ROOT.kMagenta+2,
              "Boosted"      : ROOT.kRed}

    triggers = ["HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5",
                "HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np4",
                "HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np2",
                "HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p1",
                "HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p17",
                "HLT_PFHT1050",
                "HLT_PFJet500",
                "HLT_AK8PFHT800_TrimMass50",
                "HLT_AK8PFJet400_TrimMass30",
                "HLT_AK8PFJet420_TrimMass30",
                "HLT_AK8PFJet500",
                "HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59",
                "HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94",
                "HLT_AK8PFHT750_TrimMass50",
                "HLT_AK8PFJet360_TrimMass30",
                "HLT_AK8PFJet380_TrimMass30",
                "OR"]

    categories = ["hPassed_",
                  "hResolvedPassed_",
                  "hSemiresolvedPassed_",
                  "hBoostedPassed_"]

    for sample in samples:
        print("\n Sample : %s" % (sample))
        
        for category in categories:
            print("Category : %s" % (category))
            
            for trigger in triggers:
                
                h = f.Get(sample+"/"+category+trigger)
                entries = h.GetEntries()
                failed = round(h.GetBinContent(1)/entries*100, 2)
                passed = round(h.GetBinContent(2)/entries*100, 2)
                
                print(" Trigger: %s   passed=%s  " % (trigger, passed))
            

    histos = ["h_GenPart_H1_pt",
              "h_GenPart_H2_pt",
              "h_GenPart_H1_eta",
              "h_GenPart_H2_eta",
              "h_GenPart_H1_phi",
              "h_GenPart_H2_phi",
              "h_GenPart_H1_b1_pt",
              "h_GenPart_H1_b2_pt",
              "h_GenPart_H1_b1_eta",
              "h_GenPart_H1_b2_eta",
              "h_GenPart_H1_b1_phi",
              "h_GenPart_H1_b2_phi",
              "h_GenPart_H2_b1_pt",
              "h_GenPart_H2_b2_pt",
              "h_GenPart_H2_b1_eta",
              "h_GenPart_H2_b2_eta",
              "h_GenPart_H2_b1_phi",
              "h_GenPart_H2_b2_phi",
              ]

    for sample in samples:
        print("\n Sample : %s" % (sample))
        for h in histos:
            ROOT.gStyle.SetOptStat(0)
            ROOT.gStyle.SetTextFont(42)
            
            d = ROOT.TCanvas("", "", 800, 700)
            d.SetLeftMargin(0.15)
            
            legend = ROOT.TLegend(0.65, 0.70, 0.95, 0.88)
            legend.SetFillColor(0)
            legend.SetFillStyle(0)
            legend.SetBorderSize(0)
            legend.SetTextSize(0.03)
            
            opts = GetOpts(h)
            maxY = -1.0
            
            histo = f.Get(sample+"/"+h)
            histo.Scale(1.0/histo.Integral())
            if histo.GetMaximum() > maxY:
                maxY = histo.GetMaximum()
            histo.SetTitle("")
            histo.GetYaxis().SetTitle("Arbitrary Units")
            histo.GetXaxis().SetRangeUser(opts["xmin"], opts["xmax"])
            histo.SetLineColor(ROOT.kBlue)
            histo.SetMarkerColor(ROOT.kBlue)
            histo.SetFillColorAlpha(ROOT.kBlue, 0.75)
            histo.SetFillStyle(3001)
            
            histo.Draw("hist same")
            
            legend.AddEntry(histo, "all events")
            legend.Draw("same")
            
            tex_cms = AddCMSText()
            tex_cms.Draw("same")
            
            tex_prelim = AddPreliminaryText()
            tex_prelim.Draw("same")
            
            header = ROOT.TLatex()
            header.SetTextSize(0.04)
            header.DrawLatexNDC(0.65, 0.92, "2018, #sqrt{s} = 13 TeV")
            
            # Update canvas
            d.Modified()
            d.Update()
            #d.SetLogy()
            
            # Save plot
            for s in args.formats:
                saveName = os.path.join(args.path, "AllEvents_%s_%s%s" % (h, sample, s))
                d.SaveAs(saveName)
            
    # Compare Resolved - Boosted - Semiresolved GenParticles
    histos = ["GenPart_H1_pt",
              "GenPart_H2_pt",
              "GenPart_H1_b1_pt",
              "GenPart_H1_b2_pt",
              "GenPart_H2_b1_pt",
              "GenPart_H2_b2_pt",
              "GenPart_H1_b1_eta",
              "GenPart_H1_b2_eta",
              "GenPart_H2_b1_eta",
              "GenPart_H2_b2_eta",
              "GenPart_H1_b1_phi",
              "GenPart_H1_b2_phi",
              "GenPart_H2_b1_phi",
              "GenPart_H2_b2_phi",]
    
    for sample in samples:
        
        print("\n Sample: %s" % (sample))
        
        for h in histos:
            print("Histogram name : %s" % (h))
            
            # Create canvas
            ROOT.gStyle.SetOptStat(0)
            ROOT.gStyle.SetTextFont(42)
            
            d = ROOT.TCanvas("", "", 800, 700)
            d.SetLeftMargin(0.15)
            
            legend = ROOT.TLegend(0.65, 0.70, 0.95, 0.88)
            legend.SetFillColor(0)
            legend.SetFillStyle(0)
            legend.SetBorderSize(0)
            legend.SetTextSize(0.03)
            
            opts = GetOpts(h)
            maxY = -1.0
            
            print(sample+"/hResolved_"+h)

            hResolved = f.Get(sample+"/hResolved_"+h)
            hResolved.Scale(1.0/hResolved.Integral())
            if hResolved.GetMaximum() > maxY:
                maxY = hResolved.GetMaximum()
            hResolved.SetTitle("")
            hResolved.GetYaxis().SetTitle("Arbitrary Units")
            hResolved.GetXaxis().SetRangeUser(opts["xmin"], opts["xmax"])
            hResolved.SetLineColor(ROOT.kBlue)
            hResolved.SetMarkerColor(ROOT.kBlue)
            hResolved.SetMarkerSize(1.05)
            hResolved.SetFillColorAlpha(ROOT.kBlue, 0.75)
            hResolved.SetFillStyle(3001)
            
            hSemi = f.Get(sample+"/hSemiresolved_"+h)
            hSemi.Scale(1.0/hSemi.Integral())
            if (hSemi.GetMaximum() > maxY):
                maxY = hSemi.GetMaximum()
            hSemi.SetLineColor(ROOT.kGray+2)
            hSemi.SetMarkerColor(ROOT.kGray+2)
            hSemi.SetMarkerStyle(22)
            hSemi.SetMarkerSize(1.05)
            
            hBoosted = f.Get(sample+"/hBoosted_"+h)
            hBoosted.Scale(1.0/hBoosted.Integral())
            if (hBoosted.GetMaximum() > maxY):
                maxY = hBoosted.GetMaximum()
            hBoosted.SetLineColor(ROOT.kGreen+2)
            hBoosted.SetMarkerColor(ROOT.kGreen+2)
            hBoosted.SetMarkerStyle(23)
            hBoosted.SetMarkerSize(1.05)
            hBoosted.SetFillColorAlpha(ROOT.kGreen+2, 0.75)
            hBoosted.SetFillStyle(3001)
            
            hResolved.SetMaximum(maxY*opts["ymaxfactor"])
            hResolved.Draw("hist")
            hBoosted.Draw("hist same")
            hSemi.Draw("same")
            
            legend.AddEntry(hResolved, "resolved")
            legend.AddEntry(hBoosted, "boosted")
            legend.AddEntry(hSemi, "semi-resolved")
            legend.Draw("same")
            
            tex_cms = AddCMSText()
            tex_cms.Draw("same")
            
            tex_prelim = AddPreliminaryText()
            tex_prelim.Draw("same")
            
            header = ROOT.TLatex()
            header.SetTextSize(0.04)
            header.DrawLatexNDC(0.65, 0.92, "2018, #sqrt{s} = 13 TeV")
            
            # Update canvas
            d.Modified()
            d.Update()
            #d.SetLogy()
            
            # Save plot
            for s in args.formats:
                saveName = os.path.join(args.path, "%s_%s%s" % (h, sample, s))
                d.SaveAs(saveName)
            
    # New histograms:
    histos = ["hResolved_GenJet_H1_b1_pt",
              "hResolved_GenJet_H1_b2_pt",
              "hResolved_GenJet_H2_b1_pt",
              "hResolved_GenJet_H2_b2_pt",
              "hResolved_GenJet_H1_b1_eta",
              "hResolved_GenJet_H1_b2_eta",
              "hResolved_GenJet_H2_b1_eta",
              "hResolved_GenJet_H2_b2_eta",
              "hResolved_GenJet_H1_b1_phi",
              "hResolved_GenJet_H1_b2_phi",
              "hResolved_GenJet_H2_b1_phi",
              "hResolved_GenJet_H2_b2_phi",
              "hResolved_RecoJet_H1_b1_pt",
              "hResolved_RecoJet_H1_b2_pt",
              "hResolved_RecoJet_H2_b1_pt",
              "hResolved_RecoJet_H2_b2_pt",
              "hResolved_RecoJet_H1_b1_eta",
              "hResolved_RecoJet_H1_b2_eta",
              "hResolved_RecoJet_H2_b1_eta",
              "hResolved_RecoJet_H2_b2_eta",
              "hResolved_RecoJet_H1_b1_phi",
              "hResolved_RecoJet_H1_b2_phi",
              "hResolved_RecoJet_H2_b1_phi",
              "hResolved_RecoJet_H2_b2_phi",
              "hResolved_RecoJet_H1_b1_btag",
              "hResolved_RecoJet_H1_b2_btag",
              "hResolved_RecoJet_H2_b1_btag",
              "hResolved_RecoJet_H2_b2_btag",
              "hResolved_RecoJet_DeltaR_H1b1_H1b2",
              "hResolved_RecoJet_DeltaR_H1b1_H2b1",
              "hResolved_RecoJet_DeltaR_H1b1_H2b2",
              "hResolved_RecoJet_DeltaR_H1b2_H2b1",
              "hResolved_RecoJet_DeltaR_H1b2_H2b2",
              "hResolved_RecoJet_DeltaR_H2b1_H2b2",
              "hResolved_RecoJet_DeltaEta_H1b1_H1b2",
              "hResolved_RecoJet_DeltaEta_H1b1_H2b1",
              "hResolved_RecoJet_DeltaEta_H1b1_H2b2",
              "hResolved_RecoJet_DeltaEta_H1b2_H2b1",
              "hResolved_RecoJet_DeltaEta_H1b2_H2b2",
              "hResolved_RecoJet_DeltaEta_H2b1_H2b2",
              "hResolved_RecoJet_DeltaPhi_H1b1_H1b2",
              "hResolved_RecoJet_DeltaPhi_H1b1_H2b1",
              "hResolved_RecoJet_DeltaPhi_H1b1_H2b2",
              "hResolved_RecoJet_DeltaPhi_H1b2_H2b1",
              "hResolved_RecoJet_DeltaPhi_H1b2_H2b2",
              "hResolved_RecoJet_DeltaPhi_H2b1_H2b2",
              "hResolved_RecoJet_H1_pt",
              "hResolved_RecoJet_H2_pt",
              "hResolved_RecoJet_H1_eta",
              "hResolved_RecoJet_H2_eta",
              "hResolved_RecoJet_H1_phi",
              "hResolved_RecoJet_H2_phi",
              "hResolved_RecoJet_InvMass_H1",
              "hResolved_RecoJet_InvMass_H2",
              "hResolved_RecoJet_InvMassRegressed_H1",
              "hResolved_RecoJet_InvMassRegressed_H2",
              "hResolved_RecoJet_DeltaR_H1_H2",
              "hResolved_RecoJet_DeltaEta_H1_H2",
              "hResolved_RecoJet_DeltaPhi_H1_H2",
              "hResolved_RecoJet_NJets",
              "hResolved_RecoJet_NFatJets",
              # Boosted
              "hBoosted_GenFatJet_H1_pt",
              "hBoosted_GenFatJet_H2_pt",
              "hBoosted_GenFatJet_H1_eta",
              "hBoosted_GenFatJet_H2_eta",
              "hBoosted_GenFatJet_H1_phi",
              "hBoosted_GenFatJet_H2_phi",
              "hBoosted_RecoFatJet_H1_pt",
              "hBoosted_RecoFatJet_H2_pt",
              "hBoosted_RecoFatJet_H1_eta",
              "hBoosted_RecoFatJet_H2_eta",
              "hBoosted_RecoFatJet_H1_phi",
              "hBoosted_RecoFatJet_H2_phi",
              "hBoosted_RecoFatJet_H1_TXbb",
              "hBoosted_RecoFatJet_H2_TXbb",
              "hBoosted_RecoFatJet_H1_m",
              "hBoosted_RecoFatJet_H2_m",
              "hBoosted_NJets",
              "hBoosted_NFatJets",
              "hBoosted_RecoFatJet_DeltaR_H1_H2",
              "hBoosted_RecoFatJet_DeltaEta_H1_H2",
              "hBoosted_RecoFatJet_DeltaPhi_H1_H2",
              "hBoosted_RecoFatJet_H1_mSD_Uncorrected",
              "hBoosted_RecoFatJet_H1_area",
              "hBoosted_RecoFatJet_H1_n2b1",
              "hBoosted_RecoFatJet_H1_n3b1",
              "hBoosted_RecoFatJet_H1_tau21",
              "hBoosted_RecoFatJet_H1_tau32",
              "hBoosted_RecoFatJet_H1_nsubjets",
              "hBoosted_RecoFatJet_H1_subjet1_pt",
              "hBoosted_RecoFatJet_H1_subjet1_eta",
              "hBoosted_RecoFatJet_H1_subjet1_phi",
              "hBoosted_RecoFatJet_H1_subjet1_m",
              "hBoosted_RecoFatJet_H1_subjet1_btag",
              "hBoosted_RecoFatJet_H1_subjet2_pt",
              "hBoosted_RecoFatJet_H1_subjet2_eta",
              "hBoosted_RecoFatJet_H1_subjet2_phi",
              "hBoosted_RecoFatJet_H1_subjet2_m",
              "hBoosted_RecoFatJet_H1_subjet2_btag",
              "hBoosted_RecoFatJet_H2_mSD_Uncorrected",
              "hBoosted_RecoFatJet_H2_area",
              "hBoosted_RecoFatJet_H2_n2b1",
              "hBoosted_RecoFatJet_H2_n3b1",
              "hBoosted_RecoFatJet_H2_tau21",
              "hBoosted_RecoFatJet_H2_tau32",
              "hBoosted_RecoFatJet_H2_nsubjets",
              "hBoosted_RecoFatJet_H2_subjet1_pt",
              "hBoosted_RecoFatJet_H2_subjet1_eta",
              "hBoosted_RecoFatJet_H2_subjet1_phi",
              "hBoosted_RecoFatJet_H2_subjet1_m",
              "hBoosted_RecoFatJet_H2_subjet1_btag",
              "hBoosted_RecoFatJet_H2_subjet2_pt",
              "hBoosted_RecoFatJet_H2_subjet2_eta",
              "hBoosted_RecoFatJet_H2_subjet2_phi",
              "hBoosted_RecoFatJet_H2_subjet2_m",
              "hBoosted_RecoFatJet_H2_subjet2_btag",
              # Semiresolved
              "hSemiresolved_H1Boosted_H2resolved_GenFatJet_H1_pt",
              "hSemiresolved_H1Boosted_H2resolved_GenFatJet_H1_eta",
              "hSemiresolved_H1Boosted_H2resolved_GenFatJet_H1_phi",
              "hSemiresolved_H1Boosted_H2resolved_GenJet_H2_b1_pt",
              "hSemiresolved_H1Boosted_H2resolved_GenJet_H2_b1_eta",
              "hSemiresolved_H1Boosted_H2resolved_GenJet_H2_b1_phi",
              "hSemiresolved_H1Boosted_H2resolved_GenJet_H2_b2_pt",
              "hSemiresolved_H1Boosted_H2resolved_GenJet_H2_b2_eta",
              "hSemiresolved_H1Boosted_H2resolved_GenJet_H2_b2_phi",
              "hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_pt",
              "hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_eta",
              "hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_phi",
              "hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_m",
              "hSemiresolved_H1Boosted_H2resolved_RecoJet_H2_b1_pt",
              "hSemiresolved_H1Boosted_H2resolved_RecoJet_H2_b2_pt",
              "hSemiresolved_H1Boosted_H2resolved_RecoJet_H2_b1_eta",
              "hSemiresolved_H1Boosted_H2resolved_RecoJet_H2_b2_eta",
              "hSemiresolved_H1Boosted_H2resolved_RecoJet_H2_b1_phi",
              "hSemiresolved_H1Boosted_H2resolved_RecoJet_H2_b2_phi",
              "hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_mSD_Uncorrected",
              "hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_area",
              "hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_n2b1",
              "hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_n3b1",
              "hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_tau21",
              "hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_tau32",
              "hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_nsubjets",
              "hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_pt",
              "hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_eta",
              "hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_phi",
              "hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_btag",
              "hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_m",
              "hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_pt",
              "hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_eta",
              "hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_phi",
              "hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_btag",
              "hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_m",
              "hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_TXbb",
              "hSemiresolved_H1Boosted_H2resolved_H2_pt",
              "hSemiresolved_H1Boosted_H2resolved_H2_eta",
              "hSemiresolved_H1Boosted_H2resolved_H2_phi",
              "hSemiresolved_H1Boosted_H2resolved_NJets",
              "hSemiresolved_H1Boosted_H2resolved_NFatJets",
              "hSemiresolved_H1Boosted_H2resolved_DeltaR_H1_H2",
              "hSemiresolved_H1Boosted_H2resolved_DeltaEta_H1_H2",
              "hSemiresolved_H1Boosted_H2resolved_DeltaPhi_H1_H2",
              "hSemiresolved_H1Boosted_H2resolved_InvMass_H2",
              "hSemiresolved_H1Boosted_H2resolved_InvMassRegressed_H2",
              
              "hSemiresolved_H2Boosted_H1resolved_GenFatJet_H2_pt",
              "hSemiresolved_H2Boosted_H1resolved_GenFatJet_H2_eta",
              "hSemiresolved_H2Boosted_H1resolved_GenFatJet_H2_phi",
              "hSemiresolved_H2Boosted_H1resolved_GenJet_H1_b1_pt",
              "hSemiresolved_H2Boosted_H1resolved_GenJet_H1_b1_eta",
              "hSemiresolved_H2Boosted_H1resolved_GenJet_H1_b1_phi",
              "hSemiresolved_H2Boosted_H1resolved_GenJet_H1_b2_pt",
              "hSemiresolved_H2Boosted_H1resolved_GenJet_H1_b2_eta",
              "hSemiresolved_H2Boosted_H1resolved_GenJet_H1_b2_phi",
              "hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_pt",
              "hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_eta",
              "hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_phi",
              "hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_m",
              "hSemiresolved_H2Boosted_H1resolved_RecoJet_H1_b1_pt",
              "hSemiresolved_H2Boosted_H1resolved_RecoJet_H1_b2_pt",
              "hSemiresolved_H2Boosted_H1resolved_RecoJet_H1_b1_eta",
              "hSemiresolved_H2Boosted_H1resolved_RecoJet_H1_b2_eta",
              "hSemiresolved_H2Boosted_H1resolved_RecoJet_H1_b1_phi",
              "hSemiresolved_H2Boosted_H1resolved_RecoJet_H1_b2_phi",
              "hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_mSD_Uncorrected",
              "hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_area",
              "hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_n2b1",
              "hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_n3b1",
              "hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_tau21",
              "hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_tau32",
              "hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_nsubjets",
              "hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_pt",
              "hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_eta",
              "hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_phi",
              "hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_btag",
              "hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_m",
              "hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_pt",
              "hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_eta",
              "hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_phi",
              "hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_btag",
              "hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_m",
              "hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_TXbb",
              "hSemiresolved_H2Boosted_H1resolved_NJets",
              "hSemiresolved_H2Boosted_H1resolved_NFatJets",
              "hSemiresolved_H2Boosted_H1resolved_DeltaR_H1_H2",
              "hSemiresolved_H2Boosted_H1resolved_DeltaEta_H1_H2",
              "hSemiresolved_H2Boosted_H1resolved_DeltaPhi_H1_H2",
              "hSemiresolved_H2Boosted_H1resolved_InvMass_H1",
              "hSemiresolved_H2Boosted_H1resolved_InvMassRegressed_H1",
    ]
    
        
    for h in histos:
        
        print("Processing histogram %s" % (h))
        
        # Create canvas
        ROOT.gStyle.SetOptStat(0)
        ROOT.gStyle.SetTextFont(42)
        
        d = ROOT.TCanvas("", "", 800, 700)
        d.SetLeftMargin(0.15)
        
        legend = ROOT.TLegend(0.55, 0.70, 0.95, 0.88)
        legend.SetFillColor(0)
        legend.SetFillStyle(0)
        legend.SetBorderSize(0)
        legend.SetTextSize(0.03)
        if "Resolved" in h:
            legend.SetHeader("resolved")
        elif "Semiresolved" in h:
            legend.SetHeader("semi-resolved")
        elif "Boosted" in h:
            legend.SetHeader("boosted")


        opts = GetOpts(h)
        maxY = -1.0
        
        h0 = f.Get("GluGluToHHTo4B_node_cHHH0/"+h) 
        if "NJets" in h or "NFatJets" in h:
            h0.GetYaxis().SetTitle("Events")
        else:
            h0.GetYaxis().SetTitle("Arbitrary Units")
            h0.Scale(1.0/h0.Integral())
        if h0.GetMaximum() > maxY:
            maxY = h0.GetMaximum()
        h0.SetTitle("")
        h0.GetXaxis().SetRangeUser(opts["xmin"], opts["xmax"])
        h0.SetLineColor(ROOT.kRed+1)
        h0.SetMarkerColor(ROOT.kRed+1)
        h0.SetMarkerSize(1.05)
        h0.SetMarkerStyle(20)
        #h0.SetFillColorAlpha(ROOT.kRed+1, 0.75)
        #h0.SetFillStyle(3001)
        
        h1 = f.Get("GluGluToHHTo4B_node_cHHH1/"+h)
        if "NJets" in h or "NFatJets" in h:
            h1.GetYaxis().SetTitle("Events")
        else:
            h1.GetYaxis().SetTitle("Arbitrary Units")
            h1.Scale(1.0/h1.Integral())
        if (h1.GetMaximum() > maxY):
            maxY = h1.GetMaximum()
        h1.SetTitle("")
        h1.GetXaxis().SetRangeUser(opts["xmin"], opts["xmax"])
        h1.SetLineColor(ROOT.kBlue)
        h1.SetMarkerSize(1.05)
        h1.SetMarkerColor(ROOT.kBlue)
        h1.SetFillColorAlpha(ROOT.kBlue, 0.60)
        h1.SetFillStyle(3001)

        h2 = f.Get("GluGluToHHTo4B_node_cHHH2p45/"+h)
        if "NJets" in h or "NFatJets" in h:
            h2.GetYaxis().SetTitle("Events")
        else:
            h2.GetYaxis().SetTitle("Arbitrary Units")
            h2.Scale(1.0/h2.Integral())
        if (h2.GetMaximum() > maxY):
            maxY = h2.GetMaximum()
        h2.SetTitle("")
        h2.GetXaxis().SetRangeUser(opts["xmin"], opts["xmax"])
        h2.SetLineColor(ROOT.kGreen+2)
        h2.SetMarkerSize(1.05)
        h2.SetMarkerColor(ROOT.kGreen+2)
        h2.SetMarkerStyle(21)
        #h2.SetFillColorAlpha(ROOT.kGreen+1, 0.75)
        #h2.SetFillStyle(3001)

        h5 = f.Get("GluGluToHHTo4B_node_cHHH5/"+h)
        if "NJets" in h or "NFatJets" in h:
            h5.GetYaxis().SetTitle("Events")
        else:
            h5.GetYaxis().SetTitle("Arbitrary Units")
            h5.Scale(1.0/h5.Integral())
        if (h5.GetMaximum() > maxY):
            maxY = h5.GetMaximum()
        h5.SetTitle("")
        h5.GetXaxis().SetRangeUser(opts["xmin"], opts["xmax"])
        h5.SetLineColor(ROOT.kOrange+1)
        h5.SetMarkerSize(1.05)
        h5.SetMarkerColor(ROOT.kOrange+1)
        #h5.SetFillColorAlpha(ROOT.kOrange+1, 0.75)
        h5.SetMarkerStyle(23)
        #h5.SetFillStyle(3001)

        h0.SetMaximum(maxY*opts["ymaxfactor"])
        h1.SetMaximum(maxY*opts["ymaxfactor"])
        h1.Draw("hist")
        h0.Draw("same")
        h2.Draw("same")
        h5.Draw("same")
        
        legend.AddEntry(h0, "ggHH BSM #kappa_{#lambda} = 0")
        legend.AddEntry(h1, "ggHH SM #kappa_{#lambda} = 1")
        legend.AddEntry(h2, "ggHH BSM #kappa_{#lambda} = 2.45")
        legend.AddEntry(h5, "ggHH BSM #kappa_{#lambda} = 5")
        legend.Draw("same")
            
        tex_cms = AddCMSText()
        tex_cms.Draw("same")
        
        tex_prelim = AddPreliminaryText()
        tex_prelim.Draw("same")
        
        header = ROOT.TLatex()
        header.SetTextSize(0.04)
        header.DrawLatexNDC(0.65, 0.92, "2018, #sqrt{s} = 13 TeV")
        
        # Update canvas
        d.Modified()
        d.Update()
        #d.SetLogy()
        
        # Save plot
        for s in args.formats:
            saveName = os.path.join(args.path, "%s%s" % (h, s))
            d.SaveAs(saveName)
            








    d.Close()
    print("\n===Find all the plots under: %s" % (args.path))
    return


    
    return
    
    
def plotComparisonMany(sample, hName, hRef, h1, h2, h3, h4):
    '''
    Creates a comparison plot between a reference histogram and a stack plot
    '''
    
    # Canvas and general style options
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetTextFont(42)
    
    d = ROOT.TCanvas("", "", 800, 700)
    d.SetLeftMargin(0.15)
    
    legend = ROOT.TLegend(0.60, 0.70, 0.90, 0.88)
    legend.SetHeader(GetLabel(sample))
    legend.SetFillColor(0)
    legend.SetFillStyle(0)
    legend.SetBorderSize(0)
    legend.SetTextSize(0.03)
    
    opts = GetOpts(hName)
    opts["ymax"] = opts["ymaxfactor"] * hRef.GetMaximum()
    
    hRef.SetTitle("")
    hRef.GetXaxis().SetTitle(opts["xlabel"])
    hRef.GetXaxis().SetTitleSize(0.04)
    hRef.GetXaxis().SetRangeUser(opts["xmin"], opts["xmax"])
    hRef.GetYaxis().SetTitle("Events / 5 GeV")
    hRef.GetYaxis().SetTitleSize(0.04)
    hRef.SetMaximum(opts["ymax"])
    hRef.SetLineWidth(2)
    hRef.SetMarkerStyle(20)
    hRef.SetLineColor(ROOT.kGreen+1)
    hRef.SetMarkerColor(ROOT.kGreen+1)
    
    h1.SetLineColor(ROOT.kBlue)
    h1.SetLineWidth(2)
    h1.SetMarkerColor(ROOT.kBlue)
    h1.SetMarkerStyle(21)
    h1.SetFillColorAlpha(ROOT.kBlue, 0.35)
    h1.SetFillStyle(3004)
    
    h2.SetLineColor(ROOT.kRed+1)
    h2.SetLineWidth(2)
    h2.SetMarkerColor(ROOT.kRed+1)
    h2.SetMarkerStyle(22)
    
    h3.SetLineColor(ROOT.kGray)
    h3.SetLineWidth(2)
    h3.SetMarkerColor(ROOT.kGray)
    h3.SetFillColorAlpha(ROOT.kGray, 0.35)
    h3.SetFillStyle(1001)
    
    h4.SetLineColor(ROOT.kOrange+7)
    h4.SetLineWidth(2)
    h4.SetMarkerColor(ROOT.kOrange+7)
    h4.SetMarkerStyle(23)
    
    h_stack = ROOT.THStack()
    h_stack.Add(h1.GetPtr())
    h_stack.Add(h2.GetPtr())
    h_stack.Add(h4.GetPtr())
    h_stack.Add(h3.GetPtr())
    
    # Draw histograms
    hcopy_reference = hRef.DrawCopy("hist");
    hcopy_stack     = h_stack.Draw("same nostack")
    
    legend.AddEntry(hcopy_reference, hRef.GetName())
    legend.AddEntry(h3.GetPtr(), h3.GetName())
    legend.AddEntry(h1.GetPtr(), h1.GetName())
    legend.AddEntry(h2.GetPtr(), h2.GetName())
    legend.AddEntry(h4.GetPtr(), h4.GetName())
    
    # Add header
    tex_cms = AddCMSText()
    tex_cms.Draw("same")
    
    tex_prelim = AddPreliminaryText()
    tex_prelim.Draw("same")
    
    header = ROOT.TLatex()
    header.SetTextSize(0.04)
    header.DrawLatexNDC(0.65, 0.92, "2018, #sqrt{s} = 13 TeV")
        
    xMass = 125
    if hName == "Y_m":
        xMass = float(sample.split("MY_")[-1])
        print("xMass = ", xMass)
    line = ROOT.TLine(xMass, 0.0, xMass, opts["ymax"])
    line.SetLineStyle(3)
    line.Draw("same")
    
    # Draw header
    legend.Draw("same")
    
    # Update canvas
    d.Modified()
    d.Update()
    
    # Save plot
    for f in args.formats:
        savePath = getPublicPath()
        saveName = os.path.join(args.path, "NMSSM_XYH_YToHH_6b_%s_%s%s" % (sample, hName, f))
        print(saveName)
        d.SaveAs(saveName)
        
    d.Close()

        
    
    return





if __name__ == "__main__":

    # Default values
    VERBOSE     = False
    ANALYSIS    = "GluGluToHHTo4B"
    SIGNALMASS  = "MX_700_MY_400"
    SIGNALPREFIX= "GluGluToHHTo4B"
    STUDY       = "ControlPlots"
    FORMATS     = [".png", ".pdf", ".C"]
    SAVEPATH    = getPublicPath()
    
    parser = ArgumentParser(description="Perform mass resolution studies")
    parser.add_argument("-v", "--verbose", dest="verbose", default=VERBOSE, action="store_true", help="Verbose mode for debugging purposes [default: %s]" % (VERBOSE))
    parser.add_argument("--signalmass", dest="signalmass", default=SIGNALMASS, action="store", help="Signal mass point to process [default: %s]" % (SIGNALMASS))
    parser.add_argument("--formats", dest="formats", default=FORMATS, action="store", help="Formats to save histograms")
    
    args = parser.parse_args()
    
    args.signal = "_".join([SIGNALPREFIX, SIGNALMASS])
    
    # Save path    
    args.path = os.path.join(SAVEPATH, "%s_%s_%s" % (ANALYSIS, STUDY, datetime.datetime.now().strftime('%d_%b_%Y')))
    if not os.path.exists(args.path):
        os.makedirs(args.path)

    main(args)

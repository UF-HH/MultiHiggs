#!/usr/bin/env python3
'''
DESCRIPTION

A survey on the characteristics of the ggHH(4b) signal modes: resolved, semi-resolved, and boosted
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
    labels["GluGluToHHTo4B_node_cHHH0"] = "ggHH BSM #kappa_{#lambda}=0"
    labels["GluGluToHHTo4B_node_cHHH1"] = "ggHH SM #kappa_{#lambda}=1"
    labels["GluGluToHHTo4B_node_cHHH2p45"] = "ggHH BSM #kappa_{#lambda}=2.45"
    labels["GluGluToHHTo4B_node_cHHH5"] = "ggHH BSM #kappa_{#lambda}=5"
    return labels[sample]

def GetOpts(hname):
    
    opts = {"xlabel" : "", "xmin": 0.0, "xmax": 2000.0, "ymaxfactor": 1.10}
    
    if "delta" in hname.lower() or "eta" in hname.lower():
        opts["ymaxfactor"] = 1.30
        
    if "phi" in hname:
        opts["xmin"] = -3.0
        opts["xmax"] = 3.0
    elif "PFHT" in hname:
        opts["xmin"] = 20
        opts["xmax"] = 1000
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

    if "subjet1_m" in hname or "subjet2_m" in hname:
        opts["xmax"] = 200

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

def NormalizeToUnityTH1I(h):
    hnew = h.Clone()
    for ibin in range(1, hnew.GetNbinsX()+1):
        if hnew.GetBinContent(ibin) == 0:
            hnew.SetBinContent(ibin, 0.0)
        else:
            hnew.SetBinContent(ibin, float(hnew.GetBinContent(ibin))/float(hnew.GetEntries()))

    return hnew

def GetTriggersAcceptance(f, samples):
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
                  "hSemiresolvedExclPassed_",
                  "hBoostedExclPassed_",
                  ]
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

def main(args):
    
    f = ROOT.TFile.Open("histogramsForHHTo4b_22Jan2023v2.root", "READ")
    if not args.verbose:
        ROOT.gErrorIgnoreLevel = ROOT.kWarning

    samples, selections = PrintSummary()
    labels = {"Resolved"     : "resolved",
              "Semiresolved" : "semi-resolved",
              "Boosted"      : "boosted"}
    
    colors = {"Resolved"     : ROOT.kBlue,
              "Semiresolved" : ROOT.kMagenta+2,
              "Boosted"      : ROOT.kRed}

    #GetTriggersAcceptance(f, samples)
    
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Make 2D histograms
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    histos2D = ["h2D_NBQuarksMatchedTo_RecoJetsVsRecoFatJets",
                "h2D_NHiggsMatchedTo_RecoJetsVsRecoFatJets"]

    for sample in samples:
        for h in histos2D:
            ROOT.gStyle.SetOptStat(0)
            ROOT.gStyle.SetTextFont(42)
            
            d = ROOT.TCanvas("", "", 800, 700)
            d.SetLeftMargin(0.12)
            d.SetRightMargin(0.15)
            d.SetLeftMargin(0.13)
            histo = f.Get(sample+"/"+h)
            
            for ibinx in range(1, histo.GetNbinsX()+1):
                for ibiny in range(1, histo.GetNbinsY()+1):
                    content = histo.GetBinContent(ibinx, ibiny)
                    allevents = histo.GetEntries()
                    ratio = round(float(content)/float(allevents), 2)
                    #print("ibin x=", ibinx, "  ibiny=", ibiny, "  content=", content, "   ratio=", ratio*100)
                    histo.SetBinContent(ibinx, ibiny, ratio*100)
                    
            histo.GetZaxis().SetTitle("Percentage of events (%)")
            histo.Draw("COLZ TEXT")
            tex_cms = AddCMSText()
            tex_cms.Draw("same")
            tex_prelim = AddPreliminaryText()
            tex_prelim.Draw("same")
            header = ROOT.TLatex()
            header.SetTextSize(0.04)
            header.DrawLatexNDC(0.65, 0.92, "2018, #sqrt{s} = 13 TeV")
            sampleName = ROOT.TLatex()
            sampleName.SetTextSize(0.03)
            sampleName.DrawLatexNDC(0.15, 0.85, GetLabel(sample))
            d.Modified()
            d.Update()
            for s in args.formats:
                saveName = os.path.join(args.path, "AllEvents_%s_%s%s" % (h, sample, s))
                d.SaveAs(saveName)

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
    # Make 1D hiistograms
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
    print("Make 1D histograms")
    
    histos = ["h_GenPart_H1_pt",
              "h_GenPart_H2_pt",
              "h_GenPart_H1_b1_pt",
              "h_GenPart_H1_b2_pt",
              "h_GenPart_H2_b1_pt",
              "h_GenPart_H2_b2_pt",
              "h_NJets",
              "h_Jet1Pt",
              "h_Jet2Pt",
              "h_Jet3Pt",
              "h_Jet4Pt",
              "h_NLooseBJets",
              "h_NMediumBJets",
              "h_NTightBJets",
              "h_NFatJets",
              "h_AK8Jet1Pt",
              "h_AK8Jet2Pt",
              "h_AK8Jet3Pt",
              "h_AK8Jet4Pt",
          ]
    for sample in samples:
        for h in histos:
            
            print("sample %s    |   Histogram %s" % (sample, h))
            ROOT.gStyle.SetOptStat(0)
            ROOT.gStyle.SetTextFont(42)
            d = ROOT.TCanvas("", "", 800, 700)
            d.SetLeftMargin(0.15)
            
            opts = GetOpts(h)
            maxY = -1.0
            
            histo = f.Get(sample+"/"+h)
            
            if "h_N" in h:
                histo.GetYaxis().SetTitle("Events")
                #entries = histo.GetEntries()
                #for ibin in range(1, histo.GetNbinsX()+1):
                #    content = histo.GetBinContent(ibin)
                #    ratio   = float(content)/float(entries)
                #    histo.SetBinContent(ibin, ratio*100.0)
                #histo.GetYaxis().SetTitle("Percentage of Events (%)")
            else:
                histo.Scale(1.0/histo.Integral())
                if histo.GetMaximum() > maxY:
                    maxY = histo.GetMaximum()
                histo.GetXaxis().SetRangeUser(opts["xmin"], opts["xmax"])

            histo.SetTitle("")
            histo.SetLineColor(ROOT.kBlue)
            histo.SetMarkerColor(ROOT.kBlue)
            histo.SetFillColorAlpha(ROOT.kBlue, 0.85)
            histo.SetFillStyle(3001)
            histo.Draw("hist same")
                                    
            if "_Cases" in histo.GetName():
                legend = ROOT.TLegend(0.40, 0.75, 0.95, 0.80)
                if "4GenJets" in histo.GetName():
                    legend.AddEntry(histo, "4 b-quarks matched to gen-jets")
                elif "4RecoJets" in histo.GetName():
                    legend.AddEntry(histo, "4 b-quarks matched to reco-jets")
            else:
                legend = ROOT.TLegend(0.65, 0.74, 0.95, 0.80)
                legend.AddEntry(histo, "all events")

            legend.SetFillColor(0)
            legend.SetFillStyle(0)
            legend.SetBorderSize(0)
            legend.SetTextSize(0.03)
            legend.Draw("same")
            
            tex_cms = AddCMSText()
            tex_cms.Draw("same")
            
            tex_prelim = AddPreliminaryText()
            tex_prelim.Draw("same")
            
            header = ROOT.TLatex()
            header.SetTextSize(0.04)
            header.DrawLatexNDC(0.65, 0.92, "2018, #sqrt{s} = 13 TeV")
            
            sampleName = ROOT.TLatex()
            sampleName.SetTextSize(0.03)
            sampleName.DrawLatexNDC(0.65, 0.85, GetLabel(sample))
            
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
              "GenPart_H2_b2_eta"]
    
    # Compare Resolved - BoostedExcl - SemiresolvedExcl GenParticles
    for sample in samples:
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
            
            hResolved = f.Get(sample+"/hResolved_"+h).Clone()
            hResolved.Scale(1.0/hResolved.Integral())
            hResolved.SetTitle("")
            hResolved.GetYaxis().SetTitle("Arbitrary Units")
            if "H1_b2_pt" in h or "H2_b2_pt" in h:
                hResolved.GetXaxis().SetRangeUser(0.0, 400)
            elif "H1_b1_pt" in h or "H2_b1_pt" in h:
                hResolved.GetXaxis().SetRangeUser(0.0, 700)
            else:
                hResolved.GetXaxis().SetRangeUser(opts["xmin"], opts["xmax"])
            hResolved.SetLineColor(ROOT.kBlue)
            hResolved.SetMarkerColor(ROOT.kBlue)
            hResolved.SetMarkerSize(1.05)
            hResolved.SetFillColorAlpha(ROOT.kBlue, 0.40)
            hResolved.SetFillStyle(3001)
            if "AK4PFHT" in h:
                hResolved.Rebin(2)
            if hResolved.GetMaximum() > maxY:
                maxY = hResolved.GetMaximum()
            
            hSemi = f.Get(sample+"/hSemiresolvedExcl_MassCut100GeV_"+h).Clone()
            if "H1_b2_pt" in h or "H2_b2_pt" in h:
                hSemi.GetXaxis().SetRangeUser(0.0, 400)
            elif "H1_b1_pt" in h or "H2_b1_pt" in h:
                hSemi.GetXaxis().SetRangeUser(0.0, 700)
            else:
                hSemi.GetXaxis().SetRangeUser(opts["xmin"], opts["xmax"])
            hSemi.Scale(1.0/hSemi.Integral())
            hSemi.SetLineColor(ROOT.kGray+2)
            hSemi.SetMarkerColor(ROOT.kGray+2)
            hSemi.SetMarkerStyle(22)
            hSemi.SetMarkerSize(1.05)
            if "AK4PFHT" in h:
                hSemi.Rebin(2)
            if (hSemi.GetMaximum() > maxY):
                maxY = hSemi.GetMaximum()
            
            hBoosted = f.Get(sample+"/hBoostedExcl_"+h).Clone()
            hBoosted.Scale(1.0/hBoosted.Integral())
            if "H1_b2_pt" in h or "H2_b2_pt" in h:
                hBoosted.GetXaxis().SetRangeUser(0.0, 400)
            elif "H1_b1_pt" in h or "H2_b1_pt" in h:
                hBoosted.GetXaxis().SetRangeUser(0.0, 700)
            else:
                hBoosted.GetXaxis().SetRangeUser(opts["xmin"], opts["xmax"])
            hBoosted.SetLineColor(ROOT.kGreen+2)
            hBoosted.SetMarkerColor(ROOT.kGreen+2)
            hBoosted.SetMarkerStyle(23)
            hBoosted.SetMarkerSize(1.05)
            hBoosted.SetFillColorAlpha(ROOT.kGreen+2, 0.75)
            hBoosted.SetFillStyle(3001)
            if "AK4PFHT" in h:
                hBoosted.Rebin(2)
            if (hBoosted.GetMaximum() > maxY):
                maxY = hBoosted.GetMaximum()
            
            hResolved.SetMaximum(maxY*opts["ymaxfactor"])
            hResolved.Draw("hist")
            if "H1_b2_pt" in h or "H2_b2_pt" in h:
                hResolved.GetXaxis().SetRangeUser(0.0, 400)
            elif "H1_b1_pt" in h or "H2_b1_pt" in h:
                hResolved.GetXaxis().SetRangeUser(0.0, 700)
            else:
                hResolved.GetXaxis().SetRangeUser(opts["xmin"], opts["xmax"])

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
            
            for s in args.formats:
                saveName = os.path.join(args.path, "CategoriesComparison_%s_%s%s" % (h, sample, s))
                d.SaveAs(saveName)

    print("\n==========================================")
    print("   Comparison histograms")
    print("==========================================")
    
    CompareHistos = {}
    
    CompareHistos["Reco_H1_m_Uncorrected"] = {}
    CompareHistos["Reco_H1_m_Uncorrected"]["Resolved"]     = "hResolved_RecoJet_InvMassRegressed_H1"
    CompareHistos["Reco_H1_m_Uncorrected"]["Semiresolved"] = "hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_mSD_Uncorrected"
    CompareHistos["Reco_H1_m_Uncorrected"]["Boosted"]      = "hBoostedExcl_RecoFatJet_H1_mSD_Uncorrected"
    
    CompareHistos["Reco_H1_pt"] = {}
    CompareHistos["Reco_H1_pt"]["Resolved"]     = "hResolved_RecoJet_H1_pt"
    CompareHistos["Reco_H1_pt"]["Semiresolved"] = "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_pt"
    CompareHistos["Reco_H1_pt"]["Boosted"]      = "hBoostedExcl_RecoFatJet_H1_pt"
    
    CompareHistos["Reco_H1_eta"] = {}
    CompareHistos["Reco_H1_eta"]["Resolved"]     = "hResolved_RecoJet_H1_eta"
    CompareHistos["Reco_H1_eta"]["Semiresolved"] = "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_eta"
    CompareHistos["Reco_H1_eta"]["Boosted"]      = "hBoostedExcl_RecoFatJet_H1_eta"
    #
    CompareHistos["Reco_H2_pt"] = {}
    CompareHistos["Reco_H2_pt"]["Resolved"]     = "hResolved_RecoJet_H2_pt"
    CompareHistos["Reco_H2_pt"]["Semiresolved"] = "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_H2_pt"
    CompareHistos["Reco_H2_pt"]["Boosted"]      = "hBoostedExcl_RecoFatJet_H2_pt"
    
    CompareHistos["Reco_H2_eta"] = {}
    CompareHistos["Reco_H2_eta"]["Resolved"]     = "hResolved_RecoJet_H2_eta"
    CompareHistos["Reco_H2_eta"]["Semiresolved"] = "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_H2_eta"
    CompareHistos["Reco_H2_eta"]["Boosted"]      = "hBoostedExcl_RecoFatJet_H2_eta"
    #
    #
    CompareHistos["Reco_H2_m_Uncorrected"] = {}
    CompareHistos["Reco_H2_m_Uncorrected"]["Resolved"]     = "hResolved_RecoJet_InvMassRegressed_H2"
    CompareHistos["Reco_H2_m_Uncorrected"]["Semiresolved"] = "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_InvMassRegressed_H2"
    CompareHistos["Reco_H2_m_Uncorrected"]["Boosted"]      = "hBoostedExcl_RecoFatJet_H2_mSD_Uncorrected"
    #
    CompareHistos["NJets"]   = {}
    CompareHistos["NJets"]["Resolved"]     = "hResolved_RecoJet_NJets"
    CompareHistos["NJets"]["Semiresolved"] = "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_NJets"
    CompareHistos["NJets"]["Boosted"]      = "hBoostedExcl_NJets"
    
    CompareHistos["NLooseBJets"]   = {}
    CompareHistos["NLooseBJets"]["Resolved"]     = "hResolved_RecoJet_NLooseBJets"
    CompareHistos["NLooseBJets"]["Semiresolved"] = "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_NLooseBJets"
    CompareHistos["NLooseBJets"]["Boosted"]      = "hBoostedExcl_RecoJet_NLooseBJets"
    #
    CompareHistos["NMediumBJets"]   = {}
    CompareHistos["NMediumBJets"]["Resolved"]     = "hResolved_RecoJet_NMediumBJets"
    CompareHistos["NMediumBJets"]["Semiresolved"] = "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_NMediumBJets"
    CompareHistos["NMediumBJets"]["Boosted"]      = "hBoostedExcl_RecoJet_NMediumBJets"
    #
    CompareHistos["NTightBJets"]   = {}
    CompareHistos["NTightBJets"]["Resolved"]     = "hResolved_RecoJet_NTightBJets"
    CompareHistos["NTightBJets"]["Semiresolved"] = "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_NTightBJets"
    CompareHistos["NTightBJets"]["Boosted"]      = "hBoostedExcl_RecoJet_NTightBJets"
    


    # 
    CompareHistos["NFatJets"] = {}
    CompareHistos["NFatJets"]["Resolved"]     = "hResolved_RecoJet_NFatJets"
    CompareHistos["NFatJets"]["Semiresolved"] = "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_NFatJets"
    CompareHistos["NFatJets"]["Boosted"]      = "hBoostedExcl_NFatJets"
    #
    CompareHistos["AK4PFHT"] = {}
    CompareHistos["AK4PFHT"]["Resolved"]     = "hResolved_RecoJet_PFHT"
    CompareHistos["AK4PFHT"]["Semiresolved"] = "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_PFHT"
    CompareHistos["AK4PFHT"]["Boosted"]      = "hBoostedExcl_AK4PFHT"
    #
    CompareHistos["AK8PFHT"] = {}
    CompareHistos["AK8PFHT"]["Resolved"]     = "hResolved_RecoJet_AK8PFHT"
    CompareHistos["AK8PFHT"]["Semiresolved"] = "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_AK8PFHT"
    CompareHistos["AK8PFHT"]["Boosted"]      = "hBoostedExcl_AK8PFHT"
    #
    CompareHistos["FatJet1Pt"] = {}
    CompareHistos["FatJet1Pt"]["Resolved"]     = "hResolved_RecoJet_AK8Jet1Pt"
    CompareHistos["FatJet1Pt"]["Semiresolved"] = "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_AK8Jet1Pt"
    CompareHistos["FatJet1Pt"]["Boosted"]      = "hBoostedExcl_AK8Jet1Pt"
    # 
    CompareHistos["FatJet2Pt"] = {}
    CompareHistos["FatJet2Pt"]["Resolved"]     = "hResolved_RecoJet_AK8Jet2Pt"
    CompareHistos["FatJet2Pt"]["Semiresolved"] = "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_AK8Jet2Pt"
    CompareHistos["FatJet2Pt"]["Boosted"]      = "hBoostedExcl_AK8Jet2Pt"
    #
    CompareHistos["RecoJet1Pt"] = {}
    CompareHistos["RecoJet1Pt"]["Resolved"]     = "hResolved_RecoJet_Jet1Pt"
    CompareHistos["RecoJet1Pt"]["Semiresolved"] = "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_Jet1Pt"
    CompareHistos["RecoJet1Pt"]["Boosted"]      = "hBoostedExcl_Jet1Pt"
    
    CompareHistos["RecoJet2Pt"] = {}
    CompareHistos["RecoJet2Pt"]["Resolved"]     = "hResolved_RecoJet_Jet2Pt"
    CompareHistos["RecoJet2Pt"]["Semiresolved"] = "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_Jet2Pt"
    CompareHistos["RecoJet2Pt"]["Boosted"]      = "hBoostedExcl_Jet2Pt"
    
    CompareHistos["RecoJet3Pt"] = {}
    CompareHistos["RecoJet3Pt"]["Resolved"]     = "hResolved_RecoJet_Jet3Pt"
    CompareHistos["RecoJet3Pt"]["Semiresolved"] = "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_Jet3Pt"
    CompareHistos["RecoJet3Pt"]["Boosted"]      = "hBoostedExcl_Jet3Pt"
    
    CompareHistos["RecoJet4Pt"] = {}
    CompareHistos["RecoJet4Pt"]["Resolved"]     = "hResolved_RecoJet_Jet4Pt"
    CompareHistos["RecoJet4Pt"]["Semiresolved"] = "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_Jet4Pt"
    CompareHistos["RecoJet4Pt"]["Boosted"]      = "hBoostedExcl_Jet4Pt"
        
    for sample in samples:
        for i, h in enumerate(CompareHistos):
            
            print("sample = %s    histo: %s" % (sample, h))
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
    
            hResolved=f.Get(sample+"/"+CompareHistos[h]["Resolved"]).Clone()
            hResolved.SetTitle("")
            if "NJets" in h or "NFatJets" in h:
                hResolved = NormalizeToUnityTH1I(hResolved)
            else:
                hResolved.Scale(1.0/hResolved.Integral())
            hResolved.GetYaxis().SetTitle("Arbitrary Units")
            hResolved.SetLineColor(ROOT.kBlue)
            hResolved.SetMarkerColor(ROOT.kBlue)
            hResolved.SetMarkerSize(1.05)
            hResolved.SetFillColorAlpha(ROOT.kBlue, 0.40)
            hResolved.SetFillStyle(3001)
            if "AK4PFHT" in h:# or "Reco_H1_pt" in h or "Reco_H2_pt" in h:
                hResolved.Rebin(2)
            if "AK8PFHT" in h:
                hResolved.GetXaxis().SetRangeUser(200, 2500)
            if hResolved.GetMaximum() > maxY:
                maxY = hResolved.GetMaximum()
            
            hSemi = f.Get(sample+"/"+CompareHistos[h]["Semiresolved"]).Clone()
            if "NJets" in h or "NFatJets" in h:
                hSemi = NormalizeToUnityTH1I(hSemi)
            else:
                hSemi.Scale(1.0/hSemi.Integral())
            hSemi.GetYaxis().SetTitle("Arbitrary Units")
            hSemi.SetLineColor(ROOT.kGray+2)
            hSemi.SetMarkerColor(ROOT.kGray+2)
            hSemi.SetMarkerStyle(22)
            hSemi.SetMarkerSize(1.05)
            if "AK4PFHT" in h:# or "Reco_H1_pt" in h or "Reco_H2_pt" in h:
                hSemi.Rebin(2)
            if (hSemi.GetMaximum() > maxY):
                maxY = hSemi.GetMaximum()

            hBoosted = f.Get(sample+"/"+CompareHistos[h]["Boosted"]).Clone()
            if "NJets" in h or "NFatJets" in h:
                hBoosted = NormalizeToUnityTH1I(hBoosted)
            else:
                hBoosted.Scale(1.0/hBoosted.Integral())
            hBoosted.GetYaxis().SetTitle("Arbitrary Units")
            hBoosted.SetLineColor(ROOT.kGreen+2)
            hBoosted.SetMarkerColor(ROOT.kGreen+2)
            hBoosted.SetMarkerStyle(23)
            hBoosted.SetMarkerSize(1.05)
            hBoosted.SetFillColorAlpha(ROOT.kGreen+2, 0.75)
            hBoosted.SetFillStyle(3001)
            if "AK4PFHT" in h:# or "Reco_H1_pt" in h or "Reco_H2_pt" in h:
                hBoosted.Rebin(2)

            if (hBoosted.GetMaximum() > maxY):
                maxY = hBoosted.GetMaximum()

            if "RecoJet4Pt" in h or "RecoJet3Pt" in h:
                hResolved.GetXaxis().SetRangeUser(0, 600)
                hSemi.GetXaxis().SetRangeUser(0, 600)
                hBoosted.GetXaxis().SetRangeUser(0, 600)
            elif "FatJet1Pt" in h or "FatJet2Pt" in h or "FatJet3Pt" in h or "FatJet4Pt" in h:
                hResolved.GetXaxis().SetRangeUser(200, 1000)
                hSemi.GetXaxis().SetRangeUser(200, 1000)
                hBoosted.GetXaxis().SetRangeUser(200, 1000)

            hResolved.SetMaximum(maxY*opts["ymaxfactor"])

            hResolved.Draw("hist")
            hBoosted.Draw("same hist")
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

            if "Reco_H1_m_Uncorrected" in h:
                line = ROOT.TLine(100, 0.0, 100, hResolved.GetMaximum()) 
                line.Draw("same")

            d.Modified()
            d.Update()

            for s in args.formats:
                saveName = os.path.join(args.path, "CategoriesComparison_MassCut100GeV_%s_%s%s" % (h, sample, s))
                d.SaveAs(saveName)
            

    print("\n")
    print("Individual histograms")
    histos = ["hResolved_GenJet_H1_b1_pt",
              "hResolved_GenJet_H1_b2_pt",
              "hResolved_GenJet_H2_b1_pt",
              "hResolved_GenJet_H2_b2_pt",
              "hResolved_GenJet_H1_b1_eta",
              "hResolved_GenJet_H1_b2_eta",
              "hResolved_GenJet_H2_b1_eta",
              "hResolved_GenJet_H2_b2_eta",
              "hResolved_RecoJet_H1_b1_pt",
              "hResolved_RecoJet_H1_b2_pt",
              "hResolved_RecoJet_H2_b1_pt",
              "hResolved_RecoJet_H2_b2_pt",
              "hResolved_RecoJet_H1_b1_eta",
              "hResolved_RecoJet_H1_b2_eta",
              "hResolved_RecoJet_H2_b1_eta",
              "hResolved_RecoJet_H2_b2_eta",
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
              "hResolved_RecoJet_InvMass_H1",
              "hResolved_RecoJet_InvMass_H2",
              "hResolved_RecoJet_InvMassRegressed_H1",
              "hResolved_RecoJet_InvMassRegressed_H2",
              "hResolved_RecoJet_DeltaR_H1_H2",
              "hResolved_RecoJet_DeltaEta_H1_H2",
              "hResolved_RecoJet_DeltaPhi_H1_H2",
              "hResolved_RecoJet_NJets",
              "hResolved_RecoJet_NFatJets",
              "hResolved_RecoJet_PFHT",
              "hResolved_RecoJet_NLooseBJets",
              "hResolved_RecoJet_NMediumBJets",
              "hResolved_RecoJet_NTightBJets",
              "hResolved_RecoJet_Jet1Pt",
              "hResolved_RecoJet_Jet2Pt",
              "hResolved_RecoJet_Jet3Pt",
              "hResolved_RecoJet_Jet4Pt",
              "hResolved_RecoJet_Jet1Eta",
              "hResolved_RecoJet_Jet2Eta",
              "hResolved_RecoJet_Jet3Eta",
              "hResolved_RecoJet_Jet4Eta",
              "hResolved_RecoJet_AK8Jet1Pt",
              "hResolved_RecoJet_AK8Jet2Pt",
              "hResolved_RecoJet_AK8Jet3Pt",
              ]
    '''
    for h in histos:
        print(h)
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
        if "NJets" in h or "NFatJets" in h or "NLoose" in h or "NMedium" in h or "NTight" in h:
            h0.GetYaxis().SetTitle("Events")
            h0.GetXaxis().SetRangeUser(0, 10)
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
        
        h1 = f.Get("GluGluToHHTo4B_node_cHHH1/"+h)
        if "NJets" in h or "NFatJets" in h or "NLoose" in h or "NMedium" in h or "NTight" in h:
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
        if "NJets" in h or "NFatJets" in h or "NLoose" in h or "NMedium" in h or "NTight" in h:
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
        h5.SetMarkerStyle(23)

        if "NJets" in h or "NFatJets" in h or "NLoose" in h or "NMedium" in h or "NTight" in h:
            h1.GetYaxis().SetTitle("Events")
            h1.GetXaxis().SetRangeUser(0, 10)

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

        if "Resolved" in h and "RecoJet" in h:
            if "H1_b1_pt" in h or "H2_b1_pt" in h or "H1_b2_pt" in h or "H2_b2_pt" in h:
                h1.GetXaxis().SetRangeUser(0, 350)

        # Add a line to the first histograms
        if "_btag" in h:
            if "subjet" in h:
                lineL = ROOT.TLine(0.1241, 0.0, 0.1241, h1.GetMaximum())
                lineM = ROOT.TLine(0.4184, 0.0, 0.4185, h1.GetMaximum())
                lineL.SetLineColor(ROOT.kGray)
                lineM.SetLineColor(ROOT.kGray+2)
                lineL.SetLineStyle(4)
                lineM.SetLineStyle(4)
                lineL.Draw("same")
                lineM.Draw("same")
            else:
                lineL = ROOT.TLine(0.0490, 0.0, 0.0490, h1.GetMaximum())
                lineM = ROOT.TLine(0.2770, 0.0, 0.2770, h1.GetMaximum())
                lineT = ROOT.TLine(0.7264, 0.0, 0.7264, h1.GetMaximum())
                lineL.SetLineColor(ROOT.kGray)
                lineM.SetLineColor(ROOT.kGray+2)
                lineT.SetLineColor(ROOT.kGray+4)
                lineL.SetLineStyle(4)
                lineM.SetLineStyle(4)
                lineT.SetLineStyle(4)
                lineL.Draw("same")
                lineM.Draw("same")
                lineT.Draw("same")
                
        # Update canvas
        d.Modified()
        d.Update()
        #d.SetLogy()
        
        # Save plot
        for s in args.formats:
            saveName = os.path.join(args.path, "%s%s" % (h, s))
            d.SaveAs(saveName)
    '''
     
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Boosted and Semiresolved histograms
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    histos = [
        "hBoostedExcl_GenFatJet_H1_pt",
        "hBoostedExcl_GenFatJet_H2_pt",
        "hBoostedExcl_GenFatJet_H1_eta",
        "hBoostedExcl_GenFatJet_H2_eta",
        "hBoostedExcl_RecoFatJet_H1_pt",
        "hBoostedExcl_RecoFatJet_H2_pt",
        "hBoostedExcl_RecoFatJet_H1_eta",
        "hBoostedExcl_RecoFatJet_H2_eta",
        "hBoostedExcl_RecoFatJet_H1_TXbb",
        "hBoostedExcl_RecoFatJet_H2_TXbb",
        "hBoostedExcl_RecoFatJet_H1_m",
        "hBoostedExcl_RecoFatJet_H2_m",
        "hBoostedExcl_NJets",
        "hBoostedExcl_NFatJets",
        "hBoostedExcl_AK8PFHT",
        "hBoostedExcl_AK8Jet1Pt",
        "hBoostedExcl_AK8Jet2Pt",
        "hBoostedExcl_RecoFatJet_DeltaR_H1_H2",
        "hBoostedExcl_RecoFatJet_DeltaEta_H1_H2",
        "hBoostedExcl_RecoFatJet_DeltaPhi_H1_H2",
        "hBoostedExcl_RecoFatJet_H1_mSD_Uncorrected",
        "hBoostedExcl_RecoFatJet_H1_tau32",
        "hBoostedExcl_RecoFatJet_H1_nsubjets",
        "hBoostedExcl_RecoFatJet_H1_subjet1_pt",
        "hBoostedExcl_RecoFatJet_H1_subjet1_eta",
        "hBoostedExcl_RecoFatJet_H1_subjet1_m",
        "hBoostedExcl_RecoFatJet_H1_subjet1_btag",
        "hBoostedExcl_RecoFatJet_H1_subjet2_pt",
        "hBoostedExcl_RecoFatJet_H1_subjet2_eta",
        "hBoostedExcl_RecoFatJet_H1_subjet2_m",
        "hBoostedExcl_RecoFatJet_H1_subjet2_btag",
        "hBoostedExcl_RecoFatJet_H2_mSD_Uncorrected",
        "hBoostedExcl_RecoFatJet_H2_area",
        "hBoostedExcl_RecoFatJet_H2_tau32",
        "hBoostedExcl_RecoFatJet_H2_nsubjets",
        "hBoostedExcl_RecoFatJet_H2_subjet1_pt",
        "hBoostedExcl_RecoFatJet_H2_subjet1_eta",
        "hBoostedExcl_RecoFatJet_H2_subjet1_m",
        "hBoostedExcl_RecoFatJet_H2_subjet1_btag",
        "hBoostedExcl_RecoFatJet_H2_subjet2_pt",
        "hBoostedExcl_RecoFatJet_H2_subjet2_eta",
        "hBoostedExcl_RecoFatJet_H2_subjet2_m",
        "hBoostedExcl_RecoFatJet_H2_subjet2_btag",
        
        "hSemiresolvedExcl_H1Boosted_H2resolved_GenFatJet_H1_pt",
        "hSemiresolvedExcl_H1Boosted_H2resolved_GenFatJet_H1_eta",
        "hSemiresolvedExcl_H1Boosted_H2resolved_GenJet_H2_b1_pt",
        "hSemiresolvedExcl_H1Boosted_H2resolved_GenJet_H2_b1_eta",
        "hSemiresolvedExcl_H1Boosted_H2resolved_GenJet_H2_b2_pt",
        "hSemiresolvedExcl_H1Boosted_H2resolved_GenJet_H2_b2_eta",
        "hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_pt",
        "hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_eta",
        "hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_m",
        "hSemiresolvedExcl_H1Boosted_H2resolved_RecoJet_H2_b1_pt",
        "hSemiresolvedExcl_H1Boosted_H2resolved_RecoJet_H2_b1_btag",
        "hSemiresolvedExcl_H1Boosted_H2resolved_RecoJet_H2_b2_pt",
        "hSemiresolvedExcl_H1Boosted_H2resolved_RecoJet_H2_b2_btag",
        "hSemiresolvedExcl_H1Boosted_H2resolved_RecoJet_H2_b1_eta",
        "hSemiresolvedExcl_H1Boosted_H2resolved_RecoJet_H2_b2_eta",
        "hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_mSD_Uncorrected",
        "hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_area",
        "hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_n2b1",
        "hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_n3b1",
        "hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_tau21",
        "hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_tau32",
        "hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_nsubjets",
        "hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_pt",
        "hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_eta",
        "hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_btag",
        "hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_m",
        "hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_pt",
        "hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_eta",
        "hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_btag",
        "hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_m",
        "hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_TXbb",
        "hSemiresolvedExcl_H1Boosted_H2resolved_H2_pt",
        "hSemiresolvedExcl_H1Boosted_H2resolved_H2_eta",
        "hSemiresolvedExcl_H1Boosted_H2resolved_NJets",
        "hSemiresolvedExcl_H1Boosted_H2resolved_NFatJets",
        "hSemiresolvedExcl_H1Boosted_H2resolved_PFHT",
        "hSemiresolvedExcl_H1Boosted_H2resolved_NLooseBJets",
        "hSemiresolvedExcl_H1Boosted_H2resolved_NMediumBJets",
        "hSemiresolvedExcl_H1Boosted_H2resolved_NTightBJets",
        "hSemiresolvedExcl_H1Boosted_H2resolved_Jet1Pt",
        "hSemiresolvedExcl_H1Boosted_H2resolved_Jet2Pt",
        "hSemiresolvedExcl_H1Boosted_H2resolved_Jet3Pt",
        "hSemiresolvedExcl_H1Boosted_H2resolved_Jet4Pt",
        "hSemiresolvedExcl_H1Boosted_H2resolved_Jet1Eta",
        "hSemiresolvedExcl_H1Boosted_H2resolved_Jet2Eta",
        "hSemiresolvedExcl_H1Boosted_H2resolved_Jet3Eta",
        "hSemiresolvedExcl_H1Boosted_H2resolved_Jet4Eta",
        "hSemiresolvedExcl_H1Boosted_H2resolved_AK8PFHT",
        "hSemiresolvedExcl_H1Boosted_H2resolved_AK8Jet1Pt",
        
        "hSemiresolvedExcl_H1Boosted_H2resolved_DeltaR_H1_H2",
        "hSemiresolvedExcl_H1Boosted_H2resolved_DeltaEta_H1_H2",
        "hSemiresolvedExcl_H1Boosted_H2resolved_DeltaPhi_H1_H2",
        "hSemiresolvedExcl_H1Boosted_H2resolved_InvMass_H2",
        "hSemiresolvedExcl_H1Boosted_H2resolved_InvMassRegressed_H2",
        
        
        "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_GenFatJet_H1_pt",
        "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_GenFatJet_H1_eta",
        "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_GenJet_H2_b1_pt",
        "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_GenJet_H2_b1_eta",
        "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_GenJet_H2_b2_pt",
        "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_GenJet_H2_b2_eta",
        "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_pt",
        "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_eta",
        "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_m",
        "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoJet_H2_b1_pt",
        "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoJet_H2_b2_pt",
        "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoJet_H2_b1_btag",
        "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoJet_H2_b2_btag",
        "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoJet_H2_b1_eta",
        "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoJet_H2_b2_eta",
        "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_mSD_Uncorrected",
        "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_area",
        "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_n2b1",
        "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_n3b1",
        "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_tau21",
        "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_tau32",
        "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_nsubjets",
        "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_pt",
        "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_eta",
        "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_btag",
        "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_m",
        "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_pt",
        "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_eta",
        "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_btag",
        "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_m",
        "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_TXbb",
        "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_H2_pt",
        "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_H2_eta",
        "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_NJets",
        "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_NFatJets",
        "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_PFHT",
        "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_NLooseBJets",
        "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_NMediumBJets",
        "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_NTightBJets",
        "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_Jet1Pt",
        "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_Jet2Pt",
        "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_Jet3Pt",
        "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_Jet4Pt",
        "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_Jet1Eta",
        "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_Jet2Eta",
        "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_Jet3Eta",
        "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_Jet4Eta",
        "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_AK8PFHT",
        "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_AK8Jet1Pt",
        "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_AK8Jet2Pt",
        "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_DeltaR_H1_H2",
        "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_DeltaEta_H1_H2",
        "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_DeltaPhi_H1_H2",
        "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_InvMass_H2",
        "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_InvMassRegressed_H2",
        ]

    for h in histos:
        
        print("histogram %s" % (h))
        ROOT.gStyle.SetOptStat(0)
        ROOT.gStyle.SetTextFont(42)
        
        d = ROOT.TCanvas("", "", 800, 700)
        d.SetLeftMargin(0.15)
        
        legend = ROOT.TLegend(0.55, 0.70, 0.95, 0.88)
        legend.SetFillColor(0)
        legend.SetFillStyle(0)
        legend.SetBorderSize(0)
        legend.SetTextSize(0.03)
        if "Semiresolved" in h:
            legend.SetHeader("semi-resolved")
        elif "Boosted" in h:
            legend.SetHeader("boosted")

        opts = GetOpts(h)
        maxY = -1.0
        
        '''
        h0 = f.Get("GluGluToHHTo4B_node_cHHH0/"+h) 
        if "NJets" in h or "NFatJets" in h or "NLoose" in h or "NMedium" in h or "NTight" in h:
            h0.GetYaxis().SetTitle("Events")
        else:
            h0.GetYaxis().SetTitle("Arbitrary Units")
            h0.Scale(1.0/h0.Integral())
            h0.Rebin(4)
        if h0.GetMaximum() > maxY:
            maxY = h0.GetMaximum()
        h0.SetTitle("")
        h0.GetXaxis().SetRangeUser(opts["xmin"], opts["xmax"])
        h0.SetLineColor(ROOT.kRed+1)
        h0.SetMarkerColor(ROOT.kRed+1)
        h0.SetMarkerSize(1.05)
        h0.SetMarkerStyle(20)
        '''
        
        h1 = f.Get("GluGluToHHTo4B_node_cHHH1/"+h)
        if "NJets" in h or "NFatJets" in h or "NLoose" in h or "NMedium" in h or "NTight" in h or "nsubjets" in h:
            h1.GetYaxis().SetTitle("Events")
        else:
            h1.GetYaxis().SetTitle("Arbitrary Units")
            h1.Scale(1.0/h1.Integral())
        h1.SetTitle("")
        if "subjet1_pt" in h or "subjet2_pt" in h:
            h1.Rebin(5)
        elif  "subjet1_btag" in h or "subjet2_btag" in h or "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_PFHT" in h or "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_Jet1Pt" in h or "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_Jet2Pt" in h or "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_Jet3Pt" in h or "hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_Jet4Pt" in h:
            h1.Rebin(2)
            
        #if "AK8PFHT" in h:
        #    h1.GetXaxis().SetRangeUser(0, 2000)
        #elif "Semiresolved" in h and ("RecoFatJet_H1_pt" in h or "RecoFatJet_H2_pt" in h):
        #    h1.GetXaxis().SetRangeUser(0, 1000)
        #else:
        #    h1.GetXaxis().SetRangeUser(opts["xmin"], opts["xmax"])
        if (h1.GetMaximum() > maxY):
            maxY = h1.GetMaximum()
        h1.SetLineColor(ROOT.kBlue)
        h1.SetMarkerSize(1.05)
        h1.SetMarkerColor(ROOT.kBlue)
        h1.SetFillColorAlpha(ROOT.kBlue, 0.60)
        h1.SetFillStyle(3001)
        
        '''
        h2 = f.Get("GluGluToHHTo4B_node_cHHH2p45/"+h)
        if "NJets" in h or "NFatJets" in h or "NLoose" in h or "NMedium" in h or "NTight" in h:
            h2.GetYaxis().SetTitle("Events")
        else:
            h2.GetYaxis().SetTitle("Arbitrary Units")
            h2.Scale(1.0/h2.Integral())
            h2.Rebin(4)

        if (h2.GetMaximum() > maxY):
            maxY = h2.GetMaximum()
        h2.SetTitle("")
        h2.GetXaxis().SetRangeUser(opts["xmin"], opts["xmax"])
        h2.SetLineColor(ROOT.kGreen+2)
        h2.SetMarkerSize(1.05)
        h2.SetMarkerColor(ROOT.kGreen+2)
        h2.SetMarkerStyle(21)
        
        #h5 = f.Get("GluGluToHHTo4B_node_cHHH5/"+h)
        #if "NJets" in h or "NFatJets" in h:
        #    h5.GetYaxis().SetTitle("Events")
        #else:
        #    h5.GetYaxis().SetTitle("Arbitrary Units")
        #    h5.Scale(1.0/h5.Integral())
        #if (h5.GetMaximum() > maxY):
        #    maxY = h5.GetMaximum()
        #h5.SetTitle("")
        #h5.GetXaxis().SetRangeUser(opts["xmin"], opts["xmax"])
        #h5.SetLineColor(ROOT.kOrange+1)
        #h5.SetMarkerSize(1.05)
        #h5.SetMarkerColor(ROOT.kOrange+1)
        #h5.SetMarkerStyle(23)
        '''
        
        #h0.SetMaximum(maxY*opts["ymaxfactor"])
        h1.SetMaximum(maxY*opts["ymaxfactor"])
        h1.Draw("hist")
        #h0.Draw("same")
        #h2.Draw("same")
        #h5.Draw("same")
        
        #legend.AddEntry(h0, "ggHH BSM #kappa_{#lambda} = 0")
        legend.AddEntry(h1, "ggHH SM #kappa_{#lambda} = 1")
        #legend.AddEntry(h2, "ggHH BSM #kappa_{#lambda} = 2.45")
        #legend.AddEntry(h5, "ggHH BSM #kappa_{#lambda} = 5")
        legend.Draw("same")
            
        tex_cms = AddCMSText()
        tex_cms.Draw("same")
        
        tex_prelim = AddPreliminaryText()
        tex_prelim.Draw("same")
        
        header = ROOT.TLatex()
        header.SetTextSize(0.04)
        header.DrawLatexNDC(0.65, 0.92, "2018, #sqrt{s} = 13 TeV")
        
        # Add a line to the first histograms
        if "_btag" in h:
            if "subjet" in h:
                lineL = ROOT.TLine(0.1241, 0.0, 0.1241, h1.GetMaximum())
                lineM = ROOT.TLine(0.4184, 0.0, 0.4185, h1.GetMaximum())
                lineL.SetLineColor(ROOT.kGray)
                lineM.SetLineColor(ROOT.kGray+2)
                lineL.SetLineStyle(4)
                lineM.SetLineStyle(4)
                lineL.Draw("same")
                lineM.Draw("same")
            else:
                lineL = ROOT.TLine(0.0490, 0.0, 0.0490, h1.GetMaximum())
                lineM = ROOT.TLine(0.2770, 0.0, 0.2770, h1.GetMaximum())
                lineT = ROOT.TLine(0.7264, 0.0, 0.7264, h1.GetMaximum())
                lineL.SetLineColor(ROOT.kGray)
                lineM.SetLineColor(ROOT.kGray+2)
                lineT.SetLineColor(ROOT.kGray+4)
                lineL.SetLineStyle(4)
                lineM.SetLineStyle(4)
                lineT.SetLineStyle(4)
                lineL.Draw("same")
                lineM.Draw("same")
                lineT.Draw("same")
                
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
    STUDY       = "ControlPlotsExclusive"
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

#!/usr/bin/env python
'''
 USAGE:
./getTriggerEfficiencyPerLeg_Run3.py --year <year> -d <NTuple Directory>

LAST USED:
./getTriggerEfficiencyPerLeg_Run3.py --year 2022 -d Run3_Prompt2022_MuonEG_PNetHLT
'''
#===================================
# Import modules
#===================================
from argparse import ArgumentParser
import socket
import os
import re
import sys
import subprocess
import ROOT
import socket
import getpass
import time
import datetime
ROOT.gROOT.SetBatch(True)

import array

def Verbose(msg, printHeader=False):
    '''
    Calls Print() only if verbose options is set to true.
    '''
    if not args.verbose:
        return
    print(msg)
    return

def GetHostname():
    return socket.gethostname()

def Execute(cmd):
    '''
    Executes a given command and return the output.
    '''
    Verbose("Executing command: %s" % (cmd), True)
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
    stdin  = p.stdout
    stdout = p.stdout
    ret    = []
    for line in stdout:
        ret.append(line.decode("utf-8").replace("\n", ""))
    stdout.close()
    return ret

def AddCMSText(setx=0.19, sety=0.95):
    texcms = ROOT.TLatex(0.,0., 'CMS');
    texcms.SetNDC();
    texcms.SetTextAlign(31);
    texcms.SetX(setx);
    texcms.SetY(sety);
    texcms.SetTextFont(63);
    texcms.SetLineWidth(2);
    texcms.SetTextSize(30);
    return texcms

def AddPrivateWorkText(setx=0.20, sety=0.95):
    tex = ROOT.TLatex(0.,0., 'Private Work');
    tex.SetNDC();
    tex.SetX(setx);
    tex.SetY(sety);
    tex.SetTextFont(53);
    tex.SetTextSize(28);
    tex.SetLineWidth(2)
    return tex

def AddPreliminaryText(setx=0.20, sety=0.95):
    tex = ROOT.TLatex(0.,0., 'Preliminary');
    tex.SetNDC();
    tex.SetX(setx);
    tex.SetY(sety);
    tex.SetTextFont(53);
    tex.SetTextSize(28);
    tex.SetLineWidth(2)
    return tex

def CreateLegend(opts):
    
    # Default position on canvas
    x0 = 0.85
    y0 = 0.45
    y1 = 0.20
    x1 = 0.35
    
    legend = ROOT.TLegend(x0, x1, y0, y1)
    if opts["legend"]["move"] == True:
        dx = float(opts["legend"]["dx"])
        dy = float(opts["legend"]["dy"])
        legend = ROOT.TLegend(x0+dx, x1+dx, y0+dy, y1+dy)
    else:
        pass

    legend.SetFillColor(0)
    legend.SetFillStyle(0)
    legend.SetBorderSize(0)
    legend.SetTextSize(float(opts["legend"]["size"]))
    if opts["legend"]["header"] is not None:
        legend.SetHeader(str(opts["legend"]["header"]))
    return legend

def GetOpts(h):
    
    opts = {}
    opts["formats"]    = args.formats
    opts["path"]       = args.path
    opts["xmin"]       = 0.0
    opts["xmax"]       = 1500.0
    opts["nbins"]      = 150
    opts["xlabel"]     = "M_{X} [GeV]"
    opts["ymaxfactor"] = 1.1
    opts["legend"] = {"move": False, "dx": -0.15, "dy": +0.3, "size":0.03, "header": None}
    
    if "filterht" in h.lower():
        opts["xmax"] = 1500
    elif "btagcalo" in h.lower() or "btagpfdeepcsv" in h.lower():
        opts["xmax"] = 1.0
    

    return opts

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

def plotComparison(hName, hRef, others):
    
    # Canvas and general style options
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetTextFont(42)
    
    d = ROOT.TCanvas("", "", 800, 700)
    d.SetLeftMargin(0.12)
    
    opts = GetOpts(hName)
    opts["legend"]["header"] = hName.split("_")[-1]
    legend = CreateLegend(opts)
    
    hRef.SetTitle("")
    #hRef.GetXaxis().SetTitle(opts["xlabel"])
    hRef.GetXaxis().SetTitleSize(0.04)
    hRef.GetYaxis().SetTitle("Online Efficiency")
    hRef.GetXaxis().SetRangeUser(opts["xmin"], opts["xmax"])
    hRef.GetYaxis().SetRangeUser(0.0, 1.1)
    hRef.GetYaxis().SetTitleSize(0.04)
    hRef.SetLineWidth(2)
    hRef.SetMarkerStyle(20)
    
    hRef.Draw()

    for hOther in others:
        hOther.Draw("same")
        if "TTbar" in hOther.GetName():
            legend.AddEntry(hOther, "t#bar{t}")
        elif "NMSSM" in hOther.GetName():
            legend.AddEntry(hOther, "NMSSM X#rightarrow YH#rightarrow H,HH #rightarrow 6b")
    
    legend.AddEntry(hRef, "Single #mu data")
    legend.Draw("same")
    
    tex_cms = AddCMSText(setx=0.20, sety=0.91)
    tex_cms.Draw("same")

    tex_prelim = AddPreliminaryText(setx=0.21, sety=0.91)
    tex_prelim.Draw("same")

    header = ROOT.TLatex()
    header.SetTextSize(0.04)
    header.DrawLatexNDC(0.65, 0.91, "59.74 fb^{-1} (13 TeV)")
    
    # Update canvas
    d.Modified()
    d.Update()

    # Save histogram
    for f in opts["formats"]:
        savePath = getPublicPath()
        saveName = os.path.join(opts["path"], "%s%s" % (hName, f))
        print(saveName)
        d.SaveAs(saveName)
        
    d.Close()
    return

def GetColor(sampleName):
    colors = {
        "MuonEG"     : ROOT.kBlack,
        "SingleMuon" : ROOT.kBlack,
        "TTbar"      : ROOT.kBlue, 
        "NMSSM"      : ROOT.kRed,
        }
    return colors[sampleName]

def GetPNetEfficiencies22(f, sampleName):
    
    print("\n ======= Processing sample : %s" % (sampleName))
        
    # Read the tree
    t = f.Get("TrgTree")
    
    t.SetAlias("FourPixelOnlyPFCentralJetTightIDPt20", "4PixelOnlyPFCentralJetTightIDPt20")
    t.SetAlias("ThreePixelOnlyPFCentralJetTightIDPt30", "3PixelOnlyPFCentralJetTightIDPt30")
    t.SetAlias("TwoPixelOnlyPFCentralJetTightIDPt40", "2PixelOnlyPFCentralJetTightIDPt40")
    t.SetAlias("OnePixelOnlyPFCentralJetTightIDPt60", "1PixelOnlyPFCentralJetTightIDPt60")
    
    t.SetAlias("OnePFCentralJetTightIDPt70", "1PFCentralJetTightIDPt70")
    t.SetAlias("TwoPFCentralJetTightIDPt50", "2PFCentralJetTightIDPt50")
    t.SetAlias("ThreePFCentralJetTightIDPt40", "3PFCentralJetTightIDPt40")
    t.SetAlias("FourPFCentralJetTightIDPt35", "4PFCentralJetTightIDPt35")

    nentries = t.GetEntries()
    
    print("Number of entries : %s" % (nentries))
    
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Book the histograms
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    bins_pt   = [35, 40, 45, 50, 55, 60, 65, 70, 80, 100]
    bins_HT   = [300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 850, 1000, 1200, 1600]
    bins_bDisc = [0.65, 0.67, 0.69, 0.71, 0.73, 0.75, 0.77, 0.79, 0.81, 0.83, 0.85, 0.87, 0.89, 0.91, 0.93, 0.95, 0.97, 0.99, 1.0]
    
    bins2D_HT    = [300, 400, 500, 600, 700, 850, 1000, 1500]
    bins2D_bDisc = [0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.0] 

    #-----------------------------------------------------------
    # Baseline selections:
    #-----------------------------------------------------------
    h_PFHT       = ROOT.TH1F("h_PFHT_%s" % (sampleName),       "; Offline PF H_{T} [GeV]; #varepsilon_{L1+HLT}", len(bins_HT)-1, array.array("d", bins_HT))
    h_ForthJetPt = ROOT.TH1F("h_ForthJetPt_%s" % (sampleName), "; Offline p_{T}^{4th jet} [GeV]; #varepsilon_{L1+HLT}", len(bins_pt)-1, array.array("d", bins_pt))
    h_NJets      = ROOT.TH1F("h_NJets_%s" % (sampleName),      "; Jet multiplicity; #varepsilon_{L1+HLT}", 8, 4, 12)
    h_MeanBTag   = ROOT.TH1F("h_MeanBTag_%s" % (sampleName),   "; Mean PNet score (j^{ldg btag}, j^{subldg btag}); #varepsilon_{L1+HLT}", len(bins_bDisc)-1, array.array("d", bins_bDisc))
    h_NBJets     = ROOT.TH1F("h_NBJets_%s" % (sampleName),     "; Medium b-jet multiplicity; #varepsilon_{L1+HLT}", 4, 1, 5)

    h_PFHT_Passed_L1 = ROOT.TH1F("h_PFHT_Passed_L1_%s" % (sampleName), "; Offline PF H_{T} [GeV]; #varepsilon_{L1}", len(bins_HT)-1, array.array("d", bins_HT))
    h_ForthJetPt_Passed_L1 = ROOT.TH1F("h_ForthJetPt_Passed_L1_%s" % (sampleName), "; Offline p_{T}^{4th jet} [GeV]; #varepsilon_{L1}", len(bins_pt)-1, array.array("d", bins_pt))
    
    h_PFHT_Passed_FullPath       = ROOT.TH1F("h_PFHT_Passed_FullPath_%s" % (sampleName),       "; Offline PF H_{T} [GeV]; #varepsilon_{L1+HLT}", len(bins_HT)-1, array.array("d", bins_HT))
    h_ForthJetPt_Passed_FullPath = ROOT.TH1F("h_ForthJetPt_Passed_FullPath_%s" % (sampleName), "; Offline p_{T}^{4th jet} [GeV]; #varepsilon_{L1+HLT}", len(bins_pt)-1, array.array("d", bins_pt))
    h_NJets_Passed_FullPath      = ROOT.TH1F("h_NJets_Passed_FullPath_%s" % (sampleName),      "; Jet multiplicity; #varepsilon_{L1+HLT}", 8, 4, 12)
    h_MeanBTag_Passed_FullPath   = ROOT.TH1F("h_MeanBTag_Passed_FullPath_%s" % (sampleName),   "; Mean PNet score (j^{ldg btag}, j^{subldg btag}); #varepsilon_{L1+HLT}", len(bins_bDisc)-1,array.array("d", bins_bDisc))
    h_NBJets_Passed_FullPath     = ROOT.TH1F("h_NBJets_Passed_FullPath_%s" % (sampleName),     "; Medium b-jet multiplicity; #varepsilon_{L1+HLT}", 4, 1, 5)
    
    h_PFHT_vs_MeanBTag = ROOT.TH2F("h_PFHT_vs_MeanBTag_%s" % (sampleName), "; Offline PF H_{T} [GeV]; Mean PNet score (j^{ldg btag}, j^{subldg btag}); #varepsilon_{L1+HLT}", len(bins2D_HT)-1, array.array("d", bins2D_HT), len(bins2D_bDisc)-1, array.array("d", bins2D_bDisc))
    h_PFHT_vs_MeanBTag_Passed_FullPath = ROOT.TH2F("h_PFHT_vs_MeanBTag_Passed_FullPath_%s" % (sampleName), "; Offline PF H_{T} [GeV]; Mean PNet score (j^{ldg btag}, j^{subldg btag}); #varepsilon_{L1+HLT}", len(bins2D_HT)-1, array.array("d", bins2D_HT), len(bins2D_bDisc)-1, array.array("d", bins2D_bDisc))
    
    h_PFHT_vs_ForthJetPt = ROOT.TH2F("h_PFHT_vs_ForthJetPt_%s" % (sampleName), "; Offline PF H_{T} [GeV]; Offline p_{T}^{4th jet} [GeV]; #varepsilon_{L1+HLT}", len(bins2D_HT)-1, array.array("d", bins2D_HT), len(bins_pt)-1, array.array("d", bins_pt))
    h_PFHT_vs_ForthJetPt_Passed_FullPath = ROOT.TH2F("h_PFHT_vs_ForthJetPt_Passed_FullPath_%s" % (sampleName), "; Offline PF H_{T} [GeV]; Offline p_{T}^{4th jet} [GeV]; #varepsilon_{L1+HLT}", len(bins2D_HT)-1, array.array("d", bins2D_HT),len(bins_pt)-1, array.array("d", bins_pt))
    
    #---------------------------------------------------------
    # Selections 2BTagM
    #-----------------------------------------------------------
    h_PFHT_2BTagM       = ROOT.TH1F("h_PFHT_2BTagM_%s" % (sampleName),       "; Offline PF H_{T} [GeV]; #varepsilon_{L1+HLT}", len(bins_HT)-1, array.array("d", bins_HT))
    h_ForthJetPt_2BTagM = ROOT.TH1F("h_ForthJetPt_2BTagM_%s" % (sampleName), "; Offline p_{T}^{4th jet} [GeV]; #varepsilon_{L1+HLT}", len(bins_pt)-1, array.array("d", bins_pt)) 
    h_NJets_2BTagM      = ROOT.TH1F("h_NJets_2BTagM_%s" % (sampleName),      "; Jet multiplicity; #varepsilon_{L1+HLT}", 8, 4, 12)
    h_MeanBTag_2BTagM   = ROOT.TH1F("h_MeanBTag_2BTagM_%s" % (sampleName),   "; Mean PNet score (j^{ldg btag}, j^{subldg btag}); #varepsilon_{L1+HLT}", len(bins_bDisc)-1, array.array("d", bins_bDisc))
    h_NBJets_2BTagM     = ROOT.TH1F("h_NBJets_2BTagM_%s" % (sampleName),     "; Medium b-jet multiplicity; #varepsilon_{L1+HLT}", 4, 1, 5)
    
    h_PFHT_2BTagM_Passed_FullPath = ROOT.TH1F("h_PFHT_2BTagM_Passed_FullPath_%s" % (sampleName), "; Offline PF H_{T} [GeV]; #varepsilon_{L1+HLT}", len(bins_HT)-1, array.array("d", bins_HT))
    h_ForthJetPt_2BTagM_Passed_FullPath = ROOT.TH1F("h_ForthJetPt_2BTagM_Passed_FullPath_%s" % (sampleName), "; Offline p_{T}^{4th jet} [GeV]; #varepsilon_{L1+HLT}", len(bins_pt)-1, array.array("d", bins_pt))
    h_NJets_2BTagM_Passed_FullPath = ROOT.TH1F("h_NJets_2BTagM_Passed_FullPath_%s" % (sampleName), "; Jet multiplicity; #varepsilon_{L1+HLT}", 8, 4, 12)
    h_MeanBTag_2BTagM_Passed_FullPath = ROOT.TH1F("h_MeanBTag_2BTagM_Passed_FullPath_%s" % (sampleName), "; Mean PNet score (j^{ldg btag}, j^{subldg btag}); #varepsilon_{L1+HLT}", len(bins_bDisc)-1, array.array("d", bins_bDisc))
    h_NBJets_2BTagM_Passed_FullPath = ROOT.TH1F("h_NBJets_2BTagM_Passed_FullPath_%s" % (sampleName), "; Medium b-jet multiplicity; #varepsilon_{L1+HLT}", 4, 1, 5)
    

    h_PFHT_vs_MeanBTag_2BTagM = ROOT.TH2F("h_PFHT_vs_MeanBTag_2BTagM_%s" % (sampleName), "; Offline PF H_{T} [GeV]; Mean PNet score (j^{ldg btag}, j^{subldg btag}); #varepsilon_{L1+HLT}", len(bins2D_HT)-1, array.array("d", bins2D_HT), len(bins2D_bDisc)-1, array.array("d", bins2D_bDisc))
    h_PFHT_vs_MeanBTag_2BTagM_Passed_FullPath = ROOT.TH2F("h_PFHT_vs_MeanBTag_2BTagM_Passed_FullPath_%s" % (sampleName), "; Offline PF H_{T} [GeV]; Mean PNet score (j^{ldg btag}, j^{subldg btag}); #varepsilon_{L1+HLT}", len(bins2D_HT)-1, array.array("d", bins2D_HT), len(bins2D_bDisc)-1, array.array("d", bins2D_bDisc))
    
    h_PFHT_vs_ForthJetPt_2BTagM = ROOT.TH2F("h_PFHT_vs_ForthJetPt_2BTagM_%s" % (sampleName), "; Offline PF H_{T} [GeV]; Offline p_{T}^{4th jet} [GeV]; #varepsilon_{L1+HLT}", len(bins2D_HT)-1, array.array("d", bins2D_HT), len(bins_pt)-1, array.array("d", bins_pt))
    h_PFHT_vs_ForthJetPt_2BTagM_Passed_FullPath = ROOT.TH2F("h_PFHT_vs_ForthJetPt_2BTagM_Passed_FullPath_%s" % (sampleName), "; Offline PF H_{T} [GeV]; Offline p_{T}^{4th jet} [GeV]; #varepsilon_{L1+HLT}", len(bins2D_HT)-1, array.array("d", bins2D_HT),len(bins_pt)-1, array.array("d", bins_pt))
    
    #---------------------------------------------------------
    # Selections 2BTagM + PFHT cut
    #-----------------------------------------------------------
    h_PFHT_2BTagM_PFHT400       = ROOT.TH1F("h_PFHT_2BTagM_PFHT400_%s" % (sampleName),       "; Offline PF H_{T} [GeV]; #varepsilon_{L1+HLT}", len(bins_HT)-1, array.array("d", bins_HT))
    h_ForthJetPt_2BTagM_PFHT400 = ROOT.TH1F("h_ForthJetPt_2BTagM_PFHT400_%s" % (sampleName), "; Offline p_{T}^{4th jet} [GeV]; #varepsilon_{L1+HLT}", len(bins_pt)-1, array.array("d", bins_pt)) 
    h_NJets_2BTagM_PFHT400      = ROOT.TH1F("h_NJets_2BTagM_PFHT400_%s" % (sampleName),      "; Jet multiplicity; #varepsilon_{L1+HLT}", 8, 4, 12)
    h_MeanBTag_2BTagM_PFHT400   = ROOT.TH1F("h_MeanBTag_2BTagM_PFHT400_%s" % (sampleName),   "; Mean PNet score (j^{ldg btag}, j^{subldg btag}); #varepsilon_{L1+HLT}", len(bins_bDisc)-1, array.array("d", bins_bDisc))
    h_NBJets_2BTagM_PFHT400     = ROOT.TH1F("h_NBJets_2BTagM_PFHT400_%s" % (sampleName),     "; Medium b-jet multiplicity; #varepsilon_{L1+HLT}", 4, 1, 5)
    
    h_PFHT_2BTagM_PFHT400_Passed_FullPath = ROOT.TH1F("h_PFHT_2BTagM_PFHT400_Passed_FullPath_%s" % (sampleName), "; Offline PF H_{T} [GeV]; #varepsilon_{L1+HLT}", len(bins_HT)-1, array.array("d", bins_HT))
    h_ForthJetPt_2BTagM_PFHT400_Passed_FullPath = ROOT.TH1F("h_ForthJetPt_2BTagM_PFHT400_Passed_FullPath_%s" % (sampleName), "; Offline p_{T}^{4th jet} [GeV]; #varepsilon_{L1+HLT}", len(bins_pt)-1, array.array("d", bins_pt))
    h_NJets_2BTagM_PFHT400_Passed_FullPath = ROOT.TH1F("h_NJets_2BTagM_PFHT400_Passed_FullPath_%s" % (sampleName), "; Jet multiplicity; #varepsilon_{L1+HLT}", 8, 4, 12)
    h_MeanBTag_2BTagM_PFHT400_Passed_FullPath = ROOT.TH1F("h_MeanBTag_2BTagM_PFHT400_Passed_FullPath_%s" % (sampleName), "; Mean PNet score (j^{ldg btag}, j^{subldg btag}); #varepsilon_{L1+HLT}", len(bins_bDisc)-1, array.array("d", bins_bDisc))
    h_NBJets_2BTagM_PFHT400_Passed_FullPath = ROOT.TH1F("h_NBJets_2BTagM_PFHT400_Passed_FullPath_%s" % (sampleName), "; Medium b-jet multiplicity; #varepsilon_{L1+HLT}", 4, 1, 5)
    
    h_PFHT_vs_MeanBTag_2BTagM_PFHT400 = ROOT.TH2F("h_PFHT_vs_MeanBTag_2BTagM_PFHT400_%s" % (sampleName), "; Offline PF H_{T} [GeV]; Mean PNet score (j^{ldg btag}, j^{subldg btag}); #varepsilon_{L1+HLT}", len(bins2D_HT)-1, array.array("d", bins2D_HT), len(bins2D_bDisc)-1, array.array("d", bins2D_bDisc))
    h_PFHT_vs_MeanBTag_2BTagM_PFHT400_Passed_FullPath = ROOT.TH2F("h_PFHT_vs_MeanBTag_2BTagM_PFHT400_Passed_FullPath_%s" % (sampleName), "; Offline PF H_{T} [GeV]; Mean PNet score (j^{ldg btag}, j^{subldg btag}); #varepsilon_{L1+HLT}", len(bins2D_HT)-1, array.array("d", bins2D_HT), len(bins2D_bDisc)-1, array.array("d", bins2D_bDisc))
    
    h_PFHT_vs_ForthJetPt_2BTagM_PFHT400 = ROOT.TH2F("h_PFHT_vs_ForthJetPt_2BTagM_PFHT400_%s" % (sampleName), "; Offline PF H_{T} [GeV]; Offline p_{T}^{4th jet} [GeV]; #varepsilon_{L1+HLT}", len(bins2D_HT)-1, array.array("d", bins2D_HT), len(bins_pt)-1, array.array("d", bins_pt))
    h_PFHT_vs_ForthJetPt_2BTagM_PFHT400_Passed_FullPath = ROOT.TH2F("h_PFHT_vs_ForthJetPt_2BTagM_PFHT400_Passed_FullPath_%s" % (sampleName), "; Offline PF H_{T} [GeV]; Offline p_{T}^{4th jet} [GeV]; #varepsilon_{L1+HLT}", len(bins2D_HT)-1, array.array("d", bins2D_HT),len(bins_pt)-1, array.array("d", bins_pt))
    
    #---------------------------------------------------------
    # Selections 3BTagM
    #-----------------------------------------------------------
    h_PFHT_3BTagM       = ROOT.TH1F("h_PFHT_3BTagM_%s" % (sampleName),       "; Offline PF H_{T} [GeV]; #varepsilon_{L1+HLT}", len(bins_HT)-1, array.array("d", bins_HT))
    h_ForthJetPt_3BTagM = ROOT.TH1F("h_ForthJetPt_3BTagM_%s" % (sampleName), "; Offline p_{T}^{4th jet} [GeV]; #varepsilon_{L1+HLT}", len(bins_pt)-1, array.array("d", bins_pt)) 
    h_NJets_3BTagM      = ROOT.TH1F("h_NJets_3BTagM_%s" % (sampleName),      "; Jet multiplicity; #varepsilon_{L1+HLT}", 8, 4, 12)
    h_MeanBTag_3BTagM   = ROOT.TH1F("h_MeanBTag_3BTagM_%s" % (sampleName),   "; Mean PNet score (j^{ldg btag}, j^{subldg btag}); #varepsilon_{L1+HLT}", len(bins_bDisc)-1, array.array("d", bins_bDisc))
    h_NBJets_3BTagM     = ROOT.TH1F("h_NBJets_3BTagM_%s" % (sampleName),     "; Medium b-jet multiplicity; #varepsilon_{L1+HLT}", 4, 1, 5)
    
    h_PFHT_3BTagM_Passed_FullPath = ROOT.TH1F("h_PFHT_3BTagM_Passed_FullPath_%s" % (sampleName), "; Offline PF H_{T} [GeV]; #varepsilon_{L1+HLT}", len(bins_HT)-1, array.array("d", bins_HT))
    h_ForthJetPt_3BTagM_Passed_FullPath = ROOT.TH1F("h_ForthJetPt_3BTagM_Passed_FullPath_%s" % (sampleName), "; Offline p_{T}^{4th jet} [GeV]; #varepsilon_{L1+HLT}", len(bins_pt)-1, array.array("d", bins_pt))
    h_NJets_3BTagM_Passed_FullPath = ROOT.TH1F("h_NJets_3BTagM_Passed_FullPath_%s" % (sampleName), "; Jet multiplicity; #varepsilon_{L1+HLT}", 8, 4, 12)
    h_MeanBTag_3BTagM_Passed_FullPath = ROOT.TH1F("h_MeanBTag_3BTagM_Passed_FullPath_%s" % (sampleName), "; Mean PNet score (j^{ldg btag}, j^{subldg btag}); #varepsilon_{L1+HLT}", len(bins_bDisc)-1, array.array("d", bins_bDisc))
    h_NBJets_3BTagM_Passed_FullPath = ROOT.TH1F("h_NBJets_3BTagM_Passed_FullPath_%s" % (sampleName), "; Medium b-jet multiplicity; #varepsilon_{L1+HLT}", 4, 1, 5)
    
    h_PFHT_vs_MeanBTag_3BTagM = ROOT.TH2F("h_PFHT_vs_MeanBTag_3BTagM_%s" % (sampleName), "; Offline PF H_{T} [GeV]; Mean PNet score (j^{ldg btag}, j^{subldg btag}); #varepsilon_{L1+HLT}", len(bins2D_HT)-1, array.array("d", bins2D_HT), len(bins2D_bDisc)-1, array.array("d", bins2D_bDisc))
    h_PFHT_vs_MeanBTag_3BTagM_Passed_FullPath = ROOT.TH2F("h_PFHT_vs_MeanBTag_3BTagM_Passed_FullPath_%s" % (sampleName), "; Offline PF H_{T} [GeV]; Mean PNet score (j^{ldg btag}, j^{subldg btag}); #varepsilon_{L1+HLT}", len(bins2D_HT)-1, array.array("d", bins2D_HT), len(bins2D_bDisc)-1, array.array("d", bins2D_bDisc))
    
    h_PFHT_vs_ForthJetPt_3BTagM = ROOT.TH2F("h_PFHT_vs_ForthJetPt_3BTagM_%s" % (sampleName), "; Offline PF H_{T} [GeV]; Offline p_{T}^{4th jet} [GeV]; #varepsilon_{L1+HLT}", len(bins2D_HT)-1, array.array("d", bins2D_HT), len(bins_pt)-1, array.array("d", bins_pt))
    h_PFHT_vs_ForthJetPt_3BTagM_Passed_FullPath = ROOT.TH2F("h_PFHT_vs_ForthJetPt_3BTagM_Passed_FullPath_%s" % (sampleName), "; Offline PF H_{T} [GeV]; Offline p_{T}^{4th jet} [GeV]; #varepsilon_{L1+HLT}", len(bins2D_HT)-1, array.array("d", bins2D_HT),len(bins_pt)-1, array.array("d", bins_pt))
    
    #---------------------------------------------------------
    # Selections 3BTagM + PFHT cut
    #-----------------------------------------------------------
    h_PFHT_3BTagM_PFHT400       = ROOT.TH1F("h_PFHT_3BTagM_PFHT400_%s" % (sampleName),       "; Offline PF H_{T} [GeV]; #varepsilon_{L1+HLT}", len(bins_HT)-1, array.array("d", bins_HT))
    h_ForthJetPt_3BTagM_PFHT400 = ROOT.TH1F("h_ForthJetPt_3BTagM_PFHT400_%s" % (sampleName), "; Offline p_{T}^{4th jet} [GeV]; #varepsilon_{L1+HLT}", len(bins_pt)-1, array.array("d", bins_pt)) 
    h_NJets_3BTagM_PFHT400      = ROOT.TH1F("h_NJets_3BTagM_PFHT400_%s" % (sampleName),      "; Jet multiplicity; #varepsilon_{L1+HLT}", 8, 4, 12)
    h_MeanBTag_3BTagM_PFHT400   = ROOT.TH1F("h_MeanBTag_3BTagM_PFHT400_%s" % (sampleName),   "; Mean PNet score (j^{ldg btag}, j^{subldg btag}); #varepsilon_{L1+HLT}", len(bins_bDisc)-1, array.array("d", bins_bDisc))
    h_NBJets_3BTagM_PFHT400     = ROOT.TH1F("h_NBJets_3BTagM_PFHT400_%s" % (sampleName),     "; Medium b-jet multiplicity; #varepsilon_{L1+HLT}", 4, 1, 5)
    
    h_PFHT_3BTagM_PFHT400_Passed_FullPath = ROOT.TH1F("h_PFHT_3BTagM_PFHT400_Passed_FullPath_%s" % (sampleName), "; Offline PF H_{T} [GeV]; #varepsilon_{L1+HLT}", len(bins_HT)-1, array.array("d", bins_HT))
    h_ForthJetPt_3BTagM_PFHT400_Passed_FullPath = ROOT.TH1F("h_ForthJetPt_3BTagM_PFHT400_Passed_FullPath_%s" % (sampleName), "; Offline p_{T}^{4th jet} [GeV]; #varepsilon_{L1+HLT}", len(bins_pt)-1, array.array("d", bins_pt))
    h_NJets_3BTagM_PFHT400_Passed_FullPath = ROOT.TH1F("h_NJets_3BTagM_PFHT400_Passed_FullPath_%s" % (sampleName), "; Jet multiplicity; #varepsilon_{L1+HLT}", 8, 4, 12)
    h_MeanBTag_3BTagM_PFHT400_Passed_FullPath = ROOT.TH1F("h_MeanBTag_3BTagM_PFHT400_Passed_FullPath_%s" % (sampleName), "; Mean PNet score (j^{ldg btag}, j^{subldg btag}); #varepsilon_{L1+HLT}", len(bins_bDisc)-1, array.array("d", bins_bDisc))
    h_NBJets_3BTagM_PFHT400_Passed_FullPath = ROOT.TH1F("h_NBJets_3BTagM_PFHT400_Passed_FullPath_%s" % (sampleName), "; Medium b-jet multiplicity; #varepsilon_{L1+HLT}", 4, 1, 5)
    
    h_PFHT_vs_MeanBTag_3BTagM_PFHT400 = ROOT.TH2F("h_PFHT_vs_MeanBTag_3BTagM_PFHT400_%s" % (sampleName), "; Offline PF H_{T} [GeV]; Mean PNet score (j^{ldg btag}, j^{subldg btag}); #varepsilon_{L1+HLT}", len(bins2D_HT)-1, array.array("d", bins2D_HT), len(bins2D_bDisc)-1, array.array("d", bins2D_bDisc))
    h_PFHT_vs_MeanBTag_3BTagM_PFHT400_Passed_FullPath = ROOT.TH2F("h_PFHT_vs_MeanBTag_3BTagM_PFHT400_Passed_FullPath_%s" % (sampleName), "; Offline PF H_{T} [GeV]; Mean PNet score (j^{ldg btag}, j^{subldg btag}); #varepsilon_{L1+HLT}", len(bins2D_HT)-1, array.array("d", bins2D_HT), len(bins2D_bDisc)-1, array.array("d", bins2D_bDisc))
    
    h_PFHT_vs_ForthJetPt_3BTagM_PFHT400 = ROOT.TH2F("h_PFHT_vs_ForthJetPt_3BTagM_PFHT400_%s" % (sampleName), "; Offline PF H_{T} [GeV]; Offline p_{T}^{4th jet} [GeV]; #varepsilon_{L1+HLT}", len(bins2D_HT)-1, array.array("d", bins2D_HT), len(bins_pt)-1, array.array("d", bins_pt))
    h_PFHT_vs_ForthJetPt_3BTagM_PFHT400_Passed_FullPath = ROOT.TH2F("h_PFHT_vs_ForthJetPt_3BTagM_PFHT400_Passed_FullPath_%s" % (sampleName), "; Offline PF H_{T} [GeV]; Offline p_{T}^{4th jet} [GeV]; #varepsilon_{L1+HLT}", len(bins2D_HT)-1, array.array("d", bins2D_HT),len(bins_pt)-1, array.array("d", bins_pt))

    for i, e in enumerate(t):
        
        b_HLT_QuadPFJet70_50_40_35_PFBTagParticleNet_2BTagSum0p65 = e.HLT_QuadPFJet70_50_40_35_PFBTagParticleNet_2BTagSum0p65
        b_HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_QuadPFJet70_50_40_30_PFBTagParticleNet_2BTagSum0p65 = e.HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_QuadPFJet70_50_40_30_PFBTagParticleNet_2BTagSum0p65
        
        # Baseline selection:
        if (e.PFHT < 300): continue
        if (e.MeanPNetScore < 0.65): continue
        
        h_PFHT_vs_MeanBTag.Fill(e.PFHT, e.MeanPNetScore)
        h_PFHT_vs_ForthJetPt.Fill(e.PFHT, e.ForthldgInPtJet_pt)
        h_PFHT.Fill(e.PFHT)
        h_ForthJetPt.Fill(e.ForthldgInPtJet_pt)
        h_NJets.Fill(e.NSelectedJets)
        h_NBJets.Fill(e.NMediumPNetJets)
        h_MeanBTag.Fill(e.MeanPNetScore)
        if (b_HLT_QuadPFJet70_50_40_35_PFBTagParticleNet_2BTagSum0p65):
            h_PFHT_vs_MeanBTag_Passed_FullPath.Fill(e.PFHT, e.MeanPNetScore)
            h_PFHT_vs_ForthJetPt_Passed_FullPath.Fill(e.PFHT, e.ForthldgInPtJet_pt)
            h_PFHT_Passed_FullPath.Fill(e.PFHT)
            h_ForthJetPt_Passed_FullPath.Fill(e.ForthldgInPtJet_pt)
            h_NJets_Passed_FullPath.Fill(e.NSelectedJets)
            h_NBJets_Passed_FullPath.Fill(e.NMediumPNetJets)
            h_MeanBTag_Passed_FullPath.Fill(e.MeanPNetScore)
            
        if (e.L1_L1sQuadJetOrHTTOrMuonHTT):
            h_PFHT_Passed_L1.Fill(e.PFHT)
            h_ForthJetPt_Passed_L1.Fill(e.ForthldgInPtJet_pt)
            
        if (e.NMediumPNetJets < 2): continue
        h_PFHT_vs_MeanBTag_2BTagM.Fill(e.PFHT, e.MeanPNetScore)
        h_PFHT_vs_ForthJetPt_2BTagM.Fill(e.PFHT, e.ForthldgInPtJet_pt)
        h_PFHT_2BTagM.Fill(e.PFHT)
        h_ForthJetPt_2BTagM.Fill(e.ForthldgInPtJet_pt)
        h_NJets_2BTagM.Fill(e.NSelectedJets)
        h_MeanBTag_2BTagM.Fill(e.MeanPNetScore)
        h_NBJets_2BTagM.Fill(e.NMediumPNetJets)
        if (b_HLT_QuadPFJet70_50_40_35_PFBTagParticleNet_2BTagSum0p65):
            h_PFHT_vs_MeanBTag_2BTagM_Passed_FullPath.Fill(e.PFHT, e.MeanPNetScore)
            h_PFHT_vs_ForthJetPt_2BTagM_Passed_FullPath.Fill(e.PFHT, e.ForthldgInPtJet_pt)
            h_PFHT_2BTagM_Passed_FullPath.Fill(e.PFHT)
            h_ForthJetPt_2BTagM_Passed_FullPath.Fill(e.ForthldgInPtJet_pt)
            h_NJets_2BTagM_Passed_FullPath.Fill(e.NSelectedJets)
            h_MeanBTag_2BTagM_Passed_FullPath.Fill(e.MeanPNetScore)
            h_NBJets_2BTagM_Passed_FullPath.Fill(e.NMediumPNetJets)
            
        if (e.PFHT >= 400):
            #---------------------------------------------------------
            # Selections 2BTagM + PFHT cut
            #-----------------------------------------------------------
            h_PFHT_vs_MeanBTag_2BTagM_PFHT400.Fill(e.PFHT, e.MeanPNetScore)
            h_PFHT_vs_ForthJetPt_2BTagM_PFHT400.Fill(e.PFHT, e.ForthldgInPtJet_pt)
            h_PFHT_2BTagM_PFHT400.Fill(e.PFHT)
            h_ForthJetPt_2BTagM_PFHT400.Fill(e.ForthldgInPtJet_pt)
            h_NJets_2BTagM_PFHT400.Fill(e.NSelectedJets)
            h_MeanBTag_2BTagM_PFHT400.Fill(e.MeanPNetScore)
            h_NBJets_2BTagM_PFHT400.Fill(e.NMediumPNetJets)
            if (b_HLT_QuadPFJet70_50_40_35_PFBTagParticleNet_2BTagSum0p65):
                h_PFHT_vs_MeanBTag_2BTagM_PFHT400_Passed_FullPath.Fill(e.PFHT, e.MeanPNetScore)
                h_PFHT_vs_ForthJetPt_2BTagM_PFHT400_Passed_FullPath.Fill(e.PFHT, e.ForthldgInPtJet_pt)
                h_PFHT_2BTagM_PFHT400_Passed_FullPath.Fill(e.PFHT)
                h_ForthJetPt_2BTagM_PFHT400_Passed_FullPath.Fill(e.ForthldgInPtJet_pt)
                h_NJets_2BTagM_PFHT400_Passed_FullPath.Fill(e.NSelectedJets)
                h_MeanBTag_2BTagM_PFHT400_Passed_FullPath.Fill(e.MeanPNetScore)
                h_NBJets_2BTagM_PFHT400_Passed_FullPath.Fill(e.NMediumPNetJets)
                
        if (e.NMediumPNetJets >= 3):
            #---------------------------------------------------------
            # Selections 3BTagM
            #-----------------------------------------------------------
            h_PFHT_vs_MeanBTag_3BTagM.Fill(e.PFHT, e.MeanPNetScore)
            h_PFHT_vs_ForthJetPt_3BTagM.Fill(e.PFHT, e.ForthldgInPtJet_pt)
            h_PFHT_3BTagM.Fill(e.PFHT)
            h_ForthJetPt_3BTagM.Fill(e.ForthldgInPtJet_pt)
            h_NJets_3BTagM.Fill(e.NSelectedJets)
            h_MeanBTag_3BTagM.Fill(e.MeanPNetScore)
            h_NBJets_3BTagM.Fill(e.NMediumPNetJets)
            if (b_HLT_QuadPFJet70_50_40_35_PFBTagParticleNet_2BTagSum0p65):
                h_PFHT_vs_MeanBTag_3BTagM_Passed_FullPath.Fill(e.PFHT, e.MeanPNetScore)
                h_PFHT_vs_ForthJetPt_3BTagM_Passed_FullPath.Fill(e.PFHT, e.ForthldgInPtJet_pt)
                h_PFHT_3BTagM_Passed_FullPath.Fill(e.PFHT)
                h_ForthJetPt_3BTagM_Passed_FullPath.Fill(e.ForthldgInPtJet_pt)
                h_NJets_3BTagM_Passed_FullPath.Fill(e.NSelectedJets)
                h_MeanBTag_3BTagM_Passed_FullPath.Fill(e.MeanPNetScore)
                h_NBJets_3BTagM_Passed_FullPath.Fill(e.NMediumPNetJets)
                
            if (e.PFHT >= 400):
                #---------------------------------------------------------
                # Selections 3BTagM + PFHT cut
                #-----------------------------------------------------------
                h_PFHT_vs_MeanBTag_3BTagM_PFHT400.Fill(e.PFHT, e.MeanPNetScore)
                h_PFHT_vs_ForthJetPt_3BTagM_PFHT400.Fill(e.PFHT, e.ForthldgInPtJet_pt)
                h_PFHT_3BTagM_PFHT400.Fill(e.PFHT)
                h_ForthJetPt_3BTagM_PFHT400.Fill(e.ForthldgInPtJet_pt)
                h_NJets_3BTagM_PFHT400.Fill(e.NSelectedJets)
                h_MeanBTag_3BTagM_PFHT400.Fill(e.MeanPNetScore)
                h_NBJets_3BTagM_PFHT400.Fill(e.NMediumPNetJets)
                if (b_HLT_QuadPFJet70_50_40_35_PFBTagParticleNet_2BTagSum0p65):
                    h_PFHT_vs_MeanBTag_3BTagM_PFHT400_Passed_FullPath.Fill(e.PFHT, e.MeanPNetScore)
                    h_PFHT_vs_ForthJetPt_3BTagM_PFHT400_Passed_FullPath.Fill(e.PFHT, e.ForthldgInPtJet_pt)
                    h_PFHT_3BTagM_PFHT400_Passed_FullPath.Fill(e.PFHT)
                    h_ForthJetPt_3BTagM_PFHT400_Passed_FullPath.Fill(e.ForthldgInPtJet_pt)
                    h_NJets_3BTagM_PFHT400_Passed_FullPath.Fill(e.NSelectedJets)
                    h_MeanBTag_3BTagM_PFHT400_Passed_FullPath.Fill(e.MeanPNetScore)
                    h_NBJets_3BTagM_PFHT400_Passed_FullPath.Fill(e.NMediumPNetJets)
    
    hList = []
    hList.append(h_PFHT_vs_MeanBTag)
    hList.append(h_PFHT_vs_ForthJetPt)
    hList.append(h_PFHT)
    hList.append(h_ForthJetPt)
    hList.append(h_NJets)
    hList.append(h_NBJets)
    hList.append(h_MeanBTag)
    hList.append(h_PFHT_vs_MeanBTag_Passed_FullPath)
    hList.append(h_PFHT_vs_ForthJetPt_Passed_FullPath)
    hList.append(h_PFHT_Passed_FullPath)
    hList.append(h_ForthJetPt_Passed_FullPath)
    hList.append(h_NJets_Passed_FullPath)
    hList.append(h_NBJets_Passed_FullPath)
    hList.append(h_MeanBTag_Passed_FullPath)
    hList.append(h_PFHT_Passed_L1)
    hList.append(h_ForthJetPt_Passed_L1)
    hList.append(h_PFHT_vs_MeanBTag_2BTagM)
    hList.append(h_PFHT_vs_ForthJetPt_2BTagM)
    hList.append(h_PFHT_2BTagM)
    hList.append(h_ForthJetPt_2BTagM)
    hList.append(h_NJets_2BTagM)
    hList.append(h_MeanBTag_2BTagM)
    hList.append(h_NBJets_2BTagM)
    hList.append(h_PFHT_vs_MeanBTag_2BTagM_Passed_FullPath)
    hList.append(h_PFHT_vs_ForthJetPt_2BTagM_Passed_FullPath)
    hList.append(h_PFHT_2BTagM_Passed_FullPath)
    hList.append(h_ForthJetPt_2BTagM_Passed_FullPath)
    hList.append(h_NJets_2BTagM_Passed_FullPath)
    hList.append(h_MeanBTag_2BTagM_Passed_FullPath)
    hList.append(h_NBJets_2BTagM_Passed_FullPath)
    
    hList.append(h_PFHT_vs_MeanBTag_2BTagM_PFHT400)
    hList.append(h_PFHT_vs_ForthJetPt_2BTagM_PFHT400)
    hList.append(h_PFHT_2BTagM_PFHT400)
    hList.append(h_ForthJetPt_2BTagM_PFHT400)
    hList.append(h_NJets_2BTagM_PFHT400)
    hList.append(h_MeanBTag_2BTagM_PFHT400)
    hList.append(h_NBJets_2BTagM_PFHT400)
    hList.append(h_PFHT_vs_MeanBTag_2BTagM_PFHT400_Passed_FullPath)
    hList.append(h_PFHT_vs_ForthJetPt_2BTagM_PFHT400_Passed_FullPath)
    hList.append(h_PFHT_2BTagM_PFHT400_Passed_FullPath)
    hList.append(h_ForthJetPt_2BTagM_PFHT400_Passed_FullPath)
    hList.append(h_NJets_2BTagM_PFHT400_Passed_FullPath)
    hList.append(h_MeanBTag_2BTagM_PFHT400_Passed_FullPath)
    hList.append(h_NBJets_2BTagM_PFHT400_Passed_FullPath)
    
    hList.append(h_PFHT_vs_MeanBTag_3BTagM)
    hList.append(h_PFHT_vs_ForthJetPt_3BTagM)
    hList.append(h_PFHT_3BTagM)
    hList.append(h_ForthJetPt_3BTagM)
    hList.append(h_NJets_3BTagM)
    hList.append(h_MeanBTag_3BTagM)
    hList.append(h_NBJets_3BTagM)
    hList.append(h_PFHT_vs_MeanBTag_3BTagM_Passed_FullPath)
    hList.append(h_PFHT_vs_ForthJetPt_3BTagM_Passed_FullPath)
    hList.append(h_PFHT_3BTagM_Passed_FullPath)
    hList.append(h_ForthJetPt_3BTagM_Passed_FullPath)
    hList.append(h_NJets_3BTagM_Passed_FullPath)
    hList.append(h_MeanBTag_3BTagM_Passed_FullPath)
    hList.append(h_NBJets_3BTagM_Passed_FullPath)
    
    hList.append(h_PFHT_vs_MeanBTag_3BTagM_PFHT400)
    hList.append(h_PFHT_vs_ForthJetPt_3BTagM_PFHT400)
    hList.append(h_PFHT_3BTagM_PFHT400)
    hList.append(h_ForthJetPt_3BTagM_PFHT400)
    hList.append(h_NJets_3BTagM_PFHT400)
    hList.append(h_MeanBTag_3BTagM_PFHT400)
    hList.append(h_NBJets_3BTagM_PFHT400)
    hList.append(h_PFHT_vs_MeanBTag_3BTagM_PFHT400_Passed_FullPath)
    hList.append(h_PFHT_vs_ForthJetPt_3BTagM_PFHT400_Passed_FullPath)
    hList.append(h_PFHT_3BTagM_PFHT400_Passed_FullPath)
    hList.append(h_ForthJetPt_3BTagM_PFHT400_Passed_FullPath)
    hList.append(h_NJets_3BTagM_PFHT400_Passed_FullPath)
    hList.append(h_MeanBTag_3BTagM_PFHT400_Passed_FullPath)
    hList.append(h_NBJets_3BTagM_PFHT400_Passed_FullPath)
    return hList

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def main(args):
    
    hDataList = []
    hTTList   = []
    
    if args.year == "2022":
        fData = ROOT.TFile.Open("Run3_MuonEG_2022_PromptNanoAOD_07June2023_v2/PrivateNano_MuonEG_Run2022_PromptReco_22May2023.root")
        hDataList = GetPNetEfficiencies22(fData, "MuonEG")
        
        fTT = ROOT.TFile.Open("Run3_TTto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8_08June2023/PrivateNano_TTto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8_08June2023/ntuple.root")
        hTTList = GetPNetEfficiencies22(fTT, "TT")

    fOutput = ROOT.TFile.Open(args.output, "RECREATE")
    for h in hDataList:
        h.Write()
    for h in hTTList:
        h.Write()
    fOutput.Close()

    return


if __name__ == "__main__":

    # Default values
    VERBOSE       = True
    YEAR          = "2022"
    OUTPUT        = "TriggerEfficiency"
    DIRNAME       = ""
    REDIRECTOR    = "root://cmseos.fnal.gov/"
    FORMATS       = [".png", ".pdf", ".C"]
    SAVEPATH      = getPublicPath()
    STUDY         = "TriggerEfficiency"
    
    parser = ArgumentParser(description="Derive the trigger scale factors")
    parser.add_argument("-v", "--verbose", dest="verbose", default=VERBOSE, action="store_true", help="Verbose mode for debugging purposes [default: %s]" % (VERBOSE))
    parser.add_argument("-d", "--dir", dest="dirName", type=str, action="store", default=DIRNAME, help="Location of the samples (a directory above) [default: %s]" % (DIRNAME))
    parser.add_argument("--year", dest="year", action="store", default=YEAR, help="Process year")
    parser.add_argument("--formats", dest="formats", default=FORMATS, action="store", help="Formats to save histograms")
    parser.add_argument("--output", dest="output", default=OUTPUT, action="store", help="The name of the output file")

    args = parser.parse_args()
    args.path = os.path.join(SAVEPATH, "%s_%s" % (STUDY, datetime.datetime.now().strftime('%d_%b_%Y')))
    args.output = args.output+"_%s_analyzedOn_%s.root" % (args.year, datetime.datetime.now().strftime('%d_%b_%Y'))
    if not os.path.exists(args.path):
        os.makedirs(args.path)
    main(args)

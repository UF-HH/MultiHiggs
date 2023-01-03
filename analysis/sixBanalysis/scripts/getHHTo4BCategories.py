#!/usr/bin/env python
'''
 USAGE:

./getTriggerEfficiencyByFilter.py --year 2017 -d Summer2017UL_TRGcurves_wTrgMatching_15Dec2022
./getTriggerEfficiencyByFilter.py --year 2018 -d Summer2018UL_TRGcurves_wTrgMatching_14Dec2022_4bCode

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
import math
import datetime
ROOT.gROOT.SetBatch(True)

import array
from ROOT import Math

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
        "SingleMuon" : ROOT.kBlack,
        "TTbar"      : ROOT.kBlue, 
        "NMSSM"      : ROOT.kRed,
        }
    return colors[sampleName]


def GetEfficiencies17(f, sampleName):
    hList = []
    
    # Read the tree
    t = f.Get("TrgTree")
    t.SetAlias("OnePFCentralJetLooseID75", "1PFCentralJetLooseID75")
    t.SetAlias("TwoPFCentralJetLooseID60", "2PFCentralJetLooseID60")
    t.SetAlias("ThreePFCentralJetLooseID45", "3PFCentralJetLooseID45")
    t.SetAlias("FourPFCentralJetLooseID40", "4PFCentralJetLooseID40")

    nentries = t.GetEntries()
    
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Book the histograms
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    h_caloJetSum_before_L1filterHT = ROOT.TH1F("%s__DistributionBefore_L1filterHT" %(sampleName), "%s__DistributionBefore_L1filterHT" %(sampleName), 60, 100, 1500)
    h_caloJetSum_passed_L1filterHT = ROOT.TH1F("%s__DistributionPassed_L1filterHT" %(sampleName), "%s__DistributionPassed_L1filterHT" %(sampleName), 60, 100, 1500)
    
    varBins = [15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 120, 140, 160, 180, 220, 260, 300]
    h_jetForthHighestPt_pt_before_QuadCentralJet30 = ROOT.TH1F("%s__DistributionBefore_QuadCentralJet30" % (sampleName), "%s__DistributionBefore_QuadCentralJet30" % (sampleName), len(varBins)-1, array.array("d", varBins))
    h_jetForthHighestPt_pt_passed_QuadCentralJet30 = ROOT.TH1F("%s__DistributionPassed_QuadCentralJet30" % (sampleName), "%s__DistributionPassed_QuadCentralJet30" % (sampleName), len(varBins)-1, array.array("d", varBins))
    
    h_caloJetSum_before_CaloQuadJet30HT300 = ROOT.TH1F("%s__DistributionBefore_CaloQuadJet30HT300" % (sampleName), "%s__DistributionBefore_CaloQuadJet30HT300" % (sampleName), 50, 200, 1200)
    h_caloJetSum_passed_CaloQuadJet30HT300 = ROOT.TH1F("%s__DistributionPassed_CaloQuadJet30HT300" % (sampleName), "%s__DistributionPassed_CaloQuadJet30HT300" % (sampleName), 50, 200, 1200)
    
    varBins=[0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.54, 0.58, 0.62, 0.66, 0.70, 0.74, 0.78, 0.82, 0.84, 0.86, 0.90, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99, 1.0]
    h_jetFirstHighestDeepFlavB_deepFlavB_before_BTagCaloCSVp05Double = ROOT.TH1F("%s__DistributionBefore_BTagCaloCSVp05Double" % (sampleName), "%s__DistributionBefore_BTagCaloCSVp05Double" % (sampleName), len(varBins)-1, array.array("d", varBins))
    h_jetFirstHighestDeepFlavB_deepFlavB_passed_BTagCaloCSVp05Double = ROOT.TH1F("%s__DistributionPassed_BTagCaloCSVp05Double" % (sampleName), "%s__DistributionPassed_BTagCaloCSVp05Double" % (sampleName), len(varBins)-1, array.array("d", varBins))
    
    varBins = [i for i in range(20, 100+5, 5)] + [i for i in range(100+10, 150+10, 10)] + [i for i in range(150+20, 250+20, 20)]
    h_jetForthHighestPt_pt_before_PFCentralJetLooseIDQuad30 = ROOT.TH1F("%s__DistributionBefore_PFCentralJetLooseIDQuad30" % (sampleName), "%s__DistributionBefore_PFCentralJetLooseIDQuad30" % (sampleName), len(varBins)-1, array.array("d", varBins))
    h_jetForthHighestPt_pt_passed_PFCentralJetLooseIDQuad30 = ROOT.TH1F("%s__DistributionPassed_PFCentralJetLooseIDQuad30" % (sampleName), "%s__DistributionPassed_PFCentralJetLooseIDQuad30" % (sampleName), len(varBins)-1, array.array("d", varBins))
    
    h_jetFirstHighestPt_pt_before_1PFCentralJetLooseID75 = ROOT.TH1F("%s__DistributionBefore_1PFCentralJetLooseID75" % (sampleName), "%s__DistributionBefore_1PFCentralJetLooseID75" % (sampleName), 50, 20, 500)
    h_jetFirstHighestPt_pt_passed_1PFCentralJetLooseID75 = ROOT.TH1F("%s__DistributionPassed_1PFCentralJetLooseID75" % (sampleName), "%s__DistributionPassed_1PFCentralJetLooseID75" % (sampleName), 50, 20, 500)
    
    h_jetSecondHighestPt_pt_before_2PFCentralJetLooseID60 = ROOT.TH1F("%s__DistributionBefore_2PFCentralJetLooseID60" % (sampleName), "%s__DistributionBefore_2PFCentralJetLooseID60" % (sampleName), 50, 20, 300)
    h_jetSecondHighestPt_pt_passed_2PFCentralJetLooseID60 = ROOT.TH1F("%s__DistributionPassed_2PFCentralJetLooseID60" % (sampleName), "%s__DistributionPassed_2PFCentralJetLooseID60" % (sampleName), 50, 20, 300)
    
    h_jetThirdHighestPt_pt_before_3PFCentralJetLooseID45 = ROOT.TH1F("%s__DistributionBefore_3PFCentralJetLooseID45" % (sampleName), "%s__DistributionBefore_3PFCentralJetLooseID45" % (sampleName), 40, 20, 200)
    h_jetThirdHighestPt_pt_passed_3PFCentralJetLooseID45 = ROOT.TH1F("%s__DistributionPassed_3PFCentralJetLooseID45" % (sampleName), "%s__DistributionPassed_3PFCentralJetLooseID45" % (sampleName), 40, 20, 200)
    
    h_jetForthHighestPt_pt_before_4PFCentralJetLooseID40 = ROOT.TH1F("%s__DistributionBefore_4PFCentralJetLooseID40" % (sampleName), "%s__DistributionBefore_4PFCentralJetLooseID40" % (sampleName), 40, 20, 200)
    h_jetForthHighestPt_pt_passed_4PFCentralJetLooseID40 = ROOT.TH1F("%s__DistributionPassed_4PFCentralJetLooseID40" % (sampleName), "%s__DistributionPassed_4PFCentralJetLooseID40" % (sampleName), 40, 20, 200)
    
    varBins = [i for i in range(200, 300+100, 100)] + [i for i in range(300+30, 1500+30, 30)]
    h_pfJetSum_before_PFCentralJetsLooseIDQuad30HT300 = ROOT.TH1F("%s__DistributionBefore_PFCentralJetsLooseIDQuad30HT300" % (sampleName), "%s__DistributionBefore_PFCentralJetsLooseIDQuad30HT300" % (sampleName), len(varBins)-1, array.array("d", varBins))
    h_pfJetSum_passed_PFCentralJetsLooseIDQuad30HT300 = ROOT.TH1F("%s__DistributionPassed_PFCentralJetsLooseIDQuad30HT300" % (sampleName), "%s__DistributionPassed_PFCentralJetsLooseIDQuad30HT300" % (sampleName), len(varBins)-1, array.array("d", varBins))

    if sampleName == "SingleMuon":
        varBins = [0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.84, 0.88, 0.92, 0.96, 1.0]
    else:
        varBins = [0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.54, 0.58, 0.62, 0.66, 0.70, 0.74, 0.78, 0.82, 0.86, 0.90, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99, 1.0]
    h_jetFirstHighestDeepFlavB_deepFlavB_before_BTagPFCSVp070Triple = ROOT.TH1F("%s__DistributionBefore_BTagPFCSVp070Triple" % (sampleName), "%s__DistributionBefore_BTagPFCSVp070Triple" % (sampleName), len(varBins)-1, array.array("d", varBins))
    h_jetFirstHighestDeepFlavB_deepFlavB_passed_BTagPFCSVp070Triple = ROOT.TH1F("%s__DistributionPassed_BTagPFCSVp070Triple" % (sampleName), "%s__DistributionPassed_BTagPFCSVp070Triple" % (sampleName), len(varBins)-1, array.array("d", varBins))
    
    # Loop over all events
    for i, entry in enumerate(t):
        
        # Preselection cuts
        if (entry.highestIsoElecton_pt < 10): continue
        if (entry.electronTimesMuoncharge > 0): continue;
        
        #==========================================================
        # Filter L1filterHT:
        #==========================================================
        h_caloJetSum_before_L1filterHT.Fill(entry.caloJetSum)
        if (entry.QuadCentralJet30 == 0): continue
        h_caloJetSum_passed_L1filterHT.Fill(entry.caloJetSum)
        
        #==========================================================
        # Filter QuadCentralJet30:
        #==========================================================
        if (entry.L1sQuadJetC50to60IorHTT280to500IorHTT250to340QuadJet < 1): continue
        h_jetForthHighestPt_pt_before_QuadCentralJet30.Fill(entry.jetForthHighestPt_pt)
        if (entry.QuadCentralJet30 < 4): continue
        h_jetForthHighestPt_pt_passed_QuadCentralJet30.Fill(entry.jetForthHighestPt_pt)
        
        #==========================================================
        # Filter CaloQuadJet30HT300:
        #==========================================================
        h_caloJetSum_before_CaloQuadJet30HT300.Fill(entry.caloJetSum)
        if (entry.CaloQuadJet30HT300_MaxHT < 300.0): continue
        if (entry.numberOfJetsCaloHT < 4): continue
        h_caloJetSum_passed_CaloQuadJet30HT300.Fill(entry.caloJetSum)

        #==========================================================
        # Filter BTagCaloCSVp05Double:
        #==========================================================
        h_jetFirstHighestDeepFlavB_deepFlavB_before_BTagCaloCSVp05Double.Fill(entry.jetFirstHighestDeepFlavB_deepFlavB)
        if (entry.BTagCaloCSVp05Double_jetFirstHighestDeepFlavB_triggerFlag == 0): continue
        h_jetFirstHighestDeepFlavB_deepFlavB_passed_BTagCaloCSVp05Double.Fill(entry.jetFirstHighestDeepFlavB_deepFlavB)
        
        #==========================================================
        # Filter PFCentralJetLooseIDQuad30:
        #==========================================================
        if (entry.BTagCaloCSVp05Double < 2): continue
        h_jetForthHighestPt_pt_before_PFCentralJetLooseIDQuad30.Fill(entry.jetForthHighestPt_pt)
        if (entry.PFCentralJetLooseIDQuad30 < 4): continue
        h_jetForthHighestPt_pt_passed_PFCentralJetLooseIDQuad30.Fill(entry.jetForthHighestPt_pt)

        #==========================================================
        # Filter 1PFCentralJetLooseID75
        #==========================================================
        h_jetFirstHighestPt_pt_before_1PFCentralJetLooseID75.Fill(entry.jetFirstHighestPt_pt)
        if (entry.OnePFCentralJetLooseID75 < 1): continue
        h_jetFirstHighestPt_pt_passed_1PFCentralJetLooseID75.Fill(entry.jetFirstHighestPt_pt)
        
        #==========================================================
        # Filter 2PFCentralJetLooseID60
        #==========================================================
        h_jetSecondHighestPt_pt_before_2PFCentralJetLooseID60.Fill(entry.jetSecondHighestPt_pt)
        if (entry.TwoPFCentralJetLooseID60 < 2): continue
        h_jetSecondHighestPt_pt_passed_2PFCentralJetLooseID60.Fill(entry.jetSecondHighestPt_pt)
        
        #==========================================================
        # Filter 3PFCentralJetLooseID45
        #==========================================================
        h_jetThirdHighestPt_pt_before_3PFCentralJetLooseID45.Fill(entry.jetThirdHighestPt_pt)
        if (entry.ThreePFCentralJetLooseID45 < 3): continue
        h_jetThirdHighestPt_pt_passed_3PFCentralJetLooseID45.Fill(entry.jetThirdHighestPt_pt)
        
        #==========================================================
        # Filter 4PFCentralJetLooseID40
        #==========================================================
        h_jetForthHighestPt_pt_before_4PFCentralJetLooseID40.Fill(entry.jetForthHighestPt_pt)
        if (entry.FourPFCentralJetLooseID40 < 4): continue
        h_jetForthHighestPt_pt_passed_4PFCentralJetLooseID40.Fill(entry.jetForthHighestPt_pt)
        
        #==========================================================
        # Filter PFCentralJetsLooseIDQuad30HT300
        #==========================================================
        h_pfJetSum_before_PFCentralJetsLooseIDQuad30HT300.Fill(entry.pfJetSum)
        if (entry.PFCentralJetsLooseIDQuad30HT300_MaxHT < 300): continue
        if (entry.numberOfJetsPfHT < 4): continue
        h_pfJetSum_passed_PFCentralJetsLooseIDQuad30HT300.Fill(entry.pfJetSum)
        
        #==========================================================
        # Filter BTagPFCSVp070Triple
        #==========================================================
        h_jetFirstHighestDeepFlavB_deepFlavB_before_BTagPFCSVp070Triple.Fill(entry.jetFirstHighestDeepFlavB_deepFlavB)
        if (entry.BTagPFCSVp070Triple_jetFirstHighestDeepFlavB_triggerFlag == 0): continue
        h_jetFirstHighestDeepFlavB_deepFlavB_passed_BTagPFCSVp070Triple.Fill(entry.jetFirstHighestDeepFlavB_deepFlavB)
                
    #=======================================
    # Construct efficiencies
    #=======================================
    filterName = "L1filterHT"
    h = ROOT.TGraphAsymmErrors(h_caloJetSum_passed_L1filterHT, h_caloJetSum_before_L1filterHT)
    h.SetTitle("Efficiency %s; #Sum p_{T} [GeV]; online efficiency" % (filterName))
    h.SetName("%s__Efficiency_%s" % (sampleName, filterName))
    h.SetLineColor(GetColor(sampleName))
    h.SetMarkerColor(GetColor(sampleName))
    hList.append(h)
    hList.append(h_caloJetSum_before_L1filterHT)
    hList.append(h_caloJetSum_passed_L1filterHT)
    
    filterName = "QuadCentralJet30"
    h = ROOT.TGraphAsymmErrors(h_jetForthHighestPt_pt_passed_QuadCentralJet30, h_jetForthHighestPt_pt_before_QuadCentralJet30)
    h.SetTitle("Efficiency %s; p_{T}^{4} [GeV]; online efficiency" % (filterName))
    h.SetName("%s__Efficiency_%s" % (sampleName, filterName))
    h.SetLineColor(GetColor(sampleName))
    h.SetMarkerColor(GetColor(sampleName))
    hList.append(h)
    hList.append(h_jetForthHighestPt_pt_before_QuadCentralJet30)
    hList.append(h_jetForthHighestPt_pt_passed_QuadCentralJet30)
    
    filterName = "CaloQuadJet30HT300"
    h = ROOT.TGraphAsymmErrors(h_caloJetSum_passed_CaloQuadJet30HT300, h_caloJetSum_before_CaloQuadJet30HT300)
    h.SetTitle("Efficiency %s; #sum p_{T} with p_{T}>30 GeV [GeV]; online efficiency" % (filterName))
    h.SetName("%s__Efficiency_%s" % (sampleName, filterName))
    h.SetLineColor(GetColor(sampleName))
    h.SetMarkerColor(GetColor(sampleName))
    hList.append(h)
    hList.append(h_caloJetSum_before_CaloQuadJet30HT300)
    hList.append(h_caloJetSum_passed_CaloQuadJet30HT300)

    filterName = "BTagCaloCSVp05Double"
    h = ROOT.TGraphAsymmErrors(h_jetFirstHighestDeepFlavB_deepFlavB_passed_BTagCaloCSVp05Double, h_jetFirstHighestDeepFlavB_deepFlavB_before_BTagCaloCSVp05Double)
    h.SetTitle("Efficiency %s; DeepFlavB^{1}; online efficliency" % (filterName))
    h.SetName("%s__Efficiency_%s" % (sampleName, filterName))
    h.SetLineColor(GetColor(sampleName))
    h.SetMarkerColor(GetColor(sampleName))
    hList.append(h)
    hList.append(h_jetFirstHighestDeepFlavB_deepFlavB_before_BTagCaloCSVp05Double)
    hList.append(h_jetFirstHighestDeepFlavB_deepFlavB_passed_BTagCaloCSVp05Double)
    
    filterName = "PFCentralJetLooseIDQuad30"
    h = ROOT.TGraphAsymmErrors(h_jetForthHighestPt_pt_passed_PFCentralJetLooseIDQuad30, h_jetForthHighestPt_pt_before_PFCentralJetLooseIDQuad30)
    h.SetTitle("Efficiency %s; p_{T}^{4} [GeV]; online efficiency" % (filterName))
    h.SetName("%s__Efficiency_%s" % (sampleName, filterName))
    h.SetLineColor(GetColor(sampleName))
    h.SetMarkerColor(GetColor(sampleName))
    hList.append(h)
    hList.append(h_jetForthHighestPt_pt_before_PFCentralJetLooseIDQuad30)
    hList.append(h_jetForthHighestPt_pt_passed_PFCentralJetLooseIDQuad30)

    filterName = "1PFCentralJetLooseID75"
    h = ROOT.TGraphAsymmErrors(h_jetFirstHighestPt_pt_passed_1PFCentralJetLooseID75, h_jetFirstHighestPt_pt_before_1PFCentralJetLooseID75)
    h.SetTitle("Efficiency %s; p_{T}^{1} [GeV]; online efficiency" % (filterName))
    h.SetName("%s__Efficiency_%s" % (sampleName, filterName))
    h.SetLineColor(GetColor(sampleName))
    h.SetMarkerColor(GetColor(sampleName))
    hList.append(h)
    hList.append(h_jetFirstHighestPt_pt_before_1PFCentralJetLooseID75)
    hList.append(h_jetFirstHighestPt_pt_passed_1PFCentralJetLooseID75)
    
    filterName = "2PFCentralJetLooseID60"
    h = ROOT.TGraphAsymmErrors(h_jetSecondHighestPt_pt_passed_2PFCentralJetLooseID60, h_jetSecondHighestPt_pt_before_2PFCentralJetLooseID60)
    h.SetTitle("Efficiency %s; p_{T}^{2} [GeV]; online efficiency" % (filterName))
    h.SetName("%s__Efficiency_%s" % (sampleName, filterName))
    h.SetLineColor(GetColor(sampleName))
    h.SetMarkerColor(GetColor(sampleName))
    hList.append(h)
    hList.append(h_jetSecondHighestPt_pt_before_2PFCentralJetLooseID60)
    hList.append(h_jetSecondHighestPt_pt_passed_2PFCentralJetLooseID60)
    
    filterName = "3PFCentralJetLooseID45"
    h = ROOT.TGraphAsymmErrors(h_jetThirdHighestPt_pt_passed_3PFCentralJetLooseID45, h_jetThirdHighestPt_pt_before_3PFCentralJetLooseID45)
    h.SetTitle("Efficiency %s; p_{T}^{3} [GeV]; online efficiency" % (filterName))
    h.SetName("%s__Efficiency_%s" % (sampleName, filterName))
    h.SetLineColor(GetColor(sampleName))
    h.SetMarkerColor(GetColor(sampleName))
    hList.append(h)
    hList.append(h_jetThirdHighestPt_pt_before_3PFCentralJetLooseID45)
    hList.append(h_jetThirdHighestPt_pt_passed_3PFCentralJetLooseID45)
    
    filterName = "4PFCentralJetLooseID40"
    h = ROOT.TGraphAsymmErrors(h_jetForthHighestPt_pt_passed_4PFCentralJetLooseID40, h_jetForthHighestPt_pt_before_4PFCentralJetLooseID40)
    h.SetTitle("Efficiency %s; p_{T}^{4} [GeV]; online efficiency" % (filterName))
    h.SetName("%s__Efficiency_%s" % (sampleName, filterName))
    h.SetLineColor(GetColor(sampleName))
    h.SetMarkerColor(GetColor(sampleName))
    hList.append(h)
    hList.append(h_jetForthHighestPt_pt_before_4PFCentralJetLooseID40)
    hList.append(h_jetForthHighestPt_pt_passed_4PFCentralJetLooseID40)
    
    filterName = "PFCentralJetsLooseIDQuad30HT300"
    h = ROOT.TGraphAsymmErrors(h_pfJetSum_passed_PFCentralJetsLooseIDQuad30HT300, h_pfJetSum_before_PFCentralJetsLooseIDQuad30HT300)
    h.SetTitle("Efficiency %s; #sum p_{T} with p_{T}>30 GeV [GeV]; online efficiency" % (filterName))
    h.SetName("%s__Efficiency_%s" % (sampleName, filterName))
    h.SetLineColor(GetColor(sampleName))
    h.SetMarkerColor(GetColor(sampleName))
    hList.append(h)
    hList.append(h_pfJetSum_before_PFCentralJetsLooseIDQuad30HT300)
    hList.append(h_pfJetSum_passed_PFCentralJetsLooseIDQuad30HT300)
    
    filterName = "BTagPFCSVp070Triple"
    h = ROOT.TGraphAsymmErrors(h_jetFirstHighestDeepFlavB_deepFlavB_passed_BTagPFCSVp070Triple, h_jetFirstHighestDeepFlavB_deepFlavB_before_BTagPFCSVp070Triple)
    h.SetTitle("Efficiency %s; PF DeepFlavB^{1}; online efficliency" % (filterName))
    h.SetName("%s__Efficiency_%s" % (sampleName, filterName))
    h.SetLineColor(GetColor(sampleName))
    h.SetMarkerColor(GetColor(sampleName))
    hList.append(h)
    hList.append(h_jetFirstHighestDeepFlavB_deepFlavB_before_BTagPFCSVp070Triple)
    hList.append(h_jetFirstHighestDeepFlavB_deepFlavB_passed_BTagPFCSVp070Triple)
    return hList


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def main(args):
    
    samples = {"GluGluToHHTo4B_node_cHHH0"    : args.dirName+"/GluGluToHHTo4B_node_cHHH0_TuneCP5_PSWeights_13TeV-powheg-pythia8/ntuple.root",
               "GluGluToHHTo4B_node_cHHH1"    : args.dirName+"/GluGluToHHTo4B_node_cHHH1_TuneCP5_PSWeights_13TeV-powheg-pythia8/ntuple.root",
               "GluGluToHHTo4B_node_cHHH2p45" : args.dirName+"/GluGluToHHTo4B_node_cHHH2p45_TuneCP5_PSWeights_13TeV-powheg-pythia8/ntuple.root",
               "GluGluToHHTo4B_node_cHHH5"    : args.dirName+"/GluGluToHHTo4B_node_cHHH5_TuneCP5_PSWeights_13TeV-powheg-pythia8/ntuple.root"
    }
    
    fOut = ROOT.TFile.Open("histogramsForHHTo4b.root", "RECREATE")
    for sample in samples:
        
        f = ROOT.TFile.Open(samples[sample])
        t = f.Get("sixBtree")
        
        direc = fOut.mkdir(sample)
        direc.cd()
        
        entries = t.GetEntries()
        
        # Define histograms
        h_GenPart_H1_pt  = ROOT.TH1F("h_GenPart_H1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        h_GenPart_H2_pt  = ROOT.TH1F("h_GenPart_H2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        h_GenPart_H1_eta = ROOT.TH1F("h_GenPart_H1_eta", ";#eta;Events", 120, -4.0, 4.0)
        h_GenPart_H2_eta = ROOT.TH1F("h_GenPart_H2_eta", ";#eta;Events", 120, -4.0, 4.0)
        h_GenPart_H1_phi = ROOT.TH1F("h_GenPart_H1_phi", ";#phi [rad];Events", 60, -3.0, 3.0)
        h_GenPart_H2_phi = ROOT.TH1F("h_GenPart_H2_phi", ";#phi [rad];Events", 60, -3.0, 3.0)
        
        h_GenPart_H1_b1_eta = ROOT.TH1F("h_GenPart_H1_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        h_GenPart_H1_b2_eta = ROOT.TH1F("h_GenPart_H1_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
        h_GenPart_H2_b1_eta = ROOT.TH1F("h_GenPart_H2_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        h_GenPart_H2_b2_eta = ROOT.TH1F("h_GenPart_H2_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
        h_GenPart_H1_b1_phi = ROOT.TH1F("h_GenPart_H1_b1_phi", ";#phi [rad];Events", 60, -3.0, 3.0)
        h_GenPart_H1_b2_phi = ROOT.TH1F("h_GenPart_H1_b2_phi", ";#phi [rad];Events", 60, -3.0, 3.0)
        h_GenPart_H2_b1_phi = ROOT.TH1F("h_GenPart_H2_b1_phi", ";#phi [rad];Events", 60, -3.0, 3.0)
        h_GenPart_H2_b2_phi = ROOT.TH1F("h_GenPart_H2_b2_phi", ";#phi [rad];Events", 60, -3.0, 3.0)
        h_GenPart_H1_b1_pt = ROOT.TH1F("h_GenPart_H1_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        h_GenPart_H1_b2_pt = ROOT.TH1F("h_GenPart_H1_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        h_GenPart_H2_b1_pt = ROOT.TH1F("h_GenPart_H2_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        h_GenPart_H2_b2_pt = ROOT.TH1F("h_GenPart_H2_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        
        
        hResolved_GenPart_H1_pt    = ROOT.TH1F("hResolved_GenPart_H1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolved_GenPart_H2_pt    = ROOT.TH1F("hResolved_GenPart_H2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolved_GenPart_H1_b1_pt = ROOT.TH1F("hResolved_GenPart_H1_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolved_GenPart_H1_b2_pt = ROOT.TH1F("hResolved_GenPart_H1_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolved_GenPart_H2_b1_pt = ROOT.TH1F("hResolved_GenPart_H2_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolved_GenPart_H2_b2_pt = ROOT.TH1F("hResolved_GenPart_H2_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolved_GenPart_H1_b1_eta = ROOT.TH1F("hResolved_GenPart_H1_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hResolved_GenPart_H1_b2_eta = ROOT.TH1F("hResolved_GenPart_H1_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hResolved_GenPart_H2_b1_eta = ROOT.TH1F("hResolved_GenPart_H2_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hResolved_GenPart_H2_b2_eta = ROOT.TH1F("hResolved_GenPart_H2_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hResolved_GenPart_H1_b1_phi = ROOT.TH1F("hResolved_GenPart_H1_b1_phi", ";#phi [rad];Events", 60, -3.0, 3.0)
        hResolved_GenPart_H1_b2_phi = ROOT.TH1F("hResolved_GenPart_H1_b2_phi", ";#phi [rad];Events", 60, -3.0, 3.0)
        hResolved_GenPart_H2_b1_phi = ROOT.TH1F("hResolved_GenPart_H2_b1_phi", ";#phi [rad];Events", 60, -3.0, 3.0)
        hResolved_GenPart_H2_b2_phi = ROOT.TH1F("hResolved_GenPart_H2_b2_phi", ";#phi [rad];Events", 60, -3.0, 3.0)
        hResolved_GenJet_H1_b1_pt  = ROOT.TH1F("hResolved_GenJet_H1_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolved_GenJet_H1_b2_pt  = ROOT.TH1F("hResolved_GenJet_H1_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolved_GenJet_H2_b1_pt  = ROOT.TH1F("hResolved_GenJet_H2_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolved_GenJet_H2_b2_pt  = ROOT.TH1F("hResolved_GenJet_H2_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolved_GenJet_H1_b1_eta = ROOT.TH1F("hResolved_GenJet_H1_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hResolved_GenJet_H1_b2_eta = ROOT.TH1F("hResolved_GenJet_H1_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hResolved_GenJet_H2_b1_eta = ROOT.TH1F("hResolved_GenJet_H2_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hResolved_GenJet_H2_b2_eta = ROOT.TH1F("hResolved_GenJet_H2_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hResolved_GenJet_H1_b1_phi = ROOT.TH1F("hResolved_GenJet_H1_b1_phi", ";#phi [rad];Events", 60, -3.0, 3.0)
        hResolved_GenJet_H1_b2_phi = ROOT.TH1F("hResolved_GenJet_H1_b2_phi", ";#phi [rad];Events", 60, -3.0, 3.0)
        hResolved_GenJet_H2_b1_phi = ROOT.TH1F("hResolved_GenJet_H2_b1_phi", ";#phi [rad];Events", 60, -3.0, 3.0)
        hResolved_GenJet_H2_b2_phi = ROOT.TH1F("hResolved_GenJet_H2_b2_phi", ";#phi [rad];Events", 60, -3.0, 3.0)
        hResolved_RecoJet_H1_b1_pt  = ROOT.TH1F("hResolved_RecoJet_H1_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolved_RecoJet_H1_b2_pt  = ROOT.TH1F("hResolved_RecoJet_H1_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolved_RecoJet_H2_b1_pt  = ROOT.TH1F("hResolved_RecoJet_H2_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolved_RecoJet_H2_b2_pt  = ROOT.TH1F("hResolved_RecoJet_H2_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolved_RecoJet_H1_b1_eta = ROOT.TH1F("hResolved_RecoJet_H1_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hResolved_RecoJet_H1_b2_eta = ROOT.TH1F("hResolved_RecoJet_H1_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hResolved_RecoJet_H2_b1_eta = ROOT.TH1F("hResolved_RecoJet_H2_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hResolved_RecoJet_H2_b2_eta = ROOT.TH1F("hResolved_RecoJet_H2_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hResolved_RecoJet_H1_b1_phi = ROOT.TH1F("hResolved_RecoJet_H1_b1_phi", ";#phi [rad];Events", 60, -3.0, 3.0)
        hResolved_RecoJet_H1_b2_phi = ROOT.TH1F("hResolved_RecoJet_H1_b2_phi", ";#phi [rad];Events", 60, -3.0, 3.0)
        hResolved_RecoJet_H2_b1_phi = ROOT.TH1F("hResolved_RecoJet_H2_b1_phi", ";#phi [rad];Events", 60, -3.0, 3.0)
        hResolved_RecoJet_H2_b2_phi = ROOT.TH1F("hResolved_RecoJet_H2_b2_phi", ";#phi [rad];Events", 60, -3.0, 3.0)
        hResolved_RecoJet_H1_b1_btag = ROOT.TH1F("hResolved_RecoJet_H1_b1_btag", ";b-discriminator;Events", 100, 0.0, 1.0)
        hResolved_RecoJet_H1_b2_btag = ROOT.TH1F("hResolved_RecoJet_H1_b2_btag", ";b-discriminator;Events", 100, 0.0, 1.0)
        hResolved_RecoJet_H2_b1_btag = ROOT.TH1F("hResolved_RecoJet_H2_b1_btag", ";b-discriminator;Events", 100, 0.0, 1.0)
        hResolved_RecoJet_H2_b2_btag = ROOT.TH1F("hResolved_RecoJet_H2_b2_btag", ";b-discriminator;Events", 100, 0.0, 1.0)
        hResolved_RecoJet_DeltaR_H1b1_H1b2 = ROOT.TH1F("hResolved_RecoJet_DeltaR_H1b1_H1b2", ";#Delta R;Events", 100, 0.0, 5.0);
        hResolved_RecoJet_DeltaR_H1b1_H2b1 = ROOT.TH1F("hResolved_RecoJet_DeltaR_H1b1_H2b1", ";#Delta R;Events", 100, 0.0, 5.0);
        hResolved_RecoJet_DeltaR_H1b1_H2b2 = ROOT.TH1F("hResolved_RecoJet_DeltaR_H1b1_H2b2", ";#Delta R;Events", 100, 0.0, 5.0);
        hResolved_RecoJet_DeltaR_H1b2_H2b1 = ROOT.TH1F("hResolved_RecoJet_DeltaR_H1b2_H2b1", ";#Delta R;Events", 100, 0.0, 5.0);
        hResolved_RecoJet_DeltaR_H1b2_H2b2 = ROOT.TH1F("hResolved_RecoJet_DeltaR_H1b2_H2b2", ";#Delta R;Events", 100, 0.0, 5.0);
        hResolved_RecoJet_DeltaR_H2b1_H2b2 = ROOT.TH1F("hResolved_RecoJet_DeltaR_H2b1_H2b2", ";#Delta R;Events", 100, 0.0, 5.0);
        hResolved_RecoJet_DeltaEta_H1b1_H1b2 = ROOT.TH1F("hResolved_RecoJet_DeltaEta_H1b1_H1b2", ";#Delta#eta;Events", 50, 0.0, 5.0);
        hResolved_RecoJet_DeltaEta_H1b1_H2b1 = ROOT.TH1F("hResolved_RecoJet_DeltaEta_H1b1_H2b1", ";#Delta#eta;Events", 50, 0.0, 5.0);
        hResolved_RecoJet_DeltaEta_H1b1_H2b2 = ROOT.TH1F("hResolved_RecoJet_DeltaEta_H1b1_H2b2", ";#Delta#eta;Events", 50, 0.0, 5.0);
        hResolved_RecoJet_DeltaEta_H1b2_H2b1 = ROOT.TH1F("hResolved_RecoJet_DeltaEta_H1b2_H2b1", ";#Delta#eta;Events", 50, 0.0, 5.0);
        hResolved_RecoJet_DeltaEta_H1b2_H2b2 = ROOT.TH1F("hResolved_RecoJet_DeltaEta_H1b2_H2b2", ";#Delta#eta;Events", 50, 0.0, 5.0);
        hResolved_RecoJet_DeltaEta_H2b1_H2b2 = ROOT.TH1F("hResolved_RecoJet_DeltaEta_H2b1_H2b2", ";#Delta#eta;Events", 50, 0.0, 5.0);
        hResolved_RecoJet_DeltaPhi_H1b1_H1b2 = ROOT.TH1F("hResolved_RecoJet_DeltaPhi_H1b1_H1b2", ";#Delta#phi;Events", 50, 0.0, 5.0);
        hResolved_RecoJet_DeltaPhi_H1b1_H2b1 = ROOT.TH1F("hResolved_RecoJet_DeltaPhi_H1b1_H2b1", ";#Delta#phi;Events", 50, 0.0, 5.0);
        hResolved_RecoJet_DeltaPhi_H1b1_H2b2 = ROOT.TH1F("hResolved_RecoJet_DeltaPhi_H1b1_H2b2", ";#Delta#phi;Events", 50, 0.0, 5.0);
        hResolved_RecoJet_DeltaPhi_H1b2_H2b1 = ROOT.TH1F("hResolved_RecoJet_DeltaPhi_H1b2_H2b1", ";#Delta#phi;Events", 50, 0.0, 5.0);
        hResolved_RecoJet_DeltaPhi_H1b2_H2b2 = ROOT.TH1F("hResolved_RecoJet_DeltaPhi_H1b2_H2b2", ";#Delta#phi;Events", 50, 0.0, 5.0);
        hResolved_RecoJet_DeltaPhi_H2b1_H2b2 = ROOT.TH1F("hResolved_RecoJet_DeltaPhi_H2b1_H2b2", ";#Delta#phi;Events", 50, 0.0, 5.0);
        hResolved_RecoJet_H1_pt  = ROOT.TH1F("hResolved_RecoJet_H1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolved_RecoJet_H2_pt  = ROOT.TH1F("hResolved_RecoJet_H2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolved_RecoJet_H1_eta = ROOT.TH1F("hResolved_RecoJet_H1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hResolved_RecoJet_H2_eta = ROOT.TH1F("hResolved_RecoJet_H2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hResolved_RecoJet_H1_phi = ROOT.TH1F("hResolved_RecoJet_H1_phi", ";#phi;Events", 60, -3.0, 3.0)
        hResolved_RecoJet_H2_phi = ROOT.TH1F("hResolved_RecoJet_H2_phi", ";#phi;Events", 60, -3.0, 3.0)
        hResolved_RecoJet_InvMass_H1 = ROOT.TH1F("hResolved_RecoJet_InvMass_H1", ";m_{H} [GeV]", 300, 0, 300)
        hResolved_RecoJet_InvMass_H2 = ROOT.TH1F("hResolved_RecoJet_InvMass_H2", ";m_{H} [GeV]", 300, 0, 300)
        hResolved_RecoJet_InvMassRegressed_H1 = ROOT.TH1F("hResolved_RecoJet_InvMassRegressed_H1", ";m_{H} [GeV]", 300, 0, 300)
        hResolved_RecoJet_InvMassRegressed_H2 = ROOT.TH1F("hResolved_RecoJet_InvMassRegressed_H2", ";m_{H} [GeV]", 300, 0, 300)
        hResolved_RecoJet_DeltaR_H1_H2 = ROOT.TH1F("hResolved_RecoJet_DeltaR_H1_H2", ";#Delta R;Events", 100, 0.0, 5.0)
        hResolved_RecoJet_DeltaEta_H1_H2 = ROOT.TH1F("hResolved_RecoJet_DeltaEta_H1_H2", ";#Delta#eta;Events", 50, 0.0, 5.0)
        hResolved_RecoJet_DeltaPhi_H1_H2 = ROOT.TH1F("hResolved_RecoJet_DeltaPhi_H1_H2", ";#Delta#phi;Events", 50, 0.0,5.0)
        hResolved_RecoJet_NJets = ROOT.TH1F("hResolved_RecoJet_NJets", "; jet multiplicity;Events", 15, 0, 15)
        hResolved_RecoJet_NFatJets = ROOT.TH1F("hResolved_RecoJet_NFatJets", "; fatjet multiplicity;Events", 10, 0, 10)
        
        hResolved_RecoJet_PFHT = ROOT.TH1F("hResolved_RecoJet_PFHT", "; PF H_{T} [GeV];Events", 200, 0.0, 1000)
        hResolved_RecoJet_NLooseBJets = ROOT.TH1I("hResolved_RecoJet_NLooseBJets", ";b-jets L;Events", 10, 0, 10)
        hResolved_RecoJet_NMediumBJets = ROOT.TH1I("hResolved_RecoJet_NMediumBJets", ";b-jets M;Events", 10, 0, 10)
        hResolved_RecoJet_NTightBJets = ROOT.TH1I("hResolved_RecoJet_NTightBJets", ";b-jets T;Events", 10, 0, 10)
        hResolved_RecoJet_Jet1Pt = ROOT.TH1F("hResolved_RecoJet_Jet1Pt", ";jet 1 p_{T} [GeV];Events", 100, 0.0, 500)
        hResolved_RecoJet_Jet2Pt = ROOT.TH1F("hResolved_RecoJet_Jet2Pt", ";jet 2 p_{T} [GeV];Events", 100, 0.0, 500)
        hResolved_RecoJet_Jet3Pt = ROOT.TH1F("hResolved_RecoJet_Jet3Pt", ";jet 3 p_{T} [GeV];Events", 100, 0.0, 500)
        hResolved_RecoJet_Jet4Pt = ROOT.TH1F("hResolved_RecoJet_Jet4Pt", ";jet 4 p_{T} [GeV];Events", 100, 0.0, 500)
        hResolved_RecoJet_Jet1Eta = ROOT.TH1F("hResolved_RecoJet_Jet1Eta", ";jet 1 #eta;Events", 120, -4.0, 4.0)
        hResolved_RecoJet_Jet2Eta = ROOT.TH1F("hResolved_RecoJet_Jet2Eta", ";jet 2 #eta;Events", 120, -4.0, 4.0)
        hResolved_RecoJet_Jet3Eta = ROOT.TH1F("hResolved_RecoJet_Jet3Eta", ";jet 3 #eta;Events", 120, -4.0, 4.0)
        hResolved_RecoJet_Jet4Eta = ROOT.TH1F("hResolved_RecoJet_Jet4Eta", ";jet 4 #eta;Events", 120, -4.0, 4.0)
        hResolved_RecoJet_AK8Jet1Pt = ROOT.TH1F("hResolved_RecoJet_AK8Jet1Pt", "; fatjet 1 p_{T} [GeV];Events", 200, 0.0, 1000)
        
        # Resolved exclusive
        hResolvedExcl_GenPart_H1_pt    = ROOT.TH1F("hResolvedExcl_GenPart_H1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedExcl_GenPart_H2_pt    = ROOT.TH1F("hResolvedExcl_GenPart_H2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedExcl_GenPart_H1_b1_pt = ROOT.TH1F("hResolvedExcl_GenPart_H1_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedExcl_GenPart_H1_b2_pt = ROOT.TH1F("hResolvedExcl_GenPart_H1_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedExcl_GenPart_H2_b1_pt = ROOT.TH1F("hResolvedExcl_GenPart_H2_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedExcl_GenPart_H2_b2_pt = ROOT.TH1F("hResolvedExcl_GenPart_H2_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedExcl_GenPart_H1_b1_eta = ROOT.TH1F("hResolvedExcl_GenPart_H1_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hResolvedExcl_GenPart_H1_b2_eta = ROOT.TH1F("hResolvedExcl_GenPart_H1_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hResolvedExcl_GenPart_H2_b1_eta = ROOT.TH1F("hResolvedExcl_GenPart_H2_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hResolvedExcl_GenPart_H2_b2_eta = ROOT.TH1F("hResolvedExcl_GenPart_H2_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hResolvedExcl_GenPart_H1_b1_phi = ROOT.TH1F("hResolvedExcl_GenPart_H1_b1_phi", ";#phi [rad];Events", 60, -3.0, 3.0)
        hResolvedExcl_GenPart_H1_b2_phi = ROOT.TH1F("hResolvedExcl_GenPart_H1_b2_phi", ";#phi [rad];Events", 60, -3.0, 3.0)
        hResolvedExcl_GenPart_H2_b1_phi = ROOT.TH1F("hResolvedExcl_GenPart_H2_b1_phi", ";#phi [rad];Events", 60, -3.0, 3.0)
        hResolvedExcl_GenPart_H2_b2_phi = ROOT.TH1F("hResolvedExcl_GenPart_H2_b2_phi", ";#phi [rad];Events", 60, -3.0, 3.0)
        hResolvedExcl_GenJet_H1_b1_pt  = ROOT.TH1F("hResolvedExcl_GenJet_H1_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedExcl_GenJet_H1_b2_pt  = ROOT.TH1F("hResolvedExcl_GenJet_H1_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedExcl_GenJet_H2_b1_pt  = ROOT.TH1F("hResolvedExcl_GenJet_H2_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedExcl_GenJet_H2_b2_pt  = ROOT.TH1F("hResolvedExcl_GenJet_H2_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedExcl_GenJet_H1_b1_eta = ROOT.TH1F("hResolvedExcl_GenJet_H1_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hResolvedExcl_GenJet_H1_b2_eta = ROOT.TH1F("hResolvedExcl_GenJet_H1_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hResolvedExcl_GenJet_H2_b1_eta = ROOT.TH1F("hResolvedExcl_GenJet_H2_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hResolvedExcl_GenJet_H2_b2_eta = ROOT.TH1F("hResolvedExcl_GenJet_H2_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hResolvedExcl_GenJet_H1_b1_phi = ROOT.TH1F("hResolvedExcl_GenJet_H1_b1_phi", ";#phi [rad];Events", 60, -3.0, 3.0)
        hResolvedExcl_GenJet_H1_b2_phi = ROOT.TH1F("hResolvedExcl_GenJet_H1_b2_phi", ";#phi [rad];Events", 60, -3.0, 3.0)
        hResolvedExcl_GenJet_H2_b1_phi = ROOT.TH1F("hResolvedExcl_GenJet_H2_b1_phi", ";#phi [rad];Events", 60, -3.0, 3.0)
        hResolvedExcl_GenJet_H2_b2_phi = ROOT.TH1F("hResolvedExcl_GenJet_H2_b2_phi", ";#phi [rad];Events", 60, -3.0, 3.0)
        hResolvedExcl_RecoJet_H1_b1_pt  = ROOT.TH1F("hResolvedExcl_RecoJet_H1_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedExcl_RecoJet_H1_b2_pt  = ROOT.TH1F("hResolvedExcl_RecoJet_H1_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedExcl_RecoJet_H2_b1_pt  = ROOT.TH1F("hResolvedExcl_RecoJet_H2_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedExcl_RecoJet_H2_b2_pt  = ROOT.TH1F("hResolvedExcl_RecoJet_H2_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedExcl_RecoJet_H1_b1_eta = ROOT.TH1F("hResolvedExcl_RecoJet_H1_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hResolvedExcl_RecoJet_H1_b2_eta = ROOT.TH1F("hResolvedExcl_RecoJet_H1_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hResolvedExcl_RecoJet_H2_b1_eta = ROOT.TH1F("hResolvedExcl_RecoJet_H2_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hResolvedExcl_RecoJet_H2_b2_eta = ROOT.TH1F("hResolvedExcl_RecoJet_H2_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hResolvedExcl_RecoJet_H1_b1_phi = ROOT.TH1F("hResolvedExcl_RecoJet_H1_b1_phi", ";#phi [rad];Events", 60, -3.0, 3.0)
        hResolvedExcl_RecoJet_H1_b2_phi = ROOT.TH1F("hResolvedExcl_RecoJet_H1_b2_phi", ";#phi [rad];Events", 60, -3.0, 3.0)
        hResolvedExcl_RecoJet_H2_b1_phi = ROOT.TH1F("hResolvedExcl_RecoJet_H2_b1_phi", ";#phi [rad];Events", 60, -3.0, 3.0)
        hResolvedExcl_RecoJet_H2_b2_phi = ROOT.TH1F("hResolvedExcl_RecoJet_H2_b2_phi", ";#phi [rad];Events", 60, -3.0, 3.0)
        hResolvedExcl_RecoJet_H1_b1_btag = ROOT.TH1F("hResolvedExcl_RecoJet_H1_b1_btag", ";b-discriminator;Events", 100, 0.0, 1.0)
        hResolvedExcl_RecoJet_H1_b2_btag = ROOT.TH1F("hResolvedExcl_RecoJet_H1_b2_btag", ";b-discriminator;Events", 100, 0.0, 1.0)
        hResolvedExcl_RecoJet_H2_b1_btag = ROOT.TH1F("hResolvedExcl_RecoJet_H2_b1_btag", ";b-discriminator;Events", 100, 0.0, 1.0)
        hResolvedExcl_RecoJet_H2_b2_btag = ROOT.TH1F("hResolvedExcl_RecoJet_H2_b2_btag", ";b-discriminator;Events", 100, 0.0, 1.0)
        hResolvedExcl_RecoJet_DeltaR_H1b1_H1b2 = ROOT.TH1F("hResolvedExcl_RecoJet_DeltaR_H1b1_H1b2", ";#Delta R;Events", 100, 0.0, 5.0);
        hResolvedExcl_RecoJet_DeltaR_H1b1_H2b1 = ROOT.TH1F("hResolvedExcl_RecoJet_DeltaR_H1b1_H2b1", ";#Delta R;Events", 100, 0.0, 5.0);
        hResolvedExcl_RecoJet_DeltaR_H1b1_H2b2 = ROOT.TH1F("hResolvedExcl_RecoJet_DeltaR_H1b1_H2b2", ";#Delta R;Events", 100, 0.0, 5.0);
        hResolvedExcl_RecoJet_DeltaR_H1b2_H2b1 = ROOT.TH1F("hResolvedExcl_RecoJet_DeltaR_H1b2_H2b1", ";#Delta R;Events", 100, 0.0, 5.0);
        hResolvedExcl_RecoJet_DeltaR_H1b2_H2b2 = ROOT.TH1F("hResolvedExcl_RecoJet_DeltaR_H1b2_H2b2", ";#Delta R;Events", 100, 0.0, 5.0);
        hResolvedExcl_RecoJet_DeltaR_H2b1_H2b2 = ROOT.TH1F("hResolvedExcl_RecoJet_DeltaR_H2b1_H2b2", ";#Delta R;Events", 100, 0.0, 5.0);
        hResolvedExcl_RecoJet_DeltaEta_H1b1_H1b2 = ROOT.TH1F("hResolvedExcl_RecoJet_DeltaEta_H1b1_H1b2", ";#Delta#eta;Events", 50, 0.0, 5.0);
        hResolvedExcl_RecoJet_DeltaEta_H1b1_H2b1 = ROOT.TH1F("hResolvedExcl_RecoJet_DeltaEta_H1b1_H2b1", ";#Delta#eta;Events", 50, 0.0, 5.0);
        hResolvedExcl_RecoJet_DeltaEta_H1b1_H2b2 = ROOT.TH1F("hResolvedExcl_RecoJet_DeltaEta_H1b1_H2b2", ";#Delta#eta;Events", 50, 0.0, 5.0);
        hResolvedExcl_RecoJet_DeltaEta_H1b2_H2b1 = ROOT.TH1F("hResolvedExcl_RecoJet_DeltaEta_H1b2_H2b1", ";#Delta#eta;Events", 50, 0.0, 5.0);
        hResolvedExcl_RecoJet_DeltaEta_H1b2_H2b2 = ROOT.TH1F("hResolvedExcl_RecoJet_DeltaEta_H1b2_H2b2", ";#Delta#eta;Events", 50, 0.0, 5.0);
        hResolvedExcl_RecoJet_DeltaEta_H2b1_H2b2 = ROOT.TH1F("hResolvedExcl_RecoJet_DeltaEta_H2b1_H2b2", ";#Delta#eta;Events", 50, 0.0, 5.0);
        hResolvedExcl_RecoJet_DeltaPhi_H1b1_H1b2 = ROOT.TH1F("hResolvedExcl_RecoJet_DeltaPhi_H1b1_H1b2", ";#Delta#phi;Events", 50, 0.0, 5.0);
        hResolvedExcl_RecoJet_DeltaPhi_H1b1_H2b1 = ROOT.TH1F("hResolvedExcl_RecoJet_DeltaPhi_H1b1_H2b1", ";#Delta#phi;Events", 50, 0.0, 5.0);
        hResolvedExcl_RecoJet_DeltaPhi_H1b1_H2b2 = ROOT.TH1F("hResolvedExcl_RecoJet_DeltaPhi_H1b1_H2b2", ";#Delta#phi;Events", 50, 0.0, 5.0);
        hResolvedExcl_RecoJet_DeltaPhi_H1b2_H2b1 = ROOT.TH1F("hResolvedExcl_RecoJet_DeltaPhi_H1b2_H2b1", ";#Delta#phi;Events", 50, 0.0, 5.0);
        hResolvedExcl_RecoJet_DeltaPhi_H1b2_H2b2 = ROOT.TH1F("hResolvedExcl_RecoJet_DeltaPhi_H1b2_H2b2", ";#Delta#phi;Events", 50, 0.0, 5.0);
        hResolvedExcl_RecoJet_DeltaPhi_H2b1_H2b2 = ROOT.TH1F("hResolvedExcl_RecoJet_DeltaPhi_H2b1_H2b2", ";#Delta#phi;Events", 50, 0.0, 5.0);
        hResolvedExcl_RecoJet_H1_pt  = ROOT.TH1F("hResolvedExcl_RecoJet_H1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedExcl_RecoJet_H2_pt  = ROOT.TH1F("hResolvedExcl_RecoJet_H2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedExcl_RecoJet_H1_eta = ROOT.TH1F("hResolvedExcl_RecoJet_H1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hResolvedExcl_RecoJet_H2_eta = ROOT.TH1F("hResolvedExcl_RecoJet_H2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hResolvedExcl_RecoJet_H1_phi = ROOT.TH1F("hResolvedExcl_RecoJet_H1_phi", ";#phi;Events", 60, -3.0, 3.0)
        hResolvedExcl_RecoJet_H2_phi = ROOT.TH1F("hResolvedExcl_RecoJet_H2_phi", ";#phi;Events", 60, -3.0, 3.0)
        hResolvedExcl_RecoJet_InvMass_H1 = ROOT.TH1F("hResolvedExcl_RecoJet_InvMass_H1", ";m_{H} [GeV]", 300, 0, 300)
        hResolvedExcl_RecoJet_InvMass_H2 = ROOT.TH1F("hResolvedExcl_RecoJet_InvMass_H2", ";m_{H} [GeV]", 300, 0, 300)
        hResolvedExcl_RecoJet_InvMassRegressed_H1 = ROOT.TH1F("hResolvedExcl_RecoJet_InvMassRegressed_H1", ";m_{H} [GeV]", 300, 0, 300)
        hResolvedExcl_RecoJet_InvMassRegressed_H2 = ROOT.TH1F("hResolvedExcl_RecoJet_InvMassRegressed_H2", ";m_{H} [GeV]", 300, 0, 300)
        hResolvedExcl_RecoJet_DeltaR_H1_H2 = ROOT.TH1F("hResolvedExcl_RecoJet_DeltaR_H1_H2", ";#Delta R;Events", 100, 0.0, 5.0)
        hResolvedExcl_RecoJet_DeltaEta_H1_H2 = ROOT.TH1F("hResolvedExcl_RecoJet_DeltaEta_H1_H2", ";#Delta#eta;Events", 50, 0.0, 5.0)
        hResolvedExcl_RecoJet_DeltaPhi_H1_H2 = ROOT.TH1F("hResolvedExcl_RecoJet_DeltaPhi_H1_H2", ";#Delta#phi;Events", 50, 0.0,5.0)
        hResolvedExcl_RecoJet_NJets = ROOT.TH1F("hResolvedExcl_RecoJet_NJets", "; jet multiplicity;Events", 15, 0, 15)
        hResolvedExcl_RecoJet_NFatJets = ROOT.TH1F("hResolvedExcl_RecoJet_NFatJets", "; fatjet multiplicity;Events", 10, 0, 10)
        
        hResolvedExcl_RecoJet_PFHT = ROOT.TH1F("hResolvedExcl_RecoJet_PFHT", "; PF H_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedExcl_RecoJet_NLooseBJets = ROOT.TH1I("hResolvedExcl_RecoJet_NLooseBJets", ";b-jets L;Events", 10, 0, 10)
        hResolvedExcl_RecoJet_NMediumBJets = ROOT.TH1I("hResolvedExcl_RecoJet_NMediumBJets", ";b-jets M;Events", 10, 0, 10)
        hResolvedExcl_RecoJet_NTightBJets = ROOT.TH1I("hResolvedExcl_RecoJet_NTightBJets", ";b-jets T;Events", 10, 0, 10)
        hResolvedExcl_RecoJet_Jet1Pt = ROOT.TH1F("hResolvedExcl_RecoJet_Jet1Pt", ";jet 1 p_{T} [GeV];Events", 100, 0.0, 500)
        hResolvedExcl_RecoJet_Jet2Pt = ROOT.TH1F("hResolvedExcl_RecoJet_Jet2Pt", ";jet 2 p_{T} [GeV];Events", 100, 0.0, 500)
        hResolvedExcl_RecoJet_Jet3Pt = ROOT.TH1F("hResolvedExcl_RecoJet_Jet3Pt", ";jet 3 p_{T} [GeV];Events", 100, 0.0, 500)
        hResolvedExcl_RecoJet_Jet4Pt = ROOT.TH1F("hResolvedExcl_RecoJet_Jet4Pt", ";jet 4 p_{T} [GeV];Events", 100, 0.0, 500)
        hResolvedExcl_RecoJet_Jet1Eta = ROOT.TH1F("hResolvedExcl_RecoJet_Jet1Eta", ";jet 1 #eta;Events", 120, -4.0, 4.0)
        hResolvedExcl_RecoJet_Jet2Eta = ROOT.TH1F("hResolvedExcl_RecoJet_Jet2Eta", ";jet 2 #eta;Events", 120, -4.0, 4.0)
        hResolvedExcl_RecoJet_Jet3Eta = ROOT.TH1F("hResolvedExcl_RecoJet_Jet3Eta", ";jet 3 #eta;Events", 120, -4.0, 4.0)
        hResolvedExcl_RecoJet_Jet4Eta = ROOT.TH1F("hResolvedExcl_RecoJet_Jet4Eta", ";jet 4 #eta;Events", 120, -4.0, 4.0)
        hResolvedExcl_RecoJet_AK8Jet1Pt = ROOT.TH1F("hResolvedExcl_RecoJet_AK8Jet1Pt", "; fatjet 1 p_{T} [GeV];Events", 200, 0.0, 1000)
        
        # Boosted histograms
        hBoosted_GenPart_H1_pt    = ROOT.TH1F("hBoosted_GenPart_H1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hBoosted_GenPart_H2_pt    = ROOT.TH1F("hBoosted_GenPart_H2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hBoosted_GenPart_H1_b1_pt = ROOT.TH1F("hBoosted_GenPart_H1_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hBoosted_GenPart_H1_b2_pt = ROOT.TH1F("hBoosted_GenPart_H1_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hBoosted_GenPart_H2_b1_pt = ROOT.TH1F("hBoosted_GenPart_H2_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hBoosted_GenPart_H2_b2_pt = ROOT.TH1F("hBoosted_GenPart_H2_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hBoosted_GenPart_H1_b1_eta = ROOT.TH1F("hBoosted_GenPart_H1_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hBoosted_GenPart_H1_b2_eta = ROOT.TH1F("hBoosted_GenPart_H1_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hBoosted_GenPart_H2_b1_eta = ROOT.TH1F("hBoosted_GenPart_H2_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hBoosted_GenPart_H2_b2_eta = ROOT.TH1F("hBoosted_GenPart_H2_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hBoosted_GenPart_H1_b1_phi = ROOT.TH1F("hBoosted_GenPart_H1_b1_phi", ";#phi [rad];Events", 60, -3.0, 3.0)
        hBoosted_GenPart_H1_b2_phi = ROOT.TH1F("hBoosted_GenPart_H1_b2_phi", ";#phi [rad];Events", 60, -3.0, 3.0)
        hBoosted_GenPart_H2_b1_phi = ROOT.TH1F("hBoosted_GenPart_H2_b1_phi", ";#phi [rad];Events", 60, -3.0, 3.0)
        hBoosted_GenPart_H2_b2_phi = ROOT.TH1F("hBoosted_GenPart_H2_b2_phi", ";#phi [rad];Events", 60, -3.0, 3.0)
        
        hBoosted_GenFatJet_H1_pt  = ROOT.TH1F("hBoosted_GenFatJet_H1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hBoosted_GenFatJet_H2_pt  = ROOT.TH1F("hBoosted_GenFatJet_H2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hBoosted_GenFatJet_H1_eta = ROOT.TH1F("hBoosted_GenFatJet_H1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hBoosted_GenFatJet_H2_eta = ROOT.TH1F("hBoosted_GenFatJet_H2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hBoosted_GenFatJet_H1_phi = ROOT.TH1F("hBoosted_GenFatJet_H1_phi", ";#phi [rad];Events", 60, -3.0, 3.0)
        hBoosted_GenFatJet_H2_phi = ROOT.TH1F("hBoosted_GenFatJet_H2_phi", ";#phi [rad];Events", 60, -3.0, 3.0)
        
        hBoosted_RecoFatJet_H1_pt  = ROOT.TH1F("hBoosted_RecoFatJet_H1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hBoosted_RecoFatJet_H2_pt  = ROOT.TH1F("hBoosted_RecoFatJet_H2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hBoosted_RecoFatJet_H1_eta = ROOT.TH1F("hBoosted_RecoFatJet_H1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hBoosted_RecoFatJet_H2_eta = ROOT.TH1F("hBoosted_RecoFatJet_H2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hBoosted_RecoFatJet_H1_phi = ROOT.TH1F("hBoosted_RecoFatJet_H1_phi", ";#phi [rad];Events", 60, -3.0, 3.0)
        hBoosted_RecoFatJet_H2_phi = ROOT.TH1F("hBoosted_RecoFatJet_H2_phi", ";#phi [rad];Events", 60, -3.0, 3.0)
        hBoosted_RecoFatJet_H1_TXbb = ROOT.TH1F("hBoosted_RecoFatJet_H1_TXbb", ";T_{Xbb} score;Events", 100, 0.0, 1.0)
        hBoosted_RecoFatJet_H2_TXbb = ROOT.TH1F("hBoosted_RecoFatJet_H2_TXbb", ";T_{Xbb} score;Events", 100, 0.0, 1.0)
        
        hBoosted_RecoFatJet_H1_m = ROOT.TH1F("hBoosted_RecoFatJet_H1_m", ";M [GeV];Events", 300, 0.0, 300)
        hBoosted_RecoFatJet_H2_m = ROOT.TH1F("hBoosted_RecoFatJet_H2_m", ";M [GeV];Events", 300, 0.0, 300)
        hBoosted_NJets = ROOT.TH1I("hBoosted_NJets", ";jets multiplicity;Events", 15, 0, 15)
        hBoosted_NFatJets = ROOT.TH1I("hBoosted_NFatJets", ";fatjets multiplicity;Events", 10, 0, 10)
        hBoosted_RecoFatJet_DeltaR_H1_H2 = ROOT.TH1F("hBoosted_RecoFatJet_DeltaR_H1_H2", ";#Delta R;Events", 100, 0.0, 5.0)
        hBoosted_RecoFatJet_DeltaEta_H1_H2 = ROOT.TH1F("hBoosted_RecoFatJet_DeltaEta_H1_H2", ";#Delta#eta;Events", 50, 0.0, 5.0)
        hBoosted_RecoFatJet_DeltaPhi_H1_H2 = ROOT.TH1F("hBoosted_RecoFatJet_DeltaPhi_H1_H2", ";#Delta#phi;Events", 50, 0.0, 5.0)

        hBoosted_RecoFatJet_H1_mSD_Uncorrected = ROOT.TH1F("hBoosted_RecoFatJet_H1_mSD_Uncorrected", ";m_{SD} [GeV];Events", 300, 0, 300)
        hBoosted_RecoFatJet_H1_area = ROOT.TH1F("hBoosted_RecoFatJet_H1_area", ";area;Events", 100, 0.0, 5.0)
        hBoosted_RecoFatJet_H1_n2b1 = ROOT.TH1F("hBoosted_RecoFatJet_H1_n2b1", ";n2b1;Events", 100, 0.0, 5.0)
        hBoosted_RecoFatJet_H1_n3b1 = ROOT.TH1F("hBoosted_RecoFatJet_H1_n3b1", ";n3b1;Events", 100, 0.0, 5.0)
        hBoosted_RecoFatJet_H1_tau21 = ROOT.TH1F("hBoosted_RecoFatJet_H1_tau21", ";#tau_{21};Events", 100, 0.0, 2.5)
        hBoosted_RecoFatJet_H1_tau32 = ROOT.TH1F("hBoosted_RecoFatJet_H1_tau32", ";#tau_{32};Events", 100, 0.0,2.5)
        hBoosted_RecoFatJet_H1_nsubjets = ROOT.TH1F("hBoosted_RecoFatJet_H1_nsubjets", ";subjet multiplicity;Events", 3, 0, 3)
        hBoosted_RecoFatJet_H1_subjet1_pt = ROOT.TH1F("hBoosted_RecoFatJet_H1_subjet1_pt", ";subjet 1 p_{T} [GeV];Events", 200, 0.0, 800)
        hBoosted_RecoFatJet_H1_subjet1_eta = ROOT.TH1F("hBoosted_RecoFatJet_H1_subjet1_eta", ";subjet 1 #eta;Events", 120, -4.0, 4.0)
        hBoosted_RecoFatJet_H1_subjet1_phi = ROOT.TH1F("hBoosted_RecoFatJet_H1_subjet1_phi", ";subjet 1 #phi;Events", 60, -3.0, 3.0)
        hBoosted_RecoFatJet_H1_subjet1_m = ROOT.TH1F("hBoosted_RecoFatJet_H1_subjet1_m", ";subjet 1 M [GeV];Events", 200, 0.0, 800)
        hBoosted_RecoFatJet_H1_subjet1_btag = ROOT.TH1F("hBoosted_RecoFatJet_H1_subjet1_btag", ";subjet 1 b-discriminator;Events", 100, 0.0, 1.0)
        hBoosted_RecoFatJet_H1_subjet2_pt = ROOT.TH1F("hBoosted_RecoFatJet_H1_subjet2_pt", ";subjet 2 p_{T} [GeV];Events", 200, 0.0, 800)
        hBoosted_RecoFatJet_H1_subjet2_eta = ROOT.TH1F("hBoosted_RecoFatJet_H1_subjet2_eta", ";subjet 2 #eta;Events", 120, -4.0, 4.0)
        hBoosted_RecoFatJet_H1_subjet2_phi = ROOT.TH1F("hBoosted_RecoFatJet_H1_subjet2_phi", ";subjet 2 #phi;Events", 60, -3.0, 3.0)
        hBoosted_RecoFatJet_H1_subjet2_m = ROOT.TH1F("hBoosted_RecoFatJet_H1_subjet2_m", ";subjet 2 M [GeV];Events", 200, 0.0, 800)
        hBoosted_RecoFatJet_H1_subjet2_btag = ROOT.TH1F("hBoosted_RecoFatJet_H1_subjet2_btag", ";subjet 2 b-discriminator;Events", 100,0.0, 1.0)
                
        hBoosted_RecoFatJet_H2_mSD_Uncorrected = ROOT.TH1F("hBoosted_RecoFatJet_H2_mSD_Uncorrected", ";m_{SD} [GeV];Events", 300, 0, 300)
        hBoosted_RecoFatJet_H2_area = ROOT.TH1F("hBoosted_RecoFatJet_H2_area", ";area;Events", 100, 0.0, 5.0)
        hBoosted_RecoFatJet_H2_n2b1 = ROOT.TH1F("hBoosted_RecoFatJet_H2_n2b1", ";n2b1;Events", 100, 0.0, 5.0)
        hBoosted_RecoFatJet_H2_n3b1 = ROOT.TH1F("hBoosted_RecoFatJet_H2_n3b1", ";n3b1;Events", 100, 0.0, 5.0)
        hBoosted_RecoFatJet_H2_tau21 = ROOT.TH1F("hBoosted_RecoFatJet_H2_tau21", ";#tau_{21};Events", 100, 0.0, 2.5)
        hBoosted_RecoFatJet_H2_tau32 = ROOT.TH1F("hBoosted_RecoFatJet_H2_tau32", ";#tau_{32};Events", 100, 0.0,2.5)
        hBoosted_RecoFatJet_H2_nsubjets = ROOT.TH1F("hBoosted_RecoFatJet_H2_nsubjets", ";subjet multiplicity;Events", 3, 0, 3)
        hBoosted_RecoFatJet_H2_subjet1_pt = ROOT.TH1F("hBoosted_RecoFatJet_H2_subjet1_pt", ";subjet 1 p_{T} [GeV];Events", 200, 0.0, 800)
        hBoosted_RecoFatJet_H2_subjet1_eta = ROOT.TH1F("hBoosted_RecoFatJet_H2_subjet1_eta", ";subjet 1 #eta;Events", 120, -4.0, 4.0)
        hBoosted_RecoFatJet_H2_subjet1_phi = ROOT.TH1F("hBoosted_RecoFatJet_H2_subjet1_phi", ";subjet 1 #phi;Events", 60, -3.0, 3.0)
        hBoosted_RecoFatJet_H2_subjet1_m = ROOT.TH1F("hBoosted_RecoFatJet_H2_subjet1_m", ";subjet 1 M [GeV];Events", 200, 0.0, 800)
        hBoosted_RecoFatJet_H2_subjet1_btag = ROOT.TH1F("hBoosted_RecoFatJet_H2_subjet1_btag", ";subjet 1 b-discriminator;Events", 100, 0.0, 1.0)
        hBoosted_RecoFatJet_H2_subjet2_pt = ROOT.TH1F("hBoosted_RecoFatJet_H2_subjet2_pt", ";subjet 2 p_{T} [GeV];Events", 200, 0.0, 800)
        hBoosted_RecoFatJet_H2_subjet2_eta = ROOT.TH1F("hBoosted_RecoFatJet_H2_subjet2_eta", ";subjet 2 #eta;Events", 120, -4.0, 4.0)
        hBoosted_RecoFatJet_H2_subjet2_phi = ROOT.TH1F("hBoosted_RecoFatJet_H2_subjet2_phi", ";subjet 2 #phi;Events", 60, -3.0, 3.0)
        hBoosted_RecoFatJet_H2_subjet2_m = ROOT.TH1F("hBoosted_RecoFatJet_H2_subjet2_m", ";subjet 2 M [GeV];Events", 200, 0.0, 800)
        hBoosted_RecoFatJet_H2_subjet2_btag = ROOT.TH1F("hBoosted_RecoFatJet_H2_subjet2_btag", ";subjet 2 b-discriminator;Events", 100,0.0, 1.0)
        
        # Semi-resolved regime
        hSemiresolved_GenPart_H1_pt    = ROOT.TH1F("hSemiresolved_GenPart_H1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hSemiresolved_GenPart_H2_pt    = ROOT.TH1F("hSemiresolved_GenPart_H2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hSemiresolved_GenPart_H1_b1_pt = ROOT.TH1F("hSemiresolved_GenPart_H1_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hSemiresolved_GenPart_H1_b2_pt = ROOT.TH1F("hSemiresolved_GenPart_H1_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hSemiresolved_GenPart_H2_b1_pt = ROOT.TH1F("hSemiresolved_GenPart_H2_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hSemiresolved_GenPart_H2_b2_pt = ROOT.TH1F("hSemiresolved_GenPart_H2_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hSemiresolved_GenPart_H1_b1_eta = ROOT.TH1F("hSemiresolved_GenPart_H1_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolved_GenPart_H1_b2_eta = ROOT.TH1F("hSemiresolved_GenPart_H1_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolved_GenPart_H2_b1_eta = ROOT.TH1F("hSemiresolved_GenPart_H2_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolved_GenPart_H2_b2_eta = ROOT.TH1F("hSemiresolved_GenPart_H2_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolved_GenPart_H1_b1_phi = ROOT.TH1F("hSemiresolved_GenPart_H1_b1_phi", ";#phi [rad];Events", 60, -3.0, 3.0)
        hSemiresolved_GenPart_H1_b2_phi = ROOT.TH1F("hSemiresolved_GenPart_H1_b2_phi", ";#phi [rad];Events", 60, -3.0, 3.0)
        hSemiresolved_GenPart_H2_b1_phi = ROOT.TH1F("hSemiresolved_GenPart_H2_b1_phi", ";#phi [rad];Events", 60, -3.0, 3.0)
        hSemiresolved_GenPart_H2_b2_phi = ROOT.TH1F("hSemiresolved_GenPart_H2_b2_phi", ";#phi [rad];Events", 60, -3.0, 3.0)
        
        hSemiresolved_H1Boosted_H2resolved_GenFatJet_H1_pt = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_GenFatJet_H1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hSemiresolved_H1Boosted_H2resolved_GenFatJet_H1_eta = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_GenFatJet_H1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolved_H1Boosted_H2resolved_GenFatJet_H1_phi = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_GenFatJet_H1_phi", ";#phi [rad];Events", 60, -3.0, 3.0)
        hSemiresolved_H1Boosted_H2resolved_GenJet_H2_b1_pt = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_GenJet_H2_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 800)
        hSemiresolved_H1Boosted_H2resolved_GenJet_H2_b2_pt = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_GenJet_H2_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 800)
        hSemiresolved_H1Boosted_H2resolved_GenJet_H2_b1_eta = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_GenJet_H2_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolved_H1Boosted_H2resolved_GenJet_H2_b2_eta = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_GenJet_H2_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolved_H1Boosted_H2resolved_GenJet_H2_b1_phi = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_GenJet_H2_b1_phi", ";#phi [rad];Events", 60, -3.0, 3.0)
        hSemiresolved_H1Boosted_H2resolved_GenJet_H2_b2_phi = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_GenJet_H2_b2_phi", ";#phi [rad];Events", 60, -3.0, 3.0)
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_pt = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_eta = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_phi = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_phi", ";#phi [rad];Events", 60, -3.0, 3.0)
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_m = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_m", ";H_{1} mass", 300, 0, 300)
        hSemiresolved_H1Boosted_H2resolved_RecoJet_H2_b1_pt = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_RecoJet_H2_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 800)
        hSemiresolved_H1Boosted_H2resolved_RecoJet_H2_b2_pt = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_RecoJet_H2_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 800)
        hSemiresolved_H1Boosted_H2resolved_RecoJet_H2_b1_eta = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_RecoJet_H2_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolved_H1Boosted_H2resolved_RecoJet_H2_b2_eta = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_RecoJet_H2_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolved_H1Boosted_H2resolved_RecoJet_H2_b1_phi = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_RecoJet_H2_b1_phi", ";#phi [rad];Events", 60, -3.0, 3.0)
        hSemiresolved_H1Boosted_H2resolved_RecoJet_H2_b2_phi = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_RecoJet_H2_b2_phi", ";#phi [rad];Events", 60, -3.0, 3.0)
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_TXbb = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_TXbb", ";T_{Xbb} score;Events", 100, 0.0, 1.0)
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_TXbb = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_TXbb", ";T_{Xbb} score;Events", 100, 0.0, 1.0)
                
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_mSD_Uncorrected = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_mSD_Uncorrected", ";m_{SD} [GeV];Events", 300, 0, 300) 
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_area = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_area", ";area;Events", 100, 0.0, 5.0)
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_n2b1 = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_n2b1", ";n2b1;Events", 100, 0.0, 5.0)
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_n3b1 = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_n3b1", ";n3b1;Events", 100, 0.0, 5.0)
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_tau21 = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_tau21", ";#tau_{21};Events", 100, 0.0, 2.5)
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_tau32 = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_tau32", ";#tau_{32};Events", 100, 0.0, 2.5)
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_nsubjets = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_nsubjets", ";subjet multiplicity;Events", 3, 0, 3)
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_pt = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_pt", ";subjet 1 p_{T} [GeV];Events", 200, 0.0, 800)
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_eta = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_eta", ";subjet 1 #eta;Events", 120, -4.0, 4.0)
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_phi = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_phi", ";subjet 1 #phi;Events", 60, -3.0, 3.0)
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_m = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_m", ";subjet 1 M [GeV];Events", 200, 0.0, 800)
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_btag = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_btag", ";subjet 1 b-discriminator;Events", 100, 0.0, 1.0)
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_pt = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_pt", ";subjet 2 p_{T} [GeV];Events", 200, 0.0, 800)
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_eta = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_eta", ";subjet 2 #eta;Events", 120, -4.0, 4.0)
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_phi = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_phi", ";subjet 2 #phi;Events", 60, -3.0, 3.0)
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_m = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_m", ";subjet 2 M [GeV];Events", 200, 0.0, 800)
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_btag = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_btag", ";subjet 2 b-discriminator;Events", 100,0.0, 1.0)
        
        hSemiresolved_H1Boosted_H2resolved_NJets = ROOT.TH1I("hSemiresolved_H1Boosted_H2resolved_NJets", "; jets multiplicity;Events", 15, 0, 15)
        hSemiresolved_H1Boosted_H2resolved_NFatJets = ROOT.TH1I("hSemiresolved_H1Boosted_H2resolved_NFatJets", ";fatjets multiplicity;Events", 10, 0, 10)
        hSemiresolved_H1Boosted_H2resolved_DeltaR_H1_H2 = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_DeltaR_H1_H2", ";#Delta R;Events", 100, 0.0, 5.0)
        hSemiresolved_H1Boosted_H2resolved_DeltaEta_H1_H2 = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_DeltaEta_H1_H2", ";#Delta#eta;Events", 50, 0.0, 5.0)
        hSemiresolved_H1Boosted_H2resolved_DeltaPhi_H1_H2 = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_DeltaPhi_H1_H2", ";#Delta#phi;Events", 50, 0.0,5.0)
        hSemiresolved_H1Boosted_H2resolved_InvMass_H2 = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_InvMass_H2", ";m_{H} [GeV]", 300, 0, 300)
        hSemiresolved_H1Boosted_H2resolved_InvMassRegressed_H2 = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_InvMassRegressed_H2", ";m_{H} [GeV]", 300, 0, 300)
        hSemiresolved_H1Boosted_H2resolved_H2_pt = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_H2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hSemiresolved_H1Boosted_H2resolved_H2_eta = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_H2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolved_H1Boosted_H2resolved_H2_phi = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_H2_phi", ";#phi;Events", 60, -3.0, 3.0)
        
        
        hSemiresolved_H1Boosted_H2resolved_PFHT = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_PFHT", "; PF H_{T} [GeV];Events", 200, 0.0, 1000)
        hSemiresolved_H1Boosted_H2resolved_NLooseBJets = ROOT.TH1I("hSemiresolved_H1Boosted_H2resolved_NLooseBJets", ";b-jets L;Events", 10, 0, 10)
        hSemiresolved_H1Boosted_H2resolved_NMediumBJets = ROOT.TH1I("hSemiresolved_H1Boosted_H2resolved_NMediumBJets", ";b-jets M;Events", 10, 0, 10)
        hSemiresolved_H1Boosted_H2resolved_NTightBJets = ROOT.TH1I("hSemiresolved_H1Boosted_H2resolved_NTightBJets", ";b-jets T;Events", 10, 0, 10)
        hSemiresolved_H1Boosted_H2resolved_Jet1Pt = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_Jet1Pt", ";jet 1 p_{T} [GeV];Events", 100, 0.0, 500)
        hSemiresolved_H1Boosted_H2resolved_Jet2Pt = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_Jet2Pt", ";jet 2 p_{T} [GeV];Events", 100, 0.0, 500)
        hSemiresolved_H1Boosted_H2resolved_Jet3Pt = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_Jet3Pt", ";jet 3 p_{T} [GeV];Events", 100, 0.0, 500)
        hSemiresolved_H1Boosted_H2resolved_Jet4Pt = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_Jet4Pt", ";jet 4 p_{T} [GeV];Events", 100, 0.0, 500)
        hSemiresolved_H1Boosted_H2resolved_Jet1Eta = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_Jet1Eta", ";jet 1 #eta;Events", 120, -4.0, 4.0)
        hSemiresolved_H1Boosted_H2resolved_Jet2Eta = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_Jet2Eta", ";jet 2 #eta;Events", 120, -4.0, 4.0)
        hSemiresolved_H1Boosted_H2resolved_Jet3Eta = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_Jet3Eta", ";jet 3 #eta;Events", 120, -4.0, 4.0)
        hSemiresolved_H1Boosted_H2resolved_Jet4Eta = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_Jet4Eta", ";jet 4 #eta;Events", 120, -4.0, 4.0)
        hSemiresolved_H1Boosted_H2resolved_AK8Jet1Pt = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_AK8Jet1Pt", "; fatjet 1 p_{T} [GeV];Events", 200, 0.0, 1000)
        




        hSemiresolved_H2Boosted_H1resolved_NJets = ROOT.TH1I("hSemiresolved_H2Boosted_H1resolved_NJets", ";jets multiplicity;Events", 15, 0, 15)
        hSemiresolved_H2Boosted_H1resolved_NFatJets = ROOT.TH1I("hSemiresolved_H2Boosted_H1resolved_NFatJets", ";fatjets multiplicity;Events", 10, 0, 10)
        hSemiresolved_H2Boosted_H1resolved_DeltaR_H1_H2 = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_DeltaR_H1_H2", ";#Delta R;Events", 100, 0.0, 5.0)
        hSemiresolved_H2Boosted_H1resolved_DeltaEta_H1_H2 = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_DeltaEta_H1_H2", ";#Delta#eta;Events", 50, 0.0, 5.0)
        hSemiresolved_H2Boosted_H1resolved_DeltaPhi_H1_H2 = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_DeltaPhi_H1_H2", ";#Delta#phi;Events", 50, 0.0, 5.0)
        hSemiresolved_H2Boosted_H1resolved_InvMass_H1 = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_InvMass_H1", ";m_{H} [GeV]", 300, 0, 300)
        hSemiresolved_H2Boosted_H1resolved_InvMassRegressed_H1 = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_InvMassRegressed_H1", ";m_{H} [GeV]", 300, 0, 300)
        hSemiresolved_H2Boosted_H1resolved_H1_pt = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_H1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hSemiresolved_H2Boosted_H1resolved_H1_eta = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_H1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolved_H2Boosted_H1resolved_H1_phi = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_H1_phi", ";#phi;Events", 60, -3.0, 3.0)
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_m = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_m", ";m_{H} [GeV]", 300, 0, 300)
        
        hSemiresolved_H2Boosted_H1resolved_GenFatJet_H2_pt = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_GenFatJet_H2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hSemiresolved_H2Boosted_H1resolved_GenFatJet_H2_eta = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_GenFatJet_H2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolved_H2Boosted_H1resolved_GenFatJet_H2_phi = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_GenFatJet_H2_phi", ";#phi [rad];Events", 60, -3.0, 3.0)
        hSemiresolved_H2Boosted_H1resolved_GenJet_H1_b1_pt = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_GenJet_H1_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 800)
        hSemiresolved_H2Boosted_H1resolved_GenJet_H1_b2_pt = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_GenJet_H1_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 800)
        hSemiresolved_H2Boosted_H1resolved_GenJet_H1_b1_eta = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_GenJet_H1_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolved_H2Boosted_H1resolved_GenJet_H1_b2_eta = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_GenJet_H1_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolved_H2Boosted_H1resolved_GenJet_H1_b1_phi = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_GenJet_H1_b1_phi", ";#phi [rad];Events", 60, -3.0, 3.0)
        hSemiresolved_H2Boosted_H1resolved_GenJet_H1_b2_phi = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_GenJet_H1_b2_phi", ";#phi [rad];Events", 60, -3.0, 3.0)
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_pt = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_eta = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_phi = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_phi", ";#phi [rad];Events", 60, -3.0, 3.0)
        hSemiresolved_H2Boosted_H1resolved_RecoJet_H1_b1_pt = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_RecoJet_H1_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 800)
        hSemiresolved_H2Boosted_H1resolved_RecoJet_H1_b2_pt = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_RecoJet_H1_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 800)
        hSemiresolved_H2Boosted_H1resolved_RecoJet_H1_b1_eta = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_RecoJet_H1_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolved_H2Boosted_H1resolved_RecoJet_H1_b2_eta = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_RecoJet_H1_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolved_H2Boosted_H1resolved_RecoJet_H1_b1_phi = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_RecoJet_H1_b1_phi", ";#phi [rad];Events", 60, -3.0, 3.0)
        hSemiresolved_H2Boosted_H1resolved_RecoJet_H1_b2_phi = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_RecoJet_H1_b2_phi", ";#phi [rad];Events", 60, -3.0, 3.0)
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_mSD_Uncorrected = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_mSD_Uncorrected", ";m_{SD} [GeV];Events", 300, 0, 300)
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_area = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_area", ";area;Events", 100, 0.0, 5.0)
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_n2b1 = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_n2b1", ";n2b1;Events", 100, 0.0, 5.0)
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_n3b1 = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_n3b1", ";n3b2;Events", 100, 0.0, 5.0)
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_tau21 = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_tau21", ";#tau_{21};Events", 100, 0.0, 2.5)
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_tau32 = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_tau32", ";#tau_{32};Events", 100, 0.0, 2.5)
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_nsubjets = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_nsubjets", ";subjet multiplicity;Events", 3, 0, 3)
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_pt = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_pt", ";subjet 1 p_{T} [GeV];Events", 200, 0.0, 800)
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_eta = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_eta", ";subjet 1 #eta;Events", 120, -4.0, 4.0)
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_phi = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_phi", ";subjet 1 #phi;Events", 60, -3.0, 3.0)
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_m = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_m", ";subjet 1 M [GeV];Events", 200, 0.0, 800)
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_btag = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_btag", ";subjet 1 b-discriminator;Events", 100, 0.0, 1.0)
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_pt = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_pt", ";subjet 2 p_{T} [GeV];Events", 200, 0.0, 800)
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_eta = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_eta", ";subjet 2 #eta;Events", 120, -4.0, 4.0)
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_phi = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_phi", ";subjet 2 #phi;Events", 60, -3.0, 3.0)
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_m = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_m", ";subjet 2 M [GeV];Events", 200, 0.0, 800)
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_btag = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_btag", ";subjet 2 b-discriminator;Events", 100,0.0, 1.0)
        
        hPassed_HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5 = ROOT.TH1I("hPassed_HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5", ";trigger bit;Events", 2, 0, 2)
        hPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np4 = ROOT.TH1I("hPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np4", ";trigger bit;Events", 2, 0,2)
        hPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np2 = ROOT.TH1I("hPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np2", ";trigger bit;Events", 2, 0,2)
        hPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p1 = ROOT.TH1I("hPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p1", ";trigger bit;Events", 2, 0,2)
        hPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p17 = ROOT.TH1I("hPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p17", ";trigger bit;Events", 2, 0,2)
        hPassed_HLT_PFHT1050 = ROOT.TH1I("hPassed_HLT_PFHT1050", ";trigger bit;Events", 2, 0,2)
        hPassed_HLT_PFJet500 = ROOT.TH1I("hPassed_HLT_PFJet500", ";trigger bit;Events", 2, 0,2)
        hPassed_HLT_AK8PFHT800_TrimMass50  = ROOT.TH1I("hPassed_HLT_AK8PFHT800_TrimMass50", ";trigger bit;Events", 2, 0,2)
        hPassed_HLT_AK8PFJet400_TrimMass30 = ROOT.TH1I("hPassed_HLT_AK8PFJet400_TrimMass30", ";trigger bit;Events", 2, 0,2)
        hPassed_HLT_AK8PFJet420_TrimMass30 = ROOT.TH1I("hPassed_HLT_AK8PFJet420_TrimMass30", ";trigger bit;Events", 2, 0,2)
        hPassed_HLT_AK8PFJet500 = ROOT.TH1I("hPassed_HLT_AK8PFJet500", ";trigger bit;Events", 2, 0,2)
        hPassed_HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59 = ROOT.TH1I("hPassed_HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59", ";trigger bit;Events", 2, 0,2)
        hPassed_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94 = ROOT.TH1I("hPassed_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94", ";trigger bit;Events", 2, 0,2)
        hPassed_HLT_AK8PFHT750_TrimMass50 = ROOT.TH1I("hPassed_HLT_AK8PFHT750_TrimMass50", ";trigger bit;Events", 2, 0,2)
        hPassed_HLT_AK8PFJet360_TrimMass30 = ROOT.TH1I("hPassed_HLT_AK8PFJet360_TrimMass30", ";trigger bit;Events", 2, 0,2)
        hPassed_HLT_AK8PFJet380_TrimMass30 = ROOT.TH1I("hPassed_HLT_AK8PFJet380_TrimMass30", ";trigger bit;Events", 2, 0,2)
        hPassed_OR = ROOT.TH1I("hPassed_OR", ";trigger bit;Events", 2, 0,2)
        
        # Resolved
        hResolvedPassed_HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5 = ROOT.TH1I("hResolvedPassed_HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5", ";trigger bit;Events", 2, 0, 2)
        hResolvedPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np4 = ROOT.TH1I("hResolvedPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np4", ";trigger bit;Events", 2, 0,2)
        hResolvedPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np2 = ROOT.TH1I("hResolvedPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np2", ";trigger bit;Events", 2, 0,2)
        hResolvedPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p1 = ROOT.TH1I("hResolvedPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p1", ";trigger bit;Events", 2, 0,2)
        hResolvedPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p17 = ROOT.TH1I("hResolvedPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p17", ";trigger bit;Events", 2, 0,2)
        hResolvedPassed_HLT_PFHT1050 = ROOT.TH1I("hResolvedPassed_HLT_PFHT1050", ";trigger bit;Events", 2, 0,2)
        hResolvedPassed_HLT_PFJet500 = ROOT.TH1I("hResolvedPassed_HLT_PFJet500", ";trigger bit;Events", 2, 0,2)
        hResolvedPassed_HLT_AK8PFHT800_TrimMass50  = ROOT.TH1I("hResolvedPassed_HLT_AK8PFHT800_TrimMass50", ";trigger bit;Events", 2, 0,2)
        hResolvedPassed_HLT_AK8PFJet400_TrimMass30 = ROOT.TH1I("hResolvedPassed_HLT_AK8PFJet400_TrimMass30", ";trigger bit;Events", 2, 0,2)
        hResolvedPassed_HLT_AK8PFJet420_TrimMass30 = ROOT.TH1I("hResolvedPassed_HLT_AK8PFJet420_TrimMass30", ";trigger bit;Events", 2, 0,2)
        hResolvedPassed_HLT_AK8PFJet500 = ROOT.TH1I("hResolvedPassed_HLT_AK8PFJet500", ";trigger bit;Events", 2, 0,2)
        hResolvedPassed_HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59 = ROOT.TH1I("hResolvedPassed_HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59", ";trigger bit;Events", 2, 0,2)
        hResolvedPassed_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94 = ROOT.TH1I("hResolvedPassed_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94", ";trigger bit;Events", 2, 0,2)
        hResolvedPassed_HLT_AK8PFHT750_TrimMass50 = ROOT.TH1I("hResolvedPassed_HLT_AK8PFHT750_TrimMass50", ";trigger bit;Events", 2, 0,2)
        hResolvedPassed_HLT_AK8PFJet360_TrimMass30 = ROOT.TH1I("hResolvedPassed_HLT_AK8PFJet360_TrimMass30", ";trigger bit;Events", 2, 0,2)
        hResolvedPassed_HLT_AK8PFJet380_TrimMass30 = ROOT.TH1I("hResolvedPassed_HLT_AK8PFJet380_TrimMass30", ";trigger bit;Events", 2, 0,2)
        hResolvedPassed_OR = ROOT.TH1I("hResolvedPassed_OR", ";trigger bit;Events", 2, 0,2)

        # Resolved exclusive
        hResolvedExclPassed_HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5 = ROOT.TH1I("hResolvedExclPassed_HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5", ";trigger bit;Events", 2, 0, 2)
        hResolvedExclPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np4 = ROOT.TH1I("hResolvedExclPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np4", ";trigger bit;Events", 2, 0,2)
        hResolvedExclPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np2 = ROOT.TH1I("hResolvedExclPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np2", ";trigger bit;Events", 2, 0,2)
        hResolvedExclPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p1 = ROOT.TH1I("hResolvedExclPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p1", ";trigger bit;Events", 2, 0,2)
        hResolvedExclPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p17 = ROOT.TH1I("hResolvedExclPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p17", ";trigger bit;Events", 2, 0,2)
        hResolvedExclPassed_HLT_PFHT1050 = ROOT.TH1I("hResolvedExclPassed_HLT_PFHT1050", ";trigger bit;Events", 2, 0,2)
        hResolvedExclPassed_HLT_PFJet500 = ROOT.TH1I("hResolvedExclPassed_HLT_PFJet500", ";trigger bit;Events", 2, 0,2)
        hResolvedExclPassed_HLT_AK8PFHT800_TrimMass50  = ROOT.TH1I("hResolvedExclPassed_HLT_AK8PFHT800_TrimMass50", ";trigger bit;Events", 2, 0,2)
        hResolvedExclPassed_HLT_AK8PFJet400_TrimMass30 = ROOT.TH1I("hResolvedExclPassed_HLT_AK8PFJet400_TrimMass30", ";trigger bit;Events", 2, 0,2)
        hResolvedExclPassed_HLT_AK8PFJet420_TrimMass30 = ROOT.TH1I("hResolvedExclPassed_HLT_AK8PFJet420_TrimMass30", ";trigger bit;Events", 2, 0,2)
        hResolvedExclPassed_HLT_AK8PFJet500 = ROOT.TH1I("hResolvedExclPassed_HLT_AK8PFJet500", ";trigger bit;Events", 2, 0,2)
        hResolvedExclPassed_HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59 = ROOT.TH1I("hResolvedExclPassed_HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59", ";trigger bit;Events", 2, 0,2)
        hResolvedExclPassed_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94 = ROOT.TH1I("hResolvedExclPassed_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94", ";trigger bit;Events", 2, 0,2)
        hResolvedExclPassed_HLT_AK8PFHT750_TrimMass50 = ROOT.TH1I("hResolvedExclPassed_HLT_AK8PFHT750_TrimMass50", ";trigger bit;Events", 2, 0,2)
        hResolvedExclPassed_HLT_AK8PFJet360_TrimMass30 = ROOT.TH1I("hResolvedExclPassed_HLT_AK8PFJet360_TrimMass30", ";trigger bit;Events", 2, 0,2)
        hResolvedExclPassed_HLT_AK8PFJet380_TrimMass30 = ROOT.TH1I("hResolvedExclPassed_HLT_AK8PFJet380_TrimMass30", ";trigger bit;Events", 2, 0,2)
        hResolvedExclPassed_OR = ROOT.TH1I("hResolvedExclPassed_OR", ";trigger bit;Events", 2, 0,2)

        

        # Semi-resolved
        hSemiresolvedPassed_HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5 = ROOT.TH1I("hSemiresolvedPassed_HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5", ";trigger bit;Events", 2, 0, 2)
        hSemiresolvedPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np4 = ROOT.TH1I("hSemiresolvedPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np4", ";trigger bit;Events", 2, 0,2)
        hSemiresolvedPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np2 = ROOT.TH1I("hSemiresolvedPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np2", ";trigger bit;Events", 2, 0,2)
        hSemiresolvedPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p1 = ROOT.TH1I("hSemiresolvedPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p1", ";trigger bit;Events", 2, 0,2)
        hSemiresolvedPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p17 = ROOT.TH1I("hSemiresolvedPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p17", ";trigger bit;Events", 2, 0,2)
        hSemiresolvedPassed_HLT_PFHT1050 = ROOT.TH1I("hSemiresolvedPassed_HLT_PFHT1050", ";trigger bit;Events", 2, 0,2)
        hSemiresolvedPassed_HLT_PFJet500 = ROOT.TH1I("hSemiresolvedPassed_HLT_PFJet500", ";trigger bit;Events", 2, 0,2)
        hSemiresolvedPassed_HLT_AK8PFHT800_TrimMass50  = ROOT.TH1I("hSemiresolvedPassed_HLT_AK8PFHT800_TrimMass50", ";trigger bit;Events", 2, 0,2)
        hSemiresolvedPassed_HLT_AK8PFJet400_TrimMass30 = ROOT.TH1I("hSemiresolvedPassed_HLT_AK8PFJet400_TrimMass30", ";trigger bit;Events", 2, 0,2)
        hSemiresolvedPassed_HLT_AK8PFJet420_TrimMass30 = ROOT.TH1I("hSemiresolvedPassed_HLT_AK8PFJet420_TrimMass30", ";trigger bit;Events", 2, 0,2)
        hSemiresolvedPassed_HLT_AK8PFJet500 = ROOT.TH1I("hSemiresolvedPassed_HLT_AK8PFJet500", ";trigger bit;Events", 2, 0,2)
        hSemiresolvedPassed_HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59 = ROOT.TH1I("hSemiresolvedPassed_HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59", ";trigger bit;Events", 2, 0,2)
        hSemiresolvedPassed_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94 = ROOT.TH1I("hSemiresolvedPassed_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94", ";trigger bit;Events", 2, 0,2)
        hSemiresolvedPassed_HLT_AK8PFHT750_TrimMass50 = ROOT.TH1I("hSemiresolvedPassed_HLT_AK8PFHT750_TrimMass50", ";trigger bit;Events", 2, 0,2)
        hSemiresolvedPassed_HLT_AK8PFJet360_TrimMass30 = ROOT.TH1I("hSemiresolvedPassed_HLT_AK8PFJet360_TrimMass30", ";trigger bit;Events", 2, 0,2)
        hSemiresolvedPassed_HLT_AK8PFJet380_TrimMass30 = ROOT.TH1I("hSemiresolvedPassed_HLT_AK8PFJet380_TrimMass30", ";trigger bit;Events", 2, 0,2)
        hSemiresolvedPassed_OR = ROOT.TH1I("hSemiresolvedPassed_OR", ";trigger bit;Events", 2, 0,2)
        
        # Boosted
        hBoostedPassed_HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5 = ROOT.TH1I("hBoostedPassed_HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5", ";trigger bit;Events", 2, 0, 2)
        hBoostedPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np4 = ROOT.TH1I("hBoostedPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np4", ";trigger bit;Events", 2, 0,2)
        hBoostedPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np2 = ROOT.TH1I("hBoostedPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np2", ";trigger bit;Events", 2, 0,2)
        hBoostedPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p1 = ROOT.TH1I("hBoostedPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p1", ";trigger bit;Events", 2, 0,2)
        hBoostedPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p17 = ROOT.TH1I("hBoostedPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p17", ";trigger bit;Events", 2, 0,2)
        hBoostedPassed_HLT_PFHT1050 = ROOT.TH1I("hBoostedPassed_HLT_PFHT1050", ";trigger bit;Events", 2, 0,2)
        hBoostedPassed_HLT_PFJet500 = ROOT.TH1I("hBoostedPassed_HLT_PFJet500", ";trigger bit;Events", 2, 0,2)
        hBoostedPassed_HLT_AK8PFHT800_TrimMass50  = ROOT.TH1I("hBoostedPassed_HLT_AK8PFHT800_TrimMass50", ";trigger bit;Events", 2, 0,2)
        hBoostedPassed_HLT_AK8PFJet400_TrimMass30 = ROOT.TH1I("hBoostedPassed_HLT_AK8PFJet400_TrimMass30", ";trigger bit;Events", 2, 0,2)
        hBoostedPassed_HLT_AK8PFJet420_TrimMass30 = ROOT.TH1I("hBoostedPassed_HLT_AK8PFJet420_TrimMass30", ";trigger bit;Events", 2, 0,2)
        hBoostedPassed_HLT_AK8PFJet500 = ROOT.TH1I("hBoostedPassed_HLT_AK8PFJet500", ";trigger bit;Events", 2, 0,2)
        hBoostedPassed_HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59 = ROOT.TH1I("hBoostedPassed_HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59", ";trigger bit;Events", 2, 0,2)
        hBoostedPassed_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94 = ROOT.TH1I("hBoostedPassed_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94", ";trigger bit;Events", 2, 0,2)
        hBoostedPassed_HLT_AK8PFHT750_TrimMass50 = ROOT.TH1I("hBoostedPassed_HLT_AK8PFHT750_TrimMass50", ";trigger bit;Events", 2, 0,2)
        hBoostedPassed_HLT_AK8PFJet360_TrimMass30 = ROOT.TH1I("hBoostedPassed_HLT_AK8PFJet360_TrimMass30", ";trigger bit;Events", 2, 0,2)
        hBoostedPassed_HLT_AK8PFJet380_TrimMass30 = ROOT.TH1I("hBoostedPassed_HLT_AK8PFJet380_TrimMass30", ";trigger bit;Events", 2, 0,2)
        hBoostedPassed_OR = ROOT.TH1I("hBoostedPassed_OR", ";trigger bit;Events", 2, 0,2)


        # Initialize counters
        cIsResolvedGen     = 0.0
        cIsBoostedGen      = 0.0
        cIsSemiResolvedGen = 0.0

        cIsResolvedReco     = 0.0
        cIsResolvedRecoExcl = 0.0
        cIsBoostedReco      = 0.0
        cIsSemiResolvedReco = 0.0
        cNotMatchedReco = 0.0

        print("\nProcessing sample %s" % (sample))
        print("Entries = %s" % (entries))
        
        # Loop over all events
        for i, e in enumerate(t):
            
            #print("\n Entry = %s" % (i))
            
            #================================================== Gen-level matching
            bH1_b1_genjet = e.gen_H1_b1_genjet_pt > 0.0
            bH1_b2_genjet = e.gen_H1_b2_genjet_pt > 0.0
            bH2_b1_genjet = e.gen_H2_b1_genjet_pt > 0.0
            bH2_b2_genjet = e.gen_H2_b2_genjet_pt > 0.0
            
            bH1_b1_genfatjet = e.gen_H1_b1_genfatjet_pt > 0.0
            bH1_b2_genfatjet = e.gen_H1_b2_genfatjet_pt > 0.0
            bH2_b1_genfatjet = e.gen_H2_b1_genfatjet_pt > 0.0
            bH2_b2_genfatjet = e.gen_H2_b2_genfatjet_pt > 0.0
            
            bH1_genfatjet = bH1_b1_genfatjet and bH1_b2_genfatjet and areSameJets(e.gen_H1_b1_genfatjet_eta, e.gen_H1_b2_genfatjet_eta, e.gen_H1_b1_genfatjet_phi, e.gen_H1_b2_genfatjet_phi)
            bH2_genfatjet = bH2_b1_genfatjet and bH2_b2_genfatjet and areSameJets(e.gen_H2_b1_genfatjet_eta, e.gen_H2_b2_genfatjet_eta, e.gen_H2_b1_genfatjet_phi, e.gen_H2_b2_genfatjet_phi)
            
            bH1_genfatjet_only = bH1_genfatjet and not bH2_genfatjet
            bH2_genfatjet_only = bH2_genfatjet and not bH1_genfatjet
            
            bH1Boosted_H2resolved_gen = bH1_genfatjet_only and bH2_b1_genjet and bH2_b2_genjet
            bH2Boosted_H1resolved_gen = bH2_genfatjet_only and bH1_b1_genjet and bH1_b2_genjet
            
            # Gen-level:
            bIsSemiResolvedGen = bH1Boosted_H2resolved_gen or bH2Boosted_H1resolved_gen
            bIsBoostedGen  = bH1_genfatjet and bH2_genfatjet
            bIsResolvedGen = bH1_b1_genjet and bH1_b2_genjet and bH2_b1_genjet and bH2_b2_genjet
                        
            if (bIsSemiResolvedGen): cIsSemiResolvedGen += 1
            if (bIsBoostedGen): cIsBoostedGen += 1
            if (bIsResolvedGen): cIsResolvedGen += 1

            #================================================== Reco-level matching
            bH1_b1_recojet = e.gen_H1_b1_recojet_pt > 0.0
            bH1_b2_recojet = e.gen_H1_b2_recojet_pt > 0.0
            bH2_b1_recojet = e.gen_H2_b1_recojet_pt > 0.0
            bH2_b2_recojet = e.gen_H2_b2_recojet_pt > 0.0
            
            bH1_b1_recofatjet = e.gen_H1_b1_recofatjet_pt > 0.0
            bH1_b2_recofatjet = e.gen_H1_b2_recofatjet_pt > 0.0
            bH2_b1_recofatjet = e.gen_H2_b1_recofatjet_pt > 0.0
            bH2_b2_recofatjet = e.gen_H2_b2_recofatjet_pt > 0.0
            
            bH1_recofatjet = bH1_genfatjet and bH1_b1_recofatjet and bH1_b2_recofatjet and areSameJets(e.gen_H1_b1_recofatjet_eta, e.gen_H1_b2_recofatjet_eta, e.gen_H1_b1_recofatjet_phi, e.gen_H1_b2_recofatjet_phi)
            bH2_recofatjet = bH2_genfatjet and bH2_b1_recofatjet and bH2_b2_recofatjet and areSameJets(e.gen_H2_b1_recofatjet_eta, e.gen_H2_b2_recofatjet_eta, e.gen_H2_b1_recofatjet_phi, e.gen_H2_b2_recofatjet_phi)
            
            bH1_recofatjet_only = bH1_genfatjet_only and bH1_recofatjet and not bH2_recofatjet
            bH2_recofatjet_only = bH2_genfatjet_only and bH2_recofatjet and not bH1_recofatjet
            
            bH1Boosted_H2resolved_reco = bH1_recofatjet_only and bH2_b1_recojet and bH2_b2_recojet
            bH2Boosted_H1resolved_reco = bH2_recofatjet_only and bH1_b1_recojet and bH1_b2_recojet
            
            bIsResolvedReco     = bH1_b1_recojet and bH1_b2_recojet and bH2_b1_recojet and bH2_b2_recojet
            bIsSemiResolvedReco = bH1Boosted_H2resolved_reco or bH2Boosted_H1resolved_reco
            bIsBoostedReco      = bH1_recofatjet and bH2_recofatjet
            bIsResolvedRecoExcl = bIsResolvedReco and not (bIsBoostedReco or bIsSemiResolvedReco)
            
            if (bIsResolvedReco): cIsResolvedReco += 1
            if (bIsResolvedRecoExcl): cIsResolvedRecoExcl += 1
            if (bIsSemiResolvedReco): cIsSemiResolvedReco += 1
            if (bIsBoostedReco): cIsBoostedReco += 1
            #====================================================================================================================
            h_GenPart_H1_pt.Fill(e.gen_H1_pt)
            h_GenPart_H2_pt.Fill(e.gen_H2_pt)
            h_GenPart_H1_eta.Fill(e.gen_H1_eta)
            h_GenPart_H2_eta.Fill(e.gen_H2_eta)
            h_GenPart_H1_phi.Fill(e.gen_H1_phi)
            h_GenPart_H2_phi.Fill(e.gen_H2_phi)
            h_GenPart_H1_b1_pt.Fill(e.gen_H1_b1_pt)
            h_GenPart_H1_b2_pt.Fill(e.gen_H1_b2_pt)
            h_GenPart_H2_b1_pt.Fill(e.gen_H2_b1_pt)
            h_GenPart_H2_b2_pt.Fill(e.gen_H2_b2_pt)
            h_GenPart_H1_b1_eta.Fill(e.gen_H1_b1_eta)
            h_GenPart_H1_b2_eta.Fill(e.gen_H1_b2_eta)
            h_GenPart_H2_b1_eta.Fill(e.gen_H2_b1_eta)
            h_GenPart_H2_b2_eta.Fill(e.gen_H2_b2_eta)
            h_GenPart_H1_b1_phi.Fill(e.gen_H1_b1_phi)
            h_GenPart_H1_b2_phi.Fill(e.gen_H1_b2_phi)
            h_GenPart_H2_b1_phi.Fill(e.gen_H2_b1_phi)
            h_GenPart_H2_b2_phi.Fill(e.gen_H2_b2_phi)


            # Triggers
            bPassed_HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5 = e.HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5
            bPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np4 = e.HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np4
            bPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np2 = e.HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np2
            bPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p1  = e.HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p1
            bPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p17 = e.HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p17 
            bPassed_HLT_PFHT1050 = e.HLT_PFHT1050
            bPassed_HLT_PFJet500 = e.HLT_PFJet500
            bPassed_HLT_AK8PFHT800_TrimMass50 = e.HLT_AK8PFHT800_TrimMass50
            bPassed_HLT_AK8PFJet400_TrimMass30 = e.HLT_AK8PFJet400_TrimMass30
            bPassed_HLT_AK8PFJet420_TrimMass30 = e.HLT_AK8PFJet420_TrimMass30
            bPassed_HLT_AK8PFJet500 = e.HLT_AK8PFJet500
            bPassed_HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59 = e.HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59
            bPassed_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94 = e.HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94
            bPassed_HLT_AK8PFHT750_TrimMass50 = e.HLT_AK8PFHT750_TrimMass50
            bPassed_HLT_AK8PFJet360_TrimMass30 = e.HLT_AK8PFJet360_TrimMass30
            bPassed_HLT_AK8PFJet380_TrimMass30 = e.HLT_AK8PFJet380_TrimMass30
            
            bPassed_OR = bPassed_HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5 or bPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np4 or bPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np2 or bPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p1 or bPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p17 or bPassed_HLT_PFHT1050 or bPassed_HLT_PFJet500 or bPassed_HLT_AK8PFHT800_TrimMass50 or bPassed_HLT_AK8PFJet400_TrimMass30 or bPassed_HLT_AK8PFJet420_TrimMass30 or bPassed_HLT_AK8PFJet500 or bPassed_HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59 or bPassed_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94 or bPassed_HLT_AK8PFHT750_TrimMass50 or bPassed_HLT_AK8PFJet360_TrimMass30 or bPassed_HLT_AK8PFJet380_TrimMass30
            
            hPassed_HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5.Fill(bPassed_HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5)
            hPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np4.Fill(bPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np4)
            hPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np2.Fill(bPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np2)
            hPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p1.Fill(bPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p1)
            hPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p17.Fill(bPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p17)
            hPassed_HLT_PFHT1050.Fill(bPassed_HLT_PFHT1050)
            hPassed_HLT_PFJet500.Fill(bPassed_HLT_PFJet500)
            hPassed_HLT_AK8PFHT800_TrimMass50.Fill(bPassed_HLT_AK8PFHT800_TrimMass50)
            hPassed_HLT_AK8PFJet400_TrimMass30.Fill(bPassed_HLT_AK8PFJet400_TrimMass30)
            hPassed_HLT_AK8PFJet420_TrimMass30.Fill(bPassed_HLT_AK8PFJet420_TrimMass30)
            hPassed_HLT_AK8PFJet500.Fill(bPassed_HLT_AK8PFJet500)
            hPassed_HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59.Fill(bPassed_HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59)
            hPassed_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94.Fill(bPassed_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94)
            hPassed_HLT_AK8PFHT750_TrimMass50.Fill(bPassed_HLT_AK8PFHT750_TrimMass50)
            hPassed_HLT_AK8PFJet360_TrimMass30.Fill(bPassed_HLT_AK8PFJet360_TrimMass30)
            hPassed_HLT_AK8PFJet380_TrimMass30.Fill(bPassed_HLT_AK8PFJet380_TrimMass30)
            hPassed_OR.Fill(bPassed_OR)
            
            # Drop unmatched reco-events
            if not (bIsResolvedReco or bIsSemiResolvedReco or bIsBoostedReco):
                cNotMatchedReco += 1
                continue
                
            if (bIsBoostedReco):
                hBoostedPassed_HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5.Fill(bPassed_HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5)
                hBoostedPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np4.Fill(bPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np4)
                hBoostedPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np2.Fill(bPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np2)
                hBoostedPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p1.Fill(bPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p1)
                hBoostedPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p17.Fill(bPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p17)
                hBoostedPassed_HLT_PFHT1050.Fill(bPassed_HLT_PFHT1050)
                hBoostedPassed_HLT_PFJet500.Fill(bPassed_HLT_PFJet500)
                hBoostedPassed_HLT_AK8PFHT800_TrimMass50.Fill(bPassed_HLT_AK8PFHT800_TrimMass50)
                hBoostedPassed_HLT_AK8PFJet400_TrimMass30.Fill(bPassed_HLT_AK8PFJet400_TrimMass30)
                hBoostedPassed_HLT_AK8PFJet420_TrimMass30.Fill(bPassed_HLT_AK8PFJet420_TrimMass30)
                hBoostedPassed_HLT_AK8PFJet500.Fill(bPassed_HLT_AK8PFJet500)
                hBoostedPassed_HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59.Fill(bPassed_HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59)
                hBoostedPassed_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94.Fill(bPassed_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94)
                hBoostedPassed_HLT_AK8PFHT750_TrimMass50.Fill(bPassed_HLT_AK8PFHT750_TrimMass50)
                hBoostedPassed_HLT_AK8PFJet360_TrimMass30.Fill(bPassed_HLT_AK8PFJet360_TrimMass30)
                hBoostedPassed_HLT_AK8PFJet380_TrimMass30.Fill(bPassed_HLT_AK8PFJet380_TrimMass30)
                hBoostedPassed_OR.Fill(bPassed_OR)

            if (bIsResolvedRecoExcl):
                hResolvedExclPassed_HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5.Fill(bPassed_HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5)
                hResolvedExclPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np4.Fill(bPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np4)
                hResolvedExclPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np2.Fill(bPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np2)
                hResolvedExclPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p1.Fill(bPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p1)
                hResolvedExclPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p17.Fill(bPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p17)
                hResolvedExclPassed_HLT_PFHT1050.Fill(bPassed_HLT_PFHT1050)
                hResolvedExclPassed_HLT_PFJet500.Fill(bPassed_HLT_PFJet500)
                hResolvedExclPassed_HLT_AK8PFHT800_TrimMass50.Fill(bPassed_HLT_AK8PFHT800_TrimMass50)
                hResolvedExclPassed_HLT_AK8PFJet400_TrimMass30.Fill(bPassed_HLT_AK8PFJet400_TrimMass30)
                hResolvedExclPassed_HLT_AK8PFJet420_TrimMass30.Fill(bPassed_HLT_AK8PFJet420_TrimMass30)
                hResolvedExclPassed_HLT_AK8PFJet500.Fill(bPassed_HLT_AK8PFJet500)
                hResolvedExclPassed_HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59.Fill(bPassed_HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59)
                hResolvedExclPassed_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94.Fill(bPassed_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94)
                hResolvedExclPassed_HLT_AK8PFHT750_TrimMass50.Fill(bPassed_HLT_AK8PFHT750_TrimMass50)
                hResolvedExclPassed_HLT_AK8PFJet360_TrimMass30.Fill(bPassed_HLT_AK8PFJet360_TrimMass30)
                hResolvedExclPassed_HLT_AK8PFJet380_TrimMass30.Fill(bPassed_HLT_AK8PFJet380_TrimMass30)
                hResolvedExclPassed_OR.Fill(bPassed_OR)

            if (bIsResolvedReco):
                hResolvedPassed_HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5.Fill(bPassed_HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5)
                hResolvedPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np4.Fill(bPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np4)
                hResolvedPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np2.Fill(bPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np2)
                hResolvedPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p1.Fill(bPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p1)
                hResolvedPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p17.Fill(bPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p17)
                hResolvedPassed_HLT_PFHT1050.Fill(bPassed_HLT_PFHT1050)
                hResolvedPassed_HLT_PFJet500.Fill(bPassed_HLT_PFJet500)
                hResolvedPassed_HLT_AK8PFHT800_TrimMass50.Fill(bPassed_HLT_AK8PFHT800_TrimMass50)
                hResolvedPassed_HLT_AK8PFJet400_TrimMass30.Fill(bPassed_HLT_AK8PFJet400_TrimMass30)
                hResolvedPassed_HLT_AK8PFJet420_TrimMass30.Fill(bPassed_HLT_AK8PFJet420_TrimMass30)
                hResolvedPassed_HLT_AK8PFJet500.Fill(bPassed_HLT_AK8PFJet500)
                hResolvedPassed_HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59.Fill(bPassed_HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59)
                hResolvedPassed_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94.Fill(bPassed_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94)
                hResolvedPassed_HLT_AK8PFHT750_TrimMass50.Fill(bPassed_HLT_AK8PFHT750_TrimMass50)
                hResolvedPassed_HLT_AK8PFJet360_TrimMass30.Fill(bPassed_HLT_AK8PFJet360_TrimMass30)
                hResolvedPassed_HLT_AK8PFJet380_TrimMass30.Fill(bPassed_HLT_AK8PFJet380_TrimMass30)
                hResolvedPassed_OR.Fill(bPassed_OR)
                

            if (bIsSemiResolvedReco):
                hSemiresolvedPassed_HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5.Fill(bPassed_HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5)
                hSemiresolvedPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np4.Fill(bPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np4)
                hSemiresolvedPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np2.Fill(bPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np2)
                hSemiresolvedPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p1.Fill(bPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p1)
                hSemiresolvedPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p17.Fill(bPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p17)
                hSemiresolvedPassed_HLT_PFHT1050.Fill(bPassed_HLT_PFHT1050)
                hSemiresolvedPassed_HLT_PFJet500.Fill(bPassed_HLT_PFJet500)
                hSemiresolvedPassed_HLT_AK8PFHT800_TrimMass50.Fill(bPassed_HLT_AK8PFHT800_TrimMass50)
                hSemiresolvedPassed_HLT_AK8PFJet400_TrimMass30.Fill(bPassed_HLT_AK8PFJet400_TrimMass30)
                hSemiresolvedPassed_HLT_AK8PFJet420_TrimMass30.Fill(bPassed_HLT_AK8PFJet420_TrimMass30)
                hSemiresolvedPassed_HLT_AK8PFJet500.Fill(bPassed_HLT_AK8PFJet500)
                hSemiresolvedPassed_HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59.Fill(bPassed_HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59)
                hSemiresolvedPassed_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94.Fill(bPassed_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94)
                hSemiresolvedPassed_HLT_AK8PFHT750_TrimMass50.Fill(bPassed_HLT_AK8PFHT750_TrimMass50)
                hSemiresolvedPassed_HLT_AK8PFJet360_TrimMass30.Fill(bPassed_HLT_AK8PFJet360_TrimMass30)
                hSemiresolvedPassed_HLT_AK8PFJet380_TrimMass30.Fill(bPassed_HLT_AK8PFJet380_TrimMass30)
                hSemiresolvedPassed_OR.Fill(bPassed_OR)
                hSemiresolved_GenPart_H1_pt.Fill(e.gen_H1_pt)
                hSemiresolved_GenPart_H2_pt.Fill(e.gen_H2_pt)
                hSemiresolved_GenPart_H1_b1_pt.Fill(e.gen_H1_b1_pt)
                hSemiresolved_GenPart_H1_b2_pt.Fill(e.gen_H1_b2_pt)
                hSemiresolved_GenPart_H2_b1_pt.Fill(e.gen_H2_b1_pt)
                hSemiresolved_GenPart_H2_b2_pt.Fill(e.gen_H2_b2_pt)
                hSemiresolved_GenPart_H1_b1_eta.Fill(e.gen_H1_b1_eta)
                hSemiresolved_GenPart_H1_b2_eta.Fill(e.gen_H1_b2_eta)
                hSemiresolved_GenPart_H2_b1_eta.Fill(e.gen_H2_b1_eta)
                hSemiresolved_GenPart_H2_b2_eta.Fill(e.gen_H2_b2_eta)
                hSemiresolved_GenPart_H1_b1_phi.Fill(e.gen_H1_b1_phi)
                hSemiresolved_GenPart_H1_b2_phi.Fill(e.gen_H1_b2_phi)
                hSemiresolved_GenPart_H2_b1_phi.Fill(e.gen_H2_b1_phi)
                hSemiresolved_GenPart_H2_b2_phi.Fill(e.gen_H2_b2_phi)
                if (bH1Boosted_H2resolved_reco):
                    hSemiresolved_H1Boosted_H2resolved_GenFatJet_H1_pt.Fill(e.gen_H1_b1_genfatjet_pt)
                    hSemiresolved_H1Boosted_H2resolved_GenFatJet_H1_eta.Fill(e.gen_H1_b1_genfatjet_eta)
                    hSemiresolved_H1Boosted_H2resolved_GenFatJet_H1_phi.Fill(e.gen_H1_b1_genfatjet_phi)
                    hSemiresolved_H1Boosted_H2resolved_GenJet_H2_b1_pt.Fill(e.gen_H2_b1_genjet_pt)
                    hSemiresolved_H1Boosted_H2resolved_GenJet_H2_b2_pt.Fill(e.gen_H2_b2_genjet_pt)
                    hSemiresolved_H1Boosted_H2resolved_GenJet_H2_b1_eta.Fill(e.gen_H2_b1_genjet_eta)
                    hSemiresolved_H1Boosted_H2resolved_GenJet_H2_b2_eta.Fill(e.gen_H2_b2_genjet_eta)
                    hSemiresolved_H1Boosted_H2resolved_GenJet_H2_b1_phi.Fill(e.gen_H2_b1_genjet_phi)
                    hSemiresolved_H1Boosted_H2resolved_GenJet_H2_b2_phi.Fill(e.gen_H2_b2_genjet_phi)
                    hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_pt.Fill(e.gen_H1_b1_recofatjet_pt)
                    hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_eta.Fill(e.gen_H1_b1_recofatjet_eta)
                    hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_phi.Fill(e.gen_H1_b1_recofatjet_phi)
                    hSemiresolved_H1Boosted_H2resolved_RecoJet_H2_b1_pt.Fill(e.gen_H2_b1_recojet_pt)
                    hSemiresolved_H1Boosted_H2resolved_RecoJet_H2_b2_pt.Fill(e.gen_H2_b2_recojet_pt)
                    hSemiresolved_H1Boosted_H2resolved_RecoJet_H2_b1_eta.Fill(e.gen_H2_b1_recojet_eta)
                    hSemiresolved_H1Boosted_H2resolved_RecoJet_H2_b2_eta.Fill(e.gen_H2_b2_recojet_eta)
                    hSemiresolved_H1Boosted_H2resolved_RecoJet_H2_b1_phi.Fill(e.gen_H2_b1_recojet_phi)
                    hSemiresolved_H1Boosted_H2resolved_RecoJet_H2_b2_phi.Fill(e.gen_H2_b2_recojet_phi)
                    hSemiresolved_H1Boosted_H2resolved_NJets.Fill(e.n_jet)
                    hSemiresolved_H1Boosted_H2resolved_NFatJets.Fill(e.n_fatjet)
                    
                    # RecoJets matched
                    reco_H2_b1_p4 = getP4(e.gen_H2_b1_recojet_pt, e.gen_H2_b1_recojet_eta, e.gen_H2_b1_recojet_phi, e.gen_H2_b1_recojet_m)
                    reco_H2_b2_p4 = getP4(e.gen_H2_b2_recojet_pt, e.gen_H2_b2_recojet_eta, e.gen_H2_b2_recojet_phi, e.gen_H2_b2_recojet_m)
                    reco_H2 = reco_H2_b1_p4 + reco_H2_b2_p4
                    
                    hSemiresolved_H1Boosted_H2resolved_H2_pt.Fill(reco_H2.Pt())
                    hSemiresolved_H1Boosted_H2resolved_H2_eta.Fill(reco_H2.Eta())
                    hSemiresolved_H1Boosted_H2resolved_H2_phi.Fill(reco_H2.Phi())
                    hSemiresolved_H1Boosted_H2resolved_InvMass_H2.Fill(reco_H2.M())
                    hSemiresolved_H1Boosted_H2resolved_DeltaR_H1_H2.Fill(deltaR(e.gen_H1_b1_recofatjet_eta, reco_H2.Eta(), e.gen_H1_b1_recofatjet_phi, reco_H2.Phi()))
                    hSemiresolved_H1Boosted_H2resolved_DeltaEta_H1_H2.Fill(abs(e.gen_H1_b1_recofatjet_eta - reco_H2.Eta()))
                    hSemiresolved_H1Boosted_H2resolved_DeltaPhi_H1_H2.Fill(deltaPhi(e.gen_H1_b1_recofatjet_phi, reco_H2.Phi()))
                    
                    bFound_reco_H2_b1 = False
                    bFound_reco_H2_b2 = False
                    reco_H2_b1_p4Regressed = None
                    reco_H2_b2_p4Regressed = None
                    
                    reco_PFHT = 0.0

                    nLoose = 0
                    nMedium = 0
                    nTight = 0
                    
                    for ij in range(0, e.n_jet):
                        eta = e.jet_eta.at(ij)
                        phi = e.jet_phi.at(ij)
                        pt  = e.jet_pt.at(ij)
                        btag = e.jet_btag.at(ij)
                        
                        isLoose = btag > 0.0490
                        isMedium = btag > 0.2783
                        isTight = btag > 0.7100
                        
                        if (isLoose): nLoose += 1
                        if (isMedium): nMedium += 1
                        if (isTight): nTight += 1
                        
                        if (pt > 30.0 and abs(eta) < 2.4):
                            reco_PFHT += pt

                        if (areSameJets(eta, e.gen_H2_b1_recojet_eta, phi, e.gen_H2_b1_recojet_phi)):
                            bFound_reco_H2_b1 = True
                            reco_H2_b1_p4Regressed = getP4(e.jet_ptRegressed.at(ij), e.jet_eta.at(ij), e.jet_phi.at(ij), e.jet_mRegressed.at(ij))
                        elif (areSameJets(eta, e.gen_H2_b2_recojet_eta, phi, e.gen_H2_b2_recojet_phi)):
                            bFound_reco_H2_b2 = True
                            reco_H2_b2_p4Regressed = getP4(e.jet_ptRegressed.at(ij), e.jet_eta.at(ij), e.jet_phi.at(ij), e.jet_mRegressed.at(ij))

                    hSemiresolved_H1Boosted_H2resolved_PFHT.Fill(reco_PFHT)
                    hSemiresolved_H1Boosted_H2resolved_NLooseBJets.Fill(nLoose)
                    hSemiresolved_H1Boosted_H2resolved_NMediumBJets.Fill(nMedium)
                    hSemiresolved_H1Boosted_H2resolved_NTightBJets.Fill(nTight)
                    if (e.n_jet > 0): hSemiresolved_H1Boosted_H2resolved_Jet1Pt.Fill(e.jet_pt.at(0))
                    if (e.n_jet > 1): hSemiresolved_H1Boosted_H2resolved_Jet2Pt.Fill(e.jet_pt.at(1))
                    if (e.n_jet > 2): hSemiresolved_H1Boosted_H2resolved_Jet3Pt.Fill(e.jet_pt.at(2))
                    if (e.n_jet > 3): hSemiresolved_H1Boosted_H2resolved_Jet4Pt.Fill(e.jet_pt.at(3))
                    if (e.n_jet > 0): hSemiresolved_H1Boosted_H2resolved_Jet1Eta.Fill(e.jet_eta.at(0))
                    if (e.n_jet > 1): hSemiresolved_H1Boosted_H2resolved_Jet2Eta.Fill(e.jet_eta.at(1))
                    if (e.n_jet > 2): hSemiresolved_H1Boosted_H2resolved_Jet3Eta.Fill(e.jet_eta.at(2))
                    if (e.n_jet > 3): hSemiresolved_H1Boosted_H2resolved_Jet4Eta.Fill(e.jet_eta.at(3))
                    if (e.n_fatjet > 0):
                        hSemiresolved_H1Boosted_H2resolved_AK8Jet1Pt.Fill(e.fatjet_pt.at(0))

                    if bFound_reco_H2_b1 and bFound_reco_H2_b2:
                        reco_H2_p4Regressed = reco_H2_b1_p4Regressed + reco_H2_b2_p4Regressed
                        hSemiresolved_H1Boosted_H2resolved_InvMassRegressed_H2.Fill(reco_H2_p4Regressed.M())
                                                
                    for ij in range(0, e.n_fatjet):
                        eta = e.fatjet_eta.at(ij)
                        phi = e.fatjet_phi.at(ij)
                        mass = e.fatjet_m.at(ij)
                        PXbb = e.fatjet_PNetXbb.at(ij)
                        PXcc = e.fatjet_PNetXcc.at(ij)
                        PXqq = e.fatjet_PNetXqq.at(ij)
                        
                        TXbb = PXbb/(1-PXcc-PXqq)
                        
                        if (areSameJets(eta, e.gen_H1_b1_recofatjet_eta, phi, e.gen_H1_b1_recofatjet_phi)):
                            hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_m.Fill(mass)
                            hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_TXbb.Fill(TXbb)
                            hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_mSD_Uncorrected.Fill(e.fatjet_mSD_UnCorrected.at(ij))
                            hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_area.Fill(e.fatjet_area.at(ij))
                            hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_n2b1.Fill(e.fatjet_n2b1.at(ij))
                            hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_n3b1.Fill(e.fatjet_n3b1.at(ij))
                            hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_tau21.Fill(e.fatjet_tau2.at(ij)/e.fatjet_tau1.at(ij))
                            hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_tau32.Fill(e.fatjet_tau3.at(ij)/e.fatjet_tau2.at(ij))
                            hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_nsubjets.Fill(e.fatjet_nsubjets.at(ij))
                            if (e.fatjet_nsubjets.at(ij) > 0):
                                hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_pt.Fill(e.fatjet_subjet1_pt.at(ij))
                                hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_eta.Fill(e.fatjet_subjet1_eta.at(ij))
                                hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_phi.Fill(e.fatjet_subjet1_phi.at(ij))
                                hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_m.Fill(e.fatjet_subjet1_m.at(ij))
                                hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_btag.Fill(e.fatjet_subjet1_btagDeepB.at(ij))
                            if (e.fatjet_nsubjets.at(ij) > 1):
                                hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_pt.Fill(e.fatjet_subjet2_pt.at(ij))
                                hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_eta.Fill(e.fatjet_subjet2_eta.at(ij))
                                hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_phi.Fill(e.fatjet_subjet2_phi.at(ij))
                                hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_m.Fill(e.fatjet_subjet2_m.at(ij))
                                hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_btag.Fill(e.fatjet_subjet2_btagDeepB.at(ij))
                                
                if (bH2Boosted_H1resolved_reco):
                    hSemiresolved_H2Boosted_H1resolved_GenFatJet_H2_pt.Fill(e.gen_H2_b1_genfatjet_pt)
                    hSemiresolved_H2Boosted_H1resolved_GenFatJet_H2_eta.Fill(e.gen_H2_b1_genfatjet_eta)
                    hSemiresolved_H2Boosted_H1resolved_GenFatJet_H2_phi.Fill(e.gen_H2_b1_genfatjet_phi)
                    hSemiresolved_H2Boosted_H1resolved_GenJet_H1_b1_pt.Fill(e.gen_H1_b1_genjet_pt)
                    hSemiresolved_H2Boosted_H1resolved_GenJet_H1_b2_pt.Fill(e.gen_H1_b2_genjet_pt)
                    hSemiresolved_H2Boosted_H1resolved_GenJet_H1_b1_eta.Fill(e.gen_H1_b1_genjet_eta)
                    hSemiresolved_H2Boosted_H1resolved_GenJet_H1_b2_eta.Fill(e.gen_H1_b2_genjet_eta)
                    hSemiresolved_H2Boosted_H1resolved_GenJet_H1_b1_phi.Fill(e.gen_H1_b1_genjet_phi)
                    hSemiresolved_H2Boosted_H1resolved_GenJet_H1_b2_phi.Fill(e.gen_H1_b2_genjet_phi)
                    hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_pt.Fill(e.gen_H2_b1_recofatjet_pt)
                    hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_eta.Fill(e.gen_H2_b1_recofatjet_eta)
                    hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_phi.Fill(e.gen_H2_b1_recofatjet_phi)
                    hSemiresolved_H2Boosted_H1resolved_RecoJet_H1_b1_pt.Fill(e.gen_H1_b1_recojet_pt)
                    hSemiresolved_H2Boosted_H1resolved_RecoJet_H1_b2_pt.Fill(e.gen_H1_b2_recojet_pt)
                    hSemiresolved_H2Boosted_H1resolved_RecoJet_H1_b1_eta.Fill(e.gen_H1_b1_recojet_eta)
                    hSemiresolved_H2Boosted_H1resolved_RecoJet_H1_b2_eta.Fill(e.gen_H1_b2_recojet_eta)
                    hSemiresolved_H2Boosted_H1resolved_RecoJet_H1_b1_phi.Fill(e.gen_H1_b1_recojet_phi)
                    hSemiresolved_H2Boosted_H1resolved_RecoJet_H1_b2_phi.Fill(e.gen_H1_b2_recojet_phi)
                    hSemiresolved_H2Boosted_H1resolved_NJets.Fill(e.n_jet)
                    hSemiresolved_H2Boosted_H1resolved_NFatJets.Fill(e.n_fatjet)
                    
                    # RecoJets matched
                    reco_H1_b1_p4 = getP4(e.gen_H1_b1_recojet_pt, e.gen_H1_b1_recojet_eta, e.gen_H1_b1_recojet_phi, e.gen_H1_b1_recojet_m)
                    reco_H1_b2_p4 = getP4(e.gen_H1_b2_recojet_pt, e.gen_H1_b2_recojet_eta, e.gen_H1_b2_recojet_phi, e.gen_H1_b2_recojet_m)
                    reco_H1 = reco_H1_b1_p4 + reco_H1_b2_p4
                    hSemiresolved_H2Boosted_H1resolved_DeltaR_H1_H2.Fill(deltaR(e.gen_H2_b1_recofatjet_eta, reco_H1.Eta(), e.gen_H2_b1_recofatjet_phi, reco_H1.Phi()))
                    hSemiresolved_H2Boosted_H1resolved_DeltaEta_H1_H2.Fill(abs(e.gen_H2_b1_recofatjet_eta - reco_H1.Eta()))
                    hSemiresolved_H2Boosted_H1resolved_DeltaPhi_H1_H2.Fill(deltaPhi(e.gen_H2_b1_recofatjet_phi, reco_H1.Phi()))
                    hSemiresolved_H2Boosted_H1resolved_InvMass_H1.Fill(reco_H1.M())
                    hSemiresolved_H2Boosted_H1resolved_H1_pt.Fill(reco_H1.Pt())
                    hSemiresolved_H2Boosted_H1resolved_H1_eta.Fill(reco_H1.Eta())
                    hSemiresolved_H2Boosted_H1resolved_H1_phi.Fill(reco_H1.Phi())
                    hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_m.Fill(e.gen_H2_b1_recofatjet_m)
                    
                    bFound_reco_H1_b1 = False
                    bFound_reco_H1_b2 = False
                    reco_H1_b1_p4Regressed = None
                    reco_H1_b2_p4Regressed = None
                    for ij in range(0, e.n_jet):
                        eta = e.jet_eta.at(ij)
                        phi = e.jet_phi.at(ij)
                        if (areSameJets(eta, e.gen_H1_b1_recojet_eta, phi, e.gen_H1_b1_recojet_phi)):
                            bFound_reco_H1_b1 = True
                            reco_H1_b1_p4Regressed = getP4(e.jet_ptRegressed.at(ij), e.jet_eta.at(ij), e.jet_phi.at(ij), e.jet_mRegressed.at(ij))
                        elif (areSameJets(eta, e.gen_H1_b2_recojet_eta, phi, e.gen_H1_b2_recojet_phi)):
                            bFound_reco_H1_b2 = True
                            reco_H1_b2_p4Regressed = getP4(e.jet_ptRegressed.at(ij), e.jet_eta.at(ij), e.jet_phi.at(ij), e.jet_mRegressed.at(ij))


                    if bFound_reco_H1_b1 and bFound_reco_H1_b2:        
                        reco_H1_p4Regressed = reco_H1_b1_p4Regressed + reco_H1_b2_p4Regressed
                        hSemiresolved_H2Boosted_H1resolved_InvMassRegressed_H1.Fill(reco_H1_p4Regressed.M())
                    
                    for ij in range(0, e.n_fatjet):
                        eta = e.fatjet_eta.at(ij)
                        phi = e.fatjet_phi.at(ij)
                        
                        PXbb = e.fatjet_PNetXbb.at(ij)
                        PXcc = e.fatjet_PNetXcc.at(ij)
                        PXqq = e.fatjet_PNetXqq.at(ij)
                        
                        TXbb = PXbb/(1-PXcc-PXqq)
                        if (areSameJets(eta, e.gen_H2_b1_recofatjet_eta, phi, e.gen_H2_b1_recofatjet_phi)):
                            hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_TXbb.Fill(TXbb)
                            hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_mSD_Uncorrected.Fill(e.fatjet_mSD_UnCorrected.at(ij))
                            hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_area.Fill(e.fatjet_area.at(ij))
                            hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_n2b1.Fill(e.fatjet_n2b1.at(ij))
                            hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_n3b1.Fill(e.fatjet_n3b1.at(ij))
                            hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_tau21.Fill(e.fatjet_tau2.at(ij)/e.fatjet_tau1.at(ij))
                            hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_tau32.Fill(e.fatjet_tau3.at(ij)/e.fatjet_tau2.at(ij))
                            hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_nsubjets.Fill(e.fatjet_nsubjets.at(ij))
                            if (e.fatjet_nsubjets.at(ij) > 0):
                                hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_pt.Fill(e.fatjet_subjet1_pt.at(ij))
                                hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_eta.Fill(e.fatjet_subjet1_eta.at(ij))
                                hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_phi.Fill(e.fatjet_subjet1_phi.at(ij))
                                hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_m.Fill(e.fatjet_subjet1_m.at(ij))
                                hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_btag.Fill(e.fatjet_subjet1_btagDeepB.at(ij))
                            if (e.fatjet_nsubjets.at(ij) > 1):
                                hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_pt.Fill(e.fatjet_subjet2_pt.at(ij))
                                hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_eta.Fill(e.fatjet_subjet2_eta.at(ij))
                                hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_phi.Fill(e.fatjet_subjet2_phi.at(ij))
                                hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_m.Fill(e.fatjet_subjet2_m.at(ij))
                                hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_btag.Fill(e.fatjet_subjet2_btagDeepB.at(ij))
                    
            if (bIsBoostedReco):
                hBoosted_GenPart_H1_pt.Fill(e.gen_H1_pt)
                hBoosted_GenPart_H2_pt.Fill(e.gen_H2_pt)
                hBoosted_GenPart_H1_b1_pt.Fill(e.gen_H1_b1_pt)
                hBoosted_GenPart_H1_b2_pt.Fill(e.gen_H1_b2_pt)
                hBoosted_GenPart_H2_b1_pt.Fill(e.gen_H2_b1_pt)
                hBoosted_GenPart_H2_b2_pt.Fill(e.gen_H2_b2_pt)
                hBoosted_GenPart_H1_b1_eta.Fill(e.gen_H1_b1_eta)
                hBoosted_GenPart_H1_b2_eta.Fill(e.gen_H1_b2_eta)
                hBoosted_GenPart_H2_b1_eta.Fill(e.gen_H2_b1_eta)
                hBoosted_GenPart_H2_b2_eta.Fill(e.gen_H2_b2_eta)
                hBoosted_GenPart_H1_b1_phi.Fill(e.gen_H1_b1_phi)
                hBoosted_GenPart_H1_b2_phi.Fill(e.gen_H1_b2_phi)
                hBoosted_GenPart_H2_b1_phi.Fill(e.gen_H2_b1_phi)
                hBoosted_GenPart_H2_b2_phi.Fill(e.gen_H2_b2_phi)
                hBoosted_GenFatJet_H1_pt.Fill(e.gen_H1_b1_genfatjet_pt)
                hBoosted_GenFatJet_H2_pt.Fill(e.gen_H2_b2_genfatjet_pt)
                hBoosted_GenFatJet_H1_eta.Fill(e.gen_H1_b1_genfatjet_eta)
                hBoosted_GenFatJet_H2_eta.Fill(e.gen_H2_b2_genfatjet_eta)
                hBoosted_GenFatJet_H1_phi.Fill(e.gen_H1_b1_genfatjet_phi)
                hBoosted_GenFatJet_H2_phi.Fill(e.gen_H2_b2_genfatjet_phi)
                hBoosted_RecoFatJet_H1_pt.Fill(e.gen_H1_b1_recofatjet_pt)
                hBoosted_RecoFatJet_H2_pt.Fill(e.gen_H2_b1_recofatjet_pt)
                hBoosted_RecoFatJet_H1_eta.Fill(e.gen_H1_b1_recofatjet_eta)
                hBoosted_RecoFatJet_H2_eta.Fill(e.gen_H2_b2_recofatjet_eta)
                hBoosted_RecoFatJet_H1_phi.Fill(e.gen_H1_b1_recofatjet_phi)
                hBoosted_RecoFatJet_H2_phi.Fill(e.gen_H2_b2_recofatjet_phi)
                
                hBoosted_RecoFatJet_H1_m.Fill(e.gen_H1_b1_recofatjet_m)
                hBoosted_RecoFatJet_H2_m.Fill(e.gen_H2_b1_recofatjet_m)
                hBoosted_NJets.Fill(e.n_jet)
                hBoosted_NFatJets.Fill(e.n_fatjet)
                hBoosted_RecoFatJet_DeltaR_H1_H2.Fill(deltaR(e.gen_H1_b1_genfatjet_eta, e.gen_H2_b2_genfatjet_eta, e.gen_H1_b1_genfatjet_phi, e.gen_H2_b2_genfatjet_phi))
                hBoosted_RecoFatJet_DeltaEta_H1_H2.Fill(abs(e.gen_H1_b1_genfatjet_eta - e.gen_H2_b2_genfatjet_eta))
                hBoosted_RecoFatJet_DeltaPhi_H1_H2.Fill(deltaPhi(e.gen_H1_b1_genfatjet_phi, e.gen_H2_b2_genfatjet_phi))
                
                for ij in range(0, e.n_fatjet):
                    eta = e.fatjet_eta.at(ij)
                    phi = e.fatjet_phi.at(ij)
                    
                    PXbb = e.fatjet_PNetXbb.at(ij)
                    PXcc = e.fatjet_PNetXcc.at(ij)
                    PXqq = e.fatjet_PNetXqq.at(ij)
                    TXbb = PXbb/(1-PXcc-PXqq)
                    
                    if (areSameJets(eta, e.gen_H1_b1_recofatjet_eta, phi, e.gen_H1_b1_recofatjet_phi)):
                        # H1 reco fatjet
                        hBoosted_RecoFatJet_H1_TXbb.Fill(TXbb)
                        hBoosted_RecoFatJet_H1_mSD_Uncorrected.Fill(e.fatjet_mSD_UnCorrected.at(ij))
                        hBoosted_RecoFatJet_H1_area.Fill(e.fatjet_area.at(ij))
                        hBoosted_RecoFatJet_H1_n2b1.Fill(e.fatjet_n2b1.at(ij))
                        hBoosted_RecoFatJet_H1_n3b1.Fill(e.fatjet_n3b1.at(ij))
                        hBoosted_RecoFatJet_H1_tau21.Fill(e.fatjet_tau2.at(ij)/e.fatjet_tau1.at(ij))
                        hBoosted_RecoFatJet_H1_tau32.Fill(e.fatjet_tau3.at(ij)/e.fatjet_tau2.at(ij))
                        hBoosted_RecoFatJet_H1_nsubjets.Fill(e.fatjet_nsubjets.at(ij))
                        if (e.fatjet_nsubjets.at(ij) > 0):
                            hBoosted_RecoFatJet_H1_subjet1_pt.Fill(e.fatjet_subjet1_pt.at(ij))
                            hBoosted_RecoFatJet_H1_subjet1_eta.Fill(e.fatjet_subjet1_eta.at(ij))
                            hBoosted_RecoFatJet_H1_subjet1_phi.Fill(e.fatjet_subjet1_phi.at(ij))
                            hBoosted_RecoFatJet_H1_subjet1_m.Fill(e.fatjet_subjet1_m.at(ij))
                            hBoosted_RecoFatJet_H1_subjet1_btag.Fill(e.fatjet_subjet1_btagDeepB.at(ij))
                        if (e.fatjet_nsubjets.at(ij) > 1):
                            hBoosted_RecoFatJet_H1_subjet2_pt.Fill(e.fatjet_subjet2_pt.at(ij))
                            hBoosted_RecoFatJet_H1_subjet2_eta.Fill(e.fatjet_subjet2_eta.at(ij))
                            hBoosted_RecoFatJet_H1_subjet2_phi.Fill(e.fatjet_subjet2_phi.at(ij))
                            hBoosted_RecoFatJet_H1_subjet2_m.Fill(e.fatjet_subjet2_m.at(ij))
                            hBoosted_RecoFatJet_H1_subjet2_btag.Fill(e.fatjet_subjet2_btagDeepB.at(ij))
                if (areSameJets(eta, e.gen_H2_b1_recofatjet_eta, phi, e.gen_H2_b1_recofatjet_phi)):
                        # H2 reco fatjet
                        hBoosted_RecoFatJet_H2_TXbb.Fill(TXbb)
                        hBoosted_RecoFatJet_H2_mSD_Uncorrected.Fill(e.fatjet_mSD_UnCorrected.at(ij))
                        hBoosted_RecoFatJet_H2_area.Fill(e.fatjet_area.at(ij))
                        hBoosted_RecoFatJet_H2_n2b1.Fill(e.fatjet_n2b1.at(ij))
                        hBoosted_RecoFatJet_H2_n3b1.Fill(e.fatjet_n3b1.at(ij))
                        hBoosted_RecoFatJet_H2_tau21.Fill(e.fatjet_tau2.at(ij)/e.fatjet_tau1.at(ij))
                        hBoosted_RecoFatJet_H2_tau32.Fill(e.fatjet_tau3.at(ij)/e.fatjet_tau2.at(ij))
                        hBoosted_RecoFatJet_H2_nsubjets.Fill(e.fatjet_nsubjets.at(ij))
                        if (e.fatjet_nsubjets.at(ij) > 0):
                            hBoosted_RecoFatJet_H2_subjet1_pt.Fill(e.fatjet_subjet1_pt.at(ij))
                            hBoosted_RecoFatJet_H2_subjet1_eta.Fill(e.fatjet_subjet1_eta.at(ij))
                            hBoosted_RecoFatJet_H2_subjet1_phi.Fill(e.fatjet_subjet1_phi.at(ij))
                            hBoosted_RecoFatJet_H2_subjet1_m.Fill(e.fatjet_subjet1_m.at(ij))
                            hBoosted_RecoFatJet_H2_subjet1_btag.Fill(e.fatjet_subjet1_btagDeepB.at(ij))
                        if (e.fatjet_nsubjets.at(ij) > 1):
                            hBoosted_RecoFatJet_H2_subjet2_pt.Fill(e.fatjet_subjet2_pt.at(ij))
                            hBoosted_RecoFatJet_H2_subjet2_eta.Fill(e.fatjet_subjet2_eta.at(ij))
                            hBoosted_RecoFatJet_H2_subjet2_phi.Fill(e.fatjet_subjet2_phi.at(ij))
                            hBoosted_RecoFatJet_H2_subjet2_m.Fill(e.fatjet_subjet2_m.at(ij))
                            hBoosted_RecoFatJet_H2_subjet2_btag.Fill(e.fatjet_subjet2_btagDeepB.at(ij))
                


            
            if (bIsResolvedRecoExcl):
                # GenParticles
                hResolvedExcl_GenPart_H1_pt.Fill(e.gen_H1_pt)
                hResolvedExcl_GenPart_H2_pt.Fill(e.gen_H2_pt)
                hResolvedExcl_GenPart_H1_b1_pt.Fill(e.gen_H1_b1_pt)
                hResolvedExcl_GenPart_H1_b2_pt.Fill(e.gen_H1_b2_pt)
                hResolvedExcl_GenPart_H2_b1_pt.Fill(e.gen_H2_b1_pt)
                hResolvedExcl_GenPart_H2_b2_pt.Fill(e.gen_H2_b2_pt)
                hResolvedExcl_GenPart_H1_b1_eta.Fill(e.gen_H1_b1_eta)
                hResolvedExcl_GenPart_H1_b2_eta.Fill(e.gen_H1_b2_eta)
                hResolvedExcl_GenPart_H2_b1_eta.Fill(e.gen_H2_b1_eta)
                hResolvedExcl_GenPart_H2_b2_eta.Fill(e.gen_H2_b2_eta)
                hResolvedExcl_GenPart_H1_b1_phi.Fill(e.gen_H1_b1_phi)
                hResolvedExcl_GenPart_H1_b2_phi.Fill(e.gen_H1_b2_phi)
                hResolvedExcl_GenPart_H2_b1_phi.Fill(e.gen_H2_b1_phi)
                hResolvedExcl_GenPart_H2_b2_phi.Fill(e.gen_H2_b2_phi)
                # GenJets matched
                hResolvedExcl_GenJet_H1_b1_pt.Fill(e.gen_H1_b1_genjet_pt)
                hResolvedExcl_GenJet_H1_b2_pt.Fill(e.gen_H1_b2_genjet_pt)
                hResolvedExcl_GenJet_H2_b1_pt.Fill(e.gen_H2_b1_genjet_pt)
                hResolvedExcl_GenJet_H2_b2_pt.Fill(e.gen_H2_b2_genjet_pt)
                hResolvedExcl_GenJet_H1_b1_eta.Fill(e.gen_H1_b1_genjet_eta)
                hResolvedExcl_GenJet_H1_b2_eta.Fill(e.gen_H1_b2_genjet_eta)
                hResolvedExcl_GenJet_H2_b1_eta.Fill(e.gen_H2_b1_genjet_eta)
                hResolvedExcl_GenJet_H2_b2_eta.Fill(e.gen_H2_b2_genjet_eta)
                hResolvedExcl_GenJet_H1_b1_phi.Fill(e.gen_H1_b1_genjet_phi)
                hResolvedExcl_GenJet_H1_b2_phi.Fill(e.gen_H1_b2_genjet_phi)
                hResolvedExcl_GenJet_H2_b1_phi.Fill(e.gen_H2_b1_genjet_phi)
                hResolvedExcl_GenJet_H2_b2_phi.Fill(e.gen_H2_b2_genjet_phi)
                # RecoJets matched
                reco_H1_b1_p4 = getP4(e.gen_H1_b1_recojet_pt, e.gen_H1_b1_recojet_eta, e.gen_H1_b1_recojet_phi, e.gen_H1_b1_recojet_m)
                reco_H1_b2_p4 = getP4(e.gen_H1_b2_recojet_pt, e.gen_H1_b2_recojet_eta, e.gen_H1_b2_recojet_phi, e.gen_H1_b2_recojet_m)
                reco_H2_b1_p4 = getP4(e.gen_H2_b1_recojet_pt, e.gen_H2_b1_recojet_eta, e.gen_H2_b1_recojet_phi, e.gen_H2_b1_recojet_m)
                reco_H2_b2_p4 = getP4(e.gen_H2_b2_recojet_pt, e.gen_H2_b2_recojet_eta, e.gen_H2_b2_recojet_phi, e.gen_H2_b2_recojet_m)
                reco_H1 = reco_H1_b1_p4 + reco_H1_b2_p4
                reco_H2 = reco_H2_b1_p4 + reco_H2_b2_p4
                
                hResolvedExcl_RecoJet_H1_b1_pt.Fill(e.gen_H1_b1_recojet_pt)
                hResolvedExcl_RecoJet_H1_b2_pt.Fill(e.gen_H1_b2_recojet_pt)
                hResolvedExcl_RecoJet_H2_b1_pt.Fill(e.gen_H2_b1_recojet_pt)
                hResolvedExcl_RecoJet_H2_b2_pt.Fill(e.gen_H2_b2_recojet_pt)
                hResolvedExcl_RecoJet_H1_b1_eta.Fill(e.gen_H1_b1_recojet_eta)
                hResolvedExcl_RecoJet_H1_b2_eta.Fill(e.gen_H1_b2_recojet_eta)
                hResolvedExcl_RecoJet_H2_b1_eta.Fill(e.gen_H2_b1_recojet_eta)
                hResolvedExcl_RecoJet_H2_b2_eta.Fill(e.gen_H2_b2_recojet_eta)
                hResolvedExcl_RecoJet_H1_b1_phi.Fill(e.gen_H1_b1_recojet_phi)
                hResolvedExcl_RecoJet_H1_b2_phi.Fill(e.gen_H1_b2_recojet_phi)
                hResolvedExcl_RecoJet_H2_b1_phi.Fill(e.gen_H2_b1_recojet_phi)
                hResolvedExcl_RecoJet_H2_b2_phi.Fill(e.gen_H2_b2_recojet_phi)
                hResolvedExcl_RecoJet_DeltaR_H1b1_H1b2.Fill(deltaR(e.gen_H1_b1_recojet_eta, e.gen_H1_b2_recojet_eta, e.gen_H1_b1_recojet_phi, e.gen_H1_b2_recojet_phi))
                hResolvedExcl_RecoJet_DeltaR_H1b1_H2b1.Fill(deltaR(e.gen_H1_b1_recojet_eta, e.gen_H2_b1_recojet_eta, e.gen_H1_b1_recojet_phi, e.gen_H2_b1_recojet_phi))
                hResolvedExcl_RecoJet_DeltaR_H1b1_H2b2.Fill(deltaR(e.gen_H1_b1_recojet_eta, e.gen_H2_b2_recojet_eta, e.gen_H1_b1_recojet_phi, e.gen_H2_b2_recojet_phi))
                hResolvedExcl_RecoJet_DeltaR_H1b2_H2b1.Fill(deltaR(e.gen_H1_b2_recojet_eta, e.gen_H2_b1_recojet_eta, e.gen_H1_b2_recojet_phi, e.gen_H2_b1_recojet_phi))
                hResolvedExcl_RecoJet_DeltaR_H1b2_H2b2.Fill(deltaR(e.gen_H1_b2_recojet_eta, e.gen_H2_b2_recojet_eta, e.gen_H1_b2_recojet_phi, e.gen_H2_b2_recojet_phi))
                hResolvedExcl_RecoJet_DeltaR_H2b1_H2b2.Fill(deltaR(e.gen_H2_b1_recojet_eta, e.gen_H2_b2_recojet_eta, e.gen_H2_b1_recojet_phi, e.gen_H2_b2_recojet_phi))
                
                hResolvedExcl_RecoJet_DeltaEta_H1b1_H1b2.Fill(abs(e.gen_H1_b1_recojet_eta - e.gen_H1_b2_recojet_eta))
                hResolvedExcl_RecoJet_DeltaEta_H1b1_H2b1.Fill(abs(e.gen_H1_b1_recojet_eta - e.gen_H2_b1_recojet_eta))
                hResolvedExcl_RecoJet_DeltaEta_H1b1_H2b2.Fill(abs(e.gen_H1_b1_recojet_eta - e.gen_H2_b2_recojet_eta))
                hResolvedExcl_RecoJet_DeltaEta_H1b2_H2b1.Fill(abs(e.gen_H1_b2_recojet_eta - e.gen_H2_b1_recojet_eta))
                hResolvedExcl_RecoJet_DeltaEta_H1b2_H2b2.Fill(abs(e.gen_H1_b2_recojet_eta - e.gen_H2_b2_recojet_eta))
                hResolvedExcl_RecoJet_DeltaEta_H2b1_H2b2.Fill(abs(e.gen_H2_b1_recojet_eta - e.gen_H2_b2_recojet_eta))
                
                hResolvedExcl_RecoJet_DeltaPhi_H1b1_H1b2.Fill(deltaPhi(e.gen_H1_b1_recojet_phi, e.gen_H1_b2_recojet_phi))
                hResolvedExcl_RecoJet_DeltaPhi_H1b1_H2b1.Fill(deltaPhi(e.gen_H1_b1_recojet_phi, e.gen_H2_b1_recojet_phi))
                hResolvedExcl_RecoJet_DeltaPhi_H1b1_H2b2.Fill(deltaPhi(e.gen_H1_b1_recojet_phi, e.gen_H2_b2_recojet_phi))
                hResolvedExcl_RecoJet_DeltaPhi_H1b2_H2b1.Fill(deltaPhi(e.gen_H1_b2_recojet_phi, e.gen_H2_b1_recojet_phi))
                hResolvedExcl_RecoJet_DeltaPhi_H1b2_H2b2.Fill(deltaPhi(e.gen_H1_b2_recojet_phi, e.gen_H2_b2_recojet_phi))
                hResolvedExcl_RecoJet_DeltaPhi_H2b1_H2b2.Fill(deltaPhi(e.gen_H2_b1_recojet_phi, e.gen_H2_b2_recojet_phi))
                
                hResolvedExcl_RecoJet_H1_pt.Fill(reco_H1.Pt())
                hResolvedExcl_RecoJet_H2_pt.Fill(reco_H2.Pt())
                hResolvedExcl_RecoJet_H1_eta.Fill(reco_H1.Eta())
                hResolvedExcl_RecoJet_H2_eta.Fill(reco_H2.Eta())
                hResolvedExcl_RecoJet_H1_phi.Fill(reco_H1.Phi())
                hResolvedExcl_RecoJet_H2_phi.Fill(reco_H2.Phi())
                hResolvedExcl_RecoJet_InvMass_H1.Fill(reco_H1.M())
                hResolvedExcl_RecoJet_InvMass_H2.Fill(reco_H2.M())
                hResolvedExcl_RecoJet_DeltaR_H1_H2.Fill(deltaR(reco_H1.Eta(), reco_H2.Eta(), reco_H1.Phi(), reco_H2.Phi()))
                hResolvedExcl_RecoJet_DeltaEta_H1_H2.Fill(abs(reco_H1.Eta() - reco_H2.Eta()))
                hResolvedExcl_RecoJet_DeltaPhi_H1_H2.Fill(abs(deltaPhi(reco_H1.Phi(), reco_H2.Phi())))

                hResolvedExcl_RecoJet_NJets.Fill(e.n_jet)
                hResolvedExcl_RecoJet_NFatJets.Fill(e.n_fatjet)
                
                bFound_reco_H1_b1 = False
                bFound_reco_H1_b2 = False
                bFound_reco_H2_b1 = False
                bFound_reco_H2_b2 = False
                
                reco_H1_b1_btag = -1.0
                reco_H1_b1_p4Regressed  = None
                
                reco_H1_b2_btag        = -1.0 
                reco_H1_b2_p4Regressed = None
                
                reco_H2_b1_btag        = -1.0
                reco_H2_b1_p4Regressed = None
                
                reco_H2_b2_btag        = -1.0 
                reco_H2_b2_p4Regressed = None
                

                reco_PFHT = 0.0

                nLoose = 0
                nMedium = 0
                nTight = 0

                for ij in range(0, e.n_jet):
                    eta = e.jet_eta.at(ij)
                    phi = e.jet_phi.at(ij)
                    pt  = e.jet_pt.at(ij)
                    btag = e.jet_btag.at(ij)

                    isLoose = btag > 0.0490
                    isMedium = btag > 0.2783
                    isTight = btag > 0.7100

                    if (isLoose): nLoose += 1
                    if (isMedium): nMedium += 1
                    if (isTight): nTight += 1

                    if (pt > 30.0 and abs(eta) < 2.4):
                        reco_PFHT += pt

                    if (areSameJets(eta, e.gen_H1_b1_recojet_eta, phi, e.gen_H1_b1_recojet_phi)):
                        bFound_reco_H1_b1 = True
                        reco_H1_b1_btag        = e.jet_btag.at(ij)
                        reco_H1_b1_p4Regressed = getP4(e.jet_ptRegressed.at(ij), e.jet_eta.at(ij), e.jet_phi.at(ij), e.jet_mRegressed.at(ij))
                    elif (areSameJets(eta, e.gen_H1_b2_recojet_eta, phi, e.gen_H1_b2_recojet_phi)):
                        bFound_reco_H1_b2 = True
                        reco_H1_b2_btag        = e.jet_btag.at(ij)
                        reco_H1_b2_p4Regressed = getP4(e.jet_ptRegressed.at(ij), e.jet_eta.at(ij), e.jet_phi.at(ij), e.jet_mRegressed.at(ij))
                    elif (areSameJets(eta, e.gen_H2_b1_recojet_eta, phi, e.gen_H2_b1_recojet_phi)):
                        bFound_reco_H2_b1 = True
                        reco_H2_b1_btag        = e.jet_btag.at(ij)
                        reco_H2_b1_p4Regressed = getP4(e.jet_ptRegressed.at(ij), e.jet_eta.at(ij), e.jet_phi.at(ij), e.jet_mRegressed.at(ij))
                    elif (areSameJets(eta, e.gen_H2_b2_recojet_eta, phi, e.gen_H2_b2_recojet_phi)):
                        bFound_reco_H2_b2 = True
                        reco_H2_b2_btag        = e.jet_btag.at(ij)
                        reco_H2_b2_p4Regressed = getP4(e.jet_ptRegressed.at(ij), e.jet_eta.at(ij), e.jet_phi.at(ij), e.jet_mRegressed.at(ij))
        
                                    

                hResolvedExcl_RecoJet_PFHT.Fill(reco_PFHT)
                hResolvedExcl_RecoJet_NLooseBJets.Fill(nLoose)
                hResolvedExcl_RecoJet_NMediumBJets.Fill(nMedium)
                hResolvedExcl_RecoJet_NTightBJets.Fill(nTight)
                if (e.n_jet > 0): hResolvedExcl_RecoJet_Jet1Pt.Fill(e.jet_pt.at(0))
                if (e.n_jet > 1): hResolvedExcl_RecoJet_Jet2Pt.Fill(e.jet_pt.at(1))
                if (e.n_jet > 2): hResolvedExcl_RecoJet_Jet3Pt.Fill(e.jet_pt.at(2))
                if (e.n_jet > 3): hResolvedExcl_RecoJet_Jet4Pt.Fill(e.jet_pt.at(3))
                if (e.n_jet > 0): hResolvedExcl_RecoJet_Jet1Eta.Fill(e.jet_eta.at(0))
                if (e.n_jet > 1): hResolvedExcl_RecoJet_Jet2Eta.Fill(e.jet_eta.at(1))
                if (e.n_jet > 2): hResolvedExcl_RecoJet_Jet3Eta.Fill(e.jet_eta.at(2))
                if (e.n_jet > 3): hResolvedExcl_RecoJet_Jet4Eta.Fill(e.jet_eta.at(3))
                if (e.n_fatjet > 0):
                    hResolvedExcl_RecoJet_AK8Jet1Pt.Fill(e.fatjet_pt.at(0))

                reco_H1_p4Regressed = None
                reco_H2_p4Regressed = None
                if (bFound_reco_H1_b1 and bFound_reco_H1_b2):
                    reco_H1_p4Regressed = reco_H1_b1_p4Regressed + reco_H1_b2_p4Regressed
                    hResolvedExcl_RecoJet_InvMassRegressed_H1.Fill(reco_H1_p4Regressed.M())
                if (bFound_reco_H2_b1 and bFound_reco_H2_b2):
                    reco_H2_p4Regressed = reco_H2_b1_p4Regressed + reco_H2_b2_p4Regressed
                    hResolvedExcl_RecoJet_InvMassRegressed_H2.Fill(reco_H2_p4Regressed.M())
                    
                if (bFound_reco_H1_b1):
                    hResolvedExcl_RecoJet_H1_b1_btag.Fill(reco_H1_b1_btag)
                if (bFound_reco_H1_b2):
                    hResolvedExcl_RecoJet_H1_b2_btag.Fill(reco_H1_b2_btag)
                if (bFound_reco_H2_b1):
                    hResolvedExcl_RecoJet_H2_b1_btag.Fill(reco_H2_b1_btag)
                if (bFound_reco_H2_b2):
                    hResolvedExcl_RecoJet_H2_b2_btag.Fill(reco_H2_b2_btag)





            if (bIsResolvedReco):
                # GenParticles
                hResolved_GenPart_H1_pt.Fill(e.gen_H1_pt)
                hResolved_GenPart_H2_pt.Fill(e.gen_H2_pt)
                hResolved_GenPart_H1_b1_pt.Fill(e.gen_H1_b1_pt)
                hResolved_GenPart_H1_b2_pt.Fill(e.gen_H1_b2_pt)
                hResolved_GenPart_H2_b1_pt.Fill(e.gen_H2_b1_pt)
                hResolved_GenPart_H2_b2_pt.Fill(e.gen_H2_b2_pt)
                hResolved_GenPart_H1_b1_eta.Fill(e.gen_H1_b1_eta)
                hResolved_GenPart_H1_b2_eta.Fill(e.gen_H1_b2_eta)
                hResolved_GenPart_H2_b1_eta.Fill(e.gen_H2_b1_eta)
                hResolved_GenPart_H2_b2_eta.Fill(e.gen_H2_b2_eta)
                hResolved_GenPart_H1_b1_phi.Fill(e.gen_H1_b1_phi)
                hResolved_GenPart_H1_b2_phi.Fill(e.gen_H1_b2_phi)
                hResolved_GenPart_H2_b1_phi.Fill(e.gen_H2_b1_phi)
                hResolved_GenPart_H2_b2_phi.Fill(e.gen_H2_b2_phi)
                # GenJets matched
                hResolved_GenJet_H1_b1_pt.Fill(e.gen_H1_b1_genjet_pt)
                hResolved_GenJet_H1_b2_pt.Fill(e.gen_H1_b2_genjet_pt)
                hResolved_GenJet_H2_b1_pt.Fill(e.gen_H2_b1_genjet_pt)
                hResolved_GenJet_H2_b2_pt.Fill(e.gen_H2_b2_genjet_pt)
                hResolved_GenJet_H1_b1_eta.Fill(e.gen_H1_b1_genjet_eta)
                hResolved_GenJet_H1_b2_eta.Fill(e.gen_H1_b2_genjet_eta)
                hResolved_GenJet_H2_b1_eta.Fill(e.gen_H2_b1_genjet_eta)
                hResolved_GenJet_H2_b2_eta.Fill(e.gen_H2_b2_genjet_eta)
                hResolved_GenJet_H1_b1_phi.Fill(e.gen_H1_b1_genjet_phi)
                hResolved_GenJet_H1_b2_phi.Fill(e.gen_H1_b2_genjet_phi)
                hResolved_GenJet_H2_b1_phi.Fill(e.gen_H2_b1_genjet_phi)
                hResolved_GenJet_H2_b2_phi.Fill(e.gen_H2_b2_genjet_phi)
                # RecoJets matched
                reco_H1_b1_p4 = getP4(e.gen_H1_b1_recojet_pt, e.gen_H1_b1_recojet_eta, e.gen_H1_b1_recojet_phi, e.gen_H1_b1_recojet_m)
                reco_H1_b2_p4 = getP4(e.gen_H1_b2_recojet_pt, e.gen_H1_b2_recojet_eta, e.gen_H1_b2_recojet_phi, e.gen_H1_b2_recojet_m)
                reco_H2_b1_p4 = getP4(e.gen_H2_b1_recojet_pt, e.gen_H2_b1_recojet_eta, e.gen_H2_b1_recojet_phi, e.gen_H2_b1_recojet_m)
                reco_H2_b2_p4 = getP4(e.gen_H2_b2_recojet_pt, e.gen_H2_b2_recojet_eta, e.gen_H2_b2_recojet_phi, e.gen_H2_b2_recojet_m)
                reco_H1 = reco_H1_b1_p4 + reco_H1_b2_p4
                reco_H2 = reco_H2_b1_p4 + reco_H2_b2_p4
                
                hResolved_RecoJet_H1_b1_pt.Fill(e.gen_H1_b1_recojet_pt)
                hResolved_RecoJet_H1_b2_pt.Fill(e.gen_H1_b2_recojet_pt)
                hResolved_RecoJet_H2_b1_pt.Fill(e.gen_H2_b1_recojet_pt)
                hResolved_RecoJet_H2_b2_pt.Fill(e.gen_H2_b2_recojet_pt)
                hResolved_RecoJet_H1_b1_eta.Fill(e.gen_H1_b1_recojet_eta)
                hResolved_RecoJet_H1_b2_eta.Fill(e.gen_H1_b2_recojet_eta)
                hResolved_RecoJet_H2_b1_eta.Fill(e.gen_H2_b1_recojet_eta)
                hResolved_RecoJet_H2_b2_eta.Fill(e.gen_H2_b2_recojet_eta)
                hResolved_RecoJet_H1_b1_phi.Fill(e.gen_H1_b1_recojet_phi)
                hResolved_RecoJet_H1_b2_phi.Fill(e.gen_H1_b2_recojet_phi)
                hResolved_RecoJet_H2_b1_phi.Fill(e.gen_H2_b1_recojet_phi)
                hResolved_RecoJet_H2_b2_phi.Fill(e.gen_H2_b2_recojet_phi)
                hResolved_RecoJet_DeltaR_H1b1_H1b2.Fill(deltaR(e.gen_H1_b1_recojet_eta, e.gen_H1_b2_recojet_eta, e.gen_H1_b1_recojet_phi, e.gen_H1_b2_recojet_phi))
                hResolved_RecoJet_DeltaR_H1b1_H2b1.Fill(deltaR(e.gen_H1_b1_recojet_eta, e.gen_H2_b1_recojet_eta, e.gen_H1_b1_recojet_phi, e.gen_H2_b1_recojet_phi))
                hResolved_RecoJet_DeltaR_H1b1_H2b2.Fill(deltaR(e.gen_H1_b1_recojet_eta, e.gen_H2_b2_recojet_eta, e.gen_H1_b1_recojet_phi, e.gen_H2_b2_recojet_phi))
                hResolved_RecoJet_DeltaR_H1b2_H2b1.Fill(deltaR(e.gen_H1_b2_recojet_eta, e.gen_H2_b1_recojet_eta, e.gen_H1_b2_recojet_phi, e.gen_H2_b1_recojet_phi))
                hResolved_RecoJet_DeltaR_H1b2_H2b2.Fill(deltaR(e.gen_H1_b2_recojet_eta, e.gen_H2_b2_recojet_eta, e.gen_H1_b2_recojet_phi, e.gen_H2_b2_recojet_phi))
                hResolved_RecoJet_DeltaR_H2b1_H2b2.Fill(deltaR(e.gen_H2_b1_recojet_eta, e.gen_H2_b2_recojet_eta, e.gen_H2_b1_recojet_phi, e.gen_H2_b2_recojet_phi))
                
                hResolved_RecoJet_DeltaEta_H1b1_H1b2.Fill(abs(e.gen_H1_b1_recojet_eta - e.gen_H1_b2_recojet_eta))
                hResolved_RecoJet_DeltaEta_H1b1_H2b1.Fill(abs(e.gen_H1_b1_recojet_eta - e.gen_H2_b1_recojet_eta))
                hResolved_RecoJet_DeltaEta_H1b1_H2b2.Fill(abs(e.gen_H1_b1_recojet_eta - e.gen_H2_b2_recojet_eta))
                hResolved_RecoJet_DeltaEta_H1b2_H2b1.Fill(abs(e.gen_H1_b2_recojet_eta - e.gen_H2_b1_recojet_eta))
                hResolved_RecoJet_DeltaEta_H1b2_H2b2.Fill(abs(e.gen_H1_b2_recojet_eta - e.gen_H2_b2_recojet_eta))
                hResolved_RecoJet_DeltaEta_H2b1_H2b2.Fill(abs(e.gen_H2_b1_recojet_eta - e.gen_H2_b2_recojet_eta))
                
                hResolved_RecoJet_DeltaPhi_H1b1_H1b2.Fill(deltaPhi(e.gen_H1_b1_recojet_phi, e.gen_H1_b2_recojet_phi))
                hResolved_RecoJet_DeltaPhi_H1b1_H2b1.Fill(deltaPhi(e.gen_H1_b1_recojet_phi, e.gen_H2_b1_recojet_phi))
                hResolved_RecoJet_DeltaPhi_H1b1_H2b2.Fill(deltaPhi(e.gen_H1_b1_recojet_phi, e.gen_H2_b2_recojet_phi))
                hResolved_RecoJet_DeltaPhi_H1b2_H2b1.Fill(deltaPhi(e.gen_H1_b2_recojet_phi, e.gen_H2_b1_recojet_phi))
                hResolved_RecoJet_DeltaPhi_H1b2_H2b2.Fill(deltaPhi(e.gen_H1_b2_recojet_phi, e.gen_H2_b2_recojet_phi))
                hResolved_RecoJet_DeltaPhi_H2b1_H2b2.Fill(deltaPhi(e.gen_H2_b1_recojet_phi, e.gen_H2_b2_recojet_phi))
                
                hResolved_RecoJet_H1_pt.Fill(reco_H1.Pt())
                hResolved_RecoJet_H2_pt.Fill(reco_H2.Pt())
                hResolved_RecoJet_H1_eta.Fill(reco_H1.Eta())
                hResolved_RecoJet_H2_eta.Fill(reco_H2.Eta())
                hResolved_RecoJet_H1_phi.Fill(reco_H1.Phi())
                hResolved_RecoJet_H2_phi.Fill(reco_H2.Phi())
                hResolved_RecoJet_InvMass_H1.Fill(reco_H1.M())
                hResolved_RecoJet_InvMass_H2.Fill(reco_H2.M())
                hResolved_RecoJet_DeltaR_H1_H2.Fill(deltaR(reco_H1.Eta(), reco_H2.Eta(), reco_H1.Phi(), reco_H2.Phi()))
                hResolved_RecoJet_DeltaEta_H1_H2.Fill(abs(reco_H1.Eta() - reco_H2.Eta()))
                hResolved_RecoJet_DeltaPhi_H1_H2.Fill(abs(deltaPhi(reco_H1.Phi(), reco_H2.Phi())))

                hResolved_RecoJet_NJets.Fill(e.n_jet)
                hResolved_RecoJet_NFatJets.Fill(e.n_fatjet)
                
                bFound_reco_H1_b1 = False
                bFound_reco_H1_b2 = False
                bFound_reco_H2_b1 = False
                bFound_reco_H2_b2 = False
                
                reco_H1_b1_btag = -1.0
                reco_H1_b1_p4Regressed  = None
                
                reco_H1_b2_btag        = -1.0 
                reco_H1_b2_p4Regressed = None
                
                reco_H2_b1_btag        = -1.0
                reco_H2_b1_p4Regressed = None
                
                reco_H2_b2_btag        = -1.0 
                reco_H2_b2_p4Regressed = None
                
                reco_PFHT = 0.0
                
                nLoose = 0
                nMedium = 0
                nTight = 0
                
                for ij in range(0, e.n_jet):
                    eta = e.jet_eta.at(ij)
                    phi = e.jet_phi.at(ij)
                    pt  = e.jet_pt.at(ij)
                    btag = e.jet_btag.at(ij)
                    
                    isLoose = btag > 0.0490
                    isMedium = btag > 0.2783
                    isTight = btag > 0.7100

                    if (isLoose): nLoose += 1
                    if (isMedium): nMedium += 1
                    if (isTight): nTight += 1

                    if (pt > 30.0 and abs(eta) < 2.4):
                        reco_PFHT += pt

                    if (areSameJets(eta, e.gen_H1_b1_recojet_eta, phi, e.gen_H1_b1_recojet_phi)):
                        bFound_reco_H1_b1 = True
                        reco_H1_b1_btag        = e.jet_btag.at(ij)
                        reco_H1_b1_p4Regressed = getP4(e.jet_ptRegressed.at(ij), e.jet_eta.at(ij), e.jet_phi.at(ij), e.jet_mRegressed.at(ij))
                    elif (areSameJets(eta, e.gen_H1_b2_recojet_eta, phi, e.gen_H1_b2_recojet_phi)):
                        bFound_reco_H1_b2 = True
                        reco_H1_b2_btag        = e.jet_btag.at(ij)
                        reco_H1_b2_p4Regressed = getP4(e.jet_ptRegressed.at(ij), e.jet_eta.at(ij), e.jet_phi.at(ij), e.jet_mRegressed.at(ij))
                    elif (areSameJets(eta, e.gen_H2_b1_recojet_eta, phi, e.gen_H2_b1_recojet_phi)):
                        bFound_reco_H2_b1 = True
                        reco_H2_b1_btag        = e.jet_btag.at(ij)
                        reco_H2_b1_p4Regressed = getP4(e.jet_ptRegressed.at(ij), e.jet_eta.at(ij), e.jet_phi.at(ij), e.jet_mRegressed.at(ij))
                    elif (areSameJets(eta, e.gen_H2_b2_recojet_eta, phi, e.gen_H2_b2_recojet_phi)):
                        bFound_reco_H2_b2 = True
                        reco_H2_b2_btag        = e.jet_btag.at(ij)
                        reco_H2_b2_p4Regressed = getP4(e.jet_ptRegressed.at(ij), e.jet_eta.at(ij), e.jet_phi.at(ij), e.jet_mRegressed.at(ij))
                        
                hResolved_RecoJet_PFHT.Fill(reco_PFHT)
                hResolved_RecoJet_NLooseBJets.Fill(nLoose)
                hResolved_RecoJet_NMediumBJets.Fill(nMedium)
                hResolved_RecoJet_NTightBJets.Fill(nTight)
                if (e.n_jet > 0): hResolved_RecoJet_Jet1Pt.Fill(e.jet_pt.at(0))
                if (e.n_jet > 1): hResolved_RecoJet_Jet2Pt.Fill(e.jet_pt.at(1))
                if (e.n_jet > 2): hResolved_RecoJet_Jet3Pt.Fill(e.jet_pt.at(2))
                if (e.n_jet > 3): hResolved_RecoJet_Jet4Pt.Fill(e.jet_pt.at(3))
                if (e.n_jet > 0): hResolved_RecoJet_Jet1Eta.Fill(e.jet_eta.at(0))
                if (e.n_jet > 1): hResolved_RecoJet_Jet2Eta.Fill(e.jet_eta.at(1))
                if (e.n_jet > 2): hResolved_RecoJet_Jet3Eta.Fill(e.jet_eta.at(2))
                if (e.n_jet > 3): hResolved_RecoJet_Jet4Eta.Fill(e.jet_eta.at(3))
                if (e.n_fatjet > 0):
                    hResolved_RecoJet_AK8Jet1Pt.Fill(e.fatjet_pt.at(0))
                
                reco_H1_p4Regressed = None
                reco_H2_p4Regressed = None
                if (bFound_reco_H1_b1 and bFound_reco_H1_b2):
                    reco_H1_p4Regressed = reco_H1_b1_p4Regressed + reco_H1_b2_p4Regressed
                    hResolved_RecoJet_InvMassRegressed_H1.Fill(reco_H1_p4Regressed.M())
                if (bFound_reco_H2_b1 and bFound_reco_H2_b2):
                    reco_H2_p4Regressed = reco_H2_b1_p4Regressed + reco_H2_b2_p4Regressed
                    hResolved_RecoJet_InvMassRegressed_H2.Fill(reco_H2_p4Regressed.M())
                    
                if (bFound_reco_H1_b1):
                    hResolved_RecoJet_H1_b1_btag.Fill(reco_H1_b1_btag)
                if (bFound_reco_H1_b2):
                    hResolved_RecoJet_H1_b2_btag.Fill(reco_H1_b2_btag)
                if (bFound_reco_H2_b1):
                    hResolved_RecoJet_H2_b1_btag.Fill(reco_H2_b1_btag)
                if (bFound_reco_H2_b2):
                    hResolved_RecoJet_H2_b2_btag.Fill(reco_H2_b2_btag)



        
        # Write histograms in output file
        hPassed_HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5.Write()
        hPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np4.Write()
        hPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np2.Write()
        hPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p1.Write()
        hPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p17.Write()
        hPassed_HLT_PFHT1050.Write()
        hPassed_HLT_PFJet500.Write()
        hPassed_HLT_AK8PFHT800_TrimMass50.Write()
        hPassed_HLT_AK8PFJet400_TrimMass30.Write()
        hPassed_HLT_AK8PFJet420_TrimMass30.Write()
        hPassed_HLT_AK8PFJet500.Write()
        hPassed_HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59.Write()
        hPassed_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94.Write()
        hPassed_HLT_AK8PFHT750_TrimMass50.Write()
        hPassed_HLT_AK8PFJet360_TrimMass30.Write()
        hPassed_HLT_AK8PFJet380_TrimMass30.Write()
        hPassed_OR.Write()

        hResolvedPassed_HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5.Write()
        hResolvedPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np4.Write()
        hResolvedPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np2.Write()
        hResolvedPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p1.Write()
        hResolvedPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p17.Write()
        hResolvedPassed_HLT_PFHT1050.Write()
        hResolvedPassed_HLT_PFJet500.Write()
        hResolvedPassed_HLT_AK8PFHT800_TrimMass50.Write()
        hResolvedPassed_HLT_AK8PFJet400_TrimMass30.Write()
        hResolvedPassed_HLT_AK8PFJet420_TrimMass30.Write()
        hResolvedPassed_HLT_AK8PFJet500.Write()
        hResolvedPassed_HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59.Write()
        hResolvedPassed_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94.Write()
        hResolvedPassed_HLT_AK8PFHT750_TrimMass50.Write()
        hResolvedPassed_HLT_AK8PFJet360_TrimMass30.Write()
        hResolvedPassed_HLT_AK8PFJet380_TrimMass30.Write()
        hResolvedPassed_OR.Write()

        hResolvedExclPassed_HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5.Write()
        hResolvedExclPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np4.Write()
        hResolvedExclPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np2.Write()
        hResolvedExclPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p1.Write()
        hResolvedExclPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p17.Write()
        hResolvedExclPassed_HLT_PFHT1050.Write()
        hResolvedExclPassed_HLT_PFJet500.Write()
        hResolvedExclPassed_HLT_AK8PFHT800_TrimMass50.Write()
        hResolvedExclPassed_HLT_AK8PFJet400_TrimMass30.Write()
        hResolvedExclPassed_HLT_AK8PFJet420_TrimMass30.Write()
        hResolvedExclPassed_HLT_AK8PFJet500.Write()
        hResolvedExclPassed_HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59.Write()
        hResolvedExclPassed_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94.Write()
        hResolvedExclPassed_HLT_AK8PFHT750_TrimMass50.Write()
        hResolvedExclPassed_HLT_AK8PFJet360_TrimMass30.Write()
        hResolvedExclPassed_HLT_AK8PFJet380_TrimMass30.Write()
        hResolvedExclPassed_OR.Write()
        
        hBoostedPassed_HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5.Write()
        hBoostedPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np4.Write()
        hBoostedPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np2.Write()
        hBoostedPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p1.Write()
        hBoostedPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p17.Write()
        hBoostedPassed_HLT_PFHT1050.Write()
        hBoostedPassed_HLT_PFJet500.Write()
        hBoostedPassed_HLT_AK8PFHT800_TrimMass50.Write()
        hBoostedPassed_HLT_AK8PFJet400_TrimMass30.Write()
        hBoostedPassed_HLT_AK8PFJet420_TrimMass30.Write()
        hBoostedPassed_HLT_AK8PFJet500.Write()
        hBoostedPassed_HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59.Write()
        hBoostedPassed_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94.Write()
        hBoostedPassed_HLT_AK8PFHT750_TrimMass50.Write()
        hBoostedPassed_HLT_AK8PFJet360_TrimMass30.Write()
        hBoostedPassed_HLT_AK8PFJet380_TrimMass30.Write()
        hBoostedPassed_OR.Write()

        hSemiresolvedPassed_HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5.Write()
        hSemiresolvedPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np4.Write()
        hSemiresolvedPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np2.Write()
        hSemiresolvedPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p1.Write()
        hSemiresolvedPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p17.Write()
        hSemiresolvedPassed_HLT_PFHT1050.Write()
        hSemiresolvedPassed_HLT_PFJet500.Write()
        hSemiresolvedPassed_HLT_AK8PFHT800_TrimMass50.Write()
        hSemiresolvedPassed_HLT_AK8PFJet400_TrimMass30.Write()
        hSemiresolvedPassed_HLT_AK8PFJet420_TrimMass30.Write()
        hSemiresolvedPassed_HLT_AK8PFJet500.Write()
        hSemiresolvedPassed_HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59.Write()
        hSemiresolvedPassed_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94.Write()
        hSemiresolvedPassed_HLT_AK8PFHT750_TrimMass50.Write()
        hSemiresolvedPassed_HLT_AK8PFJet360_TrimMass30.Write()
        hSemiresolvedPassed_HLT_AK8PFJet380_TrimMass30.Write()
        hSemiresolvedPassed_OR.Write()
        
        h_GenPart_H1_pt.Write()
        h_GenPart_H2_pt.Write()
        h_GenPart_H1_eta.Write()
        h_GenPart_H2_eta.Write()
        h_GenPart_H1_phi.Write()
        h_GenPart_H2_phi.Write()
        h_GenPart_H1_b1_pt.Write()
        h_GenPart_H1_b2_pt.Write()
        h_GenPart_H2_b1_pt.Write()
        h_GenPart_H2_b2_pt.Write()
        h_GenPart_H1_b1_eta.Write()
        h_GenPart_H1_b2_eta.Write()
        h_GenPart_H2_b1_eta.Write()
        h_GenPart_H2_b2_eta.Write()
        h_GenPart_H1_b1_phi.Write()
        h_GenPart_H1_b2_phi.Write()
        h_GenPart_H2_b1_phi.Write()
        h_GenPart_H2_b2_phi.Write()
        
        hResolved_GenPart_H1_pt.Write()
        hResolved_GenPart_H2_pt.Write()
        hResolved_GenPart_H1_b1_pt.Write()
        hResolved_GenPart_H1_b2_pt.Write()
        hResolved_GenPart_H2_b1_pt.Write()
        hResolved_GenPart_H2_b2_pt.Write()
        hResolved_GenPart_H1_b1_eta.Write()
        hResolved_GenPart_H1_b2_eta.Write()
        hResolved_GenPart_H2_b1_eta.Write()
        hResolved_GenPart_H2_b2_eta.Write()
        hResolved_GenPart_H1_b1_phi.Write()
        hResolved_GenPart_H1_b2_phi.Write()
        hResolved_GenPart_H2_b1_phi.Write()
        hResolved_GenPart_H2_b2_phi.Write()
        hResolved_GenJet_H1_b1_pt.Write()
        hResolved_GenJet_H1_b2_pt.Write()
        hResolved_GenJet_H2_b1_pt.Write()
        hResolved_GenJet_H2_b2_pt.Write()
        hResolved_GenJet_H1_b1_eta.Write()
        hResolved_GenJet_H1_b2_eta.Write()
        hResolved_GenJet_H2_b1_eta.Write()
        hResolved_GenJet_H2_b2_eta.Write()
        hResolved_GenJet_H1_b1_phi.Write()
        hResolved_GenJet_H1_b2_phi.Write()
        hResolved_GenJet_H2_b1_phi.Write()
        hResolved_GenJet_H2_b2_phi.Write()
        hResolved_RecoJet_H1_b1_pt.Write()
        hResolved_RecoJet_H1_b2_pt.Write()
        hResolved_RecoJet_H2_b1_pt.Write()
        hResolved_RecoJet_H2_b2_pt.Write()
        hResolved_RecoJet_H1_b1_eta.Write()
        hResolved_RecoJet_H1_b2_eta.Write()
        hResolved_RecoJet_H2_b1_eta.Write()
        hResolved_RecoJet_H2_b2_eta.Write()
        hResolved_RecoJet_H1_b1_phi.Write()
        hResolved_RecoJet_H1_b2_phi.Write()
        hResolved_RecoJet_H2_b1_phi.Write()
        hResolved_RecoJet_H2_b2_phi.Write()
        hResolved_RecoJet_H1_b1_btag.Write()
        hResolved_RecoJet_H1_b2_btag.Write()
        hResolved_RecoJet_H2_b1_btag.Write()
        hResolved_RecoJet_H2_b2_btag.Write()
        hResolved_RecoJet_DeltaR_H1b1_H1b2.Write()
        hResolved_RecoJet_DeltaR_H1b1_H2b1.Write()
        hResolved_RecoJet_DeltaR_H1b1_H2b2.Write()
        hResolved_RecoJet_DeltaR_H1b2_H2b1.Write()
        hResolved_RecoJet_DeltaR_H1b2_H2b2.Write()
        hResolved_RecoJet_DeltaR_H2b1_H2b2.Write()
        hResolved_RecoJet_DeltaEta_H1b1_H1b2.Write()
        hResolved_RecoJet_DeltaEta_H1b1_H2b1.Write()
        hResolved_RecoJet_DeltaEta_H1b1_H2b2.Write()
        hResolved_RecoJet_DeltaEta_H1b2_H2b1.Write()
        hResolved_RecoJet_DeltaEta_H1b2_H2b2.Write()
        hResolved_RecoJet_DeltaEta_H2b1_H2b2.Write()
        hResolved_RecoJet_DeltaPhi_H1b1_H1b2.Write()
        hResolved_RecoJet_DeltaPhi_H1b1_H2b1.Write()
        hResolved_RecoJet_DeltaPhi_H1b1_H2b2.Write()
        hResolved_RecoJet_DeltaPhi_H1b2_H2b1.Write()
        hResolved_RecoJet_DeltaPhi_H1b2_H2b2.Write()
        hResolved_RecoJet_DeltaPhi_H2b1_H2b2.Write()
        hResolved_RecoJet_H1_pt.Write()
        hResolved_RecoJet_H2_pt.Write()
        hResolved_RecoJet_H1_eta.Write()
        hResolved_RecoJet_H2_eta.Write()
        hResolved_RecoJet_H1_phi.Write()
        hResolved_RecoJet_H2_phi.Write()
        hResolved_RecoJet_InvMass_H1.Write()
        hResolved_RecoJet_InvMass_H2.Write()
        hResolved_RecoJet_InvMassRegressed_H1.Write()
        hResolved_RecoJet_InvMassRegressed_H2.Write()
        hResolved_RecoJet_DeltaR_H1_H2.Write()
        hResolved_RecoJet_DeltaEta_H1_H2.Write()
        hResolved_RecoJet_DeltaPhi_H1_H2.Write()
        hResolved_RecoJet_NJets.Write()
        hResolved_RecoJet_NFatJets.Write()
        hResolved_RecoJet_PFHT.Write()
        hResolved_RecoJet_NLooseBJets.Write()
        hResolved_RecoJet_NMediumBJets.Write()
        hResolved_RecoJet_NTightBJets.Write()
        hResolved_RecoJet_Jet1Pt.Write()
        hResolved_RecoJet_Jet2Pt.Write()
        hResolved_RecoJet_Jet3Pt.Write()
        hResolved_RecoJet_Jet4Pt.Write()
        hResolved_RecoJet_Jet1Eta.Write()
        hResolved_RecoJet_Jet2Eta.Write()
        hResolved_RecoJet_Jet3Eta.Write()
        hResolved_RecoJet_Jet4Eta.Write()
        hResolved_RecoJet_AK8Jet1Pt.Write()
        
        hResolvedExcl_GenPart_H1_pt.Write()
        hResolvedExcl_GenPart_H2_pt.Write()
        hResolvedExcl_GenPart_H1_b1_pt.Write()
        hResolvedExcl_GenPart_H1_b2_pt.Write()
        hResolvedExcl_GenPart_H2_b1_pt.Write()
        hResolvedExcl_GenPart_H2_b2_pt.Write()
        hResolvedExcl_GenPart_H1_b1_eta.Write()
        hResolvedExcl_GenPart_H1_b2_eta.Write()
        hResolvedExcl_GenPart_H2_b1_eta.Write()
        hResolvedExcl_GenPart_H2_b2_eta.Write()
        hResolvedExcl_GenPart_H1_b1_phi.Write()
        hResolvedExcl_GenPart_H1_b2_phi.Write()
        hResolvedExcl_GenPart_H2_b1_phi.Write()
        hResolvedExcl_GenPart_H2_b2_phi.Write()
        hResolvedExcl_GenJet_H1_b1_pt.Write()
        hResolvedExcl_GenJet_H1_b2_pt.Write()
        hResolvedExcl_GenJet_H2_b1_pt.Write()
        hResolvedExcl_GenJet_H2_b2_pt.Write()
        hResolvedExcl_GenJet_H1_b1_eta.Write()
        hResolvedExcl_GenJet_H1_b2_eta.Write()
        hResolvedExcl_GenJet_H2_b1_eta.Write()
        hResolvedExcl_GenJet_H2_b2_eta.Write()
        hResolvedExcl_GenJet_H1_b1_phi.Write()
        hResolvedExcl_GenJet_H1_b2_phi.Write()
        hResolvedExcl_GenJet_H2_b1_phi.Write()
        hResolvedExcl_GenJet_H2_b2_phi.Write()
        hResolvedExcl_RecoJet_H1_b1_pt.Write()
        hResolvedExcl_RecoJet_H1_b2_pt.Write()
        hResolvedExcl_RecoJet_H2_b1_pt.Write()
        hResolvedExcl_RecoJet_H2_b2_pt.Write()
        hResolvedExcl_RecoJet_H1_b1_eta.Write()
        hResolvedExcl_RecoJet_H1_b2_eta.Write()
        hResolvedExcl_RecoJet_H2_b1_eta.Write()
        hResolvedExcl_RecoJet_H2_b2_eta.Write()
        hResolvedExcl_RecoJet_H1_b1_phi.Write()
        hResolvedExcl_RecoJet_H1_b2_phi.Write()
        hResolvedExcl_RecoJet_H2_b1_phi.Write()
        hResolvedExcl_RecoJet_H2_b2_phi.Write()
        hResolvedExcl_RecoJet_H1_b1_btag.Write()
        hResolvedExcl_RecoJet_H1_b2_btag.Write()
        hResolvedExcl_RecoJet_H2_b1_btag.Write()
        hResolvedExcl_RecoJet_H2_b2_btag.Write()
        hResolvedExcl_RecoJet_DeltaR_H1b1_H1b2.Write()
        hResolvedExcl_RecoJet_DeltaR_H1b1_H2b1.Write()
        hResolvedExcl_RecoJet_DeltaR_H1b1_H2b2.Write()
        hResolvedExcl_RecoJet_DeltaR_H1b2_H2b1.Write()
        hResolvedExcl_RecoJet_DeltaR_H1b2_H2b2.Write()
        hResolvedExcl_RecoJet_DeltaR_H2b1_H2b2.Write()
        hResolvedExcl_RecoJet_DeltaEta_H1b1_H1b2.Write()
        hResolvedExcl_RecoJet_DeltaEta_H1b1_H2b1.Write()
        hResolvedExcl_RecoJet_DeltaEta_H1b1_H2b2.Write()
        hResolvedExcl_RecoJet_DeltaEta_H1b2_H2b1.Write()
        hResolvedExcl_RecoJet_DeltaEta_H1b2_H2b2.Write()
        hResolvedExcl_RecoJet_DeltaEta_H2b1_H2b2.Write()
        hResolvedExcl_RecoJet_DeltaPhi_H1b1_H1b2.Write()
        hResolvedExcl_RecoJet_DeltaPhi_H1b1_H2b1.Write()
        hResolvedExcl_RecoJet_DeltaPhi_H1b1_H2b2.Write()
        hResolvedExcl_RecoJet_DeltaPhi_H1b2_H2b1.Write()
        hResolvedExcl_RecoJet_DeltaPhi_H1b2_H2b2.Write()
        hResolvedExcl_RecoJet_DeltaPhi_H2b1_H2b2.Write()
        hResolvedExcl_RecoJet_H1_pt.Write()
        hResolvedExcl_RecoJet_H2_pt.Write()
        hResolvedExcl_RecoJet_H1_eta.Write()
        hResolvedExcl_RecoJet_H2_eta.Write()
        hResolvedExcl_RecoJet_H1_phi.Write()
        hResolvedExcl_RecoJet_H2_phi.Write()
        hResolvedExcl_RecoJet_InvMass_H1.Write()
        hResolvedExcl_RecoJet_InvMass_H2.Write()
        hResolvedExcl_RecoJet_InvMassRegressed_H1.Write()
        hResolvedExcl_RecoJet_InvMassRegressed_H2.Write()
        hResolvedExcl_RecoJet_DeltaR_H1_H2.Write()
        hResolvedExcl_RecoJet_DeltaEta_H1_H2.Write()
        hResolvedExcl_RecoJet_DeltaPhi_H1_H2.Write()
        hResolvedExcl_RecoJet_NJets.Write()
        hResolvedExcl_RecoJet_NFatJets.Write()
        hResolvedExcl_RecoJet_PFHT.Write()
        hResolvedExcl_RecoJet_NLooseBJets.Write()
        hResolvedExcl_RecoJet_NMediumBJets.Write()
        hResolvedExcl_RecoJet_NTightBJets.Write()
        hResolvedExcl_RecoJet_Jet1Pt.Write()
        hResolvedExcl_RecoJet_Jet2Pt.Write()
        hResolvedExcl_RecoJet_Jet3Pt.Write()
        hResolvedExcl_RecoJet_Jet4Pt.Write()
        hResolvedExcl_RecoJet_Jet1Eta.Write()
        hResolvedExcl_RecoJet_Jet2Eta.Write()
        hResolvedExcl_RecoJet_Jet3Eta.Write()
        hResolvedExcl_RecoJet_Jet4Eta.Write()
        hResolvedExcl_RecoJet_AK8Jet1Pt.Write()
        
        hBoosted_GenPart_H1_pt.Write()
        hBoosted_GenPart_H2_pt.Write()
        hBoosted_GenPart_H1_b1_pt.Write()
        hBoosted_GenPart_H1_b2_pt.Write()
        hBoosted_GenPart_H2_b1_pt.Write()
        hBoosted_GenPart_H2_b2_pt.Write()
        hBoosted_GenPart_H1_b1_eta.Write()
        hBoosted_GenPart_H1_b2_eta.Write()
        hBoosted_GenPart_H2_b1_eta.Write()
        hBoosted_GenPart_H2_b2_eta.Write()
        hBoosted_GenPart_H1_b1_phi.Write()
        hBoosted_GenPart_H1_b2_phi.Write()
        hBoosted_GenPart_H2_b1_phi.Write()
        hBoosted_GenPart_H2_b2_phi.Write()
        hBoosted_GenFatJet_H1_pt.Write()
        hBoosted_GenFatJet_H2_pt.Write()
        hBoosted_GenFatJet_H1_eta.Write()
        hBoosted_GenFatJet_H2_eta.Write()
        hBoosted_GenFatJet_H1_phi.Write()
        hBoosted_GenFatJet_H2_phi.Write()
        hBoosted_RecoFatJet_H1_pt.Write()
        hBoosted_RecoFatJet_H2_pt.Write()
        hBoosted_RecoFatJet_H1_eta.Write()
        hBoosted_RecoFatJet_H2_eta.Write()
        hBoosted_RecoFatJet_H1_phi.Write()
        hBoosted_RecoFatJet_H2_phi.Write()
        hBoosted_RecoFatJet_H1_TXbb.Write()
        hBoosted_RecoFatJet_H2_TXbb.Write()
        
        hBoosted_RecoFatJet_H1_m.Write()
        hBoosted_RecoFatJet_H2_m.Write()
        hBoosted_NJets.Write()
        hBoosted_NFatJets.Write()
        hBoosted_RecoFatJet_DeltaR_H1_H2.Write()
        hBoosted_RecoFatJet_DeltaEta_H1_H2.Write()
        hBoosted_RecoFatJet_DeltaPhi_H1_H2.Write()

        hBoosted_RecoFatJet_H1_mSD_Uncorrected.Write()
        hBoosted_RecoFatJet_H1_area.Write()
        hBoosted_RecoFatJet_H1_n2b1.Write()
        hBoosted_RecoFatJet_H1_n3b1.Write()
        hBoosted_RecoFatJet_H1_tau21.Write()
        hBoosted_RecoFatJet_H1_tau32.Write()
        hBoosted_RecoFatJet_H1_nsubjets.Write()
        hBoosted_RecoFatJet_H1_subjet1_pt.Write()
        hBoosted_RecoFatJet_H1_subjet1_eta.Write()
        hBoosted_RecoFatJet_H1_subjet1_phi.Write()
        hBoosted_RecoFatJet_H1_subjet1_m.Write()
        hBoosted_RecoFatJet_H1_subjet1_btag.Write()
        hBoosted_RecoFatJet_H1_subjet2_pt.Write()
        hBoosted_RecoFatJet_H1_subjet2_eta.Write()
        hBoosted_RecoFatJet_H1_subjet2_phi.Write()
        hBoosted_RecoFatJet_H1_subjet2_m.Write()
        hBoosted_RecoFatJet_H1_subjet2_btag.Write()
        hBoosted_RecoFatJet_H2_mSD_Uncorrected.Write()
        hBoosted_RecoFatJet_H2_area.Write()
        hBoosted_RecoFatJet_H2_n2b1.Write()
        hBoosted_RecoFatJet_H2_n3b1.Write()
        hBoosted_RecoFatJet_H2_tau21.Write()
        hBoosted_RecoFatJet_H2_tau32.Write()
        hBoosted_RecoFatJet_H2_nsubjets.Write()
        hBoosted_RecoFatJet_H2_subjet1_pt.Write()
        hBoosted_RecoFatJet_H2_subjet1_eta.Write()
        hBoosted_RecoFatJet_H2_subjet1_phi.Write()
        hBoosted_RecoFatJet_H2_subjet1_m.Write()
        hBoosted_RecoFatJet_H2_subjet1_btag.Write()
        hBoosted_RecoFatJet_H2_subjet2_pt.Write()
        hBoosted_RecoFatJet_H2_subjet2_eta.Write()
        hBoosted_RecoFatJet_H2_subjet2_phi.Write()
        hBoosted_RecoFatJet_H2_subjet2_m.Write()
        hBoosted_RecoFatJet_H2_subjet2_btag.Write()
        
        hSemiresolved_GenPart_H1_pt.Write()
        hSemiresolved_GenPart_H2_pt.Write()
        hSemiresolved_GenPart_H1_b1_pt.Write()
        hSemiresolved_GenPart_H1_b2_pt.Write()
        hSemiresolved_GenPart_H2_b1_pt.Write()
        hSemiresolved_GenPart_H2_b2_pt.Write()
        hSemiresolved_GenPart_H1_b1_eta.Write()
        hSemiresolved_GenPart_H1_b2_eta.Write()
        hSemiresolved_GenPart_H2_b1_eta.Write()
        hSemiresolved_GenPart_H2_b2_eta.Write()
        hSemiresolved_GenPart_H1_b1_phi.Write()
        hSemiresolved_GenPart_H1_b2_phi.Write()
        hSemiresolved_GenPart_H2_b1_phi.Write()
        hSemiresolved_GenPart_H2_b2_phi.Write()
        hSemiresolved_H1Boosted_H2resolved_GenFatJet_H1_pt.Write()
        hSemiresolved_H1Boosted_H2resolved_GenFatJet_H1_eta.Write()
        hSemiresolved_H1Boosted_H2resolved_GenFatJet_H1_phi.Write()
        hSemiresolved_H1Boosted_H2resolved_GenJet_H2_b1_pt.Write()
        hSemiresolved_H1Boosted_H2resolved_GenJet_H2_b2_pt.Write()
        hSemiresolved_H1Boosted_H2resolved_GenJet_H2_b1_eta.Write()
        hSemiresolved_H1Boosted_H2resolved_GenJet_H2_b2_eta.Write()
        hSemiresolved_H1Boosted_H2resolved_GenJet_H2_b1_phi.Write()
        hSemiresolved_H1Boosted_H2resolved_GenJet_H2_b2_phi.Write()
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_pt.Write()
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_eta.Write()
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_phi.Write()
        hSemiresolved_H1Boosted_H2resolved_RecoJet_H2_b1_pt.Write()
        hSemiresolved_H1Boosted_H2resolved_RecoJet_H2_b2_pt.Write()
        hSemiresolved_H1Boosted_H2resolved_RecoJet_H2_b1_eta.Write()
        hSemiresolved_H1Boosted_H2resolved_RecoJet_H2_b2_eta.Write()
        hSemiresolved_H1Boosted_H2resolved_RecoJet_H2_b1_phi.Write()
        hSemiresolved_H1Boosted_H2resolved_RecoJet_H2_b2_phi.Write()
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_mSD_Uncorrected.Write()
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_area.Write()
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_n2b1.Write()
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_n3b1.Write()
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_tau21.Write()
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_tau32.Write()
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_nsubjets.Write()
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_pt.Write()
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_eta.Write()
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_phi.Write()
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_m.Write()
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_btag.Write()
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_pt.Write()
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_eta.Write()
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_phi.Write()
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_m.Write()
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_btag.Write()
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_TXbb.Write()
        hSemiresolved_H1Boosted_H2resolved_NJets.Write()
        hSemiresolved_H1Boosted_H2resolved_NFatJets.Write()
        hSemiresolved_H1Boosted_H2resolved_DeltaR_H1_H2.Write()
        hSemiresolved_H1Boosted_H2resolved_DeltaEta_H1_H2.Write()
        hSemiresolved_H1Boosted_H2resolved_DeltaPhi_H1_H2.Write()
        hSemiresolved_H1Boosted_H2resolved_InvMass_H2.Write()
        hSemiresolved_H1Boosted_H2resolved_InvMassRegressed_H2.Write()
        hSemiresolved_H1Boosted_H2resolved_H2_pt.Write()
        hSemiresolved_H1Boosted_H2resolved_H2_eta.Write()
        hSemiresolved_H1Boosted_H2resolved_H2_phi.Write()        
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_m.Write()
        hSemiresolved_H1Boosted_H2resolved_PFHT.Write()
        hSemiresolved_H1Boosted_H2resolved_NLooseBJets.Write()
        hSemiresolved_H1Boosted_H2resolved_NMediumBJets.Write()
        hSemiresolved_H1Boosted_H2resolved_NTightBJets.Write()
        hSemiresolved_H1Boosted_H2resolved_Jet1Pt.Write()
        hSemiresolved_H1Boosted_H2resolved_Jet2Pt.Write()
        hSemiresolved_H1Boosted_H2resolved_Jet3Pt.Write()
        hSemiresolved_H1Boosted_H2resolved_Jet4Pt.Write()
        hSemiresolved_H1Boosted_H2resolved_Jet1Eta.Write()
        hSemiresolved_H1Boosted_H2resolved_Jet2Eta.Write()
        hSemiresolved_H1Boosted_H2resolved_Jet3Eta.Write()
        hSemiresolved_H1Boosted_H2resolved_Jet4Eta.Write()
        hSemiresolved_H1Boosted_H2resolved_AK8Jet1Pt.Write()
        
        hSemiresolved_H2Boosted_H1resolved_GenFatJet_H2_pt.Write()
        hSemiresolved_H2Boosted_H1resolved_GenFatJet_H2_eta.Write()
        hSemiresolved_H2Boosted_H1resolved_GenFatJet_H2_phi.Write()
        hSemiresolved_H2Boosted_H1resolved_GenJet_H1_b1_pt.Write()
        hSemiresolved_H2Boosted_H1resolved_GenJet_H1_b2_pt.Write()
        hSemiresolved_H2Boosted_H1resolved_GenJet_H1_b1_eta.Write()
        hSemiresolved_H2Boosted_H1resolved_GenJet_H1_b2_eta.Write()
        hSemiresolved_H2Boosted_H1resolved_GenJet_H1_b1_phi.Write()
        hSemiresolved_H2Boosted_H1resolved_GenJet_H1_b2_phi.Write()
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_pt.Write()
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_eta.Write()
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_phi.Write()
        hSemiresolved_H2Boosted_H1resolved_RecoJet_H1_b1_pt.Write()
        hSemiresolved_H2Boosted_H1resolved_RecoJet_H1_b2_pt.Write()
        hSemiresolved_H2Boosted_H1resolved_RecoJet_H1_b1_eta.Write()
        hSemiresolved_H2Boosted_H1resolved_RecoJet_H1_b2_eta.Write()
        hSemiresolved_H2Boosted_H1resolved_RecoJet_H1_b1_phi.Write()
        hSemiresolved_H2Boosted_H1resolved_RecoJet_H1_b2_phi.Write()
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_mSD_Uncorrected.Write()
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_area.Write()
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_n2b1.Write()
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_n3b1.Write()
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_tau21.Write()
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_tau32.Write()
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_nsubjets.Write()
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_pt.Write()
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_eta.Write()
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_phi.Write()
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_m.Write()
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_btag.Write()
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_pt.Write()
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_eta.Write()
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_phi.Write()
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_m.Write()
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_btag.Write()
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_TXbb.Write()        
        
        hSemiresolved_H2Boosted_H1resolved_NJets.Write()
        hSemiresolved_H2Boosted_H1resolved_NFatJets.Write()
        hSemiresolved_H2Boosted_H1resolved_DeltaR_H1_H2.Write()
        hSemiresolved_H2Boosted_H1resolved_DeltaEta_H1_H2.Write()
        hSemiresolved_H2Boosted_H1resolved_DeltaPhi_H1_H2.Write()
        hSemiresolved_H2Boosted_H1resolved_InvMass_H1.Write()
        hSemiresolved_H2Boosted_H1resolved_InvMassRegressed_H1.Write()
        hSemiresolved_H2Boosted_H1resolved_H1_pt.Write()
        hSemiresolved_H2Boosted_H1resolved_H1_eta.Write()
        hSemiresolved_H2Boosted_H1resolved_H1_phi.Write()        
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_m.Write()
        
        
        print("\nAll events %s" % (entries))
        print("Gen Resolved events %s" % (cIsResolvedGen))
        print("Gen Semi-Resolved events %s" % (cIsSemiResolvedGen))
        print("Gen Boosted events %s" % (cIsBoostedGen))
        print("\n")
        print("Reco Resolved events %s" % (cIsResolvedReco))
        print("Reco Resolved exclusive events %s" % (cIsResolvedRecoExcl))
        print("Reco Semi-Resolved events %s" % (cIsSemiResolvedReco))
        print("Reco Boosted events %s" % (cIsBoostedReco))
        print("Unmatched reco events %s" %(cNotMatchedReco))
    
    fOut.Close()

    return

def getP4(pt, eta, phi, m):
    v = Math.LorentzVector('ROOT::Math::PtEtaPhiM4D<double>')(pt, eta, phi, m)
    return v

def deltaPhi(phi1, phi2):
    dPhi = abs(abs(abs(phi1 - phi2) - math.pi)-math.pi)
    return dPhi

def deltaR(eta1, eta2, phi1, phi2):
    dPhi = abs(abs(abs(phi1 - phi2) - math.pi)-math.pi)
    dEta = eta1-eta2
    dR2 = dPhi*dPhi + dEta*dEta
    dR  = math.sqrt(dR2)
    return dR

def areSameJets(eta1, eta2, phi1, phi2):
    dR = deltaR(eta1, eta2, phi1, phi2)
    if (dR < 0.02):
        return True
    else:
        return False

if __name__ == "__main__":

    # Default values
    VERBOSE       = True
    YEAR          = "2018"
    OUTPUT        = "HHTo4B_23Dec2022.root"
    DIRNAME       = "root://cmseos.fnal.gov//store/user/mkolosov/MultiHiggs/DiHiggs/RunIIAutumn18_NoSelections_GluGluToHHTo4B_22Dec2022"
    REDIRECTOR    = "root://cmseos.fnal.gov/"
    FORMATS       = [".png", ".pdf", ".C"]
    SAVEPATH      = getPublicPath()
    STUDY         = "HHTo4B_Categorization"
    
    parser = ArgumentParser(description="Derive the trigger scale factors")
    parser.add_argument("-v", "--verbose", dest="verbose", default=VERBOSE, action="store_true", help="Verbose mode for debugging purposes [default: %s]" % (VERBOSE))
    parser.add_argument("-d", "--dir", dest="dirName", type=str, action="store", default=DIRNAME, help="Location of the samples (a directory above) [default: %s]" % (DIRNAME))
    parser.add_argument("--year", dest="year", action="store", default=YEAR, help="Process year")
    parser.add_argument("--formats", dest="formats", default=FORMATS, action="store", help="Formats to save histograms")
    parser.add_argument("--output", dest="output", default=OUTPUT, action="store", help="The name of the output file")
    
    args = parser.parse_args()
    args.path = os.path.join(SAVEPATH, "%s_%s_%s" % (STUDY, YEAR, datetime.datetime.now().strftime('%d_%b_%Y')))
    args.output = args.output + "_%s.root" % (args.year)
    
    if not os.path.exists(args.path):
        os.makedirs(args.path)
    main(args)

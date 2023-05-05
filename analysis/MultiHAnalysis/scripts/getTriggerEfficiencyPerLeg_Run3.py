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
    
    hList = []
    
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
    
    bins_pt   = [30, 35, 40, 45, 50, 60, 70, 80, 100]
    bins_HT   = [200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 1000, 1250, 1500, 2000]
    
    h_PFHT       = ROOT.TH1F("h_PFHT_%s" % (sampleName), "h_PFHT_%s" % (sampleName), len(bins_HT)-1, array.array("d", bins_HT))
    h_ForthJetPt = ROOT.TH1F("h_ForthJetPt_%s" % (sampleName), "h_ForthJetPt_%s" % (sampleName), len(bins_pt)-1, array.array("d", bins_pt))
    h_NJets      = ROOT.TH1F("h_NJets_%s" % (sampleName), "h_NJets_%s" % (sampleName), 8, 0, 8)
    h_NBJets     = ROOT.TH1F("h_NBJets_%s" % (sampleName), "h_NBJets_%s" % (sampleName), 6, 0, 6)
    
    # PFHT
    h_PFHT_Passed_L1 = ROOT.TH1F("h_PFHT_Passed_L1_%s" % (sampleName), "h_PFHT_Passed_L1_%s" % (sampleName), len(bins_HT)-1, array.array("d", bins_HT))
    h_PFHT_Passed_4PixelOnlyPFCentralJetTightIDPt20 = ROOT.TH1F("h_PFHT_Passed_4PixelOnlyPFCentralJetTightIDPt20_%s" % (sampleName), "h_PFHT_Passed_4PixelOnlyPFCentralJetTightIDPt20_%s" % (sampleName), len(bins_HT)-1, array.array("d", bins_HT))
    h_PFHT_Passed_3PixelOnlyPFCentralJetTightIDPt30 = ROOT.TH1F("h_PFHT_Passed_3PixelOnlyPFCentralJetTightIDPt30_%s" % (sampleName), "h_PFHT_Passed_3PixelOnlyPFCentralJetTightIDPt30_%s" % (sampleName), len(bins_HT)-1, array.array("d", bins_HT))
    h_PFHT_Passed_2PixelOnlyPFCentralJetTightIDPt40 = ROOT.TH1F("h_PFHT_Passed_2PixelOnlyPFCentralJetTightIDPt40_%s" % (sampleName), "h_PFHT_Passed_2PixelOnlyPFCentralJetTightIDPt40_%s" % (sampleName), len(bins_HT)-1, array.array("d", bins_HT))
    h_PFHT_Passed_1PixelOnlyPFCentralJetTightIDPt60 = ROOT.TH1F("h_PFHT_Passed_1PixelOnlyPFCentralJetTightIDPt60_%s" % (sampleName), "h_PFHT_Passed_1PixelOnlyPFCentralJetTightIDPt60_%s" % (sampleName), len(bins_HT)-1, array.array("d", bins_HT))
    h_PFHT_Passed_4PFCentralJetTightIDPt35 = ROOT.TH1F("h_PFHT_Passed_4PFCentralJetTightIDPt35_%s" % (sampleName), "h_PFHT_Passed_4PFCentralJetTightIDPt35_%s" % (sampleName), len(bins_HT)-1, array.array("d", bins_HT))
    h_PFHT_Passed_3PFCentralJetTightIDPt40 = ROOT.TH1F("h_PFHT_Passed_3PFCentralJetTightIDPt40_%s" % (sampleName), "h_PFHT_Passed_3PFCentralJetTightIDPt40_%s" % (sampleName), len(bins_HT)-1, array.array("d", bins_HT))
    h_PFHT_Passed_2PFCentralJetTightIDPt50 = ROOT.TH1F("h_PFHT_Passed_2PFCentralJetTightIDPt50_%s" % (sampleName), "h_PFHT_Passed_2PFCentralJetTightIDPt50_%s" % (sampleName), len(bins_HT)-1, array.array("d", bins_HT))
    h_PFHT_Passed_1PFCentralJetTightIDPt70 = ROOT.TH1F("h_PFHT_Passed_1PFCentralJetTightIDPt70_%s" % (sampleName), "h_PFHT_Passed_1PFCentralJetTightIDPt70_%s" % (sampleName), len(bins_HT)-1, array.array("d", bins_HT))
    h_PFHT_Passed_FullPath = ROOT.TH1F("h_PFHT_Passed_FullPath_%s" % (sampleName), "h_PFHT_Passed_FullPath_%s" % (sampleName), len(bins_HT)-1, array.array("d", bins_HT))
    h_PFHT_Passed_MuonEGplusFullPath = ROOT.TH1F("h_PFHT_Passed_MuonEGplusFullPath_%s" % (sampleName), "h_PFHT_Passed_MuonEGplusFullPath_%s" % (sampleName), len(bins_HT)-1, array.array("d", bins_HT))
    
    # 4th jet pT
    h_ForthJetPt = ROOT.TH1F("h_ForthJetPt_%s" % (sampleName), "h_ForthJetPt_%s" % (sampleName), len(bins_pt)-1, array.array("d", bins_pt))
    h_ForthJetPt_Passed_L1 = ROOT.TH1F("h_ForthJetPt_Passed_L1_%s" % (sampleName), "h_ForthJetPt_Passed_L1_%s" % (sampleName), len(bins_pt)-1, array.array("d", bins_pt))
    h_ForthJetPt_Passed_4PixelOnlyPFCentralJetTightIDPt20 = ROOT.TH1F("h_ForthJetPt_Passed_4PixelOnlyPFCentralJetTightIDPt20_%s" % (sampleName), "h_ForthJetPt_Passed_4PixelOnlyPFCentralJetTightIDPt20_%s" % (sampleName), len(bins_pt)-1, array.array("d", bins_pt))
    h_ForthJetPt_Passed_3PixelOnlyPFCentralJetTightIDPt30 = ROOT.TH1F("h_ForthJetPt_Passed_3PixelOnlyPFCentralJetTightIDPt30_%s" % (sampleName), "h_ForthJetPt_Passed_3PixelOnlyPFCentralJetTightIDPt30_%s" % (sampleName), len(bins_pt)-1, array.array("d", bins_pt))
    h_ForthJetPt_Passed_2PixelOnlyPFCentralJetTightIDPt40 = ROOT.TH1F("h_ForthJetPt_Passed_2PixelOnlyPFCentralJetTightIDPt40_%s" % (sampleName), "h_ForthJetPt_Passed_2PixelOnlyPFCentralJetTightIDPt40_%s" % (sampleName), len(bins_pt)-1, array.array("d", bins_pt))
    h_ForthJetPt_Passed_1PixelOnlyPFCentralJetTightIDPt60 = ROOT.TH1F("h_ForthJetPt_Passed_1PixelOnlyPFCentralJetTightIDPt60_%s" % (sampleName), "h_ForthJetPt_Passed_1PixelOnlyPFCentralJetTightIDPt60_%s" % (sampleName), len(bins_pt)-1, array.array("d", bins_pt))
    h_ForthJetPt_Passed_4PFCentralJetTightIDPt35 = ROOT.TH1F("h_ForthJetPt_Passed_4PFCentralJetTightIDPt35_%s" % (sampleName), "h_ForthJetPt_Passed_4PFCentralJetTightIDPt35_%s" % (sampleName), len(bins_pt)-1, array.array("d", bins_pt))
    h_ForthJetPt_Passed_3PFCentralJetTightIDPt40 = ROOT.TH1F("h_ForthJetPt_Passed_3PFCentralJetTightIDPt40_%s" % (sampleName), "h_ForthJetPt_Passed_3PFCentralJetTightIDPt40_%s" % (sampleName), len(bins_pt)-1, array.array("d", bins_pt))
    h_ForthJetPt_Passed_2PFCentralJetTightIDPt50 = ROOT.TH1F("h_ForthJetPt_Passed_2PFCentralJetTightIDPt50_%s" % (sampleName), "h_ForthJetPt_Passed_2PFCentralJetTightIDPt50_%s" % (sampleName), len(bins_pt)-1, array.array("d", bins_pt))
    h_ForthJetPt_Passed_1PFCentralJetTightIDPt70 = ROOT.TH1F("h_ForthJetPt_Passed_1PFCentralJetTightIDPt70_%s" % (sampleName), "h_ForthJetPt_Passed_1PFCentralJetTightIDPt70_%s" % (sampleName), len(bins_pt)-1, array.array("d", bins_pt))
    h_ForthJetPt_Passed_FullPath = ROOT.TH1F("h_ForthJetPt_Passed_FullPath_%s" % (sampleName), "h_ForthJetPt_Passed_FullPath_%s" % (sampleName), len(bins_pt)-1, array.array("d", bins_pt))
    h_ForthJetPt_Passed_MuonEGplusFullPath = ROOT.TH1F("h_ForthJetPt_Passed_MuonEGplusFullPath_%s" % (sampleName), "h_ForthJetPt_Passed_MuonEGplusFullPath_%s" % (sampleName), len(bins_pt)-1, array.array("d", bins_pt))
    
    for i, e in enumerate(t):
        
        # Triggers to study
        b_HLT_IsoMu24 = e.HLT_IsoMu24
        b_HLT_IsoMu27 = e.HLT_IsoMu27
        b_HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ = e.HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ
        b_HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_QuadPFJet70_50_40_30 = e.HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_QuadPFJet70_50_40_30
        b_HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_QuadPFJet70_50_40_30_PFBTagParticleNet_2BTagSum0p65 = e.HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_QuadPFJet70_50_40_30_PFBTagParticleNet_2BTagSum0p65
        b_HLT_QuadPFJet70_50_40_35_PFBTagParticleNet_2BTagSum0p65 = e.HLT_QuadPFJet70_50_40_35_PFBTagParticleNet_2BTagSum0p65
        
        bDen_OR = b_HLT_IsoMu24 or b_HLT_IsoMu27 or b_HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ
        if (not bDen_OR): continue
        
        # Number of selected jets
        if (e.NSelectedJets < 4): continue
        if (e.LdgInPtJet_pt < 70): continue
        if (e.SubldgInPtJet_pt < 50): continue
        if (e.ThirdldgInPtJet_pt < 40): continue
        if (e.ForthldgInPtJet_pt < 35): continue
        
        if (e.LdgInBDiscJet_bDisc < 0.2783): continue
        if (e.SubldgInBDiscJet_bDisc < 0.2783): continue


        h_PFHT.Fill(e.PFHT)
        h_ForthJetPt.Fill(e.ForthldgInPtJet_pt)
        h_NJets.Fill(e.NSelectedJets)
        h_NBJets.Fill(e.NSelectedBJets)
        
        if (b_HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_QuadPFJet70_50_40_30_PFBTagParticleNet_2BTagSum0p65):
            h_PFHT_Passed_MuonEGplusFullPath.Fill(e.PFHT)
            h_ForthJetPt_Passed_MuonEGplusFullPath.Fill(e.ForthldgInPtJet_pt)
        
        if (b_HLT_QuadPFJet70_50_40_35_PFBTagParticleNet_2BTagSum0p65):
            h_PFHT_Passed_FullPath.Fill(e.PFHT)
            h_ForthJetPt_Passed_FullPath.Fill(e.ForthldgInPtJet_pt)


        if (e.L1_L1sQuadJetOrHTTOrMuonHTT):
            h_PFHT_Passed_L1.Fill(e.PFHT)
            h_ForthJetPt_Passed_L1.Fill(e.ForthldgInPtJet_pt)
            
            if (e.FourPixelOnlyPFCentralJetTightIDPt20 >= 4):
                h_PFHT_Passed_4PixelOnlyPFCentralJetTightIDPt20.Fill(e.PFHT)
                h_ForthJetPt_Passed_4PixelOnlyPFCentralJetTightIDPt20.Fill(e.ForthldgInPtJet_pt)
                
                if (e.ThreePixelOnlyPFCentralJetTightIDPt30 >= 3):
                    h_PFHT_Passed_3PixelOnlyPFCentralJetTightIDPt30.Fill(e.PFHT)
                    h_ForthJetPt_Passed_3PixelOnlyPFCentralJetTightIDPt30.Fill(e.ForthldgInPtJet_pt)
            
                    if (e.TwoPixelOnlyPFCentralJetTightIDPt40 >= 2):
                        h_PFHT_Passed_2PixelOnlyPFCentralJetTightIDPt40.Fill(e.PFHT)
                        h_ForthJetPt_Passed_2PixelOnlyPFCentralJetTightIDPt40.Fill(e.ForthldgInPtJet_pt)
                    
                        if (e.OnePixelOnlyPFCentralJetTightIDPt60 >= 1):
                            h_PFHT_Passed_1PixelOnlyPFCentralJetTightIDPt60.Fill(e.PFHT)
                            h_ForthJetPt_Passed_1PixelOnlyPFCentralJetTightIDPt60.Fill(e.ForthldgInPtJet_pt)
                            
                            if (e.FourPFCentralJetTightIDPt35 >= 4):
                                h_PFHT_Passed_4PFCentralJetTightIDPt35.Fill(e.PFHT)
                                h_ForthJetPt_Passed_4PFCentralJetTightIDPt35.Fill(e.ForthldgInPtJet_pt)
                                
                                if (e.ThreePFCentralJetTightIDPt40 >= 3):
                                    h_PFHT_Passed_3PFCentralJetTightIDPt40.Fill(e.PFHT)
                                    h_ForthJetPt_Passed_3PFCentralJetTightIDPt40.Fill(e.ForthldgInPtJet_pt)

                                    if (e.TwoPFCentralJetTightIDPt50 >= 2):
                                        h_PFHT_Passed_2PFCentralJetTightIDPt50.Fill(e.PFHT)
                                        h_ForthJetPt_Passed_2PFCentralJetTightIDPt50.Fill(e.ForthldgInPtJet_pt)
                                    
                                        if (e.OnePFCentralJetTightIDPt70 >= 1):
                                            h_PFHT_Passed_1PFCentralJetTightIDPt70.Fill(e.PFHT)
                                            h_ForthJetPt_Passed_1PFCentralJetTightIDPt70.Fill(e.ForthldgInPtJet_pt)
                                

    hList.append(h_PFHT)
    hList.append(h_NJets)
    hList.append(h_NBJets)
    hList.append(h_ForthJetPt)
    
    hList.append(h_PFHT_Passed_FullPath)
    hList.append(h_PFHT_Passed_MuonEGplusFullPath)
    hList.append(h_PFHT_Passed_L1)
    hList.append(h_PFHT_Passed_4PixelOnlyPFCentralJetTightIDPt20)
    hList.append(h_PFHT_Passed_3PixelOnlyPFCentralJetTightIDPt30)
    hList.append(h_PFHT_Passed_2PixelOnlyPFCentralJetTightIDPt40)
    hList.append(h_PFHT_Passed_1PixelOnlyPFCentralJetTightIDPt60)
    hList.append(h_PFHT_Passed_4PFCentralJetTightIDPt35)
    hList.append(h_PFHT_Passed_3PFCentralJetTightIDPt40)
    hList.append(h_PFHT_Passed_2PFCentralJetTightIDPt50)
    hList.append(h_PFHT_Passed_1PFCentralJetTightIDPt70)
        
    hList.append(h_ForthJetPt_Passed_FullPath)
    hList.append(h_ForthJetPt_Passed_MuonEGplusFullPath)
    hList.append(h_ForthJetPt_Passed_L1)
    hList.append(h_ForthJetPt_Passed_4PixelOnlyPFCentralJetTightIDPt20)
    hList.append(h_ForthJetPt_Passed_3PixelOnlyPFCentralJetTightIDPt30)
    hList.append(h_ForthJetPt_Passed_2PixelOnlyPFCentralJetTightIDPt40)
    hList.append(h_ForthJetPt_Passed_1PixelOnlyPFCentralJetTightIDPt60)
    hList.append(h_ForthJetPt_Passed_4PFCentralJetTightIDPt35)
    hList.append(h_ForthJetPt_Passed_3PFCentralJetTightIDPt40)
    hList.append(h_ForthJetPt_Passed_2PFCentralJetTightIDPt50)
    hList.append(h_ForthJetPt_Passed_1PFCentralJetTightIDPt70)
    
    def GetTGraphAsymmErrors(hNum, hDen, filterName, xLabel, yLabel, saveName, sampleName):
        h = ROOT.TGraphAsymmErrors(hNum, hDen)
        h.SetTitle("Efficiency of %s; %s; %s" % (filterName, xLabel, yLabel))
        h.SetName("Efficiency_%s" % (saveName))
        h.SetLineColor(GetColor(sampleName))
        h.SetMarkerColor(GetColor(sampleName))
        h.GetYaxis().SetRangeUser(0.0, 1.1)
        return h
        
    xLabel = "PF H_{T} [GeV]"
    yLabel = "#varepsilon_{HLT filter}"
    var = "HT"
    hList.append(GetTGraphAsymmErrors(h_PFHT_Passed_L1, h_PFHT, "L1sQuadJetOrHTTOrMuonHTT", xLabel, "#varepsilon_{L1}", "L1_vs_HT_%s" % (sampleName), sampleName))
    hList.append(GetTGraphAsymmErrors(h_PFHT_Passed_4PixelOnlyPFCentralJetTightIDPt20, h_PFHT_Passed_L1, "4PixelOnlyPFCentralJetTightIDPt20", xLabel, yLabel, "4PixelOnlyPFCentralJetTightIDPt20_vs_%s_%s" % (var, sampleName), sampleName))
    hList.append(GetTGraphAsymmErrors(h_PFHT_Passed_3PixelOnlyPFCentralJetTightIDPt30, h_PFHT_Passed_4PixelOnlyPFCentralJetTightIDPt20, "3PixelOnlyPFCentralJetTightIDPt30", xLabel, yLabel, "3PixelOnlyPFCentralJetTightIDPt30_vs_%s_%s" % (var, sampleName), sampleName))
    hList.append(GetTGraphAsymmErrors(h_PFHT_Passed_2PixelOnlyPFCentralJetTightIDPt40, h_PFHT_Passed_3PixelOnlyPFCentralJetTightIDPt30, "2PixelOnlyPFCentralJetTightIDPt40", xLabel, yLabel, "2PixelOnlyPFCentralJetTightIDPt40_vs_%s_%s" % (var, sampleName), sampleName))
    hList.append(GetTGraphAsymmErrors(h_PFHT_Passed_1PixelOnlyPFCentralJetTightIDPt60, h_PFHT_Passed_2PixelOnlyPFCentralJetTightIDPt40, "1PixelOnlyPFCentralJetTightIDPt60", xLabel, yLabel, "1PixelOnlyPFCentralJetTightIDPt60_vs_%s_%s" % (var, sampleName), sampleName))
    hList.append(GetTGraphAsymmErrors(h_PFHT_Passed_4PFCentralJetTightIDPt35, h_PFHT_Passed_1PixelOnlyPFCentralJetTightIDPt60, "4PFCentralJetTightIDPt35", xLabel, yLabel, "4PFCentralJetTightIDPt35_vs_%s_%s" % (var, sampleName), sampleName))
    hList.append(GetTGraphAsymmErrors(h_PFHT_Passed_3PFCentralJetTightIDPt40, h_PFHT_Passed_4PFCentralJetTightIDPt35, "3PFCentralJetTightIDPt40", xLabel, yLabel, "3PFCentralJetTightIDPt40_vs_%s_%s" % (var, sampleName), sampleName))
    hList.append(GetTGraphAsymmErrors(h_PFHT_Passed_2PFCentralJetTightIDPt50, h_PFHT_Passed_3PFCentralJetTightIDPt40, "2PFCentralJetTightIDPt50", xLabel, yLabel, "2PFCentralJetTightIDPt50_vs_%s_%s" % (var, sampleName), sampleName))
    hList.append(GetTGraphAsymmErrors(h_PFHT_Passed_1PFCentralJetTightIDPt70, h_PFHT_Passed_2PFCentralJetTightIDPt50, "1PFCentralJetTightIDPt70", xLabel, yLabel, "1PFCentralJetTightIDPt70_vs_%s_%s" % (var, sampleName), sampleName))
    yLabel = "#varepsilon_{L1+HLT}"
    hList.append(GetTGraphAsymmErrors(h_PFHT_Passed_FullPath, h_PFHT, "FullPath", xLabel, yLabel, "L1plusHLT_FullPath_vs_%s_%s" % (var, sampleName), sampleName))
    hList.append(GetTGraphAsymmErrors(h_PFHT_Passed_MuonEGplusFullPath, h_PFHT, "MuonEGplusFullPath", xLabel, yLabel, "L1plusHLT_MuonEGplusFullPath_vs_%s_%s" % (var, sampleName), sampleName))
    
    xLabel = "p_{T, 4} [GeV]"
    yLabel = "#varepsilon_{HLT filter}"
    var = "Jet4Pt"
    hList.append(GetTGraphAsymmErrors(h_ForthJetPt_Passed_L1, h_ForthJetPt, "L1sQuadJetOrHTTOrMuonHTT", xLabel, "#varepsilon_{L1}", "L1_vs_%s_%s" % (var, sampleName), sampleName))
    hList.append(GetTGraphAsymmErrors(h_ForthJetPt_Passed_4PixelOnlyPFCentralJetTightIDPt20, h_ForthJetPt_Passed_L1, "4PixelOnlyPFCentralJetTightIDPt20", xLabel, yLabel, "4PixelOnlyPFCentralJetTightIDPt20_vs_%s_%s" % (var, sampleName), sampleName))
    hList.append(GetTGraphAsymmErrors(h_ForthJetPt_Passed_3PixelOnlyPFCentralJetTightIDPt30, h_ForthJetPt_Passed_4PixelOnlyPFCentralJetTightIDPt20, "3PixelOnlyPFCentralJetTightIDPt30", xLabel, yLabel, "3PixelOnlyPFCentralJetTightIDPt30_vs_%s_%s" % (var, sampleName), sampleName))
    hList.append(GetTGraphAsymmErrors(h_ForthJetPt_Passed_2PixelOnlyPFCentralJetTightIDPt40, h_ForthJetPt_Passed_3PixelOnlyPFCentralJetTightIDPt30, "2PixelOnlyPFCentralJetTightIDPt40", xLabel, yLabel, "2PixelOnlyPFCentralJetTightIDPt40_vs_%s_%s" % (var, sampleName), sampleName))
    hList.append(GetTGraphAsymmErrors(h_ForthJetPt_Passed_1PixelOnlyPFCentralJetTightIDPt60, h_ForthJetPt_Passed_2PixelOnlyPFCentralJetTightIDPt40, "1PixelOnlyPFCentralJetTightIDPt60", xLabel, yLabel, "1PixelOnlyPFCentralJetTightIDPt60_vs_%s_%s" % (var, sampleName), sampleName))
    hList.append(GetTGraphAsymmErrors(h_ForthJetPt_Passed_4PFCentralJetTightIDPt35, h_ForthJetPt_Passed_1PixelOnlyPFCentralJetTightIDPt60, "4PFCentralJetTightIDPt35", xLabel, yLabel, "4PFCentralJetTightIDPt35_vs_%s_%s" % (var, sampleName), sampleName))
    hList.append(GetTGraphAsymmErrors(h_ForthJetPt_Passed_3PFCentralJetTightIDPt40, h_ForthJetPt_Passed_4PFCentralJetTightIDPt35, "3PFCentralJetTightIDPt40", xLabel, yLabel, "3PFCentralJetTightIDPt40_vs_%s_%s" % (var, sampleName), sampleName))
    hList.append(GetTGraphAsymmErrors(h_ForthJetPt_Passed_2PFCentralJetTightIDPt50, h_ForthJetPt_Passed_3PFCentralJetTightIDPt40, "2PFCentralJetTightIDPt50", xLabel, yLabel, "2PFCentralJetTightIDPt50_vs_%s_%s" % (var, sampleName), sampleName))
    hList.append(GetTGraphAsymmErrors(h_ForthJetPt_Passed_1PFCentralJetTightIDPt70, h_ForthJetPt_Passed_2PFCentralJetTightIDPt50, "1PFCentralJetTightIDPt70", xLabel, yLabel, "1PFCentralJetTightIDPt70_vs_%s_%s" % (var, sampleName), sampleName))
    yLabel = "#varepsilon_{L1+HLT}"
    hList.append(GetTGraphAsymmErrors(h_ForthJetPt_Passed_FullPath, h_ForthJetPt, "FullPath", xLabel, yLabel, "L1plusHLT_FullPath_vs_%s_%s" % (var, sampleName), sampleName))
    hList.append(GetTGraphAsymmErrors(h_ForthJetPt_Passed_MuonEGplusFullPath, h_ForthJetPt, "MuonEGplusFullPath", xLabel, yLabel, "L1plusHLT_MuonEGplusFullPath_vs_%s_%s" % (var, sampleName), sampleName))

    




    return hList



def GetEfficiencies22(f, sampleName):
    
    hList = []
    
    # Read the tree
    t = f.Get("TrgTree")
    t.SetAlias("OnePFCentralJetTightID75", "1PFCentralJetLooseID75")
    t.SetAlias("TwoPFCentralJetLooseID60", "2PFCentralJetLooseID60")
    t.SetAlias("ThreePFCentralJetLooseID45", "3PFCentralJetLooseID45")
    t.SetAlias("FourPFCentralJetLooseID35", "4PFCentralJetLooseID35")
    
    nentries = t.GetEntries()
    
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Book the histograms
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    h_caloJetSum_before_L1filterHT = ROOT.TH1F("%s__DistributionBefore_L1filterHT" %(sampleName), "%s__DistributionBefore_L1filterHT" %(sampleName), 60, 100, 1500)
    h_caloJetSum_passed_L1filterHT = ROOT.TH1F("%s__DistributionPassed_L1filterHT" %(sampleName), "%s__DistributionPassed_L1filterHT" %(sampleName), 60, 100, 1500) 
    
    varBins = [15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 120, 140, 160, 180, 220, 260, 300]
    h_jetForthHighestPt_pt_before_QuadCentralJet30 = ROOT.TH1F("%s__DistributionBefore_QuadCentralJet30" % (sampleName), "%s__DistributionBefore_QuadCentralJet30" % (sampleName), len(varBins)-1, array.array("d", varBins))
    h_jetForthHighestPt_pt_passed_QuadCentralJet30 = ROOT.TH1F("%s__DistributionPassed_QuadCentralJet30" % (sampleName), "%s__DistributionPassed_QuadCentralJet30" % (sampleName), len(varBins)-1, array.array("d", varBins))
    
    h_caloJetSum_before_CaloQuadJet30HT320 = ROOT.TH1F("%s__DistributionBefore_CaloQuadJet30HT320" % (sampleName), "%s__DistributionBefore_CaloQuadJet30HT320" % (sampleName), 50, 200, 1200)
    h_caloJetSum_passed_CaloQuadJet30HT320 = ROOT.TH1F("%s__DistributionPassed_CaloQuadJet30HT320" % (sampleName), "%s__DistributionPassed_CaloQuadJet30HT320" % (sampleName), 50, 200, 1200)
    
    varBins=[0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.54, 0.58, 0.62, 0.66, 0.70, 0.74, 0.78, 0.82, 0.84, 0.86, 0.90, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99, 1.0]
    h_jetFirstHighestDeepFlavB_deepFlavB_before_BTagCaloDeepCSVp17Double = ROOT.TH1F("%s__DistributionBefore_BTagCaloDeepCSVp17Double" % (sampleName), "%s__DistributionBefore_BTagCaloDeepCSVp17Double" % (sampleName), len(varBins)-1, array.array("d", varBins))
    h_jetFirstHighestDeepFlavB_deepFlavB_passed_BTagCaloDeepCSVp17Double = ROOT.TH1F("%s__DistributionPassed_BTagCaloDeepCSVp17Double" % (sampleName), "%s__DistributionPassed_BTagCaloDeepCSVp17Double" % (sampleName), len(varBins)-1, array.array("d", varBins))
    
    varBins = [i for i in range(20, 100+5, 5)] + [i for i in range(100+10, 150+10, 10)] + [i for i in range(150+20, 250+20, 20)]
    h_jetForthHighestPt_pt_before_PFCentralJetLooseIDQuad30 = ROOT.TH1F("%s__DistributionBefore_PFCentralJetLooseIDQuad30" % (sampleName), "%s__DistributionBefore_PFCentralJetLooseIDQuad30" % (sampleName), len(varBins)-1, array.array("d", varBins))
    h_jetForthHighestPt_pt_passed_PFCentralJetLooseIDQuad30 = ROOT.TH1F("%s__DistributionPassed_PFCentralJetLooseIDQuad30" % (sampleName), "%s__DistributionPassed_PFCentralJetLooseIDQuad30" % (sampleName), len(varBins)-1, array.array("d", varBins))
    
    h_jetFirstHighestPt_pt_before_1PFCentralJetLooseID75 = ROOT.TH1F("%s__DistributionBefore_1PFCentralJetLooseID75" % (sampleName), "%s__DistributionBefore_1PFCentralJetLooseID75" % (sampleName), 50, 20, 500)
    h_jetFirstHighestPt_pt_passed_1PFCentralJetLooseID75 = ROOT.TH1F("%s__DistributionPassed_1PFCentralJetLooseID75" % (sampleName), "%s__DistributionPassed_1PFCentralJetLooseID75" % (sampleName), 50, 20, 500)
    
    h_jetSecondHighestPt_pt_before_2PFCentralJetLooseID60 = ROOT.TH1F("%s__DistributionBefore_2PFCentralJetLooseID60" % (sampleName), "%s__DistributionBefore_2PFCentralJetLooseID60" %(sampleName), 50, 20, 300)
    h_jetSecondHighestPt_pt_passed_2PFCentralJetLooseID60 = ROOT.TH1F("%s__DistributionPassed_2PFCentralJetLooseID60" % (sampleName), "%s__DistributionPassed_2PFCentralJetLooseID60" % (sampleName), 50, 20, 300)
    
    h_jetThirdHighestPt_pt_before_3PFCentralJetLooseID45 = ROOT.TH1F("%s__DistributionBefore_3PFCentralJetLooseID45" % (sampleName), "%s__DistributionBefore_3PFCentralJetLooseID45" % (sampleName), 40, 20, 200)
    h_jetThirdHighestPt_pt_passed_3PFCentralJetLooseID45 = ROOT.TH1F("%s__DistributionPassed_3PFCentralJetLooseID45" % (sampleName), "%s__DistributionPassed_3PFCentralJetLooseID45" % (sampleName), 40, 20, 200)
    
    h_jetForthHighestPt_pt_before_4PFCentralJetLooseID35 = ROOT.TH1F("%s__DistributionBefore_4PFCentralJetLooseID35" % (sampleName), "%s__DistributionBefore_4PFCentralJetLooseID35" % (sampleName), 40, 20, 200)
    h_jetForthHighestPt_pt_passed_4PFCentralJetLooseID35 = ROOT.TH1F("%s__DistributionPassed_4PFCentralJetLooseID35" % (sampleName), "%s__DistributionPassed_4PFCentralJetLooseID35" % (sampleName), 40, 20, 200)
    
    varBins = [i for i in range(200, 300+100, 100)] + [i for i in range(300+30, 1500+30, 30)]
    h_pfJetSum_before_PFCentralJetsLooseIDQuad30HT330 = ROOT.TH1F("%s__DistributionBefore_PFCentralJetsLooseIDQuad30HT330" % (sampleName), "%s__DistributionBefore_PFCentralJetsLooseIDQuad30HT330" % (sampleName), len(varBins)-1, array.array("d", varBins))
    h_pfJetSum_passed_PFCentralJetsLooseIDQuad30HT330 = ROOT.TH1F("%s__DistributionPassed_PFCentralJetsLooseIDQuad30HT330" % (sampleName), "%s__DistributionPassed_PFCentralJetsLooseIDQuad30HT330" % (sampleName), len(varBins)-1, array.array("d", varBins))
    
    if (sampleName == "SingleMuon"):
        varBins = [0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.84, 0.88, 0.92, 0.94, 0.96, 1.0]
    else:
        varBins = [0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.54, 0.58, 0.62, 0.66, 0.70, 0.74, 0.78, 0.82, 0.86, 0.90, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99, 1.0] 
    h_jetFirstHighestDeepFlavB_deepFlavB_before_BTagPFDeepJet4p5Triple = ROOT.TH1F("%s__DistributionBefore_BTagPFDeepJet4p5Triple" % (sampleName), "%s__DistributionBefore_BTagPFDeepJet4p5Triple" % (sampleName), len(varBins)-1, array.array("d", varBins))
    h_jetFirstHighestDeepFlavB_deepFlavB_passed_BTagPFDeepJet4p5Triple = ROOT.TH1F("%s__DistributionPassed_BTagPFDeepJet4p5Triple" % (sampleName), "%s__DistributionPassed_BTagPFDeepJet4p5Triple" % (sampleName), len(varBins)-1, array.array("d", varBins))
    
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
        # Filter hltQuadCentralJet30:
        #==========================================================
        if (entry.L1sQuadJetC50to60IorHTT280to500IorHTT250to340QuadJet < 1): continue;
        h_jetForthHighestPt_pt_before_QuadCentralJet30.Fill(entry.jetForthHighestPt_pt)
        if (entry.QuadCentralJet30 < 4): continue
        h_jetForthHighestPt_pt_passed_QuadCentralJet30.Fill(entry.jetForthHighestPt_pt)
        
        #==========================================================
        # Filter hltCaloQuadJet30HT320:
        #==========================================================
        h_caloJetSum_before_CaloQuadJet30HT320.Fill(entry.caloJetSum)
        if (entry.CaloQuadJet30HT320_MaxHT < 320.0): continue
        if (entry.numberOfJetsCaloHT < 4): continue
        h_caloJetSum_passed_CaloQuadJet30HT320.Fill(entry.caloJetSum)
        
        #==========================================================
        # Filter BTagCaloDeepCSVp17Double
        #==========================================================
        h_jetFirstHighestDeepFlavB_deepFlavB_before_BTagCaloDeepCSVp17Double.Fill(entry.jetFirstHighestDeepFlavB_deepFlavB)
        if (entry.BTagCaloDeepCSVp17Double_jetFirstHighestDeepFlavB_triggerFlag == 0): continue
        h_jetFirstHighestDeepFlavB_deepFlavB_passed_BTagCaloDeepCSVp17Double.Fill(entry.jetFirstHighestDeepFlavB_deepFlavB)
        
        #==========================================================
        # Filter PFCentralJetLooseIDQuad30
        #==========================================================
        if (entry.BTagCaloDeepCSVp17Double < 2): continue
        h_jetForthHighestPt_pt_before_PFCentralJetLooseIDQuad30.Fill(entry.jetForthHighestPt_pt)
        if (entry.PFCentralJetLooseIDQuad30 < 4): continue
        h_jetForthHighestPt_pt_passed_PFCentralJetLooseIDQuad30.Fill(entry.jetForthHighestPt_pt)
        
        #========================================================== 
        # Filter 1PFCentralJetLooseID75
        #==========================================================
        h_jetFirstHighestPt_pt_before_1PFCentralJetLooseID75.Fill(entry.jetFirstHighestPt_pt)
        if (entry.OnePFCentralJetLooseID75 == 0): continue
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
        # Filter 4PFCentralJetLooseID35
        #==========================================================
        h_jetForthHighestPt_pt_before_4PFCentralJetLooseID35.Fill(entry.jetForthHighestPt_pt)
        if (entry.FourPFCentralJetLooseID35 < 4): continue
        h_jetForthHighestPt_pt_passed_4PFCentralJetLooseID35.Fill(entry.jetForthHighestPt_pt)

        #==========================================================
        # Filter PFCentralJetsLooseIDQuad30HT330
        #==========================================================
        h_pfJetSum_before_PFCentralJetsLooseIDQuad30HT330.Fill(entry.pfJetSum)
        if (entry.PFCentralJetsLooseIDQuad30HT330_MaxHT < 330): continue
        if (entry.numberOfJetsPfHT < 4): continue
        h_pfJetSum_passed_PFCentralJetsLooseIDQuad30HT330.Fill(entry.pfJetSum)
        
        #==========================================================
        # Filter BTagPFDeepJet4p5Triple
        #==========================================================
        h_jetFirstHighestDeepFlavB_deepFlavB_before_BTagPFDeepJet4p5Triple.Fill(entry.jetFirstHighestDeepFlavB_deepFlavB)
        if (entry.BTagPFDeepJet4p5Triple_jetFirstHighestDeepFlavB_triggerFlag < 1): continue
        h_jetFirstHighestDeepFlavB_deepFlavB_passed_BTagPFDeepJet4p5Triple.Fill(entry.jetFirstHighestDeepFlavB_deepFlavB)
        

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
    
    filterName = "CaloQuadJet30HT320"
    h = ROOT.TGraphAsymmErrors(h_caloJetSum_passed_CaloQuadJet30HT320, h_caloJetSum_before_CaloQuadJet30HT320)
    h.SetTitle("Efficiency %s; #sum p_{T} with p_{T}>30 GeV [GeV]; online efficiency" % (filterName))
    h.SetName("%s__Efficiency_%s" % (sampleName, filterName))
    h.SetLineColor(GetColor(sampleName))
    h.SetMarkerColor(GetColor(sampleName))
    hList.append(h)
    hList.append(h_caloJetSum_before_CaloQuadJet30HT320)
    hList.append(h_caloJetSum_passed_CaloQuadJet30HT320)

    filterName = "BTagCaloDeepCSVp17Double"
    h = ROOT.TGraphAsymmErrors(h_jetFirstHighestDeepFlavB_deepFlavB_passed_BTagCaloDeepCSVp17Double, h_jetFirstHighestDeepFlavB_deepFlavB_before_BTagCaloDeepCSVp17Double)
    h.SetTitle("Efficiency %s; DeepFlavB^{1}; online efficliency" % (filterName))
    h.SetName("%s__Efficiency_%s" % (sampleName, filterName))
    h.SetLineColor(GetColor(sampleName))
    h.SetMarkerColor(GetColor(sampleName))
    hList.append(h)
    hList.append(h_jetFirstHighestDeepFlavB_deepFlavB_before_BTagCaloDeepCSVp17Double)
    hList.append(h_jetFirstHighestDeepFlavB_deepFlavB_passed_BTagCaloDeepCSVp17Double)
    
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
    
    filterName = "4PFCentralJetLooseID35"
    h = ROOT.TGraphAsymmErrors(h_jetForthHighestPt_pt_passed_4PFCentralJetLooseID35, h_jetForthHighestPt_pt_before_4PFCentralJetLooseID35)
    h.SetTitle("Efficiency %s; p_{T}^{4} [GeV]; online efficiency" % (filterName))
    h.SetName("%s__Efficiency_%s" % (sampleName, filterName))
    h.SetLineColor(GetColor(sampleName))
    h.SetMarkerColor(GetColor(sampleName))
    hList.append(h)
    hList.append(h_jetForthHighestPt_pt_before_4PFCentralJetLooseID35)
    hList.append(h_jetForthHighestPt_pt_passed_4PFCentralJetLooseID35)
    
    filterName = "PFCentralJetsLooseIDQuad30HT330"
    h = ROOT.TGraphAsymmErrors(h_pfJetSum_passed_PFCentralJetsLooseIDQuad30HT330, h_pfJetSum_before_PFCentralJetsLooseIDQuad30HT330)
    h.SetTitle("Efficiency %s; PF #sum p_{T} with p_{T}>30 GeV [GeV]; online efficiency" % (filterName))
    h.SetName("%s__Efficiency_%s" % (sampleName, filterName))
    h.SetLineColor(GetColor(sampleName))
    h.SetMarkerColor(GetColor(sampleName))
    hList.append(h)
    hList.append(h_pfJetSum_before_PFCentralJetsLooseIDQuad30HT330)
    hList.append(h_pfJetSum_passed_PFCentralJetsLooseIDQuad30HT330)
    
    filterName = "BTagPFDeepJet4p5Triple"
    h = ROOT.TGraphAsymmErrors(h_jetFirstHighestDeepFlavB_deepFlavB_passed_BTagPFDeepJet4p5Triple, h_jetFirstHighestDeepFlavB_deepFlavB_before_BTagPFDeepJet4p5Triple)
    h.SetTitle("Efficiency %s; PF DeepFlavB^{1}; online efficliency" % (filterName))
    h.SetName("%s__Efficiency_%s" % (sampleName, filterName))
    h.SetLineColor(GetColor(sampleName))
    h.SetMarkerColor(GetColor(sampleName))
    hList.append(h)
    hList.append(h_jetFirstHighestDeepFlavB_deepFlavB_before_BTagPFDeepJet4p5Triple)
    hList.append(h_jetFirstHighestDeepFlavB_deepFlavB_passed_BTagPFDeepJet4p5Triple)
    return hList
    

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def main(args):
    
    if args.year == "2022":
        fData = ROOT.TFile.Open(args.dirName+"/MuonEG_2022G_PromptNanoAODv11_05May2023.root")
        fTTbar = None
    
    hDataList = []
    if args.year == "2022":
        hDataList = GetPNetEfficiencies22(fData, "MuonEG")


    # Save into the output file
    fOutput = ROOT.TFile.Open(args.output, "RECREATE")
    for h in hDataList:
        h.Write()
        
    fOutput.Close()
    return

    f = ROOT.TFile.Open(args.rfile, "READ")
    Filters = ["L1filterHT",
               "QuadCentralJet30",
               "CaloQuadJet30HT320",
               "BTagCaloDeepCSVp17Double",
               "PFCentralJetLooseIDQuad30",
               "1PFCentralJetLooseID75",
               "2PFCentralJetLooseID60",
               "3PFCentralJetLooseID45",
               "4PFCentralJetLooseID35",
               "PFCentralJetsLooseIDQuad30HT330",
               "BTagPFDeepCSV4p5Triple"]
        
    for filt in Filters:
        hData_Eff   = f.Get("SingleMuon__Efficiency_%s" % (filt))
        hTT_Eff     = f.Get("TTbar__Efficiency_%s" %(filt))
        hSignal_Eff = f.Get("NMSSM__Efficiency_%s" %(filt))
    
        plotComparison("Efficiency_%s" % (filt), hData_Eff, [hTT_Eff, hSignal_Eff])
    return


if __name__ == "__main__":

    # Default values
    VERBOSE       = True
    YEAR          = "2018"
    OUTPUT        = "TriggerEfficiencyPerLeg_05May2023"
    DIRNAME       = "root://cmseos.fnal.gov//store/user/mkolosov/HHHTo6B/TriggerStudies/Summer2018UL_TRGcurves_wTrgMatching_14Dec2022_4bCode"
    REDIRECTOR    = "root://cmseos.fnal.gov/"
    FORMATS       = [".png", ".pdf", ".C"]
    SAVEPATH      = getPublicPath()
    STUDY         = "TriggerEfficiencyByFilter_wTrgMatching"
    
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

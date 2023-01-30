#!/usr/bin/env python
'''
 USAGE:


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

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def main(args):
    
    samples = {"GluGluToHHTo4B_node_cHHH0"    : args.dirName+"/GluGluToHHTo4B_node_cHHH0_TuneCP5_PSWeights_13TeV-powheg-pythia8/ntuple.root",
               "GluGluToHHTo4B_node_cHHH1"    : args.dirName+"/GluGluToHHTo4B_node_cHHH1_TuneCP5_PSWeights_13TeV-powheg-pythia8/ntuple.root",
               "GluGluToHHTo4B_node_cHHH2p45" : args.dirName+"/GluGluToHHTo4B_node_cHHH2p45_TuneCP5_PSWeights_13TeV-powheg-pythia8/ntuple.root",
               "GluGluToHHTo4B_node_cHHH5"    : args.dirName+"/GluGluToHHTo4B_node_cHHH5_TuneCP5_PSWeights_13TeV-powheg-pythia8/ntuple.root"}
    
    fOut = ROOT.TFile.Open("histogramsForHHTo4b_17Jan2023.root", "RECREATE")
    
    for sample in samples:
        
        f = ROOT.TFile.Open(samples[sample])
        t = f.Get("sixBtree")
        
        direc = fOut.mkdir(sample)
        direc.cd()
        
        entries = t.GetEntries()
        
        # Define histograms

        #-----------------------------------------------------------------------------------------------------------
        # Histograms before any matching or categorization
        #-----------------------------------------------------------------------------------------------------------
        h_GenPart_H1_pt  = ROOT.TH1F("h_GenPart_H1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        h_GenPart_H2_pt  = ROOT.TH1F("h_GenPart_H2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        h_GenPart_H1_eta = ROOT.TH1F("h_GenPart_H1_eta", ";#eta;Events", 120, -4.0, 4.0)
        h_GenPart_H2_eta = ROOT.TH1F("h_GenPart_H2_eta", ";#eta;Events", 120, -4.0, 4.0)
                
        h_GenPart_H1_b1_eta = ROOT.TH1F("h_GenPart_H1_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        h_GenPart_H1_b2_eta = ROOT.TH1F("h_GenPart_H1_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
        h_GenPart_H2_b1_eta = ROOT.TH1F("h_GenPart_H2_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        h_GenPart_H2_b2_eta = ROOT.TH1F("h_GenPart_H2_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
        
        h_GenPart_H1_b1_pt = ROOT.TH1F("h_GenPart_H1_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        h_GenPart_H1_b2_pt = ROOT.TH1F("h_GenPart_H1_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        h_GenPart_H2_b1_pt = ROOT.TH1F("h_GenPart_H2_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        h_GenPart_H2_b2_pt = ROOT.TH1F("h_GenPart_H2_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        
        h_NJets = ROOT.TH1I("h_NJets", ";jets multiplicity;Events", 15, 0, 15)
        h_Jet1Pt = ROOT.TH1F("h_Jet1Pt", ";Jet 1 p_{T} [GeV];Events", 100, 0.0, 500)
        h_Jet2Pt = ROOT.TH1F("h_Jet2Pt", ";Jet 2 p_{T} [GeV];Events", 100, 0.0, 500)
        h_Jet3Pt = ROOT.TH1F("h_Jet3Pt", ";Jet 3 p_{T} [GeV];Events", 100, 0.0, 500)
        h_Jet4Pt = ROOT.TH1F("h_Jet4Pt", ";Jet 4 p_{T} [GeV];Events", 100, 0.0, 500)
        h_NLooseBJets  = ROOT.TH1I("h_NLooseBJets", ";loose b-jets multiplicity;Events", 10, 0, 10)
        h_NMediumBJets = ROOT.TH1I("h_NMediumBJets", ";medium b-jets multiplicity;Events", 10, 0, 10)
        h_NTightBJets  = ROOT.TH1I("h_NTightBJets", ";tight b-jets multiplicity;Events", 10, 0, 10)
        h_NFatJets = ROOT.TH1I("h_NFatJets", ";fatjet multiplicity;Events", 10, 0, 10)
        h_AK8Jet1Pt = ROOT.TH1F("h_AK8Jet1Pt", "; fatjet 1 p_{T} [GeV];Events", 200, 0.0, 1000)
        h_AK8Jet2Pt = ROOT.TH1F("h_AK8Jet2Pt", "; fatjet 2 p_{T} [GeV];Events", 200, 0.0, 1000)
        h_AK8Jet3Pt = ROOT.TH1F("h_AK8Jet3Pt", "; fatjet 3 p_{T} [GeV];Events", 200, 0.0, 1000)
        h_AK8Jet4Pt = ROOT.TH1F("h_AK8Jet4Pt", "; fatjet 4 p_{T} [GeV];Events", 200, 0.0, 1000)
        
        h2D_NBQuarksMatchedTo_GenJetsVsGenFatJets = ROOT.TH2I("h2D_NBQuarksMatchedTo_GenJetsVsGenFatJets", ";b-quarks matched to gen-jets;b-quarks matched to gen-fatjets", 5, 0, 5, 5, 0, 5)
        h2D_NBQuarksMatchedTo_RecoJetsVsRecoFatJets = ROOT.TH2I("h2D_NBQuarksMatchedTo_RecoJetsVsRecoFatJets", ";b-quarks matched to reco-jets;b-quarks matched to reco-fatjets", 5, 0, 5, 5, 0, 5)
    
        h2D_NBQuarksMatchedTo_RecoJetsVsCategory = ROOT.TH2I("h2D_NBQuarksMatchedTo_RecoJetsVsCategory", ";b-quarks matched to reco-jets;category", 5, 0, 5, 3, 0, 3)
        h2D_NBQuarksMatchedTo_RecoJetsVsCategory.GetYaxis().SetBinLabel(1, "resolved")
        h2D_NBQuarksMatchedTo_RecoJetsVsCategory.GetYaxis().SetBinLabel(2, "semi-resolved")
        h2D_NBQuarksMatchedTo_RecoJetsVsCategory.GetYaxis().SetBinLabel(3, "boosted")
        
        h2D_NBQuarksMatchedTo_RecoFatJetsVsCategory = ROOT.TH2I("h2D_NBQuarksMatchedTo_RecoFatJetsVsCategory", ";b-quarks matched to reco-fatjets", 5, 0, 5, 3, 0, 3)
        h2D_NBQuarksMatchedTo_RecoFatJetsVsCategory.GetYaxis().SetBinLabel(1, "resolved")
        h2D_NBQuarksMatchedTo_RecoFatJetsVsCategory.GetYaxis().SetBinLabel(2, "semi-resolved")
        h2D_NBQuarksMatchedTo_RecoFatJetsVsCategory.GetYaxis().SetBinLabel(3, "boosted")
        
        h_GenMatchingTo4GenJets_Cases = ROOT.TH1I("h_GenMatchingTo4GenJets_Cases", ";cases;Events", 14, 1, 15)
        h_GenMatchingTo4RecoJets_Cases = ROOT.TH1I("h_GenMatchingTo4RecoJets_Cases", ";cases;Events", 14, 1, 15)
        
        #-----------------------------------------------------------------------------------------------------------
        h_IsBoostedGen_GenFatJet_H1_pt= ROOT.TH1F("h_IsBoostedGen_GenFatJet_H1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        h_IsBoostedGen_GenFatJet_H2_pt= ROOT.TH1F("h_IsBoostedGen_GenFatJet_H2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        h_IsSemiresolvedGen_GenFatJet_H1_pt = ROOT.TH1F("h_IsSemiresolvedGen_GenFatJet_H1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        h_IsSemiresolvedGen_GenFatJet_H2_pt = ROOT.TH1F("h_IsSemiresolvedGen_GenFatJet_H2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        h_GenFatJet_H1_pt = ROOT.TH1F("h_GenFatJet_H1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        h_GenFatJet_H2_pt = ROOT.TH1F("h_GenFatJet_H2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        
        h_IsBoostedGen_NotBoostedReco_GenFatJet_H1_pt = ROOT.TH1F("h_IsBoostedGen_NotBoostedReco_GenFatJet_H1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        h_IsBoostedGen_NotBoostedReco_GenFatJet_H2_pt = ROOT.TH1F("h_IsBoostedGen_NotBoostedReco_GenFatJet_H2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        h_IsSemiresolvedGen_NotSemiresolvedReco_GenFatJet_H1_pt = ROOT.TH1F("h_IsSemiresolvedGen_NotSemiresolvedReco_GenFatJet_H1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        h_IsSemiresolvedGen_NotSemiresolvedReco_GenFatJet_H2_pt = ROOT.TH1F("h_IsSemiresolvedGen_NotSemiresolvedReco_GenFatJet_H2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
                
        #-----------------------------------------------------------------------------------------------------------
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
        
        hResolved_GenJet_H1_b1_pt  = ROOT.TH1F("hResolved_GenJet_H1_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolved_GenJet_H1_b2_pt  = ROOT.TH1F("hResolved_GenJet_H1_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolved_GenJet_H2_b1_pt  = ROOT.TH1F("hResolved_GenJet_H2_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolved_GenJet_H2_b2_pt  = ROOT.TH1F("hResolved_GenJet_H2_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolved_GenJet_H1_b1_eta = ROOT.TH1F("hResolved_GenJet_H1_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hResolved_GenJet_H1_b2_eta = ROOT.TH1F("hResolved_GenJet_H1_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hResolved_GenJet_H2_b1_eta = ROOT.TH1F("hResolved_GenJet_H2_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hResolved_GenJet_H2_b2_eta = ROOT.TH1F("hResolved_GenJet_H2_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
        
        hResolved_RecoJet_H1_b1_pt  = ROOT.TH1F("hResolved_RecoJet_H1_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolved_RecoJet_H1_b2_pt  = ROOT.TH1F("hResolved_RecoJet_H1_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolved_RecoJet_H2_b1_pt  = ROOT.TH1F("hResolved_RecoJet_H2_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolved_RecoJet_H2_b2_pt  = ROOT.TH1F("hResolved_RecoJet_H2_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolved_RecoJet_H1_b1_eta = ROOT.TH1F("hResolved_RecoJet_H1_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hResolved_RecoJet_H1_b2_eta = ROOT.TH1F("hResolved_RecoJet_H1_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hResolved_RecoJet_H2_b1_eta = ROOT.TH1F("hResolved_RecoJet_H2_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hResolved_RecoJet_H2_b2_eta = ROOT.TH1F("hResolved_RecoJet_H2_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
        
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
        hResolved_RecoJet_AK8Jet2Pt = ROOT.TH1F("hResolved_RecoJet_AK8Jet2Pt", "; fatjet 2 p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolved_RecoJet_AK8Jet3Pt = ROOT.TH1F("hResolved_RecoJet_AK8Jet3Pt", "; fatjet 3 p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolved_RecoJet_AK8Jet4Pt = ROOT.TH1F("hResolved_RecoJet_AK8Jet4Pt", "; fatjet 4 p_{T} [GeV];Events", 200, 0.0, 1000)
        # Case 10
        hResolvedCase10_GenPart_H1_pt = ROOT.TH1F("hResolvedCase10_GenPart_H1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase10_GenPart_H2_pt = ROOT.TH1F("hResolvedCase10_GenPart_H2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase10_GenPart_H1_b1_pt = ROOT.TH1F("hResolvedCase10_GenPart_H1_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase10_GenPart_H1_b2_pt = ROOT.TH1F("hResolvedCase10_GenPart_H1_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase10_GenPart_H2_b1_pt = ROOT.TH1F("hResolvedCase10_GenPart_H2_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase10_GenPart_H2_b2_pt = ROOT.TH1F("hResolvedCase10_GenPart_H2_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase10_RecoJet_H1_b1_pt = ROOT.TH1F("hResolvedCase10_RecoJet_H1_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase10_RecoJet_H1_b2_pt = ROOT.TH1F("hResolvedCase10_RecoJet_H1_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase10_RecoJet_H2_b1_pt = ROOT.TH1F("hResolvedCase10_RecoJet_H2_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase10_RecoJet_H2_b2_pt = ROOT.TH1F("hResolvedCase10_RecoJet_H2_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase10_RecoJet_H1_pt = ROOT.TH1F("hResolvedCase10_RecoJet_H1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase10_RecoJet_H2_pt = ROOT.TH1F("hResolvedCase10_RecoJet_H2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase10_RecoJet_InvMass_H1 = ROOT.TH1F("hResolvedCase10_RecoJet_InvMass_H1", ";m_{H} [GeV]", 300, 0, 300)
        hResolvedCase10_RecoJet_InvMass_H2 = ROOT.TH1F("hResolvedCase10_RecoJet_InvMass_H2", ";m_{H} [GeV]", 300, 0, 300)
        hResolvedCase10_RecoJet_NJets = ROOT.TH1F("hResolvedCase10_RecoJet_NJets", "; jet multiplicity;Events", 15, 0, 15)
        hResolvedCase10_RecoJet_NFatJets = ROOT.TH1F("hResolvedCase10_RecoJet_NFatJets", "; fatjet multiplicity;Events", 15, 0, 15)
        hResolvedCase10_RecoFatJet_H1_pt = ROOT.TH1F("hResolvedCase10_RecoFatJet_H1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase10_RecoFatJet_H2_pt = ROOT.TH1F("hResolvedCase10_RecoFatJet_H2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase10_RecoFatJet_H1_m = ROOT.TH1F("hResolvedCase10_RecoFatJet_H1_m", ";m_{H} [GeV]", 300, 0, 300)
        hResolvedCase10_RecoFatJet_H2_m = ROOT.TH1F("hResolvedCase10_RecoFatJet_H2_m", ";m_{H} [GeV]", 300, 0, 300)
        hResolvedCase10_RecoJet_AK8Jet1Pt = ROOT.TH1F("hResolvedCase10_RecoJet_AK8Jet1Pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase10_RecoJet_AK8Jet2Pt = ROOT.TH1F("hResolvedCase10_RecoJet_AK8Jet2Pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase10_RecoJet_AK8Jet3Pt = ROOT.TH1F("hResolvedCase10_RecoJet_AK8Jet3Pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase10_RecoJet_AK8Jet4Pt = ROOT.TH1F("hResolvedCase10_RecoJet_AK8Jet4Pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        # Case 1
        hResolvedCase1_GenPart_H1_pt = ROOT.TH1F("hResolvedCase1_GenPart_H1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase1_GenPart_H2_pt = ROOT.TH1F("hResolvedCase1_GenPart_H2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase1_GenPart_H1_b1_pt = ROOT.TH1F("hResolvedCase1_GenPart_H1_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase1_GenPart_H1_b2_pt = ROOT.TH1F("hResolvedCase1_GenPart_H1_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase1_GenPart_H2_b1_pt = ROOT.TH1F("hResolvedCase1_GenPart_H2_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase1_GenPart_H2_b2_pt = ROOT.TH1F("hResolvedCase1_GenPart_H2_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase1_RecoJet_H1_b1_pt = ROOT.TH1F("hResolvedCase1_RecoJet_H1_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase1_RecoJet_H1_b2_pt = ROOT.TH1F("hResolvedCase1_RecoJet_H1_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase1_RecoJet_H2_b1_pt = ROOT.TH1F("hResolvedCase1_RecoJet_H2_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase1_RecoJet_H2_b2_pt = ROOT.TH1F("hResolvedCase1_RecoJet_H2_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase1_RecoJet_H1_pt = ROOT.TH1F("hResolvedCase1_RecoJet_H1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase1_RecoJet_H2_pt = ROOT.TH1F("hResolvedCase1_RecoJet_H2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase1_RecoJet_InvMass_H1 = ROOT.TH1F("hResolvedCase1_RecoJet_InvMass_H1", ";m_{H} [GeV]", 300, 0, 300)
        hResolvedCase1_RecoJet_InvMass_H2 = ROOT.TH1F("hResolvedCase1_RecoJet_InvMass_H2", ";m_{H} [GeV]", 300, 0, 300)
        hResolvedCase1_RecoJet_NJets      = ROOT.TH1F("hResolvedCase1_RecoJet_NJets", "; jet multiplicity;Events", 15, 0, 15)
        hResolvedCase1_RecoJet_NFatJets   = ROOT.TH1F("hResolvedCase1_RecoJet_NFatJets", "; fatjet multiplicity;Events", 15, 0, 15)
        hResolvedCase1_RecoJet_AK8Jet1Pt  = ROOT.TH1F("hResolvedCase1_RecoJet_AK8Jet1Pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase1_RecoJet_AK8Jet2Pt  = ROOT.TH1F("hResolvedCase1_RecoJet_AK8Jet2Pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase1_RecoJet_AK8Jet3Pt  = ROOT.TH1F("hResolvedCase1_RecoJet_AK8Jet3Pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase1_RecoJet_AK8Jet4Pt  = ROOT.TH1F("hResolvedCase1_RecoJet_AK8Jet4Pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        # Case 6
        hResolvedCase6_GenPart_H1_pt = ROOT.TH1F("hResolvedCase6_GenPart_H1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase6_GenPart_H2_pt = ROOT.TH1F("hResolvedCase6_GenPart_H2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase6_GenPart_H1_b1_pt = ROOT.TH1F("hResolvedCase6_GenPart_H1_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase6_GenPart_H1_b2_pt = ROOT.TH1F("hResolvedCase6_GenPart_H1_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase6_GenPart_H2_b1_pt = ROOT.TH1F("hResolvedCase6_GenPart_H2_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase6_GenPart_H2_b2_pt = ROOT.TH1F("hResolvedCase6_GenPart_H2_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase6_RecoJet_H1_b1_pt = ROOT.TH1F("hResolvedCase6_RecoJet_H1_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase6_RecoJet_H1_b2_pt = ROOT.TH1F("hResolvedCase6_RecoJet_H1_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase6_RecoJet_H2_b1_pt = ROOT.TH1F("hResolvedCase6_RecoJet_H2_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase6_RecoJet_H2_b2_pt = ROOT.TH1F("hResolvedCase6_RecoJet_H2_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase6_RecoJet_H1_pt = ROOT.TH1F("hResolvedCase6_RecoJet_H1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase6_RecoJet_H2_pt = ROOT.TH1F("hResolvedCase6_RecoJet_H2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase6_RecoJet_InvMass_H1 = ROOT.TH1F("hResolvedCase6_RecoJet_InvMass_H1", ";m_{H} [GeV]", 300, 0, 300)
        hResolvedCase6_RecoJet_InvMass_H2 = ROOT.TH1F("hResolvedCase6_RecoJet_InvMass_H2", ";m_{H} [GeV]", 300, 0, 300)
        hResolvedCase6_RecoJet_NJets      = ROOT.TH1F("hResolvedCase6_RecoJet_NJets", "; jet multiplicity;Events", 15, 0, 15)
        hResolvedCase6_RecoJet_NFatJets   = ROOT.TH1F("hResolvedCase6_RecoJet_NFatJets", "; fatjet multiplicity;Events", 15, 0, 15)
        hResolvedCase6_RecoFatJet_H1_pt   = ROOT.TH1F("hResolvedCase6_RecoFatJet_H1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase6_RecoJet_AK8Jet1Pt  = ROOT.TH1F("hResolvedCase6_RecoJet_AK8Jet1Pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase6_RecoJet_AK8Jet2Pt  = ROOT.TH1F("hResolvedCase6_RecoJet_AK8Jet2Pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase6_RecoJet_AK8Jet3Pt  = ROOT.TH1F("hResolvedCase6_RecoJet_AK8Jet3Pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase6_RecoJet_AK8Jet4Pt  = ROOT.TH1F("hResolvedCase6_RecoJet_AK8Jet4Pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        # Case 13
        hResolvedCase13_GenPart_H1_pt = ROOT.TH1F("hResolvedCase13_GenPart_H1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase13_GenPart_H2_pt = ROOT.TH1F("hResolvedCase13_GenPart_H2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase13_GenPart_H1_b1_pt = ROOT.TH1F("hResolvedCase13_GenPart_H1_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase13_GenPart_H1_b2_pt = ROOT.TH1F("hResolvedCase13_GenPart_H1_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase13_GenPart_H2_b1_pt = ROOT.TH1F("hResolvedCase13_GenPart_H2_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase13_GenPart_H2_b2_pt = ROOT.TH1F("hResolvedCase13_GenPart_H2_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase13_RecoJet_H1_b1_pt = ROOT.TH1F("hResolvedCase13_RecoJet_H1_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase13_RecoJet_H1_b2_pt = ROOT.TH1F("hResolvedCase13_RecoJet_H1_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase13_RecoJet_H2_b1_pt = ROOT.TH1F("hResolvedCase13_RecoJet_H2_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase13_RecoJet_H2_b2_pt = ROOT.TH1F("hResolvedCase13_RecoJet_H2_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase13_RecoJet_H1_pt = ROOT.TH1F("hResolvedCase13_RecoJet_H1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase13_RecoJet_H2_pt = ROOT.TH1F("hResolvedCase13_RecoJet_H2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase13_RecoJet_InvMass_H1 = ROOT.TH1F("hResolvedCase13_RecoJet_InvMass_H1", ";m_{H} [GeV]", 300, 0, 300)
        hResolvedCase13_RecoJet_InvMass_H2 = ROOT.TH1F("hResolvedCase13_RecoJet_InvMass_H2", ";m_{H} [GeV]", 300, 0, 300)
        hResolvedCase13_RecoJet_NJets      = ROOT.TH1F("hResolvedCase13_RecoJet_NJets", "; jet multiplicity;Events", 15, 0, 15)
        hResolvedCase13_RecoJet_NFatJets   = ROOT.TH1F("hResolvedCase13_RecoJet_NFatJets", "; fatjet multiplicity;Events", 15, 0, 15)
        hResolvedCase13_RecoFatJet_H1_pt   = ROOT.TH1F("hResolvedCase13_RecoFatJet_H1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase13_RecoJet_AK8Jet1Pt  = ROOT.TH1F("hResolvedCase13_RecoJet_AK8Jet1Pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase13_RecoJet_AK8Jet2Pt  = ROOT.TH1F("hResolvedCase13_RecoJet_AK8Jet2Pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase13_RecoJet_AK8Jet3Pt  = ROOT.TH1F("hResolvedCase13_RecoJet_AK8Jet3Pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase13_RecoJet_AK8Jet4Pt  = ROOT.TH1F("hResolvedCase13_RecoJet_AK8Jet4Pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        # Case 7
        hResolvedCase7_GenPart_H1_pt = ROOT.TH1F("hResolvedCase7_GenPart_H1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase7_GenPart_H2_pt = ROOT.TH1F("hResolvedCase7_GenPart_H2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase7_GenPart_H1_b1_pt = ROOT.TH1F("hResolvedCase7_GenPart_H1_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase7_GenPart_H1_b2_pt = ROOT.TH1F("hResolvedCase7_GenPart_H1_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase7_GenPart_H2_b1_pt = ROOT.TH1F("hResolvedCase7_GenPart_H2_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase7_GenPart_H2_b2_pt = ROOT.TH1F("hResolvedCase7_GenPart_H2_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase7_RecoJet_H1_b1_pt = ROOT.TH1F("hResolvedCase7_RecoJet_H1_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase7_RecoJet_H1_b2_pt = ROOT.TH1F("hResolvedCase7_RecoJet_H1_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase7_RecoJet_H2_b1_pt = ROOT.TH1F("hResolvedCase7_RecoJet_H2_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase7_RecoJet_H2_b2_pt = ROOT.TH1F("hResolvedCase7_RecoJet_H2_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase7_RecoJet_H1_pt = ROOT.TH1F("hResolvedCase7_RecoJet_H1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase7_RecoJet_H2_pt = ROOT.TH1F("hResolvedCase7_RecoJet_H2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase7_RecoJet_InvMass_H1 = ROOT.TH1F("hResolvedCase7_RecoJet_InvMass_H1", ";m_{H} [GeV]", 300, 0, 300)
        hResolvedCase7_RecoJet_InvMass_H2 = ROOT.TH1F("hResolvedCase7_RecoJet_InvMass_H2", ";m_{H} [GeV]", 300, 0, 300)
        hResolvedCase7_RecoJet_NJets      = ROOT.TH1F("hResolvedCase7_RecoJet_NJets", "; jet multiplicity;Events", 15, 0, 15)
        hResolvedCase7_RecoJet_NFatJets   = ROOT.TH1F("hResolvedCase7_RecoJet_NFatJets", "; fatjet multiplicity;Events", 15, 0, 15)
        hResolvedCase7_RecoFatJet_H1_pt   = ROOT.TH1F("hResolvedCase7_RecoFatJet_H1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase7_RecoJet_AK8Jet1Pt  = ROOT.TH1F("hResolvedCase7_RecoJet_AK8Jet1Pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase7_RecoJet_AK8Jet2Pt  = ROOT.TH1F("hResolvedCase7_RecoJet_AK8Jet2Pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase7_RecoJet_AK8Jet3Pt  = ROOT.TH1F("hResolvedCase7_RecoJet_AK8Jet3Pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedCase7_RecoJet_AK8Jet4Pt  = ROOT.TH1F("hResolvedCase7_RecoJet_AK8Jet4Pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        
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
        
        hResolvedExcl_GenJet_H1_b1_pt  = ROOT.TH1F("hResolvedExcl_GenJet_H1_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedExcl_GenJet_H1_b2_pt  = ROOT.TH1F("hResolvedExcl_GenJet_H1_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedExcl_GenJet_H2_b1_pt  = ROOT.TH1F("hResolvedExcl_GenJet_H2_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedExcl_GenJet_H2_b2_pt  = ROOT.TH1F("hResolvedExcl_GenJet_H2_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedExcl_GenJet_H1_b1_eta = ROOT.TH1F("hResolvedExcl_GenJet_H1_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hResolvedExcl_GenJet_H1_b2_eta = ROOT.TH1F("hResolvedExcl_GenJet_H1_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hResolvedExcl_GenJet_H2_b1_eta = ROOT.TH1F("hResolvedExcl_GenJet_H2_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hResolvedExcl_GenJet_H2_b2_eta = ROOT.TH1F("hResolvedExcl_GenJet_H2_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
        
        hResolvedExcl_RecoJet_H1_b1_pt  = ROOT.TH1F("hResolvedExcl_RecoJet_H1_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedExcl_RecoJet_H1_b2_pt  = ROOT.TH1F("hResolvedExcl_RecoJet_H1_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedExcl_RecoJet_H2_b1_pt  = ROOT.TH1F("hResolvedExcl_RecoJet_H2_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedExcl_RecoJet_H2_b2_pt  = ROOT.TH1F("hResolvedExcl_RecoJet_H2_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hResolvedExcl_RecoJet_H1_b1_eta = ROOT.TH1F("hResolvedExcl_RecoJet_H1_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hResolvedExcl_RecoJet_H1_b2_eta = ROOT.TH1F("hResolvedExcl_RecoJet_H1_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hResolvedExcl_RecoJet_H2_b1_eta = ROOT.TH1F("hResolvedExcl_RecoJet_H2_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hResolvedExcl_RecoJet_H2_b2_eta = ROOT.TH1F("hResolvedExcl_RecoJet_H2_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
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
        hBoosted_GenFatJet_H1_pt  = ROOT.TH1F("hBoosted_GenFatJet_H1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hBoosted_GenFatJet_H2_pt  = ROOT.TH1F("hBoosted_GenFatJet_H2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hBoosted_GenFatJet_H1_eta = ROOT.TH1F("hBoosted_GenFatJet_H1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hBoosted_GenFatJet_H2_eta = ROOT.TH1F("hBoosted_GenFatJet_H2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hBoosted_RecoFatJet_H1_pt  = ROOT.TH1F("hBoosted_RecoFatJet_H1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hBoosted_RecoFatJet_H2_pt  = ROOT.TH1F("hBoosted_RecoFatJet_H2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hBoosted_RecoFatJet_H1_eta = ROOT.TH1F("hBoosted_RecoFatJet_H1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hBoosted_RecoFatJet_H2_eta = ROOT.TH1F("hBoosted_RecoFatJet_H2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hBoosted_RecoFatJet_H1_TXbb = ROOT.TH1F("hBoosted_RecoFatJet_H1_TXbb", ";T_{Xbb} score;Events", 100, 0.0, 1.0)
        hBoosted_RecoFatJet_H2_TXbb = ROOT.TH1F("hBoosted_RecoFatJet_H2_TXbb", ";T_{Xbb} score;Events", 100, 0.0, 1.0)
        hBoosted_RecoFatJet_H1_m = ROOT.TH1F("hBoosted_RecoFatJet_H1_m", ";M [GeV];Events", 300, 0.0, 300)
        hBoosted_RecoFatJet_H2_m = ROOT.TH1F("hBoosted_RecoFatJet_H2_m", ";M [GeV];Events", 300, 0.0, 300)
        hBoosted_NJets = ROOT.TH1I("hBoosted_NJets", ";jets multiplicity;Events", 15, 0, 15)
        hBoosted_NFatJets = ROOT.TH1I("hBoosted_NFatJets", ";fatjets multiplicity;Events", 10, 0, 10)
        hBoosted_AK8PFHT = ROOT.TH1F("hBoosted_AK8PFHT", ";AK8 PF H_{T} [GeV];Events", 200, 0.0, 2000)
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
        hBoosted_RecoFatJet_H1_subjet1_m = ROOT.TH1F("hBoosted_RecoFatJet_H1_subjet1_m", ";subjet 1 M [GeV];Events", 200, 0.0, 800)
        hBoosted_RecoFatJet_H1_subjet1_btag = ROOT.TH1F("hBoosted_RecoFatJet_H1_subjet1_btag", ";subjet 1 b-discriminator;Events", 100, 0.0, 1.0)
        hBoosted_RecoFatJet_H1_subjet2_pt = ROOT.TH1F("hBoosted_RecoFatJet_H1_subjet2_pt", ";subjet 2 p_{T} [GeV];Events", 200, 0.0, 800)
        hBoosted_RecoFatJet_H1_subjet2_eta = ROOT.TH1F("hBoosted_RecoFatJet_H1_subjet2_eta", ";subjet 2 #eta;Events", 120, -4.0, 4.0)
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
        hBoosted_RecoFatJet_H2_subjet1_m = ROOT.TH1F("hBoosted_RecoFatJet_H2_subjet1_m", ";subjet 1 M [GeV];Events", 200, 0.0, 800)
        hBoosted_RecoFatJet_H2_subjet1_btag = ROOT.TH1F("hBoosted_RecoFatJet_H2_subjet1_btag", ";subjet 1 b-discriminator;Events", 100, 0.0, 1.0)
        hBoosted_RecoFatJet_H2_subjet2_pt = ROOT.TH1F("hBoosted_RecoFatJet_H2_subjet2_pt", ";subjet 2 p_{T} [GeV];Events", 200, 0.0, 800)
        hBoosted_RecoFatJet_H2_subjet2_eta = ROOT.TH1F("hBoosted_RecoFatJet_H2_subjet2_eta", ";subjet 2 #eta;Events", 120, -4.0, 4.0)
        hBoosted_RecoFatJet_H2_subjet2_m = ROOT.TH1F("hBoosted_RecoFatJet_H2_subjet2_m", ";subjet 2 M [GeV];Events", 200, 0.0, 800)
        hBoosted_RecoFatJet_H2_subjet2_btag = ROOT.TH1F("hBoosted_RecoFatJet_H2_subjet2_btag", ";subjet 2 b-discriminator;Events", 100, 0.0, 1.0)
        
        #=========================================================================================================================================================================
        hResolved_MatchedToTwoFatJets_DR_RecoFatJetH1_RecoFatJetH2 = ROOT.TH1F("hResolved_MatchedToTwoFatJets_DR_RecoFatJetH1_RecoFatJetH2", ";#Delta R;Events", 100, 0.0, 5.0)
        hResolved_MatchedToTwoFatJets_DR_RecoFatJetH1_b11 = ROOT.TH1F("hResolved_MatchedToTwoFatJets_DR_RecoFatJetH1_b11", ";#Delta R;Events", 100, 0.0, 5.0)
        hResolved_MatchedToTwoFatJets_DR_RecoFatJetH1_b12 = ROOT.TH1F("hResolved_MatchedToTwoFatJets_DR_RecoFatJetH1_b12", ";#Delta R;Events", 100, 0.0, 5.0)
        hResolved_MatchedToTwoFatJets_DR_b11_b12 = ROOT.TH1F("hResolved_MatchedToTwoFatJets_DR_b11_b12", ";#Delta R;Events", 100, 0.0, 5.0)
        hResolved_MatchedToTwoFatJets_DR_RecoFatJetH2_b21 = ROOT.TH1F("hResolved_MatchedToTwoFatJets_DR_RecoFatJetH2_b21", ";#Delta R;Events", 100, 0.0, 5.0)
        hResolved_MatchedToTwoFatJets_DR_RecoFatJetH2_b22 = ROOT.TH1F("hResolved_MatchedToTwoFatJets_DR_RecoFatJetH2_b22", ";#Delta R;Events", 100, 0.0, 5.0)
        hResolved_MatchedToTwoFatJets_DR_b21_b22 = ROOT.TH1F("hResolved_MatchedToTwoFatJets_DR_b21_b22", ";#Delta R;Events", 100, 0.0, 5.0)
        
        hResolved_MatchedToOneFatJet_DR_RecoFatJetH1_RecoH2 = ROOT.TH1F("hResolved_MatchedToOneFatJet_DR_RecoFatJetH1_RecoH2", ";#Delta R;Events", 100, 0.0, 5.0)
        hResolved_MatchedToOneFatJet_DR_RecoFatJetH1_b11    = ROOT.TH1F("hResolved_MatchedToOneFatJet_DR_RecoFatJetH1_b11", ";#Delta R;Events", 100, 0.0, 5.0)
        hResolved_MatchedToOneFatJet_DR_RecoFatJetH1_b12    = ROOT.TH1F("hResolved_MatchedToOneFatJet_DR_RecoFatJetH1_b12", ";#Delta R;Events", 100, 0.0, 5.0)
        hResolved_MatchedToOneFatJet_DR_b11_b12 = ROOT.TH1F("hResolved_MatchedToOneFatJet_DR_b11_b12", ";#Delta R;Events", 100, 0.0, 5.0)
        hResolved_MatchedToOneFatJet_DR_RecoH2_b21 = ROOT.TH1F("hResolved_MatchedToOneFatJet_DR_RecoH2_b21", ";#Delta R;Events", 100, 0.0, 5.0)
        hResolved_MatchedToOneFatJet_DR_RecoH2_b22 = ROOT.TH1F("hResolved_MatchedToOneFatJet_DR_RecoH2_b22", ";#Delta R;Events", 100, 0.0, 5.0)
        hResolved_MatchedToOneFatJet_DR_b21_b22 = ROOT.TH1F("hResolved_MatchedToOneFatJet_DR_b21_b22", ";#Delta R;Events", 100, 0.0, 5.0)
        #=========================================================================================================================================================================
        
        # BoostedExcl histograms
        hBoostedExcl_GenPart_H1_pt    = ROOT.TH1F("hBoostedExcl_GenPart_H1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hBoostedExcl_GenPart_H2_pt    = ROOT.TH1F("hBoostedExcl_GenPart_H2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hBoostedExcl_GenPart_H1_b1_pt = ROOT.TH1F("hBoostedExcl_GenPart_H1_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hBoostedExcl_GenPart_H1_b2_pt = ROOT.TH1F("hBoostedExcl_GenPart_H1_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hBoostedExcl_GenPart_H2_b1_pt = ROOT.TH1F("hBoostedExcl_GenPart_H2_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hBoostedExcl_GenPart_H2_b2_pt = ROOT.TH1F("hBoostedExcl_GenPart_H2_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hBoostedExcl_GenPart_H1_b1_eta = ROOT.TH1F("hBoostedExcl_GenPart_H1_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hBoostedExcl_GenPart_H1_b2_eta = ROOT.TH1F("hBoostedExcl_GenPart_H1_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hBoostedExcl_GenPart_H2_b1_eta = ROOT.TH1F("hBoostedExcl_GenPart_H2_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hBoostedExcl_GenPart_H2_b2_eta = ROOT.TH1F("hBoostedExcl_GenPart_H2_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hBoostedExcl_GenFatJet_H1_pt  = ROOT.TH1F("hBoostedExcl_GenFatJet_H1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hBoostedExcl_GenFatJet_H2_pt  = ROOT.TH1F("hBoostedExcl_GenFatJet_H2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hBoostedExcl_GenFatJet_H1_eta = ROOT.TH1F("hBoostedExcl_GenFatJet_H1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hBoostedExcl_GenFatJet_H2_eta = ROOT.TH1F("hBoostedExcl_GenFatJet_H2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hBoostedExcl_RecoFatJet_H1_pt  = ROOT.TH1F("hBoostedExcl_RecoFatJet_H1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hBoostedExcl_RecoFatJet_H2_pt  = ROOT.TH1F("hBoostedExcl_RecoFatJet_H2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hBoostedExcl_RecoFatJet_H1_eta = ROOT.TH1F("hBoostedExcl_RecoFatJet_H1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hBoostedExcl_RecoFatJet_H2_eta = ROOT.TH1F("hBoostedExcl_RecoFatJet_H2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hBoostedExcl_RecoFatJet_H1_TXbb = ROOT.TH1F("hBoostedExcl_RecoFatJet_H1_TXbb", ";T_{Xbb} score;Events", 100, 0.0, 1.0)
        hBoostedExcl_RecoFatJet_H2_TXbb = ROOT.TH1F("hBoostedExcl_RecoFatJet_H2_TXbb", ";T_{Xbb} score;Events", 100, 0.0, 1.0)
        hBoostedExcl_RecoFatJet_H1_m = ROOT.TH1F("hBoostedExcl_RecoFatJet_H1_m", ";M [GeV];Events", 300, 0.0, 300)
        hBoostedExcl_RecoFatJet_H2_m = ROOT.TH1F("hBoostedExcl_RecoFatJet_H2_m", ";M [GeV];Events", 300, 0.0, 300)
        hBoostedExcl_NJets = ROOT.TH1I("hBoostedExcl_NJets", ";jets multiplicity;Events", 15, 0, 15)
        hBoostedExcl_NFatJets = ROOT.TH1I("hBoostedExcl_NFatJets", ";fatjets multiplicity;Events", 10, 0, 10)
        hBoostedExcl_AK8PFHT = ROOT.TH1F("hBoostedExcl_AK8PFHT", ";AK8 PF H_{T} [GeV];Events", 200, 0.0, 2000)
        hBoostedExcl_RecoFatJet_DeltaR_H1_H2 = ROOT.TH1F("hBoostedExcl_RecoFatJet_DeltaR_H1_H2", ";#Delta R;Events", 100, 0.0, 5.0)
        hBoostedExcl_RecoFatJet_DeltaEta_H1_H2 = ROOT.TH1F("hBoostedExcl_RecoFatJet_DeltaEta_H1_H2", ";#Delta#eta;Events", 50, 0.0, 5.0)
        hBoostedExcl_RecoFatJet_DeltaPhi_H1_H2 = ROOT.TH1F("hBoostedExcl_RecoFatJet_DeltaPhi_H1_H2", ";#Delta#phi;Events", 50, 0.0, 5.0)
        hBoostedExcl_RecoFatJet_H1_mSD_Uncorrected = ROOT.TH1F("hBoostedExcl_RecoFatJet_H1_mSD_Uncorrected", ";m_{SD} [GeV];Events", 300, 0, 300)
        hBoostedExcl_RecoFatJet_H1_area = ROOT.TH1F("hBoostedExcl_RecoFatJet_H1_area", ";area;Events", 100, 0.0, 5.0)
        hBoostedExcl_RecoFatJet_H1_n2b1 = ROOT.TH1F("hBoostedExcl_RecoFatJet_H1_n2b1", ";n2b1;Events", 100, 0.0, 5.0)
        hBoostedExcl_RecoFatJet_H1_n3b1 = ROOT.TH1F("hBoostedExcl_RecoFatJet_H1_n3b1", ";n3b1;Events", 100, 0.0, 5.0)
        hBoostedExcl_RecoFatJet_H1_tau21 = ROOT.TH1F("hBoostedExcl_RecoFatJet_H1_tau21", ";#tau_{21};Events", 100, 0.0, 2.5)
        hBoostedExcl_RecoFatJet_H1_tau32 = ROOT.TH1F("hBoostedExcl_RecoFatJet_H1_tau32", ";#tau_{32};Events", 100, 0.0,2.5)
        hBoostedExcl_RecoFatJet_H1_nsubjets = ROOT.TH1F("hBoostedExcl_RecoFatJet_H1_nsubjets", ";subjet multiplicity;Events", 3, 0, 3)
        hBoostedExcl_RecoFatJet_H1_subjet1_pt = ROOT.TH1F("hBoostedExcl_RecoFatJet_H1_subjet1_pt", ";subjet 1 p_{T} [GeV];Events", 200, 0.0, 800)
        hBoostedExcl_RecoFatJet_H1_subjet1_eta = ROOT.TH1F("hBoostedExcl_RecoFatJet_H1_subjet1_eta", ";subjet 1 #eta;Events", 120, -4.0, 4.0)
        hBoostedExcl_RecoFatJet_H1_subjet1_m = ROOT.TH1F("hBoostedExcl_RecoFatJet_H1_subjet1_m", ";subjet 1 M [GeV];Events", 200, 0.0, 800)
        hBoostedExcl_RecoFatJet_H1_subjet1_btag = ROOT.TH1F("hBoostedExcl_RecoFatJet_H1_subjet1_btag", ";subjet 1 b-discriminator;Events", 100, 0.0, 1.0)
        hBoostedExcl_RecoFatJet_H1_subjet2_pt = ROOT.TH1F("hBoostedExcl_RecoFatJet_H1_subjet2_pt", ";subjet 2 p_{T} [GeV];Events", 200, 0.0, 800)
        hBoostedExcl_RecoFatJet_H1_subjet2_eta = ROOT.TH1F("hBoostedExcl_RecoFatJet_H1_subjet2_eta", ";subjet 2 #eta;Events", 120, -4.0, 4.0)
        hBoostedExcl_RecoFatJet_H1_subjet2_m = ROOT.TH1F("hBoostedExcl_RecoFatJet_H1_subjet2_m", ";subjet 2 M [GeV];Events", 200, 0.0, 800)
        hBoostedExcl_RecoFatJet_H1_subjet2_btag = ROOT.TH1F("hBoostedExcl_RecoFatJet_H1_subjet2_btag", ";subjet 2 b-discriminator;Events", 100,0.0, 1.0)
        hBoostedExcl_RecoFatJet_H2_mSD_Uncorrected = ROOT.TH1F("hBoostedExcl_RecoFatJet_H2_mSD_Uncorrected", ";m_{SD} [GeV];Events", 300, 0, 300)
        hBoostedExcl_RecoFatJet_H2_area = ROOT.TH1F("hBoostedExcl_RecoFatJet_H2_area", ";area;Events", 100, 0.0, 5.0)
        hBoostedExcl_RecoFatJet_H2_n2b1 = ROOT.TH1F("hBoostedExcl_RecoFatJet_H2_n2b1", ";n2b1;Events", 100, 0.0, 5.0)
        hBoostedExcl_RecoFatJet_H2_n3b1 = ROOT.TH1F("hBoostedExcl_RecoFatJet_H2_n3b1", ";n3b1;Events", 100, 0.0, 5.0)
        hBoostedExcl_RecoFatJet_H2_tau21 = ROOT.TH1F("hBoostedExcl_RecoFatJet_H2_tau21", ";#tau_{21};Events", 100, 0.0, 2.5)
        hBoostedExcl_RecoFatJet_H2_tau32 = ROOT.TH1F("hBoostedExcl_RecoFatJet_H2_tau32", ";#tau_{32};Events", 100, 0.0,2.5)
        hBoostedExcl_RecoFatJet_H2_nsubjets = ROOT.TH1F("hBoostedExcl_RecoFatJet_H2_nsubjets", ";subjet multiplicity;Events", 3, 0, 3)
        hBoostedExcl_RecoFatJet_H2_subjet1_pt = ROOT.TH1F("hBoostedExcl_RecoFatJet_H2_subjet1_pt", ";subjet 1 p_{T} [GeV];Events", 200, 0.0, 800)
        hBoostedExcl_RecoFatJet_H2_subjet1_eta = ROOT.TH1F("hBoostedExcl_RecoFatJet_H2_subjet1_eta", ";subjet 1 #eta;Events", 120, -4.0, 4.0)
        hBoostedExcl_RecoFatJet_H2_subjet1_m = ROOT.TH1F("hBoostedExcl_RecoFatJet_H2_subjet1_m", ";subjet 1 M [GeV];Events", 200, 0.0, 800)
        hBoostedExcl_RecoFatJet_H2_subjet1_btag = ROOT.TH1F("hBoostedExcl_RecoFatJet_H2_subjet1_btag", ";subjet 1 b-discriminator;Events", 100, 0.0, 1.0)
        hBoostedExcl_RecoFatJet_H2_subjet2_pt = ROOT.TH1F("hBoostedExcl_RecoFatJet_H2_subjet2_pt", ";subjet 2 p_{T} [GeV];Events", 200, 0.0, 800)
        hBoostedExcl_RecoFatJet_H2_subjet2_eta = ROOT.TH1F("hBoostedExcl_RecoFatJet_H2_subjet2_eta", ";subjet 2 #eta;Events", 120, -4.0, 4.0)
        hBoostedExcl_RecoFatJet_H2_subjet2_m = ROOT.TH1F("hBoostedExcl_RecoFatJet_H2_subjet2_m", ";subjet 2 M [GeV];Events", 200, 0.0, 800)
        hBoostedExcl_RecoFatJet_H2_subjet2_btag = ROOT.TH1F("hBoostedExcl_RecoFatJet_H2_subjet2_btag", ";subjet 2 b-discriminator;Events", 100,0.0, 1.0)
        
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        # Semi-resolved regime
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
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
        hSemiresolved_H1Boosted_H2resolved_GenFatJet_H1_pt = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_GenFatJet_H1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hSemiresolved_H1Boosted_H2resolved_GenFatJet_H1_eta = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_GenFatJet_H1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolved_H1Boosted_H2resolved_GenJet_H2_b1_pt = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_GenJet_H2_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 800)
        hSemiresolved_H1Boosted_H2resolved_GenJet_H2_b2_pt = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_GenJet_H2_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 800)
        hSemiresolved_H1Boosted_H2resolved_GenJet_H2_b1_eta = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_GenJet_H2_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolved_H1Boosted_H2resolved_GenJet_H2_b2_eta = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_GenJet_H2_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_pt = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_eta = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_m = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_m", ";H_{1} mass", 300, 0, 300)
        hSemiresolved_H1Boosted_H2resolved_RecoJet_H2_b1_pt = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_RecoJet_H2_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 800)
        hSemiresolved_H1Boosted_H2resolved_RecoJet_H2_b2_pt = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_RecoJet_H2_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 800)
        hSemiresolved_H1Boosted_H2resolved_RecoJet_H2_b1_eta = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_RecoJet_H2_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolved_H1Boosted_H2resolved_RecoJet_H2_b2_eta = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_RecoJet_H2_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
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
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_m = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_m", ";subjet 1 M [GeV];Events", 200, 0.0, 800)
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_btag = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_btag", ";subjet 1 b-discriminator;Events", 100, 0.0, 1.0)
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_pt = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_pt", ";subjet 2 p_{T} [GeV];Events", 200, 0.0, 800)
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_eta = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_eta", ";subjet 2 #eta;Events", 120, -4.0, 4.0)
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_m = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_m", ";subjet 2 M [GeV];Events", 200, 0.0, 800)
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_btag = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_btag", ";subjet 2 b-discriminator;Events", 100,0.0, 1.0)
        hSemiresolved_H1Boosted_H2resolved_NJets = ROOT.TH1I("hSemiresolved_H1Boosted_H2resolved_NJets", "; jets multiplicity;Events", 15, 0, 15)
        hSemiresolved_H1Boosted_H2resolved_NFatJets = ROOT.TH1I("hSemiresolved_H1Boosted_H2resolved_NFatJets", ";fatjets multiplicity;Events", 10, 0, 10)
        hSemiresolved_H1Boosted_H2resolved_AK8PFHT = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_AK8PFHT", ";AK8 PF H_{T} [GeV];Events", 200, 0.0, 2000)
        hSemiresolved_H1Boosted_H2resolved_DeltaR_H1_H2 = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_DeltaR_H1_H2", ";#Delta R;Events", 100, 0.0, 5.0)
        hSemiresolved_H1Boosted_H2resolved_DeltaEta_H1_H2 = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_DeltaEta_H1_H2", ";#Delta#eta;Events", 50, 0.0, 5.0)
        hSemiresolved_H1Boosted_H2resolved_DeltaPhi_H1_H2 = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_DeltaPhi_H1_H2", ";#Delta#phi;Events", 50, 0.0,5.0)
        hSemiresolved_H1Boosted_H2resolved_InvMass_H2 = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_InvMass_H2", ";m_{H} [GeV]", 300, 0, 300)
        hSemiresolved_H1Boosted_H2resolved_InvMassRegressed_H2 = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_InvMassRegressed_H2", ";m_{H} [GeV]", 300, 0, 300)
        hSemiresolved_H1Boosted_H2resolved_H2_pt = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_H2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hSemiresolved_H1Boosted_H2resolved_H2_eta = ROOT.TH1F("hSemiresolved_H1Boosted_H2resolved_H2_eta", ";#eta;Events", 120, -4.0, 4.0)
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
        # Semi-resolved regime: H2 is boosted, H1 is resolved
        hSemiresolved_H2Boosted_H1resolved_NJets = ROOT.TH1I("hSemiresolved_H2Boosted_H1resolved_NJets", ";jets multiplicity;Events", 15, 0, 15)
        hSemiresolved_H2Boosted_H1resolved_NFatJets = ROOT.TH1I("hSemiresolved_H2Boosted_H1resolved_NFatJets", ";fatjets multiplicity;Events", 10, 0, 10)
        hSemiresolved_H2Boosted_H1resolved_AK8PFHT = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_AK8PFHT", ";AK8 PF H_{T} [GeV];Events", 200,0.0, 2000)
        hSemiresolved_H2Boosted_H1resolved_DeltaR_H1_H2 = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_DeltaR_H1_H2", ";#Delta R;Events", 100, 0.0, 5.0)
        hSemiresolved_H2Boosted_H1resolved_DeltaEta_H1_H2 = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_DeltaEta_H1_H2", ";#Delta#eta;Events", 50, 0.0, 5.0)
        hSemiresolved_H2Boosted_H1resolved_DeltaPhi_H1_H2 = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_DeltaPhi_H1_H2", ";#Delta#phi;Events", 50, 0.0, 5.0)
        hSemiresolved_H2Boosted_H1resolved_InvMass_H1 = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_InvMass_H1", ";m_{H} [GeV]", 300, 0, 300)
        hSemiresolved_H2Boosted_H1resolved_InvMassRegressed_H1 = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_InvMassRegressed_H1", ";m_{H} [GeV]", 300, 0, 300)
        hSemiresolved_H2Boosted_H1resolved_H1_pt = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_H1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hSemiresolved_H2Boosted_H1resolved_H1_eta = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_H1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_m = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_m", ";m_{H} [GeV]", 300, 0, 300)
        hSemiresolved_H2Boosted_H1resolved_GenFatJet_H2_pt = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_GenFatJet_H2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hSemiresolved_H2Boosted_H1resolved_GenFatJet_H2_eta = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_GenFatJet_H2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolved_H2Boosted_H1resolved_GenJet_H1_b1_pt = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_GenJet_H1_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 800)
        hSemiresolved_H2Boosted_H1resolved_GenJet_H1_b2_pt = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_GenJet_H1_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 800)
        hSemiresolved_H2Boosted_H1resolved_GenJet_H1_b1_eta = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_GenJet_H1_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolved_H2Boosted_H1resolved_GenJet_H1_b2_eta = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_GenJet_H1_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_pt = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_eta = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolved_H2Boosted_H1resolved_RecoJet_H1_b1_pt = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_RecoJet_H1_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 800)
        hSemiresolved_H2Boosted_H1resolved_RecoJet_H1_b2_pt = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_RecoJet_H1_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 800)
        hSemiresolved_H2Boosted_H1resolved_RecoJet_H1_b1_eta = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_RecoJet_H1_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolved_H2Boosted_H1resolved_RecoJet_H1_b2_eta = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_RecoJet_H1_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_mSD_Uncorrected = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_mSD_Uncorrected", ";m_{SD} [GeV];Events", 300, 0, 300)
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_area = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_area", ";area;Events", 100, 0.0, 5.0)
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_n2b1 = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_n2b1", ";n2b1;Events", 100, 0.0, 5.0)
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_n3b1 = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_n3b1", ";n3b2;Events", 100, 0.0, 5.0)
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_tau21 = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_tau21", ";#tau_{21};Events", 100, 0.0, 2.5)
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_tau32 = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_tau32", ";#tau_{32};Events", 100, 0.0, 2.5)
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_nsubjets = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_nsubjets", ";subjet multiplicity;Events", 3, 0, 3)
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_pt = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_pt", ";subjet 1 p_{T} [GeV];Events", 200, 0.0, 800)
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_eta = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_eta", ";subjet 1 #eta;Events", 120, -4.0, 4.0)
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_m = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_m", ";subjet 1 M [GeV];Events", 200, 0.0, 800)
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_btag = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_btag", ";subjet 1 b-discriminator;Events", 100, 0.0, 1.0)
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_pt = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_pt", ";subjet 2 p_{T} [GeV];Events", 200, 0.0, 800)
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_eta = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_eta", ";subjet 2 #eta;Events", 120, -4.0, 4.0)
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_m = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_m", ";subjet 2 M [GeV];Events", 200, 0.0, 800)
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_btag = ROOT.TH1F("hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_btag", ";subjet 2 b-discriminator;Events", 100,0.0, 1.0)

        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        # Semi-resolved exclusive regime
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        hSemiresolvedExcl_GenPart_H1_pt    = ROOT.TH1F("hSemiresolvedExcl_GenPart_H1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hSemiresolvedExcl_GenPart_H2_pt    = ROOT.TH1F("hSemiresolvedExcl_GenPart_H2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hSemiresolvedExcl_GenPart_H1_b1_pt = ROOT.TH1F("hSemiresolvedExcl_GenPart_H1_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hSemiresolvedExcl_GenPart_H1_b2_pt = ROOT.TH1F("hSemiresolvedExcl_GenPart_H1_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hSemiresolvedExcl_GenPart_H2_b1_pt = ROOT.TH1F("hSemiresolvedExcl_GenPart_H2_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hSemiresolvedExcl_GenPart_H2_b2_pt = ROOT.TH1F("hSemiresolvedExcl_GenPart_H2_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hSemiresolvedExcl_GenPart_H1_b1_eta = ROOT.TH1F("hSemiresolvedExcl_GenPart_H1_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_GenPart_H1_b2_eta = ROOT.TH1F("hSemiresolvedExcl_GenPart_H1_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_GenPart_H2_b1_eta = ROOT.TH1F("hSemiresolvedExcl_GenPart_H2_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_GenPart_H2_b2_eta = ROOT.TH1F("hSemiresolvedExcl_GenPart_H2_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_H1Boosted_H2resolved_GenFatJet_H1_pt = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_GenFatJet_H1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hSemiresolvedExcl_H1Boosted_H2resolved_GenFatJet_H1_eta = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_GenFatJet_H1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_H1Boosted_H2resolved_GenJet_H2_b1_pt = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_GenJet_H2_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 800)
        hSemiresolvedExcl_H1Boosted_H2resolved_GenJet_H2_b2_pt = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_GenJet_H2_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 800)
        hSemiresolvedExcl_H1Boosted_H2resolved_GenJet_H2_b1_eta = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_GenJet_H2_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_H1Boosted_H2resolved_GenJet_H2_b2_eta = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_GenJet_H2_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_pt = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_eta = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_m = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_m", ";H_{1} mass", 300, 0, 300)
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoJet_H2_b1_pt = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_RecoJet_H2_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 800)
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoJet_H2_b2_pt = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_RecoJet_H2_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 800)
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoJet_H2_b1_eta = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_RecoJet_H2_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoJet_H2_b2_eta = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_RecoJet_H2_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_TXbb = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_TXbb", ";T_{Xbb} score;Events", 100, 0.0, 1.0)
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_TXbb = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_TXbb", ";T_{Xbb} score;Events", 100, 0.0, 1.0)
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_mSD_Uncorrected = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_mSD_Uncorrected", ";m_{SD} [GeV];Events", 300, 0, 300) 
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_area = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_area", ";area;Events", 100, 0.0, 5.0)
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_n2b1 = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_n2b1", ";n2b1;Events", 100, 0.0, 5.0)
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_n3b1 = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_n3b1", ";n3b1;Events", 100, 0.0, 5.0)
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_tau21 = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_tau21", ";#tau_{21};Events", 100, 0.0, 2.5)
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_tau32 = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_tau32", ";#tau_{32};Events", 100, 0.0, 2.5)
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_nsubjets = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_nsubjets", ";subjet multiplicity;Events", 3, 0, 3)
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_pt = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_pt", ";subjet 1 p_{T} [GeV];Events", 200, 0.0, 800)
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_eta = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_eta", ";subjet 1 #eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_m = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_m", ";subjet 1 M [GeV];Events", 200, 0.0, 800)
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_btag = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_btag", ";subjet 1 b-discriminator;Events", 100, 0.0, 1.0)
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_pt = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_pt", ";subjet 2 p_{T} [GeV];Events", 200, 0.0, 800)
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_eta = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_eta", ";subjet 2 #eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_m = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_m", ";subjet 2 M [GeV];Events", 200, 0.0, 800)
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_btag = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_btag", ";subjet 2 b-discriminator;Events", 100,0.0, 1.0)
        hSemiresolvedExcl_H1Boosted_H2resolved_NJets = ROOT.TH1I("hSemiresolvedExcl_H1Boosted_H2resolved_NJets", "; jets multiplicity;Events", 15, 0, 15)
        hSemiresolvedExcl_H1Boosted_H2resolved_NFatJets = ROOT.TH1I("hSemiresolvedExcl_H1Boosted_H2resolved_NFatJets", ";fatjets multiplicity;Events", 10, 0, 10)
        hSemiresolvedExcl_H1Boosted_H2resolved_AK8PFHT = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_AK8PFHT", ";AK8 PF H_{T} [GeV];Events", 200,0.0, 2000)
        hSemiresolvedExcl_H1Boosted_H2resolved_DeltaR_H1_H2 = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_DeltaR_H1_H2", ";#Delta R;Events", 100, 0.0, 5.0)
        hSemiresolvedExcl_H1Boosted_H2resolved_DeltaEta_H1_H2 = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_DeltaEta_H1_H2", ";#Delta#eta;Events", 50, 0.0, 5.0)
        hSemiresolvedExcl_H1Boosted_H2resolved_DeltaPhi_H1_H2 = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_DeltaPhi_H1_H2", ";#Delta#phi;Events", 50, 0.0,5.0)
        hSemiresolvedExcl_H1Boosted_H2resolved_InvMass_H2 = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_InvMass_H2", ";m_{H} [GeV]", 300, 0, 300)
        hSemiresolvedExcl_H1Boosted_H2resolved_InvMassRegressed_H2 = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_InvMassRegressed_H2", ";m_{H} [GeV]", 300, 0, 300)
        hSemiresolvedExcl_H1Boosted_H2resolved_H2_pt = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_H2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hSemiresolvedExcl_H1Boosted_H2resolved_H2_eta = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_H2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_H1Boosted_H2resolved_PFHT = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_PFHT", "; PF H_{T} [GeV];Events", 200, 0.0, 1000)
        hSemiresolvedExcl_H1Boosted_H2resolved_NLooseBJets = ROOT.TH1I("hSemiresolvedExcl_H1Boosted_H2resolved_NLooseBJets", ";b-jets L;Events", 10, 0, 10)
        hSemiresolvedExcl_H1Boosted_H2resolved_NMediumBJets = ROOT.TH1I("hSemiresolvedExcl_H1Boosted_H2resolved_NMediumBJets", ";b-jets M;Events", 10, 0, 10)
        hSemiresolvedExcl_H1Boosted_H2resolved_NTightBJets = ROOT.TH1I("hSemiresolvedExcl_H1Boosted_H2resolved_NTightBJets", ";b-jets T;Events", 10, 0, 10)
        hSemiresolvedExcl_H1Boosted_H2resolved_Jet1Pt = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_Jet1Pt", ";jet 1 p_{T} [GeV];Events", 100, 0.0, 500)
        hSemiresolvedExcl_H1Boosted_H2resolved_Jet2Pt = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_Jet2Pt", ";jet 2 p_{T} [GeV];Events", 100, 0.0, 500)
        hSemiresolvedExcl_H1Boosted_H2resolved_Jet3Pt = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_Jet3Pt", ";jet 3 p_{T} [GeV];Events", 100, 0.0, 500)
        hSemiresolvedExcl_H1Boosted_H2resolved_Jet4Pt = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_Jet4Pt", ";jet 4 p_{T} [GeV];Events", 100, 0.0, 500)
        hSemiresolvedExcl_H1Boosted_H2resolved_Jet1Eta = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_Jet1Eta", ";jet 1 #eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_H1Boosted_H2resolved_Jet2Eta = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_Jet2Eta", ";jet 2 #eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_H1Boosted_H2resolved_Jet3Eta = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_Jet3Eta", ";jet 3 #eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_H1Boosted_H2resolved_Jet4Eta = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_Jet4Eta", ";jet 4 #eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_H1Boosted_H2resolved_AK8Jet1Pt = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_AK8Jet1Pt", "; fatjet 1 p_{T} [GeV];Events", 200, 0.0, 1000)
        # Semi-resolved regime: H2 is boosted, H1 is resolved
        hSemiresolvedExcl_H2Boosted_H1resolved_NJets = ROOT.TH1I("hSemiresolvedExcl_H2Boosted_H1resolved_NJets", ";jets multiplicity;Events", 15, 0, 15)
        hSemiresolvedExcl_H2Boosted_H1resolved_NFatJets = ROOT.TH1I("hSemiresolvedExcl_H2Boosted_H1resolved_NFatJets", ";fatjets multiplicity;Events", 10, 0, 10)
        hSemiresolvedExcl_H2Boosted_H1resolved_AK8PFHT = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_AK8PFHT", ";AK8 PF H_{T} [GeV];Events", 200,0.0, 2000)
        hSemiresolvedExcl_H2Boosted_H1resolved_DeltaR_H1_H2 = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_DeltaR_H1_H2", ";#Delta R;Events", 100, 0.0, 5.0)
        hSemiresolvedExcl_H2Boosted_H1resolved_DeltaEta_H1_H2 = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_DeltaEta_H1_H2", ";#Delta#eta;Events", 50, 0.0, 5.0)
        hSemiresolvedExcl_H2Boosted_H1resolved_DeltaPhi_H1_H2 = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_DeltaPhi_H1_H2", ";#Delta#phi;Events", 50, 0.0, 5.0)
        hSemiresolvedExcl_H2Boosted_H1resolved_InvMass_H1 = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_InvMass_H1", ";m_{H} [GeV]", 300, 0, 300)
        hSemiresolvedExcl_H2Boosted_H1resolved_InvMassRegressed_H1 = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_InvMassRegressed_H1", ";m_{H} [GeV]", 300, 0, 300)
        hSemiresolvedExcl_H2Boosted_H1resolved_H1_pt = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_H1_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hSemiresolvedExcl_H2Boosted_H1resolved_H1_eta = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_H1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_m = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_m", ";m_{H} [GeV]", 300, 0, 300)
        hSemiresolvedExcl_H2Boosted_H1resolved_GenFatJet_H2_pt = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_GenFatJet_H2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hSemiresolvedExcl_H2Boosted_H1resolved_GenFatJet_H2_eta = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_GenFatJet_H2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_H2Boosted_H1resolved_GenJet_H1_b1_pt = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_GenJet_H1_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 800)
        hSemiresolvedExcl_H2Boosted_H1resolved_GenJet_H1_b2_pt = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_GenJet_H1_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 800)
        hSemiresolvedExcl_H2Boosted_H1resolved_GenJet_H1_b1_eta = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_GenJet_H1_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_H2Boosted_H1resolved_GenJet_H1_b2_eta = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_GenJet_H1_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_pt = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_pt", ";p_{T} [GeV];Events", 200, 0.0, 1000)
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_eta = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoJet_H1_b1_pt = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_RecoJet_H1_b1_pt", ";p_{T} [GeV];Events", 200, 0.0, 800)
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoJet_H1_b2_pt = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_RecoJet_H1_b2_pt", ";p_{T} [GeV];Events", 200, 0.0, 800)
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoJet_H1_b1_eta = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_RecoJet_H1_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoJet_H1_b2_eta = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_RecoJet_H1_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_mSD_Uncorrected = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_mSD_Uncorrected", ";m_{SD} [GeV];Events", 300, 0, 300)
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_area = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_area", ";area;Events", 100, 0.0, 5.0)
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_n2b1 = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_n2b1", ";n2b1;Events", 100, 0.0, 5.0)
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_n3b1 = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_n3b1", ";n3b2;Events", 100, 0.0, 5.0)
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_tau21 = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_tau21", ";#tau_{21};Events", 100, 0.0, 2.5)
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_tau32 = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_tau32", ";#tau_{32};Events", 100, 0.0, 2.5)
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_nsubjets = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_nsubjets", ";subjet multiplicity;Events", 3, 0, 3)
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_pt = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_pt", ";subjet 1 p_{T} [GeV];Events", 200, 0.0, 800)
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_eta = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_eta", ";subjet 1 #eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_m = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_m", ";subjet 1 M [GeV];Events", 200, 0.0, 800)
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_btag = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_btag", ";subjet 1 b-discriminator;Events", 100, 0.0, 1.0)
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_pt = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_pt", ";subjet 2 p_{T} [GeV];Events", 200, 0.0, 800)
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_eta = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_eta", ";subjet 2 #eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_m = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_m", ";subjet 2 M [GeV];Events", 200, 0.0, 800)
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_btag = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_btag", ";subjet 2 b-discriminator;Events", 100,0.0, 1.0)
                
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        # Trigger related histograms
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
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
        
        # Semi-resolved exclusive
        hSemiresolvedExclPassed_HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5 = ROOT.TH1I("hSemiresolvedExclPassed_HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5", ";trigger bit;Events", 2, 0, 2)
        hSemiresolvedExclPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np4 = ROOT.TH1I("hSemiresolvedExclPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np4", ";trigger bit;Events", 2, 0,2)
        hSemiresolvedExclPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np2 = ROOT.TH1I("hSemiresolvedExclPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np2", ";trigger bit;Events", 2, 0,2)
        hSemiresolvedExclPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p1 = ROOT.TH1I("hSemiresolvedExclPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p1", ";trigger bit;Events", 2, 0,2)
        hSemiresolvedExclPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p17 = ROOT.TH1I("hSemiresolvedExclPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p17", ";trigger bit;Events", 2, 0,2)
        hSemiresolvedExclPassed_HLT_PFHT1050 = ROOT.TH1I("hSemiresolvedExclPassed_HLT_PFHT1050", ";trigger bit;Events", 2, 0,2)
        hSemiresolvedExclPassed_HLT_PFJet500 = ROOT.TH1I("hSemiresolvedExclPassed_HLT_PFJet500", ";trigger bit;Events", 2, 0,2)
        hSemiresolvedExclPassed_HLT_AK8PFHT800_TrimMass50  = ROOT.TH1I("hSemiresolvedExclPassed_HLT_AK8PFHT800_TrimMass50", ";trigger bit;Events", 2, 0,2)
        hSemiresolvedExclPassed_HLT_AK8PFJet400_TrimMass30 = ROOT.TH1I("hSemiresolvedExclPassed_HLT_AK8PFJet400_TrimMass30", ";trigger bit;Events", 2, 0,2)
        hSemiresolvedExclPassed_HLT_AK8PFJet420_TrimMass30 = ROOT.TH1I("hSemiresolvedExclPassed_HLT_AK8PFJet420_TrimMass30", ";trigger bit;Events", 2, 0,2)
        hSemiresolvedExclPassed_HLT_AK8PFJet500 = ROOT.TH1I("hSemiresolvedExclPassed_HLT_AK8PFJet500", ";trigger bit;Events", 2, 0,2)
        hSemiresolvedExclPassed_HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59 = ROOT.TH1I("hSemiresolvedExclPassed_HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59", ";trigger bit;Events", 2, 0,2)
        hSemiresolvedExclPassed_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94 = ROOT.TH1I("hSemiresolvedExclPassed_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94", ";trigger bit;Events", 2, 0,2)
        hSemiresolvedExclPassed_HLT_AK8PFHT750_TrimMass50 = ROOT.TH1I("hSemiresolvedExclPassed_HLT_AK8PFHT750_TrimMass50", ";trigger bit;Events", 2, 0,2)
        hSemiresolvedExclPassed_HLT_AK8PFJet360_TrimMass30 = ROOT.TH1I("hSemiresolvedExclPassed_HLT_AK8PFJet360_TrimMass30", ";trigger bit;Events", 2, 0,2)
        hSemiresolvedExclPassed_HLT_AK8PFJet380_TrimMass30 = ROOT.TH1I("hSemiresolvedExclPassed_HLT_AK8PFJet380_TrimMass30", ";trigger bit;Events", 2, 0,2)
        hSemiresolvedExclPassed_OR = ROOT.TH1I("hSemiresolvedExclPassed_OR", ";trigger bit;Events", 2, 0,2)
        
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

        # Boosted exclusive
        hBoostedExclPassed_HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5 = ROOT.TH1I("hBoostedExclPassed_HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5", ";trigger bit;Events", 2, 0, 2)
        hBoostedExclPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np4 = ROOT.TH1I("hBoostedExclPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np4", ";trigger bit;Events", 2, 0,2)
        hBoostedExclPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np2 = ROOT.TH1I("hBoostedExclPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np2", ";trigger bit;Events", 2, 0,2)
        hBoostedExclPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p1 = ROOT.TH1I("hBoostedExclPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p1", ";trigger bit;Events", 2, 0,2)
        hBoostedExclPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p17 = ROOT.TH1I("hBoostedExclPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p17", ";trigger bit;Events", 2, 0,2)
        hBoostedExclPassed_HLT_PFHT1050 = ROOT.TH1I("hBoostedExclPassed_HLT_PFHT1050", ";trigger bit;Events", 2, 0,2)
        hBoostedExclPassed_HLT_PFJet500 = ROOT.TH1I("hBoostedExclPassed_HLT_PFJet500", ";trigger bit;Events", 2, 0,2)
        hBoostedExclPassed_HLT_AK8PFHT800_TrimMass50  = ROOT.TH1I("hBoostedExclPassed_HLT_AK8PFHT800_TrimMass50", ";trigger bit;Events", 2, 0,2)
        hBoostedExclPassed_HLT_AK8PFJet400_TrimMass30 = ROOT.TH1I("hBoostedExclPassed_HLT_AK8PFJet400_TrimMass30", ";trigger bit;Events", 2, 0,2)
        hBoostedExclPassed_HLT_AK8PFJet420_TrimMass30 = ROOT.TH1I("hBoostedExclPassed_HLT_AK8PFJet420_TrimMass30", ";trigger bit;Events", 2, 0,2)
        hBoostedExclPassed_HLT_AK8PFJet500 = ROOT.TH1I("hBoostedExclPassed_HLT_AK8PFJet500", ";trigger bit;Events", 2, 0,2)
        hBoostedExclPassed_HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59 = ROOT.TH1I("hBoostedExclPassed_HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59", ";trigger bit;Events", 2, 0,2)
        hBoostedExclPassed_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94 = ROOT.TH1I("hBoostedExclPassed_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94", ";trigger bit;Events", 2, 0,2)
        hBoostedExclPassed_HLT_AK8PFHT750_TrimMass50 = ROOT.TH1I("hBoostedExclPassed_HLT_AK8PFHT750_TrimMass50", ";trigger bit;Events", 2, 0,2)
        hBoostedExclPassed_HLT_AK8PFJet360_TrimMass30 = ROOT.TH1I("hBoostedExclPassed_HLT_AK8PFJet360_TrimMass30", ";trigger bit;Events", 2, 0,2)
        hBoostedExclPassed_HLT_AK8PFJet380_TrimMass30 = ROOT.TH1I("hBoostedExclPassed_HLT_AK8PFJet380_TrimMass30", ";trigger bit;Events", 2, 0,2)
        hBoostedExclPassed_OR = ROOT.TH1I("hBoostedExclPassed_OR", ";trigger bit;Events", 2, 0,2)
        
        # Initialize counters
        cIsResolvedGen     = 0.0
        cIsBoostedGen      = 0.0
        cIsSemiResolvedGen = 0.0

        cIsResolvedReco     = 0.0
        cIsBoostedReco      = 0.0
        cIsSemiResolvedReco = 0.0
        
        cIsResolvedRecoExcl = 0.0
        cIsBoostedRecoExcl  = 0.0
        cIsSemiResolvedRecoExcl = 0.0
        
        cNotMatchedReco = 0.0

        print("\nProcessing sample %s" % (sample))
        print("Entries = %s" % (entries))
        
        # Loop over all events
        for i, e in enumerate(t):
            
            #print("\n Entry = %s" % (i))
            
            # Counters
            nBQuarksMatchedToGenJets = 0
            nBQuarksMatchedToGenFatJets = 0

            #================================================== Gen-level matching
            bH1_b1_genjet = e.gen_H1_b1_genjet_pt > 0.0
            bH1_b2_genjet = e.gen_H1_b2_genjet_pt > 0.0
            bH2_b1_genjet = e.gen_H2_b1_genjet_pt > 0.0
            bH2_b2_genjet = e.gen_H2_b2_genjet_pt > 0.0
            
            if (bH1_b1_genjet): nBQuarksMatchedToGenJets += 1
            if (bH1_b2_genjet): nBQuarksMatchedToGenJets += 1
            if (bH2_b1_genjet): nBQuarksMatchedToGenJets += 1
            if (bH2_b2_genjet): nBQuarksMatchedToGenJets += 1
            
            bH1_b1_genfatjet = e.gen_H1_b1_genfatjet_pt > 0.0
            bH1_b2_genfatjet = e.gen_H1_b2_genfatjet_pt > 0.0
            bH2_b1_genfatjet = e.gen_H2_b1_genfatjet_pt > 0.0
            bH2_b2_genfatjet = e.gen_H2_b2_genfatjet_pt > 0.0
            
            if (bH1_b1_genfatjet): nBQuarksMatchedToGenFatJets+=1
            if (bH1_b2_genfatjet): nBQuarksMatchedToGenFatJets+=1
            if (bH2_b1_genfatjet): nBQuarksMatchedToGenFatJets+=1
            if (bH2_b2_genfatjet): nBQuarksMatchedToGenFatJets+=1
            
            h2D_NBQuarksMatchedTo_GenJetsVsGenFatJets.Fill(nBQuarksMatchedToGenJets, nBQuarksMatchedToGenFatJets)
            
            # Requirement: both b quarks are matched with a gen fatjet and the fatjet is the same
            bH1_genfatjet = bH1_b1_genfatjet and bH1_b2_genfatjet and areSameJets(e.gen_H1_b1_genfatjet_eta, e.gen_H1_b2_genfatjet_eta, e.gen_H1_b1_genfatjet_phi, e.gen_H1_b2_genfatjet_phi)
            bH2_genfatjet = bH2_b1_genfatjet and bH2_b2_genfatjet and areSameJets(e.gen_H2_b1_genfatjet_eta, e.gen_H2_b2_genfatjet_eta, e.gen_H2_b1_genfatjet_phi, e.gen_H2_b2_genfatjet_phi)
            
            b_b11_b12_sameGenFatjet = bH1_b1_genfatjet and bH1_b2_genfatjet and areSameJets(e.gen_H1_b1_genfatjet_eta, e.gen_H1_b2_genfatjet_eta, e.gen_H1_b1_genfatjet_phi, e.gen_H1_b2_genfatjet_phi)
            b_b11_b21_sameGenFatjet = bH1_b1_genfatjet and bH2_b1_genfatjet and areSameJets(e.gen_H1_b1_genfatjet_eta, e.gen_H2_b1_genfatjet_eta, e.gen_H1_b1_genfatjet_phi, e.gen_H2_b1_genfatjet_phi)
            b_b11_b22_sameGenFatjet = bH1_b1_genfatjet and bH2_b2_genfatjet and areSameJets(e.gen_H1_b1_genfatjet_eta, e.gen_H2_b2_genfatjet_eta, e.gen_H1_b1_genfatjet_phi, e.gen_H2_b2_genfatjet_phi)
            b_b12_b21_sameGenFatjet = bH1_b2_genfatjet and bH2_b1_genfatjet and areSameJets(e.gen_H1_b2_genfatjet_eta, e.gen_H2_b1_genfatjet_eta, e.gen_H1_b2_genfatjet_phi, e.gen_H2_b1_genfatjet_phi)
            b_b12_b22_sameGenFatjet = bH1_b2_genfatjet and bH2_b2_genfatjet and areSameJets(e.gen_H1_b2_genfatjet_eta, e.gen_H2_b2_genfatjet_eta, e.gen_H1_b2_genfatjet_phi, e.gen_H2_b2_genfatjet_phi)
            b_b21_b22_sameGenFatjet = bH2_b1_genfatjet and bH2_b2_genfatjet and areSameJets(e.gen_H2_b1_genfatjet_eta, e.gen_H2_b2_genfatjet_eta, e.gen_H2_b1_genfatjet_phi, e.gen_H2_b2_genfatjet_phi)
            
            bH1_genfatjet_only = bH1_genfatjet and not bH2_genfatjet
            bH2_genfatjet_only = bH2_genfatjet and not bH1_genfatjet
            
            bH1Boosted_H2resolved_gen = bH1_genfatjet_only and bH2_b1_genjet and bH2_b2_genjet
            bH2Boosted_H1resolved_gen = bH2_genfatjet_only and bH1_b1_genjet and bH1_b2_genjet
            
            # Gen-level:
            bIsSemiResolvedGen = bH1Boosted_H2resolved_gen or bH2Boosted_H1resolved_gen
            bIsBoostedGen  = bH1_genfatjet and bH2_genfatjet
            bIsResolvedGen = bH1_b1_genjet and bH1_b2_genjet and bH2_b1_genjet and bH2_b2_genjet
            
            if bIsBoostedGen:
                h_IsBoostedGen_GenFatJet_H1_pt.Fill(e.gen_H1_b1_genfatjet_pt)
                h_IsBoostedGen_GenFatJet_H2_pt.Fill(e.gen_H2_b2_genfatjet_pt)
            
            if bIsSemiResolvedGen:
                if (bH1_b1_genfatjet): h_IsSemiresolvedGen_GenFatJet_H1_pt.Fill(e.gen_H1_b1_genfatjet_pt)
                if (bH1_b2_genfatjet): h_IsSemiresolvedGen_GenFatJet_H2_pt.Fill(e.gen_H2_b2_genfatjet_pt)
            
            if bH1_b1_genfatjet:
                h_GenFatJet_H1_pt.Fill(e.gen_H1_b1_genfatjet_pt)
                                
            if bH1_b2_genfatjet:
                h_GenFatJet_H2_pt.Fill(e.gen_H2_b1_genfatjet_pt)
                

            # Investigating the events with four resolved b-quarks
            if (bIsResolvedGen):
                if (nBQuarksMatchedToGenFatJets == 4):
                    if bIsBoostedGen:
                        h_GenMatchingTo4GenJets_Cases.Fill(10)
                    else:
                        if (not (b_b11_b12_sameGenFatjet or b_b11_b21_sameGenFatjet or b_b11_b22_sameGenFatjet or b_b12_b21_sameGenFatjet or b_b12_b22_sameGenFatjet or b_b21_b22_sameGenFatjet)):
                            h_GenMatchingTo4GenJets_Cases.Fill(11)
                        else:
                            if ((b_b11_b21_sameGenFatjet and b_b12_b22_sameGenFatjet) or (b_b11_b22_sameGenFatjet and b_b12_b21_sameGenFatjet)):
                                h_GenMatchingTo4GenJets_Cases.Fill(12)
                            elif ((b_b11_b12_sameGenFatjet and not b_b21_b22_sameGenFatjet) or (b_b21_b22_sameGenFatjet and not b_b11_b12_sameGenFatjet)):
                                h_GenMatchingTo4GenJets_Cases.Fill(13)
                            elif ((b_b11_b21_sameGenFatjet and not b_b12_b22_sameGenFatjet) or (b_b11_b22_sameGenFatjet and not b_b12_b21_sameGenFatjet) or (b_b12_b21_sameGenFatjet and not b_b11_b22_sameGenFatjet) or (b_b12_b22_sameGenFatjet and not b_b11_b21_sameGenFatjet)):
                                h_GenMatchingTo4GenJets_Cases.Fill(14)
                            else:
                                print("Another case - this should never be reached!")
                elif (nBQuarksMatchedToGenFatJets == 3):
                    if (b_b11_b12_sameGenFatjet or b_b21_b22_sameGenFatjet):
                        h_GenMatchingTo4GenJets_Cases.Fill(7)
                    elif (b_b11_b21_sameGenFatjet or b_b12_b21_sameGenFatjet or b_b11_b22_sameGenFatjet or b_b12_b22_sameGenFatjet):
                        h_GenMatchingTo4GenJets_Cases.Fill(8)
                    elif (not (b_b11_b12_sameGenFatjet or b_b11_b21_sameGenFatjet or b_b11_b22_sameGenFatjet or b_b12_b21_sameGenFatjet or b_b12_b22_sameGenFatjet or b_b21_b22_sameGenFatjet)):
                        h_GenMatchingTo4GenJets_Cases.Fill(9)
                    else:
                        print("Another case - this should never be reached! 3 b-quarks matched to gen-fatjets")
                elif (nBQuarksMatchedToGenFatJets == 2):
                    if ((bH1_b1_genfatjet and bH1_b2_genfatjet and b_b11_b12_sameGenFatjet) or (bH2_b1_genfatjet and bH2_b2_genfatjet  and b_b21_b22_sameGenFatjet)):
                        h_GenMatchingTo4GenJets_Cases.Fill(6)
                    elif (b_b11_b21_sameGenFatjet or b_b11_b22_sameGenFatjet or b_b12_b22_sameGenFatjet or b_b12_b21_sameGenFatjet):
                        h_GenMatchingTo4GenJets_Cases.Fill(5)
                    elif ((bH1_b1_genfatjet and bH1_b2_genfatjet and not b_b11_b12_sameGenFatjet) or (bH2_b1_genfatjet and bH2_b2_genfatjet and not b_b21_b22_sameGenFatjet)):
                        h_GenMatchingTo4GenJets_Cases.Fill(4)
                    else:
                        h_GenMatchingTo4GenJets_Cases.Fill(3)
                elif (nBQuarksMatchedToGenFatJets == 1):
                    h_GenMatchingTo4GenJets_Cases.Fill(2)
                elif (nBQuarksMatchedToGenFatJets == 0):
                    h_GenMatchingTo4GenJets_Cases.Fill(1)
                else:
                    print("This should never be reached")


            # Increment Gen-counters
            if (bIsSemiResolvedGen): cIsSemiResolvedGen += 1
            if (bIsBoostedGen):      cIsBoostedGen += 1
            if (bIsResolvedGen):     cIsResolvedGen += 1
            
            #if (bIsResolvedGen):
            #    print(" GEN is resolved      : %s" % (bIsResolvedGen))
            #if (bIsSemiResolvedGen):
            #    print(" GEN is semi-resolved : %s" % (bIsSemiResolvedGen))
            #if (bIsBoostedGen):
            #    print("\n Entry = %s is GEN boosted,   H1 gen-fatjet pt=%s   H2 gen-fatjet pt=%s  ,  H1 reco-fatjet pt=%s     H2 reco-fatjet pt=%s" % (i, e.gen_H1_b1_genfatjet_pt, e.gen_H2_b1_genfatjet_pt, e.gen_H1_b1_recofatjet_pt, e.gen_H2_b1_recofatjet_pt))
                
            
            #================================================== Reco-level matching
            bH1_b1_recojet = e.gen_H1_b1_recojet_pt > 0.0
            bH1_b2_recojet = e.gen_H1_b2_recojet_pt > 0.0
            bH2_b1_recojet = e.gen_H2_b1_recojet_pt > 0.0
            bH2_b2_recojet = e.gen_H2_b2_recojet_pt > 0.0
            
            bH1_b1_recofatjet = e.gen_H1_b1_recofatjet_pt > 0.0
            bH1_b2_recofatjet = e.gen_H1_b2_recofatjet_pt > 0.0
            bH2_b1_recofatjet = e.gen_H2_b1_recofatjet_pt > 0.0
            bH2_b2_recofatjet = e.gen_H2_b2_recofatjet_pt > 0.0
            
            # Reco counters
            nBQuarksMatchedToRecoJets = 0
            nBQuarksMatchedToRecoFatJets = 0
            if (bH1_b1_recojet): nBQuarksMatchedToRecoJets += 1
            if (bH1_b2_recojet): nBQuarksMatchedToRecoJets += 1
            if (bH2_b1_recojet): nBQuarksMatchedToRecoJets += 1
            if (bH2_b2_recojet): nBQuarksMatchedToRecoJets += 1
            if (bH1_b1_recofatjet): nBQuarksMatchedToRecoFatJets += 1
            if (bH1_b2_recofatjet): nBQuarksMatchedToRecoFatJets += 1
            if (bH2_b1_recofatjet): nBQuarksMatchedToRecoFatJets += 1
            if (bH2_b2_recofatjet): nBQuarksMatchedToRecoFatJets += 1
            h2D_NBQuarksMatchedTo_RecoJetsVsRecoFatJets.Fill(nBQuarksMatchedToRecoJets, nBQuarksMatchedToRecoFatJets)
            
            bH1_recofatjet = bH1_genfatjet and bH1_b1_recofatjet and bH1_b2_recofatjet and areSameJets(e.gen_H1_b1_recofatjet_eta, e.gen_H1_b2_recofatjet_eta, e.gen_H1_b1_recofatjet_phi, e.gen_H1_b2_recofatjet_phi)
            bH2_recofatjet = bH2_genfatjet and bH2_b1_recofatjet and bH2_b2_recofatjet and areSameJets(e.gen_H2_b1_recofatjet_eta, e.gen_H2_b2_recofatjet_eta, e.gen_H2_b1_recofatjet_phi, e.gen_H2_b2_recofatjet_phi)
            
            # Get same fatjet combinations
            b_b11_b12_sameRecoFatjet = bH1_b1_recofatjet and bH1_b2_recofatjet and areSameJets(e.gen_H1_b1_recofatjet_eta, e.gen_H1_b2_recofatjet_eta, e.gen_H1_b1_recofatjet_phi, e.gen_H1_b2_recofatjet_phi)
            b_b11_b21_sameRecoFatjet = bH1_b1_recofatjet and bH2_b1_recofatjet and areSameJets(e.gen_H1_b1_recofatjet_eta, e.gen_H2_b1_recofatjet_eta, e.gen_H1_b1_recofatjet_phi, e.gen_H2_b1_recofatjet_phi)
            b_b11_b22_sameRecoFatjet = bH1_b1_recofatjet and bH2_b2_recofatjet and areSameJets(e.gen_H1_b1_recofatjet_eta, e.gen_H2_b2_recofatjet_eta, e.gen_H1_b1_recofatjet_phi, e.gen_H2_b2_recofatjet_phi)
            b_b12_b21_sameRecoFatjet = bH1_b2_recofatjet and bH2_b1_recofatjet and areSameJets(e.gen_H1_b2_recofatjet_eta, e.gen_H2_b1_recofatjet_eta, e.gen_H1_b2_recofatjet_phi, e.gen_H2_b1_recofatjet_phi)
            b_b12_b22_sameRecoFatjet = bH1_b2_recofatjet and bH2_b2_recofatjet and areSameJets(e.gen_H1_b2_recofatjet_eta, e.gen_H2_b2_recofatjet_eta, e.gen_H1_b2_recofatjet_phi, e.gen_H2_b2_recofatjet_phi)
            b_b21_b22_sameRecoFatjet = bH2_b1_recofatjet and bH2_b2_recofatjet and areSameJets(e.gen_H2_b1_recofatjet_eta, e.gen_H2_b2_recofatjet_eta, e.gen_H2_b1_recofatjet_phi, e.gen_H2_b2_recofatjet_phi)
                        
            bH1_recofatjet_only = bH1_genfatjet_only and bH1_recofatjet and not bH2_recofatjet
            bH2_recofatjet_only = bH2_genfatjet_only and bH2_recofatjet and not bH1_recofatjet
            
            bH1Boosted_H2resolved_reco = bH1_recofatjet_only and bH2_b1_recojet and bH2_b2_recojet
            bH2Boosted_H1resolved_reco = bH2_recofatjet_only and bH1_b1_recojet and bH1_b2_recojet
            
            bIsResolvedReco         = bH1_b1_recojet and bH1_b2_recojet and bH2_b1_recojet and bH2_b2_recojet
            bIsSemiResolvedReco     = bH1Boosted_H2resolved_reco or bH2Boosted_H1resolved_reco
            bIsBoostedReco          = bH1_recofatjet and bH2_recofatjet

            bIsResolvedRecoExcl     = bIsResolvedReco and not (bIsBoostedReco or bIsSemiResolvedReco)
            bIsBoostedRecoExcl      = bIsBoostedReco and not bIsResolvedReco
            bIsSemiResolvedRecoExcl = bIsSemiResolvedReco and not bIsResolvedReco
            
            if (bIsResolvedReco): h2D_NBQuarksMatchedTo_RecoJetsVsCategory.Fill(nBQuarksMatchedToRecoJets, 0)
            if (bIsSemiResolvedReco): h2D_NBQuarksMatchedTo_RecoJetsVsCategory.Fill(nBQuarksMatchedToRecoJets, 1)
            if (bIsBoostedReco): h2D_NBQuarksMatchedTo_RecoJetsVsCategory.Fill(nBQuarksMatchedToRecoJets, 2)
            
            if (bIsResolvedReco): h2D_NBQuarksMatchedTo_RecoFatJetsVsCategory.Fill(nBQuarksMatchedToRecoFatJets, 0)
            if (bIsSemiResolvedReco): h2D_NBQuarksMatchedTo_RecoFatJetsVsCategory.Fill(nBQuarksMatchedToRecoFatJets, 1)
            if (bIsBoostedReco): h2D_NBQuarksMatchedTo_RecoFatJetsVsCategory.Fill(nBQuarksMatchedToRecoFatJets, 2)
            
            if (bIsResolvedReco): cIsResolvedReco += 1
            if (bIsResolvedRecoExcl): cIsResolvedRecoExcl += 1
            if (bIsSemiResolvedReco): cIsSemiResolvedReco += 1
            if (bIsBoostedReco): cIsBoostedReco += 1
            if (bIsBoostedRecoExcl): cIsBoostedRecoExcl += 1
            if (bIsSemiResolvedRecoExcl): cIsSemiResolvedRecoExcl +=1
            
            bIsResolvedRecoCases = {}
            for c in range(1, 15):
                bIsResolvedRecoCases[str(c)] = False
            
            if not bIsBoostedReco:
                if bIsBoostedGen:
                    h_IsBoostedGen_NotBoostedReco_GenFatJet_H1_pt.Fill(e.gen_H1_b1_genfatjet_pt)
                    h_IsBoostedGen_NotBoostedReco_GenFatJet_H2_pt.Fill(e.gen_H2_b1_genfatjet_pt)

            if not bIsSemiResolvedReco:
                if bIsSemiResolvedGen:
                    if (e.gen_H1_b1_genfatjet_pt > 0): h_IsSemiresolvedGen_NotSemiresolvedReco_GenFatJet_H1_pt.Fill(e.gen_H1_b1_genfatjet_pt)
                    if (e.gen_H2_b1_genfatjet_pt > 0): h_IsSemiresolvedGen_NotSemiresolvedReco_GenFatJet_H2_pt.Fill(e.gen_H2_b1_genfatjet_pt)


            # Investigating the events with four resolved b-quarks
            if (bIsResolvedReco):
                '''
                print("\n ============================================ Entry = %s is resolved (non-exclusive)" % (i)) 
                print(" H1 b1 matched with recojet = %s   with reco fatjet =%s   with pT=%s" % (bH1_b1_recojet, bH1_b1_recofatjet, round(e.gen_H1_b1_recofatjet_pt, 2)))
                print(" H1 b2 matched with recojet = %s   with reco fatjet =%s   with pT=%s" % (bH1_b2_recojet, bH1_b2_recofatjet, round(e.gen_H1_b2_recofatjet_pt, 2)))
                print(" H2 b1 matched with recojet = %s   with reco fatjet =%s   with pT=%s" % (bH2_b1_recojet, bH2_b1_recofatjet, round(e.gen_H2_b1_recofatjet_pt, 2)))
                print(" H2 b2 matched with recojet = %s   with reco fatjet =%s   with pT=%s" % (bH2_b2_recojet, bH2_b2_recofatjet, round(e.gen_H2_b2_recofatjet_pt, 2)))
                print(" Quarks matched to recojet = %s     to reco fatjet= %s" % (nBQuarksMatchedToRecoJets, nBQuarksMatchedToRecoFatJets))
                print("\n")
                print(" b_b11_b12_sameRecoFatjet = ", b_b11_b12_sameRecoFatjet)
                print(" b_b11_b21_sameRecoFatjet = ", b_b11_b21_sameRecoFatjet)
                print(" b_b11_b22_sameRecoFatjet = ", b_b11_b22_sameRecoFatjet)
                print(" b_b12_b21_sameRecoFatjet = ", b_b12_b21_sameRecoFatjet)
                print(" b_b12_b22_sameRecoFatjet = ", b_b12_b22_sameRecoFatjet)
                print(" b_b21_b22_sameRecoFatjet = ", b_b21_b22_sameRecoFatjet)
                '''
                if (nBQuarksMatchedToRecoFatJets == 4):
                    if bIsBoostedReco:
                        bIsResolvedRecoCases["10"]=True
                        h_GenMatchingTo4RecoJets_Cases.Fill(10)
                    else:
                        if (not (b_b11_b12_sameRecoFatjet or b_b11_b21_sameRecoFatjet or b_b11_b22_sameRecoFatjet or b_b12_b21_sameRecoFatjet or b_b12_b22_sameRecoFatjet or b_b21_b22_sameRecoFatjet)):
                            bIsResolvedRecoCases["11"]=True
                            h_GenMatchingTo4RecoJets_Cases.Fill(11)
                        else:
                            if ((b_b11_b21_sameRecoFatjet and b_b12_b22_sameRecoFatjet) or (b_b11_b22_sameRecoFatjet and b_b12_b21_sameRecoFatjet)):
                                bIsResolvedRecoCases["12"]=True
                                h_GenMatchingTo4RecoJets_Cases.Fill(12)
                            elif ((b_b11_b12_sameRecoFatjet and not b_b21_b22_sameRecoFatjet) or (b_b21_b22_sameRecoFatjet and not b_b11_b12_sameRecoFatjet)):
                                bIsResolvedRecoCases["13"]=True
                                h_GenMatchingTo4RecoJets_Cases.Fill(13)
                            elif ((b_b11_b21_sameRecoFatjet and not b_b12_b22_sameRecoFatjet) or (b_b11_b22_sameRecoFatjet and not b_b12_b21_sameRecoFatjet) or (b_b12_b21_sameRecoFatjet and not b_b11_b22_sameRecoFatjet) or (b_b12_b22_sameRecoFatjet and not b_b11_b21_sameRecoFatjet)):
                                bIsResolvedRecoCases["14"]=True
                                h_GenMatchingTo4RecoJets_Cases.Fill(14)
                            else:
                                print("Another case - this should never be reached!")
                elif (nBQuarksMatchedToRecoFatJets == 3):
                    if (b_b11_b12_sameRecoFatjet or b_b21_b22_sameRecoFatjet):
                        bIsResolvedRecoCases["7"] = True
                        h_GenMatchingTo4RecoJets_Cases.Fill(7)
                    elif (b_b11_b21_sameRecoFatjet or b_b12_b21_sameRecoFatjet or b_b11_b22_sameRecoFatjet or b_b12_b22_sameRecoFatjet):
                        bIsResolvedRecoCases["8"] = True
                        h_GenMatchingTo4RecoJets_Cases.Fill(8)
                    elif (not (b_b11_b12_sameRecoFatjet or b_b11_b21_sameRecoFatjet or b_b11_b22_sameRecoFatjet or b_b12_b21_sameRecoFatjet or b_b12_b22_sameRecoFatjet or b_b21_b22_sameRecoFatjet)):
                        bIsResolvedRecoCases["9"] = True
                        h_GenMatchingTo4RecoJets_Cases.Fill(9)
                    else:
                        print("Another case - this should never be reached! 3 b-quarks matched to gen-fatjets")
                elif (nBQuarksMatchedToRecoFatJets == 2):
                    
                    if ((bH1_b1_recofatjet and bH1_b2_recofatjet and b_b11_b12_sameRecoFatjet) or (bH2_b1_recofatjet and bH2_b2_recofatjet  and b_b21_b22_sameRecoFatjet)):
                        bIsResolvedRecoCases["6"] = True
                        h_GenMatchingTo4RecoJets_Cases.Fill(6)
                    elif (b_b11_b21_sameRecoFatjet or b_b11_b22_sameRecoFatjet or b_b12_b22_sameRecoFatjet or b_b12_b21_sameRecoFatjet):
                        bIsResolvedRecoCases["5"] = True
                        h_GenMatchingTo4RecoJets_Cases.Fill(5)
                    elif ((bH1_b1_recofatjet and bH1_b2_recofatjet and not b_b11_b12_sameRecoFatjet) or (bH2_b1_recofatjet and bH2_b2_recofatjet and not b_b21_b22_sameRecoFatjet)):
                        bIsResolvedRecoCases["4"] = True
                        h_GenMatchingTo4RecoJets_Cases.Fill(4)
                    else:
                        bIsResolvedRecoCases["3"] = True
                        h_GenMatchingTo4RecoJets_Cases.Fill(3)
                elif (nBQuarksMatchedToRecoFatJets == 1):
                    bIsResolvedRecoCases["2"] = True
                    h_GenMatchingTo4RecoJets_Cases.Fill(2)
                elif (nBQuarksMatchedToRecoFatJets == 0):
                    bIsResolvedRecoCases["1"] = True
                    h_GenMatchingTo4RecoJets_Cases.Fill(1)
                else:
                    print("This should never be reached")

            
            #====================================================================================================================
            h_GenPart_H1_pt.Fill(e.gen_H1_pt)
            h_GenPart_H2_pt.Fill(e.gen_H2_pt)
            h_GenPart_H1_eta.Fill(e.gen_H1_eta)
            h_GenPart_H2_eta.Fill(e.gen_H2_eta)
            h_GenPart_H1_b1_pt.Fill(e.gen_H1_b1_pt)
            h_GenPart_H1_b2_pt.Fill(e.gen_H1_b2_pt)
            h_GenPart_H2_b1_pt.Fill(e.gen_H2_b1_pt)
            h_GenPart_H2_b2_pt.Fill(e.gen_H2_b2_pt)
            h_GenPart_H1_b1_eta.Fill(e.gen_H1_b1_eta)
            h_GenPart_H1_b2_eta.Fill(e.gen_H1_b2_eta)
            h_GenPart_H2_b1_eta.Fill(e.gen_H2_b1_eta)
            h_GenPart_H2_b2_eta.Fill(e.gen_H2_b2_eta)
            h_NJets.Fill(e.n_jet)
            if (e.n_jet > 0): h_Jet1Pt.Fill(e.jet_pt.at(0))
            if (e.n_jet > 1): h_Jet2Pt.Fill(e.jet_pt.at(1))
            if (e.n_jet > 2): h_Jet3Pt.Fill(e.jet_pt.at(2))
            if (e.n_jet > 3): h_Jet4Pt.Fill(e.jet_pt.at(3))
            h_NFatJets.Fill(e.n_fatjet)
            if (e.n_fatjet > 0): h_AK8Jet1Pt.Fill(e.fatjet_pt.at(0))
            if (e.n_fatjet > 1): h_AK8Jet2Pt.Fill(e.fatjet_pt.at(1))
            if (e.n_fatjet > 2): h_AK8Jet3Pt.Fill(e.fatjet_pt.at(2))
            if (e.n_fatjet > 3): h_AK8Jet4Pt.Fill(e.fatjet_pt.at(3))
            nLoose = 0
            nMedium = 0
            nTight = 0
            for ij in range(0, e.n_jet):
                btag = e.jet_btag.at(ij)
                isLoose = btag > 0.0490
                isMedium = btag > 0.2783
                isTight = btag > 0.7100
                if (isLoose): nLoose += 1
                if (isMedium): nMedium += 1
                if (isTight): nTight += 1
            h_NLooseBJets.Fill(nLoose)
            h_NMediumBJets.Fill(nMedium)
            h_NTightBJets.Fill(nTight)

            #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
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
            if not (bIsResolvedReco or bIsSemiResolvedReco or bIsBoostedReco or bIsResolvedRecoExcl or bIsSemiResolvedRecoExcl or bIsBoostedRecoExcl):
                cNotMatchedReco += 1
                continue
            
                
            if (bIsResolvedReco and bIsBoostedReco):
                
                #print("\n ============================================ Entry = %s is resolved but also matched with two reco-fatjets" % (i)) 
                #print(" H1 b1 matched with recojet = %s   with reco fatjet =%s   with pT=%s" % (bH1_b1_recojet, bH1_b1_recofatjet, round(e.gen_H1_b1_recofatjet_pt, 2)))
                #print(" H1 b2 matched with recojet = %s   with reco fatjet =%s   with pT=%s" % (bH1_b2_recojet, bH1_b2_recofatjet, round(e.gen_H1_b2_recofatjet_pt, 2)))
                #print(" H2 b1 matched with recojet = %s   with reco fatjet =%s   with pT=%s" % (bH2_b1_recojet, bH2_b1_recofatjet, round(e.gen_H2_b1_recofatjet_pt, 2)))
                #print(" H2 b2 matched with recojet = %s   with reco fatjet =%s   with pT=%s" % (bH2_b2_recojet, bH2_b2_recofatjet, round(e.gen_H2_b2_recofatjet_pt, 2)))
                #print(" Quarks matched to recojet = %s     to reco fatjet= %s" % (nBQuarksMatchedToRecoJets, nBQuarksMatchedToRecoFatJets))
                #print("\n")
                DR_RecoFatJetH1_RecoFatJetH2 = deltaR(e.gen_H1_b1_recofatjet_eta, e.gen_H2_b2_recofatjet_eta, e.gen_H1_b1_recofatjet_phi, e.gen_H2_b2_recofatjet_phi)
                hResolved_MatchedToTwoFatJets_DR_RecoFatJetH1_RecoFatJetH2.Fill(DR_RecoFatJetH1_RecoFatJetH2)
                DR_RecoFatJetH1_b11 = deltaR(e.gen_H1_b1_recofatjet_eta, e.gen_H1_b1_recojet_eta, e.gen_H1_b1_recofatjet_phi, e.gen_H1_b1_recojet_phi)
                DR_RecoFatJetH1_b12 = deltaR(e.gen_H1_b1_recofatjet_eta, e.gen_H1_b2_recojet_eta, e.gen_H1_b1_recofatjet_phi, e.gen_H1_b2_recojet_phi)
                DR_b11_b12 = deltaR(e.gen_H1_b1_recojet_eta, e.gen_H1_b2_recojet_eta, e.gen_H1_b1_recojet_phi, e.gen_H1_b2_recojet_phi)
                hResolved_MatchedToTwoFatJets_DR_RecoFatJetH1_b11.Fill(DR_RecoFatJetH1_b11)
                hResolved_MatchedToTwoFatJets_DR_RecoFatJetH1_b12.Fill(DR_RecoFatJetH1_b12)
                hResolved_MatchedToTwoFatJets_DR_b11_b12.Fill(DR_b11_b12)
                DR_RecoFatJetH2_b21 = deltaR(e.gen_H2_b1_recofatjet_eta, e.gen_H2_b1_recojet_eta, e.gen_H2_b1_recofatjet_phi, e.gen_H2_b1_recojet_phi)
                DR_RecoFatJetH2_b22 = deltaR(e.gen_H2_b2_recofatjet_eta, e.gen_H2_b2_recojet_eta, e.gen_H2_b2_recofatjet_phi, e.gen_H2_b2_recojet_phi)
                DR_b21_b22 = deltaR(e.gen_H2_b1_recojet_eta, e.gen_H2_b2_recojet_eta, e.gen_H2_b1_recojet_phi, e.gen_H2_b2_recojet_phi)
                hResolved_MatchedToTwoFatJets_DR_RecoFatJetH2_b21.Fill(DR_RecoFatJetH2_b21)
                hResolved_MatchedToTwoFatJets_DR_RecoFatJetH2_b22.Fill(DR_RecoFatJetH2_b22)
                hResolved_MatchedToTwoFatJets_DR_b21_b22.Fill(DR_b21_b22)
                #print(" DR H1 H2   = ", DR_RecoFatJetH1_RecoFatJetH2)
                #print(" DR H1 b11  = ", DR_RecoFatJetH1_b11)
                #print(" DR H1 b12  = ", DR_RecoFatJetH1_b12)
                #print(" DR b11 b12 = ", DR_b11_b12)
                #print("\n")
                #print(" DR H2 b21  = ", DR_RecoFatJetH2_b21)
                #print(" DR H2 b22  = ", DR_RecoFatJetH2_b22)
                #print(" DR b21 b22 = ", DR_b21_b22)
                
            if (bIsResolvedReco and bIsSemiResolvedReco):
                '''
                print("\n ============================================ Entry = %s is resolved but also one Higgs is matched to a reco-fatjet" % (i))
                print(" H1 b1 matched with recojet = %s   with reco fatjet =%s   with pT=%s" % (bH1_b1_recojet, bH1_b1_recofatjet, round(e.gen_H1_b1_recofatjet_pt, 2)))
                print(" H1 b2 matched with recojet = %s   with reco fatjet =%s   with pT=%s" % (bH1_b2_recojet, bH1_b2_recofatjet, round(e.gen_H1_b2_recofatjet_pt, 2)))
                print(" H2 b1 matched with recojet = %s   with reco fatjet =%s   with pT=%s" % (bH2_b1_recojet, bH2_b1_recofatjet, round(e.gen_H2_b1_recofatjet_pt, 2)))
                print(" H2 b2 matched with recojet = %s   with reco fatjet =%s   with pT=%s" % (bH2_b2_recojet, bH2_b2_recofatjet, round(e.gen_H2_b2_recofatjet_pt, 2)))
                print(" Quarks matched to recojet = %s     to reco fatjet= %s" % (nBQuarksMatchedToRecoJets, nBQuarksMatchedToRecoFatJets))
                print("\n")
                '''
                if bH1Boosted_H2resolved_reco:

                    # Find the H2 p4
                    reco_H2_b1_p4 = getP4(e.gen_H2_b1_recojet_pt, e.gen_H2_b1_recojet_eta, e.gen_H2_b1_recojet_phi, e.gen_H2_b1_recojet_m)
                    reco_H2_b2_p4 = getP4(e.gen_H2_b2_recojet_pt, e.gen_H2_b2_recojet_eta, e.gen_H2_b2_recojet_phi, e.gen_H2_b2_recojet_m)
                    reco_H2 = reco_H2_b1_p4 + reco_H2_b2_p4
                    
                    DR_RecoFatJetH1_RecoJetH2 = deltaR(e.gen_H1_b1_recofatjet_eta, reco_H2.Eta(), e.gen_H1_b1_recofatjet_phi, reco_H2.Phi())
                    DR_RecoFatJetH1_b11       = deltaR(e.gen_H1_b1_recofatjet_eta, e.gen_H1_b1_recojet_eta, e.gen_H1_b1_recofatjet_phi, e.gen_H1_b1_recojet_phi)
                    DR_RecoFatJetH1_b12       = deltaR(e.gen_H1_b1_recofatjet_eta, e.gen_H1_b2_recojet_eta, e.gen_H1_b1_recofatjet_phi, e.gen_H1_b2_recojet_phi)
                    DR_b11_b12                = deltaR(e.gen_H1_b1_recojet_eta, e.gen_H1_b2_recojet_eta, e.gen_H1_b1_recojet_phi, e.gen_H1_b2_recojet_phi)
                    
                    DR_RecoH2_b21 = deltaR(reco_H2.Eta(), e.gen_H2_b1_recojet_eta, reco_H2.Phi(), e.gen_H2_b1_recojet_phi)
                    DR_RecoH2_b22 = deltaR(reco_H2.Eta(), e.gen_H2_b2_recojet_eta, reco_H2.Phi(), e.gen_H2_b2_recojet_phi)
                    DR_b21_b22    = deltaR(e.gen_H2_b1_recojet_eta,  e.gen_H2_b2_recojet_eta, e.gen_H2_b1_recojet_phi,  e.gen_H2_b2_recojet_phi)
                    '''
                    print(" DR(H1 fatjet, H2 reconstructed) = ", DR_RecoFatJetH1_RecoJetH2)
                    print(" DR(H1 fatjet, b11)              = ", DR_RecoFatJetH1_b11)
                    print(" DR(H1 fatjet, b12)              = ", DR_RecoFatJetH1_b12)
                    print(" DR(b11, b12)                    = ", DR_b11_b12)
                    print(" DR(H2 reco, b21)                = ", DR_RecoH2_b21)
                    print(" DR(H2 reco, b22)                = ", DR_RecoH2_b22)
                    print(" DR(b21, b22)                    = ", DR_b21_b22)
                    '''
                    hResolved_MatchedToOneFatJet_DR_RecoFatJetH1_RecoH2.Fill(DR_RecoFatJetH1_RecoJetH2)
                    hResolved_MatchedToOneFatJet_DR_RecoFatJetH1_b11.Fill(DR_RecoFatJetH1_b11)
                    hResolved_MatchedToOneFatJet_DR_RecoFatJetH1_b12.Fill(DR_RecoFatJetH1_b12)
                    hResolved_MatchedToOneFatJet_DR_b11_b12.Fill(DR_b11_b12)
                    hResolved_MatchedToOneFatJet_DR_RecoH2_b21.Fill(DR_RecoH2_b21)
                    hResolved_MatchedToOneFatJet_DR_RecoH2_b22.Fill(DR_RecoH2_b22)
                    hResolved_MatchedToOneFatJet_DR_b21_b22.Fill(DR_b21_b22)
    
            if (bIsBoostedRecoExcl):
                hBoostedExclPassed_HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5.Fill(bPassed_HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5)
                hBoostedExclPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np4.Fill(bPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np4)
                hBoostedExclPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np2.Fill(bPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np2)
                hBoostedExclPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p1.Fill(bPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p1)
                hBoostedExclPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p17.Fill(bPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p17)
                hBoostedExclPassed_HLT_PFHT1050.Fill(bPassed_HLT_PFHT1050)
                hBoostedExclPassed_HLT_PFJet500.Fill(bPassed_HLT_PFJet500)
                hBoostedExclPassed_HLT_AK8PFHT800_TrimMass50.Fill(bPassed_HLT_AK8PFHT800_TrimMass50)
                hBoostedExclPassed_HLT_AK8PFJet400_TrimMass30.Fill(bPassed_HLT_AK8PFJet400_TrimMass30)
                hBoostedExclPassed_HLT_AK8PFJet420_TrimMass30.Fill(bPassed_HLT_AK8PFJet420_TrimMass30)
                hBoostedExclPassed_HLT_AK8PFJet500.Fill(bPassed_HLT_AK8PFJet500)
                hBoostedExclPassed_HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59.Fill(bPassed_HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59)
                hBoostedExclPassed_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94.Fill(bPassed_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94)
                hBoostedExclPassed_HLT_AK8PFHT750_TrimMass50.Fill(bPassed_HLT_AK8PFHT750_TrimMass50)
                hBoostedExclPassed_HLT_AK8PFJet360_TrimMass30.Fill(bPassed_HLT_AK8PFJet360_TrimMass30)
                hBoostedExclPassed_HLT_AK8PFJet380_TrimMass30.Fill(bPassed_HLT_AK8PFJet380_TrimMass30)
                hBoostedExclPassed_OR.Fill(bPassed_OR)
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
                

            if (bIsSemiResolvedRecoExcl):
                hSemiresolvedExclPassed_HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5.Fill(bPassed_HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5)
                hSemiresolvedExclPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np4.Fill(bPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np4)
                hSemiresolvedExclPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np2.Fill(bPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np2)
                hSemiresolvedExclPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p1.Fill(bPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p1)
                hSemiresolvedExclPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p17.Fill(bPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p17)
                hSemiresolvedExclPassed_HLT_PFHT1050.Fill(bPassed_HLT_PFHT1050)
                hSemiresolvedExclPassed_HLT_PFJet500.Fill(bPassed_HLT_PFJet500)
                hSemiresolvedExclPassed_HLT_AK8PFHT800_TrimMass50.Fill(bPassed_HLT_AK8PFHT800_TrimMass50)
                hSemiresolvedExclPassed_HLT_AK8PFJet400_TrimMass30.Fill(bPassed_HLT_AK8PFJet400_TrimMass30)
                hSemiresolvedExclPassed_HLT_AK8PFJet420_TrimMass30.Fill(bPassed_HLT_AK8PFJet420_TrimMass30)
                hSemiresolvedExclPassed_HLT_AK8PFJet500.Fill(bPassed_HLT_AK8PFJet500)
                hSemiresolvedExclPassed_HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59.Fill(bPassed_HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59)
                hSemiresolvedExclPassed_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94.Fill(bPassed_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94)
                hSemiresolvedExclPassed_HLT_AK8PFHT750_TrimMass50.Fill(bPassed_HLT_AK8PFHT750_TrimMass50)
                hSemiresolvedExclPassed_HLT_AK8PFJet360_TrimMass30.Fill(bPassed_HLT_AK8PFJet360_TrimMass30)
                hSemiresolvedExclPassed_HLT_AK8PFJet380_TrimMass30.Fill(bPassed_HLT_AK8PFJet380_TrimMass30)
                hSemiresolvedExclPassed_OR.Fill(bPassed_OR)

                hSemiresolvedExcl_GenPart_H1_pt.Fill(e.gen_H1_pt)
                hSemiresolvedExcl_GenPart_H2_pt.Fill(e.gen_H2_pt)
                hSemiresolvedExcl_GenPart_H1_b1_pt.Fill(e.gen_H1_b1_pt)
                hSemiresolvedExcl_GenPart_H1_b2_pt.Fill(e.gen_H1_b2_pt)
                hSemiresolvedExcl_GenPart_H2_b1_pt.Fill(e.gen_H2_b1_pt)
                hSemiresolvedExcl_GenPart_H2_b2_pt.Fill(e.gen_H2_b2_pt)
                hSemiresolvedExcl_GenPart_H1_b1_eta.Fill(e.gen_H1_b1_eta)
                hSemiresolvedExcl_GenPart_H1_b2_eta.Fill(e.gen_H1_b2_eta)
                hSemiresolvedExcl_GenPart_H2_b1_eta.Fill(e.gen_H2_b1_eta)
                hSemiresolvedExcl_GenPart_H2_b2_eta.Fill(e.gen_H2_b2_eta)
                if (bH1Boosted_H2resolved_reco):
                    hSemiresolvedExcl_H1Boosted_H2resolved_GenFatJet_H1_pt.Fill(e.gen_H1_b1_genfatjet_pt)
                    hSemiresolvedExcl_H1Boosted_H2resolved_GenFatJet_H1_eta.Fill(e.gen_H1_b1_genfatjet_eta)
                    hSemiresolvedExcl_H1Boosted_H2resolved_GenJet_H2_b1_pt.Fill(e.gen_H2_b1_genjet_pt)
                    hSemiresolvedExcl_H1Boosted_H2resolved_GenJet_H2_b2_pt.Fill(e.gen_H2_b2_genjet_pt)
                    hSemiresolvedExcl_H1Boosted_H2resolved_GenJet_H2_b1_eta.Fill(e.gen_H2_b1_genjet_eta)
                    hSemiresolvedExcl_H1Boosted_H2resolved_GenJet_H2_b2_eta.Fill(e.gen_H2_b2_genjet_eta)
                    hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_pt.Fill(e.gen_H1_b1_recofatjet_pt)
                    hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_eta.Fill(e.gen_H1_b1_recofatjet_eta)
                    hSemiresolvedExcl_H1Boosted_H2resolved_RecoJet_H2_b1_pt.Fill(e.gen_H2_b1_recojet_pt)
                    hSemiresolvedExcl_H1Boosted_H2resolved_RecoJet_H2_b2_pt.Fill(e.gen_H2_b2_recojet_pt)
                    hSemiresolvedExcl_H1Boosted_H2resolved_RecoJet_H2_b1_eta.Fill(e.gen_H2_b1_recojet_eta)
                    hSemiresolvedExcl_H1Boosted_H2resolved_RecoJet_H2_b2_eta.Fill(e.gen_H2_b2_recojet_eta)
                    hSemiresolvedExcl_H1Boosted_H2resolved_NJets.Fill(e.n_jet)
                    hSemiresolvedExcl_H1Boosted_H2resolved_NFatJets.Fill(e.n_fatjet)
                    
                    # RecoJets matched
                    reco_H2_b1_p4 = getP4(e.gen_H2_b1_recojet_pt, e.gen_H2_b1_recojet_eta, e.gen_H2_b1_recojet_phi, e.gen_H2_b1_recojet_m)
                    reco_H2_b2_p4 = getP4(e.gen_H2_b2_recojet_pt, e.gen_H2_b2_recojet_eta, e.gen_H2_b2_recojet_phi, e.gen_H2_b2_recojet_m)
                    reco_H2 = reco_H2_b1_p4 + reco_H2_b2_p4
                    
                    hSemiresolvedExcl_H1Boosted_H2resolved_H2_pt.Fill(reco_H2.Pt())
                    hSemiresolvedExcl_H1Boosted_H2resolved_H2_eta.Fill(reco_H2.Eta())
                    hSemiresolvedExcl_H1Boosted_H2resolved_InvMass_H2.Fill(reco_H2.M())
                    hSemiresolvedExcl_H1Boosted_H2resolved_DeltaR_H1_H2.Fill(deltaR(e.gen_H1_b1_recofatjet_eta, reco_H2.Eta(), e.gen_H1_b1_recofatjet_phi, reco_H2.Phi()))
                    hSemiresolvedExcl_H1Boosted_H2resolved_DeltaEta_H1_H2.Fill(abs(e.gen_H1_b1_recofatjet_eta - reco_H2.Eta()))
                    hSemiresolvedExcl_H1Boosted_H2resolved_DeltaPhi_H1_H2.Fill(deltaPhi(e.gen_H1_b1_recofatjet_phi, reco_H2.Phi()))
                    
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

                    hSemiresolvedExcl_H1Boosted_H2resolved_PFHT.Fill(reco_PFHT)
                    hSemiresolvedExcl_H1Boosted_H2resolved_NLooseBJets.Fill(nLoose)
                    hSemiresolvedExcl_H1Boosted_H2resolved_NMediumBJets.Fill(nMedium)
                    hSemiresolvedExcl_H1Boosted_H2resolved_NTightBJets.Fill(nTight)
                    if (e.n_jet > 0): hSemiresolvedExcl_H1Boosted_H2resolved_Jet1Pt.Fill(e.jet_pt.at(0))
                    if (e.n_jet > 1): hSemiresolvedExcl_H1Boosted_H2resolved_Jet2Pt.Fill(e.jet_pt.at(1))
                    if (e.n_jet > 2): hSemiresolvedExcl_H1Boosted_H2resolved_Jet3Pt.Fill(e.jet_pt.at(2))
                    if (e.n_jet > 3): hSemiresolvedExcl_H1Boosted_H2resolved_Jet4Pt.Fill(e.jet_pt.at(3))
                    if (e.n_jet > 0): hSemiresolvedExcl_H1Boosted_H2resolved_Jet1Eta.Fill(e.jet_eta.at(0))
                    if (e.n_jet > 1): hSemiresolvedExcl_H1Boosted_H2resolved_Jet2Eta.Fill(e.jet_eta.at(1))
                    if (e.n_jet > 2): hSemiresolvedExcl_H1Boosted_H2resolved_Jet3Eta.Fill(e.jet_eta.at(2))
                    if (e.n_jet > 3): hSemiresolvedExcl_H1Boosted_H2resolved_Jet4Eta.Fill(e.jet_eta.at(3))
                    if (e.n_fatjet > 0):
                        hSemiresolvedExcl_H1Boosted_H2resolved_AK8Jet1Pt.Fill(e.fatjet_pt.at(0))

                    if bFound_reco_H2_b1 and bFound_reco_H2_b2:
                        reco_H2_p4Regressed = reco_H2_b1_p4Regressed + reco_H2_b2_p4Regressed
                        hSemiresolvedExcl_H1Boosted_H2resolved_InvMassRegressed_H2.Fill(reco_H2_p4Regressed.M())

                    AK8PFHT = 0.0
                    for ij in range(0, e.n_fatjet):
                        eta = e.fatjet_eta.at(ij)
                        phi = e.fatjet_phi.at(ij)
                        mass = e.fatjet_m.at(ij)
                        PXbb = e.fatjet_PNetXbb.at(ij)
                        PXcc = e.fatjet_PNetXcc.at(ij)
                        PXqq = e.fatjet_PNetXqq.at(ij)
                        pt = e.fatjet_pt.at(ij)
                        AK8PFHT += pt
                        TXbb = PXbb/(1-PXcc-PXqq)
                        
                        if (areSameJets(eta, e.gen_H1_b1_recofatjet_eta, phi, e.gen_H1_b1_recofatjet_phi)):
                            hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_m.Fill(mass)
                            hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_TXbb.Fill(TXbb)
                            hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_mSD_Uncorrected.Fill(e.fatjet_mSD_UnCorrected.at(ij))
                            hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_area.Fill(e.fatjet_area.at(ij))
                            hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_n2b1.Fill(e.fatjet_n2b1.at(ij))
                            hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_n3b1.Fill(e.fatjet_n3b1.at(ij))
                            hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_tau21.Fill(e.fatjet_tau2.at(ij)/e.fatjet_tau1.at(ij))
                            hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_tau32.Fill(e.fatjet_tau3.at(ij)/e.fatjet_tau2.at(ij))
                            hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_nsubjets.Fill(e.fatjet_nsubjets.at(ij))
                            if (e.fatjet_nsubjets.at(ij) > 0):
                                hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_pt.Fill(e.fatjet_subjet1_pt.at(ij))
                                hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_eta.Fill(e.fatjet_subjet1_eta.at(ij))
                                hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_m.Fill(e.fatjet_subjet1_m.at(ij))
                                hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_btag.Fill(e.fatjet_subjet1_btagDeepB.at(ij))
                            if (e.fatjet_nsubjets.at(ij) > 1):
                                hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_pt.Fill(e.fatjet_subjet2_pt.at(ij))
                                hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_eta.Fill(e.fatjet_subjet2_eta.at(ij))
                                hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_m.Fill(e.fatjet_subjet2_m.at(ij))
                                hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_btag.Fill(e.fatjet_subjet2_btagDeepB.at(ij))
                    hSemiresolvedExcl_H1Boosted_H2resolved_AK8PFHT.Fill(AK8PFHT)

                if (bH2Boosted_H1resolved_reco):
                    hSemiresolvedExcl_H2Boosted_H1resolved_GenFatJet_H2_pt.Fill(e.gen_H2_b1_genfatjet_pt)
                    hSemiresolvedExcl_H2Boosted_H1resolved_GenFatJet_H2_eta.Fill(e.gen_H2_b1_genfatjet_eta)
                    hSemiresolvedExcl_H2Boosted_H1resolved_GenJet_H1_b1_pt.Fill(e.gen_H1_b1_genjet_pt)
                    hSemiresolvedExcl_H2Boosted_H1resolved_GenJet_H1_b2_pt.Fill(e.gen_H1_b2_genjet_pt)
                    hSemiresolvedExcl_H2Boosted_H1resolved_GenJet_H1_b1_eta.Fill(e.gen_H1_b1_genjet_eta)
                    hSemiresolvedExcl_H2Boosted_H1resolved_GenJet_H1_b2_eta.Fill(e.gen_H1_b2_genjet_eta)
                    hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_pt.Fill(e.gen_H2_b1_recofatjet_pt)
                    hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_eta.Fill(e.gen_H2_b1_recofatjet_eta)
                    hSemiresolvedExcl_H2Boosted_H1resolved_RecoJet_H1_b1_pt.Fill(e.gen_H1_b1_recojet_pt)
                    hSemiresolvedExcl_H2Boosted_H1resolved_RecoJet_H1_b2_pt.Fill(e.gen_H1_b2_recojet_pt)
                    hSemiresolvedExcl_H2Boosted_H1resolved_RecoJet_H1_b1_eta.Fill(e.gen_H1_b1_recojet_eta)
                    hSemiresolvedExcl_H2Boosted_H1resolved_RecoJet_H1_b2_eta.Fill(e.gen_H1_b2_recojet_eta)
                    hSemiresolvedExcl_H2Boosted_H1resolved_NJets.Fill(e.n_jet)
                    hSemiresolvedExcl_H2Boosted_H1resolved_NFatJets.Fill(e.n_fatjet)
                    
                    # RecoJets matched
                    reco_H1_b1_p4 = getP4(e.gen_H1_b1_recojet_pt, e.gen_H1_b1_recojet_eta, e.gen_H1_b1_recojet_phi, e.gen_H1_b1_recojet_m)
                    reco_H1_b2_p4 = getP4(e.gen_H1_b2_recojet_pt, e.gen_H1_b2_recojet_eta, e.gen_H1_b2_recojet_phi, e.gen_H1_b2_recojet_m)
                    reco_H1 = reco_H1_b1_p4 + reco_H1_b2_p4
                    hSemiresolvedExcl_H2Boosted_H1resolved_DeltaR_H1_H2.Fill(deltaR(e.gen_H2_b1_recofatjet_eta, reco_H1.Eta(), e.gen_H2_b1_recofatjet_phi, reco_H1.Phi()))
                    hSemiresolvedExcl_H2Boosted_H1resolved_DeltaEta_H1_H2.Fill(abs(e.gen_H2_b1_recofatjet_eta - reco_H1.Eta()))
                    hSemiresolvedExcl_H2Boosted_H1resolved_DeltaPhi_H1_H2.Fill(deltaPhi(e.gen_H2_b1_recofatjet_phi, reco_H1.Phi()))
                    hSemiresolvedExcl_H2Boosted_H1resolved_InvMass_H1.Fill(reco_H1.M())
                    hSemiresolvedExcl_H2Boosted_H1resolved_H1_pt.Fill(reco_H1.Pt())
                    hSemiresolvedExcl_H2Boosted_H1resolved_H1_eta.Fill(reco_H1.Eta())
                    hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_m.Fill(e.gen_H2_b1_recofatjet_m)
                    
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
                        hSemiresolvedExcl_H2Boosted_H1resolved_InvMassRegressed_H1.Fill(reco_H1_p4Regressed.M())
                    AK8PFHT = 0.0
                    for ij in range(0, e.n_fatjet):
                        eta = e.fatjet_eta.at(ij)
                        phi = e.fatjet_phi.at(ij)
                        pt  = e.fatjet_pt.at(ij)
                        
                        AK8PFHT+= pt
                        PXbb = e.fatjet_PNetXbb.at(ij)
                        PXcc = e.fatjet_PNetXcc.at(ij)
                        PXqq = e.fatjet_PNetXqq.at(ij)
                        
                        TXbb = PXbb/(1-PXcc-PXqq)
                        if (areSameJets(eta, e.gen_H2_b1_recofatjet_eta, phi, e.gen_H2_b1_recofatjet_phi)):
                            hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_TXbb.Fill(TXbb)
                            hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_mSD_Uncorrected.Fill(e.fatjet_mSD_UnCorrected.at(ij))
                            hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_area.Fill(e.fatjet_area.at(ij))
                            hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_n2b1.Fill(e.fatjet_n2b1.at(ij))
                            hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_n3b1.Fill(e.fatjet_n3b1.at(ij))
                            hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_tau21.Fill(e.fatjet_tau2.at(ij)/e.fatjet_tau1.at(ij))
                            hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_tau32.Fill(e.fatjet_tau3.at(ij)/e.fatjet_tau2.at(ij))
                            hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_nsubjets.Fill(e.fatjet_nsubjets.at(ij))
                            if (e.fatjet_nsubjets.at(ij) > 0):
                                hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_pt.Fill(e.fatjet_subjet1_pt.at(ij))
                                hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_eta.Fill(e.fatjet_subjet1_eta.at(ij))
                                hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_m.Fill(e.fatjet_subjet1_m.at(ij))
                                hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_btag.Fill(e.fatjet_subjet1_btagDeepB.at(ij))
                            if (e.fatjet_nsubjets.at(ij) > 1):
                                hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_pt.Fill(e.fatjet_subjet2_pt.at(ij))
                                hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_eta.Fill(e.fatjet_subjet2_eta.at(ij))
                                hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_m.Fill(e.fatjet_subjet2_m.at(ij))
                                hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_btag.Fill(e.fatjet_subjet2_btagDeepB.at(ij))
                    hSemiresolvedExcl_H2Boosted_H1resolved_AK8PFHT.Fill(AK8PFHT)
            #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            # Semiresolved category
            #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
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
                if (bH1Boosted_H2resolved_reco):
                    hSemiresolved_H1Boosted_H2resolved_GenFatJet_H1_pt.Fill(e.gen_H1_b1_genfatjet_pt)
                    hSemiresolved_H1Boosted_H2resolved_GenFatJet_H1_eta.Fill(e.gen_H1_b1_genfatjet_eta)
                    hSemiresolved_H1Boosted_H2resolved_GenJet_H2_b1_pt.Fill(e.gen_H2_b1_genjet_pt)
                    hSemiresolved_H1Boosted_H2resolved_GenJet_H2_b2_pt.Fill(e.gen_H2_b2_genjet_pt)
                    hSemiresolved_H1Boosted_H2resolved_GenJet_H2_b1_eta.Fill(e.gen_H2_b1_genjet_eta)
                    hSemiresolved_H1Boosted_H2resolved_GenJet_H2_b2_eta.Fill(e.gen_H2_b2_genjet_eta)
                    hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_pt.Fill(e.gen_H1_b1_recofatjet_pt)
                    hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_eta.Fill(e.gen_H1_b1_recofatjet_eta)
                    hSemiresolved_H1Boosted_H2resolved_RecoJet_H2_b1_pt.Fill(e.gen_H2_b1_recojet_pt)
                    hSemiresolved_H1Boosted_H2resolved_RecoJet_H2_b2_pt.Fill(e.gen_H2_b2_recojet_pt)
                    hSemiresolved_H1Boosted_H2resolved_RecoJet_H2_b1_eta.Fill(e.gen_H2_b1_recojet_eta)
                    hSemiresolved_H1Boosted_H2resolved_RecoJet_H2_b2_eta.Fill(e.gen_H2_b2_recojet_eta)
                    hSemiresolved_H1Boosted_H2resolved_NJets.Fill(e.n_jet)
                    hSemiresolved_H1Boosted_H2resolved_NFatJets.Fill(e.n_fatjet)
                    
                    # RecoJets matched
                    reco_H2_b1_p4 = getP4(e.gen_H2_b1_recojet_pt, e.gen_H2_b1_recojet_eta, e.gen_H2_b1_recojet_phi, e.gen_H2_b1_recojet_m)
                    reco_H2_b2_p4 = getP4(e.gen_H2_b2_recojet_pt, e.gen_H2_b2_recojet_eta, e.gen_H2_b2_recojet_phi, e.gen_H2_b2_recojet_m)
                    reco_H2 = reco_H2_b1_p4 + reco_H2_b2_p4
                    
                    hSemiresolved_H1Boosted_H2resolved_H2_pt.Fill(reco_H2.Pt())
                    hSemiresolved_H1Boosted_H2resolved_H2_eta.Fill(reco_H2.Eta())
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

                    AK8PFHT = 0.0
                    for ij in range(0, e.n_fatjet):
                        eta = e.fatjet_eta.at(ij)
                        phi = e.fatjet_phi.at(ij)
                        pt = e.fatjet_pt.at(ij)
                        mass = e.fatjet_m.at(ij)
                        PXbb = e.fatjet_PNetXbb.at(ij)
                        PXcc = e.fatjet_PNetXcc.at(ij)
                        PXqq = e.fatjet_PNetXqq.at(ij)
                        
                        TXbb = PXbb/(1-PXcc-PXqq)
                        AK8PFHT += pt
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
                                hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_m.Fill(e.fatjet_subjet1_m.at(ij))
                                hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_btag.Fill(e.fatjet_subjet1_btagDeepB.at(ij))
                            if (e.fatjet_nsubjets.at(ij) > 1):
                                hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_pt.Fill(e.fatjet_subjet2_pt.at(ij))
                                hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_eta.Fill(e.fatjet_subjet2_eta.at(ij))
                                hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_m.Fill(e.fatjet_subjet2_m.at(ij))
                                hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_btag.Fill(e.fatjet_subjet2_btagDeepB.at(ij))

                    hSemiresolved_H1Boosted_H2resolved_AK8PFHT.Fill(AK8PFHT)
                                
                if (bH2Boosted_H1resolved_reco):
                    hSemiresolved_H2Boosted_H1resolved_GenFatJet_H2_pt.Fill(e.gen_H2_b1_genfatjet_pt)
                    hSemiresolved_H2Boosted_H1resolved_GenFatJet_H2_eta.Fill(e.gen_H2_b1_genfatjet_eta)
                    hSemiresolved_H2Boosted_H1resolved_GenJet_H1_b1_pt.Fill(e.gen_H1_b1_genjet_pt)
                    hSemiresolved_H2Boosted_H1resolved_GenJet_H1_b2_pt.Fill(e.gen_H1_b2_genjet_pt)
                    hSemiresolved_H2Boosted_H1resolved_GenJet_H1_b1_eta.Fill(e.gen_H1_b1_genjet_eta)
                    hSemiresolved_H2Boosted_H1resolved_GenJet_H1_b2_eta.Fill(e.gen_H1_b2_genjet_eta)
                    hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_pt.Fill(e.gen_H2_b1_recofatjet_pt)
                    hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_eta.Fill(e.gen_H2_b1_recofatjet_eta)
                    hSemiresolved_H2Boosted_H1resolved_RecoJet_H1_b1_pt.Fill(e.gen_H1_b1_recojet_pt)
                    hSemiresolved_H2Boosted_H1resolved_RecoJet_H1_b2_pt.Fill(e.gen_H1_b2_recojet_pt)
                    hSemiresolved_H2Boosted_H1resolved_RecoJet_H1_b1_eta.Fill(e.gen_H1_b1_recojet_eta)
                    hSemiresolved_H2Boosted_H1resolved_RecoJet_H1_b2_eta.Fill(e.gen_H1_b2_recojet_eta)
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
                    
                    AK8PFHT = 0.0
                    for ij in range(0, e.n_fatjet):
                        eta = e.fatjet_eta.at(ij)
                        phi = e.fatjet_phi.at(ij)
                        pt  = e.fatjet_pt.at(ij)
                        
                        PXbb = e.fatjet_PNetXbb.at(ij)
                        PXcc = e.fatjet_PNetXcc.at(ij)
                        PXqq = e.fatjet_PNetXqq.at(ij)
                        
                        AK8PFHT += pt
                        
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
                                hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_m.Fill(e.fatjet_subjet1_m.at(ij))
                                hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_btag.Fill(e.fatjet_subjet1_btagDeepB.at(ij))
                            if (e.fatjet_nsubjets.at(ij) > 1):
                                hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_pt.Fill(e.fatjet_subjet2_pt.at(ij))
                                hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_eta.Fill(e.fatjet_subjet2_eta.at(ij))
                                hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_m.Fill(e.fatjet_subjet2_m.at(ij))
                                hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_btag.Fill(e.fatjet_subjet2_btagDeepB.at(ij))
                    hSemiresolved_H2Boosted_H1resolved_AK8PFHT.Fill(AK8PFHT)
            
                    
            #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            # Boosted reco category:
            #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
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
                hBoosted_GenFatJet_H1_pt.Fill(e.gen_H1_b1_genfatjet_pt)
                hBoosted_GenFatJet_H2_pt.Fill(e.gen_H2_b2_genfatjet_pt)
                hBoosted_GenFatJet_H1_eta.Fill(e.gen_H1_b1_genfatjet_eta)
                hBoosted_GenFatJet_H2_eta.Fill(e.gen_H2_b2_genfatjet_eta)
                hBoosted_RecoFatJet_H1_pt.Fill(e.gen_H1_b1_recofatjet_pt)
                hBoosted_RecoFatJet_H2_pt.Fill(e.gen_H2_b1_recofatjet_pt)
                hBoosted_RecoFatJet_H1_eta.Fill(e.gen_H1_b1_recofatjet_eta)
                hBoosted_RecoFatJet_H2_eta.Fill(e.gen_H2_b2_recofatjet_eta)
                                
                hBoosted_RecoFatJet_H1_m.Fill(e.gen_H1_b1_recofatjet_m)
                hBoosted_RecoFatJet_H2_m.Fill(e.gen_H2_b1_recofatjet_m)
                hBoosted_NJets.Fill(e.n_jet)
                hBoosted_NFatJets.Fill(e.n_fatjet)
                hBoosted_RecoFatJet_DeltaR_H1_H2.Fill(deltaR(e.gen_H1_b1_genfatjet_eta, e.gen_H2_b2_genfatjet_eta, e.gen_H1_b1_genfatjet_phi, e.gen_H2_b2_genfatjet_phi))
                hBoosted_RecoFatJet_DeltaEta_H1_H2.Fill(abs(e.gen_H1_b1_genfatjet_eta - e.gen_H2_b2_genfatjet_eta))
                hBoosted_RecoFatJet_DeltaPhi_H1_H2.Fill(deltaPhi(e.gen_H1_b1_genfatjet_phi, e.gen_H2_b2_genfatjet_phi))
                
                AK8PFHT = 0.0
                for ij in range(0, e.n_fatjet):
                    eta = e.fatjet_eta.at(ij)
                    phi = e.fatjet_phi.at(ij)
                    pt  = e.fatjet_pt.at(ij)
                    
                    AK8PFHT+=pt
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
                            hBoosted_RecoFatJet_H1_subjet1_m.Fill(e.fatjet_subjet1_m.at(ij))
                            hBoosted_RecoFatJet_H1_subjet1_btag.Fill(e.fatjet_subjet1_btagDeepB.at(ij))
                        if (e.fatjet_nsubjets.at(ij) > 1):
                            hBoosted_RecoFatJet_H1_subjet2_pt.Fill(e.fatjet_subjet2_pt.at(ij))
                            hBoosted_RecoFatJet_H1_subjet2_eta.Fill(e.fatjet_subjet2_eta.at(ij))
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
                            hBoosted_RecoFatJet_H2_subjet1_m.Fill(e.fatjet_subjet1_m.at(ij))
                            hBoosted_RecoFatJet_H2_subjet1_btag.Fill(e.fatjet_subjet1_btagDeepB.at(ij))
                        if (e.fatjet_nsubjets.at(ij) > 1):
                            hBoosted_RecoFatJet_H2_subjet2_pt.Fill(e.fatjet_subjet2_pt.at(ij))
                            hBoosted_RecoFatJet_H2_subjet2_eta.Fill(e.fatjet_subjet2_eta.at(ij))
                            hBoosted_RecoFatJet_H2_subjet2_m.Fill(e.fatjet_subjet2_m.at(ij))
                            hBoosted_RecoFatJet_H2_subjet2_btag.Fill(e.fatjet_subjet2_btagDeepB.at(ij))

                hBoosted_AK8PFHT.Fill(AK8PFHT)

            #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            # Boosted reco exclusive category:
            #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            if (bIsBoostedRecoExcl):
                hBoostedExcl_GenPart_H1_pt.Fill(e.gen_H1_pt)
                hBoostedExcl_GenPart_H2_pt.Fill(e.gen_H2_pt)
                hBoostedExcl_GenPart_H1_b1_pt.Fill(e.gen_H1_b1_pt)
                hBoostedExcl_GenPart_H1_b2_pt.Fill(e.gen_H1_b2_pt)
                hBoostedExcl_GenPart_H2_b1_pt.Fill(e.gen_H2_b1_pt)
                hBoostedExcl_GenPart_H2_b2_pt.Fill(e.gen_H2_b2_pt)
                hBoostedExcl_GenPart_H1_b1_eta.Fill(e.gen_H1_b1_eta)
                hBoostedExcl_GenPart_H1_b2_eta.Fill(e.gen_H1_b2_eta)
                hBoostedExcl_GenPart_H2_b1_eta.Fill(e.gen_H2_b1_eta)
                hBoostedExcl_GenPart_H2_b2_eta.Fill(e.gen_H2_b2_eta)
                hBoostedExcl_GenFatJet_H1_pt.Fill(e.gen_H1_b1_genfatjet_pt)
                hBoostedExcl_GenFatJet_H2_pt.Fill(e.gen_H2_b2_genfatjet_pt)
                hBoostedExcl_GenFatJet_H1_eta.Fill(e.gen_H1_b1_genfatjet_eta)
                hBoostedExcl_GenFatJet_H2_eta.Fill(e.gen_H2_b2_genfatjet_eta)
                hBoostedExcl_RecoFatJet_H1_pt.Fill(e.gen_H1_b1_recofatjet_pt)
                hBoostedExcl_RecoFatJet_H2_pt.Fill(e.gen_H2_b1_recofatjet_pt)
                hBoostedExcl_RecoFatJet_H1_eta.Fill(e.gen_H1_b1_recofatjet_eta)
                hBoostedExcl_RecoFatJet_H2_eta.Fill(e.gen_H2_b2_recofatjet_eta)
                
                hBoostedExcl_RecoFatJet_H1_m.Fill(e.gen_H1_b1_recofatjet_m)
                hBoostedExcl_RecoFatJet_H2_m.Fill(e.gen_H2_b1_recofatjet_m)
                hBoostedExcl_NJets.Fill(e.n_jet)
                hBoostedExcl_NFatJets.Fill(e.n_fatjet)
                hBoostedExcl_RecoFatJet_DeltaR_H1_H2.Fill(deltaR(e.gen_H1_b1_genfatjet_eta, e.gen_H2_b2_genfatjet_eta, e.gen_H1_b1_genfatjet_phi, e.gen_H2_b2_genfatjet_phi))
                hBoostedExcl_RecoFatJet_DeltaEta_H1_H2.Fill(abs(e.gen_H1_b1_genfatjet_eta - e.gen_H2_b2_genfatjet_eta))
                hBoostedExcl_RecoFatJet_DeltaPhi_H1_H2.Fill(deltaPhi(e.gen_H1_b1_genfatjet_phi, e.gen_H2_b2_genfatjet_phi))
                
                AK8PFHT = 0.0
                for ij in range(0, e.n_fatjet):
                    eta = e.fatjet_eta.at(ij)
                    phi = e.fatjet_phi.at(ij)
                    pt = e.fatjet_pt.at(ij)
                    
                    AK8PFHT += pt

                    PXbb = e.fatjet_PNetXbb.at(ij)
                    PXcc = e.fatjet_PNetXcc.at(ij)
                    PXqq = e.fatjet_PNetXqq.at(ij)
                    TXbb = PXbb/(1-PXcc-PXqq)
                    
                    if (areSameJets(eta, e.gen_H1_b1_recofatjet_eta, phi, e.gen_H1_b1_recofatjet_phi)):
                        # H1 reco fatjet
                        hBoostedExcl_RecoFatJet_H1_TXbb.Fill(TXbb)
                        hBoostedExcl_RecoFatJet_H1_mSD_Uncorrected.Fill(e.fatjet_mSD_UnCorrected.at(ij))
                        hBoostedExcl_RecoFatJet_H1_area.Fill(e.fatjet_area.at(ij))
                        hBoostedExcl_RecoFatJet_H1_n2b1.Fill(e.fatjet_n2b1.at(ij))
                        hBoostedExcl_RecoFatJet_H1_n3b1.Fill(e.fatjet_n3b1.at(ij))
                        hBoostedExcl_RecoFatJet_H1_tau21.Fill(e.fatjet_tau2.at(ij)/e.fatjet_tau1.at(ij))
                        hBoostedExcl_RecoFatJet_H1_tau32.Fill(e.fatjet_tau3.at(ij)/e.fatjet_tau2.at(ij))
                        hBoostedExcl_RecoFatJet_H1_nsubjets.Fill(e.fatjet_nsubjets.at(ij))
                        if (e.fatjet_nsubjets.at(ij) > 0):
                            hBoostedExcl_RecoFatJet_H1_subjet1_pt.Fill(e.fatjet_subjet1_pt.at(ij))
                            hBoostedExcl_RecoFatJet_H1_subjet1_eta.Fill(e.fatjet_subjet1_eta.at(ij))
                            hBoostedExcl_RecoFatJet_H1_subjet1_m.Fill(e.fatjet_subjet1_m.at(ij))
                            hBoostedExcl_RecoFatJet_H1_subjet1_btag.Fill(e.fatjet_subjet1_btagDeepB.at(ij))
                        if (e.fatjet_nsubjets.at(ij) > 1):
                            hBoostedExcl_RecoFatJet_H1_subjet2_pt.Fill(e.fatjet_subjet2_pt.at(ij))
                            hBoostedExcl_RecoFatJet_H1_subjet2_eta.Fill(e.fatjet_subjet2_eta.at(ij))
                            hBoostedExcl_RecoFatJet_H1_subjet2_m.Fill(e.fatjet_subjet2_m.at(ij))
                            hBoostedExcl_RecoFatJet_H1_subjet2_btag.Fill(e.fatjet_subjet2_btagDeepB.at(ij))
                if (areSameJets(eta, e.gen_H2_b1_recofatjet_eta, phi, e.gen_H2_b1_recofatjet_phi)):
                        # H2 reco fatjet
                        hBoostedExcl_RecoFatJet_H2_TXbb.Fill(TXbb)
                        hBoostedExcl_RecoFatJet_H2_mSD_Uncorrected.Fill(e.fatjet_mSD_UnCorrected.at(ij))
                        hBoostedExcl_RecoFatJet_H2_area.Fill(e.fatjet_area.at(ij))
                        hBoostedExcl_RecoFatJet_H2_n2b1.Fill(e.fatjet_n2b1.at(ij))
                        hBoostedExcl_RecoFatJet_H2_n3b1.Fill(e.fatjet_n3b1.at(ij))
                        hBoostedExcl_RecoFatJet_H2_tau21.Fill(e.fatjet_tau2.at(ij)/e.fatjet_tau1.at(ij))
                        hBoostedExcl_RecoFatJet_H2_tau32.Fill(e.fatjet_tau3.at(ij)/e.fatjet_tau2.at(ij))
                        hBoostedExcl_RecoFatJet_H2_nsubjets.Fill(e.fatjet_nsubjets.at(ij))
                        if (e.fatjet_nsubjets.at(ij) > 0):
                            hBoostedExcl_RecoFatJet_H2_subjet1_pt.Fill(e.fatjet_subjet1_pt.at(ij))
                            hBoostedExcl_RecoFatJet_H2_subjet1_eta.Fill(e.fatjet_subjet1_eta.at(ij))
                            hBoostedExcl_RecoFatJet_H2_subjet1_m.Fill(e.fatjet_subjet1_m.at(ij))
                            hBoostedExcl_RecoFatJet_H2_subjet1_btag.Fill(e.fatjet_subjet1_btagDeepB.at(ij))
                        if (e.fatjet_nsubjets.at(ij) > 1):
                            hBoostedExcl_RecoFatJet_H2_subjet2_pt.Fill(e.fatjet_subjet2_pt.at(ij))
                            hBoostedExcl_RecoFatJet_H2_subjet2_eta.Fill(e.fatjet_subjet2_eta.at(ij))
                            hBoostedExcl_RecoFatJet_H2_subjet2_m.Fill(e.fatjet_subjet2_m.at(ij))
                            hBoostedExcl_RecoFatJet_H2_subjet2_btag.Fill(e.fatjet_subjet2_btagDeepB.at(ij))
                hBoostedExcl_AK8PFHT.Fill(AK8PFHT)

            #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            # Resolved reco exclusive category: resolved but not boosted or semi-resolved
            #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
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
                # GenJets matched
                hResolvedExcl_GenJet_H1_b1_pt.Fill(e.gen_H1_b1_genjet_pt)
                hResolvedExcl_GenJet_H1_b2_pt.Fill(e.gen_H1_b2_genjet_pt)
                hResolvedExcl_GenJet_H2_b1_pt.Fill(e.gen_H2_b1_genjet_pt)
                hResolvedExcl_GenJet_H2_b2_pt.Fill(e.gen_H2_b2_genjet_pt)
                hResolvedExcl_GenJet_H1_b1_eta.Fill(e.gen_H1_b1_genjet_eta)
                hResolvedExcl_GenJet_H1_b2_eta.Fill(e.gen_H1_b2_genjet_eta)
                hResolvedExcl_GenJet_H2_b1_eta.Fill(e.gen_H2_b1_genjet_eta)
                hResolvedExcl_GenJet_H2_b2_eta.Fill(e.gen_H2_b2_genjet_eta)
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
                # GenJets matched
                hResolved_GenJet_H1_b1_pt.Fill(e.gen_H1_b1_genjet_pt)
                hResolved_GenJet_H1_b2_pt.Fill(e.gen_H1_b2_genjet_pt)
                hResolved_GenJet_H2_b1_pt.Fill(e.gen_H2_b1_genjet_pt)
                hResolved_GenJet_H2_b2_pt.Fill(e.gen_H2_b2_genjet_pt)
                hResolved_GenJet_H1_b1_eta.Fill(e.gen_H1_b1_genjet_eta)
                hResolved_GenJet_H1_b2_eta.Fill(e.gen_H1_b2_genjet_eta)
                hResolved_GenJet_H2_b1_eta.Fill(e.gen_H2_b1_genjet_eta)
                hResolved_GenJet_H2_b2_eta.Fill(e.gen_H2_b2_genjet_eta)
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
                if (e.n_fatjet > 0): hResolved_RecoJet_AK8Jet1Pt.Fill(e.fatjet_pt.at(0))
                if (e.n_fatjet > 1): hResolved_RecoJet_AK8Jet2Pt.Fill(e.fatjet_pt.at(1))
                if (e.n_fatjet > 2): hResolved_RecoJet_AK8Jet3Pt.Fill(e.fatjet_pt.at(2))
                if (e.n_fatjet > 3): hResolved_RecoJet_AK8Jet4Pt.Fill(e.fatjet_pt.at(3))
                
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
                    
                if (bIsResolvedRecoCases["10"]):
                    hResolvedCase10_GenPart_H1_pt.Fill(e.gen_H1_pt)
                    hResolvedCase10_GenPart_H2_pt.Fill(e.gen_H2_pt)
                    hResolvedCase10_GenPart_H1_b1_pt.Fill(e.gen_H1_b1_pt)
                    hResolvedCase10_GenPart_H1_b2_pt.Fill(e.gen_H1_b2_pt)
                    hResolvedCase10_GenPart_H2_b1_pt.Fill(e.gen_H2_b1_pt)
                    hResolvedCase10_GenPart_H2_b2_pt.Fill(e.gen_H2_b2_pt)
                    hResolvedCase10_RecoJet_H1_b1_pt.Fill(e.gen_H1_b1_recojet_pt)
                    hResolvedCase10_RecoJet_H1_b2_pt.Fill(e.gen_H1_b2_recojet_pt)
                    hResolvedCase10_RecoJet_H2_b1_pt.Fill(e.gen_H2_b1_recojet_pt)
                    hResolvedCase10_RecoJet_H2_b2_pt.Fill(e.gen_H2_b2_recojet_pt)
                    hResolvedCase10_RecoJet_H1_pt.Fill(reco_H1.Pt())
                    hResolvedCase10_RecoJet_H2_pt.Fill(reco_H2.Pt())
                    hResolvedCase10_RecoJet_InvMass_H1.Fill(reco_H1.M())
                    hResolvedCase10_RecoJet_InvMass_H2.Fill(reco_H2.M())
                    hResolvedCase10_RecoJet_NJets.Fill(e.n_jet)
                    hResolvedCase10_RecoJet_NFatJets.Fill(e.n_fatjet)
                    hResolvedCase10_RecoFatJet_H1_pt.Fill(e.gen_H1_b1_recofatjet_pt)
                    hResolvedCase10_RecoFatJet_H2_pt.Fill(e.gen_H2_b2_recofatjet_pt)
                    hResolvedCase10_RecoFatJet_H1_m.Fill(e.gen_H1_b1_recofatjet_m)
                    hResolvedCase10_RecoFatJet_H2_m.Fill(e.gen_H2_b2_recofatjet_m)
                    if (e.n_fatjet > 0): hResolvedCase10_RecoJet_AK8Jet1Pt.Fill(e.fatjet_pt.at(0))
                    if (e.n_fatjet > 1): hResolvedCase10_RecoJet_AK8Jet2Pt.Fill(e.fatjet_pt.at(1))
                    if (e.n_fatjet > 2): hResolvedCase10_RecoJet_AK8Jet3Pt.Fill(e.fatjet_pt.at(2))
                    if (e.n_fatjet > 3): hResolvedCase10_RecoJet_AK8Jet4Pt.Fill(e.fatjet_pt.at(3))
                elif (bIsResolvedRecoCases["6"]):
                    hResolvedCase6_GenPart_H1_pt.Fill(e.gen_H1_pt)
                    hResolvedCase6_GenPart_H2_pt.Fill(e.gen_H2_pt)
                    hResolvedCase6_GenPart_H1_b1_pt.Fill(e.gen_H1_b1_pt)
                    hResolvedCase6_GenPart_H1_b2_pt.Fill(e.gen_H1_b2_pt)
                    hResolvedCase6_GenPart_H2_b1_pt.Fill(e.gen_H2_b1_pt)
                    hResolvedCase6_GenPart_H2_b2_pt.Fill(e.gen_H2_b2_pt)
                    hResolvedCase6_RecoJet_H1_b1_pt.Fill(e.gen_H1_b1_recojet_pt)
                    hResolvedCase6_RecoJet_H1_b2_pt.Fill(e.gen_H1_b2_recojet_pt)
                    hResolvedCase6_RecoJet_H2_b1_pt.Fill(e.gen_H2_b1_recojet_pt)
                    hResolvedCase6_RecoJet_H2_b2_pt.Fill(e.gen_H2_b2_recojet_pt)
                    hResolvedCase6_RecoJet_H1_pt.Fill(reco_H1.Pt())
                    hResolvedCase6_RecoJet_H2_pt.Fill(reco_H2.Pt())
                    hResolvedCase6_RecoJet_InvMass_H1.Fill(reco_H1.M())
                    hResolvedCase6_RecoJet_InvMass_H2.Fill(reco_H2.M())
                    hResolvedCase6_RecoJet_NJets.Fill(e.n_jet)
                    hResolvedCase6_RecoJet_NFatJets.Fill(e.n_fatjet)
                    hResolvedCase6_RecoFatJet_H1_pt.Fill(e.gen_H1_b1_recofatjet_pt)
                    if (e.n_fatjet > 0): hResolvedCase6_RecoJet_AK8Jet1Pt.Fill(e.fatjet_pt.at(0))
                    if (e.n_fatjet > 1): hResolvedCase6_RecoJet_AK8Jet2Pt.Fill(e.fatjet_pt.at(1))
                    if (e.n_fatjet > 2): hResolvedCase6_RecoJet_AK8Jet3Pt.Fill(e.fatjet_pt.at(2))
                    if (e.n_fatjet > 3): hResolvedCase6_RecoJet_AK8Jet4Pt.Fill(e.fatjet_pt.at(3))
                elif (bIsResolvedRecoCases["13"]):
                    hResolvedCase13_GenPart_H1_pt.Fill(e.gen_H1_pt)
                    hResolvedCase13_GenPart_H2_pt.Fill(e.gen_H2_pt)
                    hResolvedCase13_GenPart_H1_b1_pt.Fill(e.gen_H1_b1_pt)
                    hResolvedCase13_GenPart_H1_b2_pt.Fill(e.gen_H1_b2_pt)
                    hResolvedCase13_GenPart_H2_b1_pt.Fill(e.gen_H2_b1_pt)
                    hResolvedCase13_GenPart_H2_b2_pt.Fill(e.gen_H2_b2_pt)
                    hResolvedCase13_RecoJet_H1_b1_pt.Fill(e.gen_H1_b1_recojet_pt)
                    hResolvedCase13_RecoJet_H1_b2_pt.Fill(e.gen_H1_b2_recojet_pt)
                    hResolvedCase13_RecoJet_H2_b1_pt.Fill(e.gen_H2_b1_recojet_pt)
                    hResolvedCase13_RecoJet_H2_b2_pt.Fill(e.gen_H2_b2_recojet_pt)
                    hResolvedCase13_RecoJet_H1_pt.Fill(reco_H1.Pt())
                    hResolvedCase13_RecoJet_H2_pt.Fill(reco_H2.Pt())
                    hResolvedCase13_RecoJet_InvMass_H1.Fill(reco_H1.M())
                    hResolvedCase13_RecoJet_InvMass_H2.Fill(reco_H2.M())
                    hResolvedCase13_RecoJet_NJets.Fill(e.n_jet)
                    hResolvedCase13_RecoJet_NFatJets.Fill(e.n_fatjet)
                    hResolvedCase13_RecoFatJet_H1_pt.Fill(e.gen_H1_b1_recofatjet_pt)
                    if (e.n_fatjet > 0): hResolvedCase13_RecoJet_AK8Jet1Pt.Fill(e.fatjet_pt.at(0))
                    if (e.n_fatjet > 1): hResolvedCase13_RecoJet_AK8Jet2Pt.Fill(e.fatjet_pt.at(1))
                    if (e.n_fatjet > 2): hResolvedCase13_RecoJet_AK8Jet3Pt.Fill(e.fatjet_pt.at(2))
                    if (e.n_fatjet > 3): hResolvedCase13_RecoJet_AK8Jet4Pt.Fill(e.fatjet_pt.at(3))
                elif (bIsResolvedRecoCases["7"]):
                    hResolvedCase7_GenPart_H1_pt.Fill(e.gen_H1_pt)
                    hResolvedCase7_GenPart_H2_pt.Fill(e.gen_H2_pt)
                    hResolvedCase7_GenPart_H1_b1_pt.Fill(e.gen_H1_b1_pt)
                    hResolvedCase7_GenPart_H1_b2_pt.Fill(e.gen_H1_b2_pt)
                    hResolvedCase7_GenPart_H2_b1_pt.Fill(e.gen_H2_b1_pt)
                    hResolvedCase7_GenPart_H2_b2_pt.Fill(e.gen_H2_b2_pt)
                    hResolvedCase7_RecoJet_H1_b1_pt.Fill(e.gen_H1_b1_recojet_pt)
                    hResolvedCase7_RecoJet_H1_b2_pt.Fill(e.gen_H1_b2_recojet_pt)
                    hResolvedCase7_RecoJet_H2_b1_pt.Fill(e.gen_H2_b1_recojet_pt)
                    hResolvedCase7_RecoJet_H2_b2_pt.Fill(e.gen_H2_b2_recojet_pt)
                    hResolvedCase7_RecoJet_H1_pt.Fill(reco_H1.Pt())
                    hResolvedCase7_RecoJet_H2_pt.Fill(reco_H2.Pt())
                    hResolvedCase7_RecoJet_InvMass_H1.Fill(reco_H1.M())
                    hResolvedCase7_RecoJet_InvMass_H2.Fill(reco_H2.M())
                    hResolvedCase7_RecoJet_NJets.Fill(e.n_jet)
                    hResolvedCase7_RecoJet_NFatJets.Fill(e.n_fatjet)
                    hResolvedCase7_RecoFatJet_H1_pt.Fill(e.gen_H1_b1_recofatjet_pt)
                    if (e.n_fatjet > 0): hResolvedCase7_RecoJet_AK8Jet1Pt.Fill(e.fatjet_pt.at(0))
                    if (e.n_fatjet > 1): hResolvedCase7_RecoJet_AK8Jet2Pt.Fill(e.fatjet_pt.at(1))
                    if (e.n_fatjet > 2): hResolvedCase7_RecoJet_AK8Jet3Pt.Fill(e.fatjet_pt.at(2))
                    if (e.n_fatjet > 3): hResolvedCase7_RecoJet_AK8Jet4Pt.Fill(e.fatjet_pt.at(3))                    
                elif (bIsResolvedRecoCases["1"]):
                    hResolvedCase1_GenPart_H1_pt.Fill(e.gen_H1_pt)
                    hResolvedCase1_GenPart_H2_pt.Fill(e.gen_H2_pt)
                    hResolvedCase1_GenPart_H1_b1_pt.Fill(e.gen_H1_b1_pt)
                    hResolvedCase1_GenPart_H1_b2_pt.Fill(e.gen_H1_b2_pt)
                    hResolvedCase1_GenPart_H2_b1_pt.Fill(e.gen_H2_b1_pt)
                    hResolvedCase1_GenPart_H2_b2_pt.Fill(e.gen_H2_b2_pt)
                    hResolvedCase1_RecoJet_H1_b1_pt.Fill(e.gen_H1_b1_recojet_pt)
                    hResolvedCase1_RecoJet_H1_b2_pt.Fill(e.gen_H1_b2_recojet_pt)
                    hResolvedCase1_RecoJet_H2_b1_pt.Fill(e.gen_H2_b1_recojet_pt)
                    hResolvedCase1_RecoJet_H2_b2_pt.Fill(e.gen_H2_b2_recojet_pt)
                    hResolvedCase1_RecoJet_H1_pt.Fill(reco_H1.Pt())
                    hResolvedCase1_RecoJet_H2_pt.Fill(reco_H2.Pt())
                    hResolvedCase1_RecoJet_InvMass_H1.Fill(reco_H1.M())
                    hResolvedCase1_RecoJet_InvMass_H2.Fill(reco_H2.M())
                    hResolvedCase1_RecoJet_NJets.Fill(e.n_jet)
                    hResolvedCase1_RecoJet_NFatJets.Fill(e.n_fatjet)
                    if (e.n_fatjet > 0): hResolvedCase1_RecoJet_AK8Jet1Pt.Fill(e.fatjet_pt.at(0))
                    if (e.n_fatjet > 1): hResolvedCase1_RecoJet_AK8Jet2Pt.Fill(e.fatjet_pt.at(1))
                    if (e.n_fatjet > 2): hResolvedCase1_RecoJet_AK8Jet3Pt.Fill(e.fatjet_pt.at(2))
                    if (e.n_fatjet > 3): hResolvedCase1_RecoJet_AK8Jet4Pt.Fill(e.fatjet_pt.at(3))
                    
        
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

        hBoostedExclPassed_HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5.Write()
        hBoostedExclPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np4.Write()
        hBoostedExclPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np2.Write()
        hBoostedExclPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p1.Write()
        hBoostedExclPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p17.Write()
        hBoostedExclPassed_HLT_PFHT1050.Write()
        hBoostedExclPassed_HLT_PFJet500.Write()
        hBoostedExclPassed_HLT_AK8PFHT800_TrimMass50.Write()
        hBoostedExclPassed_HLT_AK8PFJet400_TrimMass30.Write()
        hBoostedExclPassed_HLT_AK8PFJet420_TrimMass30.Write()
        hBoostedExclPassed_HLT_AK8PFJet500.Write()
        hBoostedExclPassed_HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59.Write()
        hBoostedExclPassed_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94.Write()
        hBoostedExclPassed_HLT_AK8PFHT750_TrimMass50.Write()
        hBoostedExclPassed_HLT_AK8PFJet360_TrimMass30.Write()
        hBoostedExclPassed_HLT_AK8PFJet380_TrimMass30.Write()
        hBoostedExclPassed_OR.Write()
        
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

        hSemiresolvedExclPassed_HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5.Write()
        hSemiresolvedExclPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np4.Write()
        hSemiresolvedExclPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np2.Write()
        hSemiresolvedExclPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p1.Write()
        hSemiresolvedExclPassed_HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p17.Write()
        hSemiresolvedExclPassed_HLT_PFHT1050.Write()
        hSemiresolvedExclPassed_HLT_PFJet500.Write()
        hSemiresolvedExclPassed_HLT_AK8PFHT800_TrimMass50.Write()
        hSemiresolvedExclPassed_HLT_AK8PFJet400_TrimMass30.Write()
        hSemiresolvedExclPassed_HLT_AK8PFJet420_TrimMass30.Write()
        hSemiresolvedExclPassed_HLT_AK8PFJet500.Write()
        hSemiresolvedExclPassed_HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59.Write()
        hSemiresolvedExclPassed_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94.Write()
        hSemiresolvedExclPassed_HLT_AK8PFHT750_TrimMass50.Write()
        hSemiresolvedExclPassed_HLT_AK8PFJet360_TrimMass30.Write()
        hSemiresolvedExclPassed_HLT_AK8PFJet380_TrimMass30.Write()
        hSemiresolvedExclPassed_OR.Write()
                
        h_GenPart_H1_pt.Write()
        h_GenPart_H2_pt.Write()
        h_GenPart_H1_eta.Write()
        h_GenPart_H2_eta.Write()
        h_GenPart_H1_b1_pt.Write()
        h_GenPart_H1_b2_pt.Write()
        h_GenPart_H2_b1_pt.Write()
        h_GenPart_H2_b2_pt.Write()
        h_GenPart_H1_b1_eta.Write()
        h_GenPart_H1_b2_eta.Write()
        h_GenPart_H2_b1_eta.Write()
        h_GenPart_H2_b2_eta.Write()
        
        h2D_NBQuarksMatchedTo_GenJetsVsGenFatJets.Write()
        h2D_NBQuarksMatchedTo_RecoJetsVsRecoFatJets.Write()
        h2D_NBQuarksMatchedTo_RecoJetsVsCategory.Write()
        h2D_NBQuarksMatchedTo_RecoFatJetsVsCategory.Write()
        
        h_GenMatchingTo4GenJets_Cases.Write()
        h_GenMatchingTo4RecoJets_Cases.Write()
        
        h_IsBoostedGen_GenFatJet_H1_pt.Write()
        h_IsBoostedGen_GenFatJet_H2_pt.Write()
        h_IsSemiresolvedGen_GenFatJet_H1_pt.Write()
        h_IsSemiresolvedGen_GenFatJet_H2_pt.Write()
        h_GenFatJet_H1_pt.Write()
        h_GenFatJet_H2_pt.Write()

        h_IsBoostedGen_NotBoostedReco_GenFatJet_H1_pt.Write()
        h_IsBoostedGen_NotBoostedReco_GenFatJet_H2_pt.Write()
        h_IsSemiresolvedGen_NotSemiresolvedReco_GenFatJet_H1_pt.Write()
        h_IsSemiresolvedGen_NotSemiresolvedReco_GenFatJet_H2_pt.Write()
                
        h_NJets.Write()
        h_Jet1Pt.Write()
        h_Jet2Pt.Write()
        h_Jet3Pt.Write()
        h_Jet4Pt.Write()
        h_NLooseBJets.Write()
        h_NMediumBJets.Write()
        h_NTightBJets.Write()
        h_NFatJets.Write()
        h_AK8Jet1Pt.Write()
        h_AK8Jet2Pt.Write()
        h_AK8Jet3Pt.Write()
        h_AK8Jet4Pt.Write()
        
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
        hResolved_GenJet_H1_b1_pt.Write()
        hResolved_GenJet_H1_b2_pt.Write()
        hResolved_GenJet_H2_b1_pt.Write()
        hResolved_GenJet_H2_b2_pt.Write()
        hResolved_GenJet_H1_b1_eta.Write()
        hResolved_GenJet_H1_b2_eta.Write()
        hResolved_GenJet_H2_b1_eta.Write()
        hResolved_GenJet_H2_b2_eta.Write()
        hResolved_RecoJet_H1_b1_pt.Write()
        hResolved_RecoJet_H1_b2_pt.Write()
        hResolved_RecoJet_H2_b1_pt.Write()
        hResolved_RecoJet_H2_b2_pt.Write()
        hResolved_RecoJet_H1_b1_eta.Write()
        hResolved_RecoJet_H1_b2_eta.Write()
        hResolved_RecoJet_H2_b1_eta.Write()
        hResolved_RecoJet_H2_b2_eta.Write()
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
        hResolved_RecoJet_AK8Jet2Pt.Write()
        hResolved_RecoJet_AK8Jet3Pt.Write()
        hResolved_RecoJet_AK8Jet3Pt.Write()
        
        hResolvedCase10_GenPart_H1_pt.Write()
        hResolvedCase10_GenPart_H2_pt.Write()
        hResolvedCase10_GenPart_H1_b1_pt.Write()
        hResolvedCase10_GenPart_H1_b2_pt.Write()
        hResolvedCase10_GenPart_H2_b1_pt.Write()
        hResolvedCase10_GenPart_H2_b2_pt.Write()
        hResolvedCase10_RecoJet_H1_b1_pt.Write()
        hResolvedCase10_RecoJet_H1_b2_pt.Write()
        hResolvedCase10_RecoJet_H2_b1_pt.Write()
        hResolvedCase10_RecoJet_H2_b2_pt.Write()
        hResolvedCase10_RecoJet_H1_pt.Write()
        hResolvedCase10_RecoJet_H2_pt.Write()
        hResolvedCase10_RecoJet_InvMass_H1.Write()
        hResolvedCase10_RecoJet_InvMass_H2.Write()
        hResolvedCase10_RecoJet_NJets.Write()
        hResolvedCase10_RecoJet_NFatJets.Write()
        hResolvedCase10_RecoFatJet_H1_pt.Write()
        hResolvedCase10_RecoFatJet_H2_pt.Write()
        hResolvedCase10_RecoFatJet_H1_m.Write()
        hResolvedCase10_RecoFatJet_H2_m.Write()
        hResolvedCase10_RecoJet_AK8Jet1Pt.Write()
        hResolvedCase10_RecoJet_AK8Jet2Pt.Write()
        hResolvedCase10_RecoJet_AK8Jet3Pt.Write()
        hResolvedCase10_RecoJet_AK8Jet4Pt.Write()
        hResolvedCase1_GenPart_H1_pt.Write()
        hResolvedCase1_GenPart_H2_pt.Write()
        hResolvedCase1_GenPart_H1_b1_pt.Write()
        hResolvedCase1_GenPart_H1_b2_pt.Write()
        hResolvedCase1_GenPart_H2_b1_pt.Write()
        hResolvedCase1_GenPart_H2_b2_pt.Write()
        hResolvedCase1_RecoJet_H1_b1_pt.Write()
        hResolvedCase1_RecoJet_H1_b2_pt.Write()
        hResolvedCase1_RecoJet_H2_b1_pt.Write()
        hResolvedCase1_RecoJet_H2_b2_pt.Write()
        hResolvedCase1_RecoJet_H1_pt.Write()
        hResolvedCase1_RecoJet_H2_pt.Write()
        hResolvedCase1_RecoJet_InvMass_H1.Write()
        hResolvedCase1_RecoJet_InvMass_H2.Write()
        hResolvedCase1_RecoJet_NJets.Write()
        hResolvedCase1_RecoJet_NFatJets.Write()
        hResolvedCase1_RecoJet_AK8Jet1Pt.Write()
        hResolvedCase1_RecoJet_AK8Jet2Pt.Write()
        hResolvedCase1_RecoJet_AK8Jet3Pt.Write()
        hResolvedCase1_RecoJet_AK8Jet4Pt.Write()
        
        hResolvedCase6_GenPart_H1_pt.Write()
        hResolvedCase6_GenPart_H2_pt.Write()
        hResolvedCase6_GenPart_H1_b1_pt.Write()
        hResolvedCase6_GenPart_H1_b2_pt.Write()
        hResolvedCase6_GenPart_H2_b1_pt.Write()
        hResolvedCase6_GenPart_H2_b2_pt.Write()
        hResolvedCase6_RecoJet_H1_b1_pt.Write()
        hResolvedCase6_RecoJet_H1_b2_pt.Write()
        hResolvedCase6_RecoJet_H2_b1_pt.Write()
        hResolvedCase6_RecoJet_H2_b2_pt.Write()
        hResolvedCase6_RecoJet_H1_pt.Write()
        hResolvedCase6_RecoJet_H2_pt.Write()
        hResolvedCase6_RecoJet_InvMass_H1.Write()
        hResolvedCase6_RecoJet_InvMass_H2.Write()
        hResolvedCase6_RecoJet_NJets.Write()
        hResolvedCase6_RecoJet_NFatJets.Write()
        hResolvedCase6_RecoFatJet_H1_pt.Write()
        hResolvedCase6_RecoJet_AK8Jet1Pt.Write()
        hResolvedCase6_RecoJet_AK8Jet2Pt.Write()
        hResolvedCase6_RecoJet_AK8Jet3Pt.Write()
        hResolvedCase6_RecoJet_AK8Jet4Pt.Write()

        hResolvedCase13_GenPart_H1_pt.Write()
        hResolvedCase13_GenPart_H2_pt.Write()
        hResolvedCase13_GenPart_H1_b1_pt.Write()
        hResolvedCase13_GenPart_H1_b2_pt.Write()
        hResolvedCase13_GenPart_H2_b1_pt.Write()
        hResolvedCase13_GenPart_H2_b2_pt.Write()
        hResolvedCase13_RecoJet_H1_b1_pt.Write()
        hResolvedCase13_RecoJet_H1_b2_pt.Write()
        hResolvedCase13_RecoJet_H2_b1_pt.Write()
        hResolvedCase13_RecoJet_H2_b2_pt.Write()
        hResolvedCase13_RecoJet_H1_pt.Write()
        hResolvedCase13_RecoJet_H2_pt.Write()
        hResolvedCase13_RecoJet_InvMass_H1.Write()
        hResolvedCase13_RecoJet_InvMass_H2.Write()
        hResolvedCase13_RecoJet_NJets.Write()
        hResolvedCase13_RecoJet_NFatJets.Write()
        hResolvedCase13_RecoFatJet_H1_pt.Write()
        hResolvedCase13_RecoJet_AK8Jet1Pt.Write()
        hResolvedCase13_RecoJet_AK8Jet2Pt.Write()
        hResolvedCase13_RecoJet_AK8Jet3Pt.Write()
        hResolvedCase13_RecoJet_AK8Jet4Pt.Write()

        hResolvedCase7_GenPart_H1_pt.Write()
        hResolvedCase7_GenPart_H2_pt.Write()
        hResolvedCase7_GenPart_H1_b1_pt.Write()
        hResolvedCase7_GenPart_H1_b2_pt.Write()
        hResolvedCase7_GenPart_H2_b1_pt.Write()
        hResolvedCase7_GenPart_H2_b2_pt.Write()
        hResolvedCase7_RecoJet_H1_b1_pt.Write()
        hResolvedCase7_RecoJet_H1_b2_pt.Write()
        hResolvedCase7_RecoJet_H2_b1_pt.Write()
        hResolvedCase7_RecoJet_H2_b2_pt.Write()
        hResolvedCase7_RecoJet_H1_pt.Write()
        hResolvedCase7_RecoJet_H2_pt.Write()
        hResolvedCase7_RecoJet_InvMass_H1.Write()
        hResolvedCase7_RecoJet_InvMass_H2.Write()
        hResolvedCase7_RecoJet_NJets.Write()
        hResolvedCase7_RecoJet_NFatJets.Write()
        hResolvedCase7_RecoFatJet_H1_pt.Write()
        hResolvedCase7_RecoJet_AK8Jet1Pt.Write()
        hResolvedCase7_RecoJet_AK8Jet2Pt.Write()
        hResolvedCase7_RecoJet_AK8Jet3Pt.Write()
        hResolvedCase7_RecoJet_AK8Jet4Pt.Write()
        
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
        hResolvedExcl_GenJet_H1_b1_pt.Write()
        hResolvedExcl_GenJet_H1_b2_pt.Write()
        hResolvedExcl_GenJet_H2_b1_pt.Write()
        hResolvedExcl_GenJet_H2_b2_pt.Write()
        hResolvedExcl_GenJet_H1_b1_eta.Write()
        hResolvedExcl_GenJet_H1_b2_eta.Write()
        hResolvedExcl_GenJet_H2_b1_eta.Write()
        hResolvedExcl_GenJet_H2_b2_eta.Write()
        hResolvedExcl_RecoJet_H1_b1_pt.Write()
        hResolvedExcl_RecoJet_H1_b2_pt.Write()
        hResolvedExcl_RecoJet_H2_b1_pt.Write()
        hResolvedExcl_RecoJet_H2_b2_pt.Write()
        hResolvedExcl_RecoJet_H1_b1_eta.Write()
        hResolvedExcl_RecoJet_H1_b2_eta.Write()
        hResolvedExcl_RecoJet_H2_b1_eta.Write()
        hResolvedExcl_RecoJet_H2_b2_eta.Write()
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
        hBoosted_GenFatJet_H1_pt.Write()
        hBoosted_GenFatJet_H2_pt.Write()
        hBoosted_GenFatJet_H1_eta.Write()
        hBoosted_GenFatJet_H2_eta.Write()
        hBoosted_RecoFatJet_H1_pt.Write()
        hBoosted_RecoFatJet_H2_pt.Write()
        hBoosted_RecoFatJet_H1_eta.Write()
        hBoosted_RecoFatJet_H2_eta.Write()
        hBoosted_RecoFatJet_H1_TXbb.Write()
        hBoosted_RecoFatJet_H2_TXbb.Write()
        hBoosted_RecoFatJet_H1_m.Write()
        hBoosted_RecoFatJet_H2_m.Write()
        hBoosted_NJets.Write()
        hBoosted_NFatJets.Write()
        hBoosted_AK8PFHT.Write()
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
        hBoosted_RecoFatJet_H1_subjet1_m.Write()
        hBoosted_RecoFatJet_H1_subjet1_btag.Write()
        hBoosted_RecoFatJet_H1_subjet2_pt.Write()
        hBoosted_RecoFatJet_H1_subjet2_eta.Write()
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
        hBoosted_RecoFatJet_H2_subjet1_m.Write()
        hBoosted_RecoFatJet_H2_subjet1_btag.Write()
        hBoosted_RecoFatJet_H2_subjet2_pt.Write()
        hBoosted_RecoFatJet_H2_subjet2_eta.Write()
        hBoosted_RecoFatJet_H2_subjet2_m.Write()
        hBoosted_RecoFatJet_H2_subjet2_btag.Write()
        
        hResolved_MatchedToTwoFatJets_DR_RecoFatJetH1_RecoFatJetH2.Write()
        hResolved_MatchedToTwoFatJets_DR_RecoFatJetH1_b11.Write()
        hResolved_MatchedToTwoFatJets_DR_RecoFatJetH1_b12.Write()
        hResolved_MatchedToTwoFatJets_DR_b11_b12.Write()
        hResolved_MatchedToTwoFatJets_DR_RecoFatJetH2_b21.Write()
        hResolved_MatchedToTwoFatJets_DR_RecoFatJetH2_b22.Write()
        hResolved_MatchedToTwoFatJets_DR_b21_b22.Write()
        hResolved_MatchedToOneFatJet_DR_RecoFatJetH1_RecoH2.Write()
        hResolved_MatchedToOneFatJet_DR_RecoFatJetH1_b11.Write()
        hResolved_MatchedToOneFatJet_DR_RecoFatJetH1_b12.Write()
        hResolved_MatchedToOneFatJet_DR_b11_b12.Write()
        hResolved_MatchedToOneFatJet_DR_RecoH2_b21.Write()
        hResolved_MatchedToOneFatJet_DR_RecoH2_b22.Write()
        hResolved_MatchedToOneFatJet_DR_b21_b22.Write()
        
        hBoostedExcl_GenPart_H1_pt.Write()
        hBoostedExcl_GenPart_H2_pt.Write()
        hBoostedExcl_GenPart_H1_b1_pt.Write()
        hBoostedExcl_GenPart_H1_b2_pt.Write()
        hBoostedExcl_GenPart_H2_b1_pt.Write()
        hBoostedExcl_GenPart_H2_b2_pt.Write()
        hBoostedExcl_GenPart_H1_b1_eta.Write()
        hBoostedExcl_GenPart_H1_b2_eta.Write()
        hBoostedExcl_GenPart_H2_b1_eta.Write()
        hBoostedExcl_GenPart_H2_b2_eta.Write()
        hBoostedExcl_GenFatJet_H1_pt.Write()
        hBoostedExcl_GenFatJet_H2_pt.Write()
        hBoostedExcl_GenFatJet_H1_eta.Write()
        hBoostedExcl_GenFatJet_H2_eta.Write()
        hBoostedExcl_RecoFatJet_H1_pt.Write()
        hBoostedExcl_RecoFatJet_H2_pt.Write()
        hBoostedExcl_RecoFatJet_H1_eta.Write()
        hBoostedExcl_RecoFatJet_H2_eta.Write()
        hBoostedExcl_RecoFatJet_H1_TXbb.Write()
        hBoostedExcl_RecoFatJet_H2_TXbb.Write()
        hBoostedExcl_RecoFatJet_H1_m.Write()
        hBoostedExcl_RecoFatJet_H2_m.Write()
        hBoostedExcl_NJets.Write()
        hBoostedExcl_NFatJets.Write()
        hBoostedExcl_AK8PFHT.Write()
        hBoostedExcl_RecoFatJet_DeltaR_H1_H2.Write()
        hBoostedExcl_RecoFatJet_DeltaEta_H1_H2.Write()
        hBoostedExcl_RecoFatJet_DeltaPhi_H1_H2.Write()
        hBoostedExcl_RecoFatJet_H1_mSD_Uncorrected.Write()
        hBoostedExcl_RecoFatJet_H1_area.Write()
        hBoostedExcl_RecoFatJet_H1_n2b1.Write()
        hBoostedExcl_RecoFatJet_H1_n3b1.Write()
        hBoostedExcl_RecoFatJet_H1_tau21.Write()
        hBoostedExcl_RecoFatJet_H1_tau32.Write()
        hBoostedExcl_RecoFatJet_H1_nsubjets.Write()
        hBoostedExcl_RecoFatJet_H1_subjet1_pt.Write()
        hBoostedExcl_RecoFatJet_H1_subjet1_eta.Write()
        hBoostedExcl_RecoFatJet_H1_subjet1_m.Write()
        hBoostedExcl_RecoFatJet_H1_subjet1_btag.Write()
        hBoostedExcl_RecoFatJet_H1_subjet2_pt.Write()
        hBoostedExcl_RecoFatJet_H1_subjet2_eta.Write()
        hBoostedExcl_RecoFatJet_H1_subjet2_m.Write()
        hBoostedExcl_RecoFatJet_H1_subjet2_btag.Write()
        hBoostedExcl_RecoFatJet_H2_mSD_Uncorrected.Write()
        hBoostedExcl_RecoFatJet_H2_area.Write()
        hBoostedExcl_RecoFatJet_H2_n2b1.Write()
        hBoostedExcl_RecoFatJet_H2_n3b1.Write()
        hBoostedExcl_RecoFatJet_H2_tau21.Write()
        hBoostedExcl_RecoFatJet_H2_tau32.Write()
        hBoostedExcl_RecoFatJet_H2_nsubjets.Write()
        hBoostedExcl_RecoFatJet_H2_subjet1_pt.Write()
        hBoostedExcl_RecoFatJet_H2_subjet1_eta.Write()
        hBoostedExcl_RecoFatJet_H2_subjet1_m.Write()
        hBoostedExcl_RecoFatJet_H2_subjet1_btag.Write()
        hBoostedExcl_RecoFatJet_H2_subjet2_pt.Write()
        hBoostedExcl_RecoFatJet_H2_subjet2_eta.Write()
        hBoostedExcl_RecoFatJet_H2_subjet2_m.Write()
        hBoostedExcl_RecoFatJet_H2_subjet2_btag.Write()
        
        # Write the semi-resolved histograms
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
        hSemiresolved_H1Boosted_H2resolved_GenFatJet_H1_pt.Write()
        hSemiresolved_H1Boosted_H2resolved_GenFatJet_H1_eta.Write()
        hSemiresolved_H1Boosted_H2resolved_GenJet_H2_b1_pt.Write()
        hSemiresolved_H1Boosted_H2resolved_GenJet_H2_b2_pt.Write()
        hSemiresolved_H1Boosted_H2resolved_GenJet_H2_b1_eta.Write()
        hSemiresolved_H1Boosted_H2resolved_GenJet_H2_b2_eta.Write()
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_pt.Write()
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_eta.Write()
        hSemiresolved_H1Boosted_H2resolved_RecoJet_H2_b1_pt.Write()
        hSemiresolved_H1Boosted_H2resolved_RecoJet_H2_b2_pt.Write()
        hSemiresolved_H1Boosted_H2resolved_RecoJet_H2_b1_eta.Write()
        hSemiresolved_H1Boosted_H2resolved_RecoJet_H2_b2_eta.Write()
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_mSD_Uncorrected.Write()
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_area.Write()
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_n2b1.Write()
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_n3b1.Write()
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_tau21.Write()
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_tau32.Write()
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_nsubjets.Write()
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_pt.Write()
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_eta.Write()
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_m.Write()
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_btag.Write()
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_pt.Write()
        hSemiresolved_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_eta.Write()
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
        hSemiresolved_H1Boosted_H2resolved_AK8PFHT.Write()
        
        hSemiresolved_H2Boosted_H1resolved_GenFatJet_H2_pt.Write()
        hSemiresolved_H2Boosted_H1resolved_GenFatJet_H2_eta.Write()
        hSemiresolved_H2Boosted_H1resolved_GenJet_H1_b1_pt.Write()
        hSemiresolved_H2Boosted_H1resolved_GenJet_H1_b2_pt.Write()
        hSemiresolved_H2Boosted_H1resolved_GenJet_H1_b1_eta.Write()
        hSemiresolved_H2Boosted_H1resolved_GenJet_H1_b2_eta.Write()
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_pt.Write()
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_eta.Write()
        hSemiresolved_H2Boosted_H1resolved_RecoJet_H1_b1_pt.Write()
        hSemiresolved_H2Boosted_H1resolved_RecoJet_H1_b2_pt.Write()
        hSemiresolved_H2Boosted_H1resolved_RecoJet_H1_b1_eta.Write()
        hSemiresolved_H2Boosted_H1resolved_RecoJet_H1_b2_eta.Write()
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_mSD_Uncorrected.Write()
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_area.Write()
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_n2b1.Write()
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_n3b1.Write()
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_tau21.Write()
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_tau32.Write()
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_nsubjets.Write()
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_pt.Write()
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_eta.Write()
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_m.Write()
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_btag.Write()
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_pt.Write()
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_eta.Write()
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_m.Write()
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_btag.Write()
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_TXbb.Write()        
        hSemiresolved_H2Boosted_H1resolved_NJets.Write()
        hSemiresolved_H2Boosted_H1resolved_NFatJets.Write()
        hSemiresolved_H2Boosted_H1resolved_AK8PFHT.Write()
        hSemiresolved_H2Boosted_H1resolved_DeltaR_H1_H2.Write()
        hSemiresolved_H2Boosted_H1resolved_DeltaEta_H1_H2.Write()
        hSemiresolved_H2Boosted_H1resolved_DeltaPhi_H1_H2.Write()
        hSemiresolved_H2Boosted_H1resolved_InvMass_H1.Write()
        hSemiresolved_H2Boosted_H1resolved_InvMassRegressed_H1.Write()
        hSemiresolved_H2Boosted_H1resolved_H1_pt.Write()
        hSemiresolved_H2Boosted_H1resolved_H1_eta.Write()
        hSemiresolved_H2Boosted_H1resolved_RecoFatJet_H2_m.Write()
        
        # Semiresolved exclusive category
        hSemiresolvedExcl_GenPart_H1_pt.Write()
        hSemiresolvedExcl_GenPart_H2_pt.Write()
        hSemiresolvedExcl_GenPart_H1_b1_pt.Write()
        hSemiresolvedExcl_GenPart_H1_b2_pt.Write()
        hSemiresolvedExcl_GenPart_H2_b1_pt.Write()
        hSemiresolvedExcl_GenPart_H2_b2_pt.Write()
        hSemiresolvedExcl_GenPart_H1_b1_eta.Write()
        hSemiresolvedExcl_GenPart_H1_b2_eta.Write()
        hSemiresolvedExcl_GenPart_H2_b1_eta.Write()
        hSemiresolvedExcl_GenPart_H2_b2_eta.Write()
        hSemiresolvedExcl_H1Boosted_H2resolved_GenFatJet_H1_pt.Write()
        hSemiresolvedExcl_H1Boosted_H2resolved_GenFatJet_H1_eta.Write()
        hSemiresolvedExcl_H1Boosted_H2resolved_GenJet_H2_b1_pt.Write()
        hSemiresolvedExcl_H1Boosted_H2resolved_GenJet_H2_b2_pt.Write()
        hSemiresolvedExcl_H1Boosted_H2resolved_GenJet_H2_b1_eta.Write()
        hSemiresolvedExcl_H1Boosted_H2resolved_GenJet_H2_b2_eta.Write()
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_pt.Write()
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_eta.Write()
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoJet_H2_b1_pt.Write()
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoJet_H2_b2_pt.Write()
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoJet_H2_b1_eta.Write()
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoJet_H2_b2_eta.Write()
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_mSD_Uncorrected.Write()
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_area.Write()
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_n2b1.Write()
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_n3b1.Write()
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_tau21.Write()
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_tau32.Write()
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_nsubjets.Write()
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_pt.Write()
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_eta.Write()
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_m.Write()
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_btag.Write()
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_pt.Write()
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_eta.Write()
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_m.Write()
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_btag.Write()
        hSemiresolvedExcl_H1Boosted_H2resolved_AK8PFHT.Write()
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_TXbb.Write()
        hSemiresolvedExcl_H1Boosted_H2resolved_NJets.Write()
        hSemiresolvedExcl_H1Boosted_H2resolved_NFatJets.Write()
        hSemiresolvedExcl_H1Boosted_H2resolved_DeltaR_H1_H2.Write()
        hSemiresolvedExcl_H1Boosted_H2resolved_DeltaEta_H1_H2.Write()
        hSemiresolvedExcl_H1Boosted_H2resolved_DeltaPhi_H1_H2.Write()
        hSemiresolvedExcl_H1Boosted_H2resolved_InvMass_H2.Write()
        hSemiresolvedExcl_H1Boosted_H2resolved_InvMassRegressed_H2.Write()
        hSemiresolvedExcl_H1Boosted_H2resolved_H2_pt.Write()
        hSemiresolvedExcl_H1Boosted_H2resolved_H2_eta.Write()
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_m.Write()
        hSemiresolvedExcl_H1Boosted_H2resolved_PFHT.Write()
        hSemiresolvedExcl_H1Boosted_H2resolved_NLooseBJets.Write()
        hSemiresolvedExcl_H1Boosted_H2resolved_NMediumBJets.Write()
        hSemiresolvedExcl_H1Boosted_H2resolved_NTightBJets.Write()
        hSemiresolvedExcl_H1Boosted_H2resolved_Jet1Pt.Write()
        hSemiresolvedExcl_H1Boosted_H2resolved_Jet2Pt.Write()
        hSemiresolvedExcl_H1Boosted_H2resolved_Jet3Pt.Write()
        hSemiresolvedExcl_H1Boosted_H2resolved_Jet4Pt.Write()
        hSemiresolvedExcl_H1Boosted_H2resolved_Jet1Eta.Write()
        hSemiresolvedExcl_H1Boosted_H2resolved_Jet2Eta.Write()
        hSemiresolvedExcl_H1Boosted_H2resolved_Jet3Eta.Write()
        hSemiresolvedExcl_H1Boosted_H2resolved_Jet4Eta.Write()
        hSemiresolvedExcl_H1Boosted_H2resolved_AK8Jet1Pt.Write()
        
        hSemiresolvedExcl_H2Boosted_H1resolved_GenFatJet_H2_pt.Write()
        hSemiresolvedExcl_H2Boosted_H1resolved_GenFatJet_H2_eta.Write()
        hSemiresolvedExcl_H2Boosted_H1resolved_GenJet_H1_b1_pt.Write()
        hSemiresolvedExcl_H2Boosted_H1resolved_GenJet_H1_b2_pt.Write()
        hSemiresolvedExcl_H2Boosted_H1resolved_GenJet_H1_b1_eta.Write()
        hSemiresolvedExcl_H2Boosted_H1resolved_GenJet_H1_b2_eta.Write()
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_pt.Write()
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_eta.Write()
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoJet_H1_b1_pt.Write()
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoJet_H1_b2_pt.Write()
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoJet_H1_b1_eta.Write()
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoJet_H1_b2_eta.Write()
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_mSD_Uncorrected.Write()
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_area.Write()
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_n2b1.Write()
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_n3b1.Write()
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_tau21.Write()
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_tau32.Write()
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_nsubjets.Write()
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_pt.Write()
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_eta.Write()
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_m.Write()
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_btag.Write()
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_pt.Write()
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_eta.Write()
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_m.Write()
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_btag.Write()
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_TXbb.Write()        
        hSemiresolvedExcl_H2Boosted_H1resolved_NJets.Write()
        hSemiresolvedExcl_H2Boosted_H1resolved_NFatJets.Write()
        hSemiresolvedExcl_H2Boosted_H1resolved_AK8PFHT.Write()
        hSemiresolvedExcl_H2Boosted_H1resolved_DeltaR_H1_H2.Write()
        hSemiresolvedExcl_H2Boosted_H1resolved_DeltaEta_H1_H2.Write()
        hSemiresolvedExcl_H2Boosted_H1resolved_DeltaPhi_H1_H2.Write()
        hSemiresolvedExcl_H2Boosted_H1resolved_InvMass_H1.Write()
        hSemiresolvedExcl_H2Boosted_H1resolved_InvMassRegressed_H1.Write()
        hSemiresolvedExcl_H2Boosted_H1resolved_H1_pt.Write()
        hSemiresolvedExcl_H2Boosted_H1resolved_H1_eta.Write()
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_m.Write()
                
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        # Printout statements
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        print("\nAll events %s" % (entries))
        print("Gen Resolved events %s" % (cIsResolvedGen))
        print("Gen Semi-Resolved events %s" % (cIsSemiResolvedGen))
        print("Gen Boosted events %s" % (cIsBoostedGen))
        print("\n")
        print("Resolved-favored:")
        print("Reco Resolved events (four b-quarks matched to reco-jets)            = %s" % (cIsResolvedReco))
        print("Reco Semi-resolved events exclusive (semi-resolved but not resolved) = %s" % (cIsSemiResolvedRecoExcl))
        print("Reco Boosted events exclusive (boosted but not resolved)             = %s" % (cIsBoostedRecoExcl))
        print("\n")
        print("Not resolved favored:")
        print("Reco Resolved exclusive events %s" % (cIsResolvedRecoExcl))
        print("Reco Semi-Resolved events %s" % (cIsSemiResolvedReco))
        print("Reco Boosted events %s" % (cIsBoostedReco))
        print("\n")
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
    OUTPUT        = "HHTo4B_12Jan2023.root"
    DIRNAME       = "root://cmseos.fnal.gov//store/user/mkolosov/MultiHiggs/DiHiggs/RunIIAutumn18_NoSelections_GluGluToHHTo4B_22Dec2022"
    STUDY         = "HHTo4B_Categorization"
    
    parser = ArgumentParser(description="Get the characteristics of the ggHH to 4b signal modes (resolved, semi-resolved, boosted)")
    parser.add_argument("-v", "--verbose", dest="verbose", default=VERBOSE, action="store_true", help="Verbose mode for debugging purposes [default: %s]" % (VERBOSE))
    parser.add_argument("-d", "--dir", dest="dirName", type=str, action="store", default=DIRNAME, help="Location of the samples (a directory above) [default: %s]" % (DIRNAME))
    parser.add_argument("--year", dest="year", action="store", default=YEAR, help="Process year")
    parser.add_argument("--output", dest="output", default=OUTPUT, action="store", help="The name of the output file")
    
    args = parser.parse_args()
    args.output = args.output + "_%s.root" % (args.year)
    main(args)

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
    
    samples = {
        #"GluGluToHHTo4B_node_cHHH0"    : args.dirName+"/GluGluToHHTo4B_node_cHHH0_TuneCP5_PSWeights_13TeV-powheg-pythia8/ntuple.root",
        "GluGluToHHTo4B_node_cHHH1"    : args.dirName+"/GluGluToHHTo4B_node_cHHH1_TuneCP5_PSWeights_13TeV-powheg-pythia8/ntuple.root",
        #"GluGluToHHTo4B_node_cHHH2p45" : args.dirName+"/GluGluToHHTo4B_node_cHHH2p45_TuneCP5_PSWeights_13TeV-powheg-pythia8/ntuple.root",
        #"GluGluToHHTo4B_node_cHHH5"    : args.dirName+"/GluGluToHHTo4B_node_cHHH5_TuneCP5_PSWeights_13TeV-powheg-pythia8/ntuple.root"}
    }
    fOut = ROOT.TFile.Open("histogramsForHHTo4b_22Jan2023v2.root", "RECREATE")
    
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
        h_GenPart_H1_pt  = ROOT.TH1F("h_GenPart_H1_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        h_GenPart_H2_pt  = ROOT.TH1F("h_GenPart_H2_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        h_GenPart_H1_eta = ROOT.TH1F("h_GenPart_H1_eta", ";#eta;Events", 120, -4.0, 4.0)
        h_GenPart_H2_eta = ROOT.TH1F("h_GenPart_H2_eta", ";#eta;Events", 120, -4.0, 4.0)
                
        h_GenPart_H1_b1_eta = ROOT.TH1F("h_GenPart_H1_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        h_GenPart_H1_b2_eta = ROOT.TH1F("h_GenPart_H1_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
        h_GenPart_H2_b1_eta = ROOT.TH1F("h_GenPart_H2_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        h_GenPart_H2_b2_eta = ROOT.TH1F("h_GenPart_H2_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
        
        h_GenPart_H1_b1_pt = ROOT.TH1F("h_GenPart_H1_b1_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        h_GenPart_H1_b2_pt = ROOT.TH1F("h_GenPart_H1_b2_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        h_GenPart_H2_b1_pt = ROOT.TH1F("h_GenPart_H2_b1_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        h_GenPart_H2_b2_pt = ROOT.TH1F("h_GenPart_H2_b2_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        
        h_NJets = ROOT.TH1F("h_NJets", ";jets multiplicity;Events", 15, 0, 15)
        h_Jet1Pt = ROOT.TH1F("h_Jet1Pt", ";Jet 1 p_{T} [GeV];Events", 100, 0.0, 500)
        h_Jet2Pt = ROOT.TH1F("h_Jet2Pt", ";Jet 2 p_{T} [GeV];Events", 100, 0.0, 500)
        h_Jet3Pt = ROOT.TH1F("h_Jet3Pt", ";Jet 3 p_{T} [GeV];Events", 100, 0.0, 500)
        h_Jet4Pt = ROOT.TH1F("h_Jet4Pt", ";Jet 4 p_{T} [GeV];Events", 100, 0.0, 500)
        h_NLooseBJets  = ROOT.TH1F("h_NLooseBJets", ";loose b-jets multiplicity;Events", 10, 0, 10)
        h_NMediumBJets = ROOT.TH1F("h_NMediumBJets", ";medium b-jets multiplicity;Events", 10, 0, 10)
        h_NTightBJets  = ROOT.TH1F("h_NTightBJets", ";tight b-jets multiplicity;Events", 10, 0, 10)
        h_NFatJets = ROOT.TH1F("h_NFatJets", ";fatjet multiplicity;Events", 10, 0, 10)
        h_AK8Jet1Pt = ROOT.TH1F("h_AK8Jet1Pt", "; fatjet 1 p_{T} [GeV];Events", 100, 0.0, 1000)
        h_AK8Jet2Pt = ROOT.TH1F("h_AK8Jet2Pt", "; fatjet 2 p_{T} [GeV];Events", 100, 0.0, 1000)
        h_AK8Jet3Pt = ROOT.TH1F("h_AK8Jet3Pt", "; fatjet 3 p_{T} [GeV];Events", 100, 0.0, 1000)
        h_AK8Jet4Pt = ROOT.TH1F("h_AK8Jet4Pt", "; fatjet 4 p_{T} [GeV];Events", 100, 0.0, 1000)
        
        h2D_NBQuarksMatchedTo_GenJetsVsGenFatJets = ROOT.TH2I("h2D_NBQuarksMatchedTo_GenJetsVsGenFatJets", ";b-quarks matched to gen-jets;b-quarks matched to gen-fatjets", 5, 0, 5, 5, 0, 5)
        h2D_NHiggsMatchedTo_GenJetsVsGenFatJets = ROOT.TH2I("h2D_NHiggsMatchedTo_GenJetsVsGenFatJets", ";Higgs matched to gen-jets; Higgs matched to gen-fatjets", 3, 0, 3, 3, 0, 3)
        
        h2D_NBQuarksMatchedTo_RecoJetsVsRecoFatJets = ROOT.TH2I("h2D_NBQuarksMatchedTo_RecoJetsVsRecoFatJets", ";b-quarks matched to reco-jets;b-quarks matched to reco-fatjets", 5, 0, 5, 5, 0, 5)
        h2D_NHiggsMatchedTo_RecoJetsVsRecoFatJets   = ROOT.TH2I("h2D_NHiggsMatchedTo_RecoJetsVsRecoFatJets", ";Higgs matched to reco-jets; Higgs matched to reco-fatjets", 3, 0, 3, 3, 0, 3)
        
        h_GenMatchingTo4RecoJets_Cases = ROOT.TH1F("h_GenMatchingTo4RecoJets_Cases", ";cases;Events", 14, 1, 15)
        
        #-----------------------------------------------------------------------------------------------------------
        h_IsBoostedGen_GenFatJet_H1_pt= ROOT.TH1F("h_IsBoostedGen_GenFatJet_H1_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        h_IsBoostedGen_GenFatJet_H2_pt= ROOT.TH1F("h_IsBoostedGen_GenFatJet_H2_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        h_IsSemiresolvedGen_GenFatJet_H1_pt = ROOT.TH1F("h_IsSemiresolvedGen_GenFatJet_H1_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        h_IsSemiresolvedGen_GenFatJet_H2_pt = ROOT.TH1F("h_IsSemiresolvedGen_GenFatJet_H2_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        h_GenFatJet_H1_pt = ROOT.TH1F("h_GenFatJet_H1_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        h_GenFatJet_H2_pt = ROOT.TH1F("h_GenFatJet_H2_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        
        h_IsBoostedGen_NotBoostedReco_GenFatJet_H1_pt = ROOT.TH1F("h_IsBoostedGen_NotBoostedReco_GenFatJet_H1_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        h_IsBoostedGen_NotBoostedReco_GenFatJet_H2_pt = ROOT.TH1F("h_IsBoostedGen_NotBoostedReco_GenFatJet_H2_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        h_IsSemiresolvedGen_NotSemiresolvedReco_GenFatJet_H1_pt = ROOT.TH1F("h_IsSemiresolvedGen_NotSemiresolvedReco_GenFatJet_H1_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        h_IsSemiresolvedGen_NotSemiresolvedReco_GenFatJet_H2_pt = ROOT.TH1F("h_IsSemiresolvedGen_NotSemiresolvedReco_GenFatJet_H2_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        
        #-----------------------------------------------------------------------------------------------------------
        
        hResolved_GenPart_H1_pt    = ROOT.TH1F("hResolved_GenPart_H1_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolved_GenPart_H2_pt    = ROOT.TH1F("hResolved_GenPart_H2_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolved_GenPart_H1_b1_pt = ROOT.TH1F("hResolved_GenPart_H1_b1_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolved_GenPart_H1_b2_pt = ROOT.TH1F("hResolved_GenPart_H1_b2_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolved_GenPart_H2_b1_pt = ROOT.TH1F("hResolved_GenPart_H2_b1_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolved_GenPart_H2_b2_pt = ROOT.TH1F("hResolved_GenPart_H2_b2_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolved_GenPart_H1_b1_eta = ROOT.TH1F("hResolved_GenPart_H1_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hResolved_GenPart_H1_b2_eta = ROOT.TH1F("hResolved_GenPart_H1_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hResolved_GenPart_H2_b1_eta = ROOT.TH1F("hResolved_GenPart_H2_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hResolved_GenPart_H2_b2_eta = ROOT.TH1F("hResolved_GenPart_H2_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
        
        hResolved_GenJet_H1_b1_pt  = ROOT.TH1F("hResolved_GenJet_H1_b1_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolved_GenJet_H1_b2_pt  = ROOT.TH1F("hResolved_GenJet_H1_b2_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolved_GenJet_H2_b1_pt  = ROOT.TH1F("hResolved_GenJet_H2_b1_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolved_GenJet_H2_b2_pt  = ROOT.TH1F("hResolved_GenJet_H2_b2_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolved_GenJet_H1_b1_eta = ROOT.TH1F("hResolved_GenJet_H1_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hResolved_GenJet_H1_b2_eta = ROOT.TH1F("hResolved_GenJet_H1_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hResolved_GenJet_H2_b1_eta = ROOT.TH1F("hResolved_GenJet_H2_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hResolved_GenJet_H2_b2_eta = ROOT.TH1F("hResolved_GenJet_H2_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
        
        hResolved_RecoJet_H1_b1_pt  = ROOT.TH1F("hResolved_RecoJet_H1_b1_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolved_RecoJet_H1_b2_pt  = ROOT.TH1F("hResolved_RecoJet_H1_b2_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolved_RecoJet_H2_b1_pt  = ROOT.TH1F("hResolved_RecoJet_H2_b1_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolved_RecoJet_H2_b2_pt  = ROOT.TH1F("hResolved_RecoJet_H2_b2_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
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
        hResolved_RecoJet_H1_pt  = ROOT.TH1F("hResolved_RecoJet_H1_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolved_RecoJet_H2_pt  = ROOT.TH1F("hResolved_RecoJet_H2_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolved_RecoJet_H1_eta = ROOT.TH1F("hResolved_RecoJet_H1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hResolved_RecoJet_H2_eta = ROOT.TH1F("hResolved_RecoJet_H2_eta", ";#eta;Events", 120, -4.0, 4.0)
        
        hResolved_RecoJet_InvMass_H1 = ROOT.TH1F("hResolved_RecoJet_InvMass_H1", ";m_{H} [GeV]", 150, 0, 300)
        hResolved_RecoJet_InvMass_H2 = ROOT.TH1F("hResolved_RecoJet_InvMass_H2", ";m_{H} [GeV]", 150, 0, 300)
        hResolved_RecoJet_InvMassRegressed_H1 = ROOT.TH1F("hResolved_RecoJet_InvMassRegressed_H1", ";m_{H} [GeV]", 150, 0, 300)
        hResolved_RecoJet_InvMassRegressed_H2 = ROOT.TH1F("hResolved_RecoJet_InvMassRegressed_H2", ";m_{H} [GeV]", 150, 0, 300)
        hResolved_RecoJet_DeltaR_H1_H2 = ROOT.TH1F("hResolved_RecoJet_DeltaR_H1_H2", ";#Delta R;Events", 100, 0.0, 5.0)
        hResolved_RecoJet_DeltaEta_H1_H2 = ROOT.TH1F("hResolved_RecoJet_DeltaEta_H1_H2", ";#Delta#eta;Events", 50, 0.0, 5.0)
        hResolved_RecoJet_DeltaPhi_H1_H2 = ROOT.TH1F("hResolved_RecoJet_DeltaPhi_H1_H2", ";#Delta#phi;Events", 50, 0.0,5.0)
        hResolved_RecoJet_NJets = ROOT.TH1F("hResolved_RecoJet_NJets", "; jet multiplicity;Events", 15, 0, 15)
        hResolved_RecoJet_NFatJets = ROOT.TH1F("hResolved_RecoJet_NFatJets", "; fatjet multiplicity;Events", 10, 0, 10)
        hResolved_RecoJet_PFHT = ROOT.TH1F("hResolved_RecoJet_PFHT", "; PF H_{T} [GeV];Events", 125, 0.0, 2500)
        hResolved_RecoJet_NLooseBJets = ROOT.TH1F("hResolved_RecoJet_NLooseBJets", ";b-jets L;Events", 10, 0, 10)
        hResolved_RecoJet_NMediumBJets = ROOT.TH1F("hResolved_RecoJet_NMediumBJets", ";b-jets M;Events", 10, 0, 10)
        hResolved_RecoJet_NTightBJets = ROOT.TH1F("hResolved_RecoJet_NTightBJets", ";b-jets T;Events", 10, 0, 10)
        hResolved_RecoJet_Jet1Pt = ROOT.TH1F("hResolved_RecoJet_Jet1Pt", ";jet 1 p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolved_RecoJet_Jet2Pt = ROOT.TH1F("hResolved_RecoJet_Jet2Pt", ";jet 2 p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolved_RecoJet_Jet3Pt = ROOT.TH1F("hResolved_RecoJet_Jet3Pt", ";jet 3 p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolved_RecoJet_Jet4Pt = ROOT.TH1F("hResolved_RecoJet_Jet4Pt", ";jet 4 p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolved_RecoJet_Jet1Eta = ROOT.TH1F("hResolved_RecoJet_Jet1Eta", ";jet 1 #eta;Events", 120, -4.0, 4.0)
        hResolved_RecoJet_Jet2Eta = ROOT.TH1F("hResolved_RecoJet_Jet2Eta", ";jet 2 #eta;Events", 120, -4.0, 4.0)
        hResolved_RecoJet_Jet3Eta = ROOT.TH1F("hResolved_RecoJet_Jet3Eta", ";jet 3 #eta;Events", 120, -4.0, 4.0)
        hResolved_RecoJet_Jet4Eta = ROOT.TH1F("hResolved_RecoJet_Jet4Eta", ";jet 4 #eta;Events", 120, -4.0, 4.0)
        hResolved_RecoJet_AK8Jet1Pt = ROOT.TH1F("hResolved_RecoJet_AK8Jet1Pt", "; fatjet 1 p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolved_RecoJet_AK8Jet2Pt = ROOT.TH1F("hResolved_RecoJet_AK8Jet2Pt", "; fatjet 2 p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolved_RecoJet_AK8Jet3Pt = ROOT.TH1F("hResolved_RecoJet_AK8Jet3Pt", "; fatjet 3 p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolved_RecoJet_AK8Jet4Pt = ROOT.TH1F("hResolved_RecoJet_AK8Jet4Pt", "; fatjet 4 p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolved_RecoJet_AK8PFHT   = ROOT.TH1F("hResolved_RecoJet_AK8PFHT", "; AK8 PF H_{T} [GeV];Events", 125, 0.0, 2500)

        # Case 10
        hResolvedCase10_GenPart_H1_pt = ROOT.TH1F("hResolvedCase10_GenPart_H1_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase10_GenPart_H2_pt = ROOT.TH1F("hResolvedCase10_GenPart_H2_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase10_GenPart_H1_b1_pt = ROOT.TH1F("hResolvedCase10_GenPart_H1_b1_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase10_GenPart_H1_b2_pt = ROOT.TH1F("hResolvedCase10_GenPart_H1_b2_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase10_GenPart_H2_b1_pt = ROOT.TH1F("hResolvedCase10_GenPart_H2_b1_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase10_GenPart_H2_b2_pt = ROOT.TH1F("hResolvedCase10_GenPart_H2_b2_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase10_RecoJet_H1_b1_pt = ROOT.TH1F("hResolvedCase10_RecoJet_H1_b1_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase10_RecoJet_H1_b2_pt = ROOT.TH1F("hResolvedCase10_RecoJet_H1_b2_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase10_RecoJet_H2_b1_pt = ROOT.TH1F("hResolvedCase10_RecoJet_H2_b1_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase10_RecoJet_H2_b2_pt = ROOT.TH1F("hResolvedCase10_RecoJet_H2_b2_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase10_RecoJet_H1_pt = ROOT.TH1F("hResolvedCase10_RecoJet_H1_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase10_RecoJet_H2_pt = ROOT.TH1F("hResolvedCase10_RecoJet_H2_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase10_RecoJet_InvMass_H1 = ROOT.TH1F("hResolvedCase10_RecoJet_InvMass_H1", ";m_{H} [GeV]", 150, 0, 300)
        hResolvedCase10_RecoJet_InvMass_H2 = ROOT.TH1F("hResolvedCase10_RecoJet_InvMass_H2", ";m_{H} [GeV]", 150, 0, 300)
        hResolvedCase10_RecoJet_NJets = ROOT.TH1F("hResolvedCase10_RecoJet_NJets", "; jet multiplicity;Events", 15, 0, 15)
        hResolvedCase10_RecoJet_NFatJets = ROOT.TH1F("hResolvedCase10_RecoJet_NFatJets", "; fatjet multiplicity;Events", 15, 0, 15)
        hResolvedCase10_RecoFatJet_H1_pt = ROOT.TH1F("hResolvedCase10_RecoFatJet_H1_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase10_RecoFatJet_H2_pt = ROOT.TH1F("hResolvedCase10_RecoFatJet_H2_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase10_RecoFatJet_H1_m = ROOT.TH1F("hResolvedCase10_RecoFatJet_H1_m", ";m_{H} [GeV]", 150, 0, 300)
        hResolvedCase10_RecoFatJet_H2_m = ROOT.TH1F("hResolvedCase10_RecoFatJet_H2_m", ";m_{H} [GeV]", 150, 0, 300)
        hResolvedCase10_RecoJet_AK8Jet1Pt = ROOT.TH1F("hResolvedCase10_RecoJet_AK8Jet1Pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase10_RecoJet_AK8Jet2Pt = ROOT.TH1F("hResolvedCase10_RecoJet_AK8Jet2Pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase10_RecoJet_AK8Jet3Pt = ROOT.TH1F("hResolvedCase10_RecoJet_AK8Jet3Pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase10_RecoJet_AK8Jet4Pt = ROOT.TH1F("hResolvedCase10_RecoJet_AK8Jet4Pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        # Case 1
        hResolvedCase1_GenPart_H1_pt = ROOT.TH1F("hResolvedCase1_GenPart_H1_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase1_GenPart_H2_pt = ROOT.TH1F("hResolvedCase1_GenPart_H2_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase1_GenPart_H1_b1_pt = ROOT.TH1F("hResolvedCase1_GenPart_H1_b1_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase1_GenPart_H1_b2_pt = ROOT.TH1F("hResolvedCase1_GenPart_H1_b2_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase1_GenPart_H2_b1_pt = ROOT.TH1F("hResolvedCase1_GenPart_H2_b1_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase1_GenPart_H2_b2_pt = ROOT.TH1F("hResolvedCase1_GenPart_H2_b2_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase1_RecoJet_H1_b1_pt = ROOT.TH1F("hResolvedCase1_RecoJet_H1_b1_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase1_RecoJet_H1_b2_pt = ROOT.TH1F("hResolvedCase1_RecoJet_H1_b2_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase1_RecoJet_H2_b1_pt = ROOT.TH1F("hResolvedCase1_RecoJet_H2_b1_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase1_RecoJet_H2_b2_pt = ROOT.TH1F("hResolvedCase1_RecoJet_H2_b2_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase1_RecoJet_H1_pt = ROOT.TH1F("hResolvedCase1_RecoJet_H1_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase1_RecoJet_H2_pt = ROOT.TH1F("hResolvedCase1_RecoJet_H2_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase1_RecoJet_InvMass_H1 = ROOT.TH1F("hResolvedCase1_RecoJet_InvMass_H1", ";m_{H} [GeV]", 150, 0, 300)
        hResolvedCase1_RecoJet_InvMass_H2 = ROOT.TH1F("hResolvedCase1_RecoJet_InvMass_H2", ";m_{H} [GeV]", 150, 0, 300)
        hResolvedCase1_RecoJet_NJets      = ROOT.TH1F("hResolvedCase1_RecoJet_NJets", "; jet multiplicity;Events", 15, 0, 15)
        hResolvedCase1_RecoJet_NFatJets   = ROOT.TH1F("hResolvedCase1_RecoJet_NFatJets", "; fatjet multiplicity;Events", 15, 0, 15)
        hResolvedCase1_RecoJet_AK8Jet1Pt  = ROOT.TH1F("hResolvedCase1_RecoJet_AK8Jet1Pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase1_RecoJet_AK8Jet2Pt  = ROOT.TH1F("hResolvedCase1_RecoJet_AK8Jet2Pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase1_RecoJet_AK8Jet3Pt  = ROOT.TH1F("hResolvedCase1_RecoJet_AK8Jet3Pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase1_RecoJet_AK8Jet4Pt  = ROOT.TH1F("hResolvedCase1_RecoJet_AK8Jet4Pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        # Case 6
        hResolvedCase6_GenPart_H1_pt = ROOT.TH1F("hResolvedCase6_GenPart_H1_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase6_GenPart_H2_pt = ROOT.TH1F("hResolvedCase6_GenPart_H2_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase6_GenPart_H1_b1_pt = ROOT.TH1F("hResolvedCase6_GenPart_H1_b1_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase6_GenPart_H1_b2_pt = ROOT.TH1F("hResolvedCase6_GenPart_H1_b2_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase6_GenPart_H2_b1_pt = ROOT.TH1F("hResolvedCase6_GenPart_H2_b1_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase6_GenPart_H2_b2_pt = ROOT.TH1F("hResolvedCase6_GenPart_H2_b2_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase6_RecoJet_H1_b1_pt = ROOT.TH1F("hResolvedCase6_RecoJet_H1_b1_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase6_RecoJet_H1_b2_pt = ROOT.TH1F("hResolvedCase6_RecoJet_H1_b2_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase6_RecoJet_H2_b1_pt = ROOT.TH1F("hResolvedCase6_RecoJet_H2_b1_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase6_RecoJet_H2_b2_pt = ROOT.TH1F("hResolvedCase6_RecoJet_H2_b2_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase6_RecoJet_H1_pt = ROOT.TH1F("hResolvedCase6_RecoJet_H1_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase6_RecoJet_H2_pt = ROOT.TH1F("hResolvedCase6_RecoJet_H2_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase6_RecoJet_InvMass_H1 = ROOT.TH1F("hResolvedCase6_RecoJet_InvMass_H1", ";m_{H} [GeV]", 150, 0, 300)
        hResolvedCase6_RecoJet_InvMass_H2 = ROOT.TH1F("hResolvedCase6_RecoJet_InvMass_H2", ";m_{H} [GeV]", 150, 0, 300)
        hResolvedCase6_RecoJet_NJets      = ROOT.TH1F("hResolvedCase6_RecoJet_NJets", "; jet multiplicity;Events", 15, 0, 15)
        hResolvedCase6_RecoJet_NFatJets   = ROOT.TH1F("hResolvedCase6_RecoJet_NFatJets", "; fatjet multiplicity;Events", 15, 0, 15)
        hResolvedCase6_RecoFatJet_H1_pt   = ROOT.TH1F("hResolvedCase6_RecoFatJet_H1_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase6_RecoJet_AK8Jet1Pt  = ROOT.TH1F("hResolvedCase6_RecoJet_AK8Jet1Pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase6_RecoJet_AK8Jet2Pt  = ROOT.TH1F("hResolvedCase6_RecoJet_AK8Jet2Pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase6_RecoJet_AK8Jet3Pt  = ROOT.TH1F("hResolvedCase6_RecoJet_AK8Jet3Pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase6_RecoJet_AK8Jet4Pt  = ROOT.TH1F("hResolvedCase6_RecoJet_AK8Jet4Pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        # Case 13
        hResolvedCase13_GenPart_H1_pt = ROOT.TH1F("hResolvedCase13_GenPart_H1_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase13_GenPart_H2_pt = ROOT.TH1F("hResolvedCase13_GenPart_H2_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase13_GenPart_H1_b1_pt = ROOT.TH1F("hResolvedCase13_GenPart_H1_b1_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase13_GenPart_H1_b2_pt = ROOT.TH1F("hResolvedCase13_GenPart_H1_b2_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase13_GenPart_H2_b1_pt = ROOT.TH1F("hResolvedCase13_GenPart_H2_b1_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase13_GenPart_H2_b2_pt = ROOT.TH1F("hResolvedCase13_GenPart_H2_b2_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase13_RecoJet_H1_b1_pt = ROOT.TH1F("hResolvedCase13_RecoJet_H1_b1_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase13_RecoJet_H1_b2_pt = ROOT.TH1F("hResolvedCase13_RecoJet_H1_b2_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase13_RecoJet_H2_b1_pt = ROOT.TH1F("hResolvedCase13_RecoJet_H2_b1_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase13_RecoJet_H2_b2_pt = ROOT.TH1F("hResolvedCase13_RecoJet_H2_b2_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase13_RecoJet_H1_pt = ROOT.TH1F("hResolvedCase13_RecoJet_H1_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase13_RecoJet_H2_pt = ROOT.TH1F("hResolvedCase13_RecoJet_H2_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase13_RecoJet_InvMass_H1 = ROOT.TH1F("hResolvedCase13_RecoJet_InvMass_H1", ";m_{H} [GeV]", 150, 0, 300)
        hResolvedCase13_RecoJet_InvMass_H2 = ROOT.TH1F("hResolvedCase13_RecoJet_InvMass_H2", ";m_{H} [GeV]", 150, 0, 300)
        hResolvedCase13_RecoJet_NJets      = ROOT.TH1F("hResolvedCase13_RecoJet_NJets", "; jet multiplicity;Events", 15, 0, 15)
        hResolvedCase13_RecoJet_NFatJets   = ROOT.TH1F("hResolvedCase13_RecoJet_NFatJets", "; fatjet multiplicity;Events", 15, 0, 15)
        hResolvedCase13_RecoFatJet_H1_pt   = ROOT.TH1F("hResolvedCase13_RecoFatJet_H1_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase13_RecoJet_AK8Jet1Pt  = ROOT.TH1F("hResolvedCase13_RecoJet_AK8Jet1Pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase13_RecoJet_AK8Jet2Pt  = ROOT.TH1F("hResolvedCase13_RecoJet_AK8Jet2Pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase13_RecoJet_AK8Jet3Pt  = ROOT.TH1F("hResolvedCase13_RecoJet_AK8Jet3Pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase13_RecoJet_AK8Jet4Pt  = ROOT.TH1F("hResolvedCase13_RecoJet_AK8Jet4Pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        # Case 7
        hResolvedCase7_GenPart_H1_pt = ROOT.TH1F("hResolvedCase7_GenPart_H1_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase7_GenPart_H2_pt = ROOT.TH1F("hResolvedCase7_GenPart_H2_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase7_GenPart_H1_b1_pt = ROOT.TH1F("hResolvedCase7_GenPart_H1_b1_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase7_GenPart_H1_b2_pt = ROOT.TH1F("hResolvedCase7_GenPart_H1_b2_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase7_GenPart_H2_b1_pt = ROOT.TH1F("hResolvedCase7_GenPart_H2_b1_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase7_GenPart_H2_b2_pt = ROOT.TH1F("hResolvedCase7_GenPart_H2_b2_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase7_RecoJet_H1_b1_pt = ROOT.TH1F("hResolvedCase7_RecoJet_H1_b1_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase7_RecoJet_H1_b2_pt = ROOT.TH1F("hResolvedCase7_RecoJet_H1_b2_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase7_RecoJet_H2_b1_pt = ROOT.TH1F("hResolvedCase7_RecoJet_H2_b1_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase7_RecoJet_H2_b2_pt = ROOT.TH1F("hResolvedCase7_RecoJet_H2_b2_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase7_RecoJet_H1_pt = ROOT.TH1F("hResolvedCase7_RecoJet_H1_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase7_RecoJet_H2_pt = ROOT.TH1F("hResolvedCase7_RecoJet_H2_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase7_RecoJet_InvMass_H1 = ROOT.TH1F("hResolvedCase7_RecoJet_InvMass_H1", ";m_{H} [GeV]", 150, 0, 300)
        hResolvedCase7_RecoJet_InvMass_H2 = ROOT.TH1F("hResolvedCase7_RecoJet_InvMass_H2", ";m_{H} [GeV]", 150, 0, 300)
        hResolvedCase7_RecoJet_NJets      = ROOT.TH1F("hResolvedCase7_RecoJet_NJets", "; jet multiplicity;Events", 15, 0, 15)
        hResolvedCase7_RecoJet_NFatJets   = ROOT.TH1F("hResolvedCase7_RecoJet_NFatJets", "; fatjet multiplicity;Events", 15, 0, 15)
        hResolvedCase7_RecoFatJet_H1_pt   = ROOT.TH1F("hResolvedCase7_RecoFatJet_H1_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase7_RecoJet_AK8Jet1Pt  = ROOT.TH1F("hResolvedCase7_RecoJet_AK8Jet1Pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase7_RecoJet_AK8Jet2Pt  = ROOT.TH1F("hResolvedCase7_RecoJet_AK8Jet2Pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase7_RecoJet_AK8Jet3Pt  = ROOT.TH1F("hResolvedCase7_RecoJet_AK8Jet3Pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hResolvedCase7_RecoJet_AK8Jet4Pt  = ROOT.TH1F("hResolvedCase7_RecoJet_AK8Jet4Pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        
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
        hBoostedExcl_GenPart_H1_pt    = ROOT.TH1F("hBoostedExcl_GenPart_H1_pt", ";p_{T} [GeV];Events", 100, 0.0, 2000)
        hBoostedExcl_GenPart_H2_pt    = ROOT.TH1F("hBoostedExcl_GenPart_H2_pt", ";p_{T} [GeV];Events", 100, 0.0, 2000)
        hBoostedExcl_GenPart_H1_b1_pt = ROOT.TH1F("hBoostedExcl_GenPart_H1_b1_pt", ";p_{T} [GeV];Events", 100, 0.0, 2000)
        hBoostedExcl_GenPart_H1_b2_pt = ROOT.TH1F("hBoostedExcl_GenPart_H1_b2_pt", ";p_{T} [GeV];Events", 100, 0.0, 2000)
        hBoostedExcl_GenPart_H2_b1_pt = ROOT.TH1F("hBoostedExcl_GenPart_H2_b1_pt", ";p_{T} [GeV];Events", 100, 0.0, 2000)
        hBoostedExcl_GenPart_H2_b2_pt = ROOT.TH1F("hBoostedExcl_GenPart_H2_b2_pt", ";p_{T} [GeV];Events", 100, 0.0, 2000)
        hBoostedExcl_GenPart_H1_b1_eta = ROOT.TH1F("hBoostedExcl_GenPart_H1_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hBoostedExcl_GenPart_H1_b2_eta = ROOT.TH1F("hBoostedExcl_GenPart_H1_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hBoostedExcl_GenPart_H2_b1_eta = ROOT.TH1F("hBoostedExcl_GenPart_H2_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hBoostedExcl_GenPart_H2_b2_eta = ROOT.TH1F("hBoostedExcl_GenPart_H2_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hBoostedExcl_GenFatJet_H1_pt  = ROOT.TH1F("hBoostedExcl_GenFatJet_H1_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hBoostedExcl_GenFatJet_H2_pt  = ROOT.TH1F("hBoostedExcl_GenFatJet_H2_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hBoostedExcl_GenFatJet_H1_eta = ROOT.TH1F("hBoostedExcl_GenFatJet_H1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hBoostedExcl_GenFatJet_H2_eta = ROOT.TH1F("hBoostedExcl_GenFatJet_H2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hBoostedExcl_RecoFatJet_H1_pt  = ROOT.TH1F("hBoostedExcl_RecoFatJet_H1_pt", ";p_{T} [GeV];Events", 100, 0.0, 2000)
        hBoostedExcl_RecoFatJet_H2_pt  = ROOT.TH1F("hBoostedExcl_RecoFatJet_H2_pt", ";p_{T} [GeV];Events", 100, 0.0, 2000)
        hBoostedExcl_RecoFatJet_H1_eta = ROOT.TH1F("hBoostedExcl_RecoFatJet_H1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hBoostedExcl_RecoFatJet_H2_eta = ROOT.TH1F("hBoostedExcl_RecoFatJet_H2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hBoostedExcl_RecoFatJet_H1_TXbb = ROOT.TH1F("hBoostedExcl_RecoFatJet_H1_TXbb", ";T_{Xbb} score;Events", 100, 0.0, 1.0)
        hBoostedExcl_RecoFatJet_H2_TXbb = ROOT.TH1F("hBoostedExcl_RecoFatJet_H2_TXbb", ";T_{Xbb} score;Events", 100, 0.0, 1.0)
        hBoostedExcl_RecoFatJet_H1_m = ROOT.TH1F("hBoostedExcl_RecoFatJet_H1_m", ";M [GeV];Events", 300, 0.0, 300)
        hBoostedExcl_RecoFatJet_H2_m = ROOT.TH1F("hBoostedExcl_RecoFatJet_H2_m", ";M [GeV];Events", 300, 0.0, 300)
        hBoostedExcl_NJets = ROOT.TH1F("hBoostedExcl_NJets", ";jets multiplicity;Events", 15, 0, 15)
        hBoostedExcl_AK4PFHT = ROOT.TH1F("hBoostedExcl_AK4PFHT", "; PF H_{T} [GeV];Events", 125, 0.0, 2500)
        hBoostedExcl_RecoJet_NLooseBJets = ROOT.TH1F("hBoostedExcl_RecoJet_NLooseBJets", ";b-jets L;Events", 10, 0, 10)
        hBoostedExcl_RecoJet_NMediumBJets = ROOT.TH1F("hBoostedExcl_RecoJet_NMediumBJets", ";b-jets M;Events", 10, 0, 10)
        hBoostedExcl_RecoJet_NTightBJets = ROOT.TH1F("hBoostedExcl_RecoJet_NTightBJets", ";b-jets T;Events", 10, 0, 10)
        #=====================
        hBoostedExcl_NFatJets = ROOT.TH1F("hBoostedExcl_NFatJets", ";fatjets multiplicity;Events", 10, 0, 10)
        hBoostedExcl_AK8PFHT = ROOT.TH1F("hBoostedExcl_AK8PFHT", ";AK8 PF H_{T} [GeV];Events", 125, 0.0, 2500)
        hBoostedExcl_AK8Jet1Pt = ROOT.TH1F("hBoostedExcl_AK8Jet1Pt", "; fatjet 1 p_{T} [GeV];Events", 100, 0.0, 1000)
        hBoostedExcl_AK8Jet2Pt = ROOT.TH1F("hBoostedExcl_AK8Jet2Pt", "; fatjet 2 p_{T} [GeV];Events", 100, 0.0, 1000)
        hBoostedExcl_AK8Jet3Pt = ROOT.TH1F("hBoostedExcl_AK8Jet3Pt", "; fatjet 3 p_{T} [GeV];Events", 100, 0.0, 1000)
        hBoostedExcl_AK8Jet4Pt = ROOT.TH1F("hBoostedExcl_AK8Jet4Pt", "; fatjet 4 p_{T} [GeV];Events", 100, 0.0, 1000)
        #===================
        hBoostedExcl_RecoFatJet_DeltaR_H1_H2 = ROOT.TH1F("hBoostedExcl_RecoFatJet_DeltaR_H1_H2", ";#Delta R;Events", 100, 0.0, 5.0)
        hBoostedExcl_RecoFatJet_DeltaEta_H1_H2 = ROOT.TH1F("hBoostedExcl_RecoFatJet_DeltaEta_H1_H2", ";#Delta#eta;Events", 50, 0.0, 5.0)
        hBoostedExcl_RecoFatJet_DeltaPhi_H1_H2 = ROOT.TH1F("hBoostedExcl_RecoFatJet_DeltaPhi_H1_H2", ";#Delta#phi;Events", 50, 0.0, 5.0)
        hBoostedExcl_RecoFatJet_H1_mSD_Uncorrected = ROOT.TH1F("hBoostedExcl_RecoFatJet_H1_mSD_Uncorrected", ";m_{SD} [GeV];Events", 150, 0, 300)
        hBoostedExcl_RecoFatJet_H1_area = ROOT.TH1F("hBoostedExcl_RecoFatJet_H1_area", ";area;Events", 100, 0.0, 5.0)
        hBoostedExcl_RecoFatJet_H1_n2b1 = ROOT.TH1F("hBoostedExcl_RecoFatJet_H1_n2b1", ";n2b1;Events", 100, 0.0, 5.0)
        hBoostedExcl_RecoFatJet_H1_n3b1 = ROOT.TH1F("hBoostedExcl_RecoFatJet_H1_n3b1", ";n3b1;Events", 100, 0.0, 5.0)
        hBoostedExcl_RecoFatJet_H1_tau21 = ROOT.TH1F("hBoostedExcl_RecoFatJet_H1_tau21", ";#tau_{21};Events", 100, 0.0, 2.5)
        hBoostedExcl_RecoFatJet_H1_tau32 = ROOT.TH1F("hBoostedExcl_RecoFatJet_H1_tau32", ";#tau_{32};Events", 100, 0.0, 2.5)
        hBoostedExcl_RecoFatJet_H1_nsubjets = ROOT.TH1F("hBoostedExcl_RecoFatJet_H1_nsubjets", ";subjet multiplicity;Events", 3, 0, 3)
        hBoostedExcl_RecoFatJet_H1_subjet1_pt = ROOT.TH1F("hBoostedExcl_RecoFatJet_H1_subjet1_pt", ";subjet 1 p_{T} [GeV];Events", 250, 0.0, 1000)
        hBoostedExcl_RecoFatJet_H1_subjet1_eta = ROOT.TH1F("hBoostedExcl_RecoFatJet_H1_subjet1_eta", ";subjet 1 #eta;Events", 120, -4.0, 4.0)
        hBoostedExcl_RecoFatJet_H1_subjet1_m = ROOT.TH1F("hBoostedExcl_RecoFatJet_H1_subjet1_m", ";subjet 1 M [GeV];Events", 200, 0.0, 800)
        hBoostedExcl_RecoFatJet_H1_subjet1_btag = ROOT.TH1F("hBoostedExcl_RecoFatJet_H1_subjet1_btag", ";subjet 1 b-discriminator;Events", 100, 0.0, 1.0)
        hBoostedExcl_RecoFatJet_H1_subjet2_pt = ROOT.TH1F("hBoostedExcl_RecoFatJet_H1_subjet2_pt", ";subjet 2 p_{T} [GeV];Events", 250, 0.0, 1000)
        hBoostedExcl_RecoFatJet_H1_subjet2_eta = ROOT.TH1F("hBoostedExcl_RecoFatJet_H1_subjet2_eta", ";subjet 2 #eta;Events", 120, -4.0, 4.0)
        hBoostedExcl_RecoFatJet_H1_subjet2_m = ROOT.TH1F("hBoostedExcl_RecoFatJet_H1_subjet2_m", ";subjet 2 M [GeV];Events", 200, 0.0, 800)
        hBoostedExcl_RecoFatJet_H1_subjet2_btag = ROOT.TH1F("hBoostedExcl_RecoFatJet_H1_subjet2_btag", ";subjet 2 b-discriminator;Events", 100,0.0, 1.0)
        hBoostedExcl_RecoFatJet_H2_mSD_Uncorrected = ROOT.TH1F("hBoostedExcl_RecoFatJet_H2_mSD_Uncorrected", ";m_{SD} [GeV];Events", 150, 0, 300)
        hBoostedExcl_RecoFatJet_H2_area = ROOT.TH1F("hBoostedExcl_RecoFatJet_H2_area", ";area;Events", 100, 0.0, 5.0)
        hBoostedExcl_RecoFatJet_H2_n2b1 = ROOT.TH1F("hBoostedExcl_RecoFatJet_H2_n2b1", ";n2b1;Events", 100, 0.0, 5.0)
        hBoostedExcl_RecoFatJet_H2_n3b1 = ROOT.TH1F("hBoostedExcl_RecoFatJet_H2_n3b1", ";n3b1;Events", 100, 0.0, 5.0)
        hBoostedExcl_RecoFatJet_H2_tau21 = ROOT.TH1F("hBoostedExcl_RecoFatJet_H2_tau21", ";#tau_{21};Events", 100, 0.0, 2.5)
        hBoostedExcl_RecoFatJet_H2_tau32 = ROOT.TH1F("hBoostedExcl_RecoFatJet_H2_tau32", ";#tau_{32};Events", 100, 0.0,2.5)
        hBoostedExcl_RecoFatJet_H2_nsubjets = ROOT.TH1F("hBoostedExcl_RecoFatJet_H2_nsubjets", ";subjet multiplicity;Events", 3, 0, 3)
        hBoostedExcl_RecoFatJet_H2_subjet1_eta = ROOT.TH1F("hBoostedExcl_RecoFatJet_H2_subjet1_eta", ";subjet 1 #eta;Events", 120, -4.0, 4.0)
        hBoostedExcl_RecoFatJet_H2_subjet1_m = ROOT.TH1F("hBoostedExcl_RecoFatJet_H2_subjet1_m", ";subjet 1 M [GeV];Events", 200, 0.0, 800)
        hBoostedExcl_RecoFatJet_H2_subjet1_btag = ROOT.TH1F("hBoostedExcl_RecoFatJet_H2_subjet1_btag", ";subjet 1 b-discriminator;Events", 100, 0.0, 1.0)
        hBoostedExcl_RecoFatJet_H2_subjet1_pt = ROOT.TH1F("hBoostedExcl_RecoFatJet_H2_subjet1_pt", ";subjet 1 p_{T} [GeV];Events", 100, 0.0, 1000)
        hBoostedExcl_RecoFatJet_H2_subjet2_pt = ROOT.TH1F("hBoostedExcl_RecoFatJet_H2_subjet2_pt", ";subjet 2 p_{T} [GeV];Events", 100, 0.0, 1000)
        hBoostedExcl_RecoFatJet_H2_subjet2_eta = ROOT.TH1F("hBoostedExcl_RecoFatJet_H2_subjet2_eta", ";subjet 2 #eta;Events", 120, -4.0, 4.0)
        hBoostedExcl_RecoFatJet_H2_subjet2_m = ROOT.TH1F("hBoostedExcl_RecoFatJet_H2_subjet2_m", ";subjet 2 M [GeV];Events", 200, 0.0, 800)
        hBoostedExcl_RecoFatJet_H2_subjet2_btag = ROOT.TH1F("hBoostedExcl_RecoFatJet_H2_subjet2_btag", ";subjet 2 b-discriminator;Events", 100,0.0, 1.0)
        hBoostedExcl_Jet1Pt = ROOT.TH1F("hBoostedExcl_Jet1Pt", ";jet 1 p_{T} [GeV];Events", 100, 0.0, 1000)
        hBoostedExcl_Jet2Pt = ROOT.TH1F("hBoostedExcl_Jet2Pt", ";jet 2 p_{T} [GeV];Events", 100, 0.0, 1000)
        hBoostedExcl_Jet3Pt = ROOT.TH1F("hBoostedExcl_Jet3Pt", ";jet 3 p_{T} [GeV];Events", 100, 0.0, 1000)
        hBoostedExcl_Jet4Pt = ROOT.TH1F("hBoostedExcl_Jet4Pt", ";jet 4 p_{T} [GeV];Events", 100, 0.0, 1000)

        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        # Semi-resolved exclusive regime
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        hSemiresolvedExcl_GenPart_H1_pt    = ROOT.TH1F("hSemiresolvedExcl_GenPart_H1_pt", ";p_{T} [GeV];Events", 100, 0.0, 2000)
        hSemiresolvedExcl_GenPart_H2_pt    = ROOT.TH1F("hSemiresolvedExcl_GenPart_H2_pt", ";p_{T} [GeV];Events", 100, 0.0, 2000)
        hSemiresolvedExcl_GenPart_H1_b1_pt = ROOT.TH1F("hSemiresolvedExcl_GenPart_H1_b1_pt", ";p_{T} [GeV];Events", 100, 0.0, 2000)
        hSemiresolvedExcl_GenPart_H1_b2_pt = ROOT.TH1F("hSemiresolvedExcl_GenPart_H1_b2_pt", ";p_{T} [GeV];Events", 100, 0.0, 2000)
        hSemiresolvedExcl_GenPart_H2_b1_pt = ROOT.TH1F("hSemiresolvedExcl_GenPart_H2_b1_pt", ";p_{T} [GeV];Events", 100, 0.0, 2000)
        hSemiresolvedExcl_GenPart_H2_b2_pt = ROOT.TH1F("hSemiresolvedExcl_GenPart_H2_b2_pt", ";p_{T} [GeV];Events", 100, 0.0, 2000)
        hSemiresolvedExcl_GenPart_H1_b1_eta = ROOT.TH1F("hSemiresolvedExcl_GenPart_H1_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_GenPart_H1_b2_eta = ROOT.TH1F("hSemiresolvedExcl_GenPart_H1_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_GenPart_H2_b1_eta = ROOT.TH1F("hSemiresolvedExcl_GenPart_H2_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_GenPart_H2_b2_eta = ROOT.TH1F("hSemiresolvedExcl_GenPart_H2_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_H1Boosted_H2resolved_GenFatJet_H1_pt = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_GenFatJet_H1_pt", ";p_{T} [GeV];Events", 100, 0.0, 2000)
        hSemiresolvedExcl_H1Boosted_H2resolved_GenFatJet_H1_eta = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_GenFatJet_H1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_H1Boosted_H2resolved_GenJet_H2_b1_pt = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_GenJet_H2_b1_pt", ";p_{T} [GeV];Events", 100, 0.0, 2000)
        hSemiresolvedExcl_H1Boosted_H2resolved_GenJet_H2_b2_pt = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_GenJet_H2_b2_pt", ";p_{T} [GeV];Events", 100, 0.0, 2000)
        hSemiresolvedExcl_H1Boosted_H2resolved_GenJet_H2_b1_eta = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_GenJet_H2_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_H1Boosted_H2resolved_GenJet_H2_b2_eta = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_GenJet_H2_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_pt = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_pt", ";p_{T} [GeV];Events", 100, 0.0, 2000)
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_eta = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_m = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_m", ";H_{1} mass", 150, 0, 300)
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoJet_H2_b1_pt = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_RecoJet_H2_b1_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoJet_H2_b2_pt = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_RecoJet_H2_b2_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoJet_H2_b1_btag = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_RecoJet_H2_b1_btag", ";b-discriminator;Events", 100, 0.0, 1.0)
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoJet_H2_b2_btag = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_RecoJet_H2_b2_btag", ";b-discriminator;Events", 100, 0.0,1.0)
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoJet_H2_b1_eta = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_RecoJet_H2_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoJet_H2_b2_eta = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_RecoJet_H2_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_TXbb = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_TXbb", ";T_{Xbb} score;Events", 100, 0.0, 1.0)
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_TXbb = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_TXbb", ";T_{Xbb} score;Events", 100, 0.0, 1.0)
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_mSD_Uncorrected = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_mSD_Uncorrected", ";m_{SD} [GeV];Events", 150, 0, 300) 
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_area = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_area", ";area;Events", 100, 0.0, 5.0)
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_n2b1 = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_n2b1", ";n2b1;Events", 100, 0.0, 5.0)
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_n3b1 = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_n3b1", ";n3b1;Events", 100, 0.0, 5.0)
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_tau21 = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_tau21", ";#tau_{21};Events", 100, 0.0, 2.5)
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_tau32 = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_tau32", ";#tau_{32};Events", 100, 0.0, 2.5)
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_nsubjets = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_nsubjets", ";subjet multiplicity;Events", 3, 0, 3)
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_pt = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_pt", ";subjet 1 p_{T} [GeV];Events", 100, 0.0, 1000)
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_eta = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_eta", ";subjet 1 #eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_m = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_m", ";subjet 1 M [GeV];Events", 200, 0.0, 800)
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_btag = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_btag", ";subjet 1 b-discriminator;Events", 100, 0.0, 1.0)
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_pt = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_pt", ";subjet 2 p_{T} [GeV];Events", 100, 0.0, 1000)
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_eta = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_eta", ";subjet 2 #eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_m = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_m", ";subjet 2 M [GeV];Events", 200, 0.0, 800)
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_btag = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_btag", ";subjet 2 b-discriminator;Events", 100,0.0, 1.0)
        hSemiresolvedExcl_H1Boosted_H2resolved_NJets = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_NJets", "; jets multiplicity;Events", 15, 0, 15)
        hSemiresolvedExcl_H1Boosted_H2resolved_NFatJets = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_NFatJets", ";fatjets multiplicity;Events", 10, 0, 10)
        hSemiresolvedExcl_H1Boosted_H2resolved_AK8PFHT = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_AK8PFHT", ";AK8 PF H_{T} [GeV];Events", 125, 0.0, 2500)
        hSemiresolvedExcl_H1Boosted_H2resolved_DeltaR_H1_H2 = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_DeltaR_H1_H2", ";#Delta R;Events", 100, 0.0, 5.0)
        hSemiresolvedExcl_H1Boosted_H2resolved_DeltaEta_H1_H2 = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_DeltaEta_H1_H2", ";#Delta#eta;Events", 50, 0.0, 5.0)
        hSemiresolvedExcl_H1Boosted_H2resolved_DeltaPhi_H1_H2 = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_DeltaPhi_H1_H2", ";#Delta#phi;Events", 50, 0.0,5.0)
        hSemiresolvedExcl_H1Boosted_H2resolved_InvMass_H2 = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_InvMass_H2", ";m_{H} [GeV]", 150, 0, 300)
        hSemiresolvedExcl_H1Boosted_H2resolved_InvMassRegressed_H2 = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_InvMassRegressed_H2", ";m_{H} [GeV]", 150, 0, 300)
        hSemiresolvedExcl_H1Boosted_H2resolved_H2_pt = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_H2_pt", ";p_{T} [GeV];Events", 100, 0.0, 2000)
        hSemiresolvedExcl_H1Boosted_H2resolved_H2_eta = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_H2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_H1Boosted_H2resolved_PFHT = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_PFHT", "; PF H_{T} [GeV];Events", 125, 0.0, 2500)
        hSemiresolvedExcl_H1Boosted_H2resolved_NLooseBJets = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_NLooseBJets", ";b-jets L;Events", 10, 0, 10)
        hSemiresolvedExcl_H1Boosted_H2resolved_NMediumBJets = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_NMediumBJets", ";b-jets M;Events", 10, 0, 10)
        hSemiresolvedExcl_H1Boosted_H2resolved_NTightBJets = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_NTightBJets", ";b-jets T;Events", 10, 0, 10)
        hSemiresolvedExcl_H1Boosted_H2resolved_Jet1Pt = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_Jet1Pt", ";jet 1 p_{T} [GeV];Events", 100, 0.0, 1000)
        hSemiresolvedExcl_H1Boosted_H2resolved_Jet2Pt = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_Jet2Pt", ";jet 2 p_{T} [GeV];Events", 100, 0.0, 1000)
        hSemiresolvedExcl_H1Boosted_H2resolved_Jet3Pt = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_Jet3Pt", ";jet 3 p_{T} [GeV];Events", 100, 0.0, 1000)
        hSemiresolvedExcl_H1Boosted_H2resolved_Jet4Pt = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_Jet4Pt", ";jet 4 p_{T} [GeV];Events", 100, 0.0, 1000)
        hSemiresolvedExcl_H1Boosted_H2resolved_Jet1Eta = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_Jet1Eta", ";jet 1 #eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_H1Boosted_H2resolved_Jet2Eta = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_Jet2Eta", ";jet 2 #eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_H1Boosted_H2resolved_Jet3Eta = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_Jet3Eta", ";jet 3 #eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_H1Boosted_H2resolved_Jet4Eta = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_Jet4Eta", ";jet 4 #eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_H1Boosted_H2resolved_AK8Jet1Pt = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_AK8Jet1Pt", "; fatjet 1 p_{T} [GeV];Events", 100, 0.0, 2000)
        hSemiresolvedExcl_H1Boosted_H2resolved_AK8Jet2Pt = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_AK8Jet2Pt", "; fatjet 2 p_{T} [GeV];Events", 100, 0.0, 2000)
        hSemiresolvedExcl_H1Boosted_H2resolved_AK8Jet3Pt = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_AK8Jet3Pt", "; fatjet 3 p_{T} [GeV];Events", 100, 0.0, 2000)
        hSemiresolvedExcl_H1Boosted_H2resolved_AK8Jet4Pt = ROOT.TH1F("hSemiresolvedExcl_H1Boosted_H2resolved_AK8Jet4Pt", "; fatjet 4 p_{T} [GeV];Events", 100, 0.0, 2000)
        
        # Semi-resolved regime: H2 is boosted, H1 is resolved
        hSemiresolvedExcl_H2Boosted_H1resolved_NJets = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_NJets", ";jets multiplicity;Events", 15, 0, 15)
        hSemiresolvedExcl_H2Boosted_H1resolved_NFatJets = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_NFatJets", ";fatjets multiplicity;Events", 10, 0, 10)
        hSemiresolvedExcl_H2Boosted_H1resolved_AK8PFHT = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_AK8PFHT", ";AK8 PF H_{T} [GeV];Events", 125, 0.0, 2500)
        hSemiresolvedExcl_H2Boosted_H1resolved_DeltaR_H1_H2 = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_DeltaR_H1_H2", ";#Delta R;Events", 100, 0.0, 5.0)
        hSemiresolvedExcl_H2Boosted_H1resolved_DeltaEta_H1_H2 = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_DeltaEta_H1_H2", ";#Delta#eta;Events", 50, 0.0, 5.0)
        hSemiresolvedExcl_H2Boosted_H1resolved_DeltaPhi_H1_H2 = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_DeltaPhi_H1_H2", ";#Delta#phi;Events", 50, 0.0, 5.0)
        hSemiresolvedExcl_H2Boosted_H1resolved_InvMass_H1 = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_InvMass_H1", ";m_{H} [GeV]", 150, 0, 300)
        hSemiresolvedExcl_H2Boosted_H1resolved_InvMassRegressed_H1 = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_InvMassRegressed_H1", ";m_{H} [GeV]", 150, 0, 300)
        hSemiresolvedExcl_H2Boosted_H1resolved_H1_pt = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_H1_pt", ";p_{T} [GeV];Events", 100, 0.0, 2000)
        hSemiresolvedExcl_H2Boosted_H1resolved_H1_eta = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_H1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_m = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_m", ";m_{H} [GeV]", 150, 0, 300)
        hSemiresolvedExcl_H2Boosted_H1resolved_GenFatJet_H2_pt = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_GenFatJet_H2_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hSemiresolvedExcl_H2Boosted_H1resolved_GenFatJet_H2_eta = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_GenFatJet_H2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_H2Boosted_H1resolved_GenJet_H1_b1_pt = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_GenJet_H1_b1_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hSemiresolvedExcl_H2Boosted_H1resolved_GenJet_H1_b2_pt = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_GenJet_H1_b2_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hSemiresolvedExcl_H2Boosted_H1resolved_GenJet_H1_b1_eta = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_GenJet_H1_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_H2Boosted_H1resolved_GenJet_H1_b2_eta = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_GenJet_H1_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_pt = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_eta = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoJet_H1_b1_pt = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_RecoJet_H1_b1_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoJet_H1_b2_pt = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_RecoJet_H1_b2_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoJet_H1_b1_eta = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_RecoJet_H1_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoJet_H1_b2_eta = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_RecoJet_H1_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_mSD_Uncorrected = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_mSD_Uncorrected", ";m_{SD} [GeV];Events", 150, 0, 300)
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_area = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_area", ";area;Events", 100, 0.0, 5.0)
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_n2b1 = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_n2b1", ";n2b1;Events", 100, 0.0, 5.0)
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_n3b1 = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_n3b1", ";n3b2;Events", 100, 0.0, 5.0)
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_tau21 = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_tau21", ";#tau_{21};Events", 100, 0.0, 2.5)
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_tau32 = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_tau32", ";#tau_{32};Events", 100, 0.0, 2.5)
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_nsubjets = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_nsubjets", ";subjet multiplicity;Events", 3, 0, 3)
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_pt = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_pt", ";subjet 1 p_{T} [GeV];Events", 100, 0.0, 1000)
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_eta = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_eta", ";subjet 1 #eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_m = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_m", ";subjet 1 M [GeV];Events", 100, 0.0, 1000)
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_btag = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_subjet1_btag", ";subjet 1 b-discriminator;Events", 100, 0.0, 1.0)
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_pt = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_pt", ";subjet 2 p_{T} [GeV];Events", 100, 0.0, 1000)
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_eta = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_eta", ";subjet 2 #eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_m = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_m", ";subjet 2 M [GeV];Events", 100, 0.0, 1000)
        hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_btag = ROOT.TH1F("hSemiresolvedExcl_H2Boosted_H1resolved_RecoFatJet_H2_subjet2_btag", ";subjet 2 b-discriminator;Events", 100,0.0, 1.0)
        
        
        hSemiresolvedExcl_MassCut100GeV_GenPart_H1_pt    = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_GenPart_H1_pt", ";p_{T} [GeV];Events", 100, 0.0, 2000)
        hSemiresolvedExcl_MassCut100GeV_GenPart_H2_pt    = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_GenPart_H2_pt", ";p_{T} [GeV];Events", 100, 0.0, 2000)
        hSemiresolvedExcl_MassCut100GeV_GenPart_H1_b1_pt = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_GenPart_H1_b1_pt", ";p_{T} [GeV];Events", 100, 0.0, 2000)
        hSemiresolvedExcl_MassCut100GeV_GenPart_H1_b2_pt = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_GenPart_H1_b2_pt", ";p_{T} [GeV];Events", 100, 0.0, 2000)
        hSemiresolvedExcl_MassCut100GeV_GenPart_H2_b1_pt = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_GenPart_H2_b1_pt", ";p_{T} [GeV];Events", 100, 0.0, 2000)
        hSemiresolvedExcl_MassCut100GeV_GenPart_H2_b2_pt = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_GenPart_H2_b2_pt", ";p_{T} [GeV];Events", 100, 0.0, 2000)
        hSemiresolvedExcl_MassCut100GeV_GenPart_H1_b1_eta = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_GenPart_H1_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_MassCut100GeV_GenPart_H1_b2_eta = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_GenPart_H1_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_MassCut100GeV_GenPart_H2_b1_eta = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_GenPart_H2_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_MassCut100GeV_GenPart_H2_b2_eta = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_GenPart_H2_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_GenFatJet_H1_pt = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_GenFatJet_H1_pt", ";p_{T} [GeV];Events", 100, 0.0, 2000)
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_GenFatJet_H1_eta = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_GenFatJet_H1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_GenJet_H2_b1_pt = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_GenJet_H2_b1_pt", ";p_{T} [GeV];Events", 100, 0.0, 2000)
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_GenJet_H2_b2_pt = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_GenJet_H2_b2_pt", ";p_{T} [GeV];Events", 100, 0.0, 2000)
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_GenJet_H2_b1_eta = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_GenJet_H2_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_GenJet_H2_b2_eta = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_GenJet_H2_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_pt = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_pt", ";p_{T} [GeV];Events", 100, 0.0, 2000)
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_eta = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_m = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_m", ";H_{1} mass", 150, 0, 300)
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoJet_H2_b1_pt = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoJet_H2_b1_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoJet_H2_b2_pt = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoJet_H2_b2_pt", ";p_{T} [GeV];Events", 100, 0.0, 1000)
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoJet_H2_b1_btag = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoJet_H2_b1_btag", ";b-discriminator;Events", 100, 0.0, 1.0)
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoJet_H2_b2_btag = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoJet_H2_b2_btag", ";b-discriminator;Events", 100, 0.0, 1.0)
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoJet_H2_b1_eta = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoJet_H2_b1_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoJet_H2_b2_eta = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoJet_H2_b2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_TXbb = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_TXbb", ";T_{Xbb} score;Events", 100, 0.0, 1.0)
        hSemiresolvedExcl_MassCut100GeV_H2Boosted_H1resolved_RecoFatJet_H2_TXbb = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_H2Boosted_H1resolved_RecoFatJet_H2_TXbb", ";T_{Xbb} score;Events", 100, 0.0, 1.0)
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_mSD_Uncorrected = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_mSD_Uncorrected", ";m_{SD} [GeV];Events", 150, 0, 300) 
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_area = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_area", ";area;Events", 100, 0.0, 5.0)
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_n2b1 = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_n2b1", ";n2b1;Events", 100, 0.0, 5.0)
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_n3b1 = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_n3b1", ";n3b1;Events", 100, 0.0, 5.0)
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_tau21 = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_tau21", ";#tau_{21};Events", 100, 0.0, 2.5)
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_tau32 = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_tau32", ";#tau_{32};Events", 100, 0.0, 2.5)
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_nsubjets = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_nsubjets", ";subjet multiplicity;Events", 3, 0, 3)
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_pt = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_pt", ";subjet 1 p_{T} [GeV];Events", 100, 0.0, 1000)
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_eta = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_eta", ";subjet 1 #eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_m = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_m", ";subjet 1 M [GeV];Events", 200, 0.0, 800)
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_btag = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_btag", ";subjet 1 b-discriminator;Events", 100, 0.0, 1.0)
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_pt = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_pt", ";subjet 2 p_{T} [GeV];Events", 100, 0.0, 1000)
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_eta = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_eta", ";subjet 2 #eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_m = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_m", ";subjet 2 M [GeV];Events", 200, 0.0, 800)
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_btag = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_btag", ";subjet 2 b-discriminator;Events", 100,0.0, 1.0)
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_NJets = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_NJets", "; jets multiplicity;Events", 15, 0, 15)
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_NFatJets = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_NFatJets", ";fatjets multiplicity;Events", 10, 0, 10)
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_AK8PFHT = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_AK8PFHT", ";AK8 PF H_{T} [GeV];Events", 125, 0.0, 2500)
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_DeltaR_H1_H2 = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_DeltaR_H1_H2", ";#Delta R;Events", 100, 0.0, 5.0)
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_DeltaEta_H1_H2 = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_DeltaEta_H1_H2", ";#Delta#eta;Events", 50, 0.0, 5.0)
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_DeltaPhi_H1_H2 = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_DeltaPhi_H1_H2", ";#Delta#phi;Events", 50, 0.0, 5.0)
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_InvMass_H2 = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_InvMass_H2", ";m_{H} [GeV]", 150, 0, 300)
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_InvMassRegressed_H2 = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_InvMassRegressed_H2", ";m_{H} [GeV]", 150, 0, 300)
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_H2_pt = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_H2_pt", ";p_{T} [GeV];Events", 100, 0.0, 2000)
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_H2_eta = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_H2_eta", ";#eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_PFHT = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_PFHT", "; PF H_{T} [GeV];Events", 125, 0.0, 2500)
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_NLooseBJets = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_NLooseBJets", ";b-jets L;Events", 10, 0, 10)
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_NMediumBJets = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_NMediumBJets", ";b-jets M;Events", 10, 0, 10)
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_NTightBJets = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_NTightBJets", ";b-jets T;Events", 10, 0, 10)
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_Jet1Pt = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_Jet1Pt", ";jet 1 p_{T} [GeV];Events", 100, 0.0, 1000)
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_Jet2Pt = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_Jet2Pt", ";jet 2 p_{T} [GeV];Events", 100, 0.0, 1000)
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_Jet3Pt = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_Jet3Pt", ";jet 3 p_{T} [GeV];Events", 100, 0.0, 1000)
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_Jet4Pt = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_Jet4Pt", ";jet 4 p_{T} [GeV];Events", 100, 0.0, 1000)
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_Jet1Eta = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_Jet1Eta", ";jet 1 #eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_Jet2Eta = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_Jet2Eta", ";jet 2 #eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_Jet3Eta = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_Jet3Eta", ";jet 3 #eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_Jet4Eta = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_Jet4Eta", ";jet 4 #eta;Events", 120, -4.0, 4.0)
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_AK8Jet1Pt = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_AK8Jet1Pt", "; fatjet 1 p_{T} [GeV];Events", 100, 0.0, 2000)
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_AK8Jet2Pt = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_AK8Jet2Pt", "; fatjet 2 p_{T} [GeV];Events", 100, 0.0, 2000)
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_AK8Jet3Pt = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_AK8Jet3Pt", "; fatjet 3 p_{T} [GeV];Events", 100, 0.0, 2000)
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_AK8Jet4Pt = ROOT.TH1F("hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_AK8Jet4Pt", "; fatjet 4 p_{T} [GeV];Events", 100, 0.0, 2000)
        


        
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
        cNotMatchedReco = 0.0

        print("\nProcessing sample %s" % (sample))
        print("Entries = %s" % (entries))
        for i, e in enumerate(t):
            
            #print("\n Entry = %s" % (i))
            
            # Counters
            nBQuarksMatchedToGenJets = 0
            nBQuarksMatchedToGenFatJets = 0

            nHiggsMatchedToGenJets = 0
            nHiggsMatchedToGenFatJets = 0
            
            #================================================== Gen-level matching
            
            # Check if the b-quarks are matched to gen-jets
            bH1_b1_genjet = e.gen_H1_b1_genjet_pt > 0.0
            bH1_b2_genjet = e.gen_H1_b2_genjet_pt > 0.0
            bH2_b1_genjet = e.gen_H2_b1_genjet_pt > 0.0
            bH2_b2_genjet = e.gen_H2_b2_genjet_pt > 0.0
            
            # Number of b-quarks matched to GenJets
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
            if bH1_genfatjet: nHiggsMatchedToGenFatJets +=1
            if bH2_genfatjet: nHiggsMatchedToGenFatJets +=1
            
            bH1_genjets = bH1_b1_genjet and bH1_b2_genjet
            bH2_genjets = bH2_b1_genjet and bH2_b2_genjet
            if bH1_genjets: nHiggsMatchedToGenJets += 1
            if bH2_genjets: nHiggsMatchedToGenJets += 1
            
            h2D_NHiggsMatchedTo_GenJetsVsGenFatJets.Fill(nHiggsMatchedToGenJets, nHiggsMatchedToGenFatJets)
            
            #=================================================================================================================================================================================
            bH1_isResolved = bH1_genjets
            bH2_isResolved = bH2_genjets
            
            bH1_isBoosted  = not bH1_isResolved and bH1_genfatjet
            bH2_isBoosted  = not bH2_isResolved and bH2_genfatjet
            
            #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            # At gen-level:
            # Resolved: any event matched with four gen-jets
            # Boosted: H1 is not resolved and H2 is not resolved, H1 is boosted, H2 is boosted
            # Semiresolved: not resolved, not boosted, either of the Higgs is resolved and the other is boosted
            #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            bIsResolvedGen = bH1_isResolved and bH2_isResolved
            bIsBoostedGen  = not bIsResolvedGen and bH1_isBoosted and bH2_isBoosted
            bIsSemiresolvedGen = not bIsResolvedGen and not bIsBoostedGen and ((bH1_isResolved and bH2_isBoosted) or (bH2_isResolved and bH1_isBoosted))
            
            if 0:
                if bIsResolvedGen:
                    print("\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
                    print("   Entry = %s is RESOLVED" % (i))
                    print(" H1 b1 gen-jet pt=%s,  H1 b2 gen-jet pt=%s,  H2 b1 gen-jet pt=%s,   H2 b2 gen-jet pt=%s" % (round(e.gen_H1_b1_genjet_pt,2), round(e.gen_H1_b2_genjet_pt,2), round(e.gen_H2_b1_genjet_pt, 2), round(e.gen_H2_b2_genjet_pt, 2)))
                elif bIsBoostedGen:
                    print("\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
                    print("   Entry = %s is BOOSTED" % (i))
                    print(" H1 b1 gen-jet pt=%s,  H1 b2 gen-jet pt=%s,  H2 b1 gen-jet pt=%s,   H2 b2 gen-jet pt=%s" % (round(e.gen_H1_b1_genjet_pt,2), round(e.gen_H1_b2_genjet_pt,2), round(e.gen_H2_b1_genjet_pt, 2), round(e.gen_H2_b2_genjet_pt, 2)))
                elif bIsSemiresolvedGen:
                    print("\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
                    print("   Entry = %s is semi-resolved" % (i))
                    print("H1 b1 gen-jet pt=%s,  H1 b2 gen-jet pt=%s,   |  H2 b1 gen-jet pt=%s,   H2 b2 gen-jet pt=%s  | H1 b1 fatjet pt=%s, mass=%s,   H1 b2 fatjet pt=%s, mass=%s   |   H2 b1 fatjet pt=%s,  mass=%s , H2 b2 fatjet pt=%s,  mass=%s |  H1=%s,  H2=%s" % (round(e.gen_H1_b1_genjet_pt,2), round(e.gen_H1_b2_genjet_pt,2), round(e.gen_H2_b1_genjet_pt, 2), round(e.gen_H2_b2_genjet_pt, 2), round(e.gen_H1_b1_genfatjet_pt,2), round(e.gen_H1_b1_genfatjet_m,2), round(e.gen_H1_b2_genfatjet_pt,2), round(e.gen_H1_b2_genfatjet_m,2),   round(e.gen_H2_b1_genfatjet_pt,2), round(e.gen_H2_b1_genfatjet_m,2), round(e.gen_H2_b2_genfatjet_pt,2), round(e.gen_H2_b2_genfatjet_m,2), bH1_genfatjet, bH2_genfatjet))
                else:
                    print("\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
                    print("   Entry = %s is neither resolved or boosted" % (i))
                    print("H1 b1 gen-jet pt=%s,  H1 b2 gen-jet pt=%s,   |  H2 b1 gen-jet pt=%s,   H2 b2 gen-jet pt=%s  | H1 b1 fatjet pt=%s, mass=%s,   H1 b2 fatjet pt=%s, mass=%s   |   H2 b1 fatjet pt=%s,  mass=%s , H2 b2 fatjet pt=%s,  mass=%s |  H1=%s,  H2=%s" % (round(e.gen_H1_b1_genjet_pt,2), round(e.gen_H1_b2_genjet_pt,2), round(e.gen_H2_b1_genjet_pt, 2), round(e.gen_H2_b2_genjet_pt, 2), round(e.gen_H1_b1_genfatjet_pt,2), round(e.gen_H1_b1_genfatjet_m,2), round(e.gen_H1_b2_genfatjet_pt,2), round(e.gen_H1_b2_genfatjet_m,2),   round(e.gen_H2_b1_genfatjet_pt,2), round(e.gen_H2_b1_genfatjet_m,2), round(e.gen_H2_b2_genfatjet_pt,2), round(e.gen_H2_b2_genfatjet_m,2), bH1_genfatjet, bH2_genfatjet))
                
            
            # General - if H1 is matched to a fatjet
            if bH1_genfatjet:
                h_GenFatJet_H1_pt.Fill(e.gen_H1_b1_genfatjet_pt)
            if bH2_genfatjet:
                h_GenFatJet_H2_pt.Fill(e.gen_H2_b1_genfatjet_pt)
            
            if bIsBoostedGen:
                h_IsBoostedGen_GenFatJet_H1_pt.Fill(e.gen_H1_b1_genfatjet_pt)
                h_IsBoostedGen_GenFatJet_H2_pt.Fill(e.gen_H2_b2_genfatjet_pt)
            
            if bIsSemiresolvedGen:
                if (bH1_isBoosted): h_IsSemiresolvedGen_GenFatJet_H1_pt.Fill(e.gen_H1_b1_genfatjet_pt)
                if (bH2_isBoosted): h_IsSemiresolvedGen_GenFatJet_H2_pt.Fill(e.gen_H2_b2_genfatjet_pt)
            
            #==================================================
            # Increment Gen-counters
            if (bIsSemiresolvedGen): cIsSemiResolvedGen += 1
            if (bIsBoostedGen):      cIsBoostedGen += 1
            if (bIsResolvedGen):     cIsResolvedGen += 1
            #==================================================
            
            
            #================================================================================================================================================================ Reco-level matching
            # RECO matching
            #================================================================================================================================================================ Reco-level matching
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
            nHiggsMatchedToRecoFatJets = 0
            if bH1_recofatjet: nHiggsMatchedToRecoFatJets += 1
            if bH2_recofatjet: nHiggsMatchedToRecoFatJets += 1
            
            bH1_recojets = bH1_b1_recojet and bH1_b2_recojet
            bH2_recojets = bH2_b1_recojet and bH2_b2_recojet
            nHiggsMatchedToRecoJets = 0
            if bH1_recojets: nHiggsMatchedToRecoJets += 1
            if bH2_recojets:  nHiggsMatchedToRecoJets +=1
            
            h2D_NHiggsMatchedTo_RecoJetsVsRecoFatJets.Fill(nHiggsMatchedToRecoJets, nHiggsMatchedToRecoFatJets)
            
            # Get same fatjet combinations
            b_b11_b12_sameRecoFatjet = bH1_b1_recofatjet and bH1_b2_recofatjet and areSameJets(e.gen_H1_b1_recofatjet_eta, e.gen_H1_b2_recofatjet_eta, e.gen_H1_b1_recofatjet_phi, e.gen_H1_b2_recofatjet_phi)
            b_b11_b21_sameRecoFatjet = bH1_b1_recofatjet and bH2_b1_recofatjet and areSameJets(e.gen_H1_b1_recofatjet_eta, e.gen_H2_b1_recofatjet_eta, e.gen_H1_b1_recofatjet_phi, e.gen_H2_b1_recofatjet_phi)
            b_b11_b22_sameRecoFatjet = bH1_b1_recofatjet and bH2_b2_recofatjet and areSameJets(e.gen_H1_b1_recofatjet_eta, e.gen_H2_b2_recofatjet_eta, e.gen_H1_b1_recofatjet_phi, e.gen_H2_b2_recofatjet_phi)
            b_b12_b21_sameRecoFatjet = bH1_b2_recofatjet and bH2_b1_recofatjet and areSameJets(e.gen_H1_b2_recofatjet_eta, e.gen_H2_b1_recofatjet_eta, e.gen_H1_b2_recofatjet_phi, e.gen_H2_b1_recofatjet_phi)
            b_b12_b22_sameRecoFatjet = bH1_b2_recofatjet and bH2_b2_recofatjet and areSameJets(e.gen_H1_b2_recofatjet_eta, e.gen_H2_b2_recofatjet_eta, e.gen_H1_b2_recofatjet_phi, e.gen_H2_b2_recofatjet_phi)
            b_b21_b22_sameRecoFatjet = bH2_b1_recofatjet and bH2_b2_recofatjet and areSameJets(e.gen_H2_b1_recofatjet_eta, e.gen_H2_b2_recofatjet_eta, e.gen_H2_b1_recofatjet_phi, e.gen_H2_b2_recofatjet_phi)
                        

            #==============
            bH1_isResolved = bH1_recojets
            bH2_isResolved = bH2_recojets
            
            bH1_isBoosted = not bH1_isResolved and bH1_recofatjet
            bH2_isBoosted = not bH2_isResolved and bH2_recofatjet
            #==============
            
            # Define exclusive regions:
            bIsResolvedReco     = bH1_isResolved and bH2_isResolved
            bIsBoostedReco      = not bIsResolvedReco and bH1_isBoosted and bH2_isBoosted
            bIsSemiresolvedReco = not bIsResolvedReco and not bIsBoostedReco and ((bH1_isResolved and bH2_isBoosted) or (bH2_isResolved and bH1_isBoosted))
            
            bH1Boosted_H2resolved_reco = bIsSemiresolvedReco and bH1_isBoosted and bH2_isResolved
            bH2Boosted_H1resolved_reco = bIsSemiresolvedReco and bH2_isBoosted and bH1_isResolved
            
            if (bIsResolvedReco): cIsResolvedReco += 1
            if (bIsSemiresolvedReco): cIsSemiResolvedReco += 1
            if (bIsBoostedReco): cIsBoostedReco += 1
            
            bIsResolvedRecoCases = {}
            for c in range(1, 15):
                bIsResolvedRecoCases[str(c)] = False
            
            if bIsResolvedReco:
                
                if (nBQuarksMatchedToRecoFatJets == 4):
                    if bH1_recofatjet and bH2_recofatjet:
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


    
            if not bIsBoostedReco:
                if bIsBoostedGen:
                    h_IsBoostedGen_NotBoostedReco_GenFatJet_H1_pt.Fill(e.gen_H1_b1_genfatjet_pt)
                    h_IsBoostedGen_NotBoostedReco_GenFatJet_H2_pt.Fill(e.gen_H2_b1_genfatjet_pt)

            if not bIsSemiresolvedReco:
                if bIsSemiresolvedGen:
                    if (e.gen_H1_b1_genfatjet_pt > 0): h_IsSemiresolvedGen_NotSemiresolvedReco_GenFatJet_H1_pt.Fill(e.gen_H1_b1_genfatjet_pt)
                    if (e.gen_H2_b1_genfatjet_pt > 0): h_IsSemiresolvedGen_NotSemiresolvedReco_GenFatJet_H2_pt.Fill(e.gen_H2_b1_genfatjet_pt)

            
            #====================================================================================================================
            # All events
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
            if not (bIsResolvedReco or bIsSemiresolvedReco or bIsBoostedReco):
                cNotMatchedReco += 1
                continue

            if bIsResolvedReco:
                # Trigger plots
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

                AK8PFHT = 0.0
                for ij in range(0, e.n_fatjet):
                    pt = e.fatjet_pt.at(ij)
                    AK8PFHT += pt
                hResolved_RecoJet_AK8PFHT.Fill(AK8PFHT)
                                
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
            elif bIsBoostedReco:
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
                if (e.n_jet > 0): hBoostedExcl_Jet1Pt.Fill(e.jet_pt.at(0))
                if (e.n_jet > 1): hBoostedExcl_Jet2Pt.Fill(e.jet_pt.at(1))
                if (e.n_jet > 2): hBoostedExcl_Jet3Pt.Fill(e.jet_pt.at(2))
                if (e.n_jet > 3): hBoostedExcl_Jet4Pt.Fill(e.jet_pt.at(3))

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

                hBoostedExcl_AK4PFHT.Fill(reco_PFHT)
                hBoostedExcl_RecoJet_NLooseBJets.Fill(nLoose)
                hBoostedExcl_RecoJet_NMediumBJets.Fill(nMedium)
                hBoostedExcl_RecoJet_NTightBJets.Fill(nTight)
                
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
                hBoostedExcl_AK8Jet1Pt.Fill(e.fatjet_pt.at(0))
                hBoostedExcl_AK8Jet2Pt.Fill(e.fatjet_pt.at(1))
                if (e.n_fatjet > 2): hBoostedExcl_AK8Jet3Pt.Fill(e.fatjet_pt.at(2))
                if (e.n_fatjet > 3): hBoostedExcl_AK8Jet4Pt.Fill(e.fatjet_pt.at(3))

            elif bIsSemiresolvedReco:
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
                
                # Other plots
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
                            hSemiresolvedExcl_H1Boosted_H2resolved_RecoJet_H2_b1_btag.Fill(btag)
                        elif (areSameJets(eta, e.gen_H2_b2_recojet_eta, phi, e.gen_H2_b2_recojet_phi)):
                            bFound_reco_H2_b2 = True
                            hSemiresolvedExcl_H1Boosted_H2resolved_RecoJet_H2_b2_btag.Fill(btag)
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
                    
                    if (e.n_fatjet > 0): hSemiresolvedExcl_H1Boosted_H2resolved_AK8Jet1Pt.Fill(e.fatjet_pt.at(0))
                    if (e.n_fatjet > 1): hSemiresolvedExcl_H1Boosted_H2resolved_AK8Jet2Pt.Fill(e.fatjet_pt.at(1))
                    if (e.n_fatjet > 2): hSemiresolvedExcl_H1Boosted_H2resolved_AK8Jet3Pt.Fill(e.fatjet_pt.at(2))
                    if (e.n_fatjet > 3): hSemiresolvedExcl_H1Boosted_H2resolved_AK8Jet4Pt.Fill(e.fatjet_pt.at(3))
                    
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
                            #print("H1 Mass=", mass, "    mSD=", e.fatjet_mSD_UnCorrected.at(ij))
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
                    
                    if (e.gen_H1_b1_recofatjet_m > 100):

                        #print("H1 mass = ", e.gen_H1_b1_recofatjet_m)
                        # Other plots
                        hSemiresolvedExcl_MassCut100GeV_GenPart_H1_pt.Fill(e.gen_H1_pt)
                        hSemiresolvedExcl_MassCut100GeV_GenPart_H2_pt.Fill(e.gen_H2_pt)
                        hSemiresolvedExcl_MassCut100GeV_GenPart_H1_b1_pt.Fill(e.gen_H1_b1_pt)
                        hSemiresolvedExcl_MassCut100GeV_GenPart_H1_b2_pt.Fill(e.gen_H1_b2_pt)
                        hSemiresolvedExcl_MassCut100GeV_GenPart_H2_b1_pt.Fill(e.gen_H2_b1_pt)
                        hSemiresolvedExcl_MassCut100GeV_GenPart_H2_b2_pt.Fill(e.gen_H2_b2_pt)
                        hSemiresolvedExcl_MassCut100GeV_GenPart_H1_b1_eta.Fill(e.gen_H1_b1_eta)
                        hSemiresolvedExcl_MassCut100GeV_GenPart_H1_b2_eta.Fill(e.gen_H1_b2_eta)
                        hSemiresolvedExcl_MassCut100GeV_GenPart_H2_b1_eta.Fill(e.gen_H2_b1_eta)
                        hSemiresolvedExcl_MassCut100GeV_GenPart_H2_b2_eta.Fill(e.gen_H2_b2_eta)
                        
                        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_GenFatJet_H1_pt.Fill(e.gen_H1_b1_genfatjet_pt)
                        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_GenFatJet_H1_eta.Fill(e.gen_H1_b1_genfatjet_eta)
                        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_GenJet_H2_b1_pt.Fill(e.gen_H2_b1_genjet_pt)
                        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_GenJet_H2_b2_pt.Fill(e.gen_H2_b2_genjet_pt)
                        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_GenJet_H2_b1_eta.Fill(e.gen_H2_b1_genjet_eta)
                        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_GenJet_H2_b2_eta.Fill(e.gen_H2_b2_genjet_eta)
                        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_pt.Fill(e.gen_H1_b1_recofatjet_pt)
                        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_eta.Fill(e.gen_H1_b1_recofatjet_eta)
                        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoJet_H2_b1_pt.Fill(e.gen_H2_b1_recojet_pt)
                        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoJet_H2_b2_pt.Fill(e.gen_H2_b2_recojet_pt)
                        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoJet_H2_b1_eta.Fill(e.gen_H2_b1_recojet_eta)
                        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoJet_H2_b2_eta.Fill(e.gen_H2_b2_recojet_eta)
                        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_NJets.Fill(e.n_jet)
                        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_NFatJets.Fill(e.n_fatjet)
                        reco_H2_b1_p4 = getP4(e.gen_H2_b1_recojet_pt, e.gen_H2_b1_recojet_eta, e.gen_H2_b1_recojet_phi, e.gen_H2_b1_recojet_m)
                        reco_H2_b2_p4 = getP4(e.gen_H2_b2_recojet_pt, e.gen_H2_b2_recojet_eta, e.gen_H2_b2_recojet_phi, e.gen_H2_b2_recojet_m)
                        reco_H2 = reco_H2_b1_p4 + reco_H2_b2_p4
                        
                        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_H2_pt.Fill(reco_H2.Pt())
                        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_H2_eta.Fill(reco_H2.Eta())
                        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_InvMass_H2.Fill(reco_H2.M())
                        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_DeltaR_H1_H2.Fill(deltaR(e.gen_H1_b1_recofatjet_eta, reco_H2.Eta(), e.gen_H1_b1_recofatjet_phi, reco_H2.Phi()))
                        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_DeltaEta_H1_H2.Fill(abs(e.gen_H1_b1_recofatjet_eta - reco_H2.Eta()))
                        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_DeltaPhi_H1_H2.Fill(deltaPhi(e.gen_H1_b1_recofatjet_phi, reco_H2.Phi()))
                        
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
                                hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoJet_H2_b1_btag.Fill(btag)
                            elif (areSameJets(eta, e.gen_H2_b2_recojet_eta, phi, e.gen_H2_b2_recojet_phi)):
                                bFound_reco_H2_b2 = True
                                reco_H2_b2_p4Regressed = getP4(e.jet_ptRegressed.at(ij), e.jet_eta.at(ij), e.jet_phi.at(ij), e.jet_mRegressed.at(ij))
                                hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoJet_H2_b2_btag.Fill(btag)
                                
                        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_PFHT.Fill(reco_PFHT)
                        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_NLooseBJets.Fill(nLoose)
                        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_NMediumBJets.Fill(nMedium)
                        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_NTightBJets.Fill(nTight)
                        if (e.n_jet > 0): hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_Jet1Pt.Fill(e.jet_pt.at(0))
                        if (e.n_jet > 1): hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_Jet2Pt.Fill(e.jet_pt.at(1))
                        if (e.n_jet > 2): hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_Jet3Pt.Fill(e.jet_pt.at(2))
                        if (e.n_jet > 3): hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_Jet4Pt.Fill(e.jet_pt.at(3))
                        if (e.n_jet > 0): hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_Jet1Eta.Fill(e.jet_eta.at(0))
                        if (e.n_jet > 1): hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_Jet2Eta.Fill(e.jet_eta.at(1))
                        if (e.n_jet > 2): hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_Jet3Eta.Fill(e.jet_eta.at(2))
                        if (e.n_jet > 3): hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_Jet4Eta.Fill(e.jet_eta.at(3))
                        
                        if (e.n_fatjet > 0): hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_AK8Jet1Pt.Fill(e.fatjet_pt.at(0))
                        if (e.n_fatjet > 1): hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_AK8Jet2Pt.Fill(e.fatjet_pt.at(1))
                        if (e.n_fatjet > 2): hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_AK8Jet3Pt.Fill(e.fatjet_pt.at(2))
                        if (e.n_fatjet > 3): hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_AK8Jet4Pt.Fill(e.fatjet_pt.at(3))
                        
                        if bFound_reco_H2_b1 and bFound_reco_H2_b2:
                            reco_H2_p4Regressed = reco_H2_b1_p4Regressed + reco_H2_b2_p4Regressed
                            hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_InvMassRegressed_H2.Fill(reco_H2_p4Regressed.M())
                            
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
                                hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_m.Fill(mass)
                                hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_TXbb.Fill(TXbb)
                                hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_mSD_Uncorrected.Fill(e.fatjet_mSD_UnCorrected.at(ij))
                                hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_area.Fill(e.fatjet_area.at(ij))
                                hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_n2b1.Fill(e.fatjet_n2b1.at(ij))
                                hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_n3b1.Fill(e.fatjet_n3b1.at(ij))
                                hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_tau21.Fill(e.fatjet_tau2.at(ij)/e.fatjet_tau1.at(ij))
                                hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_tau32.Fill(e.fatjet_tau3.at(ij)/e.fatjet_tau2.at(ij))
                                hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_nsubjets.Fill(e.fatjet_nsubjets.at(ij))
                                if (e.fatjet_nsubjets.at(ij) > 0):
                                    hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_pt.Fill(e.fatjet_subjet1_pt.at(ij))
                                    hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_eta.Fill(e.fatjet_subjet1_eta.at(ij))
                                    hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_m.Fill(e.fatjet_subjet1_m.at(ij))
                                    hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_btag.Fill(e.fatjet_subjet1_btagDeepB.at(ij))
                                if (e.fatjet_nsubjets.at(ij) > 1):
                                    hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_pt.Fill(e.fatjet_subjet2_pt.at(ij))
                                    hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_eta.Fill(e.fatjet_subjet2_eta.at(ij))
                                    hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_m.Fill(e.fatjet_subjet2_m.at(ij))
                                    hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_btag.Fill(e.fatjet_subjet2_btagDeepB.at(ij))
                        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_AK8PFHT.Fill(AK8PFHT)


                #%%%%%%%% H2 is boosted, H2 is resolved
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
        h2D_NHiggsMatchedTo_GenJetsVsGenFatJets.Write()
        
        h2D_NBQuarksMatchedTo_RecoJetsVsRecoFatJets.Write()
        h2D_NHiggsMatchedTo_RecoJetsVsRecoFatJets.Write()
        
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
        hResolved_RecoJet_AK8PFHT.Write()
        
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
        hBoostedExcl_AK4PFHT.Write()
        hBoostedExcl_AK8Jet1Pt.Write()
        hBoostedExcl_AK8Jet2Pt.Write()
        hBoostedExcl_AK8Jet3Pt.Write()
        hBoostedExcl_AK8Jet4Pt.Write()
        hBoostedExcl_Jet1Pt.Write()
        hBoostedExcl_Jet2Pt.Write()
        hBoostedExcl_Jet3Pt.Write()
        hBoostedExcl_Jet4Pt.Write()
        
        hBoostedExcl_RecoJet_NLooseBJets.Write()
        hBoostedExcl_RecoJet_NMediumBJets.Write()
        hBoostedExcl_RecoJet_NTightBJets.Write()
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
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoJet_H2_b1_btag.Write()
        hSemiresolvedExcl_H1Boosted_H2resolved_RecoJet_H2_b2_btag.Write()
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
        hSemiresolvedExcl_H1Boosted_H2resolved_AK8Jet2Pt.Write()
        hSemiresolvedExcl_H1Boosted_H2resolved_AK8Jet3Pt.Write()
        hSemiresolvedExcl_H1Boosted_H2resolved_AK8Jet4Pt.Write()

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


        
        hSemiresolvedExcl_MassCut100GeV_GenPart_H1_pt.Write()
        hSemiresolvedExcl_MassCut100GeV_GenPart_H2_pt.Write()
        hSemiresolvedExcl_MassCut100GeV_GenPart_H1_b1_pt.Write()
        hSemiresolvedExcl_MassCut100GeV_GenPart_H1_b2_pt.Write()
        hSemiresolvedExcl_MassCut100GeV_GenPart_H2_b1_pt.Write()
        hSemiresolvedExcl_MassCut100GeV_GenPart_H2_b2_pt.Write()
        hSemiresolvedExcl_MassCut100GeV_GenPart_H1_b1_eta.Write()
        hSemiresolvedExcl_MassCut100GeV_GenPart_H1_b2_eta.Write()
        hSemiresolvedExcl_MassCut100GeV_GenPart_H2_b1_eta.Write()
        hSemiresolvedExcl_MassCut100GeV_GenPart_H2_b2_eta.Write()
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_GenFatJet_H1_pt.Write()
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_GenFatJet_H1_eta.Write()
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_GenJet_H2_b1_pt.Write()
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_GenJet_H2_b2_pt.Write()
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_GenJet_H2_b1_eta.Write()
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_GenJet_H2_b2_eta.Write()
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_pt.Write()
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_eta.Write()
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoJet_H2_b1_pt.Write()
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoJet_H2_b2_pt.Write()
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoJet_H2_b1_eta.Write()
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoJet_H2_b2_eta.Write()
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoJet_H2_b1_btag.Write()
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoJet_H2_b2_btag.Write()
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_mSD_Uncorrected.Write()
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_area.Write()
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_n2b1.Write()
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_n3b1.Write()
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_tau21.Write()
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_tau32.Write()
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_nsubjets.Write()
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_pt.Write()
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_eta.Write()
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_m.Write()
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_subjet1_btag.Write()
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_pt.Write()
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_eta.Write()
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_m.Write()
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_subjet2_btag.Write()
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_AK8PFHT.Write()
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_TXbb.Write()
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_NJets.Write()
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_NFatJets.Write()
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_DeltaR_H1_H2.Write()
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_DeltaEta_H1_H2.Write()
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_DeltaPhi_H1_H2.Write()
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_InvMass_H2.Write()
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_InvMassRegressed_H2.Write()
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_H2_pt.Write()
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_H2_eta.Write()
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_RecoFatJet_H1_m.Write()
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_PFHT.Write()
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_NLooseBJets.Write()
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_NMediumBJets.Write()
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_NTightBJets.Write()
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_Jet1Pt.Write()
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_Jet2Pt.Write()
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_Jet3Pt.Write()
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_Jet4Pt.Write()
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_Jet1Eta.Write()
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_Jet2Eta.Write()
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_Jet3Eta.Write()
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_Jet4Eta.Write()
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_AK8Jet1Pt.Write()
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_AK8Jet2Pt.Write()
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_AK8Jet3Pt.Write()
        hSemiresolvedExcl_MassCut100GeV_H1Boosted_H2resolved_AK8Jet4Pt.Write()


                
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        # Printout statements
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        print("\nAll events %s" % (entries))
        print("Gen Resolved events %s" % (cIsResolvedGen))
        print("Gen Semi-Resolved events %s" % (cIsSemiResolvedGen))
        print("Gen Boosted events %s" % (cIsBoostedGen))
        print("\n")
        print("Reco Resolved events      = %s" % (cIsResolvedReco))
        print("Reco Semi-Resolved events = %s" % (cIsSemiResolvedReco))
        print("Reco Boosted events       = %s" % (cIsBoostedReco))
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

#!/usr/bin/env python
'''
DESCRIPTION:

PREREQUISITES:

 Run getTriggerEfficiencyByFilter.py first


LAST USED:
./plotTriggerEfficiencyByFilter.py --rfile ../data/trigger/2018/TriggerEfficiency_BeforeFit_2018_wMatching.root --year 2018
./plotTriggerEfficiencyByFilter.py --rfile ../data/trigger/2017/TriggerEfficiency_BeforeFit_2017_wMatching.root --year 2017
./plotTriggerEfficiencyByFilter.py --rfile TriggerEfficiencyByFilter_2022.root --year 2022
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
    x1 = 0.50
    x2 = 0.85
    
    y1 = 0.15
    y2 = 0.30
        
    legend = ROOT.TLegend(x1, y1, x2, y2)
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
    
    if args.year == "2022":
        for hOther in others:
            hOther.SetLineColor(ROOT.kBlue)
            hOther.SetMarkerColor(ROOT.kBlue)
            hOther.Draw("same")
            legend.AddEntry(hOther, "2018 (59.74 fb^{-1})")
    else:
        for hOther in others:
            hOther.Draw("same")
            if "TTbar" in hOther.GetName():
                legend.AddEntry(hOther, "t#bar{t}")
            elif "NMSSM" in hOther.GetName():
                legend.AddEntry(hOther, "NMSSM X#rightarrow YH#rightarrow H,HH #rightarrow 6b")
    
    legend.AddEntry(hRef, "2022 (30.57 fb^{-1})")
    legend.Draw("same")
    
    tex_cms = AddCMSText(setx=0.20, sety=0.91)
    tex_cms.Draw("same")

    tex_prelim = AddPreliminaryText(setx=0.21, sety=0.91)
    tex_prelim.Draw("same")

    header = ROOT.TLatex()
    header.SetTextSize(0.04)
    if (0):
        if args.year == "2022":
            header.DrawLatexNDC(0.62, 0.91, "30.57 fb^{-1} (13.6 TeV)")
        elif args.year == "2018":
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

def main(args):
    
    f = ROOT.TFile.Open(args.rfile, "READ")
    
    f17 = ROOT.TFile.Open("../data/trigger/2017/TriggerEfficiency_BeforeFit_2017_wMatching.root", "READ")
    f18 = ROOT.TFile.Open("../data/trigger/2018/TriggerEfficiency_BeforeFit_2018_wMatching.root", "READ")
    
    Filters = {}
    Filters["2018"] = ["L1filterHT",
                       "QuadCentralJet30",
                       "CaloQuadJet30HT320",
                       "BTagCaloDeepCSVp17Double",
                       "PFCentralJetLooseIDQuad30",
                       "1PFCentralJetLooseID75",
                       "2PFCentralJetLooseID60",
                       "3PFCentralJetLooseID45",
                       "4PFCentralJetLooseID40",
                       "PFCentralJetsLooseIDQuad30HT330",
                       "BTagPFDeepCSV4p5Triple"]
    
    Filters["2022"] = ["L1filterHT",
                       "QuadCentralJet30",
                       "CaloQuadJet30HT320",
                       "BTagCaloDeepCSVp17Double",
                       "PFCentralJetLooseIDQuad30",
                       "1PFCentralJetLooseID75",
                       "2PFCentralJetLooseID60",
                       "3PFCentralJetLooseID45",
                       "4PFCentralJetLooseID40",
                       "PFCentralJetsLooseIDQuad30HT330",
                       "BTagPFDeepJet4p5Triple"]
    
    Filters["2017"] = ["L1filterHT",
                       "QuadCentralJet30",
                       "CaloQuadJet30HT300",
                       "BTagCaloCSVp05Double",
                       "PFCentralJetLooseIDQuad30",
                       "1PFCentralJetLooseID75",
                       "2PFCentralJetLooseID60",
                       "3PFCentralJetLooseID45",
                       "4PFCentralJetLooseID40",
                       "PFCentralJetsLooseIDQuad30HT300",
                       "BTagPFCSVp070Triple"]
    
    for filt in Filters[args.year]:
        hData_Eff   = f.Get("SingleMuon__Efficiency_%s" % (filt))
        hTT_Eff     = f.Get("TTbar__Efficiency_%s" %(filt))
        hSignal_Eff = f.Get("NMSSM__Efficiency_%s" %(filt))
        
        if filt == "BTagPFDeepJet4p5Triple":
            hData18_Eff = f18.Get("SingleMuon__Efficiency_%s" % ("BTagPFDeepCSV4p5Triple"))
        else:
            hData18_Eff = f18.Get("SingleMuon__Efficiency_%s" % (filt))

        if args.year == "2022":
            plotComparison("Efficiency_%s" % (filt), hData_Eff, [hData18_Eff])
        elif args.year == "2018":
            plotComparison("Efficiency_%s" % (filt), hData_Eff, [hTT_Eff, hSignal_Eff])
        elif args.year == "2017":
            plotComparison("Efficiency_%s" % (filt), hData_Eff, [hTT_Eff])
        else:
            pass

    return


if __name__ == "__main__":

    # Default values
    VERBOSE       = True
    YEAR          = "2018"
    TRGROOTFILE   = "TriggerEfficiencies_2018.root"
    REDIRECTOR    = "root://cmseos.fnal.gov/"
    FORMATS       = [".png", ".pdf", ".C"]
    SAVEPATH      = getPublicPath()
    STUDY         = "TriggerEfficiencies_wTrgMatching"
    
    parser = ArgumentParser(description="Derive the trigger scale factors")
    parser.add_argument("-v", "--verbose", dest="verbose", default=VERBOSE, action="store_true", help="Verbose mode for debugging purposes [default: %s]" % (VERBOSE))
    parser.add_argument("--rfile", dest="rfile", type=str, action="store", default=TRGROOTFILE, help="ROOT file containint the per-filter efficiencies [default: %s]" % (TRGROOTFILE))
    parser.add_argument("--year", dest="year", action="store", default=YEAR, help="Process year")
    parser.add_argument("--formats", dest="formats", default=FORMATS, action="store", help="Formats to save histograms")
    
    args = parser.parse_args()
    args.path = os.path.join(SAVEPATH, "%s_%s_%s" % (STUDY, args.year, datetime.datetime.now().strftime('%d_%b_%Y')))
    if not os.path.exists(args.path):
        os.makedirs(args.path)

    main(args)

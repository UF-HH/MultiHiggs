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

import array
import ctypes

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
    labels["TTTo2L2Nu"] = "t#bar{t}"
    labels["TTJets"] = "t#bar{t}+jets"
    labels["NMSSM_XYH_YToHH_6b_MX_450_MY_300"] = "M_{X} = 400, M_{Y} = 300 GeV"
    labels["NMSSM_XYH_YToHH_6b_MX_500_MY_300"] = "M_{X} = 500, M_{Y} = 300 GeV"
    labels["NMSSM_XYH_YToHH_6b_MX_600_MY_300"] = "M_{X} = 600, M_{Y} = 300 GeV"
    labels["NMSSM_XYH_YToHH_6b_MX_600_MY_400"] = "M_{X} = 600, M_{Y} = 400 GeV"
    labels["NMSSM_XYH_YToHH_6b_MX_700_MY_300"] = "M_{X} = 700, M_{Y} = 300 GeV"
    labels["NMSSM_XYH_YToHH_6b_MX_700_MY_400"] = "M_{X} = 700, M_{Y} = 400 GeV"
    labels["NMSSM_XYH_YToHH_6b_MX_700_MY_500"] = "M_{X} = 700, M_{Y} = 500 GeV"
    labels["NMSSM_XYH_YToHH_6b_MX_800_MY_300"] = "M_{X} = 800, M_{Y} = 300 GeV"
    labels["NMSSM_XYH_YToHH_6b_MX_800_MY_400"] = "M_{X} = 800, M_{Y} = 400 GeV"
    labels["NMSSM_XYH_YToHH_6b_MX_800_MY_500"] = "M_{X} = 800, M_{Y} = 500 GeV"
    labels["NMSSM_XYH_YToHH_6b_MX_800_MY_600"] = "M_{X} = 800, M_{Y} = 600 GeV"
    labels["NMSSM_XYH_YToHH_6b_MX_900_MY_300"] = "M_{X} = 900, M_{Y} = 300 GeV"
    labels["NMSSM_XYH_YToHH_6b_MX_900_MY_400"] = "M_{X} = 900, M_{Y} = 400 GeV"
    labels["NMSSM_XYH_YToHH_6b_MX_900_MY_500"] = "M_{X} = 900, M_{Y} = 500 GeV"
    labels["NMSSM_XYH_YToHH_6b_MX_900_MY_600"] = "M_{X} = 900, M_{Y} = 600 GeV"
    labels["NMSSM_XYH_YToHH_6b_MX_900_MY_700"] = "M_{X} = 900, M_{Y} = 700 GeV"
    labels["NMSSM_XYH_YToHH_6b_MX_1000_MY_300"] = "M_{X} = 1000, M_{Y} = 300 GeV"
    labels["NMSSM_XYH_YToHH_6b_MX_1000_MY_400"] = "M_{X} = 1000, M_{Y} = 400 GeV"
    labels["NMSSM_XYH_YToHH_6b_MX_1000_MY_500"] = "M_{X} = 1000, M_{Y} = 500 GeV"
    labels["NMSSM_XYH_YToHH_6b_MX_1000_MY_600"] = "M_{X} = 1000, M_{Y} = 600 GeV"
    labels["NMSSM_XYH_YToHH_6b_MX_1000_MY_700"] = "M_{X} = 1000, M_{Y} = 700 GeV"
    labels["NMSSM_XYH_YToHH_6b_MX_1000_MY_800"] = "M_{X} = 1000, M_{Y} = 800 GeV"
    labels["NMSSM_XYH_YToHH_6b_MX_1100_MY_300"] = "M_{X} = 1100, M_{Y} = 300 GeV"
    labels["NMSSM_XYH_YToHH_6b_MX_1100_MY_400"] = "M_{X} = 1100, M_{Y} = 400 GeV"
    labels["NMSSM_XYH_YToHH_6b_MX_1100_MY_500"] = "M_{X} = 1100, M_{Y} = 500 GeV"
    labels["NMSSM_XYH_YToHH_6b_MX_1100_MY_600"] = "M_{X} = 1100, M_{Y} = 600 GeV"
    labels["NMSSM_XYH_YToHH_6b_MX_1100_MY_700"] = "M_{X} = 1100, M_{Y} = 700 GeV"
    labels["NMSSM_XYH_YToHH_6b_MX_1100_MY_800"] = "M_{X} = 1100, M_{Y} = 800 GeV"
    labels["NMSSM_XYH_YToHH_6b_MX_1100_MY_900"] = "M_{X} = 1100, M_{Y} = 900 GeV"
    labels["NMSSM_XYH_YToHH_6b_MX_1200_MY_300"] = "M_{X} = 1200, M_{Y} = 300 GeV"
    labels["NMSSM_XYH_YToHH_6b_MX_1200_MY_400"] = "M_{X} = 1200, M_{Y} = 400 GeV"
    labels["NMSSM_XYH_YToHH_6b_MX_1200_MY_500"] = "M_{X} = 1200, M_{Y} = 500 GeV"
    labels["NMSSM_XYH_YToHH_6b_MX_1200_MY_600"] = "M_{X} = 1200, M_{Y} = 600 GeV"
    labels["NMSSM_XYH_YToHH_6b_MX_1200_MY_700"] = "M_{X} = 1200, M_{Y} = 700 GeV"
    labels["NMSSM_XYH_YToHH_6b_MX_1200_MY_800"] = "M_{X} = 1200, M_{Y} = 800 GeV"
    labels["NMSSM_XYH_YToHH_6b_MX_1200_MY_900"] = "M_{X} = 1200, M_{Y} = 900 GeV"
    return labels[sample]

def GetOpts(hname):
    opts = {"xlabel" : "", "xmin": 0.0, "xmax": 2000.0, "ymaxfactor": 1.50}
    if "triggerScaleFactor" in hname:
        opts["xlabel"] = "trigger SF"
        opts["xmin"]   = 0.0
        opts["xmax"]   = 2.0
    elif "triggerDataEfficiency" in hname:
        opts["xlabel"] = "trigger efficiency"
        opts["xmin"] = 0.0
        opts["xmax"] = 1.0
    else:
        pass
    return opts

def AddPreliminaryText():
    # Setting up preliminary text
    tex = ROOT.TLatex(0.,0., 'Simulation Preliminary');
    tex.SetNDC();
    tex.SetX(0.21);
    tex.SetY(0.935);
    tex.SetTextFont(53);
    tex.SetTextSize(28);
    tex.SetLineWidth(2)
    return tex

def AddCMSText():
    # Settign up cms text
    texcms = ROOT.TLatex(0.,0., 'CMS');
    texcms.SetNDC();
    texcms.SetTextAlign(31);
    texcms.SetX(0.20);
    texcms.SetY(0.935);
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
        if (isFolder):
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

    fTrg = ROOT.TFile.Open("histogramsForTrgValidation_WithTrgMatching_19Dec2022_AllSelections.root", "READ")
    fNoTrg = ROOT.TFile.Open("histogramsForTrgValidation_NoTrg_19Dec2022_AllSelections.root", "READ")
    
    if not args.verbose:
        ROOT.gErrorIgnoreLevel = ROOT.kWarning
    
    samples, selections = PrintSummary()

    opts = GetOpts("triggerScaleFactor")
    variables = ["X_m", "H1_m", "HX_m", "H2_m"]
    
    for sample in samples:
        
        print("\n====== Sample %s" % (sample))
        for j, sel in enumerate(selections):
            
            for var in variables:
                
                # Create a canvas
                ROOT.gStyle.SetOptStat(0)
                ROOT.gStyle.SetTextFont(42)
                
                d = ROOT.TCanvas("", "", 800, 700)
                d.SetLeftMargin(0.15)
                
                pad1 = ROOT.TPad("pad1", "pad1", 0, 0.35, 1, 1.0)
                pad1.SetLeftMargin(0.12)
                pad1.SetBottomMargin(0)
                pad1.SetGridx()
                pad1.Draw()
                pad1.cd()
                
                legend = ROOT.TLegend(0.60, 0.70, 0.85, 0.88)
                legend.SetHeader(GetLabel(sample))
                legend.SetFillColor(0)
                legend.SetFillStyle(0)
                legend.SetBorderSize(0)
                legend.SetTextSize(0.04)
                
                hTrg   = fTrg.Get("/".join([sample, sel, var]))
                opts["ymax"] = opts["ymaxfactor"] * hTrg.GetMaximum()            
                hTrg.SetMaximum(opts["ymax"])
                
                hNoTrg = fNoTrg.Get("/".join([sample, sel, var+"_scaled"])) 
                hNoTrg.SetMaximum(opts["ymax"])
                
                hNoTrgUp   = fNoTrg.Get("/".join([sample, sel, var+"_scaledUp"]))
                hNoTrgDown = fNoTrg.Get("/".join([sample, sel, var+"_scaledDown"]))
                
                hTrg.Rebin(2)
                hNoTrg.Rebin(2)
                hNoTrgUp.Rebin(2)
                hNoTrgDown.Rebin(2)


                #=========== Triggered histogram ===========
                xvalues = []
                xerrorhigh = []
                xerrorlow  = []
                yvalues    = []
                yerrorhigh = []
                yerrorlow  = []
                for i in range(1, hTrg.GetNbinsX()+1):
                    xvalues.append(hTrg.GetBinCenter(i))
                    yvalues.append(hTrg.GetBinContent(i))
                    yerrorhigh.append(hTrg.GetBinError(i)/2.0)
                    yerrorlow.append(hTrg.GetBinError(i)/2.0)
                    xerrorhigh.append(hTrg.GetBinWidth(i)/2.0)
                    xerrorlow.append(hTrg.GetBinWidth(i)/2.0)
                
                grTriggered = ROOT.TGraphAsymmErrors(len(xvalues), array.array("d", xvalues), array.array("d", yvalues), array.array("d", xerrorlow), array.array("d", xerrorhigh), array.array("d", yerrorlow), array.array("d", yerrorhigh))
                grTriggered.SetMarkerColor(ROOT.kRed)
                grTriggered.SetLineColor(ROOT.kRed)
                grTriggered.SetMarkerStyle(20)
                grTriggered.SetMarkerSize(0.5)
                grTriggered.SetFillStyle(3001)
                grTriggered.SetFillColor(ROOT.kRed)
                
                xvalues = []
                xerrorhigh = []
                xerrorlow  = []
                yvalues    = []
                yerrorhigh = []
                yerrorlow  = []
                for i in range(1, hNoTrg.GetNbinsX()+1):
                    yvalue     = hNoTrg.GetBinContent(i)
                    yStatError = hNoTrg.GetBinError(i)
                    
                    content     = hNoTrg.GetBinContent(i)
                    contentUp   = hNoTrgUp.GetBinContent(i)
                    contentDown = hNoTrgDown.GetBinContent(i) 
                    
                    xvalues.append(hNoTrg.GetBinCenter(i))
                    xerrorhigh.append(hNoTrg.GetBinWidth(i)/2.0)
                    xerrorlow.append(hNoTrg.GetBinWidth(i)/2.0)
                    yvalues.append(content)
                    yerrorlow.append(-(contentDown-content))
                    yerrorhigh.append(contentUp - content)
                    
                array_xvalues = array.array("d", xvalues)
                array_yvalues = array.array("d", yvalues)
                
                grWeighted = ROOT.TGraphAsymmErrors(len(xvalues), array.array("d", xvalues), array.array("d", yvalues), array.array("d", xerrorlow), array.array("d", xerrorhigh), array.array("d", yerrorlow), array.array("d", yerrorhigh))
                grWeighted.SetMarkerColor(ROOT.kBlack)
                grWeighted.SetLineColor(ROOT.kBlack)
                grWeighted.SetMarkerStyle(20)
                grWeighted.SetMarkerSize(0.5)
                grWeighted.SetFillStyle(3001)
                grWeighted.SetFillColor(ROOT.kGray+2)
                
                if "X_m" in var and "HX_m" not in var:
                    xmin = 400.0 
                    xmax = 2000.0
                else:
                    xmin = 50.0
                    xmax = 250.0
                
                grTriggered.GetXaxis().SetRangeUser(xmin, xmax)
                grWeighted.GetXaxis().SetRangeUser(xmin, xmax)
                
                mgr = ROOT.TMultiGraph()
                mgr.Add(grWeighted)
                mgr.Add(grTriggered)
                mgr.GetXaxis().SetRangeUser(xmin, xmax)
                mgr.Draw("AP E2")
                
                mgr.GetYaxis().SetTitle("Events")
                mgr.GetYaxis().SetTitleSize(0.065)
                mgr.GetYaxis().SetTitleOffset(0.7)
                
                grTriggered.GetXaxis().SetRangeUser(xmin, xmax)
                grWeighted.GetXaxis().SetRangeUser(xmin, xmax)
                
                legend.AddEntry(grTriggered, "triggered")
                legend.AddEntry(grWeighted, "weighted")
                legend.Draw("same")
                
                tex_cms = AddCMSText()
                tex_cms.Draw("same")
                
                tex_prelim = AddPreliminaryText()
                tex_prelim.Draw("same")
                
                header = ROOT.TLatex()
                header.SetTextSize(0.05)
                header.DrawLatexNDC(0.71, 0.93, "2018, #sqrt{s} = 13 TeV")
                
                # Pad2
                d.Modified()
                d.Update()
                d.cd() # Go back to the main canvas before defining pad2
                
                pad2 = ROOT.TPad("pad2", "pad2", 0, 0., 1, 0.35)
                pad2.SetTopMargin(0)
                pad2.SetBottomMargin(0.2)
                pad2.SetGridx() 
                pad2.SetGridy()
                pad2.Draw()
                pad2.SetLeftMargin(0.12);
                pad2.SetBottomMargin(0.3);
                pad2.cd()
                
                #============================================
                # Divide the two histograms
                #============================================
                xvalues_ratio = []
                yvalues_ratio = []
                
                exlvalues_ratio = []
                exhvalues_ratio = []
                eylvalues_ratio = []
                eyhvalues_ratio = []
                
                ratioError = ROOT.TGraphAsymmErrors()
                
                for i in range(1, hTrg.GetNbinsX()+1):
                    x_Triggered = ctypes.c_double(0)
                    y_Triggered = ctypes.c_double(0)
                    x_Weighted  = ctypes.c_double(0)
                    y_Weighted  = ctypes.c_double(0)
                    grTriggered.GetPoint(i-1, x_Triggered, y_Triggered)
                    grWeighted.GetPoint(i-1, x_Weighted, y_Weighted)
                    
                    # Sanity check
                    assert(x_Triggered.value == x_Weighted.value)
                    
                    if (y_Weighted.value == 0):
                        ratio=1
                        eyl = 0.0
                        eyh = 0.0
                    else:
                        ratio = y_Triggered.value/y_Weighted.value
                        error = hTrg.GetBinError(i)/y_Weighted.value
                        eyl = grWeighted.GetErrorYlow(i-1)/y_Weighted.value
                        eyh = grWeighted.GetErrorYhigh(i-1)/y_Weighted.value
                    
                    exl = grWeighted.GetErrorXlow(i-1)
                    exh = grWeighted.GetErrorXhigh(i-1)
                    
                    xvalues_ratio.append(x_Triggered.value)
                    exlvalues_ratio.append(hTrg.GetBinWidth(i)/2.0)
                    exhvalues_ratio.append(hTrg.GetBinWidth(i)/2.0)
                    
                    yvalues_ratio.append(ratio)
                    eylvalues_ratio.append(error/2.0)
                    eyhvalues_ratio.append(error/2.0)
                    
                    ratioError.SetPoint(i-1, x_Triggered.value, 1.0)
                    ratioError.SetPointError(i-1, exl, exh, eyl, eyh)
                    
                    print(" Bin = %s  | Ratio = %s  | Error = %s , exl=%s,  exh=%s,  eyl=%s,  eyh=%s" % (i, ratio, error, exl, exh, eyl, eyh))
                    
                hRatio=ROOT.TGraphAsymmErrors(len(xvalues_ratio), array.array("d", xvalues_ratio), array.array("d", yvalues_ratio), array.array("d", exlvalues_ratio), array.array("d", exhvalues_ratio), array.array("d", eylvalues_ratio), array.array("d", eyhvalues_ratio))
                #hRatio.SetAxisRange(xmin, xmax)
                hRatio.GetXaxis().SetRangeUser(xmin, xmax)
                
                hRatio.SetTitle("")
                hRatio.SetMinimum(0.0)
                hRatio.SetMaximum(2.0)
                hRatio.Draw("AP")
                hRatio.GetYaxis().SetTitle("ratio")
                hRatio.GetYaxis().SetNdivisions(505)
                hRatio.GetYaxis().SetTitleSize(0.1)
                hRatio.GetYaxis().SetTitleOffset(0.5)
                hRatio.GetYaxis().SetLabelSize(0.1)
                
                if "HX_m" in var:
                    xlabel = "m_{H_{X}} (GeV)"
                elif "X_m" in var:
                    xlabel = "m_{X} (GeV)"
                elif "H1_m" in var:
                    xlabel = "m_{H_{1}} (GeV)"
                else:
                    xlabel = "m_{H_{1}} (GeV)"
                
                hRatio.GetXaxis().SetTitle(xlabel)
                hRatio.GetXaxis().SetTitleSize(0.15)
                hRatio.GetXaxis().SetTitleOffset(0.85)
                hRatio.GetXaxis().SetLabelSize(0.13)
                
                ratioError.SetFillStyle(3001)
                ratioError.SetFillColor(ROOT.kGray+2)
                ratioError.GetXaxis().SetRangeUser(xmin, xmax)
                ratioError.Draw("same E2")
                                
                # Update canvas
                d.cd()
                d.Modified()
                d.Update()
                                
                # Save plot
                for s in args.formats:
                    saveName = os.path.join(args.path, "%s_%s_%s%s" % ("trgVal_"+var, sel, sample, s))
                    print("saveName = ", saveName)
                    d.SaveAs(saveName)
        d.Close()

    print("\n===Find all the plots under: %s" % (args.path))
    return
    
    

if __name__ == "__main__":

    # Default values
    VERBOSE     = False
    ANALYSIS    = "NMSSM_XYH_YToHH_6b"
    STUDY       = "TriggerSFs"
    YEAR        = "2018"
    FORMATS     = [".png", ".pdf"]
    SAVEPATH    = getPublicPath()
    
    parser = ArgumentParser(description="Perform mass resolution studies")
    parser.add_argument("-v", "--verbose", dest="verbose", default=VERBOSE, action="store_true", help="Verbose mode for debugging purposes [default: %s]" % (VERBOSE))
    parser.add_argument("--formats", dest="formats", default=FORMATS, action="store", help="Formats to save histograms")
    parser.add_argument("--year", dest="year", default=YEAR, action="store", help="Which year you process")
    
    args = parser.parse_args()
    args.path = os.path.join(SAVEPATH, "%s_%s_%s_%s" % (ANALYSIS, STUDY, YEAR, datetime.datetime.now().strftime('%d_%b_%Y')))
    if not os.path.exists(args.path):
        os.makedirs(args.path)
    main(args)

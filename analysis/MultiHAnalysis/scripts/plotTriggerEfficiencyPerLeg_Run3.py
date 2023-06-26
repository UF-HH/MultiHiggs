#!/usr/bin/env python
'''
DESCRIPTION:

PREREQUISITES:

LAST USED:
./plotTriggerEfficiencyPerLeg_Run3.py --rfile TriggerEfficiency_2022_analyzedOn_09_Jun_2023.root
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
import array
import math

ROOT.gROOT.SetBatch(True)

def Verbose(msg, printHeader=False):
    '''
    Calls Print() only if verbose options is set to true.
    '''
    if not args.verbose:
        return
    print(msg)
    return
    
def _divideOrZero(numerator, denominator):
    if denominator == 0:
        return 0
    return numerator/denominator

def _getCrossSection(sampleName, energy):
    
    crossSections = {}
    crossSections["13"]   = {}
    crossSections["13.6"] = {}
    crossSections["13"]["TTto2L2Nu"] = 831.76*0.3259*0.3259
    return crossSections[energy][sampleName]

def _getLuminosity(year):
    if year =="2022":
        return 29259 # pb 
        
def _normalizeHistogram(h, isData):
    
    if isData:
        return h
    else:
        # Normalize to cross-section
        h = _normalizeToFactor(h, _getCrossSection("TTto2L2Nu","13"))
        # Normalize to luminosity
        h = _normalizeToFactor(h, _getLuminosity("2022"))
    return h

def _normalizeToFactor(h, f):
    backup = ROOT.gErrorIgnoreLevel
    ROOT.gErrorIgnoreLevel = ROOT.kError
    h.Sumw2() # errors are also scaled after this call 
    ROOT.gErrorIgnoreLevel = backup
    h.Scale(f)
    return h

def _createRatioErrorPropagation(histo1, histo2):
    '''
    Creates a ratio histogram by propagating the uncertainties to the ratio
    
    \return TH1 or TGraphAsymmErrors of histo1/histo2
    
    In case of asymmetric uncertainties, the uncertainties are added in
    quadrature for both sides separately (a rather crude approximation).
    '''
    if isinstance(histo1, ROOT.TGraph) and isinstance(histo2, ROOT.TGraph):
        xvalues = []
        yvalues = []
        yerrs = []
        
        for i in range(0, histo1.GetN()):
            yval = histo2.GetY()[i]
            if yval == 0:
                continue
            xvalues.append(histo1.GetX()[i])
            yvalue = histo1.GetY()[i] / yval
            yvalues.append(yvalue)
            
            err1 = max(histo1.GetErrorYhigh(i), histo1.GetErrorYlow(i))
            err2 = max(histo2.GetErrorYhigh(i), histo2.GetErrorYlow(i))
            yerrs.append( yvalue * math.sqrt( _divideOrZero(err1, histo1.GetY()[i])**2 +
                                              _divideOrZero(err2, histo2.GetY()[i])**2 ) )
            
        if len(xvalues) > 0:
            gr = ROOT.TGraphAsymmErrors(len(xvalues), array.array("d", xvalues), array.array("d", yvalues),
                                        histo1.GetEXlow(), histo1.GetEXhigh(),
                                        array.array("d", yerrs), array.array("d", yerrs))
        else:
            gr = ROOT.TGraphAsymmErrors()
        return gr
    else:
        raise Exception("type of histo is: %s" %(type(histo1)))

class ComparisonPlot_DataMC:
    '''
    Create Comparison plot with TGraphAsymmErrors for Data and MC
    '''
    def __init__(self, hData, hMC, **kwargs):
        
        hData.SetMarkerColor(ROOT.kBlack)
        hData.SetLineColor(ROOT.kBlack)
        hData.SetMarkerStyle(20)
        
        hMC.SetMarkerColor(ROOT.kBlue)
        hMC.SetMarkerStyle(20)
        hMC.SetLineColor(ROOT.kBlue)
        
        self._hData  = hData
        self._hMC    = hMC
        self._ratio  = _createRatioErrorPropagation(self._hData, self._hMC)
        self._kwargs = kwargs
        return
        
    def _createFrame(self, framename, createRatio=False):
        
        ratioType = "binomial"
        drawStyle = "EP"
        
        statSysError = None
        statError = None
        
        frame = CanvasFrameTwo(self._ratio, self._hData, self._hMC, framename, **self._kwargs)
        return frame

    def _getFrame(self):
        return self.frame
    
    def _getPad(self):
        return self.cf.pad

class CanvasFrameTwo:
    '''
    Create TCanvas and frames for two TPads
    '''
    def __init__(self, ratio, h1, h2, name, **kwargs):
        '''
        Create TCanvas and TH1 for the frame
        '''
        class FrameWrapper:
            
            def __init__(self, pad1, frame1, pad2, frame2):
                self.pad1 = pad1
                self.frame1 = frame1
                self.pad2 = pad2
                self.frame2 = frame2
                
            def GetXaxis(self):
                return self.frame2.GetXaxis()

            def GetYaxis(self):
                return self.frame1.GetYaxis()

        histos1 = []
        if isinstance(h1, list):
            histos1 = h1[:]
        else:
            histos1.append(h1)
        histos2 = []
        if isinstance(h2, list):
            histos2 = h2[:]
        else:
            histos2.append(h2)
        if len(histos2) == 0:
            raise Exception("Empty set of histograms for the second pad!")
        
        # Create the canvas, divide it to two
        canvasFactor = kwargs.get("canvasFactor", 1.25)
        divisionPoint = 1-1/canvasFactor
        self.canvas = ROOT.TCanvas(name, name, ROOT.gStyle.GetCanvasDefW(), int(ROOT.gStyle.GetCanvasDefH()*canvasFactor))
        self.canvas.Divide(1, 2)
        
        # Do it like this (create empty, update from kwargs) in order
        # to make a copy and NOT modify the dictionary in the caller
        opts1 = {}
        opts1.update(kwargs.get("opts", {}))
        opts2 = {}
        opts2.update(kwargs.get("opts2", {}))
        
        if "xmin" in opts2 or "xmax" in opts2 or "nbins" in opts2 or "nbinsx" in opts2:
            raise Exception("No 'xmin', 'xmax', 'nbins', or 'nbinsy' allowed in opts2, values are taken from opts/opts1")
            
        opts2["xmin"] = opts1["xmin"]
        opts2["xmax"] = opts1["xmax"]
        opts2["nbins"] = opts1.get("nbins", None)
        opts2["nbinsx"] = opts1.get("nbinsx", None)
        
        topMargin = ROOT.gStyle.GetPadTopMargin()
        bottomMargin = ROOT.gStyle.GetPadBottomMargin()
        divisionPoint += (1-divisionPoint)*bottomMargin # correct for (almost-)zeroing bottom margin of pad1
        divisionPointForPad1 = 1-( (1-divisionPoint) / (1-0.02) ) # then correct for the non-zero bottom margin, but for pad1 only

        # Set the lower point of the upper pad to divisionPoint
        self.pad1 = self.canvas.cd(1)
        yup = 1.0
        ylow = divisionPointForPad1
        xup = 1.0
        xlow = 0.0
        self.pad1.SetPad(xlow, ylow, xup, yup)
        self.pad1.SetFillStyle(4000) # transparent
        self.pad1.SetBottomMargin(0.02) # need some bottom margin here for eps/pdf output (at least in ROOT 5.34)

        # Set the upper point of the lower pad to divisionPoint
        self.pad2 = self.canvas.cd(2)
        yup = divisionPoint
        ylow = 0.0
        self.pad2.SetPad(xlow, ylow, xup, yup)
        self.pad2.SetFillStyle(4000)
        self.pad2.SetTopMargin(0.0)
        self.pad2.SetBottomMargin(bottomMargin/(canvasFactor*divisionPoint))
        
        yoffsetFactor = canvasFactor
        xoffsetFactor = 1/divisionPoint
        
        # Check if the first histogram has x axis bin labels
        self.canvas.cd(1)
        self.frame1 = _drawFrame(self.pad1, opts1["xmin"], opts1["ymin"], opts1["xmax"], opts1["ymax"], opts1.get("nbins", None), opts1.get("nbinsx", None), opts1.get("nbinsy", None))
        (labelSize, titleSize) = (self.frame1.GetXaxis().GetLabelSize(), self.frame1.GetXaxis().GetTitleSize())
        self.frame1.GetXaxis().SetLabelSize(0)
        self.frame1.GetXaxis().SetTitleSize(0)
        self.frame1.GetYaxis().SetTitle(opts1["ylabel"])
        self.frame1.GetYaxis().SetTitleSize(0.05)
        self.frame1.GetYaxis().SetTitleOffset(self.frame1.GetYaxis().GetTitleOffset()*yoffsetFactor)
        
        self.canvas.cd(2)
        self.frame2 = _drawFrame(self.pad2, opts2["xmin"], opts2["ymin"], opts2["xmax"], opts2["ymax"], opts2.get("nbins", None), opts2.get("nbinsx", None))
        self.frame2.GetXaxis().SetTitle(opts1["xlabel"])
        self.frame2.GetYaxis().SetTitle(opts2["ylabel"])
        self.frame2.GetXaxis().SetTitleSize(0.10)
        self.frame2.GetYaxis().SetTitleSize(0.08)
        self.frame2.GetXaxis().SetLabelSize(0.08)
        self.frame2.GetYaxis().SetLabelSize(0.06)
        self.frame2.GetYaxis().SetTitleOffset(0.4)
        
        self.canvas.cd(1)
        
        # Default position on canvas
        leg = ROOT.TLegend(0.50, 0.20, 0.75, 0.40, "")
        leg.SetFillColor(0)
        leg.SetFillStyle(0)
        leg.SetBorderSize(0)
        leg.SetTextColor(ROOT.kBlack)
        
        histos1[0].SetMarkerColor(ROOT.kBlack)
        histos1[0].SetMarkerStyle(20)
        histos1[0].Draw("same PE")
        leg.AddEntry(histos1[0], "Data")
        
        histos2[0].SetMarkerColor(ROOT.kBlue)
        histos2[0].SetMarkerStyle(20)
        histos2[0].Draw("same PE")
        leg.AddEntry(histos2[0], "Simulation (postEE)")
                
        texcms = ROOT.TLatex()
        texcms.SetTextAlign(31)
        texcms.SetTextFont(63)
        texcms.SetLineWidth(2)
        texcms.SetTextSize(30)
        texcms.DrawLatexNDC(0.20, 0.91, "CMS")
        
        texPriv = ROOT.TLatex()
        texPriv.SetTextFont(53)
        texPriv.SetTextSize(28)
        texPriv.SetLineWidth(2)
        texPriv.DrawLatexNDC(0.21, 0.91, "Private Work")
        
        header = ROOT.TLatex()
        header.SetTextSize(0.04)
        header.DrawLatexNDC(0.62, 0.91, "29.26 fb^{-1} (2022, 13.6 TeV)")
        
        line = ROOT.TLine(opts1["xmin"], 1.0, opts1["xmax"], 1.0)
        line.SetLineStyle(ROOT.kDashDotted)
        line.SetLineColor(13)
        line.DrawClone("same")
        
        
        self.canvas.cd(2)        
        ratio.SetMarkerStyle(20)
        ratio.Draw("same PE")
        
        line = ROOT.TLine(opts1["xmin"], 1.0, opts1["xmax"], 1.0)
        line.SetLineStyle(ROOT.kDashDotted)
        line.SetLineColor(13)
        line.DrawClone("same")
        


        self.canvas.cd(1)
        leg.DrawClone("same")
        
        self.frame = FrameWrapper(self.pad1, self.frame1, self.pad2, self.frame2)
        self.frame2.GetYaxis().SetNdivisions(505)
        self.pad = self.pad1


def _drawFrame(pad, xmin, ymin, xmax, ymax, nbins=None, nbinsx=None, nbinsy=None):
    '''
    Draw a frame

    \param pad   TPad to draw the frame to
    \param xmin  Minimum X axis value
    \param ymin  Minimum Y axis value
    \param xmax  Maximum X axis value
    \param ymax  Maximum Y axis value
    \param nbins Number of x axis bins
    \param nbinsx Number of x axis bins
    \param nbinsy Number of y axis bins
    
    If nbins is None, TPad.DrawFrame is used. Otherwise a custom TH1 is
    created for the frame with nbins bins in x axis.
    
    Use case: selection flow histogram (or whatever having custom x axis
    lables).
    '''
    if nbins is not None and nbinsx is not None:
        raise Exception("Both 'nbins' and 'nbinsx' should not be set, please use the latter only")
    if nbins is None:
        nbins = nbinsx

    if nbinsx is None and nbinsy is None:
        return pad.DrawFrame(xmin, ymin, xmax, ymax)
    else:
        pad.cd()
        # From TPad.cc
        frame = pad.FindObject("hframe")
        if frame is not None:
            # frame.Delete()
            frame = None
        if nbinsx is not None and nbinsy is None:
            frame = ROOT.TH1F("hframe", "hframe", nbinsx, xmin, xmax)
        elif nbinsx is None and nbinsy is not None:
            frame = ROOT.TH2F("hframe", "hframe", 100,xmin,xmax, nbinsy,ymin,ymax)
        else: # neither is None
            frame = ROOT.TH2F("hframe", "hframe", nbinsx,xmin,xmax, nbinsy,ymin,ymax)

        frame.SetBit(ROOT.TH1.kNoStats)
        frame.SetBit(ROOT.kCanDelete)
        frame.SetMinimum(ymin)
        frame.SetMaximum(1.1)#ymax)
        frame.GetYaxis().SetLimits(ymin, ymax)
        frame.SetDirectory(0)
        frame.Draw(" ")
        return frame





def convert2TGraph(tefficiency):
    '''
    Converts a TEfficiency histogram into a TGraph
    '''
    if (0): print("Convert TEfficiency into a TGraph")
    x     = []
    y     = []
    xerrl = []
    xerrh = []
    yerrl = []
    yerrh = []
    
    h = tefficiency.GetCopyTotalHisto()
    name = h.GetName()
    n = h.GetNbinsX()

    xMin= h.GetXaxis().GetXmin()
    xMax= h.GetXaxis().GetXmax()

    for i in range(1,n+1):
        
        if (0):
            print("x = %s,     y = %s" % (h.GetBinLowEdge(i)+5*h.GetBinWidth(i), tefficiency.GetEfficiency(i)))
        
        x.append(h.GetBinLowEdge(i)+0.5*h.GetBinWidth(i))
        xerrl.append(0.5*h.GetBinWidth(i))
        xerrh.append(0.5*h.GetBinWidth(i))
        y.append(tefficiency.GetEfficiency(i))
        yerrl.append(tefficiency.GetEfficiencyErrorLow(i))
        
        # ugly hack to prevent error going above 1
        errUp = tefficiency.GetEfficiencyErrorUp(i)
        if y[-1] == 1.0:
            errUp = 0
        yerrh.append(errUp)
        
        # Save values to a TGraph
        tgraph= ROOT.TGraphAsymmErrors(n,array.array("d",x),
                                       array.array("d",y),
                                       array.array("d",xerrl),
                                       array.array("d",xerrh),
                                       array.array("d",yerrl),
                                       array.array("d",yerrh))

        tgraph.SetName(name)
    return tgraph

def RemoveNegatives(histo):
    for binX in range(histo.GetNbinsX()+1):
        if histo.GetBinContent(binX) < 0:
            histo.SetBinContent(binX, 0.0)
    return

def CheckNegatives(n, d, verbose=False):
    '''
    '''
    table    = []
    txtAlign = "{:<5} {:>20} {:>20}"
    hLine    = "="*50
    table.append(hLine)
    table.append(txtAlign.format("Bin #", "Numerator (8f)", "Denominator (8f)"))
    table.append(hLine)
    
    # For-loop: All bins in x-axis
    for i in range(1, n.GetNbinsX()+1):
        nbin = n.GetBinContent(i)
        dbin = d.GetBinContent(i)

        table.append(txtAlign.format(i, "%0.8f" % (nbin), "%0.8f" % (dbin) ))
        
        # Numerator > Denominator
        if nbin > dbin:
            n.SetBinContent(i,dbin)

        # Numerator < 0 
        if nbin < 0:
            n.SetBinContent(i,0)

        # Denominator < 0
        if dbin < 0:
            n.SetBinContent(i,0)
            d.SetBinContent(i,0)
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

def AddCMSText(setx=0.20, sety=0.91):
    texcms = ROOT.TLatex(0.,0., 'CMS');
    texcms.SetNDC();
    texcms.SetTextAlign(31);
    texcms.SetX(setx);
    texcms.SetY(sety);
    texcms.SetTextFont(63);
    texcms.SetLineWidth(2);
    texcms.SetTextSize(30);
    return texcms

def AddPreliminaryText(setx=0.21, sety=0.91):
    tex = ROOT.TLatex(0.,0., 'Preliminary');
    tex.SetNDC();
    tex.SetX(setx);
    tex.SetY(sety);
    tex.SetTextFont(53);
    tex.SetTextSize(28);
    tex.SetLineWidth(2)
    return tex

def AddPrivateWorkText(setx=0.21, sety=0.91):
    tex = ROOT.TLatex(0.,0., 'Private Work');
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
    
    y1 = 0.20
    y2 = 0.40
        
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
    
    if "PFHT" in h:
        opts["xmin"] = 300
        opts["xmax"] = 1600
    elif "ForthJetPt" in h:
        opts["xmin"] = 35
        opts["xmax"] = 100
    

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


def getCanvas():
    d = ROOT.TCanvas("", "", 800, 700)
    d.SetLeftMargin(0.12)
    d.SetRightMargin(0.15)
    d.SetLeftMargin(0.13)
    return d


def SetEfficiencyStyle(h, isData):
    
    if isData:
        h.SetMarkerStyle(22)
        h.SetMarkerColor(ROOT.kBlack)
        h.SetLineColor(ROOT.kBlack)
    else:
        h.SetMarkerStyle(22)
        h.SetMarkerColor(ROOT.kBlue)
        h.SetLineColor(ROOT.kBlue)
    return h

def main(args):
    
    f = ROOT.TFile.Open(args.rfile, "READ")
    
    # Use Clopper-Pearson statistical option
    statOption = ROOT.TEfficiency.kFCP
    
    #=======================================================================================================================
    # Efficiency of L1 Seeds:
    #=======================================================================================================================
    hName = "L1_Efficiency_vs_PFHT_baseline"
    d = getCanvas()
    
    opts = GetOpts(hName)
    opts["legend"]["header"] = hName.split("_")[-1]
    legend = CreateLegend(opts)
    legend.SetHeader("")
    
    hNum  = f.Get("h_PFHT_Passed_L1_MuonEG")
    hDen  = f.Get("h_PFHT_MuonEG")
    hNum.GetYaxis().SetTitle("#varepsilon_{L1}")
    hDen.GetYaxis().SetTitle("#varepsilon_{L1}")
    
    hEff  = ROOT.TEfficiency(hNum, hDen)
    hEff.SetStatisticOption(statOption)
    hEff.Draw()

    # MC distributions -> Need to normalize them to reflect the integrated luminosity
    hNumMC = f.Get("h_PFHT_Passed_L1_TT")
    hDenMC = f.Get("h_PFHT_TT")
    hNumMC.GetYaxis().SetTitle("#varepsilon_{L1}")
    hDenMC.GetYaxis().SetTitle("#varepsilon_{L1}")
    
    #hNumMC = _normalizeHistogram(hNumMC, False)
    #hDenMC = _normalizeHistogram(hDenMC, False)
    #==========================================
        
    hEffMC = ROOT.TEfficiency(hNumMC, hDenMC)
    hEffMC.SetStatisticOption(statOption)
    hEffMC.Draw("same")
    
    d.Modified()
    d.Update()
    
    hEff.GetPaintedGraph().GetXaxis().SetRangeUser(300, 1600)
    hEff.GetPaintedGraph().GetYaxis().SetRangeUser(0.0, 1.1)
    legend.AddEntry(hEff, "Data")
    legend.AddEntry(hEffMC, "t#bar{t}")
    

    tGraph_Eff_Data = convert2TGraph(hEff)
    tGraph_Eff_MC   = convert2TGraph(hEffMC)
    

    d.Modified()
    d.Update()
    tex_cms = AddCMSText()
    tex_cms.Draw("same")
    tex_prelim = AddPrivateWorkText()
    tex_prelim.Draw("same")
    
    header = ROOT.TLatex()
    header.SetTextSize(0.04)
    header.DrawLatexNDC(0.47, 0.91, "29.26 fb^{-1} (2022, 13.6 TeV)")

    line = ROOT.TLine(400,0.0,400,1.1)
    line.SetLineStyle(6)
    line.SetLineColor(ROOT.kBlue)
    line.Draw("same")
    
    hEff.GetPaintedGraph().GetYaxis().SetTitle("#varepsilon_{L1}")
    legend.Draw("same")
    
    # Update canvas
    d.Modified()
    d.Update()
    d.SaveAs("%s.pdf" % (hName))
    #============================================================================================================================================
    
    kwargs = {}
    kwargs["opts"]={"xmin": 200, "xmax":1600, "xlabel": "Offline PF H_{T} [GeV]", "ylabel": "#varepsilon_{L1}", "ymin":0.5, "ymax": 1.1, "ymaxfactor":1.1, "legend": {"move": False, "dx": -0.15, "dy": +0.3, "size":0.03, "header": None} }
    kwargs["opts2"]={"ylabel": "Data / MC", "ymin": 0.7, "ymax": 1.3}
    p = ComparisonPlot_DataMC(tGraph_Eff_Data, tGraph_Eff_MC, **kwargs)
    frame = p._createFrame("frame_L1EffvsPFHT_baseline", createRatio=True)
    frame.canvas.SaveAs("L1Efficiency_vs_HT_DataVsMC.pdf")
    
    ROOT.gStyle.SetPaintTextFormat("4.2f");
    
    # ===== DATA
    # Efficiency = Offline Selection && Reference Trigger && Signal Trigger / Offline Selection && Reference Trigger
    selections = ["baseline", "2BTagM", "2BTagM_PFHT400", "3BTagM", "3BTagM_PFHT400"]
    for sel in selections:
        
        hName = "L1_HLT_Efficiency_2D_PFHT_vs_MeanBTagPNet_%s_MuonEG_Data" % (sel)
        d2D = getCanvas()
        if sel == "baseline":
            hNum = f.Get("h_PFHT_vs_MeanBTag_Passed_FullPath_MuonEG")
            hDen = f.Get("h_PFHT_vs_MeanBTag_MuonEG")
        else:
            hNum = f.Get("h_PFHT_vs_MeanBTag_%s_Passed_FullPath_MuonEG" % (sel))
            hDen = f.Get("h_PFHT_vs_MeanBTag_%s_MuonEG" % (sel))
        
        hNum.GetXaxis().SetRangeUser(300, 1600)
        hDen.GetXaxis().SetRangeUser(300, 1600)
        
        hEff2D = ROOT.TEfficiency(hNum, hDen)
        hEff2D.Draw("text COLZ")
        hEff2D.SetStatisticOption(statOption)
        
        tex_cms = AddCMSText()
        tex_cms.Draw("same")
        tex_prelim = AddPrivateWorkText()
        tex_prelim.Draw("same")
        header = ROOT.TLatex()
        header.SetTextSize(0.04)
        header.DrawLatexNDC(0.47, 0.91, "29.26 fb^{-1} (2022, 13.6 TeV)")
        
        d2D.Modified()
        d2D.Update()
        
        hEff2D.GetPaintedHistogram().SetMinimum(0.0)
        hEff2D.GetPaintedHistogram().SetMaximum(1.0)
                
        d2D.Modified()
        d2D.Update()
        d2D.SaveAs("%s.pdf" % (hName))
        #============================================================================================================================================
        
        # 2D PFHT vs 4th jet pt:
        hName = "L1_HLT_Efficiency_2D_PFHT_vs_ForthJetPt_%s_Data_MuonEG" % (sel)
        d = getCanvas()
        if sel == "baseline":
            hNum = f.Get("h_PFHT_vs_ForthJetPt_Passed_FullPath_MuonEG")
            hDen = f.Get("h_PFHT_vs_ForthJetPt_MuonEG")
        else:
            hNum = f.Get("h_PFHT_vs_ForthJetPt_%s_Passed_FullPath_MuonEG" % (sel))
            hDen = f.Get("h_PFHT_vs_ForthJetPt_%s_MuonEG" % (sel))
        
        hEff2D = ROOT.TEfficiency(hNum, hDen)
        hEff2D.SetStatisticOption(statOption)
        hEff2D.Draw("text COLZ")
        
        tex_cms = AddCMSText()
        tex_cms.Draw("same")
        tex_prelim = AddPrivateWorkText()
        tex_prelim.Draw("same")
        header = ROOT.TLatex()
        header.SetTextSize(0.04)
        header.DrawLatexNDC(0.47, 0.91, "29.26 fb^{-1} (2022, 13.6 TeV)")
        
        d.Modified()
        d.Update()
        
        hEff2D.GetPaintedHistogram().SetMinimum(0.0)
        hEff2D.GetPaintedHistogram().SetMaximum(1.0)
        
        d.Modified()
        d.Update()
        d.SaveAs("%s.pdf" % (hName))
    

    # ===== TT Simulation
    #==============================
    # Efficiency = Offline Selection && Reference Trigger && Signal Trigger / Offline Selection && Reference Trigger
    selections = ["baseline", "2BTagM", "2BTagM_PFHT400", "3BTagM", "3BTagM_PFHT400"]
    for sel in selections:
        
        hName = "L1_HLT_Efficiency_2D_PFHT_vs_MeanBTagPNet_%s_TT" % (sel)
        d2D = getCanvas()
        if sel == "baseline":
            hNum = f.Get("h_PFHT_vs_MeanBTag_Passed_FullPath_TT")
            hDen = f.Get("h_PFHT_vs_MeanBTag_TT")
        else:
            hNum = f.Get("h_PFHT_vs_MeanBTag_%s_Passed_FullPath_TT" % (sel))
            hDen = f.Get("h_PFHT_vs_MeanBTag_%s_TT" % (sel))
        
        hNum.GetXaxis().SetRangeUser(300, 1600)
        hDen.GetXaxis().SetRangeUser(300, 1600)
        
        hEff2D_TT = ROOT.TEfficiency(hNum, hDen)
        hEff2D_TT.Draw("text COLZ")
        hEff2D_TT.SetStatisticOption(statOption)
        
        tex_cms = AddCMSText()
        tex_cms.Draw("same")
        tex_prelim = AddPrivateWorkText()
        tex_prelim.Draw("same")
        header = ROOT.TLatex()
        header.SetTextSize(0.04)
        header.DrawLatexNDC(0.47, 0.91, "29.26 fb^{-1} (2022, 13.6 TeV)")
        
        d2D.Modified()
        d2D.Update()
        
        #hEff2D_TT.GetPaintedHistogram().SetMinimum(0.0)
        #hEff2D_TT.GetPaintedHistogram().SetMaximum(1.0)
                
        d2D.Modified()
        d2D.Update()
        d2D.SaveAs("%s.pdf" % (hName))
        #============================================================================================================================================
        
        # 2D PFHT vs 4th jet pt:
        hName = "L1_HLT_Efficiency_2D_PFHT_vs_ForthJetPt_%s_TT" % (sel)
        d = getCanvas()
        if sel == "baseline":
            hNum = f.Get("h_PFHT_vs_ForthJetPt_Passed_FullPath_TT")
            hDen = f.Get("h_PFHT_vs_ForthJetPt_TT")
        else:
            hNum = f.Get("h_PFHT_vs_ForthJetPt_%s_Passed_FullPath_TT" % (sel))
            hDen = f.Get("h_PFHT_vs_ForthJetPt_%s_TT" % (sel))
        
        hEff2D_TT = ROOT.TEfficiency(hNum, hDen)
        hEff2D_TT.SetStatisticOption(statOption)
        hEff2D_TT.Draw("text COLZ")
        
        print("\n MARINA")
        print(type(hEff2D_TT))
        tex_cms = AddCMSText()
        tex_cms.Draw("same")
        tex_prelim = AddPrivateWorkText()
        tex_prelim.Draw("same")
        header = ROOT.TLatex()
        header.SetTextSize(0.04)
        header.DrawLatexNDC(0.47, 0.91, "29.26 fb^{-1} (2022, 13.6 TeV)")
        
        d2D.Modified()
        d2D.Update()
        
        #hEff2D_TT.GetPaintedHistogram().SetMinimum(0.0)
        #hEff2D_TT.GetPaintedHistogram().SetMaximum(1.0)
        
        d.Modified()
        d.Update()
        d.SaveAs("%s.pdf" % (hName))
    
    

    #====================== Data vs MC agreement

    Vars = ["PFHT", "NJets", "NBJets", "ForthJetPt", "MeanBTag"]
    for sel in selections:
        for var in Vars:
            
            hName = "L1_HLT_Efficiency_vs_%s_%s_DataVsMC" % (var, sel)
            
            d = getCanvas()
            legend = CreateLegend(opts)
            
            if sel == "baseline":
                hDen = f.Get("h_%s_MuonEG" % (var))
                hNum = f.Get("h_%s_Passed_FullPath_MuonEG" % (var))
            else:
                hDen = f.Get("h_%s_%s_MuonEG" % (var, sel))
                hNum = f.Get("h_%s_%s_Passed_FullPath_MuonEG" % (var, sel))
            
                
            if sel == "baseline":
                hDenMC = f.Get("h_%s_TT" % (var))
                hNumMC = f.Get("h_%s_Passed_FullPath_TT" % (var))
            else:
                hDenMC = f.Get("h_%s_%s_TT" % (var, sel))
                hNumMC = f.Get("h_%s_%s_Passed_FullPath_TT" % (var, sel))
            
            #hNumMC = _normalizeHistogram(hNumMC, False)
            #hDenMC = _normalizeHistogram(hDenMC, False)
            
            if "NBJets" in var:
                hNum.GetXaxis().SetRangeUser(1, 5)
                hDen.GetXaxis().SetRangeUser(1, 5)
                hNumMC.GetXaxis().SetRangeUser(1, 5)
                hDenMC.GetXaxis().SetRangeUser(1, 5)
            elif "MeanBTag" in var:
                hNum.GetXaxis().SetRangeUser(0.60, 1.1)
                hDen.GetXaxis().SetRangeUser(0.60, 1.1)
                hNumMC.GetXaxis().SetRangeUser(0.60, 1.1)
                hDenMC.GetXaxis().SetRangeUser(0.60, 1.1)
            elif "PFHT" in var:
                hNum.GetYaxis().SetTitle("#varepsilon_{L1+HLT}")
                hDen.GetYaxis().SetTitle("#varepsilon_{L1+HLT}")
                hNumMC.GetYaxis().SetTitle("#varepsilon_{L1+HLT}")
                hDenMC.GetYaxis().SetTitle("#varepsilon_{L1+HLT}")

            hEff = ROOT.TEfficiency(hNum, hDen)
            hEff.SetStatisticOption(statOption)
            hEff.SetName("Efficiency_%s_%s_MuonEG" % (var, sel))
            hEff.SetMarkerStyle(22)
            hEff.SetMarkerColor(ROOT.kBlack)
            hEff.SetLineColor(ROOT.kBlack)
            hEff.Draw()

            hEffMC = ROOT.TEfficiency(hNumMC, hDenMC)
            hEffMC.SetStatisticOption(statOption)
            hEffMC.SetName("Efficiency_%s_%s_TT" % (var, sel))
            hEffMC.SetMarkerStyle(22)
            hEffMC.SetMarkerColor(ROOT.kBlue)
            hEffMC.SetLineColor(ROOT.kBlue)
            hEffMC.Draw("same")
            
            d.Modified()
            d.Update()
            
            if "NBJets" in var:
                hEff.GetPaintedGraph().GetXaxis().SetRangeUser(1, 5)
                hEffMC.GetPaintedGraph().GetXaxis().SetRangeUser(1, 5)
            elif "PFHT" in var:
                hEff.GetPaintedGraph().GetXaxis().SetRangeUser(300, 1600)
                hEffMC.GetPaintedGraph().GetXaxis().SetRangeUser(300, 1600)

            hEff.GetPaintedGraph().GetYaxis().SetRangeUser(0.0, 1.1)
            hEff.GetPaintedGraph().GetYaxis().SetTitle("#varepsilon_{L1+HLT}")
            
            legend.SetHeader("")
            legend.AddEntry(hEff, "Data")
            legend.Draw("same")
            
            d.Modified()
            d.Update()
            
            tex_cms = AddCMSText()
            tex_cms.Draw("same")
            
            tex_prelim = AddPrivateWorkText()
            tex_prelim.Draw("same")
            
            header = ROOT.TLatex()
            header.SetTextSize(0.04)
            header.DrawLatexNDC(0.47, 0.91, "29.26 fb^{-1} (2022, 13.6 TeV)")
            
            # Update canvas
            d.Modified()
            d.Update()
            d.SaveAs("%s.pdf" % (hName))
            
            
            tGraph_Eff_Data = convert2TGraph(hEff)
            tGraph_Eff_MC   = convert2TGraph(hEffMC)
            
            kwargs = {}
            kwargs["opts"]={"xmin": 200, "xmax":1600, "xlabel": "Offline PF H_{T} [GeV]", "ylabel": "#varepsilon_{L1}", "ymin":0.5, "ymax": 1.1, "ymaxfactor":1.1, "legend": {"move": False, "dx": -0.15, "dy": +0.3, "size":0.03, "header": None} }
            kwargs["opts2"]={"ylabel": "Data / MC", "ymin": 0.7, "ymax": 1.3}
            
            kwargs["opts"]["ylabel"] = "#varepsilon_{L1+HLT}"
            if "NBJets" in var:
                kwargs["opts"]["xlabel"] = "b-jet multiplicity"
                kwargs["opts"]["xmin"]   = 1
                kwargs["opts"]["xmax"]   = 5
                kwargs["opts"]["ymin"] = 0.0
            elif "ForthJetPt" in var:
                kwargs["opts"]["xlabel"] = "Offline p_{T}^{4th jet} [GeV]"
                kwargs["opts"]["xmin"] = 30.0
                kwargs["opts"]["xmax"] = 100
                kwargs["opts"]["ymin"] = 0.0
            elif "NJets" in var:
                kwargs["opts"]["xlabel"] = "Jet multiplicity"
                kwargs["opts"]["xmin"]   = 4
                kwargs["opts"]["xmax"]   = 12
                kwargs["opts"]["ymin"] = 0.0
            elif "MeanBTag" in var:
                kwargs["opts"]["xlabel"] = "Mean PNet score(j^{ldg btag}, j^{subldg btag})"
                kwargs["opts"]["xmin"]   = 0.60
                kwargs["opts"]["xmax"]   = 1.05
                kwargs["opts"]["ymin"] = 0.0
            elif "PFHT" in var:
                kwargs["opts"]["ymin"] = 0.0
                
            p = ComparisonPlot_DataMC(tGraph_Eff_Data, tGraph_Eff_MC, **kwargs)
            frame = p._createFrame("frame_L1EffvsPFHT_baseline", createRatio=True)
            frame.canvas.SaveAs("L1_HL_Efficiency_vs_%s_%s_DataVsMC.pdf" % (var, sel))





    d.Close()

    return
    

if __name__ == "__main__":

    # Default values
    VERBOSE       = True
    YEAR          = "2022"
    TRGROOTFILE   = "TriggerEfficiencies_2018.root"
    REDIRECTOR    = "root://cmseos.fnal.gov/"
    FORMATS       = [".pdf"]
    #FORMATS       = [".png", ".pdf", ".C"]
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

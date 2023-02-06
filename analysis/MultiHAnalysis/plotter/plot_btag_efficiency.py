#!/bin/env python3

import ROOT, os

ROOT.gROOT.SetBatch(1)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetTextFont(42)

def format_hf(histo, linewidth=2, color=ROOT.kBlack, name=None, **kwargs):
  histo.SetLineWidth(linewidth)
  histo.SetLineColor(color)
  histo.SetMarkerColor(color)
  if name:
    histo.SetName(name)
  histo.SetTitle("")

  return histo

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

def plot_wp_efficiency(tfile, wp, variable, output='.'):
  hf5 = format_hf(
    tfile.Get(f"eff/{wp}_hf5_{variable}"),
    color=ROOT.kBlue,
    name='b #rightarrow b',
  )

  hf4 = format_hf(
    tfile.Get(f"eff/{wp}_hf4_{variable}"),
    color=ROOT.kRed,
    name='c #rightarrow b',
  )

  hf0 = format_hf(
    tfile.Get(f"eff/{wp}_hf0_{variable}"),
    color=ROOT.kGreen+2,
    name='guds #rightarrow b',
  )

  canvas = ROOT.TCanvas("", "", 800, 700)
  canvas.SetLeftMargin(0.15)

  legend = ROOT.TLegend(0.60, 0.12, 0.85, 0.3)
  legend.SetHeader(f'DeepJet - {wp.capitalize()}')
  legend.SetFillColor(0)
  legend.SetFillStyle(0)
  legend.SetBorderSize(0)
  legend.SetTextSize(0.04)

  hf5.Draw("ACP")
  legend.AddEntry(hf5, hf5.GetName())

  hf4.Draw("CP same")
  legend.AddEntry(hf4, hf4.GetName())

  hf0.Draw("CP same")
  legend.AddEntry(hf0, hf0.GetName())

  legend.Draw()

  canvas.Update()
  axis = hf5.GetPaintedGraph()
  axis.SetMaximum(1.2e0)
  axis.SetMinimum(0.5e-3)
  canvas.SetLogy()

  prelim_txt = AddPreliminaryText()
  prelim_txt.Draw()

  cms_txt = AddCMSText()
  cms_txt.Draw()

  canvas.Draw()
  canvas.SaveAs(f'{output}/{wp}_btageff_{variable}.png')
  

def plot_all_efficiency(fname, output):
  if not os.path.exists(output):
    os.mkdir(output)

  tfile = ROOT.TFile.Open(fname, 'read')

  for wp in ('loose','medium','tight'):
    for variable in ('jet_pt','jet_eta'):
      plot_wp_efficiency(tfile, wp, variable, output)

if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('--input', help='input root file to plot efficiency. input file produced by skim_btageff.cpp')
  parser.add_argument('--output', help='output directory to store images', default='plots_btageff')

  args = parser.parse_args()
  plot_all_efficiency(args.input, args.output)
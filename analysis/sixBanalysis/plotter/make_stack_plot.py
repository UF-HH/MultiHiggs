import ROOT
ROOT.gROOT.SetBatch(True)

def histo_name(var, sel, sample, nametag=None):
    if not nametag:
        return '{}/{}/{}'.format(sample, sel, var)
    else:
        return '{}/{}/{}_{}'.format(sample, sel, var, nametag)

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--var',  dest='var',  required=True)
parser.add_argument('--sel',  dest='sel',  required=True)
parser.add_argument('--file', dest='file', required=True)
parser.add_argument('--nt',   dest='nametag', help='nametag', default=None)
args = parser.parse_args()

bkgs = ['ttbar','qcd']
sigs = ['nmssm']
data = ['data_obs']

bkg_colors = [ROOT.kBlue-7, ROOT.kGreen+1, ROOT.kRed+1, ROOT.kCyan]
sig_colors = [ROOT.kMagenta, ROOT.kMagenta-9]

fIn = ROOT.TFile.Open(args.file)
bkg_histos  = [fIn.Get(histo_name(args.var, args.sel, s, args.nametag)) for s in bkgs]
sig_histos  = [fIn.Get(histo_name(args.var, args.sel, s, args.nametag)) for s in sigs]
data_histos = [fIn.Get(histo_name(args.var, args.sel, d, args.nametag)) for d in data]
data_histo  = data_histos[0]

print('.... read', len(bkg_histos), 'bkg histos')
print('.... read', len(sig_histos), 'sig histos')
print('.... read', len(data_histos), 'data histos')

for ib, b in enumerate(bkg_histos):
    b.SetLineColor(bkg_colors[ib])
    b.SetFillColor(bkg_colors[ib])

sig_max = 0
for isig, sig in enumerate(sig_histos):
    sig.SetLineColor(sig_colors[isig])
    sig.SetLineWidth(3)
    sig.SetFillColor(0)
    if sig.GetMaximum() > sig_max: sig_max = sig.GetMaximum()

data_histo.SetLineColor(ROOT.kBlack)
data_histo.SetMarkerColor(ROOT.kBlack)
data_histo.SetMarkerSize(0.8)
data_histo.SetMarkerStyle(8)

bkg_stack = ROOT.THStack('bkg_stack', ';{};Events'.format(args.var))
for b in bkg_histos:
    bkg_stack.Add(b)

## build the error histogram
bkg_err = bkg_stack.GetStack().Last().Clone('bkg_err')
bkg_err.SetFillColor(ROOT.kGray+3)
bkg_err.SetFillStyle(3008)
bkg_err.SetMarkerStyle(0)
bkg_err.SetMarkerSize(0)

c1 = ROOT.TCanvas('c1', 'c1', 600, 600)
c1.SetFrameLineWidth(3)

mmaxs = max([bkg_stack.GetMaximum(), data_histo.GetMaximum(), sig_max])
bkg_stack.SetMaximum(1.15*mmaxs)
bkg_stack.Draw('hist')
bkg_err.Draw('E2 same')

for sig in sig_histos:
    sig.Draw('hist same')

data_histo.Draw('pe same')

c1.BuildLegend()

oname = 'plot_{}_{}.pdf'.format(args.sel, args.var) if not args.nametag else 'plot_{}_{}_{}.pdf'.format(args.sel, args.var, args.nametag)
c1.Print('plots/'+oname, 'pdf')

oname = oname.replace('.pdf','.png')
c1.Print('plots/'+oname, 'png')
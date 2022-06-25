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
data = ['data_obs']

colors = [ROOT.kBlue-7, ROOT.kGreen+1, ROOT.kRed+1, ROOT.kCyan]

fIn = ROOT.TFile.Open(args.file)
bkg_histos  = [fIn.Get(histo_name(args.var, args.sel, s, args.nametag)) for s in bkgs]
data_histos = [fIn.Get(histo_name(args.var, args.sel, d, args.nametag)) for d in data]
data_histo  = data_histos[0]

print('.... read', len(bkg_histos), 'bkg histos')
print('.... read', len(data_histos), 'data histos')

for ib, b in enumerate(bkg_histos):
    b.SetLineColor(colors[ib])
    b.SetFillColor(colors[ib])
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

mmaxs = max([bkg_stack.GetMaximum(), data_histo.GetMaximum()])
bkg_stack.SetMaximum(1.15*mmaxs)
bkg_stack.Draw('hist')
bkg_err.Draw('E2 same')
data_histo.Draw('pe same')

oname = 'plot_{}_{}.pdf'.format(args.sel, args.var) if not args.nametag else 'plot_{}_{}_{}.pdf'.format(args.sel, args.var, args.nametag)
c1.Print(oname, 'pdf')

oname = oname.replace('.pdf','.png')
c1.Print(oname, 'png')
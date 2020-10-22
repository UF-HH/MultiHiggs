import ROOT
from array import array
import numpy as np
import matplotlib.pyplot as plt

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

# note : this runs on a special skim where all events are kept (no "continue" statements based on reco jets conditions or triggers)

sigs = [
    'NMSSM_XYH_YToHH_6b_MX_600_MY_400',
    'NMSSM_XYH_YToHH_6b_MX_500_MY_300',
    'NMSSM_XYH_YToHH_6b_MX_700_MY_500',
    'NMSSM_XYH_YToHH_6b_MX_450_MY_300',
    'NMSSM_XYH_YToHH_6b_MX_600_MY_300',
    'NMSSM_XYH_YToHH_6b_MX_700_MY_300',
    'NMSSM_XYH_YToHH_6b_MX_700_MY_400',
]

masses = {
    'NMSSM_XYH_YToHH_6b_MX_600_MY_400' : (600, 400),
    'NMSSM_XYH_YToHH_6b_MX_500_MY_300' : (500, 300),
    'NMSSM_XYH_YToHH_6b_MX_700_MY_500' : (700, 500),
    'NMSSM_XYH_YToHH_6b_MX_450_MY_300' : (450, 300),
    'NMSSM_XYH_YToHH_6b_MX_600_MY_300' : (600, 300),
    'NMSSM_XYH_YToHH_6b_MX_700_MY_300' : (700, 300),
    'NMSSM_XYH_YToHH_6b_MX_700_MY_400' : (700, 400),
}

fIns = {n : '../../' + n + '.root' for n in sigs}
effs = {}

for s in sigs:
    fIn = ROOT.TFile.Open(fIns[s])
    tIn = fIn.Get('sixBtree')
    nTot = tIn.GetEntries()
    nPass = tIn.GetEntries("gen_HX_b1_recojet_pt > 20 && gen_HX_b2_recojet_pt > 20 && gen_HY1_b1_recojet_pt > 20 && gen_HY1_b2_recojet_pt > 20 && gen_HY2_b1_recojet_pt > 20 && gen_HY2_b2_recojet_pt > 20 && gen_bs_N_reco_match == 6")
    # nPass = tIn.GetEntries("gen_HX_b1_recojet_pt > 20 && gen_HX_b2_recojet_pt > 20 && gen_HY1_b1_recojet_pt > 20 && gen_HY1_b2_recojet_pt > 20 && gen_HY2_b1_recojet_pt > 20 && gen_HY2_b2_recojet_pt > 20")
    effs[s] = 1.*nPass/nTot

for s in sigs:
    print '{:<35} : {:.1f}%'.format(s, 100.*effs[s])

## make a scatter eff plot
x_vals = sorted(list(set([x[0] for x in masses.values()])))
y_vals = sorted(list(set([x[1] for x in masses.values()])))

x_bins = x_vals
y_bins = y_vals
x_bins.append(x_vals[-1] + 1.0 * (x_vals[-1] - x_vals[-2]))
y_bins.append(y_vals[-1] + 1.0 * (y_vals[-1] - y_vals[-2]))

h_effs = ROOT.TH2D('h_effs', ';m_{X} [GeV];m_{Y} [GeV];#varepsilon', len(x_bins)-1,  array('d', x_bins), len(y_bins)-1, array('d', y_bins))
for ix, mx in enumerate(x_vals):
    ibinx = h_effs.GetXaxis().FindBin(mx)
    for iy, my in enumerate(y_vals):
        ibiny = h_effs.GetYaxis().FindBin(my)
        key = 'NMSSM_XYH_YToHH_6b_MX_%i_MY_%i' % (mx, my)
        if key in effs:
            h_effs.SetBinContent(ibinx, ibiny, effs[key])

c1 = ROOT.TCanvas('c1', 'c1', 600, 600)
c1.SetRightMargin(0.13)
h_effs.Draw('colz text')

## also print a marker for every actual point
markers = []
for m in masses.values():
    mrk = ROOT.TMarker(m[0], m[1], 8)
    mrk.SetNDC(False)
    mrk.SetMarkerSize(1.5)
    mrk.SetMarkerColor(ROOT.kBlack)
    markers.append(mrk)
for mrk in markers:
    mrk.Draw()

## and small arrows to indicate the direction
arrs = []
arrlen = 20.
for m in masses.values():
    arr = ROOT.TArrow(m[0]+arrlen, m[1]+arrlen, m[0]+3, m[1]+3, 0.03, '|>')
    arr.SetLineColor(ROOT.kBlack)
    arr.SetNDC(False)
    arrs.append(arr)
for arr in arrs:
    arr.Draw()


c1.Print('effs_2d.pdf', 'pdf')

# x_vals = np.asarray(x_vals)
# y_vals = np.asarray(y_vals)

# effs_array = np.zeros((x_vals.shape[0],y_vals.shape[0]))
# for ix, mx in enumerate(x_vals):
#     for iy, my in enumerate(y_vals):
#         key = 'NMSSM_XYH_YToHH_6b_MX_%i_MY_%i' % (mx, my)
#         eff = 0 if not key in effs else effs[key]
#         effs_array[ix][iy] = eff
# print effs_array

# # plt.plot(effs_array, cmap='hot')
# # plt.savefig('effs_2d.pdf')
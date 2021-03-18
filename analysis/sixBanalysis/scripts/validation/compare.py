# python compare.py  --file output/validation_VBF_SM_HH_2016MC.root --ref reference/ref_VBF_SM_HH_2016MC.root

import ROOT
import argparse
import collections
import math
from plotutils import plotMaker

ROOT.gROOT.SetBatch(True)
ROOT.gErrorIgnoreLevel = ROOT.kWarning

def has_nonzero_bins(h):
    nbins = h.GetNbinsX()
    for i in range(0, nbins+1):
        if h.GetBinContent(i) != 0:
            return True
    return False

parser = argparse.ArgumentParser('command line options')
parser.add_argument('--file', dest='file', help='The file to run the validation on', required=True)
parser.add_argument('--ref',  dest='ref',  help='The reference file to compare to',  required=True)
args = parser.parse_args()

f_this = ROOT.TFile.Open(args.file)
f_ref  = ROOT.TFile.Open(args.ref)

t_this = f_this.Get('sixBtree')
t_ref  = f_ref.Get('sixBtree')

### 1) compare N entries #####################################################
n_this = t_this.GetEntries()
n_ref = t_ref.GetEntries()

entries_check = 'OK' if n_this == n_ref else 'BAD'
print "[{ec:<3}] ... N entries check (this={n1} vs ref={n2})".format(ec=entries_check, n1=n_this, n2=n_ref)

### 2) compare the list of branches ###########################################
br_this = [x.GetName() for x in t_this.GetListOfBranches()]
br_ref  = [x.GetName() for x in t_ref.GetListOfBranches()]

in_this_not_in_ref = [x for x in br_this if x not in br_ref]
in_ref_not_in_this = [x for x in br_ref if x not in br_this]
common             = [x for x in br_ref if x in br_this]

branch_check = 'OK' if len(in_this_not_in_ref) == 0 and len(in_ref_not_in_this) == 0 else 'BAD'
print "[{ec:<3}] ... branches check".format(ec=branch_check, n1=n_this, n2=n_ref)
print "      ......... {} in this, not in ref: ".format(len(in_this_not_in_ref)), in_this_not_in_ref
print "      ......... {} in ref,  not in this: ".format(len(in_ref_not_in_this)), in_ref_not_in_this

### 3) compare the content ###################################################
c1 = ROOT.TCanvas()
# c1.SetLogy(True)
c1.cd()
pad1 = ROOT.TPad ("pad1", "pad1", 0, 0.25, 1, 1.0)
pad1.SetFrameLineWidth(3)
pad1.SetLeftMargin(0.15);
pad1.SetBottomMargin(0.02);
pad1.SetTopMargin(0.055);
# pad1.Draw()
pad1.SetLogy(True)

c1.cd()
pad2 = ROOT.TPad ("pad2", "pad2", 0, 0.0, 1, 0.2496)
pad2.SetLeftMargin(0.15);
pad2.SetTopMargin(0.05);
# pad2.SetBottomMargin(0.35);
pad2.SetBottomMargin(0.35);
pad2.SetGridy(True);
pad2.SetFrameLineWidth(3)
# pad2.Draw()

c1.cd()

ROOT.SetOwnership(c1, False)
ROOT.SetOwnership(pad1, False)
ROOT.SetOwnership(pad2, False)

histos = collections.OrderedDict()
for vname in common:
    vmin  = t_ref.GetMinimum(vname)
    vmax  = t_ref.GetMaximum(vname)
    delta = abs(vmax-vmin)
    if delta == 0: # identical variables
        delta = 1 ## just set a rndm range
    xmin  = vmin - 0.1*delta
    xmax  = vmax + 0.1*delta
    histos[vname] = {
        'name'  : vname,
        'title' : '%s;%s;Events' % (vname,vname),
        'expr'  : vname,
        'nbins' : 100,
        'xmin'  : xmin,
        'xmax'  : xmax,
    }
# print len(histos)
# print '... start'

#### check that the contents are correctly filled - boundaries must make sens
wrong_boundaries = []
for hname, hparams in histos.items():
    if math.isnan(hparams['xmin']) or math.isnan(hparams['xmax']) or math.isinf(hparams['xmin']) or math.isinf(hparams['xmax']):
        wrong_boundaries.append(hname)
        hparams['xmin'] = 0 ## dummy values
        hparams['xmax'] = 1 ## dummy values

vals_check = 'OK' if len(wrong_boundaries) == 0 else 'BAD'
print "[{ec:<3}] ... content check".format(ec=vals_check)
print "      ......... {} variables appear to have undefined max/min: ".format(len(wrong_boundaries)), wrong_boundaries

#### make the plots to compare the content

pm_ref          = plotMaker.plotMaker()
pm_ref.tag      = 'ref'
pm_ref.msg_head = "        %s >> " % pm_ref.tag
pm_ref.verb     = 1
pm_ref.c1       = c1
pm_ref.load_histos(histos)
pm_ref.build_histos(t_ref)

pm_this          = plotMaker.plotMaker()
pm_this.tag      = 'this'
pm_this.msg_head = "        %s >> " % pm_this.tag
pm_this.verb     = 1
pm_this.c1       = c1
pm_this.load_histos(histos)
pm_this.build_histos(t_this)

overlays = {}
for h in histos:
    overlays[h] = {
        'parts'   : ['ref_' + h, 'this_' + h],
        'leg'     : {
            'ref_'  + h : 'reference',
            'this_' + h : 'this',
        },
        'styles'     : {
            'ref_'  + h : 'line',
            'this_' + h : 'dots',
        },
        'title'         : histos[h]['title'],
        'compare'       : 'norm', ## diff or ratio or norm (this-ref)/ref
        'target'        : 'ref_'  + h, ## the destination of the comparison
    }

pm_comp          = plotMaker.plotMaker()
pm_comp.tag      = 'comp'
pm_comp.msg_head = "        %s >> " % pm_comp.tag
pm_comp.verb     = 1
pm_comp.c1       = c1
pm_comp.pad1     = pad1
pm_comp.pad2     = pad2
pm_comp.merge(pm_this)
pm_comp.merge(pm_ref)
pm_comp.set_overlays(overlays)
pm_comp.plot_name_proto = 'plots/{hname}.pdf'
pm_comp.plot_all(do_pdf=True)

print '... done'

## check all the histos that have a non-0 bin
diff_histos = []
for h in histos:
    h_diff = pm_comp.bottom_diffs[h][0]
    if has_nonzero_bins(h_diff):
        diff_histos.append(h)

distr_check = 'OK' if len(diff_histos) == 0 else 'BAD'
print "[{ec:<3}] ... variable distribution check".format(ec=distr_check)
print "      ......... {} variables appear to be difference: ".format(len(diff_histos)), diff_histos

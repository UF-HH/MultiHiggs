# from a new shell
# . /cvmfs/sft.cern.ch/lcg/views/LCG_100/x86_64-centos7-gcc8-opt/setup.sh

#### TO DO 
# - handle systematics
# - make documentation of what is created in each step
# - verify that weight = [] and weights = None do not impact data
# - add a function for debug run (small datasets loading?)

import ROOT
import modules.Sample as sam
import importlib
import argparse

ROOT.EnableImplicitMT()
ROOT.EnableThreadSafety()
ROOT.TH1.AddDirectory(False)

parser = argparse.ArgumentParser('Command line arguments for plotter')
parser.add_argument('--cfg',    dest='cfg',    help = 'config file for this plot', required=True)
parser.add_argument('--output', dest='output', help = 'output file name', required=True)
args = parser.parse_args()

print('... importing python config file', args.cfg)

spec = importlib.util.spec_from_file_location("cfg", args.cfg)
cfg  = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cfg)

# print(cfg.samples)

### declare the new functions to the interpreter
for expr in cfg.declarations:
    ROOT.gInterpreter.Declare(expr)

### declare the new columns to the samples
for cname, cexpr in cfg.new_columns.items():
    for s in cfg.samples:
        s.evt_sample.add_column(cname, cexpr)

# attach the selections to the samples
for s in cfg.samples:
      s.evt_sample.selections_defs = cfg.selections_defs

# make the histograms
for s in cfg.samples:
    s.do_histos(histos_descs=cfg.histos, norm_weights=cfg.norm_weights)

fOut = ROOT.TFile.Open(args.output, 'recreate')

for s in cfg.samples:
    s.write_histos(fOut)

for s in cfg.samples:
    s.print_end_summary()

for s in cfg.samples:
    if s.sampletype == 'mc':
        s.norm_sample.write_cache()
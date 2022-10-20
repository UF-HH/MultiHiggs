#!/usr/bin/env python
'''
# from a new shell
# . /cvmfs/sft.cern.ch/lcg/views/LCG_100/x86_64-centos7-gcc8-opt/setup.sh

#### TO DO 
# - handle systematics
# - make documentation of what is created in each step
# - verify that weight = [] and weights = None do not impact data
# - add a function for debug run (small datasets loading?)
'''
import ROOT
import modules.Sample as sam
import importlib
from argparse import ArgumentParser
import subprocess

ROOT.ROOT.EnableImplicitMT()
ROOT.ROOT.EnableThreadSafety()
ROOT.TH1.AddDirectory(False)

def main(args):
    
    spec = importlib.util.spec_from_file_location("cfg", args.cfg)
    cfg  = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cfg)
    
    # Declare the new functions to the interpreter
    for expr in cfg.declarations:
        ROOT.gInterpreter.Declare(expr)
        
    # Get the content of the tree
    if 0:
        for s in cfg.samples:
            s.evt_sample.GetContent()
        
    # Declare the new columns to the samples
    for cname, cexpr in cfg.new_columns.items():
        for s in cfg.samples:
            s.evt_sample.add_column(cname, cexpr)

    # Attach the selections to the samples
    for s in cfg.samples:
        s.evt_sample.selections_defs = cfg.selections_defs

    # make the histograms
    for s in cfg.samples:
        s.do_histos(histos_descs=cfg.histos, norm_weights=cfg.norm_weights)

    fOuts = []
    for i,s in enumerate(cfg.samples):
        out = "/tmp/%i_%i.root" % (i, hash(args.output))
        fOut = ROOT.TFile.Open(out, 'recreate')
        s.write_histos(fOut)
        fOuts.append(fOut)

    for s in cfg.samples:
        s.print_end_summary()

    for s in cfg.samples:
        if s.sampletype == 'mc':
            s.norm_sample.write_cache()

    def get_name(fOut):
        name = fOut.GetName()
        fOut.Close()
        return name

    outlist=' '.join([ get_name(fOut) for fOut in fOuts ])
    cmd = 'hadd -f '+args.output+' '+outlist
    subprocess.call(cmd, shell=True)
    cmd = 'rm '+outlist
    subprocess.call(cmd, shell=True)
    return

if __name__ == "__main__":
    
    # Default values
    VERBOSE   = 1
    TREENAME  = "sixBtree"
    
    parser = ArgumentParser(description="Histogrammer")
    
    parser.add_argument('--cfg',    dest='cfg',    help='config file for this plot', required=True)
    parser.add_argument('--output', dest='output', help='output file name', required=True)
    
    args = parser.parse_args()
    
    print("=== Importing python config file %s" % (args.cfg))
    main(args)

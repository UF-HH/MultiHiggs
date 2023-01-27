#!/usr/bin/env python

from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('-i','--input',required=True)
parser.add_argument('-p','--process',nargs='+', default=['qcd','ttbar'])
# parser.add_argument('-o','--output',default='tmp_bkg_model.root')

parser.add_argument('-v','--version',default=None)

args = parser.parse_args()

import ROOT, os


infile = ROOT.TFile.Open(args.input)

class Region:
    def __init__(self, indir, name):
        if args.version: name = args.version+'_'+name

        self.tdir = indir.GetDirectory(name)
        self.histos = {
            key.GetName():self.tdir.Get(key.GetName())
            for key in self.tdir.GetListOfKeys()
        }
    def __getitem__(self, key): return self.histos[key]
    def add(self, region):
        for histo in self.histos:
            self[histo].Add( region.histos[histo] )
    def integral(self):
        return max([ self[histo].Integral() for histo in self.histos ])
    def scale(self, value):
        for histo in self.histos:
            self[histo].Scale(value)
    def save(self, otdir, name):
        if args.version: name = args.version+'_'+name

        otdir.cd()
        tdir = otdir.mkdir(name)
        tdir.cd()
        for histo in self.histos:
            histo = self[histo].Clone()
            hname = [otdir.GetName(), name]+histo.GetTitle().split('_')[2:]
            hname = '_'.join(hname)
            histo.SetTitle(hname)
            histo.SetDirectory(tdir)
            histo.Write()

class Process:
    def __init__(self, infile, name):
        self.tdir = infile.GetDirectory(name)
        self.regions = { region:Region(self.tdir, region) for region in ('A','B','C','D') }
    def __getitem__(self, key): return self.regions[key]
    def add(self, proc):
        for region in self.regions:
            self[region].add(proc.regions[region])
    def save(self, otfile, name):
        otfile.cd()
        tdir = otfile.mkdir(name)
        self['B'].save(tdir, 'A')

processes = [ Process(infile, proc) for proc in args.process ]
process = processes[0]
for proc in processes[1:]:
    process.add(proc)

k_factor = process['C'].integral()/process['D'].integral()
print('C/D k_factor: ',k_factor)

process['B'].scale(k_factor)
ratio = process['B'].integral()/process['A'].integral()
print('k_factor*B/A: ',ratio)


tmp = '/tmp/%s.%s.root' % (args.input, hash(args.input))
otfile = ROOT.TFile(tmp,'recreate')
process.save(otfile,'bkg_model')

infile.Close()
otfile.Close()

os.system('rootmv %s:bkg_model %s' % (tmp, args.input))
os.system('rm %s' % tmp)
import glob
import ROOT
import subprocess

files = glob.glob('/eos/uscms/store/user/srosenzw/sixb/ntuples/Summer2018UL/maxbtag_4b/Official_NMSSM/*')
files.sort()
for f in files:
    if 'NMSSM' not in f.split('/')[-1]: continue
    rfile = ROOT.TFile.Open("{}/ntuple.root".format(f), "READ")
    if not rfile.GetListOfKeys().Contains("NormWeightTree"): 
        print "python scripts/submitSkimOnBatch.py --tag Summer2018UL/maxbtag_4b/Official_NMSSM/ --outputDir /store/user/srosenzw/sixb/ntuples --cfg config/skim_ntuple_2018_106X_NanoAODv9.cfg --njobs 100 --input input/Run2_UL/RunIISummer20UL18NanoAODv9/NMSSM_XToYHTo6B/{}.txt --is-signal --forceOverwrite --memory 4000".format(f.split('/')[-1])

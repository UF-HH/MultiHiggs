#!/usr/bin/env python
'''
DESCRIPTION:
Calculate the pile-up using pileupCalc for collision data.

Useful Links:
[1] https://twiki.cern.ch/twiki/bin/view/CMS/PileupJSONFileforData
[2] https://twiki.cern.ch/twiki/bin/view/CMS/PileupJSONFileforData#Centrally_produced_ROOT_histogra
[3] https://uscms.org/uscms_at_work/computing/LPC/usingEOSAtLPC.shtml
[4] https://uscms.org/uscms_at_work/computing/LPC/additionalEOSatLPC.shtml

PREREQUISITES:

1) If working at FNAL, you need to copy the appropriate pileup_latest.txt file locally to your working directory:

2018: /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/PileUp/UltraLegacy/pileup_latest.txt
2017: /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/PileUp/UltraLegacy/pileup_latest.txt
2016: /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/PileUp/UltraLegacy/pileup_latest.txt

2) pileupCalc.py needs cmsenv

USAGE:
./getPileup.py -d <directory in EOS> --year <year> --offsite --copyToEOS

LAST USED:
./getPileup.py -d /store/user/mkolosov/HHHTo6B/Summer2018UL_29Sep2022_withoutLeptonVeto --year 2018 --offsite --copyToEOS

COMMENTS:
 When running pileupCalc.py this message appears:

 Significant probability density outside of your histogram
 Consider using a higher value of --maxPileupBin, 
 Mean 48.639296, RMS 24.106512, Integrated probability 0.978179

 No changes when using higher value of maxPileupBin. Pileup distribution matches the centrally produced one located in [2].
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

def Verbose(msg, printHeader=False):
    '''
    Calls Print() only if verbose options is set to true.
    '''
    if not args.verbose:
        return
    print(msg)
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

PrimaryDatasets = ["BTagCSV", "BTagMu", "Charmonium", "Commissioning", "DisplacedJet", "DoubleEG", "DoubleMuon", "DoubleMuonLowMass", "HLTPhysics", 
                   "HTMHT", "JetHT", "MET", "MuOnia", "MuonEG", "SingleElectron", "SingleMuon", "SinglePhoton", "Tau", "ZeroBias"]
minBiasXsecNominal = 69200
NormTagJSON        = "/cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json" # covers all of Run 2 
PileUpJSON_2018    = "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/PileUp/pileup_latest.txt"
PileUpJSON_2017    = "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/PileUp/pileup_latest.txt"
PileUpJSON_2016    = "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/PileUp/pileup_latest.txt"

def CalcPileup(task, fOUT, inputFile, inputLumiJSON, minBiasXsec, calcMode="true", maxPileupBin="200", numPileupBins="200", pileupHistName="pileup", trigger=""):
    '''
    inputFile: the JSON file defining the lumi sections your analysis uses. This is generally the appropriate certification JSON file from PdmV or processedLumis.json from CRAB.
    inputLumiJSON: the appropriate pileup file for your analysis (central file)
    minBiasXsec: defines the minimum bias corss sectio to use (in microb). Run II recommendation is 69200.
    fOut: is the name of the output file
    '''
    cmd = "pileupCalc.py -i %s --inputLumiJSON %s --calcMode %s --minBiasXsec %s --maxPileupBin %s --numPileupBins %s --pileupHistName %s %s" % (inputFile, inputLumiJSON, calcMode, minBiasXsec, maxPileupBin, numPileupBins, pileupHistName, fOUT)
    return Execute(cmd)
    
def main(args):
    
    if args.year == "2016":
        PileUpJSON = PileUpJSON_2016
        LumiJSON   = "../data/lumi_cert/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt"
        if args.offsite:
            PileUpJSON = "pileup_latest.txt"
    elif args.year == "2017":
        PileUpJSON = PileUpJSON_2017
        LumiJSON   = "../data/lumi_cert/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt"
        if args.offsite:
            PileUpJSON = "pileup_latest.txt"
    elif args.year == "2018":
        PileUpJSON = PileUpJSON_2018
        LumiJSON   = "../data/lumi_cert/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt"
        if args.offsite:
            PileUpJSON = "pileup_latest.txt"
    else:
        raise Exception("Please provide the pileup file from '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/'")
    
    if args.offsite:
        if not os.path.exists("pileup_latest.txt"):
            raise Exception("You need to scp the %s file from LXPLUS afs, check the description for details." % (PileUpJSON))
    
    if (1):
        print("Using pileup file with name %s" % (PileUpJSON))
            
    cmd = "eos root://cmseos.fnal.gov find --childcount --maxdepth 1 -d" + " " + args.dirName
    dirContents = Execute(cmd)
    
    for count, d in enumerate(dirContents):
        
        # Skip the first directory, which is the args.dirName
        if count == 0 or "analysis_tar" in d:
            continue
            
        sampleName = d.split(args.dirName)[-1].split("/")[1]
        
        # Skip samples that are not Data
        if sampleName not in PrimaryDatasets:
            continue
        
        print("\nCalculating pileup distributions for data %s and year %s" % (sampleName, args.year))
        
        minBiasXS = minBiasXsecNominal
        print("\nCalculating nominal pileup distribution")
        ret = CalcPileup(sampleName, "PileUp.root", LumiJSON, PileUpJSON, minBiasXS, pileupHistName="pileup")
        print("Return =", ret)
        
        minBiasXSup = minBiasXsecNominal * (1 + args.pileupUnc)
        print("\nCalculating up pileup distribution")
        ret = CalcPileup(sampleName, "PileUp_up.root", LumiJSON, PileUpJSON, minBiasXSup, pileupHistName="pileup_up")
        print("Return =", ret)
        
        minBiasXSdown = minBiasXsecNominal * (1 - args.pileupUnc)
        print("\nCalculating down pileup distribution")
        ret = CalcPileup(sampleName, "PileUp_down.root", LumiJSON, PileUpJSON, minBiasXSdown, pileupHistName="pileup_down")
        print("Return =", ret)
        
        # Sanity check: the ROOT files are created and the histograms exist and are filled
        fPU      = ROOT.TFile.Open("PileUp.root", "UPDATE")
        fPU_up   = ROOT.TFile.Open("PileUp_up.root", "READ")
        fPU_down = ROOT.TFile.Open("PileUp_down.root", "READ")
        
        h_pu      = fPU.Get("pileup")
        h_pu_up   = fPU_up.Get("pileup_up")
        h_pu_down = fPU_down.Get("pileup_down")
        
        hList = []
        hList.append(h_pu)
        hList.append(h_pu_up)
        hList.append(h_pu_down)
        for h in hList:
            print("Histogram %s (xMin=%s, xMax=%s) has %s entries (mean=%s, RMS=%s)" % (h.GetName(), h.GetXaxis().GetXmin(), h.GetXaxis().GetXmax(), h.GetEntries(), h.GetMean(), h.GetRMS() ) )
            
        print("Task %s, writing Up/Down Pileup ROOT histos to %s file" % (sampleName, fPU.GetName()))
        fPU.cd()
        h_pu_up.Write()
        h_pu_down.Write()
        
        Verbose("Task %s, closing Pileup ROOT files" % (sampleName) )
        fPU.Close()
        fPU_up.Close()
        fPU_down.Close()
        
        # Save ROOT files names
        rList = [fPU.GetName(), fPU_up.GetName(), fPU_down.GetName()]
        
        # Copy fPU to EOS under the sample directory
        if args.copyToEOS:
            cmd = "xrdcp PileUp.root root://cmseos.fnal.gov/%s/%s/PileUp.root" % (args.dirName, sampleName)
            ret = Execute(cmd)
            print("Return =", ret)
        
            # Check if the file is copied
            cmd = "eos root://cmseos.fnal.gov ls %s/%s/PileUp.root" % (args.dirName, sampleName)
            ret = Execute(cmd)
            print("Return =", ret)
            
    return

if __name__ == "__main__":

    # Default values
    VERBOSE       = True
    DIRNAME       = "/store/user/mkolosov/HHHTo6B/Summer2018UL_29Sep2022_withoutLeptonVeto"
    OVERWRITE     = False
    YEAR          = None
    OFFSITE       = True
    PUUNCERTAINTY = 0.05
    COPYTOEOS     = False
    
    parser = ArgumentParser(description="Save ROOT files location in .txt")
    
    parser.add_argument("-v", "--verbose", dest="verbose", default=VERBOSE, action="store_true", help="Verbose mode for debugging purposes [default: %s]" % (VERBOSE))
    parser.add_argument("-d", "--dir", dest="dirName", type=str, action="store", default=DIRNAME, help="Location of the samples (a directory above) [default: %s]" % (DIRNAME))
    parser.add_argument("--overwrite", dest="overwrite", action="store_true", default=OVERWRITE, help="Overwrite .txt files [default: %s]" % (OVERWRITE))
    parser.add_argument("--year", dest="year", action="store", default=YEAR, help="The year to use")
    parser.add_argument("--offsite", dest="offsite", action="store_true", default=OFFSITE, help="Running pileupCalc from FNAL [default: %s]" % (OFFSITE))
    parser.add_argument("--puUnc", dest="pileupUnc", action="store", default=PUUNCERTAINTY, help="Pileup uncertainty [default: %s]" % (PUUNCERTAINTY))
    parser.add_argument("--copyToEOS", dest="copyToEOS", action="store_true", default=COPYTOEOS, help="Copy ROOT file to EOS [default: %s]" % (COPYTOEOS))
    
    args = parser.parse_args()

    HostName = GetHostname()
    if "fnal.gov" in HostName:
        args.offsite = True
    elif "lxplus.cern.ch" in HostName:
        args.offsite = False
    else:
        args.offsite = True

    if args.year == None:
        raise Exception("Must provide the year to process")
    
    if args.dirName == "":
        raise Exception("Must provide a location of the samples with the -d option.")
    else:
        main(args)

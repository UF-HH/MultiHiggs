#!/usr/bin/env python3
'''
DESCRIPTION:
This script is used to retrieve the list of ROOT files for each sample from DAS.

USAGE:
./getSamplesFromDAS.py

PREREQUISITES:
Before using the script, one needs to create a proxy with the command below:
voms-proxy-init -voms cms -rfc

USEFUL LINKS:
https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookLocatingDataSamples
https://uscms.org/uscms_at_work/computing/LPC/usingEOSAtLPC.shtml
https://uscms.org/uscms_at_work/computing/LPC/additionalEOSatLPC.shtml
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

def WriteFile(filename, rootfiles):
    '''
    Creates a new .txt file and stores the paths of all ROOT files.
    '''
    with open(filename, 'w') as f:
        for rf in rootfiles:
            f.write(rf)
            f.write("\n")
        f.close()
    return

def CreateList(args):
    '''
    Create a list of all the signal samples
    '''
    Verbose("CreateList()", True)
    
    if args.usage:
        cmd = "dasgoclient -help"
        exe = Execute(cmd)
        for count, d in enumerate(exe):
            print(d)

    # Get all samples:
    if args.allowInProduction:
        cmd = 'dasgoclient -query="dataset status=* dataset=/NMSSM_XToYHTo6B_MX-*_MY-*_TuneCP5_13TeV-madgraph-pythia8/%s*/*NANO*"' % (args.campaign)
    else:
        cmd = 'dasgoclient -query="dataset status=VALID dataset=/NMSSM_XToYHTo6B_MX-*_MY-*_TuneCP5_13TeV-madgraph-pythia8/%s*/*NANO*"' % (args.campaign)
    exe = Execute(cmd)
    for count, sample in enumerate(exe):
                
        sampleName = sample.split("/")[1]
        print(count, " ", sample, "   sampleName = ", sampleName)
        
        cmd = 'dasgoclient -query="file dataset=%s"' % (sample)
        files = Execute(cmd)
        rootfiles = []
        for i, rfile in enumerate(files):
            rootfiles.append("".join([args.redirector, rfile]))
            
        filename = "".join([sampleName, ".txt"])
        fileExists = os.path.exists(filename)
        if fileExists:
            if args.overwrite:
                Verbose("Will overwrite file %s" % (filename), True)
                WriteFile(filename, rootfiles)
            else:
                Verbose("File %s exists, will not overwrite" % (filename), True)
        else:
            WriteFile(filename, rootfiles)
    
    return

if __name__ == "__main__":

    # Default values
    VERBOSE           = True
    DATASET           = "NMSSM_XToYHTo6B_MX-*_MY-*_TuneCP5_13TeV-madgraph-pythia8"
    CAMPAIGN          = "RunIISummer20UL18"
    REDIRECTOR        = "root://cmsxrootd.fnal.gov/"
    OVERWRITE         = False
    USAGE             = False
    ALLOWINPRODUCTION = False
    
    parser = ArgumentParser(description="Save ROOT files location in .txt")
    
    parser.add_argument("-v", "--verbose", dest="verbose", default=VERBOSE, action="store_true", help="Verbose mode for debugging purposes [default: %s]" % (VERBOSE))
    parser.add_argument("-d", "--dataset", dest="dataset", type=str, action="store", default=DATASET, help="Dataset name on DAS [default: %s]" % (DATASET))
    parser.add_argument("-c", "--campaign", dest="campaign", action="store", type=str, default=CAMPAIGN, help="The production campaign [default: %s]" % (CAMPAIGN))
    parser.add_argument("--overwrite", dest="overwrite", action="store_true", default=OVERWRITE, help="Overwrite .txt files [default: %s]" % (OVERWRITE))
    parser.add_argument("--usage", dest="usage", action="store_true", default=USAGE, help="Print the usage of dasgoclient [default: %s]" % (USAGE))
    parser.add_argument("--redirector", dest="redirector", action="store", type=str, default=REDIRECTOR, help="Redirector to read files [default: %s]" % (REDIRECTOR))
    parser.add_argument("--allowInProduction", dest="allowInProduction", action="store_true", default=ALLOWINPRODUCTION, help="Allow to save files in production [default: %s]" % (ALLOWINPRODUCTION))
    
    args = parser.parse_args()
    
    if args.dataset == "":
        raise Exception("Must provide the dataset name on DAS with the -d option.")
    else:
        CreateList(args)

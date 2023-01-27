#!/usr/bin/env python
'''
DESCRIPTION:
This script is used to merge (hadd) the list of ROOT files for each sample

USAGE:
./mergeSamples.py -d /store/user/mkolosov/HHHTo6B/Summer2018UL_29Sep2022_withoutLeptonVeto

Useful Links:
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

def PrintSummary(reports):
    '''
    Print sample merging info
    '''
    Verbose("PrintSummary")
    
    table = []
    msgAlign = "{:<3} {:<60} {:^15} {:^10} {:^5}"
    header   = msgAlign.format("#", "Sample name", "Input Files", "Merged file", "Size")
    hLine    = "="*len(header)
    table.append("")
    table.append(hLine)
    table.append(header)
    table.append(hLine)
    
    for i, k in enumerate(reports.keys()):
        r = reports[k]
        table.append(msgAlign.format(i, r.dataset, r.nInputFiles, r.mergedFile, r.mergedFileSize))

    for l in table:
        print(l)
    return

class Report:
    def __init__(self, dataset):
        self.dataset     = dataset
        self.inputFiles  = []
        self.mergedFile  = "ntuple.root"
        
        cmd = "eos root://cmseos.fnal.gov find" + " " + "/".join([args.dirName, self.dataset])
        files = Execute(cmd)

        # Count the list of files to be merged
        for f in files:
            if "ntuple_" in f and ".root" in f:
                self.inputFiles.append(f)
                
        # Merge the files
        dest = "/".join([args.dirName, self.dataset, "output/"])
        cmd = "hadd %s `xrdfs root://cmseos.fnal.gov ls -u %s | grep '\.root'`" % (self.mergedFile, dest)
        merge = Execute(cmd)
        for i in merge:
            print(i)
        
        # Get the size of the file
        cmd = "ls -lh %s | awk '{print $5}'" % (self.mergedFile)
        size = Execute(cmd)
        
        cmd = "xrdcp %s " % (self.mergedFile) + "".join(["root://cmseos.fnal.gov/", args.dirName, "/", self.dataset, "/ntuple.root"])
        copy = Execute(cmd)
        for i in copy:
            print(i)
        
        # Delete the root file that was created locally
        cmd = "rm -rf %s" % (self.mergedFile)
        remove = Execute(cmd)
        for i in remove:
            print(i)
        
        self.nInputFiles    = len(self.inputFiles)
        self.mergedFileSize = size[0]
        return

def MergeSamples(args):
    '''
    Merge (hadd) the ROOT files of all samples under a given location
    '''
    Verbose("MergeSamples()", True)
    if "fnal.gov" in GetHostname():
        
        # This counts numbers of files in a directory
        cmd = "eos root://cmseos.fnal.gov find --childcount --maxdepth 1 -d" + " " + args.dirName
        Verbose(cmd)
        dirContents = Execute(cmd)
        
        taskReports = {}
        for count, d in enumerate(dirContents):
            
            # Skip the first directory, which is the args.dirName
            if count == 0 or "analysis_tar" in d:
                continue

            # Samples have the following structure: srosenzw_NMSSM_XYH_YToHH_6b_MX_900_MY_700_sl7_nano_100k (Keep it for now)
            sampleName = d.split(args.dirName)[-1].split("/")[1]
            taskReports[sampleName] = Report(sampleName)

        PrintSummary(taskReports)
    else:
        raise Exception("Hostname is not LPC. Fix needed for creating .txt files from LXPLUS.")
    return

if __name__ == "__main__":

    # Default values
    VERBOSE   = True
    DIRNAME   = "/store/user/mkolosov/HHHTo6B/Summer2018UL_29Sep2022_withoutLeptonVeto"
    OVERWRITE = False
    
    parser = ArgumentParser(description="Save ROOT files location in .txt")
    
    parser.add_argument("-v", "--verbose", dest="verbose", default=VERBOSE, action="store_true", help="Verbose mode for debugging purposes [default: %s]" % (VERBOSE))
    parser.add_argument("-d", "--dir", dest="dirName", type=str, action="store", default=DIRNAME, help="Location of the samples (a directory above) [default: %s]" % (DIRNAME))
    parser.add_argument("--overwrite", dest="overwrite", action="store_true", default=OVERWRITE, help="Overwrite .txt files [default: %s]" % (OVERWRITE))
    
    args = parser.parse_args()
    
    if args.dirName == "":
        raise Exception("Must provide a location of the samples with the -d option.")
    else:
        MergeSamples(args)

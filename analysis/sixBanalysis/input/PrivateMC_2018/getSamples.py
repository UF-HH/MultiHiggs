#!/usr/bin/env python3
'''
DESCRIPTION:
This script is used to retrieve the list of ROOT files for each sample.

USAGE:
./getSamples.py -d /eos/uscms/store/group/lpchbb/srosenzw/XYH_YToHH/CRAB_PrivateMC

 To overwrite existing .TXT files, do:
./getSamples.py -d /eos/uscms/store/group/lpchbb/srosenzw/XYH_YToHH/CRAB_PrivateMC --overwrite

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

def CreateList(args):
    '''
    Create a list of all the samples under a given location and save them in a .txt file
    '''
    Verbose("CreateList()", True)
    
    if "fnal.gov" in GetHostname():
        
        # This counts numbers of files in a directory
        cmd = "eos root://cmseos.fnal.gov find --childcount --maxdepth 1 -d" + " " + args.dirName
        Verbose(cmd)
        dirContents = Execute(cmd)
        
        for count, d in enumerate(dirContents):
            
            # Skip the first directory, which is the args.dirName
            if count == 0:
                continue
            
            # Samples have the following structure: srosenzw_NMSSM_XYH_YToHH_6b_MX_900_MY_700_sl7_nano_100k (Keep it for now)
            subdir = d.split(args.dirName)[-1].split("/")[1]
            print(subdir)
            
            # Find all files and directories under the
            cmd = "eos root://cmseos.fnal.gov find" + " " + "/".join([args.dirName, subdir])
            files = Execute(cmd)
            
            rootfiles = []
            for f in files:
                if "nanoAOD" in f and ".root" in f:
                    rfname = f.replace("/eos/uscms/", "root://cmseos.fnal.gov//")
                    rootfiles.append(rfname)
            
            filename = "".join([subdir, ".txt"])
            fileExists = os.path.exists(filename)
            if fileExists:
                if args.overwrite:
                    Verbose("Will overwrite file %s" % (filename), True)
                    WriteFile(filename, rootfiles)
                else:
                    Verbose("File %s exists, will not overwrite" % (filename), True)
            else:
                WriteFile(filename, rootfiles)
    else:
        raise Exception("Hostname is not LPC. Fix needed for creating .txt files from LXPLUS.")
    return

if __name__ == "__main__":

    # Default values
    VERBOSE   = True
    DIRNAME   = "/eos/uscms/store/group/lpchbb/srosenzw/XYH_YToHH/CRAB_PrivateMC"
    OVERWRITE = False
    
    parser = ArgumentParser(description="Save ROOT files location in .txt")
    
    parser.add_argument("-v", "--verbose", dest="verbose", default=VERBOSE, action="store_true", help="Verbose mode for debugging purposes [default: %s]" % (VERBOSE))
    parser.add_argument("-d", "--dir", dest="dirName", type=str, action="store", default=DIRNAME, help="Location of the samples (a directory above) [default: %s]" % (DIRNAME))
    parser.add_argument("--overwrite", dest="overwrite", action="store_true", default=OVERWRITE, help="Overwrite .txt files [default: %s]" % (OVERWRITE))
    
    args = parser.parse_args()
    
    if args.dirName == "":
        raise Exception("Must provide a location of the samples with the -d option.")
    else:
        CreateList(args)

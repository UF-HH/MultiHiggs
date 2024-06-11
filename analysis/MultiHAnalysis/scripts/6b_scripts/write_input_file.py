"""
This script will populate a text file with all ROOT files available in a given CRAB output directory.

# python3 write_input_file.py -a 6b --year 2018 --dir /store/user/srosenzw/path/to/files/######_######/
# python3 write_input_file.py --dir /store/group/lpchbb/srosenzw/XYH_YToHH/CRAB_PrivateMC/<NMSSM-file>/######_######/
"""

from argparse import ArgumentParser
import os
import re
import shlex
import subprocess
import sys

print(".. parsing argument line")
parser = ArgumentParser(description='Command line parser of model options and tags')
parser.add_argument('--year', dest='year', help='conditions of which year', default=2018)
parser.add_argument('--dir', dest='dir', help='CRAB output directory', required=True)
parser.add_argument('-a', '--analysis', dest='analysis', help='6b or 8b', default='6b')
args = parser.parse_args()

textfile = f"{re.search('(NMSSM_XYH_YToHH_.+)_sl7', args.dir).group(1)}.txt"

def exists_on_eos(lfn):
   """ check if lfn (starting with /store/group) exists """
   retcode = os.system('eos root://cmseos.fnal.gov ls -s %s > /dev/null 2>&1' % lfn)
   # print "THE FOLDER", lfn, "RETURNED CODE", retcode
   return True if retcode == 0 else False

outputName = f"input/PrivateMC/NMSSM_XYH_YToHH_{args.analysis}/Private_{args.year}/{textfile}"

with open(outputName, "w") as f:
   if (exists_on_eos(args.dir)):
      print(f".. writing to file: {outputName}")
      output = subprocess.check_output(shlex.split(f"eos root://cmseos.fnal.gov ls {args.dir}"))
      listOfDirs = output.decode("utf-8").split("\n")
      print(listOfDirs)
      for eachDir in listOfDirs:
         if eachDir != '':
               fullPath = args.dir + eachDir
               output = subprocess.check_output(["eos", "root://cmseos.fnal.gov", "ls", fullPath])
               listOfFiles = output.decode("utf-8").split("\n")
               for fileName in listOfFiles:
                  if fileName != '':
                     f.write(f"root://cmseos.fnal.gov/{fullPath}/{fileName}\n")
   else:
      print("[ERROR] Directory not found... Failed to write.")
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

dirName = args.dir
if dirName[-1] != '/': dirName = dirName + '/'
ending = [out for out in dirName.split('/') if 'MX_' in out][0].split('_')[-1]
if ending == '100k': ending = ''
elif ending == '500k': ending = ''
else: ending = '_' + ending

# find the desired file name, NMSSM_XYH_YToHH_6b_MX_###_MY_###
# Assumption: crab job was saved in the format
# srosenzw_NMSSM_XYH_YToHH_6b_MX_###_MY_###_sl7_nano_100k
start = re.search('NMSSM*',dirName).start()
end = re.search('_sl7',dirName).start()

textfile = f"{dirName[start:end]}{ending}.txt"

def exists_on_eos(lfn):
   """ check if lfn (starting with /store/group) exists """
   retcode = os.system('eos root://cmseos.fnal.gov ls -s %s > /dev/null 2>&1' % lfn)
   # print "THE FOLDER", lfn, "RETURNED CODE", retcode
   return True if retcode == 0 else False

outputName = f"input/PrivateMC_{args.year}/NMSSM_XYH_YToHH_{args.analysis}/{textfile}"
with open(outputName, "w") as f:
   if (exists_on_eos(dirName)):
      print(f".. writing to file: {outputName}")
      output = subprocess.check_output(shlex.split(f"eos root://cmseos.fnal.gov ls {dirName}"))
      listOfDirs = output.decode("utf-8").split("\n")
      print(listOfDirs)
      for eachDir in listOfDirs:
         if eachDir != '':
               fullPath = dirName + eachDir
               output = subprocess.check_output(["eos", "root://cmseos.fnal.gov", "ls", fullPath])
               listOfFiles = output.decode("utf-8").split("\n")
               for fileName in listOfFiles:
                  if fileName != '':
                     f.write(f"root://cmseos.fnal.gov/{fullPath}/{fileName}\n")
   else:
      print("[ERROR] Directory not found... Failed to write.")
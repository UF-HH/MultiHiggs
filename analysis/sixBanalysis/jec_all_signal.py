from argparse import ArgumentParser
from colorama import Fore, Style
import os
import re
import shlex
import subprocess
import sys

parser = ArgumentParser(description='Command line parser of model options and tags')

parser.add_argument('--jer-only', dest='jes', help='set jes to false', action='store_false', default=True)
parser.add_argument('--jes-only', dest='jer', help='set jer to false', action='store_false', default=True)
parser.add_argument('--eta', dest='eta', help='set eta to true', action='store_true', default=False)
parser.add_argument('--phi', dest='phi', help='set phi to true', action='store_true', default=False)
parser.add_argument('--pt',  dest='pt', help='set pt to true', action='store_true',   default=True)
parser.add_argument('--btag', dest='btag', action='store_true', default=False)
parser.add_argument('--bias', dest='bias', action='store_true', default=False)
parser.add_argument('--presel', dest='presel', action='store_true', default=False)

args = parser.parse_args()

if args.bias:
   extra = ''
   tag = 'bias'
if args.btag: 
   tag = 'btag'
   extra = '-b'

outfile="output.root"
cfg="config/skim_ntuple_2018.cfg"

jes_dict = {
   '2016' : '',
   '2017' : '',
   '2018' : 'data/jec/RegroupedV2_Summer19UL18_V5_MC_UncertaintySources_AK4PFchs.txt'
}

if args.jes:
   with open("data/jec/RegroupedV2_Summer19UL18_V5_MC_UncertaintySources_AK4PFchs.txt") as f:
      output = f.read()
      result = re.findall('\[(.*)\]', output, re.MULTILINE)
      print(result)
   systematics = result[:-1]
elif args.jer:
   systematics = ['']

N_syst = len(systematics)
print(systematics)
print("# systematics =",N_syst)

if args.jes and args.jer:
   N_syst += 1
elif args.jer and not args.jes:
   j = 0

if args.jes:
   prog_bar2 = '-'*N_syst + '>'
   with open("data/jec/RegroupedV2_Summer19UL18_V5_MC_UncertaintySources_AK4PFchs.txt") as f:
      output = f.read()
      result = re.findall('\[(.*)\]', output, re.MULTILINE)

   for j,systematic in enumerate(systematics):
      # if 'BBEC' not in systematic: continue
      prog_bar2 = '='*(j+1) + '-'*(N_syst-j-1) + '>'
      print(f"\n{Fore.CYAN}SYST PROGRESS{Style.RESET_ALL}",prog_bar2)
      print(systematic)
      devnull = open(os.devnull, 'w')
      print(".. submitting up jobs")
      cmd = f"sh scripts/submit_all_signal.sh {extra} --jes {systematic}:up -t {tag}/NMSSM/syst/{systematic}/up"
      subprocess.call(shlex.split(cmd))
      print(".. submitting down jobs")
      cmd = f"sh scripts/submit_all_signal.sh {extra} --jes {systematic}:down -t {tag}/NMSSM/syst/{systematic}/down"
      subprocess.call(shlex.split(cmd))

if args.jer:
   cmd = 'ls data/jer'
   output = subprocess.check_output(shlex.split(cmd))
   files = output.decode("utf-8").split('\n')
   if files[-1] == '': files = files[:-1]
   JER_files = [f for f in files if f.startswith('Summer19UL')]

   if args.eta: kin = 'Eta'
   elif args.phi: kin = 'Phi'
   elif args.pt: kin = 'Pt'
   else: raise("No kinematic provided!")

   for JER_file in JER_files:
      if kin in JER_file:
         prog_bar2 = '='*(j+1) + '-'*(N_syst-j-1) + '>'
         print(f"\n{Fore.CYAN}SYST PROGRESS{Style.RESET_ALL}",prog_bar2)
         print(kin)

         devnull = open(os.devnull, 'w')
         cmd = f"sh scripts/submit_all_signal.sh {extra} --jer up -t {tag}/NMSSM/syst/JER/{kin.lower()}/up"
         print(".. submitting up jobs")
         # subprocess.call(shlex.split(cmd), stdout=devnull, stderr=devnull)
         subprocess.call(shlex.split(cmd))
         # output = subprocess.check_output(shlex.split(cmd))
         # output = output.decode("utf-8").split('\n')
         # print(output)

         cmd = f"sh scripts/submit_all_signal.sh {extra} --jer down -t {tag}/NMSSM/syst/JER/{kin.lower()}/down"
         print(".. submitting down jobs")
         # subprocess.call(shlex.split(cmd), stdout=devnull, stderr=devnull)
         subprocess.call(shlex.split(cmd))
         # output = subprocess.check_output(shlex.split(cmd))
         # output = output.decode("utf-8").split('\n')
         # print(output)
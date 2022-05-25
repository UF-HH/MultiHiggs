from argparse import ArgumentParser
import re
import shlex
import subprocess
import sys

parser = ArgumentParser(description='Command line parser of model options and tags')

parser.add_argument('--jer-only', dest='jes', help='set jes to false', action='store_false', default=True)
parser.add_argument('--jes-only', dest='jer', help='set jer to false', action='store_false', default=True)
parser.add_argument('--eta', dest='eta', help='set eta to true', action='store_true', default=False)
parser.add_argument('--phi', dest='phi', help='set phi to true', action='store_true', default=False)
parser.add_argument('--pt',  dest='pt', help='set pt to true', action='store_true',   default=False)

args = parser.parse_args()

print(args.eta, args.phi, args.pt)

outfile="output.root"
infile="input/PrivateMC_2018/NMSSM_XYH_YToHH_6b/NMSSM_XYH_YToHH_6b_MX_700_MY_400.txt --is-signal"
cfg="config/skim_ntuple_2018.cfg"

if args.jes:
   with open("data/jec/RegroupedV2_Summer19UL18_V5_MC_UncertaintySources_AK4PFchs.txt") as f:
      output = f.read()
      result = re.findall('\[(.*)\]', output, re.MULTILINE)

   for systematic in result[:-1]:
      print(systematic)
      cmd = f"sh scripts/submit_all_signal.sh --jes {systematic}:up -t dHHH_pairs/NMSSM/syst/{systematic}/up"
      subprocess.call(shlex.split(cmd))
      cmd = f"sh scripts/submit_all_signal.sh --jes {systematic}:down -t dHHH_pairs/NMSSM/syst/{systematic}/down"
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
      if 'SF' in JER_file: continue
      if kin in JER_file:
         tag = f'dHHH_pairs/NMSSM/syst/JER/{kin.lower()}'

         cmd = f"sh scripts/submit_all_signal.sh --jer up -t {tag}/up"
         subprocess.call(shlex.split(cmd))
         cmd = f"sh scripts/submit_all_signal.sh --jer down -t {tag}/down"
         subprocess.call(shlex.split(cmd))

   
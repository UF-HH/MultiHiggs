from argparse import ArgumentParser
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
parser.add_argument('--pt',  dest='pt', help='set pt to true', action='store_true',   default=False)

args = parser.parse_args()

outfile="output.root"
cfg="config/skim_ntuple_2018.cfg"

sixb_base = "input/Run2_UL/RunIISummer20UL18NanoAODv9/NMSSM_XToYHTo6B/"
cmd = f"ls {sixb_base}"
output = subprocess.check_output(shlex.split(cmd))
files = output.decode("utf-8").split('\n')
if files[-1] == '': files = files[:-1]

if args.jes:
   with open("data/jec/RegroupedV2_Summer19UL18_V5_MC_UncertaintySources_AK4PFchs.txt") as f:
      output = f.read()
      result = re.findall('\[(.*)\]', output, re.MULTILINE)
      print(result)
   systematics = result[:-1]
elif args.jer:
   systematics = ['']

N_files = len(files)
print("# files =",N_files)
N_syst = len(systematics)
print("# systematics =",N_syst)
N_jobs = 0

if args.jes and args.jer:
   N_syst += 1
elif args.jer and not args.jes:
   j = 0

indir = 'input/PrivateMC_2018/NMSSM_XYH_YToHH_6b'
ODIR="/store/user/srosenzw/sixb/ntuples/Summer2018UL/"

prog_bar1 = '-'*N_files + '>'
for i,infile in enumerate(files):
   sample = infile.split('.')[0]
   print(infile)
   infile += " --is-signal"

   prog_bar1 = '='*(i+1) + '-'*(N_files-i-1) + '>'
   print("\nFILE PROGRESS", prog_bar1)

   if args.jes:
      prog_bar2 = '-'*N_syst + '>'
      with open("data/jec/2018/Summer19UL18_V5_MC_UncertaintySources_AK4PFchs.txt") as f:
         output = f.read()
         result = re.findall('\[(.*)\]', output, re.MULTILINE)

      for j,systematic in enumerate(systematics):
         if 'BBEC' not in systematic: continue
         prog_bar2 = '='*(j+1) + '-'*(N_syst-j-1) + '>'
         print("\nSYST PROGRESS",prog_bar2)
         print(systematic)
         devnull = open(os.devnull, 'w')
         print(".. submitting up jobs")
         cmd = f"python scripts/submitSkimOnBatch.py --tag {tag}/NMSSM/syst/{systematic}/up --outputDir {ODIR} --cfg {cfg} --njobs 100 --input {indir}/{infile} --is-signal --jes-shift-syst {systematic}:up --forceOverwrite"
         # subprocess.call(shlex.split(cmd), stdout=devnull, stderr=devnull)
         print(".. submitting down jobs")
         cmd = f"python scripts/submitSkimOnBatch.py --tag {tag}/NMSSM/syst/{systematic}/down --outputDir {ODIR} --cfg {cfg} --njobs 100 --input {indir}/{infile} --is-signal --jes-shift-syst {systematic}:down --forceOverwrite"
         # subprocess.call(shlex.split(cmd), stdout=devnull, stderr=devnull)

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
            print("\nSYST PROGRESS",prog_bar2)
            print(kin)
            Tag = f'{tag}/NMSSM/syst/JER/{kin.lower()}'

            devnull = open(os.devnull, 'w')
            # cmd = f"sh scripts/submit_all_signal.sh --jer up -t {tag}/up"
            cmd = f"python scripts/submitSkimOnBatch.py --tag {Tag}/up --outputDir {ODIR} --cfg {cfg} --njobs 100 --input {indir}/{infile} --is-signal --jer-shift-syst up --forceOverwrite"
            print(".. submitting up jobs")
            # subprocess.call(shlex.split(cmd), stdout=devnull, stderr=devnull)

            # cmd = f"sh scripts/submit_all_signal.sh --jer down -t {tag}/down"
            cmd = f"python scripts/submitSkimOnBatch.py --tag {Tag}/down --outputDir {ODIR} --cfg {cfg} --njobs 100 --input {indir}/{infile} --is-signal --jer-shift-syst down --forceOverwrite"
            print(".. submitting down jobs")
            # subprocess.call(shlex.split(cmd), stdout=devnull, stderr=devnull)

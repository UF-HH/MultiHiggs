from colorama import Fore, Style
import os
import re
import shlex
import subprocess
import sys
from argparse import ArgumentParser

parser = ArgumentParser(description='Command line parser of model options and tags')
parser.add_argument('--jer-only', dest='jer_only', help='conditions of which year', action='store_true', default=False)
args = parser.parse_args()

jer_only = args.jer_only

cfg="config/skim_ntuple_2018_106X_NanoAODv9.cfg"
sh_cmd="scripts/6b_scripts/submit_all_6b_signal.sh"

with open("data/jec/RegroupedV2_Summer19UL18_V5_MC_UncertaintySources_AK4PFchs.txt") as f:
   output = f.read()
   result = re.findall('\[(.*)\]', output, re.MULTILINE)
systematics = result[:-1]

print(f"[INFO] {', '.join(systematics)}")

input_dir = 'input/Run2_UL/RunIISummer20UL18NanoAODv9/NMSSM_XToYHTo6B'
cmd = f'ls {input_dir}'
output = subprocess.check_output(shlex.split(cmd)).decode('utf-8').split('\n')
output = [out for out in output if 'NMSSM' in out]
signals = [out for out in output if int(out.split('_')[2].split('-')[1]) < 1300]

try: subprocess.run("rm -r /eos/uscms/store/user/srosenzw/sixb/ntuples/Summer2018UL/maxbtag_4b/Official_NMSSM/syst/*/*/analysis_tar", shell=True)
except: pass

for signal in signals:
   # if '950_MY-250' not in signal: continue
   print(f"[INFO] Processing signal: {Fore.MAGENTA}{signal}{Style.RESET_ALL}")

   jer = "phi"

   print(f"[INFO] Processing systematic: {Fore.CYAN}JER/{jer}{Style.RESET_ALL}:up")
   tag = f'Summer2018UL/maxbtag_4b/Official_NMSSM/syst/JER{jer}/up'
   submit_cmd = f'python scripts/submitSkimOnBatch.py --tag {tag} --jer-shift-syst up --outputDir /store/user/srosenzw/sixb/ntuples --cfg config/skim_ntuple_2018_106X_NanoAODv9.cfg --njobs 100 --input {input_dir}/{signal} --is-signal --memory 4000 --forceOverwrite'
   print(f"{Style.DIM}{submit_cmd}{Style.RESET_ALL}")
   subprocess.run(shlex.split(submit_cmd))

   print(f"[INFO] Processing systematic: {Fore.CYAN}JER/{jer}{Style.RESET_ALL}:down")
   tag = f'Summer2018UL/maxbtag_4b/Official_NMSSM/syst/JER{jer}/down'
   submit_cmd = f'python scripts/submitSkimOnBatch.py --tag {tag} --jer-shift-syst down --outputDir /store/user/srosenzw/sixb/ntuples --cfg config/skim_ntuple_2018_106X_NanoAODv9.cfg --njobs 100 --input {input_dir}/{signal} --is-signal --memory 4000 --forceOverwrite'
   print(f"{Style.DIM}{submit_cmd}{Style.RESET_ALL}")
   subprocess.run(shlex.split(submit_cmd))

   if jer_only: sys.exit()

   print(f"[INFO] Processing systematic: {Fore.CYAN}bJER{Style.RESET_ALL}:up")
   tag = f'Summer2018UL/maxbtag_4b/Official_NMSSM/syst/bJER/up'
   submit_cmd = f'python scripts/submitSkimOnBatch.py --tag {tag} --bjer-shift-syst up --outputDir /store/user/srosenzw/sixb/ntuples --cfg config/skim_ntuple_2018_106X_NanoAODv9.cfg --njobs 100 --input {input_dir}/{signal} --is-signal --memory 4000 --forceOverwrite'
   print(f"{Style.DIM}{submit_cmd}{Style.RESET_ALL}")
   subprocess.run(shlex.split(submit_cmd))

   print(f"[INFO] Processing systematic: {Fore.CYAN}bJER{Style.RESET_ALL}:down")
   tag = f'Summer2018UL/maxbtag_4b/Official_NMSSM/syst/bJER/down'
   submit_cmd = f'python scripts/submitSkimOnBatch.py --tag {tag} --bjer-shift-syst down --outputDir /store/user/srosenzw/sixb/ntuples --cfg config/skim_ntuple_2018_106X_NanoAODv9.cfg --njobs 100 --input {input_dir}/{signal} --is-signal --memory 4000 --forceOverwrite'
   print(f"{Style.DIM}{submit_cmd}{Style.RESET_ALL}")
   subprocess.run(shlex.split(submit_cmd))


   for syst in systematics:
      if 'BBEC1' not in syst: continue
      print(f"[INFO] Processing systematic: {Fore.CYAN}{syst}{Style.RESET_ALL}:up")
      tag = f'Summer2018UL/maxbtag_4b/Official_NMSSM/syst/{syst}/up'
      submit_cmd = f'python scripts/submitSkimOnBatch.py --tag {tag} --jes-shift-syst {syst}:up --outputDir /store/user/srosenzw/sixb/ntuples --cfg config/skim_ntuple_2018_106X_NanoAODv9.cfg --njobs 100 --input {input_dir}/{signal} --is-signal --memory 4000 --forceOverwrite'
      print(f"{Style.DIM}{submit_cmd}{Style.RESET_ALL}")
      subprocess.run(shlex.split(submit_cmd))


      print(f"[INFO] Processing systematic: {Fore.CYAN}{syst}{Style.RESET_ALL}:down")
      tag = f'Summer2018UL/maxbtag_4b/Official_NMSSM/syst/{syst}/down'
      submit_cmd = f'python scripts/submitSkimOnBatch.py --tag {tag} --jes-shift-syst {syst}:down --outputDir /store/user/srosenzw/sixb/ntuples --cfg config/skim_ntuple_2018_106X_NanoAODv9.cfg --njobs 100 --input {input_dir}/{signal} --is-signal --memory 4000 --forceOverwrite'
      print(f"{Style.DIM}{submit_cmd}{Style.RESET_ALL}")
      subprocess.run(shlex.split(submit_cmd))
   
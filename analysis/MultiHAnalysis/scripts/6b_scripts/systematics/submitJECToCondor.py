# python3 scripts/6b_scripts/systematics/submitJECToCondor.py

from colorama import Fore, Style
import os
import re
import shlex
import subprocess
import sys
from argparse import ArgumentParser
from configparser import ConfigParser

year = '2018'

cfg = f"config/skim_ntuple_{year}_106X_NanoAODv9.cfg"
config = ConfigParser()
config.read(cfg)

parser = ArgumentParser(description='Command line parser of model options and tags')
parser.add_argument('--jer-only', dest='jer_only', help='conditions of which year', action='store_true', default=False)
args = parser.parse_args()

jer_only = args.jer_only

njobs = 50
memory = 4000
grid = 'voms-proxy-init --rfc --voms cms -hours 72'

sys_files = {
   '2018' : 'RegroupedV2_Summer19UL18_V5_MC_UncertaintySources_AK4PFchs.txt',
   '2017' : 'RegroupedV2_Summer19UL17_V5_MC_UncertaintySources_AK4PFchs.txt',
   '2016' : 'RegroupedV2_Summer19UL16_V7_MC_UncertaintySources_AK4PFchs.txt',
   '2016APV' : 'RegroupedV2_Summer19UL16APV_V7_MC_UncertaintySources_AK4PFchs.txt'
}

f_sys = f"data/jec/{year}/{sys_files[year]}"

with open(f_sys) as f:
   output = f.read()
   result = re.findall('\[(.*)\]', output, re.MULTILINE)
systematics = result[:-1]

print(f"[INFO] {', '.join(systematics)}")

input_dir = f'input/Run2_UL/RunIISummer20UL{year[2:]}NanoAODv9/NMSSM_XToYHTo6B'

cmd = f'ls {input_dir}'
output = subprocess.check_output(shlex.split(cmd)).decode('utf-8').split('\n')
output = [out for out in output if 'NMSSM' in out]
signals = [out for out in output if int(out.split('_')[2].split('-')[1]) < 1300]

try: subprocess.run(f"rm -r /eos/uscms/store/user/srosenzw/sixb/ntuples/Summer{year}UL/maxbtag_4b/Official_NMSSM/syst/*/*/analysis_tar", shell=True)
except: pass

# masses_to_run = ['MX-1000_MY-250']
masses_to_run = ['MX-400_MY-250']
masses_to_run += ['MX-450_MY-250', 'MX-450_MY-300']
masses_to_run += ['MX-500_MY-250', 'MX-500_MY-300', 'MX-500_MY-350']
masses_to_run += ['MX-550_MY-250', 'MX-550_MY-300', 'MX-550_MY-350', 'MX-550_MY-400']
masses_to_run += ['MX-600_MY-250', 'MX-600_MY-300', 'MX-600_MY-350', 'MX-600_MY-400', 'MX-600_MY-450']
masses_to_run += ['MX-650_MY-250', 'MX-650_MY-300', 'MX-650_MY-350', 'MX-650_MY-400', 'MX-650_MY-450', 'MX-650_MY-500']
masses_to_run += ['MX-700_MY-250', 'MX-700_MY-300', 'MX-700_MY-350', 'MX-700_MY-400', 'MX-700_MY-450', 'MX-700_MY-500']
masses_to_run += ['MX-750_MY-250', 'MX-750_MY-300', 'MX-750_MY-350', 'MX-750_MY-400', 'MX-750_MY-450', 'MX-750_MY-500', 'MX-750_MY-600']
masses_to_run += ['MX-800_MY-250', 'MX-800_MY-300', 'MX-800_MY-350', 'MX-800_MY-400', 'MX-800_MY-450', 'MX-800_MY-500', 'MX-800_MY-600']
masses_to_run += ['MX-850_MY-250', 'MX-850_MY-300', 'MX-850_MY-350', 'MX-850_MY-400', 'MX-850_MY-450', 'MX-850_MY-500', 'MX-850_MY-600', 'MX-850_MY-700']
masses_to_run += ['MX-900_MY-250', 'MX-900_MY-300', 'MX-900_MY-350', 'MX-900_MY-400', 'MX-900_MY-450', 'MX-900_MY-500', 'MX-900_MY-600', 'MX-900_MY-700']
masses_to_run += ['MX-950_MY-250', 'MX-950_MY-300', 'MX-950_MY-350', 'MX-950_MY-400', 'MX-950_MY-450', 'MX-950_MY-500', 'MX-950_MY-600', 'MX-950_MY-700', 'MX-950_MY-800']
masses_to_run += ['MX-1000_MY-250', 'MX-1000_MY-300', 'MX-1000_MY-350', 'MX-1000_MY-400', 'MX-1000_MY-450', 'MX-1000_MY-500', 'MX-1000_MY-600', 'MX-1000_MY-700', 'MX-1000_MY-800']
masses_to_run += ['MX-1100_MY-250', 'MX-1100_MY-300', 'MX-1100_MY-350', 'MX-1100_MY-400', 'MX-1100_MY-450', 'MX-1100_MY-500', 'MX-1100_MY-600', 'MX-1100_MY-700', 'MX-1100_MY-800', 'MX-1100_MY-900']
masses_to_run += ['MX-1200_MY-250', 'MX-1200_MY-300', 'MX-1200_MY-350', 'MX-1200_MY-400', 'MX-1200_MY-450', 'MX-1200_MY-500', 'MX-1200_MY-600', 'MX-1200_MY-700', 'MX-1200_MY-800', 'MX-1200_MY-900', 'MX-1200_MY-1000']

signals = [s for s in signals if re.search("(MX-\d+_MY-\d+)", s).group(1) in masses_to_run]

for signal in signals:
   print(f"[INFO] Processing signal: {Fore.MAGENTA}{signal}{Style.RESET_ALL}")

   # jer = re.search("MC_(.+)Resolution", config['parameters']['JERResolutionFile']).group(1).lower()

   # print(f"[INFO] Processing systematic: {Fore.CYAN}JER/{jer}{Style.RESET_ALL}:up")
   # tag = f'Summer2018UL/maxbtag_4b/Official_NMSSM/syst/JER{jer}/up'
   # submit_cmd = f'python scripts/submitSkimOnBatch.py --tag {tag} --jer-shift-syst up --outputDir /store/user/srosenzw/sixb/ntuples --cfg {cfg} --njobs {njobs} --input {input_dir}/{signal} --is-signal --memory {memory} --forceOverwrite'
   # print(f"{Style.DIM}{submit_cmd}{Style.RESET_ALL}")
   # subprocess.run(shlex.split(submit_cmd))

   # print(f"[INFO] Processing systematic: {Fore.CYAN}JER/{jer}{Style.RESET_ALL}:down")
   # tag = f'Summer2018UL/maxbtag_4b/Official_NMSSM/syst/JER{jer}/down'
   # submit_cmd = f'python scripts/submitSkimOnBatch.py --tag {tag} --jer-shift-syst down --outputDir /store/user/srosenzw/sixb/ntuples --cfg {cfg} --njobs {njobs} --input {input_dir}/{signal} --is-signal --memory {memory} --forceOverwrite'
   # print(f"{Style.DIM}{submit_cmd}{Style.RESET_ALL}")
   # subprocess.run(shlex.split(submit_cmd))

   # if jer_only: sys.exit()

   # print(f"[INFO] Processing systematic: {Fore.CYAN}bJER{Style.RESET_ALL}:up")
   # tag = f'Summer2018UL/maxbtag_4b/Official_NMSSM/syst/bJER/up'
   # submit_cmd = f'python scripts/submitSkimOnBatch.py --tag {tag} --bjer-shift-syst up --outputDir /store/user/srosenzw/sixb/ntuples --cfg {cfg} --njobs {njobs} --input {input_dir}/{signal} --is-signal --memory {memory} --forceOverwrite'
   # print(f"{Style.DIM}{submit_cmd}{Style.RESET_ALL}")
   # subprocess.run(shlex.split(submit_cmd))

   # print(f"[INFO] Processing systematic: {Fore.CYAN}bJER{Style.RESET_ALL}:down")
   # tag = f'Summer2018UL/maxbtag_4b/Official_NMSSM/syst/bJER/down'
   # submit_cmd = f'python scripts/submitSkimOnBatch.py --tag {tag} --bjer-shift-syst down --outputDir /store/user/srosenzw/sixb/ntuples --cfg {cfg} --njobs {njobs} --input {input_dir}/{signal} --is-signal --memory {memory} --forceOverwrite'
   # print(f"{Style.DIM}{submit_cmd}{Style.RESET_ALL}")
   # subprocess.run(shlex.split(submit_cmd))

   for syst in systematics:
      
      if syst != 'FlavorQCD': continue
      # if syst == 'Absolute_2018': continue

      print(f"[INFO] Processing systematic: {Fore.CYAN}{syst}{Style.RESET_ALL}:up")
      tag = f'Summer2018UL/maxbtag_4b/Official_NMSSM/syst/{syst}/up'
      submit_cmd = f'python scripts/submitSkimOnBatch.py --tag {tag} --jes-shift-syst {syst}:up --outputDir /store/user/srosenzw/sixb/ntuples --cfg {cfg} --njobs {njobs} --input {input_dir}/{signal} --is-signal --memory {memory} --forceOverwrite'
      print(f"{Style.DIM}{submit_cmd}{Style.RESET_ALL}")
      subprocess.run(shlex.split(submit_cmd))

      print(f"[INFO] Processing systematic: {Fore.CYAN}{syst}{Style.RESET_ALL}:down")
      tag = f'Summer2018UL/maxbtag_4b/Official_NMSSM/syst/{syst}/down'
      submit_cmd = f'python scripts/submitSkimOnBatch.py --tag {tag} --jes-shift-syst {syst}:down --outputDir /store/user/srosenzw/sixb/ntuples --cfg {cfg} --njobs {njobs} --input {input_dir}/{signal} --is-signal --memory {memory} --forceOverwrite'
      print(f"{Style.DIM}{submit_cmd}{Style.RESET_ALL}")
      subprocess.run(shlex.split(submit_cmd))
   
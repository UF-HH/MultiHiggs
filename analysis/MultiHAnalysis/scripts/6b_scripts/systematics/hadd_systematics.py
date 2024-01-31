from colorama import Fore, Style
import re
import shlex
import subprocess
import sys

base="/store/user/srosenzw/sixb/ntuples/Summer2018UL/maxbtag_4b/Official_NMSSM/syst"
eos="/eos/uscms{}".format(base)

with open("data/jec/RegroupedV2_Summer19UL18_V5_MC_UncertaintySources_AK4PFchs.txt") as f:
   output = f.read()
   result = re.findall('\[(.*)\]', output, re.MULTILINE)
systematics = result[:-1]
print("[INFO] {}".format(', '.join(systematics)))

input_dir = 'input/Run2_UL/RunIISummer20UL18NanoAODv9/NMSSM_XToYHTo6B'
cmd = 'ls {}'.format(input_dir)
output = subprocess.check_output(shlex.split(cmd)).decode('utf-8').split('\n')
output = [out for out in output if 'NMSSM' in out]
signals = [out for out in output if int(out.split('_')[2].split('-')[1]) < 1300]

def hadd_files(sig, syst, var):
   assert var == "up" or var == "down"
   cmd = "hadd -f ntuple.root `xrdfs root://cmseos.fnal.gov ls -u {}/{}/{}/{}/output | grep '\.root'`".format(base,syst,var,sig)
   print(".. hadding files into local dir")
   subprocess.call(cmd, shell=True)
   cmd = "xrdcp -f ntuple.root root://cmseos.fnal.gov/{}/{}/{}/{}/ntuple.root".format(base,syst,var,sig)
   print(".. copying file to eos")
   subprocess.call(cmd, shell=True)
   
for signal in signals:
   if '950_MY-250' not in signal: continue
   print("[INFO] Processing signal: {}{}{}".format(Fore.MAGENTA, signal, Style.RESET_ALL))
   sig = signal.replace(".txt", "")

   syst = "bJER"
   print("[INFO] Processing systematic: {}{}{}:up".format(Fore.CYAN, syst, Style.RESET_ALL))
   hadd_files(sig, syst, "up")
   print("[INFO] Processing systematic: {}{}{}:down".format(Fore.CYAN, syst, Style.RESET_ALL))
   hadd_files(sig, syst, "down")

   for syst in ["JERpt", "JEReta", "JERphi"]:
      if syst != "JERpt": continue
      print("[INFO] Processing systematic: {}{}{}:up".format(Fore.CYAN, syst, Style.RESET_ALL))
      hadd_files(sig, syst, "up")
      print("[INFO] Processing systematic: {}{}{}:down".format(Fore.CYAN, syst, Style.RESET_ALL))
      hadd_files(sig, syst, "down")

   for syst in systematics:
      cmd = "ls -l {}/{}/up/{}/ntuple.root".format(eos,syst,sig)
      output = subprocess.check_output(cmd, shell=True).decode('utf-8').split()
      # size = int(output[4])
      # if size == 0:
      print("[INFO] Processing systematic: {}{}{}:up".format(Fore.CYAN, syst, Style.RESET_ALL))
      hadd_files(sig, syst, "up")

      cmd = "ls -l {}/{}/down/{}/ntuple.root".format(eos,syst,sig)
      output = subprocess.check_output(cmd, shell=True).decode('utf-8').split()
      # size = int(output[4])
      # if size == 0:
      print("[INFO] Processing systematic: {}{}{}:down".format(Fore.CYAN, syst, Style.RESET_ALL))
      hadd_files(sig, syst, "down")

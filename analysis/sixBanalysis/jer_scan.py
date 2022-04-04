import re
import shlex
import subprocess

outfile="output.root"
infile="input/PrivateMC_2018/NMSSM_XYH_YToHH_6b/NMSSM_XYH_YToHH_6b_MX_700_MY_400.txt --is-signal"
cfg="config/skim_ntuple_2018.cfg"

with open("data/jec/RegroupedV2_Summer19UL18_V5_MC_UncertaintySources_AK4PFchs.txt") as f:
   output = f.read()
   result = re.findall('\[(.*)\]', output, re.MULTILINE)

for systematic in result[:-1]:
   print(systematic)
   cmd = f"sh scripts/submit_all_signal.sh -j {systematic}:up -t dHHH_pairs/NMSSM/syst/{systematic}/up"
   subprocess.call(shlex.split(cmd))
   cmd = f"sh scripts/submit_all_signal.sh -j {systematic}:down -t dHHH_pairs/NMSSM/syst/{systematic}/down"
   subprocess.call(shlex.split(cmd))
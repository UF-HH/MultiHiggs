import glob
import os
import random
import subprocess
import sys
from colorama import Fore, Style

year = "Summer2018UL"
fpath = f"/eos/uscms/store/user/srosenzw/sixb/ntuples/{year}/maxbtag_4b/Official_NMSSM/syst"

systs = glob.glob(f"{fpath}/*")

for i,syst in enumerate(systs):
    variations = glob.glob(f"{syst}/*")
    for j,var in enumerate(variations):
        masses = glob.glob(f"{var}/NMSSM*")
        for k,mass in enumerate(masses):
            print(f"{Fore.GREEN}[INFO] hadding {i+1}/{len(systs)}{Style.RESET_ALL} ".ljust(100,f'-'))
            print(f"{Fore.GREEN}[INFO] hadding {j+1}/{len(variations)}{Style.RESET_ALL} ".ljust(100,f'-'))
            print(f"{Fore.GREEN}[INFO] hadding {k+1}/{len(masses)}{Style.RESET_ALL} ".ljust(100,f'-'))
            # if os.path.exists(f"{mass}/ntuple.root"): continue
            dirname = mass.replace("/eos/uscms", "")
            print(dirname)
            rnum = random.getrandbits(32)
            print(f"[BEGIN] Hadding {mass}")
            cmd = f"hadd -f {rnum}.root `xrdfs root://cmseos.fnal.gov ls -u {dirname}/output | grep '\.root'`"
            print(f"{Style.DIM}{cmd}{Style.RESET_ALL}")
            print(".. hadding files into local dir")
            
            try: 
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
                print(f"output = {result.stdout}")

                cmd = f"xrdcp -f {rnum}.root root://cmseos.fnal.gov/{dirname}/ntuple.root"
                print(f"{Style.DIM}{cmd}{Style.RESET_ALL}")
                print(".. copying file to eos")
                subprocess.call(cmd, shell=True)

                subprocess.call(f"rm {rnum}.root", shell=True)
            except:
                print(f"{Fore.RED}[ERROR] {mass}{Style.RESET_ALL}")


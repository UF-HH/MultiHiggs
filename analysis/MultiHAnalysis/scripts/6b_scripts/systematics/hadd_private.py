from colorama import Fore, Style
import subprocess, shlex

# base="/store/user/srosenzw/sixb/ntuples/Summer2018UL/maxbtag_4b/Official_NMSSM"
base="/store/user/srosenzw/sixb/ntuples/Summer2018UL/maxbtag/NMSSM"
eos="/eos/uscms{}".format(base)

cmd = 'ls {}'.format(eos)
output = subprocess.check_output(shlex.split(cmd)).decode('utf-8').split('\n')
signals = [out for out in output if 'NMSSM' in out]

for signal in signals:
    print("[INFO] Processing signal: {}{}{}".format(Fore.MAGENTA, signal, Style.RESET_ALL))
    cmd = "hadd -f ntuple.root `xrdfs root://cmseos.fnal.gov ls -u {}/{}/output | grep '\.root'`".format(base,signal)
    print(".. hadding files into local dir")
    subprocess.call(cmd, shell=True)
    cmd = "xrdcp -f ntuple.root root://cmseos.fnal.gov/{}/{}/ntuple.root".format(base,signal)
    print(".. copying file to eos")
    subprocess.call(cmd, shell=True)


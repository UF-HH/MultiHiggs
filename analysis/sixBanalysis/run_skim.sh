#!/bin/sh

eval `scramv1 runtime -sh`
source scripts/setup.sh

# output="NMSSM_XYH_YToHH_6b_MX_700_MY_400_accstudies_500k_Jul2021-v2.root"
output="output-tree.root"

# --input input/Run2_UL/2018/QCD_Pt_600to800_TuneCP5_13TeV_pythia8.txt \
    
make exe -j && \
    bin/skim_ntuple.exe \
	--input input/PrivateMC_2021/NMSSM_XYH_YToHH_6b_MX_700_MY_400-v2.txt \
	--is-signal \
	--cfg config/skim_ntuple_2018.cfg \
	--output $output \
	$@

#!/bin/sh

eval `scramv1 runtime -sh`
source scripts/setup.sh

exe=bin/skim_ntuple_Run3.exe

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Run3 2022
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
cfg="config/skim_ntuple_HHTo4b_2022_PromptNanoAODv11.cfg"
input="input/Run3/2022/PrivateNano_JetMET_Run2022F_PromptReco_v1_22May2023.txt --is-data"
output="NTuple_Run3_2022_JetMET_Run2022F_PromptReco_v1_22May2023.root"

make exe -j && \
    $exe \
    --input $input \
    --cfg  $cfg \
    --output $output \
    $@

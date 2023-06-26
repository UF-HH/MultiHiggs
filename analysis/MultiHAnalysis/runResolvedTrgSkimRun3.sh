#!/bin/sh

exe=bin/skim_trigger_Run3.exe

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# 2022
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
cfg="config/skim_PNetHLT_2022_PromptNanoAODv11.cfg"

# Run 2022 Data
#output="Run3_MuonEG_2022F_PrivateNano_PromptReco_22May2023_TriggerEffMeasurement.root"
#input="input/Run3/2022/PrivateNano_MuonEG_Run2022F_PromptReco_v1_22May2023.txt --is-data"

output="TTto2L2Nu_TuneCP5_13p6TeV_powheg_pythia8_TriggerEffMeasurement.root"
input="input/Run3/2022/postEE/PrivateNano_TTto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8_08June2023.txt"

make exe -j && \
    $exe \
    --input $input \
    --cfg  $cfg \
    --output $output \
     --maxEvts 2000000 \
    $@

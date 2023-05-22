#!/bin/sh

exe=bin/skim_trigger_Run3.exe

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# 2022
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
cfg="config/skim_PNetHLT_2022_PromptNanoAODv11.cfg"

# Run 2022 Data
output="Run3_MuonEG_2022G_PrivateNano_PromptNanoAODv11_v1_v2_TrgStudies.root"
input="input/Run3/PrivateNano_MuonEG_Run2022EFG_PromptReco_EOS.txt"

make exe -j && \
    $exe \
    --input $input \
    --cfg  $cfg \
    --output $output \
    --is-data \
#    --maxEvts -1 \
    $@

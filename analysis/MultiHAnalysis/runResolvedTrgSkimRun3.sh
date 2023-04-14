#!/bin/sh

exe=bin/skim_trigger_Run3.exe

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# 2022
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#cfg="config/skim_trigger_2022_NanoAODv10.cfg"
cfg="config/skim_PNetHLT_2022_NanoAODv10.cfg"

# Run 2022 Data
output="Run3_MuonEG_2022G_TrgStudies.root"
input="input/Run3/MuonEG_Run2022G_v1-v2.txt"

make exe -j && \
    $exe \
    --input $input \
    --cfg  $cfg \
    --output $output \
    --is-data \
    --maxEvts 200000 \
    $@

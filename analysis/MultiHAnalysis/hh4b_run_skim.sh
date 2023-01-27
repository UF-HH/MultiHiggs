#!/bin/sh

# eval `scramv1 runtime -sh`
# source scripts/setup.sh

exe=bin/skim_ntuple.exe

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# 2018
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
cfg="config/skim_4b_ntuple_2018_102X_NanoAODv7.cfg"
input="input/Run2_Autumn18/GluGluToHHTo4B_node_cHHH0_TuneCP5_PSWeights_13TeV-powheg-pythia8.txt --is-signal"
output="NTuple_GluGluToHHTo4B_node_cHHH0.root"

make exe -j && \
    $exe \
    --input $input \
    --cfg  $cfg \
    --output $output \
    $@

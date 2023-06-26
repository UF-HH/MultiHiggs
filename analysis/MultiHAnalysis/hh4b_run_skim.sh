#!/bin/sh

# eval `scramv1 runtime -sh`
# source scripts/setup.sh

exe=bin/skim_ntuple.exe

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# 2018
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
cfg="config/skim_ntuple_HHTo4b_2018_106X_NanoAODv9.cfg"
#input="input/PrivateMC_2018/GluGluToHHTo4B_node_cHHH1_TuneCP5_13TeV-powheg-pythia8/GluGluToHHTo4B_node_cHHH1_TuneCP5_13TeV-powheg-pythia8.txt --is-signal"
#output="NTuple_GluGluToHHTo4B_node_cHHH1_TuneCP5_13TeV-powheg-pythia8.root"

input="input/Run2_UL/RunIISummer20UL18NanoAODv9/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8.txt"
output="NTuple_QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8.root"

make exe -j && \
    $exe \
    --input $input \
    --cfg  $cfg \
    --output $output \
    $@

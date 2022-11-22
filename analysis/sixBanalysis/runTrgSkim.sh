#!/bin/sh

cfg="config/skim_trigger_2018_106X_NanoAODv9.cfg"
exe=bin/skim_trigger.exe

#------------------------------------------------------------------------
# Run Data
#------------------------------------------------------------------------
output="SingleMuonA_TrgStudies.root"
input="input/Run2_UL/RunIISummer20UL18NanoAODv9/SingleMuon_Run2018A.txt"

make exe -j && \
    $exe \
    --input $input \
    --cfg  $cfg \
    --output $output \
    --is-data \
    --match \
    --maxEvts 200000 \
    $@

#------------------------------------------------------------------------
# Run TTTo2L2Nu
#------------------------------------------------------------------------
#output="TTTo2L2Nu_TrgStudies.root"
#input="input/Run2_UL/RunIISummer20UL18NanoAODv9/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8.txt"
#make exe -j && \
#    $exe \
#    --input $input \
#    --cfg  $cfg \
#    --output $output \
#    --match \
#    --maxEvts 20000 \
#    $@
#------------------------------------------------------------------------
# Run Signal
#------------------------------------------------------------------------
#output="NMSSM_XYH_YToHH_6b_MX_800_MY_300_TrgStudies.root"
#input="input/PrivateMC_2018/srosenzw_NMSSM_XYH_YToHH_6b_MX_800_MY_300_sl7_nano_100k.txt"
#make exe -j && \
#    $exe \
#    --input $input \
#    --cfg  $cfg \
#    --output $output \
#    --match \
#    --is-signal \
#    --maxEvts 2000 \
#    $@

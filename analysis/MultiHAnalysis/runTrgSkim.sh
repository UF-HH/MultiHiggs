#!/bin/sh

exe=bin/skim_trigger.exe

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# 2022
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#cfg="config/skim_trigger_2022_NanoAODv10.cfg"
cfg="config/skim_PNetHLT_2022_NanoAODv10.cfg"

# Run 2022 Data
output="Run3_SingleMuonD_2022_TrgStudies.root"
input="input/Run3/Muon_Run2022G_v1-v2.txt"

make exe -j && \
    $exe \
    --input $input \
    --cfg  $cfg \
    --output $output \
    --is-data \
    --match \
    --maxEvts 200000 \
    $@

# Run 2022 TT
#output="Run3_TT_TrgStudies.root"
#input="input/Run3/TT_TuneCP5_13p6TeV_powheg-pythia8.txt"
#make exe -j && \
#    $exe \
#    --input $input \
#    --cfg  $cfg \
#    --output $output \
#    --match \
#    --maxEvts 20000 \
#    $@

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# 2017
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#cfg="config/skim_trigger_2017_106X_NanoAODv9.cfg"

# Run 2017 Data
#output="SingleMuonB_2017_TrgStudies.root"
#input="input/Run2_UL/RunIISummer20UL17NanoAODv9/SingleMuon_Run2017B.txt"
#make exe -j && \
#    $exe \
#    --input $input \
#    --cfg  $cfg \
#    --output $output \
#    --is-data \
#    --match \
#    --maxEvts 200000 \
#    $@

# Run 2017 TTTo2L2Nu
#output="TTTo2L2Nu_2017_TrgStudies.root"
#input="input/Run2_UL/RunIISummer20UL17NanoAODv9/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8.txt"
#make exe -j && \
#    $exe \
#    --input $input \
#    --cfg  $cfg \
#    --output $output \
#    --match \
#    --maxEvts 20000 \
#    $@

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# 2018
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#cfg="config/skim_trigger_2018_106X_NanoAODv9.cfg"

# Run 2018 Data
#output="SingleMuonA_2018_TrgStudies.root"
#input="input/Run2_UL/RunIISummer20UL18NanoAODv9/SingleMuon_Run2018A.txt --is-data"
#make exe -j && \
#    $exe \
#    --input $input \
#    --cfg  $cfg \
#    --output $output \
#    --match \
#    --maxEvts 200000 \
#    $@

# Run 2018 TTTo2L2Nu
#output="TTTo2L2Nu_2018_TrgStudies.root"
#input="input/Run2_UL/RunIISummer20UL18NanoAODv9/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8.txt"

# Run 2018 Signal
#output="NMSSM_XYH_YToHH_6b_MX_800_MY_300_2018_TrgStudies.root"
#input="input/PrivateMC_2018/srosenzw_NMSSM_XYH_YToHH_6b_MX_800_MY_300_sl7_nano_100k.txt --is-signal"

#make exe -j && \
#    $exe \
#    --input $input \
#    --cfg  $cfg \
#    --output $output \
#    --match \
#    --maxEvts 2000 \
#    $@

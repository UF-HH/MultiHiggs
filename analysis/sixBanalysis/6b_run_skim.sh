#!/bin/sh

# eval `scramv1 runtime -sh`
# source scripts/setup.sh

exe=bin/skim_ntuple.exe

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# 2017
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#cfg="config/skim_ntuple_2017_106X_NanoAODv9.cfg" 

# Run 2017 data
#output="NTuple_BTagCSV_Run2017B.root"
#input="input/Run2_UL/RunIISummer20UL17NanoAODv9/BTagCSV_Run2017B.txt --is-data"

# Run 2017 background samples
#output="NTuple_TTJets_2017.root"
#input="input/Run2_UL/RunIISummer20UL17NanoAODv9/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8.txt"

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# 2018
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
cfg="config/skim_ntuple_2018_106X_NanoAODv9.cfg"

# Run signal
#output="NTuple_NMSSM_XYH_YToHH_6b_MX_450_MY_300.root"
#input="input/PrivateMC_2018/srosenzw_NMSSM_XYH_YToHH_6b_MX_450_MY_300_sl7_nano_100k.txt --is-signal"

output="NTuple_TTJets.root"
input="input/Run2_UL/RunIISummer20UL18NanoAODv9/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8.txt --maxEvts 2000"

#output="NTuple_QCD_bEnriched_HT700to1000.root"
#input="input/Run2_UL/RunIISummer20UL18NanoAODv9/QCD_bEnriched_HT700to1000_TuneCP5_13TeV-madgraph-pythia8.txt"

# Run data
#output="NTuple_Data.root"
#input="input/Run2_UL/RunIISummer20UL18NanoAODv9/JetHT_Run2018A.txt --is-data"

make exe -j && \
    $exe \
    --input $input \
    --cfg  $cfg \
    --output $output \
    $@

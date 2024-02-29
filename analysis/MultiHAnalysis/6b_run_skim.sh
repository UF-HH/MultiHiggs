#!/bin/sh

# eval `scramv1 runtime -sh`
# source scripts/setup.sh

exe=bin/skim_ntuple.exe

# output="NMSSM_XYH_YToHH_6b_MX_700_MY_400_accstudies_500k_Jul2021-v2.root"
# output="output-tree.root"
output="output.root"

extra=""

####################################################################################################
# Data
####################################################################################################
# input="input/Run2_UL/RunIISummer20UL18NanoAODv9/JetHT_Run2018C.txt --is-data "
# input="input/Run2_UL/RunIISummer20UL17NanoAODv9/BTagCSV_Run2017B.txt --is-data "
# input="input/Run2_UL/RunIISummer20UL16NanoAODv9/BTagCSV_Run2016B_ver2_HIPM.txt --is-data "

####################################################################################################
# Background
####################################################################################################
# input="input/Run2_UL/RunIISummer20UL18NanoAODv9/QCD_bEnriched_HT700to1000_TuneCP5_13TeV-madgraph-pythia8.txt"
# input="input/Run2_UL/RunIISummer20UL18NanoAODv9/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8.txt"

####################################################################################################
# Signal
####################################################################################################
# input="input/Run2_UL/RunIISummer20UL16NanoAODv9/NMSSM_XToYHTo6B/NMSSM_XToYHTo6B_MX-1000_MY-250_TuneCP5_13TeV-madgraph-pythia8.txt --is-signal"
# input="input/Run2_UL/RunIISummer20UL16NanoAODv9/preVFP/NMSSM_XToYHTo6B/NMSSM_XToYHTo6B_MX-1000_MY-250_TuneCP5_13TeV-madgraph-pythia8.txt --is-signal"
# input="input/Run2_UL/RunIISummer20UL17NanoAODv9/NMSSM_XToYHTo6B/NMSSM_XToYHTo6B_MX-700_MY-400_TuneCP5_13TeV-madgraph-pythia8.txt --is-signal"
input="input/Run2_UL/RunIISummer20UL18NanoAODv9/NMSSM_XToYHTo6B/NMSSM_XToYHTo6B_MX-1000_MY-250_TuneCP5_13TeV-madgraph-pythia8.txt --is-signal"
# input="input/PrivateMC_2018/NMSSM_XYH_YToHH_6b/NMSSM_XYH_YToHH_6b_MX_700_MY_400_2M.txt --is-signal"

# input="test.txt --is-signal"

cfg="config/skim_ntuple_2018_106X_NanoAODv9.cfg"
# cfg="config/skim_ntuple_2017_106X_NanoAODv9.cfg"
# cfg="config/skim_ntuple_2016postVFP_106X_NanoAODv9.cfg"
# cfg="config/skim_ntuple_2016preVFP_106X_NanoAODv9.cfg"
     
make exe -j && \
    $exe \
	--input $input \
	--cfg  $cfg \
	--output $output \
	--maxEvts 10000 \
	$extra \
	$@

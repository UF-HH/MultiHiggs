#!/bin/sh


output="TTToHadronic_test.root"
input="input/Run2_UL/RunIISummer20UL18NanoAODv9/TTToHadronic_TuneCP5_13TeV-powheg-pythia8.txt --is-signal"
cfg="config/ttbar_config/skim_ntuple_2018.cfg"
     
	 
# output="QCD_bEnriched_HT700to1000_test.root"
# input="input/Run2_UL/RunIISummer20UL16NanoAODv9/QCD_bEnriched_HT700to1000_TuneCP5_13TeV-madgraph-pythia8.txt"
# cfg="config/8b_config/skim_ntuple_2016_t8btag_minmass.cfg"

make exe -j && \
    ./bin/skim_ntuple.exe \
	--input $input \
	--cfg  $cfg \
	--output $output \
	$@

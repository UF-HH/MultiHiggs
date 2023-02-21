#!/bin/sh


output="NMSSM_XYY_YToHH_8b_MX_1000_MY_450_test.root"
input="input/PrivateMC_2018/NMSSM_XYY_YToHH_8b/NMSSM_XYY_YToHH_8b_MX_1000_MY_450.txt --is-signal"
cfg="config/8b_config/skim_ntuple_2018_t8btag_minmass.cfg"
     
	 
# output="QCD_bEnriched_HT700to1000_test.root"
# input="input/Run2_UL/RunIISummer20UL16NanoAODv9/QCD_bEnriched_HT700to1000_TuneCP5_13TeV-madgraph-pythia8.txt"
# cfg="config/8b_config/skim_ntuple_2016_t8btag_minmass.cfg"

make exe -j && \
    ./bin/skim_ntuple.exe \
	--input $input \
	--cfg  $cfg \
	--output $output \
	$@

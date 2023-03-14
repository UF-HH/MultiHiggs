#!/bin/sh


# output="NMSSM_XYY_YToHH_8b_MX_1000_MY_450_test.root"
# input="input/PrivateMC_2018/NMSSM_XYY_YToHH_8b/NMSSM_XYY_YToHH_8b_MX_1000_MY_450.txt --is-signal"
# cfg="config/8b_config/skim_ntuple_2018_t8btag_minmass.cfg"
     
output="qcd_test.root"
input="input/Run2_UL/RunIISummer20UL17NanoAODv9/QCD_bEnriched_HT700to1000_TuneCP5_13TeV-madgraph-pythia8.txt"
cfg="config/8b_config/skim_ntuple_2017_t8btag_minmass.cfg"
	 
# output="Data_JetHT_test.root"
# input="input/Run2_UL/RunIISummer20UL18NanoAODv9/JetHT_Run2018A.txt --is-data"
# cfg="config/8b_config/skim_ntuple_2018_t8btag_minmass.cfg"
	 

# output="QCD_bEnriched_HT700to1000_test.root"
# input="input/Run2_UL/RunIISummer20UL18NanoAODv9/QCD_bEnriched_HT700to1000_TuneCP5_13TeV-madgraph-pythia8.txt"
# cfg="config/8b_config/skim_ntuple_2018_t8btag_minmass.cfg"

output="TTToHadronic_test.root"
input="input/Run2_UL/RunIISummer20UL18NanoAODv9/TTToHadronic_TuneCP5_13TeV-powheg-pythia8.txt"
cfg="config/8b_config/skim_ntuple_2018_t8btag_minmass.cfg"

make exe -j && \
    ./bin/skim_ntuple.exe \
	--input $input \
	--cfg  $cfg \
	--output $output \
	$@

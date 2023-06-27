#!/bin/sh

# output="NMSSM_XYY_YToHH_8b_MX_500_MY_250_test.root"
# input="input/PrivateMC_2018/NMSSM_XYY_YToHH_8b/12_4_8_500K/NMSSM_XYY_YToHH_8b_MX_500_MY_250.txt --is-signal"

# output="NMSSM_XYY_YToHH_8b_MX_1000_MY_250_test.root"
# input="input/PrivateMC_2018/NMSSM_XYY_YToHH_8b/12_4_8_1M/NMSSM_XYY_YToHH_8b_MX_1000_MY_250.txt --is-signal"

output="NMSSM_XYY_YToHH_8b_MX_1000_MY_450_test.root"
input="input/PrivateMC_2018/NMSSM_XYY_YToHH_8b/pu/group/NMSSM_XYY_YToHH_8b_MX_1000_MY_450.txt --is-signal"
# cfg="config/8b_config/skim_ntuple_2018_t8btag_minmass.cfg"
# cfg="config/8b_config/skim_ntuple_2018_boosted.cfg"
cfg="config/8b_config/skim_ntuple_2018_feynnet.cfg"
     
# output="Data_JetHT_test.root"
# input="input/Run2_UL/RunIISummer20UL18NanoAODv9/JetHT_Run2018A.txt --is-data"
# cfg="config/8b_config/skim_ntuple_2018_t8btag_minmass.cfg"
	 

# output="QCD_bEnriched_HT700to1000_test.root"
# input="input/Run2_UL/RunIISummer20UL18NanoAODv9/QCD_bEnriched_HT700to1000_TuneCP5_13TeV-madgraph-pythia8.txt"
# cfg="config/8b_config/skim_ntuple_2018_t8btag_minmass.cfg"

# output="TTToHadronic_test.root"
# input="input/Run2_UL/RunIISummer20UL18NanoAODv9/TTToHadronic_TuneCP5_13TeV-powheg-pythia8.txt"
# cfg="config/8b_config/skim_ntuple_2018_t8btag_minmass.cfg"

make exe -j && \
    ./bin/skim_ntuple.exe \
	--input $input \
	--cfg  $cfg \
	--output $output \
	$@

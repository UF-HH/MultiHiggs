#!/bin/sh

output="output.root"
input="input/PrivateMC_2018/NMSSM_XYY_YToHH_8b/NMSSM_XYY_YToHH_8b_MX_1000_MY_450.txt --is-signal"

cfg="config/8b_config/accstudies_2018.cfg"
     
make exe -j && \
    ./bin/skim_ntuple.exe \
	--input $input \
	--cfg  $cfg \
	--output $output \
	$@

with_pu="input/PrivateMC_2018/NMSSM_XYY_YToHH_8b/"
no_pu="input/PrivateMC_2018/NMSSM_XYY_YToHH_8b/no_pu/"
training="input/PrivateMC_2018/NMSSM_XYY_YToHH_8b/training/"

indir=$with_pu
# indir=$training

cfg="config/8b_config/skim_ntuple_2018_ranked_quadh.cfg"

skim_ntuple.exe --input $indir/NMSSM_XYY_YToHH_8b_MX_1000_MY_300.txt --cfg $cfg --output NMSSM_XYY_YToHH_8b_MX_1000_MY_300_accstudies.root --is-signal &
skim_ntuple.exe --input $indir/NMSSM_XYY_YToHH_8b_MX_1000_MY_450.txt --cfg $cfg --output NMSSM_XYY_YToHH_8b_MX_1000_MY_450_accstudies.root --is-signal &
skim_ntuple.exe --input $indir/NMSSM_XYY_YToHH_8b_MX_700_MY_300.txt --cfg $cfg --output NMSSM_XYY_YToHH_8b_MX_700_MY_300_accstudies.root --is-signal   &
skim_ntuple.exe --input $indir/NMSSM_XYY_YToHH_8b_MX_800_MY_300.txt --cfg $cfg --output NMSSM_XYY_YToHH_8b_MX_800_MY_300_accstudies.root --is-signal   &
skim_ntuple.exe --input $indir/NMSSM_XYY_YToHH_8b_MX_800_MY_350.txt --cfg $cfg --output NMSSM_XYY_YToHH_8b_MX_800_MY_350_accstudies.root --is-signal   &
skim_ntuple.exe --input $indir/NMSSM_XYY_YToHH_8b_MX_900_MY_300.txt --cfg $cfg --output NMSSM_XYY_YToHH_8b_MX_900_MY_300_accstudies.root --is-signal   &
skim_ntuple.exe --input $indir/NMSSM_XYY_YToHH_8b_MX_900_MY_400.txt --cfg $cfg --output NMSSM_XYY_YToHH_8b_MX_900_MY_400_accstudies.root --is-signal   &
skim_ntuple.exe --input $indir/NMSSM_XYY_YToHH_8b_MX_1200_MY_500.txt --cfg $cfg --output NMSSM_XYY_YToHH_8b_MX_1200_MY_500_accstudies.root --is-signal &

wait $!
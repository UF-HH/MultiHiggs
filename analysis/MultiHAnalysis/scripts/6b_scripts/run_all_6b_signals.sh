with_pu="input/PrivateMC_2018/NMSSM_XYY_YToHH_8b/"
no_pu="input/PrivateMC_2018/NMSSM_XYY_YToHH_8b/no_pu/"
training="input/PrivateMC_2018/NMSSM_XYY_YToHH_8b/training/"

indir=$no_pu
# indir=$with_pu
# indir=$training

cfg="config/8b_config/accstudies_2018.cfg"
outdir="/eos/uscms/store/user/ekoenig/8BAnalysis/NTuples/2018/accstudies/raw_no_pu/"

run_skim() {
    skim_ntuple.exe --input ${1}/NMSSM_XYY_YToHH_8b_${3}.txt --cfg ${2} --output NMSSM_XYY_YToHH_8b_${3}_accstudies.root --is-signal
}
export -f run_skim

time \
    parallel -j4 \
        run_skim $indir $cfg\
        ::: MX_1000_MY_300 MX_1000_MY_450 MX_700_MY_300 MX_800_MY_300 MX_800_MY_350 MX_900_MY_300 MX_900_MY_400 MX_1200_MY_500

mkdir -p $outdir/NMSSM_XYY_YToHH_8b
mv NMSSM_XYY_YToHH_8b*.root $outdir/NMSSM_XYY_YToHH_8b
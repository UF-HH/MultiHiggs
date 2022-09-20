with_pu="input/PrivateMC_2018/NMSSM_XYY_YToHH_8b/"
no_pu="input/PrivateMC_2018/NMSSM_XYY_YToHH_8b/no_pu/"
training="input/PrivateMC_2018/NMSSM_XYY_YToHH_8b/training/"


# indir=$no_pu
indir=$with_pu
# indir=$training

# CFG="config/8b_config/accstudies_2018.cfg"
# ODIR="/eos/uscms/store/user/ekoenig/8BAnalysis/NTuples/2018/accstudies/raw_no_pu"

CFG="config/8b_config/skim_ntuple_2018_ranked_quadh.cfg"
ODIR="/eos/uscms/store/user/ekoenig/8BAnalysis/NTuples/2018/preselection/ranked_quadh/"

TAG="NMSSM_XYY_YToHH_8b"

rm -rf $ODIR/$TAG/analysis_tar
make exe -j || exit -1

echo "... tag       : ", $TAG
echo "... saving to : ", $ODIR

files=$(ls $indir/NMSSM_XYY_YToHH_8b_MX_*)

for input in ${files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-signal --forceOverwrite
done

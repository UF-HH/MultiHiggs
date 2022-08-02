ODIR="/store/user/ekoenig/8BAnalysis/NTuples/2018/training/training_5M"
# ODIR="/store/user/srosenzw/analysis/"

. scripts/arg_submit.sh -v sr "$@"
TAG="NMSSM_XYY_YToHH_8b"
CFG="config/8b_config/skim_ntuple_2018_t8btag.cfg"

make exe -j || exit -1

echo "... tag       : ", $TAG
echo "... saving to : ", $ODIR

files=$(ls input/PrivateMC_2018/NMSSM_XYY_YToHH_8b/training_5M/NMSSM_XYY_YToHH_8b_MX_*)

for input in ${files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --memory 2500 --is-signal
done

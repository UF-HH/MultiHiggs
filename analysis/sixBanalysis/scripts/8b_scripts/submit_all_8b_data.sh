ODIR="/store/user/ekoenig/8BAnalysis/NTuples/2018/preselection/ranked_quadh/"
# ODIR="/store/user/srosenzw/analysis/"

. scripts/arg_submit.sh -v qcd "$@"
TAG="JetHT_Data"
CFG="config/8b_config/skim_ntuple_2018_ranked_quadh.cfg"

make exe -j || exit -1

echo "... tag       : ", $TAG
echo "... saving to : ", $ODIR

qcd_files=$(ls input/Run2_UL/2018/JetHT*)

for input in ${qcd_files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 200 --input $input --is-data
done

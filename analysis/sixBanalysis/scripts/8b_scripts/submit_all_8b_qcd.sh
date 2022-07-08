ODIR="/store/user/ekoenig/8BAnalysis/NTuples/2018/preselection/jet_net/"
# ODIR="/store/user/srosenzw/analysis/"

. scripts/arg_submit.sh -v qcd "$@"
TAG="QCD"
CFG="config/8b_config/skim_ntuple_2018_gnn_jet.cfg"

make exe -j || exit -1

echo "... tag       : ", $TAG
echo "... saving to : ", $ODIR

qcd_files=$(ls input/Run2_Autumn18/QCD*BGenFilter* input/Run2_UL/2018/QCD*bEnriched*)

for input in ${qcd_files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --memory 2500
done

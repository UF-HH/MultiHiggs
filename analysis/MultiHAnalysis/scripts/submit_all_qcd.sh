# ODIR="/store/user/ekoenig/6BAnalysis/NTuples/2018/"
# ODIR="/store/user/srosenzw/analysis/"

ODIR="/store/user/srosenzw/sixb/ntuples/Summer2018UL/"

. scripts/arg_submit.sh -v qcd "$@"
TAG="dHHH_pairs/QCD"
CFG="config/skim_ntuple_2018.cfg"

make exe -j || exit -1

echo "... tag       : ", $TAG
echo "... saving to : ", $ODIR

qcd_files=$(ls input/Run2_Autumn18/QCD*BGenFilter* input/Run2_UL/2018/QCD*bEnriched* input/Run2_Autumn18/QCD_bEnriched_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8.txt)

for input in ${qcd_files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --forceOverwrite
done

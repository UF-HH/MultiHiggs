ODIR="/store/user/ekoenig/6BAnalysis/NTuples/2018/"

. scripts/arg_submit.sh -v qcd "$@"
TAG="${TAG}TTJets"

make exe -j || exit -1

echo "... tag       : ", $TAG
echo "... saving to : ", $ODIR

python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input input/Run2_UL/2018/TTJets.txt         
# python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg config/skim_ntuple_2018_ttbar.cfg --njobs 100 --input input/Run2_UL/2018/SingleMuon_Run2.txt --is-data


CFG="config/8b_config/skim_ntuple_2018_t8btag_minmass.cfg"
ODIR="/store/user/ekoenig/8BAnalysis/NTuples/2018/preselection/t8btag_minmass/"


VERSION="Run2_UL/RunIISummer20UL18NanoAODv9"
TAG="$VERSION/TTJets/"

rm -rf /eos/uscms/$ODIR/$TAG/analysis_tar
make exe -j || exit -1

echo "... tag       : ", $TAG
echo "... saving to : ", $ODIR

ttbar_files=$(ls input/$VERSION/TT*)


for input in ${ttbar_files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 150 --input $input --memory 2500 --forceOverwrite
done
# python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg config/skim_ntuple_2018_ttbar.cfg --njobs 100 --input input/Run2_UL/2018/SingleMuon_Run2.txt --is-data


#############

# TAG="ttbar_2018_10Jan2022"
# ODIR="/store/group/lpchbb/lcadamur/sixb_ntuples/"

# echo "... tag       : ", $TAG
# echo "... saving to : ", $ODIR

# python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg config/skim_ntuple_2018_ttbar.cfg --njobs 100 --input input/Run2_UL/2018/TTJets.txt         
# python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg config/skim_ntuple_2018_ttbar.cfg --njobs 100 --input input/Run2_UL/2018/SingleMuon_Run2.txt --is-data
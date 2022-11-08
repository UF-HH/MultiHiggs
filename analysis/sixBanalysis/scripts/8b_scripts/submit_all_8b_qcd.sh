
CFG="config/8b_config/skim_ntuple_2018_t8btag_minmass_jet_eta28.cfg"
ODIR="/store/user/ekoenig/8BAnalysis/NTuples/2018/preselection/t8btag_minmass_jet_eta28/"

TAG="QCD"

rm -rf $ODIR/$TAG/analysis_tar
make exe -j || exit -1

echo "... tag       : ", $TAG
echo "... saving to : ", $ODIR

qcd_files=$(ls input/Run2_Autumn18/QCD*BGenFilter* input/Run2_UL/2018/QCD*bEnriched*)

for input in ${qcd_files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --memory 2500 --forceOverwrite
done

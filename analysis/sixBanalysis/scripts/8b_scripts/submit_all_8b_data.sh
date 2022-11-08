
CFG="config/8b_config/skim_ntuple_2018_t8btag_minmass_jet_eta28.cfg"
ODIR="/store/user/ekoenig/8BAnalysis/NTuples/2018/preselection/t8btag_minmass_jet_eta28/"

TAG="JetHT_Data"

rm -rf $ODIR/$TAG/analysis_tar
make exe -j || exit -1

echo "... tag       : ", $TAG
echo "... saving to : ", $ODIR

qcd_files=$(ls input/Run2_UL/2018/JetHT_Run2018{A,B,C,D}.txt)

for input in ${qcd_files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 200 --input $input --is-data --forceOverwrite
done

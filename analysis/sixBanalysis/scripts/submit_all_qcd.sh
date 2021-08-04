ODIR="/store/user/ekoenig/6BAnalysis/NTuples/UL/2018/Higgs_CR"
TAG="QCD"

make exe -j || exit -1

echo "... tag       : ", $TAG
echo "... saving to : ", $ODIR

qcd_files=$(ls input/Run2_UL/2018/QCD*HT*)

for input in ${qcd_files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg config/skim_ntuple_2018_cr.cfg --njobs 100 --input $input
done

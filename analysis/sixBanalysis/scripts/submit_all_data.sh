ODIR="/store/user/ekoenig/6BAnalysis/NTuples/2018/"
TAG="JetHT_Data"

make exe -j || exit -1

echo "... tag       : ", $TAG
echo "... saving to : ", $ODIR

qcd_files=$(ls input/Run2_UL/2018/JetHT*)

for input in ${qcd_files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg config/skim_ntuple_2018_cr.cfg --njobs 100 --input $input --is-data
done

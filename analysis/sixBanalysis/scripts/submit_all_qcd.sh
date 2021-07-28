ODIR="/store/user/ekoenig/6BAnalysis/NTuples/2018/"
TAG="QCD"

make exe -j || exit -1

echo "... tag       : ", $TAG
echo "... saving to : ", $ODIR

qcd_files=$(ls input/Run2_Autumn18/QCD*HT*)

for input in ${qcd_files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg config/skim_ntuple_2018.cfg --njobs 100 --input $input
done

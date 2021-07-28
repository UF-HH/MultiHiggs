
ODIR="/store/user/ekoenig/6BAnalysis/NTuples/2018/"
TAG="NMSSM"

make exe -j || exit -1

echo "... tag       : ", $TAG
echo "... saving to : ", $ODIR

files=$(ls input/PrivateMC_2021/*)

for input in ${files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg config/skim_ntuple_2018.cfg --njobs 100 --input $input --is-signal
done

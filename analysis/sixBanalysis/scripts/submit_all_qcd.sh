TAG="qcd_2018_sixb"
ODIR="/store/user/ekoenig/6BAnalysis/NTuples/2018/QCD/"

echo "... tag       : ", $TAG
echo "... saving to : ", $ODIR

qcd_files=$(ls input/Run2_UL/2018/QCD_Pt_*)

make exe -j || exit -1

for input in ${qcd_files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg config/skim_ntuple_2018.cfg --njobs 100 --input $input
    break
done

ODIR="/store/user/ekoenig/6BAnalysis/NTuples/2018/QCD/"

make exe -j || exit -1

echo "... saving to : ", $ODIR

qcd_files=$(ls input/Run2_UL/2018/QCD_Pt_*)

for input in ${qcd_files[@]}; do
    TAG=$(basename $input)
    TAG=${TAG/.txt/""}
    echo "... tag       : ", $TAG
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg config/skim_ntuple_2018.cfg --njobs 100 --input $input
done

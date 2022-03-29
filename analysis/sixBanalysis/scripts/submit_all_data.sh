ODIR="/store/user/srosenzw/sixb/sixb_ntuples/Summer2018UL/"

. scripts/arg_submit.sh -v qcd "$@"
TAG="dHHH_pairs"
CFG="config/skim_ntuple_2018.cfg"

make exe -j || exit -1

echo "... tag       : ", $TAG
echo "... saving to : ", $ODIR

qcd_files=$(ls input/Run2_UL/2018/JetHT*)

for input in ${qcd_files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 200 --input $input --is-data
done

ODIR="/store/user/srosenzw/sixb/sixb_ntuples/Summer2018UL/"

. scripts/arg_submit.sh -v sr "$@"

# CFG="config/skim_ntuple_2018_nocuts.cfg"
# TAG="NMSSM_nocuts"

CFG="config/skim_ntuple_2018.cfg"
# TAG="dHHH_pairs/NMSSM"
TAG="dHHH_pairs_maxbtag/NMSSM"

make exe -j || exit -1

echo "... tag       : ", $TAG
echo "... saving to : ", $ODIR

relDir='input/PrivateMC_2018/NMSSM_XYH_YToHH_6b/'
files=$(ls ${relDir})
# files=$(ls input/PrivateMC_2018/NMSSM_XYH_YToHH_6b_MX_450_MY_300.txt )
for input in ${files[@]}; do
    if [[ "$input" == "misc" ]]; then
        continue
    fi
    input="${relDir}${input}"
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-signal
done
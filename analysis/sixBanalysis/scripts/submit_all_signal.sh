# ODIR="/store/user/srosenzw/studies/"
ODIR="/store/user/srosenzw/analysis/"

. scripts/arg_submit.sh -v sr "$@"
# TAG="${TAG}NMSSM"

# CFG="config/skim_ntuple_2018_nocuts.cfg"
# CFG="config/skim_ntuple_2018_btag.cfg"
CFG="config/skim_ntuple_2018.cfg"
# TAG="NMSSM_nocuts"
TAG="btag_sort"

make exe -j || exit -1

echo "... tag       : ", $TAG
echo "... saving to : ", $ODIR

# files=$(ls input/PrivateMC_2018/NMSSM_XYH_YToHH_6b_MX_450_MY_300.txt )
# for input in ${files[@]}; do
#     python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-signal
# done

# files=$(ls input/PrivateMC_2018/NMSSM_XYH_YToHH_6b_MX_500_MY_300.txt )
# for input in ${files[@]}; do
#     python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-signal
# done

# files=$(ls input/PrivateMC_2018/NMSSM_XYH_YToHH_6b_MX_600_MY_300.txt )
# for input in ${files[@]}; do
#     python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-signal
# done

# files=$(ls input/PrivateMC_2018/NMSSM_XYH_YToHH_6b_MX_600_MY_400.txt )
# for input in ${files[@]}; do
#     python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-signal
# done

# files=$(ls input/PrivateMC_2018/NMSSM_XYH_YToHH_6b_MX_700_MY_300.txt )
# for input in ${files[@]}; do
#     python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-signal
# done

files=$(ls input/PrivateMC_2018/NMSSM_XYH_YToHH_6b_MX_700_MY_400.txt )
# files=$(ls input/PrivateMC_2021/NMSSM_XYH_YToHH_6b_MX_700_MY_400_10M.txt )
for input in ${files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-signal
done

# files=$(ls input/PrivateMC_2018/NMSSM_XYH_YToHH_6b_MX_700_MY_500.txt )
# for input in ${files[@]}; do
#     python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-signal
# done
#input/PrivateMC_2021/NMSSM_XYH_YToHH_6b_MX_700_MY_400_10M.txt

# for input in ${files[@]}; do
    # python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-signal
# done

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# To produce the input .txt files:
# 
# cd <working_area>/sixB/analysis/sixBanalysis/input/PrivateMC_2018
# ./getSamples.py -d /eos/uscms/store/group/lpchbb/srosenzw/XYH_YToHH/CRAB_PrivateMC
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
ODIR="/store/user/mkolosov/HHHTo6B/"

. scripts/arg_submit.sh -v sr "$@"

# TAG="${TAG}NMSSM"
# CFG="config/skim_ntuple_2018_nocuts.cfg"
# TAG="NMSSM_nocuts"

CFG="config/skim_ntuple_2018_marina.cfg"
TAG="Summer2018UL_29Sep2022_withoutLeptonVeto"

make exe -j || exit -1

echo "... tag       : ", $TAG
echo "... saving to : ", $ODIR

files=$(ls input/PrivateMC_2018/srosenzw_NMSSM_XYH_YToHH_6b_MX_450_MY_300_sl7_nano_100k.txt )
for input in ${files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-signal
done

files=$(ls input/PrivateMC_2018/srosenzw_NMSSM_XYH_YToHH_6b_MX_500_MY_300_sl7_nano_100k.txt )
for input in ${files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-signal
done

files=$(ls input/PrivateMC_2018/srosenzw_NMSSM_XYH_YToHH_6b_MX_600_MY_300_sl7_nano_100k.txt )
for input in ${files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-signal
done

files=$(ls input/PrivateMC_2018/srosenzw_NMSSM_XYH_YToHH_6b_MX_600_MY_400_sl7_nano_100k.txt )
for input in ${files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-signal
done

files=$(ls input/PrivateMC_2018/srosenzw_NMSSM_XYH_YToHH_6b_MX_700_MY_300_sl7_nano_100k.txt )
for input in ${files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-signal
done

files=$(ls input/PrivateMC_2018/srosenzw_NMSSM_XYH_YToHH_6b_MX_700_MY_400_sl7_nano_2M.txt )
for input in ${files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-signal
done

files=$(ls input/PrivateMC_2018/srosenzw_NMSSM_XYH_YToHH_6b_MX_700_MY_500_sl7_nano_100k.txt )
for input in ${files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-signal
done

files=$(ls input/PrivateMC_2018/srosenzw_NMSSM_XYH_YToHH_6b_MX_800_MY_300_sl7_nano_100k.txt )
for input in ${files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-signal
done

files=$(ls input/PrivateMC_2018/srosenzw_NMSSM_XYH_YToHH_6b_MX_800_MY_400_sl7_nano_100k.txt )
for input in ${files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-signal
done

files=$(ls input/PrivateMC_2018/srosenzw_NMSSM_XYH_YToHH_6b_MX_800_MY_500_sl7_nano_100k.txt )
for input in ${files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-signal
done

files=$(ls input/PrivateMC_2018/srosenzw_NMSSM_XYH_YToHH_6b_MX_800_MY_600_sl7_nano_100k.txt )
for input in ${files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-signal
done

files=$(ls input/PrivateMC_2018/srosenzw_NMSSM_XYH_YToHH_6b_MX_900_MY_300_sl7_nano_100k.txt )
for input in ${files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-signal
done

files=$(ls input/PrivateMC_2018/srosenzw_NMSSM_XYH_YToHH_6b_MX_900_MY_400_sl7_nano_100k.txt )
for input in ${files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-signal
done

files=$(ls input/PrivateMC_2018/srosenzw_NMSSM_XYH_YToHH_6b_MX_900_MY_500_sl7_nano_100k.txt )
for input in ${files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-signal
done

files=$(ls input/PrivateMC_2018/srosenzw_NMSSM_XYH_YToHH_6b_MX_900_MY_600_sl7_nano_100k.txt )
for input in ${files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-signal
done

files=$(ls input/PrivateMC_2018/srosenzw_NMSSM_XYH_YToHH_6b_MX_900_MY_700_sl7_nano_100k.txt )
for input in ${files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-signal
done

files=$(ls input/PrivateMC_2018/srosenzw_NMSSM_XYH_YToHH_6b_MX_1000_MY_300_sl7_nano_100k.txt )
for input in ${files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-signal
done

files=$(ls input/PrivateMC_2018/srosenzw_NMSSM_XYH_YToHH_6b_MX_1000_MY_400_sl7_nano_100k.txt ) 
for input in ${files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-signal
done

files=$(ls input/PrivateMC_2018/srosenzw_NMSSM_XYH_YToHH_6b_MX_1000_MY_500_sl7_nano_100k.txt )
for input in ${files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-signal
done

files=$(ls input/PrivateMC_2018/srosenzw_NMSSM_XYH_YToHH_6b_MX_1000_MY_600_sl7_nano_100k.txt )
for input in ${files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-signal
done

files=$(ls input/PrivateMC_2018/srosenzw_NMSSM_XYH_YToHH_6b_MX_1000_MY_700_sl7_nano_100k.txt )
for input in ${files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-signal
done

files=$(ls input/PrivateMC_2018/srosenzw_NMSSM_XYH_YToHH_6b_MX_1000_MY_800_sl7_nano_100k.txt )
for input in ${files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-signal
done

files=$(ls input/PrivateMC_2018/srosenzw_NMSSM_XYH_YToHH_6b_MX_1100_MY_300_sl7_nano_100k.txt )
for input in ${files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-signal
done

files=$(ls input/PrivateMC_2018/srosenzw_NMSSM_XYH_YToHH_6b_MX_1100_MY_400_sl7_nano_100k.txt )
for input in ${files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-signal
done

files=$(ls input/PrivateMC_2018/srosenzw_NMSSM_XYH_YToHH_6b_MX_1100_MY_500_sl7_nano_100k.txt )
for input in ${files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-signal
done

files=$(ls input/PrivateMC_2018/srosenzw_NMSSM_XYH_YToHH_6b_MX_1100_MY_600_sl7_nano_100k.txt )
for input in ${files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-signal
done

files=$(ls input/PrivateMC_2018/srosenzw_NMSSM_XYH_YToHH_6b_MX_1100_MY_700_sl7_nano_100k.txt )
for input in ${files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-signal
done

files=$(ls input/PrivateMC_2018/srosenzw_NMSSM_XYH_YToHH_6b_MX_1100_MY_800_sl7_nano_100k.txt )
for input in ${files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-signal
done

files=$(ls input/PrivateMC_2018/srosenzw_NMSSM_XYH_YToHH_6b_MX_1100_MY_900_sl7_nano_100k.txt )
for input in ${files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-signal
done

files=$(ls input/PrivateMC_2018/srosenzw_NMSSM_XYH_YToHH_6b_MX_1200_MY_300_sl7_nano_100k.txt )
for input in ${files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-signal
done

files=$(ls input/PrivateMC_2018/srosenzw_NMSSM_XYH_YToHH_6b_MX_1200_MY_400_sl7_nano_100k.txt )
for input in ${files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-signal
done

files=$(ls input/PrivateMC_2018/srosenzw_NMSSM_XYH_YToHH_6b_MX_1200_MY_500_sl7_nano_100k.txt )
for input in ${files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-signal
done

files=$(ls input/PrivateMC_2018/srosenzw_NMSSM_XYH_YToHH_6b_MX_1200_MY_600_sl7_nano_100k.txt )
for input in ${files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-signal
done

files=$(ls input/PrivateMC_2018/srosenzw_NMSSM_XYH_YToHH_6b_MX_1200_MY_700_sl7_nano_100k.txt )
for input in ${files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-signal
done

files=$(ls input/PrivateMC_2018/srosenzw_NMSSM_XYH_YToHH_6b_MX_1200_MY_800_sl7_nano_100k.txt )
for input in ${files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-signal
done

files=$(ls input/PrivateMC_2018/srosenzw_NMSSM_XYH_YToHH_6b_MX_1200_MY_900_sl7_nano_100k.txt )
for input in ${files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-signal
done

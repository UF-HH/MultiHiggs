# sh scripts/6b_scripts/submit_all_6b_private.sh

ODIR="/store/user/srosenzw/sixb/ntuples"

# TAG="Summer2016UL/preVFP/maxbtag/NMSSM"
# CFG="config/skim_ntuple_2016preVFP_106X_NanoAODv9.cfg"
# VERSION="input/PrivateMC/NMSSM_XYH_YToHH_6b/Private_2016/preVFP"

# TAG="Summer2016UL/maxbtag/NMSSM"
# CFG="config/skim_ntuple_2016_106X_NanoAODv9.cfg"
# VERSION="input/PrivateMC/NMSSM_XYH_YToHH_6b/Private_2016"

# TAG="Summer2017UL/maxbtag/NMSSM"
# CFG="config/skim_ntuple_2017_106X_NanoAODv9.cfg"
# VERSION="input/PrivateMC/NMSSM_XYH_YToHH_6b/Private_2017"

TAG="Summer2018UL/maxbtag/NMSSM"
CFG="config/skim_ntuple_2018_106X_NanoAODv9.cfg"
VERSION="input/PrivateMC/NMSSM_XYH_YToHH_6b/Private_2018"

files=$(ls $VERSION/NMSSM_XYH_YToHH_6b_*)

rm -rf /eos/uscms/$ODIR/$TAG/analysis_tar
make exe -j || exit -1

echo "... tag       : ", $TAG
echo "... saving to : ", $ODIRs

for input in ${files[@]}; do
    tmp=${input#*NMSSM_XYH_YToHH_6b_}   # remove prefix ending in "NMSSM_XYH_YToHH_6b_"
    tmp=${tmp%.txt*} 
    mx=${tmp#*MX_}   
    mx=${mx%_MY*}   
    my=${tmp#*_MY_}   

    mx=$(($mx))
    my=$(($my))

    echo "$mx, $my"

    # if [[ $mx != 1100 ]]; then
    if [[ $mx -gt 2000 ]]; then
    # if [[ "$mx" -gt 1200 ]] || [[ "$mx" -lt 850 ]]; then
    # if [[ $mx -le 1200 || $mx -gt 2000 ]]; then
        echo ".. skipping because mx=$mx" 
        continue
    fi
    # if [[ $my -lt 300 ]]; then
    #     echo ".. skipping because mx=$my" 
    #     continue
    # fi
    echo "python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 1 --input $input --is-signal --forceOverwrite --memory 4000"
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 1 --input $input --is-signal --forceOverwrite --memory 4000 --maxEvts 500000
    # exit
done

# python scripts/submitSkimOnBatch.py --tag Summer2018UL/maxbtag/NMSSM --outputDir /store/user/srosenzw/sixb/ntuples --cfg config/skim_ntuple_2018_106X_NanoAODv9.cfg --njobs 1 --input input/PrivateMC/NMSSM_XYH_YToHH_6b/Private_2018/NMSSM_XYH_YToHH_6b_MX_800_MY_300.txt  --is-signal --forceOverwrite --maxEvts 500000

# python scripts/submitSkimOnBatch.py --tag Summer2017UL/maxbtag/NMSSM --outputDir /store/user/srosenzw/sixb/ntuples --cfg config/skim_ntuple_2017_106X_NanoAODv9.cfg --njobs 1 --input input/PrivateMC/NMSSM_XYH_YToHH_6b/Private_2017/NMSSM_XYH_YToHH_6b_MX_700_MY_400.txt  --is-signal --forceOverwrite

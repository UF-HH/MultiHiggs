# TAG="Summer2018UL/cutflow_studies/presel/NMSSM"
# TAG="Summer2018UL/maxbtag_4b/NMSSM"
# TAG="Summer2018UL/maxbtag/NMSSM"
# TAG="Summer2018UL/maxbtag/Official_NMSSM"
# TAG="Summer2018UL/btag_pt/NMSSM"

TAG="Summer2018UL/maxbtag/NMSSM"
CFG="config/skim_ntuple_2018_106X_NanoAODv9_private.cfg"
VERSION="input/PrivateMC_2018/NMSSM_XYH_YToHH_6b"

files=$(ls $VERSION/NMSSM_XYH_YToHH_6b_*)

rm -rf /eos/uscms/$ODIR/$TAG/analysis_tar
make exe -j || exit -1

echo "... tag       : ", $TAG
echo "... saving to : ", $ODIRs

for input in ${files[@]}; do
    tmp=${input#*NMSSM_XYH_YToHH_6b_}   # remove prefix ending in "NMSSM_XYH_YToHH_6b_"
    tmp=${tmp%.txt*} 
    tmp=${tmp%_1M} 
    tmp=${tmp%_2M} 
    tmp=${tmp%_3M} 
    tmp=${tmp%_4M} 
    tmp=${tmp%_5M} 
    tmp=${tmp%_10M} 
    tmp=${tmp%_*k*} 
    mx=${tmp#*MX_}   
    mx=${mx%_MY*}   
    my=${tmp#*_MY_}   

    mx=$(($mx))
    my=$(($my))

    # if [[ $mx -gt 2000 ]]; then
    if [[ $mx -gt 1200 ]]; then
    # if [[ $mx -le 1200 || $mx -gt 2000 ]]; then
        echo ".. skipping because mx=$mx" 
        continue
    fi
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 75 --input $input --is-signal --forceOverwrite --memory 4000
done

# python scripts/submitSkimOnBatch.py --tag Summer2018UL/maxbtag/NMSSM --outputDir /store/user/srosenzw/sixb/ntuples --cfg config/skim_ntuple_2018_106X_NanoAODv9.cfg --njobs 100 --input input/PrivateMC_2018/NMSSM_XYH_YToHH_6b/NMSSM_XYH_YToHH_6b_MX_700_MY_400.txt  --is-signal --forceOverwrite

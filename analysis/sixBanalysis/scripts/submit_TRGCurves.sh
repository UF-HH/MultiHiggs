# Samples used for trigger studies
DATA_files=$(ls input/Run2_UL/RunIISummer20UL18NanoAODv9/SingleMuon_Run2018D.txt)
TT_files=$(ls input/Run2_UL/RunIISummer20UL18NanoAODv9/TTTo2L2Nu_TuneCP5_13TeV*)
Signal_files=$(ls input/PrivateMC_2018/srosenzw_NMSS*)
Signal8B_files=$(ls input/PrivateMC_2018/NMSSM_XYY_YToHH_8b/NMSSM*)

ODIR="/store/user/mkolosov/HHHTo6B/TriggerStudies/"
CFG="config/skim_trigger_2018_106X_NanoAODv9.cfg"

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Submit Trigger skimming with matching
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#TAG="Summer2018UL_TRGcurves_wTrgMatching_10Nov2022"

#make exe -j || exit -1
#echo "... tag       : ", $TAG
#echo "... saving to : ", $ODIR

#for input in ${DATA_files[@]}; do
#    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --match --is-data
#done

#for input in ${TT_files[@]}; do
#    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --match
#done

#for input in ${Signal_files[@]}; do
#    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --match --is-signal
#done

#for input in ${Signal8B_files[@]}; do
#    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --match --is-signal
#done

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Sumbit Trigger skimming without matching
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
TAG="Summer2018UL_TRGcurves_woTrgMatching_10Nov2022_8BSignal"

make exe -j || exit -1
echo "... tag       : ", $TAG
echo "... saving to : ", $ODIR

#for input in ${DATA_files[@]}; do
#    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-data
#done

#for input in ${TT_files[@]}; do
#    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input
#done

#for input in ${Signal_files[@]}; do
#    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-signal
#done

for input in ${Signal8B_files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-signal
done

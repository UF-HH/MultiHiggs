#
# Script to submit CONDOR jobs to get the TT dilepton sample for the trigger studies
#
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# 2022 Samples for trigger studies
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
DATA_files=$(ls input/Run3/*Muon_Run*)
ODIR="/store/user/mkolosov/MultiHiggs/DiHiggs/2022/TriggerEfficiency/"
CFG="config/skim_PNetHLT_2022_NanoAODv10.cfg"
TAG="Run3_TrgEff_ResolvedPNetPath_07Feb2023_SingleMuonPD"

make exe -j || exit -1
echo "... tag       : ", $TAG
echo "... saving to : ", $ODIR

for input in ${DATA_files[@]}; do
    python scripts/submitPNetTrgSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --match --is-data
done


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
# TripleBTag path efficiencies
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
#DATA_files=$(ls input/Run3/*)
#ODIR="/store/user/mkolosov/MultiHiggs/DiHiggs/2022/TriggerEfficiency/"
#CFG="config/skim_trigger_2022_NanoAODv10.cfg"

#TAG="Run3_2022_TriggerEfficiency_30Jan2023"

#make exe -j || exit -1
#echo "... tag       : ", $TAG
#echo "... saving to : ", $ODIR

#for input in ${DATA_files[@]}; do
#    python scripts/submitTrgSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --match --is-data
#done

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# 2017 Samples for trigger studies
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#DATA_files=$(ls input/Run2_UL/RunIISummer20UL17NanoAODv9/SingleMuon*)
#TT_files=$(ls input/Run2_UL/RunIISummer20UL17NanoAODv9/TTTo2L2Nu_TuneCP5_13TeV*)

#ODIR="/store/user/mkolosov/HHHTo6B/TriggerStudies/"
#CFG="config/skim_trigger_2017_106X_NanoAODv9.cfg"

# Submit Trigger skimming with matching
#TAG="Summer2017UL_TRGcurves_wTrgMatching_15Dec2022"

#make exe -j || exit -1
#echo "... tag       : ", $TAG
#echo "... saving to : ", $ODIR

#for input in ${DATA_files[@]}; do
#    python scripts/submitTrgSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --match --is-data
#done
#for input in ${TT_files[@]}; do
#    python scripts/submitTrgSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --match
#done

# Submit Trigger skimming without matching
#TAG="Summer2017UL_TRGcurves_woTrgMatching_28Nov2022"

#make exe -j || exit -1
#echo "... tag       : ", $TAG
#echo "... saving to : ", $ODIR

#for input in ${DATA_files[@]}; do
#    python scripts/submitTrgSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-data
#done
#for input in ${TT_files[@]}; do
#    python scripts/submitTrgSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input
#done


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# 2018 Samples used for trigger studies
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#DATA_files=$(ls input/Run2_UL/RunIISummer20UL18NanoAODv9/SingleMuon*)
#TT_files=$(ls input/Run2_UL/RunIISummer20UL18NanoAODv9/TTTo2L2Nu_TuneCP5_13TeV*)
#Signal_files=$(ls input/PrivateMC_2018/srosenzw_NMSS*)
#Signal8B_files=$(ls input/PrivateMC_2018/NMSSM_XYY_YToHH_8b/NMSSM*)

#ODIR="/store/user/mkolosov/HHHTo6B/TriggerStudies/"
#CFG="config/skim_trigger_2018_106X_NanoAODv9.cfg"

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Submit Trigger skimming with matching
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#TAG="Summer2018UL_TRGcurves_wTrgMatching_14Dec2022_4bCode"

#make exe -j || exit -1
#echo "... tag       : ", $TAG
#echo "... saving to : ", $ODIR

#for input in ${DATA_files[@]}; do
#    python scripts/submitTrgSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --match --is-data
#done

#for input in ${TT_files[@]}; do
#    python scripts/submitTrgSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --match
#done

#for input in ${Signal_files[@]}; do
#    python scripts/submitTrgSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --match --is-signal
#done

#for input in ${Signal8B_files[@]}; do
#    python scripts/submitTrgSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --match --is-signal
#done

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Sumbit Trigger skimming without matching
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#TAG="Summer2018UL_TRGcurves_woTrgMatching_15Dec2022"

#make exe -j || exit -1
#echo "... tag       : ", $TAG
#echo "... saving to : ", $ODIR

#for input in ${DATA_files[@]}; do
#    python scripts/submitTrgSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-data
#done

#for input in ${TT_files[@]}; do
#    python scripts/submitTrgSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input
#done

#for input in ${Signal_files[@]}; do
#    python scripts/submitTrgSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-signal
#done

#for input in ${Signal8B_files[@]}; do
#    python scripts/submitTrgSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-signal
#done

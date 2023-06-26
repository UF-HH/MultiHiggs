#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Script to submit NTuples on CONDOR
#
# - Comment out what you do not need :)
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#ODIR="/store/user/mkolosov/MultiHiggs/DiHiggs/RunII/FeynNetTraining/"

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# 2018
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#Signal_files=$(ls input/PrivateMC_2018/GluGluToHHTo4B_node_cHHH1_TuneCP5_13TeV-powheg-pythia8/GluGluToHHTo4B*)
#QCD_files=$(ls input/Run2_UL/RunIISummer20UL18NanoAODv9/QCD_*)
#TTJets_files=$(ls input/Run2_UL/RunIISummer20UL18NanoAODv9/TTJets_TuneCP5_13TeV*)

#CFG="config/skim_ntuple_HHTo4b_2018_106X_NanoAODv9.cfg"
#TAG="ForFeynNet_UL18_Background_23May2023"

#make exe -j || exit -1
#echo "... tag       : ", $TAG
#echo "... saving to : ", $ODIR

#for input in ${QCD_files[@]}; do
#    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input
#done

#for input in ${TTJets_files[@]}; do
#    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input
#done

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# 2022
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
ODIR="/store/user/mkolosov/MultiHiggs/DiHiggs/RunIII/FirstLook/"
DATA_files=$(ls input/Run3/2022/PrivateNano_JetMET_Run2022*)
CFG="config/skim_ntuple_HHTo4b_2022_PromptNanoAODv11.cfg"
TAG="JetMET_2022_DataOnly_10June2023"

make exe -j || exit -1
echo "... tag       : ", $TAG
echo "... saving to : ", $ODIR
for input in ${DATA_files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-data
done

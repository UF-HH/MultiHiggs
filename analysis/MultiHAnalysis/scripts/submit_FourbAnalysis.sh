#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Script to submit NTuples on CONDOR
#
# - Comment out what you do not need :)
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
ODIR="/store/user/mkolosov/MultiHiggs/DiHiggs/"

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# 2018
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Signal_files=$(ls input/Run2_Autumn18/GluGluToHHTo4B_node*)

CFG="config/skim_4b_ntuple_2018_102X_NanoAODv7.cfg"
TAG="RunIIAutumn18_NoSelections_GluGluToHHTo4B_22Dec2022"

make exe -j || exit -1
echo "... tag       : ", $TAG
echo "... saving to : ", $ODIR

# Signal only available for 2018 for the moment
for input in ${Signal_files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-signal
done

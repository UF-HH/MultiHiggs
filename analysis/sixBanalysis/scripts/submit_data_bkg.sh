#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Submit UL Data and NanoAODv9 simulated samples
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
ODIR="/store/user/mkolosov/HHHTo6B/"

. scripts/arg_submit.sh -v sr "$@"

CFG="config/skim_ntuple_2018_106X_NanoAODv9.cfg"
TAG="Summer2018UL_29Sep2022_withoutLeptonVeto"

make exe -j || exit -1

echo "... tag       : ", $TAG
echo "... saving to : ", $ODIR

DATA_files=$(ls input/Run2_UL/RunIISummer20UL18NanoAODv9/JetHT*)
QCD_files=$(ls input/Run2_UL/RunIISummer20UL18NanoAODv9/QCD_bEnriched*)
TTJets_files=$(ls input/Run2_UL/RunIISummer20UL18NanoAODv9/TTJets.txt)

for input in ${DATA_files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-data
done

for input in ${QCD_files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input
done

for input in ${TTJets_files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input
done


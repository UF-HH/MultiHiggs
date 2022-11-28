# Samples used for trigger studies
DATA_files=$(ls input/Run2_UL/RunIISummer20UL18NanoAODv9/JetHT*)
TTJets_files=$(ls input/Run2_UL/RunIISummer20UL18NanoAODv9/TTJets*)
QCD_files=$(ls input/Run2_UL/RunIISummer20UL18NanoAODv9/QCD_bEnriched*)
Signal_files=$(ls input/PrivateMC_2018/srosenzw_NMSS*)

ODIR="/store/user/mkolosov/HHHTo6B/"
CFG="config/skim_ntuple_2018_106X_NanoAODv9_marina.cfg"

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Submit Main Analysis skimming with trigger matching
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
TAG="RunIISummer20UL18_NMSSM_XYH_YToHH_6b_NoLeptonVeto_TrgSFwMatching_22Nov2022_1545"

make exe -j || exit -1
echo "... tag       : ", $TAG
echo "... saving to : ", $ODIR

for input in ${DATA_files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-data
done

for input in ${QCD_files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input
done

for input in ${TTJets_files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input
done

for input in ${Signal_files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-signal
done

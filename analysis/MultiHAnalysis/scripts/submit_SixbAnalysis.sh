#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Script to submit NTuples on CONDOR
#
# - Comment out what you do not need :)
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
ODIR="/store/user/mkolosov/HHHTo6B/"

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# 2017
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#DATA_files=$(ls input/Run2_UL/RunIISummer20UL17NanoAODv9/BTagCSV*)
#TTJets_files=$(ls input/Run2_UL/RunIISummer20UL17NanoAODv9/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8.txt)
#QCD_files=$(ls input/Run2_UL/RunIISummer20UL17NanoAODv9/QCD_bEnriched*)

# Submit Main Analysis skimming
#CFG="config/skim_ntuple_2017_106X_NanoAODv9.cfg"
#TAG="RunIISummer20UL17_DataBkgOnly_NoLeptonVeto_TrgSFwMatching_JetCuts_60_40_40_40_19Dec2022"
#TAG="RunIISummer20UL17_DataBkgOnly_NoLeptonVeto_NoTrgRequirement_JetCuts_60_40_40_40_19Dec2022"

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# 2018
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#DATA_files=$(ls input/Run2_UL/RunIISummer20UL18NanoAODv9/JetHT*)
TTJets_files=$(ls input/Run2_UL/RunIISummer20UL18NanoAODv9/TTJets*)
#QCD_files=$(ls input/Run2_UL/RunIISummer20UL18NanoAODv9/QCD_bEnriched*)
Signal_files=$(ls input/Run2_UL/RunIISummer20UL18NanoAODv9/NMSSM_XToYHTo6B/NMSSM_XToYHTo6B_MX*.txt)

# Submit Main Analysis skimming with trigger matching
CFG="config/skim_ntuple_2018_106X_NanoAODv9.cfg"
TAG="RunIISummer20UL18_NoLeptonVeto_NoTrgApplied_TrgPtThresholdsApplied_21Feb2023"

make exe -j || exit -1
echo "... tag       : ", $TAG
echo "... saving to : ", $ODIR

for input in ${Signal_files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-signal
done

#for input in ${DATA_files[@]}; do
#    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-data
#done

#for input in ${QCD_files[@]}; do
#    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input
#done

for input in ${TTJets_files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input
done

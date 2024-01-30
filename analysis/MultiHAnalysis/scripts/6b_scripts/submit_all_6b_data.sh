
ODIR="/store/user/srosenzw/sixb/ntuples/"
CFG="config/skim_ntuple_2018_106X_NanoAODv9.cfg"
# CFG="config/skim_ntuple_2017_106X_NanoAODv9.cfg"
# CFG="config/skim_ntuple_2016postVFP_106X_NanoAODv9.cfg"
# CFG="config/skim_ntuple_2016preVFP_106X_NanoAODv9.cfg"

VERSION="Run2_UL/RunIISummer20UL18NanoAODv9"
# VERSION="Run2_UL/RunIISummer20UL17NanoAODv9"
# VERSION="Run2_UL/RunIISummer20UL16NanoAODv9"
# VERSION="Run2_UL/RunIISummer20UL16NanoAODv9/preVFP"

TAG="Summer2018UL/maxbtag_4b/JetHT_Data_UL/"
# TAG="Summer2018UL/maxbtag_mmmm/JetHT_Data_UL/"
# TAG="Summer2017UL/maxbtag_4b/BTagCSV_Data_UL/"
# TAG="Summer2016UL/maxbtag_4b/BTagCSV_Data_UL/"
# TAG="Summer2016UL/preVFP/maxbtag_4b/BTagCSV_Data_UL/"

rm -rf /eos/uscms/$ODIR/$TAG/analysis_tar
make exe -j || exit -1

echo "... tag       : ", $TAG
echo "... saving to : ", $ODIR

qcd_files=$(ls input/Run2_UL/RunIISummer20UL18NanoAODv9/JetHT_Run2018{A,B,C,D}.txt)
# qcd_files=$(ls input/Run2_UL/RunIISummer20UL17NanoAODv9/BTagCSV_Run2017{B,C,D,E,F}.txt)
# qcd_files=$(ls input/Run2_UL/RunIISummer20UL16NanoAODv9/BTagCSV*)
# qcd_files=$(ls input/Run2_UL/RunIISummer20UL16NanoAODv9/preVFP/BTagCSV*)

extra=""
for input in ${qcd_files[@]}; do
    if [[ "$input" == *"2018C"* ]] || [[ "$input" == *"2018D"* ]]; then
    extra="--correct-HEM"
    elif [[ "$input" == *"2018B"* ]]; then
    extra="--check-HEM"
    fi
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 200 --input $input --is-data --forceOverwrite $extra
done



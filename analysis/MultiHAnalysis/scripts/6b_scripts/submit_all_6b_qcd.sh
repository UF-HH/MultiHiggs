
ODIR="/store/user/srosenzw/sixb/ntuples/"

# VERSION="Run2_UL/RunIISummer20UL16NanoAODv9"
# CFG="config/skim_ntuple_2016_106X_NanoAODv9.cfg"

# VERSION="Run2_UL/RunIISummer20UL17NanoAODv9"
# CFG="config/skim_ntuple_2017_106X_NanoAODv9.cfg"

# VERSION="Run2_Autumn18"
VERSION="Run2_UL/RunIISummer20UL18NanoAODv9"
CFG="config/skim_ntuple_2018_106X_NanoAODv9.cfg"
# TAG="Summer2018UL/cutflow_studies/nocuts/QCD"
# TAG="Summer2018UL/maxbtag_4b/QCD"

# VERSION="Run2_UL/RunIISummer20UL16NanoAODv9/preVFP"
# CFG="config/skim_ntuple_2016preVFP_106X_NanoAODv9.cfg"
# TAG="Summer2016UL/preVFP/maxbtag_4b/QCD"

TAG="Summer2018UL/maxbtag_4b/QCD"
# TAG="Summer2018UL/maxbtag/QCD"
# TAG="Autumn18/maxbtag/QCD"
# TAG="Summer2018UL/btag_pt/QCD"


rm -rf /eos/uscms/$ODIR/$TAG/analysis_tar
make exe -j || exit -1

echo "... tag       : ", $TAG
echo "... saving to : ", $ODIR

# qcd_files=$(ls input/$VERSION/QCD*BGenFilter*.txt input/$VERSION/QCD*bEnriched*.txt)
# qcd_files=$(ls input/$VERSION/QCD*PSWeights*.txt)
qcd_files=$(ls input/$VERSION/QCD*BGenFilter*.txt input/$VERSION/QCD*bEnriched*.txt)

for input in ${qcd_files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --memory 2500 --forceOverwrite --maxEvts 100000
done

# python scripts/submitSkimOnBatch.py --tag Summer2018UL/cutflow_studies/nocuts/QCD  --outputDir /store/user/srosenzw/sixb/ntuples/ --cfg config/skim_ntuple_2018_106X_NanoAODv9.cfg --njobs 100 --input input/Run2_UL/RunIISummer20UL18NanoAODv9/QCD_bEnriched_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8.txt  --memory 2500 --forceOverwrite

# python scripts/submitSkimOnBatch.py --tag Summer2016UL/preVFP/maxbtag_4b/QCD  --outputDir /store/user/srosenzw/sixb/ntuples/ --cfg config/skim_ntuple_2016preVFP_106X_NanoAODv9.cfg --njobs 100 --input input/Run2_UL/RunIISummer20UL16NanoAODv9/preVFP/QCD_bEnriched_HT200to300_TuneCP5_13TeV-madgraph-pythia8.txt --memory 2500 --forceOverwrite

# python scripts/submitSkimOnBatch.py --tag Summer2017UL/maxbtag_4b/QCD  --outputDir /store/user/srosenzw/sixb/ntuples/ --cfg config/skim_ntuple_2017_106X_NanoAODv9.cfg --njobs 100 --input input/Run2_UL/RunIISummer20UL17NanoAODv9/QCD_bEnriched_HT300to500_TuneCP5_13TeV-madgraph-pythia8.txt --memory 2500 --forceOverwrite

# input/Run2_UL/RunIISummer20UL18NanoAODv9/QCD_bEnriched_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8.txt
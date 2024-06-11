# sh scripts/6b_scripts/submit_all_6b_qcd.sh

ODIR="/store/user/srosenzw/sixb/ntuples/"

VERSION="Run2_UL/RunIISummer20UL17NanoAODv9"
CFG="config/skim_ntuple_2017_106X_NanoAODv9.cfg"
TAG="Summer2017UL/maxbtag/QCD"

rm -rf /eos/uscms/$ODIR/$TAG/analysis_tar
make exe -j || exit -1

echo "... tag       : ", $TAG
echo "... saving to : ", $ODIR

# qcd_files=$(ls input/$VERSION/QCD*PSWeights*.txt)
qcd_files=$(ls input/$VERSION/QCD*BGenFilter*.txt input/$VERSION/QCD*bEnriched*.txt)

for input in ${qcd_files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --memory 2500 --forceOverwrite --no-genw-tree
done

# python scripts/submitSkimOnBatch.py --tag Summer2018UL/maxbtag_4b/QCD  --outputDir /store/user/srosenzw/sixb/ntuples/ --cfg config/skim_ntuple_2018_106X_NanoAODv9.cfg --njobs 100 --input input/Run2_UL/RunIISummer20UL18NanoAODv9/QCD_bEnriched_HT700to1000_TuneCP5_13TeV-madgraph-pythia8.txt --memory 2500 --no-genw-tree --forceOverwrite

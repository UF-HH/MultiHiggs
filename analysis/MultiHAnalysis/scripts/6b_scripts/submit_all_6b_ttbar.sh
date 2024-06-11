# sh scripts/6b_scripts/submit_all_6b_ttbar.sh

ODIR="/store/user/srosenzw/sixb/ntuples/"

VERSION="Run2_UL/RunIISummer20UL17NanoAODv9"
CFG="config/skim_ntuple_2017_106X_NanoAODv9.cfg"
TAG="Summer2017UL/maxbtag/TTJets"

rm -rf /eos/uscms/$ODIR/$TAG/analysis_tar
make exe -j || exit -1

echo "... tag       : ", $TAG
echo "... saving to : ", $ODIR

ttbar_files=$(ls input/$VERSION/TTJets_*)

for input in ${ttbar_files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --memory 4000 --forceOverwrite --no-genw-tree
done
# python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg config/skim_ntuple_2018_ttbar.cfg --njobs 100 --input input/Run2_UL/2018/SingleMuon_Run2.txt --is-data

#############

# TAG="ttbar_2018_10Jan2022"
# ODIR="/store/group/lpchbb/lcadamur/sixb_ntuples/"

# echo "... tag       : ", $TAG
# echo "... saving to : ", $ODIR

# python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg config/skim_ntuple_2018_ttbar.cfg --njobs 100 --input input/Run2_UL/2018/TTJets.txt         
# python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg config/skim_ntuple_2018_ttbar.cfg --njobs 100 --input input/Run2_UL/2018/SingleMuon_Run2.txt --is-data

# python scripts/submitSkimOnBatch.py --tag Summer2018UL/maxbtag_4b/Official_NMSSM/btagsf --outputDir /store/user/srosenzw/sixb/ntuples --cfg config/skim_ntuple_2018_106X_NanoAODv9.cfg --njobs 100 --input input/Run2_UL/RunIISummer20UL18NanoAODv9/NMSSM_XToYHTo6B/NMSSM_XToYHTo6B_MX-700_MY-400_TuneCP5_13TeV-madgraph-pythia8.txt  --is-signal --forceOverwrite
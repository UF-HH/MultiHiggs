
CFG="config/skim_ntuple_2018_106X_NanoAODv9.cfg"
ODIR="/store/user/srosenzw/sixb/ntuples/"


VERSION="Run2_UL/RunIISummer20UL18NanoAODv9"
TAG="$VERSION/TTJets/"
# TAG="Summer2018UL/cutflow_studies/presel/TTJets"
# TAG="Summer2018UL/btag_pt/TTJets"
# TAG="Summer2018UL/maxbtag/TTJets"
TAG="Summer2018UL/maxbtag_4b/TTJets"
# TAG="Summer2018UL/maxbtag_mmmm/TTJets"

rm -rf /eos/uscms$ODIR/$TAG/analysis_tar
make exe -j || exit -1

echo "... tag       : ", $TAG
echo "... saving to : ", $ODIR

# ttbar_files=$(ls input/$VERSION/TTJets_*)
ttbar_files=$(ls input/$VERSION/small_TTJets_*)


for input in ${ttbar_files[@]}; do
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --memory 2500 --forceOverwrite
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
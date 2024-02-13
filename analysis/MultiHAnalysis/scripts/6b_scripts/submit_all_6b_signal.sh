ODIR="/store/user/srosenzw/sixb/ntuples"

# TAG="Summer2016UL/maxbtag_4b/Official_NMSSM"
# CFG="config/skim_ntuple_2016postVFP_106X_NanoAODv9.cfg"
# VERSION="input/Run2_UL/RunIISummer20UL16NanoAODv9/NMSSM_XToYHTo6B"

# TAG="Summer2016UL/preVFP/maxbtag_4b/Official_NMSSM"
# CFG="config/skim_ntuple_2016preVFP_106X_NanoAODv9.cfg"
# VERSION="input/Run2_UL/RunIISummer20UL16NanoAODv9/preVFP/NMSSM_XToYHTo6B"

# TAG="Summer2017UL/maxbtag_4b/Official_NMSSM"
# CFG="config/skim_ntuple_2017_106X_NanoAODv9.cfg"
# VERSION="input/Run2_UL/RunIISummer20UL17NanoAODv9/NMSSM_XToYHTo6B"

# TAG="Summer2018UL/maxbtag_4b/Official_NMSSM"
# CFG="config/skim_ntuple_2018_106X_NanoAODv9.cfg"
# VERSION="input/Run2_UL/RunIISummer20UL18NanoAODv9/NMSSM_XToYHTo6B"

# files=$(ls $VERSION/NMSSM_XToYHTo6B_MX-*)

TAG="Summer2018UL/maxbtag/NMSSM"
CFG="config/skim_ntuple_2018_106X_NanoAODv9.cfg"
VERSION="input/PrivateMC_2018/NMSSM_XYH_YToHH_6b"
files=$(ls $VERSION/NMSSM_XYH_YToHH_6b_*)



# TAG="Summer2018UL/cutflow_studies/presel/NMSSM"
# TAG="Summer2018UL/maxbtag_4b/NMSSM"
# TAG="Summer2018UL/maxbtag/NMSSM"
# TAG="Summer2018UL/maxbtag/Official_NMSSM"
# TAG="Summer2018UL/btag_pt/NMSSM"


rm -rf /eos/uscms/$ODIR/$TAG/analysis_tar
make exe -j || exit -1

echo "... tag       : ", $TAG
echo "... saving to : ", $ODIR


for input in ${files[@]}; do
    # tmp=${input#*XToYHTo6B_}   # remove prefix ending in "XToYHTo6B_"
    # b=${tmp%_Tune*}   # remove suffix starting with "_Tune"
    # mx=${b#*MX-}   # remove prefix ending in "_"
    # mx=${mx%_MY*}   # remove prefix ending in "_"
    # my=${b#*_MY-}   # remove prefix ending in "_"

    tmp=${input#*NMSSM_XYH_YToHH_6b_}   # remove prefix ending in "NMSSM_XYH_YToHH_6b_"
    tmp=${tmp%.txt*} 
    tmp=${tmp%_1M} 
    tmp=${tmp%_2M} 
    tmp=${tmp%_3M} 
    tmp=${tmp%_4M} 
    tmp=${tmp%_5M} 
    tmp=${tmp%_10M} 
    tmp=${tmp%_*k*} 
    mx=${tmp#*MX_}   
    mx=${mx%_MY*}   
    my=${tmp#*_MY_}   

    mx=$(($mx))
    my=$(($my))

    # tmp=${input%.*}
    memory=3000
    # if [[ ${tmp:0-1}="M" ]]; then
    #     memory=4000
    # fi
    if [[ $mx -gt 1200 ]]; then
        echo ".. skipping because mx=$mx" 
        continue
    fi
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-signal --forceOverwrite --memory 4000
done


# python scripts/submitSkimOnBatch.py --tag Summer2018UL/maxbtag_4b/Official_NMSSM/ --outputDir /store/user/srosenzw/sixb/ntuples --cfg config/skim_ntuple_2018_106X_NanoAODv9.cfg --njobs 100 --input input/Run2_UL/RunIISummer20UL18NanoAODv9/NMSSM_XToYHTo6B/NMSSM_XToYHTo6B_MX-1200_MY-400_TuneCP5_13TeV-madgraph-pythia8.txt --is-signal --forceOverwrite --memory 3000

# python scripts/submitSkimOnBatch.py --tag Summer2017UL/maxbtag_4b/Official_NMSSM --outputDir /store/user/srosenzw/sixb/ntuples --cfg config/skim_ntuple_2017_106X_NanoAODv9.cfg --njobs 100 --input input/Run2_UL/RunIISummer20UL17NanoAODv9/NMSSM_XToYHTo6B/NMSSM_XToYHTo6B_MX-700_MY-400_TuneCP5_13TeV-madgraph-pythia8.txt  --is-signal --forceOverwrite

# python scripts/submitSkimOnBatch.py --tag Summer2016UL/maxbtag_4b/Official_NMSSM --outputDir /store/user/srosenzw/sixb/ntuples --cfg config/skim_ntuple_2016postVFP_106X_NanoAODv9.cfg --njobs 100 --input input/Run2_UL/RunIISummer20UL16NanoAODv9/NMSSM_XToYHTo6B/NMSSM_XToYHTo6B_MX-700_MY-400_TuneCP5_13TeV-madgraph-pythia8.txt  --is-signal --forceOverwrite

# python scripts/submitSkimOnBatch.py --tag Summer2018UL/maxbtag_4b/Official_NMSSM/syst/FlavorQCD/up --outputDir /store/user/srosenzw/sixb/ntuples --cfg config/skim_ntuple_2018_106X_NanoAODv9.cfg --njobs 100 --input input/Run2_UL/RunIISummer20UL18NanoAODv9/NMSSM_XToYHTo6B/NMSSM_XToYHTo6B_MX-750_MY-500_TuneCP5_13TeV-madgraph-pythia8.txt --is-signal --jes-shift-syst FlavorQCD:up --forceOverwrite

# python scripts/submitSkimOnBatch.py --tag Summer2018UL/maxbtag/NMSSM --outputDir /store/user/srosenzw/sixb/ntuples --cfg config/skim_ntuple_2018_106X_NanoAODv9.cfg --njobs 100 --input input/PrivateMC_2018/NMSSM_XYH_YToHH_6b/NMSSM_XYH_YToHH_6b_MX_700_MY_400.txt  --is-signal --forceOverwrite

# LIMITED USE - for producing central samples at maxbtag level
# python scripts/submitSkimOnBatch.py --tag Summer2018UL/maxbtag/Official_NMSSM --outputDir /store/user/srosenzw/sixb/ntuples --cfg config/skim_ntuple_2018_106X_NanoAODv9.cfg --njobs 100 --input input/Run2_UL/RunIISummer20UL18NanoAODv9/NMSSM_XToYHTo6B/NMSSM_XToYHTo6B_MX-450_MY-300_TuneCP5_13TeV-madgraph-pythia8.txt  --is-signal --forceOverwrite
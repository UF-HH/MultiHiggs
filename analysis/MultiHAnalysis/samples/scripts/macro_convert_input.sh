#!/bin/bash

SAMPLES=(
    "JetHT=JetHT_Run*txt"
    "QCD_PSWeights=QCD*PSWeights*txt"
    "QCD_bEnriched=QCD*bEnriched*txt"
    "QCD_BGenFilter=QCD*BGenFilter*txt"
    "TTJets_MLM=TTJets*MLM*txt"
    "TTJets_FXFX=TTJets*FXFX*txt"
    "TTbar=TTTo*txt"
)

DIRECTORY=(
    Run2_UL/RunIISummer20UL16NanoAODv9  
    Run2_UL/RunIISummer20UL17NanoAODv9  
    Run2_UL/RunIISummer20UL18NanoAODv9
)

for sample in "${SAMPLES[@]}"; do
    pattern=${sample/*=/}
    sample=${sample/=*/}

    for dir in "${DIRECTORY[@]}"; do
        INPUT=../input/$dir/$pattern
        NFILES=$(ls -1 $INPUT | wc -l)

        if [[ $NFILES -eq 0 ]]; then
            echo ... skipping
            continue
        fi

        bash scripts/convert_input.sh $dir/$sample.py $INPUT
    done

done
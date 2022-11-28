#!/bin/sh

while getopts v:b:r:t: flag
do
    case "${flag}" in
	# Changeable Default Arguments
	v) region=${OPTARG};;
	b) tag=${OPTARG}/;;
	
	# Argument handler script for submission scripts
	r) region=${OPTARG};;
	t) tag=${OPTARG}/;;
    esac
done

case "${region}" in
    "sr")
	TAG="SR/${tag}"
	CFG="config/skim_ntuple_2018_106X_NanoAODv9_marina.cfg";;
    "qcd")
	TAG="QCD_SR/${tag}"
	CFG="config/skim_ntuple_2018_106X_NanoAODv9_marina.cfg";;
    "cr")
	TAG="Higgs_CR/${tag}"
	CFG="config/skim_ntuple_2018_106X_NanoAODv9_marina.cfg";;
    *)
	TAG="SR/${tag}"
	CFG="config/skim_ntuple_2018_106X_NanoAODv9_marina.cfg";;
esac

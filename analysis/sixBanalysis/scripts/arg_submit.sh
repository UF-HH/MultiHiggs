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
	CFG="config/skim_ntuple_2018.cfg";;
    "qcd")
	TAG="QCD_SR/${tag}"
	CFG="config/skim_ntuple_2018_qcd.cfg";;
    "cr")
	TAG="Higgs_CR/${tag}"
	CFG="config/skim_ntuple_2018_cr.cfg";;
    *)
	TAG="SR/${tag}"
	CFG="config/skim_ntuple_2018.cfg";;
esac

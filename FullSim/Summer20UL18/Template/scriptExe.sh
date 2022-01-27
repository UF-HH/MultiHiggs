#!/bin/bash
BASE=$PWD
nEvents=500

echo "================= CMSRUN starting jobNum=$1 ====================" | tee -a job.log
export SCRAM_ARCH=slc7_amd64_gcc700
source /cvmfs/cms.cern.ch/cmsset_default.sh

build_cmssw() {

    echo "================= CMSRUN setting up CMSSW_$1 ===================="| tee -a job.log
    if [ -r CMSSW_$1/src ] ; then 
    echo release CMSSW_$1 already exists
    else
    scram p CMSSW CMSSW_$1
    fi
    
    cd CMSSW_$1/src
    eval `scram runtime -sh`

    cd $BASE
}

build_cmssw 10_6_19_patch3
echo "================= CMSRUN starting GEN-SIM step ====================" | tee -a job.log
cmsRun -j genSim_step.log genSim_step.py jobNum=$1 nEvents=$nEvents || exit $? ;

build_cmssw 10_6_17_patch1
echo "================= CMSRUN starting DIGI-PREMIX step ====================" | tee -a job.log
cmsRun -j digiRaw_step.log digiPremix_step.py nEvents=$nEvents || exit $? ;

build_cmssw 10_2_16_UL
echo "================= CMSRUN starting HLT step ====================" | tee -a job.log
cmsRun -j hlt_step.log hlt_step.py nEvents=$nEvents || exit $? ;

build_cmssw 10_6_17_patch1
echo "================= CMSRUN starting RECO-AOD step ====================" | tee -a job.log
cmsRun -j recoAOD_step.log recoAOD_step.py nEvents=$nEvents || exit $? ;

echo "================= CMSRUN starting MiniAOD step  ====================" | tee -a job.log
# cmsRun -e -j FrameworkJobReport.xml miniAOD_step.py nEvents=$nEvents
cmsRun -j miniAOD_step.log miniAOD_step.py nEvents=$nEvents || exit $? ;

build_cmssw 10_6_19_patch2
echo "================= CMSRUN starting NanoAOD step  ====================" | tee -a job.log
cmsRun -e -j FrameworkJobReport.xml nanoAOD_step.py || exit $? ;

echo "================= CMSRUN finished ====================" | tee -a job.log

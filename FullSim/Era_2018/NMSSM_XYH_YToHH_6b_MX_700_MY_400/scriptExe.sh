#!/bin/bash
BASE=$PWD

echo "================= CMSRUN starting jobNum=$1 ====================" | tee -a job.log
export SCRAM_ARCH=slc7_amd64_gcc700
source /cvmfs/cms.cern.ch/cmsset_default.sh

echo "================= CMSRUN setting up CMSSW_10_2_22 ===================="| tee -a job.log
if [ -r CMSSW_10_2_22/src ] ; then 
 echo release CMSSW_10_2_22 already exists
else
scram p CMSSW CMSSW_10_2_22
fi

cd CMSSW_10_2_22/src
eval `scram runtime -sh`

cd $BASE

echo "================= CMSRUN starting GEN-SIM step ====================" | tee -a job.log
cmsRun -j genSim_step.log genSim_step.py jobNum=$1 nEvents=1000 

echo "================= CMSRUN starting DIGI-RAW step ====================" | tee -a job.log
cmsRun -j digiRaw_step.log digiRaw_step.py nEvents=1000

echo "================= CMSRUN starting RECO-AOD step ====================" | tee -a job.log
cmsRun -j recoAOD_step.log recoAOD_step.py nEvents=1000

echo "================= CMSRUN starting MiniAOD step  ====================" | tee -a job.log
# cmsRun -e -j FrameworkJobReport.xml miniAOD_step.py nEvents=1000
cmsRun -j miniAOD_step.log miniAOD_step.py nEvents=1000

echo "================= CMSRUN starting NanoAOD step  ====================" | tee -a job.log
cmsRun -e -j FrameworkJobReport.xml nanoAOD_step.py

echo "================= CMSRUN finished ====================" | tee -a job.log

## Setting up tar ball of the skimmer code

    cd workdir/
    source /cvmfs/cms.cern.ch/cmsset_default.sh
    export SCRAM_ARCH=slc7_amd64_gcc700
    cmsrel CMSSW_10_6_28
    cd CMSSW_10_6_28/src/
    cmsenv
    git cms-addpkg CommonTools/Utils CondFormats/JetMETObjects CondFormats/Serialization FWCore/MessageLogger FWCore/Utilities JetMETCorrections/Modules PhysicsTools/TensorFlow PhysicsTools/ONNXRuntime
    scram b -j
    git clone https://github.com/UF-HH/MultiHiggs
    cd MultiHiggs/analysis/MultiHAnalysis
    source scripts/setup.sh
    make exe -j
    tar -chJf tars/sixBanalysis.tar.xz bin/ lib/ config/ data/ models/

The sixBanalysis.tar.xz is the tarball that each condor job will run.


## Setup grid certificate

On UAF machine, if you just got the account you won't have the grid certificate.
So do the usual setup thingy with pkcs12 yada.

## Setting up ProjectMetis

New terminal preferred.

    ssh uaf-10
    cd workdir/
    git clone https://github.com/aminnj/ProjectMetis.git
    cd ProjectMetis
    voms-proxy-init -hours 168 -voms cms -rfc # to setup proxy
    source setup.sh
    cd ../
    cp /home/users/phchang/public_html/dump/forEvan/sixbskim/samples.py .
    cp /home/users/phchang/public_html/dump/forEvan/sixbskim/submit.py .
    cp /home/users/phchang/public_html/dump/forEvan/sixbskim/condor_executable_metis.sh .
    cp /path/to/workdir/tars/sixBanalysis.tar.xz .
    python submit.py #edit submit.py for different tag name and etc.

## What to update and change

In samples.py add samples using "DBSSample".

For private samples, use "DirectorySample" to give the path in ```/ceph/``` area and give a user defined name

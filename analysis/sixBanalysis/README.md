## Installation

```
cmsrel CMSSW_10_6_28
cd CMSSW_10_6_28/src
cmsenv
git cms-addpkg CommonTools/Utils CondFormats/JetMETObjects CondFormats/Serialization FWCore/MessageLogger FWCore/Utilities JetMETCorrections/Modules PhysicsTools/TensorFlow PhysicsTools/ONNXRuntime
scram b -j 4
git clone https://github.com/UF-HH/sixB
cd sixB/analysis/sixBanalysis/
source scripts/setup.sh
make exe -j
```

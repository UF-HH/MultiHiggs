## Installation

```
cmsrel CMSSW_10_2_18
cd CMSSW_10_2_18/src
cmsenv
git cms-addpkg CommonTools/Utils CondFormats/JetMETObjects CondFormats/Serialization FWCore/MessageLogger FWCore/Utilities JetMETCorrections/Modules
scram b -j 4
git clone https://github.com/ekoenig4/sixB
cd sixB/analysis/sixBanalysis/
source scripts/setup.sh
make exe -j
```

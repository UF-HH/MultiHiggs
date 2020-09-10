# sixB

## Generator level studies

### Install instruction

Note:
   * CMSSW recommended release from [here](https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookWhichRelease)
   * MadGraph version as in the gen scripts [here](https://github.com/cms-sw/genproductions/blob/master/bin/MadGraph5_aMCatNLO/gridpack_generation.sh)

```
# install CMSSW release
cmsrel CMSSW_10_2_18
cd CMSSW_10_2_18/src
git clone https://github.com/UF-HH/sixB
cd sixB

# install MadGraph
cd MadGraph
wget https://cms-project-generators.web.cern.ch/cms-project-generators/MG5_aMC_v2.6.5.tar.gz
tar xzf MG5_aMC_v2.6.5.tar.gz

# now install the BSM model for the process
cd MG5_aMC_v2_6_5
wget https://cms-project-generators.web.cern.ch/cms-project-generators/NMSSMHET_UFO_fermioncouplings.zip
cd models
unzip ../NMSSMHET_UFO_fermioncouplings.zip
```

### Running instructions

These steps allow for generating a LHE file and run Pythia (within the CMSSW framework) on top of it.

#### LHE step

To generate the MadGraph process (needed only once) see below.
It will generate the diagrams and copy updated run and param cards to the destination folder called ``X_YH_HHH_6b``.

```
cd MadGraph/scripts
source setup_process.sh
```

To generate a LHE file see below. Note that this takes approx 30s for 10 000 events, so can be reasonably run locally with minimal parallelisation.

NOTE: to run a parallelisation of this step, one has to copy the X_YH_HHH_6b and run multiple copies of the script, adapting the folder name (MadGraph can generate one LHE at the time in a given folder)

```
source generate_LHE.sh <mX> <mY> [nevents: default 10000]
```

This will create a folder with the zipped LHE file under ``MG5_aMC_v2_6_5/X_YH_HHH_6b/Events/gen6b_<mX>_<mY>``
# 6b Analysis

## Table of Contents
- [6b Analysis](#6b-analysis)
  - [Table of Contents](#table-of-contents)
  - [Install Instructions](#install-instructions)
  - [Gridpack Generation](#gridpack-generation)
  - [Running Instructions](#running-instructions)
    - [LHE step](#lhe-step)
      - [Hadronisaton and ntuple step](#hadronisaton-and-ntuple-step)
    - [Content and description of the ntuples](#content-and-description-of-the-ntuples)
  - [Perform Skim on NTuples](#perform-skim-on-ntuples)
  - [HiggsCombine](#higgscombine)

## Repository Contents

This repository contains three projects:

1. Sample skimming for Multi-Higgs analyses

This project is used to skim both private and centrally-produced samples. For instructions on how to perform skims, see [analysis/MultiHAnalysis](https://github.com/UF-HH/MultiHiggs/tree/master/analysis/MultiHAnalysis).

2. Gridpack production with MadGraph5

This project is used to produce gridpacks, which are used for gen-level event generation (located in `MadGraph/`). See installation and running instructions below.

3. Full simulation private sample generation 

This project is used to generate event simulations that propagate the gen-level events through the detectors. For instructions on how to perform skims, see [FullSim](https://github.com/UF-HH/MultiHiggs/tree/master/FullSim).



## Install Instructions

Note:
   * CMSSW recommended release from [here](https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookWhichRelease)
   * MadGraph version as in the gen scripts [here](https://github.com/cms-sw/genproductions/blob/master/bin/MadGraph5_aMCatNLO/gridpack_generation.sh)

Follow these steps to install CMSSW, MadGraph, and the BSM model

```
# install CMSSW release
cmsrel CMSSW_10_6_28_patch2
cd CMSSW_10_6_28_patch2/src
cmsenv
git cms-addpkg CommonTools/Utils CondFormats/JetMETObjects CondFormats/Serialization FWCore/MessageLogger FWCore/Utilities JetMETCorrections/Modules PhysicsTools/TensorFlow PhysicsTools/ONNXRuntime
scram b -j 4
git clone https://github.com/UF-HH/MultiHiggs

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

## Gridpack Generation

Sample event production can be done through the manual production of LHE events through MadGraph and hadronization of LHE events through Pythia. See [Running Instructions (Manual)](#running-instructions).

Sample event production can also be done by generating a gridpack (consisting of several mass points) and using [genproductions](https://github.com/cms-sw/genproductions). See [MadGraph/gridpacks/README.md](https://github.com/UF-HH/sixB/tree/master/MadGraph/gridpacks) for instructions to generate the cards and [Quick tutorial on how to produce a gridpack](https://twiki.cern.ch/twiki/bin/viewauth/CMS/QuickGuideMadGraph5aMCatNLO#Quick_tutorial_on_how_to_produce)

After running `python generate_grid.py`, navigate to the directory `sixB/MadGraph/gridpacks/genproductions/bin/MadGraph5_aMCatNLO/` and modify and run `sh generate_6b_gridpacks.sh`. This will generate the tarballs, which you can copy to `FullSim/Summer20UL18/Template/`, in which you can modify `genSim_step.py` and `crabConfig.py` and submit each Full Sim sample to CRAB via the command `crab submit crabConfig.py`.

### Running Instructions


These steps allow for generating an LHE file and run Pythia (within the CMSSW framework) on top of it.
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

To uncompress the file for running the Pythia step, use ``gunzip filename.tar.gz``.

#### Hadronisaton and ntuple step

This step runs Pythia within CMSSW on top of the previously produced LHE file.
First you need to compile the code with ``scram b -j 4`` (just once).

To run on a single file locally:

```
cd PythiaAndNtuples
cmsRun pythia_and_ntuples.py inputFiles=file:/path/to/the/LHE outputFile=output_file_name.root
```

This step takes approximately 90s to hadronise and ntuplise 1000 events (a few error messages from Pythia may appear) when running locally.

For test purposes you can add at the end ``maxEvents=<num_events>`` (e.g. to run on 100 events)


#### Content and description of the ntuples

Conventions:
   * The particles in the process are labeled as X &#8594; Y HX, and Y &#8594; HY1 HY2. The three H bosons (HX, HY1, HY2) decay to b1 b2.
   * Objects are ordered in pt, so that pt(HY1) > pt(HY1) and pt(b1) > pt (b2) .
   * The first and last copy of the bosons in the hadronisation are labelled ``fc`` and ``lc`` respectively. Note that this only matters for X, as Y, HX, HY1, HY2 are identical between ``lc`` and ``fc``

Content:
   * A vector of pt/eta/phi/m of all the genjets satisfying minimal pt requirements (both in the cases where the neutrinos are clustered and are not clustered in the jet)
   * The pt/eta/phi/m of the gen particles as individual floats X, Y, HY, HY1, HY1, HY_b1, HY_b2, HY1_b1, HY1_b2, HY1_b1, HY1_b2
   * For every gen b the index of the genjet matched (matched = the closest within a cone dR = 0.4). Value ``-1`` if no match found

## Perform Skim on NTuples

For instructions on how to perform skims, see [analysis/MultiHAnalysis](https://github.com/UF-HH/MultiHiggs/tree/master/analysis/MultiHAnalysis).

## HiggsCombine

See [this page](https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/#for-end-users-that-dont-need-to-commit-or-do-any-development) for instructions on how to install and run Combine ([HiggsAnalysis-CombinedLimit GitHub](https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit))

Notes:
- Documentation recommends using CMSSW_10_2_18 to run Combine
- Must start a new shell to run Combine (i.e., no cms environments)
- 

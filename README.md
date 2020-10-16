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

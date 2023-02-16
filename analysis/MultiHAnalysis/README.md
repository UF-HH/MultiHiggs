## Installation

Please see the README.md in the root folder before attempting to run these skims if you haven't already. Once installation of the repo has been completed, follow these steps to set up the analysis code.

```
source scripts/setup.sh
make exe -j
```

## Run Skims

- Executable file is `bin/skim_ntuple.exe`
- Config files are located in `config/` directory
- Input files are located in `input/` directory (make sure to update these any time new samples are generated)

### To run a skim locally
The executable is run with command line options which can be printed out using 
```
./bin/skim_ntuple.exe --help
```

The main required options to run the script are
```
./bin/skim_ntuple.exe --input input/${file_list}.txt --cfg  config/${skim_config}.cfg --output ${output_file_name}.root
```

The shell script `run_skim.sh` can be modified to run on desired input file (remember to include `--is-signal` for signal files and `--is-data` for data files) with desired config file. Any command line argument passed to `run_skim.sh` are passed directly to `bin/skim_ntuple.exe`. You can change the max number of events to run on with `--maxEvts 1000`, for example. 
```
sh run_skim.sh --maxEvts 1000
```

### To submit skim jobs to Condor

Scripts to submit jobs to condor are in `scripts/` directory. Options are included to make it simple to submit jobs with no cuts `-n`, only apply preselections `-p`, jet energy scale `--jes` and jet energy resolution `--jer`, or to select events by btag `-b`.

```
sh scripts/submit_all_signal.sh
```

### Calculating B-Tag Efficiency

The [skim_btageff.cpp](test/skim_btageff.cpp) script can be used to calculate the efficiencies using the output from [skim_ntuple.cpp](test/skim_ntuple.cpp). A config needs to be used that defines 

```yaml
[parameters]
# year used to fetch the correct cross sections
year = 2018

# Cuts for WP : Loose, Medium, Tight WPs
bTagWPDef = 0.0490, 0.2783, 0.7100  

# Path to a cross section config
xsec = data/xsec/mc_2018.cfg

# Base path used for each sample 
path = /eos/uscms/store/user/ekoenig/8BAnalysis/NTuples/2018/preselection/t8btag_minmass/Run2_UL/RunIISummer20UL18NanoAODv9/

# !! OPTIONAL: to disable and use all jets available just comment out
[select]
# Will restrict to using only the first maxjets jets in each event
maxjets = 8

# Specifies a variable to use to order the jets before selecting 
value = btag

# List of qcd samples to use for efficiencies
[qcd]
# Each sample should match a sample in the cross section config
QCD_bEnriched_HT1500to2000 = /QCD/QCD_bEnriched_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/ntuple.root
QCD_bEnriched_HT2000toInf  = /QCD/QCD_bEnriched_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/ntuple.root

# List of ttbar samples to use for efficiencies
[ttbar]
TTJets = /TTJets/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/ntuple_*.root
```

More QCD and TTbar samples can be added in the proper sections. The filenames support glob. With a config, the script can be run as

```bash
make exe -j
./bin/skim_btageff.cpp --cfg /path/to/config.cfg --out /path/to/output.root
```

In the output.root file, there will be a qcd, ttbar, and eff folder. The eff folder has the final efficiencies in pt, eta, and 2D pt eta. Hadron flavors are labeled as: hf0 = guds, hf4 = c, and hf5 = b. The qcd and ttbar folders have the histograms used to calculate the efficiencies. Only QCD is used to calculate guds and TTbar is used to calculate c and b, although all hadron flavour histograms are saved in the qcd and ttbar folder.

A plotter is provided in [plotter/plot_btag_efficiency.py](plotter/plot_btag_efficiency.py). This script needs to be run in a fresh shell, and can be ran using

```bash
cd plotter 
source setup.sh
./plot_btag_efficiency.py --input /path/to/btageff_output.root --output /path/to/save/plots/to/ --analysis NMSSM_XYY_YToHH_8b --year 2018
```

The analysis and year options are optional, but they are default to 8b and 2018. 

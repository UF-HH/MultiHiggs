## Installation

Please see the README.md in the root folder before attempting to run these skims if you haven't already. Once installation of the repo has been completed, follow these steps to set up the analysis code.

```
source scripts/setup.sh
make exe -j
```

## Run Skims

- Config files are located in `config/` directory
- Input files are located in `input/` directory (make sure to update these any time new samples are generated)

### To run a skim locally

Modify `run_skim.sh` to run on desired input file (remember to include `--is-signal` for signal files and `--is-data` for data files) with desired config file. You can specify the max number of events to run on with `--maxEvts 1000`, for example.
```
sh run_skim.sh --maxEvts 1000
```

### To submit skim jobs to Condor

Scripts to submit jobs to condor are in `scripts/` directory. Options are included to make it simple to submit jobs with no cuts `-n`, only apply preselections `-p`, jet energy scale `--jes` and jet energy resolution `--jer`, or to select events by btag `-b`.

```
sh scripts/submit_all_signal.sh
```
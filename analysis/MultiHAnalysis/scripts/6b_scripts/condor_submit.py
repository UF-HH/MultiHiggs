#!/usr/bin/env python

from argparse import ArgumentParser
import subprocess, os
from glob import glob

# subprocess.check_call(["make -j exe"])

masslist = [
    'MX-700_MY-250',
    # 'MX-700_MY-300',
    'MX-700_MY-350',
    'MX-700_MY-400',
    'MX-700_MY-450',
    'MX-700_MY-500'

    'MX-800_MY-250',
    # 'MX-800_MY-300',
    # 'MX-800_MY-350',
    'MX-800_MY-400',
    'MX-800_MY-450',
    'MX-800_MY-500',
    'MX-800_MY-600'

    'MX-900_MY-250',
    # 'MX-900_MY-300',
    'MX-900_MY-350',
    # 'MX-900_MY-400',
    'MX-900_MY-450',
    'MX-900_MY-500',
    'MX-900_MY-600',
    'MX-900_MY-700'

    'MX-1000_MY-250',
    # 'MX-1000_MY-350',
    'MX-1000_MY-400',
    # 'MX-1000_MY-450',
    'MX-1000_MY-500',
    'MX-1000_MY-600',
    'MX-1000_MY-700',
    'MX-1000_MY-800'

    'MX-1100_MY-250',
    'MX-1100_MY-300',
    'MX-1100_MY-350',
    'MX-1100_MY-400',
    'MX-1100_MY-450',
    'MX-1100_MY-500',
    'MX-1100_MY-600',
    'MX-1100_MY-700',
    'MX-1100_MY-800',
    'MX-1100_MY-900',

    'MX-1200_MY-1000',
    'MX-1200_MY-250',
    'MX-1200_MY-300',
    'MX-1200_MY-350',
    'MX-1200_MY-400',
    # 'MX-1200_MY-450',
    'MX-1200_MY-600',
    'MX-1200_MY-700',
    'MX-1200_MY-800',
    'MX-1200_MY-900'
]

sample_defaults = dict(
    feynnet=dict(
        files=["input/Run2_UL/RunIISummer20UL18NanoAODv9/NMSSM_XToYHTo6B/NMSSM_XToYHTo6B_%s_TuneCP5_13TeV-madgraph-pythia8.txt" % mass for mass in masslist],
        tag="NMSSM_XYH_YToHH_6b",
        njobs=100,
        forceOverwrite=True,
        is_signal=True,
    ),
    signal=dict(
        files=["input/Run2_UL/RunIISummer20UL18NanoAODv9/NMSSM_XToYHTo6B/NMSSM_XToYHTo6B_*_TuneCP5_13TeV-madgraph-pythia8.txt"],
        tag="NMSSM_XYH_YToHH_6b",
        njobs=100,
        forceOverwrite=True,
        is_signal=True,
    ),
    qcdb=dict(
        files=["input/Run2_UL/RunIISummer20UL18NanoAODv9/QCD*BGenFilter*.txt", "input/Run2_UL/RunIISummer20UL18NanoAODv9/QCD*bEnriched*.txt"],
        tag="Run2_UL/RunIISummer20UL18NanoAODv9/QCD",
        njobs=100,
        forceOverwrite=True,
    ),
    qcdb_2017=dict(
        files=["input/Run2_UL/RunIISummer20UL17NanoAODv9/QCD*BGenFilter*.txt", "input/Run2_UL/RunIISummer20UL17NanoAODv9/QCD*bEnriched*.txt"],
        tag="Run2_UL/RunIISummer20UL17NanoAODv9/QCD",
        njobs=100,
        forceOverwrite=True,
    ),
    qcdht=dict(
        files=["input/Run2_UL/RunIISummer20UL18NanoAODv9/QCD*PSWeight*.txt"],
        # files=["input/Run2_UL/RunIISummer20UL18NanoAODv9/QCD*700to1000*PSWeight*.txt"],
        tag="Run2_UL/RunIISummer20UL18NanoAODv9/QCD",
        njobs=100,
        forceOverwrite=True,
    ),
    ttbar=dict(
        files=["input/Run2_UL/RunIISummer20UL18NanoAODv9/TTTo*.txt"],
        tag="Run2_UL/RunIISummer20UL18NanoAODv9/TTJets",
        njobs=150,
        forceOverwrite=True,
    ),
    ttjet=dict(
        files=["input/Run2_UL/RunIISummer20UL18NanoAODv9/TTJets*.txt"],
        tag="Run2_UL/RunIISummer20UL18NanoAODv9/TTJets",
        njobs=150,
        forceOverwrite=True,
    ),
    ttjet_2017=dict(
        files=["input/Run2_UL/RunIISummer20UL17NanoAODv9/TTJets*.txt"],
        tag="Run2_UL/RunIISummer20UL17NanoAODv9/TTJets",
        njobs=150,
        forceOverwrite=True,
    ),
    data=dict(
        files=["input/Run2_UL/RunIISummer20UL18NanoAODv9/JetHT_Run2018*.txt"],
        tag="Run2_UL/RunIISummer20UL18NanoAODv9/JetHT_Data",
        njobs=200,
        forceOverwrite=True,
        is_data=True,
    )
)


parser = ArgumentParser()

parser.add_argument("-p","--path", default="/store/user/ekoenig/6BAnalysis/NTuples/2018", help="master path to use for condor output")
parser.add_argument("-o","--odir", help="output directory to cat onto path; path/odir")
parser.add_argument("-c","--cfg",  help="config to use in skim")

parser.set_defaults(
    odir="feynnet",
    cfg="config/6b_config/skim_ntuple_2018_feynnet.cfg"
)

subparser = parser.add_subparsers(dest='sample')
def add_parser(sample, defaults):
    sample_parser = subparser.add_parser(sample)
    for key, value in defaults.items():
        kwargs = dict(default=value)
        if isinstance(value, list): kwargs['nargs'] = "*"
        sample_parser.add_argument("--"+key, **kwargs)

    return sample_parser

sample_parsers = [ add_parser(sample, defaults) for sample, defaults in sample_defaults.iteritems() ]
args, submit_args = parser.parse_known_args()

samplelist = [ fn for filelist in args.files for fn in glob(filelist) ]
outputDir = os.path.join(args.path, args.odir)

kwargs = ["--outputDir",outputDir]

for key,value in vars(args).items():
    if key in ['files','path','odir','sample']: continue
    kwargs.append("--"+key.replace('_','-'))
    if isinstance(value, list):
        kwargs = kwargs + value
    elif not isinstance(value, bool):
        kwargs.append( str(value) )

kwargs = kwargs + submit_args

tar = "/eos/uscms/%s/%s/analysis_tar/sixBanalysis.tar.gz" % (outputDir, args.tag)
if os.path.exists(tar):
    print('... removing %s' % tar)
    os.remove(tar)

for sample in samplelist:
    command = ['python','scripts/submitSkimOnBatch.py', '--input', sample] + kwargs
    print(' '.join(command))
    subprocess.check_call(command)
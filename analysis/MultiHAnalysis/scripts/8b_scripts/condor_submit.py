#!/usr/bin/env python

from argparse import ArgumentParser
import subprocess, os
from glob import glob

# subprocess.check_call(["make -j exe"])

sample_defaults = dict(
    signal=dict(
        files=["input/PrivateMC_2018/NMSSM_XYY_YToHH_8b/*.txt"],
        tag="NMSSM_XYY_YToHH_8b",
        njobs=100,
        forceOverwrite=True,
    ),
    training=dict(
        files=["input/PrivateMC_2018/NMSSM_XYY_YToHH_8b/training_5M/*.txt"],
        tag="NMSSM_XYY_YToHH_8b",
        njobs=100,
        forceOverwrite=True,
    ),
    qcd=dict(
        files=["input/Run2_UL/RunIISummer20UL18NanoAODv9/QCD*BGenFilter*.txt", "input/Run2_UL/RunIISummer20UL18NanoAODv9/QCD*bEnriched*.txt"],
        tag="Run2_UL/RunIISummer20UL18NanoAODv9/QCD",
        njobs=100,
        forceOverwrite=True,
    ),
    ttbar=dict(
        files=["input/Run2_UL/RunIISummer20UL18NanoAODv9/TT*.txt"],
        tag="Run2_UL/RunIISummer20UL18NanoAODv9/TTJets",
        njobs=150,
        forceOverwrite=True,
    ),
    data=dict(
        files=["input/Run2_UL/RunIISummer20UL18NanoAODv9/JetHT_Run2018*.txt"],
        tag="Run2_UL/RunIISummer20UL18NanoAODv9/JetHT_Data",
        njobs=200,
        forceOverwrite=True,
    )
)


parser = ArgumentParser()

parser.add_argument("-p","--path", default="/store/user/ekoenig/8BAnalysis/NTuples/2018", help="master path to use for condor output")
parser.add_argument("-o","--odir", help="output directory to cat onto path; path/odir")
parser.add_argument("-c","--cfg",  help="config to use in skim")

parser.set_defaults(
    odir="preselection/t8btag_minmass",
    cfg="config/8b_config/skim_ntuple_2018_t8btag_minmass.cfg"
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
sampleflag = '--is-signal' if args.sample in ['signal','training'] else '--is-data' if args.sample == 'data' else None

kwargs = ["--outputDir",outputDir]
if sampleflag: kwargs.append(sampleflag)

for key,value in vars(args).items():
    if key in ['files','path','odir','sample']: continue
    kwargs.append("--"+key)
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
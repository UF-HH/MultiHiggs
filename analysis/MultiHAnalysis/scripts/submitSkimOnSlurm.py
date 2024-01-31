#!/

import condortools.inputsplit as inputtools
import condortools.eostools as eostools
import condortools.scriptgen as scripttools

def exists(path):
    if path.startswith('/store/user/'):
        return eostools.exists_on_eos(path)
    else:
        return os.path.exists(path)
    
def makedir(path):
    if path.startswith('/store/user/'):
        return eostools.makedir_on_eos(path)
    else:
        if not os.path.exists(path):
          return os.makedirs(path)
        
def copy(input, output, eos_server):
    if output.startswith('/store/user/'):
      print_("[INFO] transmitting to EOS at", output)
      command = 'xrdcp -f -s {} {}{}'.format(input, eos_server, output)
      if os.system(command) != 0:
          print_("[ERROR] Could not xrdcp the tar to remote, aborting")
          raise RuntimeError("xrdcp of tar failed")
    else:
      print_("[INFO] transmitting to local at", output)
      command = 'cp {} {}'.format(input, output)
      if os.system(command) != 0:
          print_("[ERROR] Could not cp the tar to local, aborting")
          raise RuntimeError("cp of tar failed")
    
def print_(*args):
    # python 2 print_(function)
    print " ".join([str(x) for x in args])

import os
import sys
import argparse
import getpass

parser = argparse.ArgumentParser(description='Command line parser of skim options')
parser.add_argument('--input'     ,  dest = 'input'     ,  help = 'input filelist'           ,  required = True        )
parser.add_argument('--tag'       ,  dest = 'tag'       ,  help = 'production tag'           ,  required = True        )
parser.add_argument('--njobs'     ,  dest = 'njobs'     ,  help = 'njobs'                    ,  type     = int         ,   default = 50    )
parser.add_argument('--jes-shift-syst'     ,  dest = 'jes'     ,  help = 'jes'                    ,  type     = str         ,   default = ""    )
parser.add_argument('--memory'    ,  dest = 'memory'    ,  help = 'request memory'           ,  type     = int         ,   default = None  )
#### --------------------------------------------------- - expert usage
parser.add_argument('--outputName', dest='oname',  help='the name of the directory of this sample (if not given, auto from filelist)', default = None)
parser.add_argument('--outputDir',  dest='odir',   help='the base EOS output directory. Use a {0} for username placeholder, or give it explicitely', default = "/store/user/{0}/sixb_ntuples/")
#### --------------------------------------------------- - debug only
parser.add_argument('--forceOverwrite', dest='overwrite',   help='force creation and submission of jobs if destination folder exists on EOS (FOR DEBUG ONLY)', default = False, action='store_true')
parser.add_argument('--dryrun',         dest='submitjobs',   help='make all preparation but do not submit jobs (FOR DEBUG ONLY)', default = True, action='store_false')
parser.add_argument('--qos',           dest='qos',   help='qos to use for the jobs', default = 'avery-b')

# every argument that is unknown is forwarded to the skimmer
# pay attention not to define argparse keys that are also used by the skimmer - apart from those handled in the code
args, unknown = parser.parse_known_args()

executable = 'bin/skim_ntuple.exe'
eos_server = 'root://cmseos.fnal.gov/'
username = getpass.getuser()

print_("... Welcome", username)

## -----------------------------------------------------
## check that environment was set up

cmssw_version  = os.environ.get('CMSSW_VERSION')
cmssw_base     = os.environ.get('CMSSW_BASE')
scram_arch     = os.environ.get('SCRAM_ARCH')
cpp_boost_path = os.environ.get('CPP_BOOST_PATH')

if None in [cmssw_version, cmssw_base, scram_arch, cpp_boost_path]:
    raise RuntimeError("Env variables not set (please do cmsenv and source setup before)")

## -----------------------------------------------------
## check that I am in the base folder for submission
here = os.getcwd()
# exp_here = '/'.join([cmssw_base, 'src/sixB/analysis/sixBanalysis'])
exp_here = '/'.join([cmssw_base, 'src/MultiHiggs/analysis/MultiHAnalysis'])
if here != exp_here:
    print_("[ERROR] please launch this code from the base sixBanalysis directory that is:")
    print_(exp_here)
    raise RuntimeError("wrong execution path")

## -----------------------------------------------------
## check that options generated here are not passed

generated_opts = ['output', 'seed']
if len([x for x in generated_opts if x in args]):
    print_("[ERROR] : the following options are created automatically by this code and should not be added")
    print_(generated_opts)
    raise RuntimeError("wrong options passed")

## -----------------------------------------------------
## check proxy and create it if needed

while not eostools.proxy_valid():
    '[INFO] your GRID proxy is expired, creating a new one'
    eostools.create_proxy()

## -----------------------------------------------------
## prepare the folder structure

odir_base = args.odir.format(username)
if odir_base[-1] == '/' : odir_base = odir_base[:-1]

osamplename = args.oname
if not osamplename:
    osamplename = os.path.basename(args.input)
    osamplename = os.path.splitext(osamplename)[0]
    # osamplename = args.input.rsplit(r'/', 1)[-1].rsplit('.', 1)[0]
# osamplename = 'SKIM_' + osamplename
odir_sample = '/'.join([odir_base, args.tag, osamplename])

# first of all, abort if trying to overwrite an existing folder
if exists(odir_sample) and not args.overwrite:
    print_("[ERROR] the target directory of the sample exists already: ", odir_sample)
    print_("[ERROR] aborting script")
    raise RuntimeError("Existing sample directory")
makedir(odir_sample)
makedir(odir_sample + '/filelist')
makedir(odir_sample + '/output')

# if not exists(odir_base):
#     print_("[INFO] creating base directory: ", odir_base)
#     makedirs(odir_base)

odir_tag = odir_base + '/' + args.tag
# if not exists(odir_tag):
#     print_("[INFO] creating tag directory: ", odir_tag)
#     makedirs(odir_tag)

odir_tar = odir_tag + '/' + 'analysis_tar'
if not exists(odir_tar):
    print_("[INFO] creating tarball directory: ", odir_tar)
    makedir(odir_tar)


## -----------------------------------------------------
## check if an analysis tar is needed for this tag and make it in case

tarname       = 'sixBanalysis.tar.gz'
if exists(odir_tar + '/' + tarname):
    print_("[INFO] will use the tarball found at ", odir_tar + '/' + tarname)
else:
    print_("[INFO] creating the tarball")
    base_work_dir = os.getcwd()
    tar_loc_path  = base_work_dir + '/tars/' + tarname
    to_include = [ # things to include in the tarball
                  'bin/',
                  'lib/',
                  'config/',
                  'data/',
                  'models/',
    ]
    command = 'tar -zcf {0} '.format(tar_loc_path)
    for ti in to_include:
        command += ti + ' '
    if os.system(command) != 0:
        print_("[ERROR] Could not tar the repository, aborting")
        raise RuntimeError("tar failed")

    copy(tar_loc_path, odir_tag, eos_server)

## -----------------------------------------------------
## prepare the jobs folder

jobsdir = '/'.join(['skim_jobs', args.tag, osamplename])
print_("[INFO] jobs will be submitted from folder:", jobsdir)
if os.system('mkdir -p %s' % jobsdir) != 0:
    print_("[ERROR] Could not create the jobs folder, aborting")
    raise RuntimeError("failed to setup jobs dir")

## -----------------------------------------------------
## prepare the filelists

files = inputtools.parseInputFileList(args.input)
njobs = args.njobs if args.njobs <= len (files) else len (files)
print_("[INFO] will create", njobs, 'jobs')
fileblocks = inputtools.splitInBlocks (files, njobs)

filelist_proto = 'filelist_{ijob}.txt'
for ijob in range(njobs):
    scripttools.write_flist(jobsdir + '/' + filelist_proto.format(ijob=ijob), fileblocks[ijob])

## -----------------------------------------------------
## send the filelists to eos

print_("[INFO] copying filelists")
copy(jobsdir+'/'+filelist_proto.format(ijob='*'), odir_sample + '/filelist', eos_server)

## -----------------------------------------------------
## prepare job scripts

ofile_proto    = 'ntuple_{ijob}.root'
## options created by the skim
skim_base_commands = [
    executable,
    '--input %s'    % filelist_proto.format(ijob='${IJOB}'),
    '--output %s'   % 'ntuple_${IJOB}.root',
    '--seed ${IJOB}',
]
skim_command = ' '.join(skim_base_commands)
## now forward all the other commands to skim_command
skim_command += ' ' + ' '.join(unknown)

sbatchname = 'skim.sbtach'

resources = {
    'account' : 'avery',
    'qos':args.qos,
    'cpus-per-task' : '1',
    'mem-per-cpu' : '2000',
    'time' : '08:00:00',
}
SBATCH = '\n'.join(['#SBATCH --{}={}'.format(k, v) for k, v in resources.iteritems()])

script='''#!/bin/bash

#SBATCH --job-name=multihiggs
#SBATCH --output={jobsdir}/%A_%a.out
{SBATCH}
#SBATCH --array={jobs}

if [ -z $SLURM_ARRAY_TASK_ID ]; then
    SLURM_ARRAY_TASK_ID=0
fi

SCRATCH=$TMPDIR/$SLURM_ARRAY_TASK_ID
mkdir -p $SCRATCH
cd $SCRATCH

IJOB=$SLURM_ARRAY_TASK_ID
echo "[-] JOB NUMBER : ${{IJOB}}"  #job number
echo "... starting job on `date`"  #Date/time of start of job
echo "... running on: `uname -a`"  #Condor job is running on this node
echo "... hostname: `hostname`"
echo "... system software: `cat /etc/redhat-release`" #Operating System on that node

source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH={scram_arch}
eval `scramv1 project CMSSW {cmssw_version}`

cd {cmssw_version}/src
eval `scramv1 runtime -sh`

echo "... retrieving bbbb executables tarball"
cp {tarball} .

echo "... uncompressing bbbb executables tarball"
tar -xzf {tarname}
rm {tarname}

echo "... retrieving filelist"
cp {filelist_proto} .

COPY_TO_LOCAL=1
if [ ${{COPY_TO_LOCAL}} -eq 1 ]; then
    echo "... copying input files to local"
    cat filelist_${{IJOB}}.txt | xargs -n 1 -i sh 'echo {{}}; xrdcp -f -s {{}} .'
    if [ $? -eq 0 ]; then
        echo "... successfully copied input files to local"
        ls *.root > filelist_${{IJOB}}.txt
    else
        echo "... failed to copy input files to local"
    fi
fi

export CPP_BOOST_PATH={cpp_boost_path}
export LD_LIBRARY_PATH=${{LD_LIBRARY_PATH}}:./lib:${{CPP_BOOST_PATH}}/lib

echo "... executing the command below:"
echo "{full_command}"

echo "... starting execution"
{full_command}
if [ $? -ne 0 ]; then
    echo "... execution finished with status $?"
    echo "... exiting script"
    exit $?
fi

echo "... copying output file {outfile_name} to storage"
cp {outfile_name} {odir_sample}/output
if [ $? -ne 0 ]; then
    echo "... copy done with status $?"
    echo "... exiting script"
    exit $?
fi

cd $SCRATCH
rm -rf {cmssw_version}

echo "... finished job on " `date`
echo "... exiting script"
'''.format(
    SBATCH=SBATCH,
    scram_arch=scram_arch,
    cmssw_version=cmssw_version,
    tarball=odir_tag + '/' + tarname,
    tarname=tarname,
    filelist_proto=odir_sample + '/filelist/' + filelist_proto.format(ijob='${IJOB}'),
    cpp_boost_path=cpp_boost_path,
    full_command=skim_command,
    outfile_name=ofile_proto.format(ijob='${IJOB}'),
    odir_sample=odir_sample,
    jobs='{0}-{1}'.format(0, njobs-1) if njobs > 1 else "0,",
    jobsdir=os.path.abspath(jobsdir),
)

with open(jobsdir + '/' + sbatchname, 'w') as f:
    f.write(script)

print_("-- Summary")
print_("** Production tag        :", args.tag)
print_("** Skim of filelist      :", args.input)
print_("** Njobs                 :", njobs)
print_("** Saving output to      :", odir_sample)

## -----------------------------------------------------
## save info about this run in a file

import json
metainfoname = os.path.join(jobsdir, 'sub_info.json')
metadata = {
    'input filelist' : args.input,
    'base folder': odir_base,
    'output folder': odir_sample,
    'ntuple proto': ofile_proto,
    'num jobs': njobs,
}
with open(metainfoname, 'w') as outfile:
    json.dump(metadata, outfile, indent=4)

## -----------------------------------------------------
## submit jobs

if args.submitjobs:
    print_("[INFO] submitting jobs")
    command = 'sbatch {jobsdir}/{sbatchname}'.format(jobsdir=jobsdir, sbatchname=sbatchname)
    if os.system(command) != 0:
        print_("[ERROR] Could not submit jobs, aborting")
        raise RuntimeError("failed to submit jobs")
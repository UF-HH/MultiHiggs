# test : python scripts/submitSkimOnBatch.py --input TTJets_dummy.txt --tag prova_4 --cfg config/skim_ntuple_2018_ttbar.cfg --maxEvts 50000 --force

import condortools.inputsplit as inputtools
import condortools.eostools as eostools
import condortools.scriptgen as scripttools

import os
import sys
import argparse
import getpass

parser = argparse.ArgumentParser(description='Command line parser of skim options')
parser.add_argument('--input'     ,  dest = 'input'     ,  help = 'input filelist'           ,  required = True        )
parser.add_argument('--tag'       ,  dest = 'tag'       ,  help = 'production tag'           ,  required = True        )
parser.add_argument('--njobs'     ,  dest = 'njobs'     ,  help = 'njobs'                    ,  type     = int         ,   default = 50    )
parser.add_argument('--memory'    ,  dest = 'memory'    ,  help = 'request memory'           ,  type     = int         ,   default = None  )
#### --------------------------------------------------- - expert usage
parser.add_argument('--outputName', dest='oname',  help='the name of the directory of this sample (if not given, auto from filelist)', default = None)
parser.add_argument('--outputDir',  dest='odir',   help='the base EOS output directory. Use a {0} for username placeholder, or give it explicitely', default = "/store/user/{0}/HHHTo6B/TriggerStudies/")
#### --------------------------------------------------- - debug only
parser.add_argument('--forceOverwrite', dest='overwrite',   help='force creation and submission of jobs if destination folder exists on EOS (FOR DEBUG ONLY)', default = False, action='store_true')
parser.add_argument('--dryrun',         dest='submitjobs',   help='make all preparation but do not submit jobs (FOR DEBUG ONLY)', default = True, action='store_false')

# every argument that is unknown is forwarded to the skimmer
# pay attention not to define argparse keys that are also used by the skimmer - apart from those handled in the code
args, unknown = parser.parse_known_args()

#### the output is saved in
#### odir / tag / oname
##### e.g.
#### root://cmseos.fnal.gov//store/user/lcadamur/bbbb_ntuples/' + TAG + '/' + ONAME
#### tree structure
# odir_base / tag / sample / filelist
#                          / output
# odir_base / tag / analysis_tar

#executable = 'bin/skim_ntuple.exe'
executable = 'bin/skim_trigger.exe'
eos_server = 'root://cmseos.fnal.gov/'
username = getpass.getuser()

print "... Welcome", username

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
exp_here = '/'.join([cmssw_base, 'src/sixB/analysis/MultiHAnalysis'])
if here != exp_here:
    print "[ERROR] please launch this code from the base sixBanalysis directory that is:"
    print exp_here
    raise RuntimeError("wrong execution path")

## -----------------------------------------------------
## check that options generated here are not passed

generated_opts = ['output', 'seed']
if len([x for x in generated_opts if x in args]):
    print "[ERROR] : the following options are created automatically by this code and should not be added"
    print generated_opts
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
if eostools.exists_on_eos(odir_sample) and not args.overwrite:
    print "[ERROR] the target directory of the sample exists already: ", odir_sample
    print "[ERROR] aborting script"
    raise RuntimeError("Existing sample directory")
eostools.makedir_on_eos(odir_sample)
eostools.makedir_on_eos(odir_sample + '/filelist')
eostools.makedir_on_eos(odir_sample + '/output')

# if not eostools.exists_on_eos(odir_base):
#     print "[INFO] creating base directory: ", odir_base
#     eostools.makedir_on_eos(odir_base)

odir_tag = odir_base + '/' + args.tag
# if not eostools.exists_on_eos(odir_tag):
#     print "[INFO] creating tag directory: ", odir_tag
#     eostools.makedir_on_eos(odir_tag)

odir_tar = odir_tag + '/' + 'analysis_tar'
if not eostools.exists_on_eos(odir_tar):
    print "[INFO] creating tarball directory: ", odir_tar
    eostools.makedir_on_eos(odir_tar)

## -----------------------------------------------------
## check if an analysis tar is needed for this tag and make it in case

tarname       = 'sixBanalysis.tar.gz'
if eostools.exists_on_eos(odir_tar + '/' + tarname):
    print "[INFO] will use the tarball found at ", odir_tar + '/' + tarname
else:
    print "[INFO] creating the tarball"
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
        print "[ERROR] Could not tar the repository, aborting"
        raise RuntimeError("tar failed")
    print "[INFO] transmitting the tarball to EOS at", odir_tar
    command = 'xrdcp -f -s {} {}{}'.format(tar_loc_path, eos_server, odir_tar)
    if os.system(command) != 0:
        print "[ERROR] Could not xrdcp the tar to remote, aborting"
        raise RuntimeError("xrdcp of tar failed")

## -----------------------------------------------------
## prepare the jobs folder

jobsdir = '/'.join(['skim_jobs', args.tag, osamplename])
print "[INFO] jobs will be submitted from folder:", jobsdir
if os.system('mkdir -p %s' % jobsdir) != 0:
    print "[ERROR] Could not create the jobs folder, aborting"
    raise RuntimeError("failed to setup jobs dir")

## -----------------------------------------------------
## prepare the filelists

files = inputtools.parseInputFileList(args.input)
njobs = args.njobs if args.njobs <= len (files) else len (files)
print "[INFO] will create", njobs, 'jobs'
fileblocks = inputtools.splitInBlocks (files, njobs)

filelist_proto = 'filelist_{ijob}.txt'
for ijob in range(njobs):
    scripttools.write_flist(jobsdir + '/' + filelist_proto.format(ijob=ijob), fileblocks[ijob])

## -----------------------------------------------------
## send the filelists to eos

print "[INFO] copying filelists to EOS"
command = 'xrdcp -f -s {} {}{}'.format(jobsdir+'/'+filelist_proto.format(ijob='*'), eos_server, odir_sample + '/filelist')
#command = 'cp -f {} {}'.format(jobsdir+'/'+filelist_proto.format(ijob='*'), odir_sample + '/filelist')
if os.system(command) != 0:
    print "[ERROR] Could not copy the filelists to EOS, aborting"
    raise RuntimeError("failed to copy filelists to eos")

## -----------------------------------------------------
## prepare job scripts

ofile_proto    = 'ntuple_{ijob}.root'
## options created by the skim
skim_base_commands = [
    executable,
    '--input %s'    % filelist_proto,
    '--output %s'   % 'ntuple_{ijob}.root',
#    '--seed {ijob}',
]
skim_command = ' '.join(skim_base_commands)
## now forward all the other commands to skim_command
skim_command += ' ' + ' '.join(unknown)

eosdest = '{}{}/output'. format(eos_server, odir_sample)

jdlname = 'skim_6b.jdl'
scripttools.make_jdl(jobsdir+'/'+jdlname, 'skim_6b.sh', njobs, args.memory)
scripttools.make_exec_script(
    filename           = jobsdir+'/skim_6b.sh',
    analysis_tarball   = eos_server + odir_tar + '/' + tarname,
    filelist_proto     = '{}{}/filelist/{}'.format(eos_server, odir_sample, filelist_proto),
    outfile_proto      = ofile_proto,
    full_command_proto = skim_command,
    eos_dest           = eosdest
)

print "-- Summary"
print "** Production tag        :", args.tag
print "** Skim of filelist      :", args.input
print "** Njobs                 :", njobs
print "** Saving output to      :", odir_sample

## -----------------------------------------------------
## save info about this run in a file
metainfoname = '/'.join(['skim_jobs', args.tag, osamplename, 'sub_info.txt'])
fmetainfo = open(metainfoname, 'w')
fmetainfo.write('input filelist : ' + str(args.input)  + '\n')
fmetainfo.write('base folder    : ' + str(odir_base)   + '\n')
fmetainfo.write('output folder  : ' + str(eosdest)     + '\n')
fmetainfo.write('nutple proto   : ' + str(ofile_proto) + '\n')
fmetainfo.write('num jobs       : ' + str(njobs)       + '\n')
fmetainfo.close()

## -----------------------------------------------------
## submit jobs

if args.submitjobs:
    print "[INFO] submitting jobs"
    os.chdir(jobsdir)
    command = 'condor_submit ' + jdlname
    exitcode = os.system(command)
    if exitcode != 0:
        print "[ERROR] Something went wrong when submitting jobs (code = {})".format(exitcode)
        raise RuntimeError("job submission failed")

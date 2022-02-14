# tools to generate scripts for the batch system

def writeln(f, line):
    f.write(line + '\n')

def make_jdl(filename, executable, njobs, memory=None):
    """ build a jdl condor file that submits njobs running executable. Job must expect job idx as first parameter """
    fout = open(filename, 'w')
    writeln (fout, 'universe = vanilla')
    writeln (fout, 'Executable = %s' % executable)
    writeln (fout, 'should_transfer_files = YES')
    writeln (fout, 'when_to_transfer_output = ON_EXIT')
    if memory: writeln (fout, 'request_memory = %i' % memory)
    writeln (fout, 'Output = job_$(Cluster)_$(Process).stdout')
    writeln (fout, 'Error = job_$(Cluster)_$(Process).stderr')
    writeln (fout, 'Log = job_$(Cluster)_$(Process).log')
    writeln (fout, 'Arguments = $(Process)')
    writeln (fout, 'Queue %s' % njobs)
    fout.close()

import os
def make_exec_script(filename, analysis_tarball, filelist_proto, outfile_proto, full_command_proto, eos_dest):

    """ job-wise indexes in commands must contain a ijob formattable field """

    tarname      = os.path.basename(analysis_tarball)
    flist_name   = filelist_proto.format(ijob='${IJOB}')
    outfile_name = outfile_proto.format(ijob='${IJOB}')
    full_command = full_command_proto.format(ijob='${IJOB}')

    cmssw_version  = os.environ.get('CMSSW_VERSION')
    scram_arch     = os.environ.get('SCRAM_ARCH')
    cpp_boost_path = os.environ.get('CPP_BOOST_PATH')

    if None in [cmssw_version, scram_arch, cpp_boost_path]:
        raise RuntimeError("Env variables not set (do cmsenv and source setup)")

    fout = open(filename, 'w')
    #------------------ headers
    writeln(fout, '#!/bin/bash')
    writeln(fout, '{') ## start of redirection..., keep stderr and stdout in a single file, it's easier
    # writeln(fout, 'set -x') ## alternatively, can have every typed command redirected to stderr with this
    writeln(fout, 'IJOB=$1')  #job number    
    writeln(fout, 'echo "[-] JOB NUMBER : ${IJOB}"')  #job number
    writeln(fout, 'echo "... starting job on `date`"')  #Date/time of start of job
    writeln(fout, 'echo "... running on: `uname -a`"')  #Condor job is running on this node
    writeln(fout, 'echo "... hostname: `hostname`"')
    writeln(fout, 'echo "... system software: `cat /etc/redhat-release`"') #Operating System on that node
    #------------------ cms environment    
    writeln(fout, 'source /cvmfs/cms.cern.ch/cmsset_default.sh')
    writeln(fout, 'export SCRAM_ARCH=%s' % scram_arch)
    writeln(fout, 'eval `scramv1 project CMSSW %s`' % cmssw_version)
    writeln(fout, 'cd %s/src' % cmssw_version)
    writeln(fout, 'eval `scramv1 runtime -sh`')
    #------------------ analysis tarball and filelists
    writeln(fout, 'echo "... retrieving bbbb executables tarball"')
    writeln(fout, 'xrdcp -f -s %s .' % analysis_tarball) ## force overwrite CMSSW tar
    writeln(fout, 'echo "... uncompressing bbbb executables tarball"')
    writeln(fout, 'tar -xzf %s' % tarname)
    writeln(fout, 'rm %s' % tarname)
    writeln(fout, 'echo "... retrieving filelist"')
    writeln(fout, 'xrdcp -f -s %s .' % flist_name) ## force overwrite file list
    #------------------ environment configurations
    writeln(fout, 'export CPP_BOOST_PATH=%s' % cpp_boost_path)
    writeln(fout, 'export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:./lib:${CPP_BOOST_PATH}/lib')
    #------------------ run the code
    writeln(fout, 'echo "... executing the command below:"')
    writeln(fout, 'echo "%s"' % full_command)
    writeln(fout, 'echo "... starting execution"')
    writeln(fout, '%s' % full_command)
    writeln(fout, 'echo "... execution finished with status $?"')
    #------------------ copy the output    
    writeln(fout, 'echo "... copying output file %s to EOS in %s"' % (outfile_name, eos_dest))
    writeln(fout, 'xrdcp -f -s %s %s' % (outfile_name, eos_dest)) ## force overwrite output in destination (useful for resubmission)
    writeln(fout, 'echo "... copy done with status $?"')
    #------------------ 
    writeln(fout, 'cd ${_CONDOR_SCRATCH_DIR}')
    writeln(fout, 'rm -rf %s' % cmssw_version)
    # writeln(fout, 'echo "... job finished with status $?"')
    writeln(fout, 'echo "... finished job on " `date`')
    writeln(fout, 'echo "... exiting script"')    
    writeln(fout, '} 2>&1') ## end of redirection
    fout.close()

def write_flist(filename, filelist):
    fout = open(filename, 'w')
    for f in filelist:
        writeln(fout, f)
    fout.close()
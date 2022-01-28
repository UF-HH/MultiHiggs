# tools to analyze the status of a task

import glob
import re
import os
import collections
from datetime import datetime

def find_job_idxs(folder, flist_proto='filelist_{ijob}.txt', log_proto='job_{cluster}_{ijob}.log', stdout_proto='job_{cluster}_{ijob}.stdout'):

    """ find the indexes of the jobs given a folder """

    # use absolute paths
    flist_proto  = folder + '/' + flist_proto
    log_proto    = folder + '/' + log_proto
    stdout_proto = folder + '/' + stdout_proto

    # first find job idxs by filelist
    all_flist  = glob.glob(flist_proto.format(ijob='*'))
    idxs_flist = [int(re.search(flist_proto.format(ijob='(\d+)'), x).group(1)) for x in all_flist]

    # find also by log - there should be >= 1 log per submitted job (> 1 if resubmitted)
    all_logs         = glob.glob(log_proto.format(ijob='*', cluster='*'))
    matches_logs     = [re.search(log_proto.format(ijob='(\d+)', cluster='(\d+)'), x) for x in all_logs]
    cluster_idx_logs = [(int(x.group(1)), int(x.group(2))) for x in matches_logs]

    # finally check which stdout_proto are found
    all_stdout         = glob.glob(stdout_proto.format(ijob='*', cluster='*'))
    matches_stdout     = [re.search(stdout_proto.format(ijob='(\d+)', cluster='(\d+)'), x) for x in all_stdout]
    cluster_idx_stdout = [(int(x.group(1)), int(x.group(2))) for x in matches_stdout]

    data = {
        'idxs_flist'         : idxs_flist, 
        'cluster_idx_logs'   : cluster_idx_logs,
        'cluster_idx_stdout' : cluster_idx_stdout,
    }

    return data

def parse_stdout(filename):
    
    """ parse the stdout log file and retrieve the exit codes from the text (if they exist) """

    data = {
        'skim_done' : False,
        'skim_code' : None,
        'copy_code' : None,
    }

    skim_done_txt = '[INFO] ... skim finished'
    skim_code_txt = '... execution finished with status'
    copy_code_txt = '... copy done with status'

    f = open(filename)
    for line in f:
        
        if skim_done_txt in line:
            data['skim_done'] = True
        
        elif skim_code_txt in line:
            code = int(re.search('%s (\d+)' % skim_code_txt, line).group(1))
            data['skim_code'] = code

        elif copy_code_txt in line:
            code = int(re.search('%s (\d+)' % copy_code_txt, line).group(1))
            data['copy_code'] = code

    f.close()
    return data

def parse_metadata(filename):

    """ parse the metadata file """
    data = {}
    f = open(filename)
    for l in f:
        v = l.split(':', 1)
        data[v[0].strip()] = v[1].strip()
    f.close()
    return data

def jobidx_has_duplicates(idxlist):
    """ check if the (cluster, idx) list has cluster duplicates for the same idx """

    clusters, idxs = zip(*idxlist)
    u_idxs = set(idxs)
    if len(u_idxs) != len(idxs):
        return True
    return False

def generate_resub_cmds(failed_cluster_idx_list,
    log_proto='job_{cluster}_{ijob}.log', stdout_proto='job_{cluster}_{ijob}.stdout', stderr_proto='job_{cluster}_{ijob}.stderr',
    jdl_name='skim_6b.jdl'):
    commands = []

    # all backups etc are indexed by this timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # first make a backup folder
    bkpfol    = 'resub_backup_%s' % timestamp
    commands.append('mkdir %s #make bkp folder' % bkpfol)

    # now copy all stdout, stderr, and logs in the backup
    for cluster, idx in failed_cluster_idx_list:
        logname    = log_proto.format(cluster=cluster, ijob=idx)
        stdoutname = stdout_proto.format(cluster=cluster, ijob=idx)
        stderrname = stderr_proto.format(cluster=cluster, ijob=idx)
        commands.append('mv %s %s' % (logname, bkpfol))
        commands.append('mv %s %s' % (stdoutname, bkpfol))
        commands.append('mv %s %s' % (stderrname, bkpfol))

    # NOTE: assume that output of job is copied with xrdcp -f, so that the new output will overwrite the previous one

    # make a new jdl file
    new_jdl = 'resub_%s_%s' % (timestamp, jdl_name)
    commands.append('cp %s %s #new jdl sub file' % (jdl_name, new_jdl))

    # replace in the new jdl the queue argument
    ijoblist = list(zip(*failed_cluster_idx_list)[1])
    ijoblist.sort()
    ijoblist = [str(x) for x in ijoblist]
    strjoblist = 'Queue Process in ' + ', '.join(ijoblist)
    commands.append("sed -i 's/^Queue.*$/%s/' %s #replace queue with job idx" % (strjoblist, new_jdl))

    # finally the submission commands
    commands.append('condor_submit %s' % new_jdl)

    return commands
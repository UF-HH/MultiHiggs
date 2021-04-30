### TO DO 
# - handle failures that do not result in .log being transmitted
# === ttbar_2018_21Apr2021/SingleMuon_Run2 has some good examples
# LPC job removed by SYSTEM_PERIODIC_REMOVE due to job exceeding requested memory.
# 012 (12522113.014.000) 04/21 15:10:28 Job was held.
# Job was aborted by the user  |||||| <-- when I did condor_rm
# CFR: good termination is :
## 005 (12522113.019.000) 04/21 15:22:34 Job terminated.
##  (1) Normal termination (return value 0)
# - add options to force idxjob to resubmit

import condortools.taskstatus as ts
import argparse
import glob
import os
import collections

parser = argparse.ArgumentParser(description='Command line parser of skim options')

pgroup = parser.add_mutually_exclusive_group(required=True)
pgroup.add_argument('--folder',     dest = 'folder',       help = 'folder with job logs (single check)')
pgroup.add_argument('--tag',        dest = 'tag',          help = 'name of the tag (check all folders in tag)')

extragroup = parser.add_mutually_exclusive_group()
extragroup.add_argument('--resub',      dest = 'resub',        help = 'resubmit failed jobs',   action='store_true', default=False)
extragroup.add_argument('--makeflist',  dest = 'makeflist',    help = 'make a filelist for good jobs',   action='store_true', default=False)

parser.add_argument('--long',       dest = 'long',         help = 'detailed report',        action='store_true', default=False)
parser.add_argument('--test-resub', dest = 'issue_resub',  help = 'do not actually resubmit, just print the commands executed (for debug)',   action='store_false', default=True)
parser.add_argument('--flistname',  dest = 'flistname',    help = 'name of the filelist (valid only if using --folder)',  default=None)
parser.add_argument('--flistdest',  dest = 'flistdest',    help = 'destination folder for the filelist',  default='./')

args = parser.parse_args()

###########################################
# handle collisions between options
if args.tag and args.makeflist and args.flistname:
    print '... please do not use --flistname together with --tag (cannot use same name for all different filelists)'
    raise RuntimeError("colliding options")

###########################################
# expected file prototypes

logname_proto    = 'job_{cluster}_{ijob}.log'
stdoutname_proto = 'job_{cluster}_{ijob}.stdout'
stderrname_proto = 'job_{cluster}_{ijob}.stderr'

###########################################
# determine folders

if args.folder: # single folder
    print '[INFO] running on folder:', args.folder
    p = args.folder
    p = p.strip()
    if p[-1] == '/':
        p = p[:-1]
    base_path, fldrname = p.rsplit('/', 1)
    folders = [fldrname]

elif args.tag: # list all taks in folder
    print '[INFO] running on tag:', args.tag
    # FIXME: can let the code determine automatically if skim_jobs must be added
    # for now assume we are launching this from sixBanalysis/
    t = args.tag.strip()
    if t[-1] == '/':
        t = t[:-1]
    base_path = 'skim_jobs/' + t
    folders = glob.glob(base_path + '/*/')
    folders = [os.path.basename(x[:-1]) for x in folders] # remove trailing '/' and get just basename
    print '...... tag contains', len(folders), 'folders'

###########################################
# analyse status for every folder

data = {}

for fol in folders:
    
    data[fol] = {}
    idxs = ts.find_job_idxs('/'.join([base_path, fol]))
    # print idxs
    
    # n jobs created determined from flist
    data[fol]['ncreated'] = len(idxs['idxs_flist'])

    # n jobs submitted is determined from log list
    if len(idxs['cluster_idx_logs']) > 0 and ts.jobidx_has_duplicates(idxs['cluster_idx_logs']):
        print '[ERROR] duplicates found for job .log (was it resubmitted)? . Handling of this case not yet implemented'
        raise RuntimeError("duplicate log found")
    data[fol]['nsubmitted'] = len(idxs['cluster_idx_logs'])

    # n jobs finished is determined from stdout list
    if len(idxs['cluster_idx_stdout']) and ts.jobidx_has_duplicates(idxs['cluster_idx_stdout']):
        print '[ERROR] duplicates found for job .stodut (was it resubmitted)? . Handling of this case not yet implemented'
        raise RuntimeError("duplicate stdout found")
    data[fol]['nfinished'] = len(idxs['cluster_idx_stdout'])

    # get idxs of jobs running by intersecting the two filelists
    cluster_idx_running = [x for x in idxs['cluster_idx_logs'] if x not in idxs['cluster_idx_stdout']]
    data[fol]['cluster_idx_running'] = cluster_idx_running

    # for all the jobs with a log, check the status codes
    data[fol]['finished_codes'] = collections.OrderedDict()
    for cluster, idx in idxs['cluster_idx_stdout']:
        logname = '/'.join([base_path, fol, stdoutname_proto]).format(cluster=cluster, ijob=idx)
        codes   = ts.parse_stdout(logname)
        data[fol]['finished_codes'][(cluster, idx)] = codes


###########################################
# print a summary

bad_folders = []
bad_folders_jobs = {}
good_folders_jobs = {}

for fol in folders:
    print '\n=================================='
    print '====', fol
    print '====', '/'.join([base_path, fol])
    if data[fol]['ncreated'] == 0:
        print '** no jobs found'
        continue

    ntot = data[fol]['ncreated']
    print "-- N. jobs prepared  : {}".format(ntot)
    print "-- N. jobs submitted : {} ({:.1f}%)".format(data[fol]['nsubmitted'], 100.*data[fol]['nsubmitted']/ntot)
    print "-- N. jobs running   : {} ({:.1f}%)".format(ntot-data[fol]['nfinished'], 100.*(ntot-data[fol]['nfinished'])/ntot)
    print "-- N. jobs finished  : {} ({:.1f}%)".format(data[fol]['nfinished'], 100.*data[fol]['nfinished']/ntot)

    nsuccess  = 0
    nbad_skim_done = 0
    nbad_skim_code = 0
    nbad_skim_copy = 0
    good_cluster_idx = []
    for (cluster, idx), codes in data[fol]['finished_codes'].items():
        if not codes['skim_done']        : nbad_skim_done += 1
        elif not codes['skim_code'] == 0 : nbad_skim_code += 1
        elif not codes['copy_code'] == 0 : nbad_skim_copy += 1
        else:
            nsuccess += 1
            good_cluster_idx.append((cluster, idx))

    print "   ** SUCCESS        : {} ({:.1f}%)".format(nsuccess, 100.*nsuccess/ntot)
    print "   ** Skim failed    : {} ({:.1f}%)".format((nbad_skim_done + nbad_skim_code), 100.*(nbad_skim_done + nbad_skim_code)/ntot)
    print "   ** Copy failed    : {} ({:.1f}%)".format(nbad_skim_copy, 100.*nbad_skim_copy/ntot)

    bad_cluster_idx = [x for x in data[fol]['finished_codes'].keys() if x not in good_cluster_idx]
    good_folders_jobs[fol] = good_cluster_idx
    bad_folders_jobs[fol]  = bad_cluster_idx
    if args.long:
        print '... the following', len(data[fol]['cluster_idx_running']), 'jobs are still running (no stdout found)'
        if len(data[fol]['cluster_idx_running']) > 0:
            print zip(*data[fol]['cluster_idx_running'])[1]
        print '... more info on the', len(bad_cluster_idx), 'failed jobs in the logs below'
        for cluster, idx in bad_cluster_idx:
            logname = '/'.join([base_path, fol, stdoutname_proto]).format(cluster=cluster, ijob=idx)
            print '   ... Skim : {} | code : {} | copy : {} | log : {}'.format(
                data[fol]['finished_codes'][(cluster, idx)]['skim_done'], data[fol]['finished_codes'][(cluster, idx)]['skim_code'], data[fol]['finished_codes'][(cluster, idx)]['copy_code'], logname) 

    if nsuccess != ntot:
        bad_folders.append(fol)

print '\n--- SUMMARY : there are', len(bad_folders), 'skims stll running or with some jobs failed'
for bf in bad_folders:
    print '*', bf


###########################################
# resubmit failed jobs

if args.resub:
    print '\n[INFO] going to resubmit the failed jobs for each of the', len(bad_folders), 'folders'
    workdir = os.getcwd()
    for fol in bad_folders:
        thisfol = '/'.join([base_path, fol])

        os.chdir(thisfol)            
        commands = ts.generate_resub_cmds(bad_folders_jobs[fol]) # the list of os commands to execute
        

        if args.issue_resub:
            print '... folder : ', fol, ' . Will resubmit', len(bad_folders_jobs[fol]), 'jobs'
            for c in commands:
                os.system(c)
        else: # just print
            print '... folder : ', fol,  ', not resubmitting. Resubmission would execute the following commands:'
            for c in commands: print c

    # back to initial work dir
    os.chdir(workdir)

###########################################
# making filelists

if args.makeflist:
    print '\n[INFO] generating filelists'
    listname = args.flistname
    if not listname:
        listname = '{fol}.txt'
    listdir = args.flistdest
    if listdir[-1] != '/':
        listdir += '/'
    olist_proto = listdir + listname

    for fol in folders:
        cluster_idx  = good_folders_jobs[fol]
        metadataname = '/'.join([base_path, fol, 'sub_info.txt'])
        metadata = ts.parse_metadata(metadataname)
        # print metadata
        if len(cluster_idx) == 0:
            print "[WARNING] : list of good files for", fol, "is empty, no filelist done"
            continue
        job_idx = sorted(list(zip(*cluster_idx)[1]))
        flist = []
        ofile_proto = metadata['output folder'] + '/' + metadata['nutple proto']
        for idx in job_idx:
            flist.append(ofile_proto.format(ijob=idx))

        olist = olist_proto.format(fol=fol)
        print '... folder ', fol, 'saved in', olist
        fout = open(olist, 'w')
        for f in flist:
            fout.write(f + '\n')
        fout.close()
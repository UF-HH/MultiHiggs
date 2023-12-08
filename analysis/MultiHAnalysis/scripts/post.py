"""
Script to post-process skimmed ntuples
recursively in a directory.
"""

from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument('skimDir', help='Directory containing skimmed ntuples', nargs='+')

# force merge option
parser.add_argument('--force', action='store_true', help='Force merge')

# resubmit failed jobs
parser.add_argument('--resubmit', action='store_true', help='Resubmit failed jobs')

def slurm_status(args, skimDir, njobs):
    import pandas as pd
    import subprocess, io, re

    jobids = {'running': [], 'failed': [], 'completed': []}

    pattern = re.compile(r'(\d+)_(\d+).out')
    logfiles = list(filter(pattern.match, os.listdir(skimDir)))

    slurminfo = {}
    slurmjobs = { pattern.match(f).group(1) for f in logfiles }
    for slurmid in sorted(slurmjobs):
        cmd = 'sacct -j %s --format=JobID,State,ExitCode --parsable ' % slurmid
        print('Querying SLURM:\n  %s' % cmd)
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out = p.communicate()[0].decode('utf-8')
        if p.returncode != 0:
            raise RuntimeError('Failed to query SLURM job status')
        
        df = pd.read_csv(io.StringIO(out), sep='|')
        # remove entries with .batch in the jobid
        df = df[~df['JobID'].str.contains('.batch')]
        # remove the last column
        df = df.iloc[:, :-1]
        # remove the slurmid prefix
        slurminfo[slurmid] = df

    for jobid in range(njobs):
        for slurmid, info in reversed(slurminfo.items()):
            id = slurmid + '_' + str(jobid)
            mask = info['JobID'] == id

            if not mask.any():
                continue

            state = info[mask]['State'].values[0]

            if state == 'COMPLETED':
                jobids['completed'].append(str(jobid))
                break

            if state == 'FAILED':
                jobids['failed'].append(str(jobid))
                break

            if state == 'RUNNING':
                jobids['running'].append(str(jobid))
                
    return jobids

def resubmit(args, skimDir, jobids):
    import subprocess

    cmd = f'sbatch --array={",".join(jobids)} {skimDir}/skim.sbatch'
    print('Resubmitting failed jobs:\n  %s' % cmd)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = p.communicate()[0].decode('utf-8')
    if p.returncode != 0:
        raise RuntimeError('Failed to resubmit jobs')

    print(out)

def merge(args, skimDir, output, njobs):
    import subprocess
    print(f'Merging output files to: {output}/ntuple.root')

    if os.path.exists(f'{skimDir}/.merged'):
        print(f'Found existing {skimDir}/.merged file.')
        if not args.force:
            print('Will not merge.')
            return
        else:
            print('Will merge anyway.')

    skimfiles = [ os.path.join(output, 'output', f) for f in os.listdir(f'{output}/output/') if f.endswith('.root') ]

    if len(skimfiles) != njobs:
        print(f'Only found {len(skimfiles)} files out of {njobs} jobs.')
        if not args.force:
            print('Will not merge.')
            return
        else:
            print('Will merge anyway.')
    
    cmd = f'hadd -f {output}/ntuple.root {" ".join(skimfiles)}'
    print('Running command:\n  %s' % cmd)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = p.communicate()[0].decode('utf-8')
    print(out)
    if p.returncode != 0:
        raise RuntimeError('Failed to merge files')

    with open(f'{skimDir}/.merged', 'w') as f:
        f.write('')

def main(args, skimDir):
    import json

    with open('{}/sub_info.json'.format(skimDir)) as f:
        sub_info = json.load(f)

    output = sub_info['output folder']
    njobs = sub_info['num jobs']

    # TODO: add condor support
    jobids = slurm_status(args, skimDir, njobs)

    assert sum(len(jobids[k]) for k in jobids) == njobs

    all_completed = len(jobids['completed']) == njobs
    any_running = len(jobids['running']) > 0
    any_failed = len(jobids['failed']) > 0

    info = {k: len(jobids[k]) for k in jobids if len(jobids[k])}
    print('Job %s status: ' % skimDir + str(info))

    if all_completed or args.force:
        return merge(args, skimDir, output, njobs)

    if args.resubmit and any_failed:
        print('Resubmitting failed jobs')
        return resubmit(args, skimDir, jobids['failed'])
    
    if any_running:
        print('Some jobs are still running. Will not merge.')
        return

if __name__ == "__main__":
    args = parser.parse_args()

    import os

    for skimDir in args.skimDir:
      for root, dirs, files in os.walk(skimDir):
          if any(dirs): continue
          print('Processing directory: {}'.format(root))
          main(args, root)
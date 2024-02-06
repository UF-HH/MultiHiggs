import os

from metis.Sample import DBSSample
from metis.LocalMergeTask import LocalMergeTask
from metis.CondorTask import CondorTask
from metis.StatsParser import StatsParser
import argparse
import samples

from time import sleep
import sys

condorpath = os.path.dirname(os.path.realpath(__file__))
user = os.environ['USER']

output = "${OUTPUT}"
tag = "${TAG}"
config = "${CONFIG}"

tarfile = 'project.tar.xz'

# Avoid spamming too many short jobs to condor
# Less dileptn pairs = faster = more input files per job
def split_func(dsname):
    return 1
    # if "QCD" in dsname:
    #     return 7 # running 7 files at a time
    # else:
    #     return 1

if __name__ == "__main__":
    # Samples
    samples = samples.samples

    merged_dir = "/ceph/cms/store/user/{user}/{output}/{tag}/merged/".format(user=user, output=output, tag=tag)

    # Task summary for printing out msummary
    task_summary = {}

    # To skip tail events
    skip_tail = False

    # Infinite loop until all tasks are complete
    # It will sleep every 10 minutes (600 seconds) and re-check automatically
    while True:

        # Boolean to aggregate whether all tasks are complete
        all_tasks_complete = True

        # Loop over the dataset provided by the user few lines above, and do the Metis magic
        for shortname, ds in samples.items():
            task = CondorTask(
                    sample = ds,
                    files_per_output = split_func(ds.get_datasetname()),
                    output_name = "output.root",
                    tag = tag,
                    condor_submit_params = {
                        "sites": "T2_US_UCSD,UAF",
                        "use_xrootd":True,
                        "classads": [
                            ["metis_extraargs", "--cfg {config}".format(config=config)]
                            ]
                        },
                    cmssw_version = "CMSSW_10_6_28",
                    scram_arch = "slc7_amd64_gcc700",
                    input_executable = "{}/condor_executable_metis.sh".format(condorpath), # your condor executable here
                    tarfile = tarfile, # your tarfile with assorted goodies here
                    special_dir = "{output}/{tag}".format(output=output, tag=tag),
                    min_completion_fraction = 0.50 if skip_tail else 1.0,
                    # max_jobs = 1,
            )
                        # When babymaking task finishes, fire off a task that takes outputs and merges them locally (hadd)
            # into a file that ends up on nfs (specified by `merged_dir` above)
            merge_task = LocalMergeTask(
                    input_filenames=task.get_outputs(),
                    output_filename="{}/{}.root".format(merged_dir,shortname),
                    ignore_bad = skip_tail,
                    )
            # Straightforward logic
            if not task.complete():
                task.process()
            else:
                if not merge_task.complete():
                    merge_task.process()

            # Aggregate whether all tasks are complete
            all_tasks_complete = all_tasks_complete and task.complete()

            # Set task summary
            task_summary[task.get_sample().get_datasetname()] = task.get_task_summary()

        # Parse the summary and make a summary.txt that will be used to pretty status of the jobs
        os.system("rm -f web_summary.json")
        webdir="~/public_html/{output}_{tag}".format(output=output, tag=tag)
        StatsParser(data=task_summary, webdir=webdir).do()
        os.system("chmod -R 755 {}".format(webdir))
        os.system("msummary -r -i {}/web_summary.json".format(webdir))

        # If all done exit the loop
        if all_tasks_complete:
            print("")
            print("All job finished")
            print("")
            break

        # Neat trick to not exit the script for force updating
        print('Press Ctrl-C to force update, otherwise will sleep for 600 seconds')
        try:
            for i in reversed(range(0, 600)):
                sleep(1) # could use a backward counter to be preeety :)
                sys.stdout.write("\r{} mins {} seconds till updating ...".format(i/60, i%60))
                sys.stdout.flush()
        except KeyboardInterrupt:
            raw_input("Press Enter to force update, or Ctrl-C to quit.")
            print("Force updating...")


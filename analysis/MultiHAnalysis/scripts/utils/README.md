This folder contains all tools that can be useful to analyse the code performance / debug issues / other utilities non-essential to run the analysis.

The goal of each script is listed below with a minimal usage example. ``[opt=value]`` denotes an optional argument and its default.

* ``check_mem.sh`` : use ``top`` to follow the stat of one process and save it every 15 seconds (tunable in the script). Usage ``source check_mem.sh [logname=mem_log.txt] [procname=skim_ntuple]``
* ``plot_mem_usage.py`` : make a plot of RES, SHR, VIRT vs time using the log saved above
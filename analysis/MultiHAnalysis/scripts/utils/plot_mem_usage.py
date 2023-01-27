from datetime import datetime
import matplotlib
matplotlib.use('agg')

import matplotlib.pyplot as plt
import sys

col_def = ['PID', 'USER', 'PR',  'NI',    'VIRT',    'RES',    'SHR', 'S',  '%CPU', '%MEM',     'TIME+',  'COMMAND']

def memstr_to_float(s):
    mult = 1.
    if 'g' in s:
        mult = 1000.
        s = s.replace('g', '')
    f = float(s)
    return mult*f

def parse_data(filename):
    f = open(filename)
    timestamp = None
    data = []
     # 423 root      20   0  182528 103120 102932 S   0.7  0.8   1:04.15 systemd-journal
    timestamp_format = '%a %b %d %H:%M:%S CDT %Y' #Wed Apr 21 18:41:12 CDT 2021
    for line in f:
        l = line.strip()
        if not l:
            continue
        if 'all finished' in line:
            break
        #if a timestamp was found, this must be a content line
        if timestamp:
            tokens = l.split()
            if not 'lcadamur' in tokens:
                continue
            # print tokens
            # for i in [0, 2, 3, 4, 5, 6]:
            #     tokens[i] = int(tokens[i])
            # for i in [8, 9]:
            #     tokens[i] = float(tokens[i])
            for i in [col_def.index('PID'), col_def.index('PR'), col_def.index('NI')]:
                tokens[i] = int(tokens[i])
            for i in [col_def.index('%CPU'), col_def.index('%MEM')]:
                tokens[i] = float(tokens[i])
            for i in [col_def.index('VIRT'), col_def.index('RES'), col_def.index('SHR')]:
                tokens[i] = memstr_to_float(tokens[i])
            data.append((timestamp, tokens))
            timestamp = None # and reset
        #otherwise check if it is a timestamp
        try:
            d = datetime.strptime(l, timestamp_format)
            timestamp = d
        except ValueError:
            pass
    return data


import argparse
parser = argparse.ArgumentParser(description='cmd line options')
parser.add_argument('--filename', dest='filename', help='input txt file from top command', default='mem_log.txt')
parser.add_argument('--output',   dest='output',   help='pdf plot output', default='mem_usage.pdf')
parser.add_argument('--xmin',     dest='xmin',     help='xmin of plot',    default=None, type=float)
parser.add_argument('--xmax',     dest='xmax',     help='xmax of plot',    default=None, type=float)
parser.add_argument('--title',    dest='title',    help='plot title',      default=None)
args = parser.parse_args()

# filename = 'logfile.txt'
# if len(sys.argv) > 1:
#     filename = sys.argv[1]
print '.. analysing file:', args.filename
treefill = parse_data(args.filename)

# time in minutes
timeseries = [(x[0] - treefill[0][0]).total_seconds()/60. for x in treefill]

# column to print
# VIRT  --  Virtual Image (kb)
# SWAP  --  Swapped size (kb)
# RES  --  Resident size (kb)
icol_RES = col_def.index('RES')
RES = [x[1][icol_RES] for x in treefill]

icol_SHR = col_def.index('SHR')
SHR = [x[1][icol_SHR] for x in treefill]

icol_VIRT = col_def.index('VIRT')
VIRT = [x[1][icol_VIRT] for x in treefill]

## transform memory in MB
RES  = [x/1000. for x in RES]
SHR = [x/1000. for x in SHR]
VIRT = [x/1000. for x in VIRT]

## make plot

plt.plot(timeseries, RES,  label='RES')
plt.plot(timeseries, SHR,  label='SHR')
plt.plot(timeseries, VIRT, label='VIRT')
plt.legend(loc='best')

xmin, xmax = plt.gca().get_xlim()
xmin = args.xmin if args.xmin else xmin
xmax = args.xmax if args.xmax else xmax
plt.xlim((xmin, xmax))
plt.xlabel('Time since start [min]')
plt.ylabel('Memory usage [MB]')
if args.title: plt.title(args.title)
print '.. saving plot as:', args.output
plt.savefig(args.output)

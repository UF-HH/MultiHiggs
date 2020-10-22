# ** without** doing cmsenv (i.e. in a fresh shell) do :
# source /cvmfs/sft.cern.ch/lcg/views/LCG_97/x86_64-centos7-gcc8-opt/setup.sh

import matplotlib
matplotlib.use('agg') # backend for remote server

import uproot
import matplotlib.pyplot as plt
import numpy as np
import sys
import pandas as pd

masses = [
    (450, 300),
    (500, 300),
    (600, 300),
    (600, 400),
    (700, 300),
    (700, 400),
    (700, 500),
]

var_to_plot = 'gen_Hb_recojet_ptmax'
## set the cut below

datas = []
names = []
for m in masses:
    df = pd.read_pickle('dataframes/df_mx_{}_my_{}.pkl'.format(*m))
    data = df[df['gen_bs_N_reco_match_in_acc'] == 6][var_to_plot]
    # q2p5  = np.percentile(data, 2.5)
    # q16   = np.percentile(data, 16)
    # q50   = np.percentile(data, 50)
    # q84   = np.percentile(data, 84)
    # q97p5 = np.percentile(data, 97.5)
    # plt.boxplot(data, vert=False)
    ## the box contains 50% of data (2-3rd quartile)
    ## whis=[5, 95] has the lines (whiskers) extend to the 5 and 95 percentiles
    datas.append(data)
    names.append('$m_{X} = %i, m_{Y} = %i$' % (m[0], m[1]))
bplot = plt.boxplot(datas, showfliers=False, whis=[5, 95], vert=False, patch_artist=True)

for patch in bplot['boxes']:
        patch.set_facecolor('lightblue')
        patch.set_edgecolor('black')
for patch in bplot['whiskers']:
    patch.set_color('black')
for patch in bplot['medians']:
        patch.set_color('red')

plt.yticks([i+1 for i in range(len(masses))], names)
plt.xlabel('Max jet $p_{T}$ [GeV]', horizontalalignment='right', x=1.0)
plt.xlim (0, 300)
plt.grid(linestyle=':')
plt.tight_layout()
plt.savefig('test_whisker_plot.pdf')

import pickle
import matplotlib
matplotlib.use('pdf')
import matplotlib.pyplot as plt
import numpy as np
import sys

masses = [
    (600, 400),
    (700, 500),
    (700, 400),
    (600, 300),
    (500, 300),
    (450, 300),
    (700, 300),
]

data = {}
for m in masses:
    f = open('data/out_data_MX_{}_MY_{}.pkl'.format(*m), 'rb')
    data[m] = pickle.load(f)['njets_effs']

# print data

eff_to_plot = 'gen'  # gen, reco, reco_acc
if len(sys.argv) > 1:
    eff_to_plot = sys.argv[1]

if eff_to_plot == 'gen':
    title = 'Gen jet efficiency'
    oname = 'gen_frequencies.pdf'

if eff_to_plot == 'reco': # gen, reco, reco_acc
    title = 'Reco jet efficiency'
    oname = 'reco_frequencies.pdf'

if eff_to_plot == 'reco_acc': # gen, reco, reco_acc
    title = r'Reco jet efficiency ($p_{T}$ > 20 GeV, $|\eta|$ < 4.8)'
    oname = 'reco_acc_frequencies.pdf'


xvals = np.asarray([0, 1, 2, 3, 4, 5, 6])
for im, m in enumerate(masses):
    values = np.asarray(data[m][eff_to_plot])
    # print values.shape
    plt.bar(xvals+0.1*im, values, width=0.1, align = 'edge', label = '$m_{X} = %i, m_{Y} = %i$' % (m[0], m[1]))

plt.title(title)
plt.xlabel('Number of matched jets')
plt.ylabel('Frequency [%]')
plt.legend(loc='upper left')
plt.savefig(oname)
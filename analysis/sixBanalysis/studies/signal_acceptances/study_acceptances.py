# ** without** doing cmsenv (i.e. in a fresh shell) do :
# source /cvmfs/sft.cern.ch/lcg/views/LCG_97/x86_64-centos7-gcc8-opt/setup.sh

import matplotlib
matplotlib.use('pdf') # backend for remote server

import uproot
import matplotlib.pyplot as plt
import numpy as np
import sys

fin_name   = '../../prova.root'
fout_name  = 'data/out_data_prova.pkl'
masses     = (999, 888)

if len(sys.argv) > 2:
    mX = int(sys.argv[1])
    mY = int(sys.argv[2])
    fin_name  = '../../NMSSM_XYH_YToHH_6b_MX_{mX}_MY_{mY}_accstudies.root'.format(mX=mX, mY=mY)
    fout_name  = 'data/out_data_MX_{mX}_MY_{mY}.pkl'.format(mX=mX, mY=mY)
    masses     = (mX, mY)

print '... opening file: ', fin_name
print '... output file : ', fout_name
file = uproot.open(fin_name)
tree = file['sixBtree']
df   = tree.pandas.df(
    ["gen_H*_b*",
    'gen_bs_N_reco_match', 'gen_bs_N_reco_match_in_acc',
    'gen_bs_match_recojet_minv', 'gen_bs_match_in_acc_recojet_minv']
)

print '... done, there are', df.shape[0], 'entries'

genbs_names = [
    "gen_HX_b1_{}",
    "gen_HX_b2_{}",
    "gen_HY1_b1_{}",
    "gen_HY1_b2_{}",
    "gen_HY2_b1_{}",
    "gen_HY2_b2_{}"
]

genjet_names = [
    "gen_HX_b1_genjet_{}",
    "gen_HX_b2_genjet_{}",
    "gen_HY1_b1_genjet_{}",
    "gen_HY1_b2_genjet_{}",
    "gen_HY2_b1_genjet_{}",
    "gen_HY2_b2_genjet_{}"
]

recojet_names = [
    "gen_HX_b1_recojet_{}",
    "gen_HX_b2_recojet_{}",
    "gen_HY1_b1_recojet_{}",
    "gen_HY1_b2_recojet_{}",
    "gen_HY2_b1_recojet_{}",
    "gen_HY2_b2_recojet_{}"
]

print '... replacing -999 values with NaN'
df = df.replace(-999, np.nan)

## add counters for columns with valid N objects
df['n_good_genbs']   = df[[b.format('pt') for b in genbs_names]]  .count(axis=1)
df['n_good_genjet']  = df[[b.format('pt') for b in genjet_names]] .count(axis=1)
df['n_good_recojet'] = df[[b.format('pt') for b in recojet_names]].count(axis=1)

## add abs(eta) info on branches
print '... adding gen eta info'
for b in genbs_names + genjet_names + recojet_names:
    df[b.format('abseta')] = df[b.format('eta')].abs()

####### add min-max infos to df
print '... adding min-max jet info'

df['gen_Hb_ptmin']         = df[[b.format('pt') for b in genbs_names]].min(axis=1)
df['gen_Hb_ptmax']         = df[[b.format('pt') for b in genbs_names]].max(axis=1)

df['gen_Hb_genjet_ptmin']  = df[[b.format('pt') for b in genjet_names]].min(axis=1)
df['gen_Hb_genjet_ptmax']  = df[[b.format('pt') for b in genjet_names]].max(axis=1)

df['gen_Hb_recojet_ptmin'] = df[[b.format('pt') for b in recojet_names]].min(axis=1)
df['gen_Hb_recojet_ptmax'] = df[[b.format('pt') for b in recojet_names]].max(axis=1)


df['gen_Hb_absetamin']         = df[[b.format('abseta') for b in genbs_names]].min(axis=1)
df['gen_Hb_absetamax']         = df[[b.format('abseta') for b in genbs_names]].max(axis=1)

df['gen_Hb_genjet_absetamin']  = df[[b.format('abseta') for b in genjet_names]].min(axis=1)
df['gen_Hb_genjet_absetamax']  = df[[b.format('abseta') for b in genjet_names]].max(axis=1)

df['gen_Hb_recojet_absetamin'] = df[[b.format('abseta') for b in recojet_names]].min(axis=1)
df['gen_Hb_recojet_absetamax'] = df[[b.format('abseta') for b in recojet_names]].max(axis=1)

#############################
## plot the fractions of well reconstructed objects
ntot = df.shape[0]

out_values = {
    'gen'      : [],
    'reco'     : [],
    # 'reco_2'   : [],
    'reco_acc' : [],
}

print '\n--- GEN JET ---'
for i in range(0,7):
    n = df[df['n_good_genjet'] == i].shape[0]
    v = 100.*n/ntot
    print 'N = {} : {:.1f}%'.format(i, v)
    out_values['gen'].append(v)

print '\n--- RECO JET ---'
for i in range(0,7):
    n = df[df['n_good_recojet'] == i].shape[0]
    v = 100.*n/ntot
    print 'N = {} : {:.1f}%'.format(i, v)
    out_values['reco'].append(v)

# print '\n--- RECO JET (xcheck) ---'
# for i in range(0,7):
#     n = df[df['gen_bs_N_reco_match'] == i].shape[0]
#     v = 100.*n/ntot
#     print 'N = {} : {:.1f}%'.format(i, v)
#     out_values['reco_2'].append(v)

print '\n--- RECO JET in acceptance ---'
for i in range(0,7):
    n = df[df['gen_bs_N_reco_match_in_acc'] == i].shape[0]
    v = 100.*n/ntot
    print 'N = {} : {:.1f}%'.format(i, v)
    out_values['reco_acc'].append(v)

import pickle
out_data = {}
out_data['njets_effs'] = out_values
out_data['masses']     = masses
fout = open(fout_name, 'wb')
pickle.dump(out_data, fout)


#### make a plot of the most fwd b quark in various b multiplicities

fig = plt.figure(1, figsize=(5.5,5.5))

plt.title('$m_{X} = %i GeV, m_{Y} = %i GeV$' % (masses[0], masses[1]))
plt.hist(df[df['gen_bs_N_reco_match_in_acc'] == 4]['gen_Hb_absetamax'], label = '4 reco jets', fc=None, ec='b', density=True, fill=False, histtype='step', bins=np.arange(0, 5, step=0.1))
plt.hist(df[df['gen_bs_N_reco_match_in_acc'] == 5]['gen_Hb_absetamax'], label = '5 reco jets', fc=None, ec='r', density=True, fill=False, histtype='step', bins=np.arange(0, 5, step=0.1))
plt.hist(df[df['gen_bs_N_reco_match_in_acc'] == 6]['gen_Hb_absetamax'], label = '6 reco jets', fc=None, ec='g', density=True, fill=False, histtype='step', bins=np.arange(0, 5, step=0.1))
plt.plot([2.5, 2.5], [0, 0.5], [4.8, 4.8], [0, 0.5], color='gray', linestyle=':')
plt.xlabel('Gen b quark $|\eta|$ max (all 6 b considered)')
plt.ylabel('a.u.')
plt.legend(loc='best')
plt.savefig('plots/maxabseta_mx_{}_my_{}.pdf'.format(*masses))

### make a plot of the lowest pt b quark in various b multiplicities
plt.clf()
plt.title('$m_{X} = %i GeV, m_{Y} = %i GeV$' % (masses[0], masses[1]))
plt.hist(df[df['gen_bs_N_reco_match_in_acc'] == 4]['gen_Hb_ptmin'], label = '4 reco jets', fc=None, ec='b', density=True, fill=False, histtype='step', bins=np.arange(0, 100, step=2))
plt.hist(df[df['gen_bs_N_reco_match_in_acc'] == 5]['gen_Hb_ptmin'], label = '5 reco jets', fc=None, ec='r', density=True, fill=False, histtype='step', bins=np.arange(0, 100, step=2))
plt.hist(df[df['gen_bs_N_reco_match_in_acc'] == 6]['gen_Hb_ptmin'], label = '6 reco jets', fc=None, ec='g', density=True, fill=False, histtype='step', bins=np.arange(0, 100, step=2))
plt.plot([20, 20], [0, 0.05], color='gray', linestyle=':')
plt.xlabel('Gen b quark $p_{T} min [GeV] (all 6 b considered)$')
plt.ylabel('a.u.')
plt.legend(loc='best')
plt.savefig('plots/minpt_mx_{}_my_{}.pdf'.format(*masses))

### make a plot of the invariant mass
plt.clf()
plt.title('$m_{X} = %i GeV, m_{Y} = %i GeV$' % (masses[0], masses[1]))
plt.hist(df[df['gen_bs_N_reco_match_in_acc'] == 4]['gen_bs_match_in_acc_recojet_minv'], label = '4 reco jets', fc=None, ec='b', density=True, fill=False, histtype='step', bins=np.arange(0, 1.3*masses[0], step=10))
plt.hist(df[df['gen_bs_N_reco_match_in_acc'] == 5]['gen_bs_match_in_acc_recojet_minv'], label = '5 reco jets', fc=None, ec='r', density=True, fill=False, histtype='step', bins=np.arange(0, 1.3*masses[0], step=10))
plt.hist(df[df['gen_bs_N_reco_match_in_acc'] == 6]['gen_bs_match_in_acc_recojet_minv'], label = '6 reco jets', fc=None, ec='g', density=True, fill=False, histtype='step', bins=np.arange(0, 1.3*masses[0], step=10))
plt.xlabel('Invariant mass of reconstructed objects [GeV]')
plt.ylabel('a.u.')
plt.legend(loc='upper left')
plt.savefig('plots/invmass_mx_{}_my_{}.pdf'.format(*masses))


### make a plot of the max pt
plt.clf()
plt.title('$m_{X} = %i GeV, m_{Y} = %i GeV$' % (masses[0], masses[1]))
plt.hist(df[df['gen_bs_N_reco_match_in_acc'] == 4]['gen_Hb_recojet_ptmax'], label = '4 reco jets', fc=None, ec='b', density=True, fill=False, histtype='step', bins=np.arange(0, 500, step=10))
plt.hist(df[df['gen_bs_N_reco_match_in_acc'] == 5]['gen_Hb_recojet_ptmax'], label = '5 reco jets', fc=None, ec='r', density=True, fill=False, histtype='step', bins=np.arange(0, 500, step=10))
plt.hist(df[df['gen_bs_N_reco_match_in_acc'] == 6]['gen_Hb_recojet_ptmax'], label = '6 reco jets', fc=None, ec='g', density=True, fill=False, histtype='step', bins=np.arange(0, 500, step=10))
plt.xlabel('Leading jet $p_{T}$ [GeV]')
plt.ylabel('a.u.')
plt.legend(loc='upper right')
plt.savefig('plots/maxptreco_mx_{}_my_{}.pdf'.format(*masses))


##################
# save the dataframe in output, to be reused in other scripts
df.to_pickle('dataframes/df_mx_{}_my_{}.pkl'.format(*masses))
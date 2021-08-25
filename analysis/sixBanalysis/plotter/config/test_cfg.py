import modules.Sample as sam
import collections
import copy

###################### COMMON INFO, DEFINITIONS, ETC #######################
## things reused throughout the config (to avoid redundance)

lumi_info = {'lumi' : 59.740, 'lumi_units' : 'fbinv'}

###################### SAMPLES #######################
## all samples to be processed should be in a "samples" list

ttbar = sam.Sample(name='ttbar', sampletype='mc', filelist='../skim_filelists/ttbar_2018_1Mag2021_2b/TTJets.txt',
    sampledesc= {**lumi_info, 'xs' : 815.96, 'xs_units' : 'pb'}
)
data_obs = sam.Sample(name='data_obs', sampletype='data', filelist='../skim_filelists/ttbar_2018_1Mag2021_2b/SingleMuon_Run2.txt')

samples = [ttbar, data_obs]

###################### ROOT FUNCTIONS #######################
## all variables to declare to the gInterpreter should be listed in a "declarations" variable

minv = """
double minv(double pt1, double eta1, double phi1, double m1, double pt2, double eta2, double phi2, double m2) {
    ROOT::Math::PtEtaPhiMVector v1 (pt1, eta1, phi1, m1);
    ROOT::Math::PtEtaPhiMVector v2 (pt2, eta2, phi2, m2);
    double m = (v1+v2).M();
    return m;
}
"""

declarations = [minv]

###################### NEW COLUMNS #######################
## all columns to declare in the samples should be listed in a "new_columns" dictionary (name -> expression)

new_columns = collections.OrderedDict()
new_columns['mll'] = 'minv(mu_1_pt, mu_1_eta, mu_1_phi, mu_1_m, ele_1_pt, ele_1_eta, ele_1_phi, ele_1_m)'

###################### SELECTIONS #######################

selections_defs = {
    # 'baseline' : 'n_mu_loose == 1 && n_ele_loose == 1 && bjet1_pt > 20 && bjet2_pt > 20',
    'tight'    : 'n_mu_loose == 1 && n_ele_loose == 1 && bjet1_pt > 30 && bjet2_pt > 30 && mu_1_pt > 30 && ele_1_pt > 20',
    'tight2b'  : 'n_mu_loose == 1 && n_ele_loose == 1 && bjet1_pt > 30 && bjet2_pt > 30 && mu_1_pt > 30 && ele_1_pt > 20 && bjet1_DeepJet > 0.2783 && bjet2_DeepJet > 0.2783',
}

###################### WEIGHTS DEFINITION #######################
# weights that appear in norm_weights undergo a rescaling by sum(w) when filling the plots
# these weights must be defined both in the norm_tree and in the event_tree

norm_weights = ['genWeight', 'PUWeight']

###################### HISTOGRAMS DESCRIPTIONS #######################
# all histograms should be listed in a "histos" list
# a histogram is represented by a dictionary containing its description

histos_descs = [
    {
        'var'        : 'bjet1_pt',
        'weightlist' : ['genWeight'],
        'bins'       : (100, 0, 400),
        'nametag'    : 'gw'
    },
    {
        'var'        : 'bjet1_pt',
        'weightlist' : ['genWeight', 'PUWeight'],
        'bins'       : (100, 0, 400),
        'nametag'    : 'gw_pu'
    },
    {
        'var'        : 'bjet1_pt',
        'weightlist' : ['genWeight', 'PUWeight', 'btagSF_WP_M'],
        'bins'       : (100, 0, 400),
        'nametag'    : 'gw_pu_btagsf'
    },
    {
        'var'        : 'rhofastjet_all',
        'weightlist' : ['genWeight'],
        'bins'       : (100, 0, 100),
        'nametag'    : 'gw'
    },
    {
        'var'        : 'rhofastjet_all',
        'weightlist' : ['genWeight', 'PUWeight'],
        'bins'       : (100, 0, 100),
        'nametag'    : 'gw_pu'
    },
    {
        'var'        : 'rhofastjet_all',
        'weightlist' : ['genWeight', 'PUWeight', 'btagSF_WP_M'],
        'bins'       : (100, 0, 100),
        'nametag'    : 'gw_pu_btagsf'
    },    
]

### declare the histograms - make one histogram for every selection declared
### any type of manipulation can be done here
histos = []
for hd in histos_descs:
    for s in selections_defs.keys():
        d2 = copy.deepcopy(hd)
        d2['sel'] = s
        histos.append(d2)

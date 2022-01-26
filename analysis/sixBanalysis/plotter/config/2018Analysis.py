import modules.Sample as sam
import collections
import copy

###################### COMMON INFO, DEFINITIONS, ETC #######################
## things reused throughout the config (to avoid redundance)

lumi_info = {'lumi' : 59.740, 'lumi_units' : 'fbinv'}

###################### SAMPLES #######################
## all samples to be processed should be in a "samples" list

nmssm = sam.Sample(name='nmssm', sampletype='mc', files=['root://cmseos.fnal.gov//store/user/srosenzw/analysis/NMSSM/NMSSM_XYH_YToHH_6b_MX_700_MY_400/ntuple.root'],
    sampledesc= {**lumi_info, 'xs' : 0.3, 'xs_units' : 'pb'}
)
# data_obs = sam.Sample(name='data_obs', sampletype='data', filelist='../skim_filelists/ttbar_2018_10Jan2022/SingleMuon_Run2.txt')

# ttbar = sam.Sample(name='ttbar', sampletype='mc', files=['../prova_ttbar.root'],
#     sampledesc= {**lumi_info, 'xs' : 815.96, 'xs_units' : 'pb'}
# )
# data_obs = sam.Sample(name='data_obs', sampletype='data', files=['../prova_singlemu_ttbarskim.root'])


# samples = [ttbar, data_obs]
samples = [nmssm]

###################### ROOT FUNCTIONS #######################
## all variables to declare to the gInterpreter should be listed in a "declarations" variable

minv = """
double minv(double pt1, double eta1, double phi1, double m1, double pt2, double eta2, double phi2, double m2, double pt3, double eta3, double phi3, double m3) {
    ROOT::Math::PtEtaPhiMVector v1 (pt1, eta1, phi1, m1);
    ROOT::Math::PtEtaPhiMVector v2 (pt2, eta2, phi2, m2);
    ROOT::Math::PtEtaPhiMVector v3 (pt3, eta3, phi3, m3);
    double m = (v1+v2+v3).M();
    return m;
}
"""
btagavg = """
double btagavg(double btag1, double btag2, double btag3, double btag4, double btag5, double btag6) {
    double btagsum = (btag1 + btag2 + btag3 + btag4 + btag5 + btag6)/6;
    return btagsum;
}
"""
mdiff = """
double mdiff(double m) {
    double deltam = std::abs(m - 125);
    return deltam;
}
"""

declarations = [minv, btagavg, mdiff]

###################### NEW COLUMNS #######################
## all columns to declare in the samples should be listed in a "new_columns" dictionary (name -> expression)

new_columns = collections.OrderedDict()
new_columns['mx'] = 'minv(HX_pt, HX_eta, HX_phi, HX_m, HY1_pt, HY1_eta, HY1_phi, HY1_m, HY2_pt, HY2_eta, HY2_phi, HY2_m)'

###################### SELECTIONS #######################

selections_defs = {
    'CRls' : 'mdiff > 60 && btagsum < 0.65',
    'CRhs' : 'mdiff > 60 && btagsum >= 0.65',
    'VRls' : 'mdiff <= 60 && mdiff > 25 && btagsum < 0.65',
    'VRhs' : 'mdiff <= 60 && mdiff > 25 && btagsum >= 0.65'
    # 'baseline' : 'n_mu_loose == 1 && n_ele_loose == 1 && bjet1_pt > 20 && bjet2_pt > 20',
    # 'tight'    : 'n_mu_loose == 1 && n_ele_loose == 1 && bjet1_pt > 30 && bjet2_pt > 30 && mu_1_pt > 30 && ele_1_pt > 20',
    # 'tight2b'  : 'n_mu_loose == 1 && n_ele_loose == 1 && bjet1_pt > 30 && bjet2_pt > 30 && mu_1_pt > 30 && ele_1_pt > 20 && bjet1_DeepJet > 0.2783 && bjet2_DeepJet > 0.2783',
}

###################### WEIGHTS DEFINITION #######################
# weights that appear in norm_weights undergo a rescaling by sum(w) when filling the plots
# these weights must be defined both in the norm_tree and in the event_tree

# norm_weights = ['genWeight', 'PUWeight']
norm_weights = ['genWeight']

###################### HISTOGRAMS DESCRIPTIONS #######################
# all histograms should be listed in a "histos" list
# a histogram is represented by a dictionary containing its description

# histos_descs = [
#     {
#         'var'        : 'bjet1_pt',
#         'weightlist' : ['genWeight'],
#         'bins'       : (100, 0, 400),
#         'nametag'    : 'gw'
#     },
#     {
#         'var'        : 'bjet1_pt',
#         'weightlist' : ['genWeight', 'PUWeight'],
#         'bins'       : (100, 0, 400),
#         'nametag'    : 'gw_pu'
#     },
#     {
#         'var'        : 'bjet1_pt',
#         'weightlist' : ['genWeight', 'PUWeight', 'btagSF_WP_M'],
#         'bins'       : (100, 0, 400),
#         'nametag'    : 'gw_pu_btagsf'
#     },
#     {
#         'var'        : 'rhofastjet_all',
#         'weightlist' : ['genWeight'],
#         'bins'       : (100, 0, 100),
#         'nametag'    : 'gw'
#     },
#     {
#         'var'        : 'rhofastjet_all',
#         'weightlist' : ['genWeight', 'PUWeight'],
#         'bins'       : (100, 0, 100),
#         'nametag'    : 'gw_pu'
#     },
#     {
#         'var'        : 'rhofastjet_all',
#         'weightlist' : ['genWeight', 'PUWeight', 'btagSF_WP_M'],
#         'bins'       : (100, 0, 100),
#         'nametag'    : 'gw_pu_btagsf'
#     },    
# ]

histos_descs = [
    {
        'var'        : 'mx',
        'weightlist' : ['genWeight'],
        'bins'       : (100, 0, 2000),
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

import modules.Sample as sam
import collections
import copy

###################### COMMON INFO, DEFINITIONS, ETC #######################
## things reused throughout the config (to avoid redundance)

lumi_info = {'lumi' : 59.740, 'lumi_units' : 'fbinv'}

###################### SAMPLES #######################
## all samples to be processed should be in a "samples" list

version = 't8btag_minmass/'
path = '/eos/uscms/store/user/ekoenig/8BAnalysis/NTuples/2018/preselection/'+version

nmssm = sam.Sample(name='nmssm', sampletype='mc', files=[path+'/NMSSM_XYY_YToHH_8b/NMSSM_XYY_YToHH_8b_MX_1000_MY_450_accstudies.root'],
    sampledesc= {**lumi_info, 'xs' : 10, 'xs_units' : 'fb'}
)
# data_obs = sam.Sample(name='data_obs', sampletype='data', filelist='../skim_filelists/ttbar_2018_10Jan2022/SingleMuon_Run2.txt')

ttbar_xs = {
    'TTJets':831.76
}

ttbars = [
    sam.Sample(name='ttbar', sampletype='mc', filelist='filelists/'+version+sample+'.txt',
        sampledesc= {**lumi_info, 'xs' : xsec, 'xs_units' : 'pb'}
    )
    for sample, xsec in ttbar_xs.items()
]

qcd_xs = {
    "QCD_bEnriched_HT100to200_TuneCP5_13TeV-madgraph-pythia8": 1127000.0,
    "QCD_bEnriched_HT200to300_TuneCP5_13TeV-madgraph-pythia8": 80430.0,
    "QCD_bEnriched_HT300to500_TuneCP5_13TeV-madgraph-pythia8": 16620.0,
    "QCD_bEnriched_HT500to700_TuneCP5_13TeV-madgraph-pythia8": 1487.0,
    "QCD_bEnriched_HT700to1000_TuneCP5_13TeV-madgraph-pythia8": 296.5,
    "QCD_bEnriched_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8": 46.61,
    "QCD_bEnriched_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8": 3.72,
    "QCD_bEnriched_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8": 0.6462,

    "QCD_HT100to200_BGenFilter_TuneCP5_13TeV-madgraph-pythia8": 1275000.0,
    "QCD_HT200to300_BGenFilter_TuneCP5_13TeV-madgraph-pythia8": 111700.0,
    "QCD_HT300to500_BGenFilter_TuneCP5_13TeV-madgraph-pythia8": 27960.0,
    "QCD_HT500to700_BGenFilter_TuneCP5_13TeV-madgraph-pythia8": 3078.0,
    "QCD_HT700to1000_BGenFilter_TuneCP5_13TeV-madgraph-pythia8": 721.8,
    "QCD_HT1000to1500_BGenFilter_TuneCP5_13TeV-madgraph-pythia8": 138.2,
    "QCD_HT1500to2000_BGenFilter_TuneCP5_13TeV-madgraph-pythia8": 13.61,
    "QCD_HT2000toInf_BGenFilter_TuneCP5_13TeV-madgraph-pythia8": 2.92,
    }

qcds = [
    sam.Sample(name='qcd', sampletype='mc', filelist='filelists/'+version+sample+'.txt',
    sampledesc={**lumi_info, 'xs':xsec, 'xs_units':'pb'}
    )
    for sample,xsec in qcd_xs.items()
]


data_obs = [
    sam.Sample(name='data_obs', sampletype='mc', filelist='filelists/'+version+sample+'.txt',
    sampledesc={**lumi_info, 'xs':xsec, 'xs_units':'pb'}
    )
    for sample,xsec in dict(**qcd_xs,**ttbar_xs).items()
]


# samples = [ttbar, data_obs]
samples = [nmssm] + ttbars + qcds + data_obs
###################### ROOT FUNCTIONS #######################
## all variables to declare to the gInterpreter should be listed in a "declarations" variable

# minv = """
# double minv(double pt1, double eta1, double phi1, double m1, double pt2, double eta2, double phi2, double m2, double pt3, double eta3, double phi3, double m3) {
#     ROOT::Math::PtEtaPhiMVector v1 (pt1, eta1, phi1, m1);
#     ROOT::Math::PtEtaPhiMVector v2 (pt2, eta2, phi2, m2);
#     ROOT::Math::PtEtaPhiMVector v3 (pt3, eta3, phi3, m3);
#     double m = (v1+v2+v3).M();
#     return m;
# }
# """
# btagavg = """
# double btagavg(double btag1, double btag2, double btag3, double btag4, double btag5, double btag6) {
#     double btagsum = (btag1 + btag2 + btag3 + btag4 + btag5 + btag6)/6;
#     return btagsum;
# }
# """
# mdiff = """
# double mdiff(double m) {
#     double deltam = std::abs(m - 125);
#     return deltam;
# }
# """
n_medium_btag="""
int n_medium_btag(double btag1, double btag2, double btag3, double btag4, double btag5, double btag6, double btag7, double btag8) {
    double btagwp = 0.2783;
    std::vector<double> btags = {btag1,btag2,btag3,btag4,btag5,btag6,btag7,btag8};
    int n_medium = 0;
    for (double btag : btags) {
        if (btag > btagwp) {
            n_medium++;
        }
    }
    return n_medium;
}
"""

# declarations = [minv, btagavg, mdiff]
declarations = [n_medium_btag]

###################### NEW COLUMNS #######################
## all columns to declare in the samples should be listed in a "new_columns" dictionary (name -> expression)

new_columns = collections.OrderedDict()
# new_columns['mx'] = 'minv(HX_pt, HX_eta, HX_phi, HX_m, HY1_pt, HY1_eta, HY1_phi, HY1_m, HY2_pt, HY2_eta, HY2_phi, HY2_m)'
# new_columns['btagsum'] = 'btagavg(HX_b1_DeepJet, HX_b2_DeepJet, HY1_b1_DeepJet, HY1_b2_DeepJet, HY2_b1_DeepJet, HY2_b2_DeepJet)'
# new_columns['mXdiff'] = 'mdiff(HX_m)'
# new_columns['mY1diff'] = 'mdiff(HY1_m)'
# new_columns['mY2diff'] = 'mdiff(HY2_m)'
new_columns['n_medium_btag'] = 'n_medium_btag(H1Y1_b1_btag,H1Y1_b2_btag,H2Y1_b1_btag,H2Y1_b2_btag,H1Y2_b1_btag,H1Y2_b2_btag,H2Y2_b1_btag,H2Y2_b2_btag)'

###################### SELECTIONS #######################

selections_defs = {
    # 'baseline' : 'n_mu_loose == 1 && n_ele_loose == 1 && bjet1_pt > 20 && bjet2_pt > 20',
    # 'tight'    : 'n_mu_loose == 1 && n_ele_loose == 1 && bjet1_pt > 30 && bjet2_pt > 30 && mu_1_pt > 30 && ele_1_pt > 20',
    # 'tight2b'  : 'n_mu_loose == 1 && n_ele_loose == 1 && bjet1_pt > 30 && bjet2_pt > 30 && mu_1_pt > 30 && ele_1_pt > 20 && bjet1_DeepJet > 0.2783 && bjet2_DeepJet > 0.2783',
    'baseline' : 'n_medium_btag > 3',
    'tight5b'  : 'n_medium_btag > 4',
    'loose3b'  : 'n_medium_btag > 2'
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
        'var'        : 'X_m',
        'weightlist' : ['genWeight'],
        'bins'       : (100, 500, 2000),
    }, 
    {
        'var'        : 'X_m',
        'weightlist' : ['genWeight'],
        'bins'       : (1  , 800, 1200),
        'nametag'    : 'single_bin'
    },
    {
        'var'        : 'X_m',
        'weightlist' : ['genWeight'],
        'bins'       : (50  , 500, 2000),
        'nametag'    : '50_bins'
    },
    {
        'var'        : 'X_m',
        'weightlist' : ['genWeight'],
        'bins'       : (25  , 500, 2000),
        'nametag'    : '25_bins'
    }
]

### declare the histograms - make one histogram for every selection declared
### any type of manipulation can be done here
histos = []
for hd in histos_descs:
    for s in selections_defs.keys():
        d2 = copy.deepcopy(hd)
        d2['sel'] = s
        histos.append(d2)

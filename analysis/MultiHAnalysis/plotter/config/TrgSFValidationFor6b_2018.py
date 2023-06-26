import modules.Sample as sam
import collections
import ROOT
import copy
import numpy as np
import hep_ml

ROOT.gInterpreter.ProcessLine('#include <cmath>')

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#                      SAMPLES
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
year = "2018"

from modules.Samples_NMSSM_XYH_YToHH_6b import dsetGroups
samples = dsetGroups["NMSSM_XYH_YToHH_6b"][year] # + dsetGroups["TTJets"][year]

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#                  ROOT FUNCTIONS
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
average_btag = """
double average_btag(std::vector<double> bdiscs) {
  double sum = 0.0;
  for (unsigned int i=0; i<bdiscs.size(); i++)
    {
      sum += bdiscs.at(i);
    }
  return sum/bdiscs.size();
}
"""

Dm_cand = """
double Dm_cand(double HX_m, double H1_m, double H2_m, double center)
{
  double dm_HX  = std::abs(HX_m - center);
  double dm_H1 = std::abs(H1_m - center);
  double dm_H2 = std::abs(H2_m - center);

  dm_HX = dm_HX * dm_HX;
  dm_H1 = dm_H1 * dm_H1;
  dm_H2 = dm_H2 * dm_H2;

  double sum = dm_HX + dm_H1 + dm_H2;
  double dm_cand = sqrt(sum);
  return dm_cand;
}
"""

## all variables to declare to the gInterpreter should be listed in a "declarations" variable
declarations = [average_btag, Dm_cand]

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#              New columns to declare
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
new_columns                    = collections.OrderedDict()
new_columns["X_m_scaled"]      = "X_m"
new_columns["X_m_scaledUp"]    = "X_m"
new_columns["X_m_scaledDown"]  = "X_m"
new_columns["HX_m_scaled"]     = "HX_m"
new_columns["HX_m_scaledUp"]   = "HX_m"
new_columns["HX_m_scaledDown"] = "HX_m"
new_columns["H1_m_scaled"]     = "H1_m"
new_columns["H1_m_scaledUp"]   = "H1_m"
new_columns["H1_m_scaledDown"] = "H1_m"
new_columns["H2_m_scaled"]     = "H2_m"
new_columns["H2_m_scaledUp"]   = "H2_m"
new_columns["H2_m_scaledDown"] = "H2_m"

#new_columns["leptonveto"]    = "n_muon == 0 && n_ele == 0"
new_columns['average_btag']  = 'average_btag({H1_b1_btag, H1_b2_btag, H2_b1_btag, H2_b2_btag, HX_b1_btag, HX_b2_btag})'
new_columns['Dm_cand']       = 'Dm_cand(HX_m, H1_m, H2_m, 125.0)'

new_columns['A_SR_mask']     = 'Dm_cand <= 30.0'
new_columns['A_CR_mask']     = '(Dm_cand > 30.0) && (Dm_cand <= 40.0)' # Analysis CR
new_columns['ls_mask']       = 'average_btag < 0.6'
new_columns['hs_mask']       = 'average_btag >= 0.6'

new_columns['A_CRls_mask']   = 'A_CR_mask && ls_mask'
new_columns['A_CRhs_mask']   = 'A_CR_mask && hs_mask'
new_columns['A_SRls_mask']   = 'A_SR_mask && ls_mask'
new_columns['A_SRhs_mask']   = 'A_SR_mask && hs_mask'
  
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#              Perform plots for all selections
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
selections_defs = {
    'baseline'            : 'n_jet > 0',
    'A_SR_highbtag'       : 'A_SRhs_mask == 1',
    'A_CR_highbtag'       : 'A_CRhs_mask == 1',
    'A_SR_lowbtag'        : 'A_SRls_mask == 1',
    'A_CR_lowbtag'        : 'A_CRls_mask == 1',
}

###################### WEIGHTS DEFINITION #######################
# weights that appear in norm_weights undergo a rescaling by sum(w) when filling the plots
# these weights must be defined both in the norm_tree and in the event_tree
norm_weights = ['genWeight', 'PUWeight']

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Histograms to be created
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
minMX = 375.0
maxMX = 2000.0
nbins = int(65)

x = 375
binList = [x]
for i in range(0, 65):
    x+= 25.0
    binList.append(x)
mBins = tuple(binList)

histos_descs = [
    # For the trigger validation
    {'var': 'X_m',             'weightlist': ["genWeight"], 'nbins': nbins, 'min': minMX, 'max': maxMX},
    {'var': 'X_m_scaled',      'weightlist': ["genWeight", 'triggerMcEfficiency'], 'nbins': nbins, 'min': minMX, 'max': maxMX},
    {'var': 'X_m_scaledUp',    'weightlist': ["genWeight", 'triggerMcEfficiencyUp'], 'nbins': nbins, 'min': minMX, 'max': maxMX},
    {'var': 'X_m_scaledDown',  'weightlist': ["genWeight", 'triggerMcEfficiencyDown'], 'nbins': nbins, 'min': minMX, 'max': maxMX},
    {'var': 'HX_m',            'weightlist': ["genWeight"], 'bins': (300, 0.0, 600),},
    {'var': 'HX_m_scaled',     'weightlist': ["genWeight", 'triggerMcEfficiency'], 'bins': (300, 0.0, 600),},
    {'var': 'HX_m_scaledUp',   'weightlist': ["genWeight", 'triggerMcEfficiencyUp'], 'bins': (300, 0.0, 600),},
    {'var': 'HX_m_scaledDown', 'weightlist': ["genWeight", 'triggerMcEfficiencyDown'], 'bins': (300, 0.0, 600),},
    {'var': 'H1_m',            'weightlist': ["genWeight"], 'bins': (300, 0.0, 600),},
    {'var': 'H1_m_scaled',     'weightlist': ["genWeight", 'triggerMcEfficiency'], 'bins': (300, 0.0, 600),},
    {'var': 'H1_m_scaledUp',   'weightlist': ["genWeight", 'triggerMcEfficiencyUp'], 'bins': (300, 0.0, 600),},
    {'var': 'H1_m_scaledDown', 'weightlist': ["genWeight", 'triggerMcEfficiencyDown'], 'bins': (300, 0.0, 600),},
    {'var': 'H2_m',            'weightlist': ["genWeight"], 'bins': (300, 0.0, 600),},
    {'var': 'H2_m_scaled',     'weightlist': ["genWeight", 'triggerMcEfficiency'], 'bins': (300, 0.0, 600),},
    {'var': 'H2_m_scaledUp',   'weightlist': ["genWeight", 'triggerMcEfficiencyUp'], 'bins': (300, 0.0, 600),},
    {'var': 'H2_m_scaledDown', 'weightlist': ["genWeight", 'triggerMcEfficiencyDown'], 'bins': (300, 0.0, 600),},
    {'var': 'triggerScaleFactor', 'weightlist' : ["genWeight"], 'bins': (200, -2.0, 2.0),},
    {'var': 'triggerScaleFactorDown', 'weightlist' : ["genWeight"], 'bins': (200, -2.0, 2.0),},
    {'var': 'triggerScaleFactorUp', 'weightlist' : ["genWeight"], 'bins': (200, -2.0, 2.0),},
    {'var': 'triggerDataEfficiency', 'weightlist' : ["genWeight"], 'bins': (100, 0.0, 1.0),},
    {'var': 'triggerMcEfficiency', 'weightlist':["genWeight"], 'bins': (100, 0.0, 1.0),},
    {'var': 'triggerDataEfficiencyUp', 'weightlist':["genWeight"], 'bins': (100, 0.0, 1.0),},
    {'var': 'triggerDataEfficiencyDown', 'weightlist':["genWeight"], 'bins': (100, 0.0, 1.0),},
    {'var': 'triggerMcEfficiencyUp', 'weightlist':["genWeight"], 'bins': (100, 0.0, 1.0),},
    {'var': 'triggerMcEfficiencyDown', 'weightlist':["genWeight"], 'bins': (100, 0.0, 1.0),},
    {'var': 'HLT_Data_effL1', 'weightlist':["genWeight"], 'bins': (100, 0.0, 1.0),},
    {'var': 'HLT_Data_effQuad30CaloJet', 'weightlist':["genWeight"], 'bins': (100, 0.0, 1.0),},
    {'var': 'HLT_Data_effCaloHT', 'weightlist':["genWeight"], 'bins': (100, 0.0, 1.0),},
    {'var': 'HLT_Data_effQuad30PFJet', 'weightlist':["genWeight"], 'bins': (100, 0.0, 1.0),},
    {'var': 'HLT_Data_effSingle75PFJet', 'weightlist':["genWeight"], 'bins': (100, 0.0, 1.0),},
    {'var': 'HLT_Data_effDouble60PFJet', 'weightlist':["genWeight"], 'bins': (100, 0.0, 1.0),},
    {'var': 'HLT_Data_effTriple54PFJet', 'weightlist':["genWeight"], 'bins': (100, 0.0, 1.0),},
    {'var': 'HLT_Data_effQuad40PFJet', 'weightlist':["genWeight"], 'bins': (100, 0.0, 1.0),},
    {'var': 'HLT_Data_effPFHT', 'weightlist':["genWeight"], 'bins': (100, 0.0, 1.0),},
    {'var': 'HLT_Data_threeBtagEfficiency', 'weightlist':["genWeight"], 'bins': (100, 0.0, 1.0),},
    {'var': 'HLT_Data_twoBtagEfficiency', 'weightlist':["genWeight"], 'bins': (100, 0.0, 1.0),},
    {'var': 'HLT_MC_effL1', 'weightlist':["genWeight"], 'bins': (100, 0.0, 1.0),},
    {'var': 'HLT_MC_effQuad30CaloJet', 'weightlist':["genWeight"], 'bins': (100, 0.0, 1.0),},
    {'var': 'HLT_MC_effCaloHT', 'weightlist':["genWeight"], 'bins': (100, 0.0, 1.0),},
    {'var': 'HLT_MC_effQuad30PFJet', 'weightlist':["genWeight"], 'bins': (100, 0.0, 1.0),},
    {'var': 'HLT_MC_effSingle75PFJet', 'weightlist':["genWeight"], 'bins': (100, 0.0, 1.0),},
    {'var': 'HLT_MC_effDouble60PFJet', 'weightlist':["genWeight"], 'bins': (100, 0.0, 1.0),},
    {'var': 'HLT_MC_effTriple54PFJet', 'weightlist':["genWeight"], 'bins': (100, 0.0, 1.0),},
    {'var': 'HLT_MC_effQuad40PFJet', 'weightlist':["genWeight"], 'bins': (100, 0.0, 1.0),},
    {'var': 'HLT_MC_effPFHT', 'weightlist':["genWeight"], 'bins': (100, 0.0, 1.0),},
    {'var': 'HLT_MC_threeBtagEfficiency', 'weightlist':["genWeight"], 'bins': (100, 0.0, 1.0),},
    {'var': 'HLT_MC_twoBtagEfficiency', 'weightlist':["genWeight"], 'bins': (100, 0.0, 1.0),},
]

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Create a histogram for each selection declared
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
histos = []
for hd in histos_descs:
    for s in selections_defs.keys():
        d2 = copy.deepcopy(hd)
        d2['sel'] = s
        histos.append(d2)

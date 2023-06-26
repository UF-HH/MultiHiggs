import os
import modules.Sample as sam
from modules.XSections import bkgXSectionList as xs

# This needs to be calculated. No hardcoded lumi. #fixme
lumiMap = {}
lumiMap["2018A"] = {"lumi": 14030, "lumi_units" : "pbinv"}
lumiMap["2018B"] = {"lumi": 7070,  "lumi_units" : "pbinv"}
lumiMap["2018C"] = {"lumi": 6900,  "lumi_units" : "pbinv"}
lumiMap["2018D"] = {"lumi": 31750, "lumi_units" : "pbinv"}
lumiMap["2018" ] = {'lumi' : 59.740, 'lumi_units' : 'fbinv'}

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#                      DEFINITIONS
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
version    = ""
energy     = "13" # TeV
redirector = "root://cmsxrootd.fnal.gov/"

directories = {}
directories["2016"] = ''
directories["2017"] = ''
directories["2018"] = "/store/user/mkolosov/HHHTo6B/RunIISummer20UL18_NoLeptonVeto_TrgSFwMatching_TrgPtThresholdsApplied_21Feb2023/"

directories["2018-trgSFValidation-wTrg"]  = "/store/user/mkolosov/HHHTo6B/RunIISummer20UL18_NoLeptonVeto_TrgSFwMatching_TrgPtThresholdsApplied_21Feb2023/"
directories["2018-trgSFValidation-noTrg"] = "/store/user/mkolosov/HHHTo6B/RunIISummer20UL18_NoLeptonVeto_NoTrgApplied_TrgPtThresholdsApplied_21Feb2023/"

path = {}
path["2016"] = ""
path["2017"] = ""
#path["2018"] = "".join([redirector, directories["2018-trgSFValidation-wTrg"]])
path["2018"] = "".join([redirector, directories["2018-trgSFValidation-noTrg"]])

dsetGroups = {}
dsetGroups["NMSSM_XYH_YToHH_6b"] = {"2018" : [], "2017" : [], "2016" : []}
dsetGroups["Data"]               = {"2018" : [], "2017" : [], "2016" : []}
dsetGroups["TTJets"]             = {"2018" : [], "2017" : [], "2016" : []}
dsetGroups["QCD"]                = {"2018" : [], "2017" : [], "2016" : []}


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Dataset JetHT
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
JetHT_Run2018A = sam.Sample(name = "Data", sampletype="data", files=[path["2018"]+'/JetHT_Run2018A/ntuple.root'], sampledesc={**lumiMap["2018A"]})
JetHT_Run2018B = sam.Sample(name = "Data", sampletype="data", files=[path["2018"]+'/JetHT_Run2018B/ntuple.root'], sampledesc={**lumiMap["2018B"]})
JetHT_Run2018C = sam.Sample(name = "Data", sampletype="data", files=[path["2018"]+'/JetHT_Run2018C/ntuple.root'], sampledesc={**lumiMap["2018C"]})
JetHT_Run2018D = sam.Sample(name = "Data", sampletype="data", files=[path["2018"]+'/JetHT_Run2018D/ntuple.root'], sampledesc={**lumiMap["2018D"]})
dsetGroups["Data"]["2018"] = [JetHT_Run2018A, JetHT_Run2018B, JetHT_Run2018C, JetHT_Run2018D]

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Dataset TTJets
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
TTJets = sam.Sample(name       = "TTJets",
                    sampletype = "mc",
                    files      = [path["2018"]+'TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/ntuple.root'], 
                    sampledesc = {**lumiMap["2018"], 'xs' : xs.get("TTJets", energy), 'xs_units' : 'pb'})
dsetGroups["TTJets"]["2018"]    = [TTJets]

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Dataset QCD b-Enriched
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
QCD_bEnriched_HT100to200 = sam.Sample(name       = "QCD",
                                      sampletype = "mc",
                                      files      = [path["2018"]+'QCD_bEnriched_HT100to200_TuneCP5_13TeV-madgraph-pythia8/ntuple.root'],
                                      sampledesc = {**lumiMap["2018"], 'xs': xs.get("QCD_bEnriched_HT100to200", energy), 'xs_units':'pb'})
QCD_bEnriched_HT200to300 = sam.Sample(name       = "QCD",
                                      sampletype = "mc",
                                      files   = [path["2018"]+'QCD_bEnriched_HT200to300_TuneCP5_13TeV-madgraph-pythia8/ntuple.root'],
                                      sampledesc = {**lumiMap["2018"], 'xs': xs.get("QCD_bEnriched_HT200to300", energy), 'xs_units':'pb'})
QCD_bEnriched_HT300to500 = sam.Sample(name       = "QCD",
                                      sampletype = "mc",
                                      files   = [path["2018"]+'QCD_bEnriched_HT300to500_TuneCP5_13TeV-madgraph-pythia8/ntuple.root'],
                                      sampledesc = {**lumiMap["2018"], 'xs': xs.get("QCD_bEnriched_HT300to500", energy), 'xs_units':'pb'})
QCD_bEnriched_HT500to700 = sam.Sample(name       = "QCD",
                                      sampletype = "mc",
                                      files = [path["2018"]+'QCD_bEnriched_HT500to700_TuneCP5_13TeV-madgraph-pythia8/ntuple.root'],
                                      sampledesc = {**lumiMap["2018"], 'xs': xs.get("QCD_bEnriched_HT500to700", energy), 'xs_units':'pb'})
QCD_bEnriched_HT700to1000 = sam.Sample(name        = "QCD",
                                       sampletype  = "mc",
                                       files       = [path["2018"]+'QCD_bEnriched_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/ntuple.root'],
                                       sampledesc  = {**lumiMap["2018"], 'xs': xs.get("QCD_bEnriched_HT700to1000", energy), 'xs_units':'pb'})
QCD_bEnriched_HT1000to1500 = sam.Sample(name       = "QCD",
                                        sampletype = "mc",
                                        files      = [path["2018"]+'QCD_bEnriched_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/ntuple.root'],
                                        sampledesc = {**lumiMap["2018"], 'xs': xs.get("QCD_bEnriched_HT1000to1500", energy), 'xs_units':'pb'})
QCD_bEnriched_HT1500to2000 = sam.Sample(name       = "QCD",
                                        sampletype = "mc",
                                        files      = [path["2018"]+'QCD_bEnriched_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/ntuple.root'],
                                        sampledesc = {**lumiMap["2018"], 'xs': xs.get("QCD_bEnriched_HT1500to2000", energy), 'xs_units':'pb'})
QCD_bEnriched_HT2000toInf = sam.Sample(name        = "QCD",
                                       sampletype  = "mc",
                                       files       = [path["2018"]+'QCD_bEnriched_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/ntuple.root'],
                                       sampledesc = {**lumiMap["2018"], 'xs': xs.get("QCD_bEnriched_HT2000toInf", energy), 'xs_units':'pb'})

dsetGroups["QCD"]["2018"]       = [QCD_bEnriched_HT100to200,
                                   QCD_bEnriched_HT200to300,
                                   QCD_bEnriched_HT300to500,
                                   QCD_bEnriched_HT500to700,
                                   QCD_bEnriched_HT700to1000,
                                   QCD_bEnriched_HT1000to1500,
                                   QCD_bEnriched_HT1500to2000,
                                   QCD_bEnriched_HT2000toInf]

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Dataset NMSSM XToYHTo6B
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
masses = {}

masses["400"] = ["250"]
masses["450"] = ["250", "300"]
masses["500"] = ["250", "350"]
masses["550"] = ["250", "300", "350", "400"]
masses["600"] = ["250", "300", "350", "400", "450"]
masses["650"] = ["250", "300", "350", "400", "450"]
masses["700"] = ["250", "300", "350", "400", "450", "500"]
masses["750"] = ["300", "350", "400", "450", "500", "600"]
masses["800"] = ["250", "300", "350", "400", "450", "500", "600"]
masses["850"] = ["250", "300", "350", "400", "450", "500", "600", "700"]
masses["900"] = ["250", "300", "350", "400", "450", "500", "600", "700"]
masses["950"] = ["300", "350", "400", "450", "500", "600", "700", "800"]
masses["1000"] = ["250", "350", "400", "450", "500", "600", "700", "800"]
masses["1100"] = ["250", "300", "350", "400", "450", "500", "600", "700", "800", "900"]
masses["1200"] = ["250", "300", "350", "400", "450", "600", "700", "800", "900", "1000"]

#masses["1300"] = ["250", "300", "350", "400", "450", "600", "700", "800", "900", "1000", "1100"]
#masses["1400"] = ["250", "300", "350", "400", "450", "500", "600", "700", "800", "900", "1000", "1100", "1200"]

# to be added
'''
NMSSM_XToYHTo6B_MX-1500_MY-1000_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1500_MY-1100_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1500_MY-1200_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1500_MY-1300_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1500_MY-250_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1500_MY-300_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1500_MY-350_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1500_MY-400_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1500_MY-450_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1500_MY-500_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1500_MY-600_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1500_MY-700_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1500_MY-800_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1500_MY-900_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1600_MY-1000_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1600_MY-1100_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1600_MY-1200_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1600_MY-1300_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1600_MY-1400_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1600_MY-250_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1600_MY-300_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1600_MY-350_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1600_MY-400_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1600_MY-450_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1600_MY-500_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1600_MY-600_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1600_MY-700_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1600_MY-800_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1600_MY-900_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1700_MY-1000_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1700_MY-1100_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1700_MY-1200_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1700_MY-1300_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1700_MY-1400_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1700_MY-250_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1700_MY-300_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1700_MY-350_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1700_MY-400_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1700_MY-450_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1700_MY-500_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1700_MY-600_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1700_MY-700_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1700_MY-800_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1700_MY-900_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1800_MY-1000_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1800_MY-1100_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1800_MY-1200_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1800_MY-1300_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1800_MY-1400_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1800_MY-1600_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1800_MY-250_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1800_MY-300_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1800_MY-350_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1800_MY-400_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1800_MY-450_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1800_MY-500_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1800_MY-600_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1800_MY-700_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1800_MY-800_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1800_MY-900_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1900_MY-1000_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1900_MY-1100_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1900_MY-1200_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1900_MY-1300_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1900_MY-1400_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1900_MY-1600_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1900_MY-250_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1900_MY-300_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1900_MY-350_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1900_MY-400_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1900_MY-450_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1900_MY-500_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1900_MY-600_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1900_MY-700_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1900_MY-800_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-1900_MY-900_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2000_MY-1000_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2000_MY-1100_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2000_MY-1200_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2000_MY-1300_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2000_MY-1400_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2000_MY-1600_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2000_MY-250_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2000_MY-300_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2000_MY-400_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2000_MY-450_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2000_MY-500_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2000_MY-600_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2000_MY-700_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2000_MY-800_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2000_MY-900_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2200_MY-1000_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2200_MY-1100_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2200_MY-1200_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2200_MY-1300_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2200_MY-1400_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2200_MY-1600_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2200_MY-1800_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2200_MY-2000_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2200_MY-250_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2200_MY-300_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2200_MY-350_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2200_MY-400_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2200_MY-450_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2200_MY-500_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2200_MY-600_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2200_MY-700_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2200_MY-800_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2200_MY-900_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2400_MY-1000_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2400_MY-1100_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2400_MY-1200_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2400_MY-1300_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2400_MY-1400_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2400_MY-1600_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2400_MY-1800_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2400_MY-2000_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2400_MY-2200_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2400_MY-250_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2400_MY-300_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2400_MY-350_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2400_MY-400_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2400_MY-450_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2400_MY-600_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2400_MY-700_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2400_MY-800_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2400_MY-900_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2500_MY-1000_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2500_MY-1100_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2500_MY-1200_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2500_MY-1300_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2500_MY-1400_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2500_MY-1600_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2500_MY-1800_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2500_MY-2000_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2500_MY-2200_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2500_MY-250_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2500_MY-300_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2500_MY-350_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2500_MY-450_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2500_MY-500_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2500_MY-700_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2500_MY-800_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2500_MY-900_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2600_MY-1000_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2600_MY-1100_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2600_MY-1200_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2600_MY-1300_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2600_MY-1400_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2600_MY-1600_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2600_MY-1800_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2600_MY-2000_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2600_MY-2200_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2600_MY-2400_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2600_MY-250_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2600_MY-300_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2600_MY-350_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2600_MY-400_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2600_MY-500_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2600_MY-600_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2600_MY-700_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2600_MY-800_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2600_MY-900_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2800_MY-1000_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2800_MY-1100_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2800_MY-1200_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2800_MY-1400_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2800_MY-1600_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2800_MY-1800_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2800_MY-2000_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2800_MY-2200_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2800_MY-2400_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2800_MY-2500_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2800_MY-250_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2800_MY-2600_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2800_MY-300_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2800_MY-350_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2800_MY-400_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2800_MY-450_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2800_MY-500_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2800_MY-600_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2800_MY-700_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2800_MY-800_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-2800_MY-900_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-3000_MY-1000_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-3000_MY-1100_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-3000_MY-1200_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-3000_MY-1300_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-3000_MY-1400_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-3000_MY-1600_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-3000_MY-1800_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-3000_MY-2000_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-3000_MY-2200_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-3000_MY-2400_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-3000_MY-2500_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-3000_MY-250_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-3000_MY-2600_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-3000_MY-2800_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-3000_MY-300_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-3000_MY-350_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-3000_MY-400_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-3000_MY-450_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-3000_MY-500_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-3000_MY-600_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-3000_MY-800_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-3000_MY-900_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-3500_MY-1000_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-3500_MY-1100_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-3500_MY-1200_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-3500_MY-1300_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-3500_MY-1400_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-3500_MY-1600_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-3500_MY-1800_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-3500_MY-2000_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-3500_MY-2200_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-3500_MY-2400_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-3500_MY-2500_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-3500_MY-250_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-3500_MY-2600_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-3500_MY-2800_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-3500_MY-300_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-3500_MY-350_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-3500_MY-400_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-3500_MY-450_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-3500_MY-500_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-3500_MY-600_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-3500_MY-700_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-3500_MY-800_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-3500_MY-900_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-4000_MY-1000_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-4000_MY-1100_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-4000_MY-1200_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-4000_MY-1300_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-4000_MY-1400_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-4000_MY-1600_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-4000_MY-1800_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-4000_MY-2000_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-4000_MY-2200_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-4000_MY-2400_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-4000_MY-2500_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-4000_MY-250_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-4000_MY-2600_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-4000_MY-2800_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-4000_MY-300_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-4000_MY-350_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-4000_MY-400_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-4000_MY-450_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-4000_MY-500_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-4000_MY-600_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-4000_MY-700_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-4000_MY-800_TuneCP5_13TeV-madgraph-pythia8
NMSSM_XToYHTo6B_MX-4000_MY-900_TuneCP5_13TeV-madgraph-pythia8
'''

dsetGroups["NMSSM_XYH_YToHH_6b"]["2018"] = []
for i, MX in enumerate(masses):
    for MY in masses[MX]:
        sample = sam.Sample(name = "NMSSM_XToYHTo6B_MX-%s_MY-%s" % (MX, MY),
                            sampletype = "mc",
                            files      = [path["2018"]+"NMSSM_XToYHTo6B_MX-%s_MY-%s_TuneCP5_13TeV-madgraph-pythia8/ntuple.root" % (MX, MY)],
                            sampledesc = {**lumiMap["2018"], 'xs' : 1, 'xs_units' : 'pb'}
                            )
        dsetGroups["NMSSM_XYH_YToHH_6b"]["2018"].append(sample)
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

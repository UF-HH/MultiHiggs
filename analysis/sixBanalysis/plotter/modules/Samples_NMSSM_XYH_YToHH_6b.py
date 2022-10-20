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
directories["2018"] = '/store/user/mkolosov/HHHTo6B/Summer2018UL_29Sep2022_withoutLeptonVeto/' # Marina's samples

path = {}
path["2016"] = ""
path["2017"] = ""
path["2018"] = "".join([redirector, directories["2018"]])

JetHT_Run2018A = sam.Sample(name = "Data", sampletype="data", files=[path["2018"]+'/JetHT_Run2018A/ntuple.root'], sampledesc={**lumiMap["2018A"]})
JetHT_Run2018B = sam.Sample(name = "Data", sampletype="data", files=[path["2018"]+'/JetHT_Run2018B/ntuple.root'], sampledesc={**lumiMap["2018B"]})
JetHT_Run2018C = sam.Sample(name = "Data", sampletype="data", files=[path["2018"]+'/JetHT_Run2018C/ntuple.root'], sampledesc={**lumiMap["2018C"]})
JetHT_Run2018D = sam.Sample(name = "Data", sampletype="data", files=[path["2018"]+'/JetHT_Run2018D/ntuple.root'], sampledesc={**lumiMap["2018D"]})

# Marina's new samples
NMSSM_XYH_YToHH_6b_MX_450_MY_300 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_450_MY_300",
                                              sampletype = "mc",
                                              files      = [path["2018"]+'srosenzw_NMSSM_XYH_YToHH_6b_MX_450_MY_300_sl7_nano_100k/ntuple.root'],
                                              sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_500_MY_300 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_500_MY_300",
                                              sampletype = "mc",
                                              files      = [path["2018"]+'srosenzw_NMSSM_XYH_YToHH_6b_MX_500_MY_300_sl7_nano_100k/ntuple.root'],
                                              sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_600_MY_300 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_600_MY_300",
                                              sampletype = "mc",
                                              files      = [path["2018"]+'srosenzw_NMSSM_XYH_YToHH_6b_MX_600_MY_300_sl7_nano_100k/ntuple.root'],
                                              sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_600_MY_400 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_600_MY_400",
                                              sampletype = "mc",
                                              files      = [path["2018"]+'srosenzw_NMSSM_XYH_YToHH_6b_MX_600_MY_400_sl7_nano_100k/ntuple.root'],
                                              sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_700_MY_300 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_700_MY_300",
                                              sampletype = "mc",
                                              files      = [path["2018"]+'srosenzw_NMSSM_XYH_YToHH_6b_MX_700_MY_300_sl7_nano_100k/ntuple.root'],
                                              sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_700_MY_400 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_700_MY_400",
                                              sampletype = "mc",
                                              files      = [path["2018"]+'srosenzw_NMSSM_XYH_YToHH_6b_MX_700_MY_400_sl7_nano_2M/ntuple.root'],
                                              sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_700_MY_500 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_700_MY_500",
                                              sampletype = "mc",
                                              files      = [path["2018"]+'srosenzw_NMSSM_XYH_YToHH_6b_MX_700_MY_500_sl7_nano_100k/ntuple.root'],
                                              sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_800_MY_300 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_800_MY_300",
                                              sampletype = "mc",
                                              files      = [path["2018"]+'srosenzw_NMSSM_XYH_YToHH_6b_MX_800_MY_300_sl7_nano_100k/ntuple.root'],
                                              sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_800_MY_400 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_800_MY_400",
                                              sampletype = "mc",
                                              files      = [path["2018"]+'srosenzw_NMSSM_XYH_YToHH_6b_MX_800_MY_400_sl7_nano_100k/ntuple.root'],
                                              sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_800_MY_500 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_800_MY_500",
                                              sampletype = "mc",
                                              files      = [path["2018"]+'srosenzw_NMSSM_XYH_YToHH_6b_MX_800_MY_500_sl7_nano_100k/ntuple.root'],
                                              sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_800_MY_600 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_800_MY_600",
                                              sampletype = "mc",
                                              files      = [path["2018"]+'srosenzw_NMSSM_XYH_YToHH_6b_MX_800_MY_600_sl7_nano_100k/ntuple.root'],
                                              sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_900_MY_300 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_900_MY_300",
                                              sampletype = "mc",
                                              files      = [path["2018"]+'srosenzw_NMSSM_XYH_YToHH_6b_MX_900_MY_300_sl7_nano_100k/ntuple.root'],
                                              sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_900_MY_400 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_900_MY_400",
                                              sampletype = "mc",
                                              files      = [path["2018"]+'srosenzw_NMSSM_XYH_YToHH_6b_MX_900_MY_400_sl7_nano_100k/ntuple.root'],
                                              sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_900_MY_500 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_900_MY_500",
                                              sampletype = "mc",
                                              files      = [path["2018"]+'srosenzw_NMSSM_XYH_YToHH_6b_MX_900_MY_500_sl7_nano_100k/ntuple.root'],
                                              sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_900_MY_600 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_900_MY_600",
                                              sampletype = "mc",
                                              files      = [path["2018"]+'srosenzw_NMSSM_XYH_YToHH_6b_MX_900_MY_600_sl7_nano_100k/ntuple.root'],
                                              sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_900_MY_700 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_900_MY_700",
                                              sampletype = "mc",
                                              files      = [path["2018"]+'srosenzw_NMSSM_XYH_YToHH_6b_MX_900_MY_700_sl7_nano_100k/ntuple.root'],
                                              sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_1000_MY_300 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_1000_MY_300",
                                               sampletype = "mc",
                                               files      = [path["2018"]+'srosenzw_NMSSM_XYH_YToHH_6b_MX_1000_MY_300_sl7_nano_100k/ntuple.root'],
                                               sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_1000_MY_400 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_1000_MY_400",
                                               sampletype = "mc",
                                               files      = [path["2018"]+'srosenzw_NMSSM_XYH_YToHH_6b_MX_1000_MY_400_sl7_nano_100k/ntuple.root'],
                                               sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_1000_MY_500 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_1000_MY_500",
                                               sampletype = "mc",
                                               files      = [path["2018"]+'srosenzw_NMSSM_XYH_YToHH_6b_MX_1000_MY_500_sl7_nano_100k/ntuple.root'],
                                               sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_1000_MY_600 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_1000_MY_600",
                                               sampletype = "mc",
                                               files      = [path["2018"]+'srosenzw_NMSSM_XYH_YToHH_6b_MX_1000_MY_600_sl7_nano_100k/ntuple.root'],
                                               sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_1000_MY_700 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_1000_MY_700",
                                               sampletype = "mc",
                                               files      = [path["2018"]+'srosenzw_NMSSM_XYH_YToHH_6b_MX_1000_MY_700_sl7_nano_100k/ntuple.root'],
                                               sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_1000_MY_800 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_1000_MY_800",
                                               sampletype = "mc",
                                               files      = [path["2018"]+'srosenzw_NMSSM_XYH_YToHH_6b_MX_1000_MY_800_sl7_nano_100k/ntuple.root'],
                                               sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_1100_MY_300 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_1100_MY_300",
                                               sampletype = "mc",
                                               files      = [path["2018"]+'srosenzw_NMSSM_XYH_YToHH_6b_MX_1100_MY_300_sl7_nano_100k/ntuple.root'],
                                               sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_1100_MY_400 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_1100_MY_400",
                                               sampletype = "mc",
                                               files      = [path["2018"]+'srosenzw_NMSSM_XYH_YToHH_6b_MX_1100_MY_400_sl7_nano_100k/ntuple.root'],
                                               sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_1100_MY_500 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_1100_MY_500",
                                               sampletype = "mc",
                                               files      = [path["2018"]+'srosenzw_NMSSM_XYH_YToHH_6b_MX_1100_MY_500_sl7_nano_100k/ntuple.root'],
                                               sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_1100_MY_600 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_1100_MY_600",
                                               sampletype = "mc",
                                               files      = [path["2018"]+'srosenzw_NMSSM_XYH_YToHH_6b_MX_1100_MY_600_sl7_nano_100k/ntuple.root'],
                                               sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_1100_MY_700 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_1100_MY_700",
                                               sampletype = "mc",
                                               files      = [path["2018"]+'srosenzw_NMSSM_XYH_YToHH_6b_MX_1100_MY_700_sl7_nano_100k/ntuple.root'],
                                               sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_1100_MY_800 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_1100_MY_800",
                                               sampletype = "mc",
                                               files      = [path["2018"]+'srosenzw_NMSSM_XYH_YToHH_6b_MX_1100_MY_800_sl7_nano_100k/ntuple.root'],
                                               sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_1100_MY_900 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_1100_MY_900",
                                               sampletype = "mc",
                                               files      = [path["2018"]+'srosenzw_NMSSM_XYH_YToHH_6b_MX_1100_MY_900_sl7_nano_100k/ntuple.root'],
                                               sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_1200_MY_300 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_1200_MY_300",
                                               sampletype = "mc",
                                               files      = [path["2018"]+'srosenzw_NMSSM_XYH_YToHH_6b_MX_1200_MY_300_sl7_nano_100k/ntuple.root'],
                                               sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_1200_MY_400 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_1200_MY_400",
                                               sampletype = "mc",
                                               files      = [path["2018"]+'srosenzw_NMSSM_XYH_YToHH_6b_MX_1200_MY_400_sl7_nano_100k/ntuple.root'],
                                               sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_1200_MY_500 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_1200_MY_500",
                                               sampletype = "mc",
                                               files      = [path["2018"]+'srosenzw_NMSSM_XYH_YToHH_6b_MX_1200_MY_500_sl7_nano_100k/ntuple.root'],
                                               sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_1200_MY_600 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_1200_MY_600",
                                               sampletype = "mc",
                                               files      = [path["2018"]+'srosenzw_NMSSM_XYH_YToHH_6b_MX_1200_MY_600_sl7_nano_100k/ntuple.root'],
                                               sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_1200_MY_700 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_1200_MY_700",
                                               sampletype = "mc",
                                               files      = [path["2018"]+'srosenzw_NMSSM_XYH_YToHH_6b_MX_1200_MY_700_sl7_nano_100k/ntuple.root'],
                                               sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_1200_MY_800 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_1200_MY_800",
                                               sampletype = "mc",
                                               files      = [path["2018"]+'srosenzw_NMSSM_XYH_YToHH_6b_MX_1200_MY_800_sl7_nano_100k/ntuple.root'],
                                               sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_1200_MY_900 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_1200_MY_900",
                                               sampletype = "mc",
                                               files      = [path["2018"]+'srosenzw_NMSSM_XYH_YToHH_6b_MX_1200_MY_900_sl7_nano_100k/ntuple.root'],
                                               sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
'''
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Suzanne's samples

directories["2018"] = '/store/user/srosenzw/sixb/ntuples/Summer2018UL/bias/NMSSM/'
path["2018"] = "".join([redirector, directories["2018"]])
NMSSM_XYH_YToHH_6b_MX_450_MY_300 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_450_MY_300",
                                              sampletype = "mc",
                                              files      = [path["2018"]+'NMSSM_XYH_YToHH_6b_MX_450_MY_300/ntuple.root'],
                                              sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_500_MY_300 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_500_MY_300",
                                              sampletype = "mc",
                                              files      = [path["2018"]+'NMSSM_XYH_YToHH_6b_MX_500_MY_300/ntuple.root'],
                                              sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_600_MY_300 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_600_MY_300",
                                              sampletype = "mc",
                                              files      = [path["2018"]+'NMSSM_XYH_YToHH_6b_MX_600_MY_300/ntuple.root'],
                                              sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_600_MY_400 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_600_MY_400",
                                              sampletype = "mc",
                                              files      = [path["2018"]+'NMSSM_XYH_YToHH_6b_MX_600_MY_400/ntuple.root'],
                                              sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_700_MY_300 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_700_MY_300",
                                              sampletype = "mc",
                                              files      = [path["2018"]+'NMSSM_XYH_YToHH_6b_MX_700_MY_300/ntuple.root'],
                                              sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_700_MY_400 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_700_MY_400",
                                              sampletype = "mc",
                                              files      = [path["2018"]+'NMSSM_XYH_YToHH_6b_MX_700_MY_400/ntuple.root'],
                                              sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_700_MY_500 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_700_MY_500",
                                              sampletype = "mc",
                                              files      = [path["2018"]+'NMSSM_XYH_YToHH_6b_MX_700_MY_500/ntuple.root'],
                                              sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_800_MY_300 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_800_MY_300",
                                              sampletype = "mc",
                                              files      = [path["2018"]+'NMSSM_XYH_YToHH_6b_MX_800_MY_300/ntuple.root'],
                                              sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_800_MY_400 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_800_MY_400",
                                              sampletype = "mc",
                                              files      = [path["2018"]+'NMSSM_XYH_YToHH_6b_MX_800_MY_400/ntuple.root'],
                                              sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_800_MY_500 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_800_MY_500",
                                              sampletype = "mc",
                                              files      = [path["2018"]+'NMSSM_XYH_YToHH_6b_MX_800_MY_500/ntuple.root'],
                                              sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_800_MY_600 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_800_MY_600",
                                              sampletype = "mc",
                                              files      = [path["2018"]+'NMSSM_XYH_YToHH_6b_MX_800_MY_600/ntuple.root'],
                                              sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_900_MY_300 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_900_MY_300",
                                              sampletype = "mc",
                                              files      = [path["2018"]+'NMSSM_XYH_YToHH_6b_MX_900_MY_300/ntuple.root'],
                                              sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_900_MY_400 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_900_MY_400",
                                              sampletype = "mc",
                                              files      = [path["2018"]+'NMSSM_XYH_YToHH_6b_MX_900_MY_400/ntuple.root'],
                                              sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_900_MY_500 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_900_MY_500",
                                              sampletype = "mc",
                                              files      = [path["2018"]+'NMSSM_XYH_YToHH_6b_MX_900_MY_500/ntuple.root'],
                                              sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_900_MY_600 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_900_MY_600",
                                              sampletype = "mc",
                                              files      = [path["2018"]+'NMSSM_XYH_YToHH_6b_MX_900_MY_600/ntuple.root'],
                                              sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_900_MY_700 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_900_MY_700",
                                              sampletype = "mc",
                                              files      = [path["2018"]+'NMSSM_XYH_YToHH_6b_MX_900_MY_700/ntuple.root'],
                                              sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_1000_MY_300 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_1000_MY_300",
                                               sampletype = "mc",
                                               files      = [path["2018"]+'NMSSM_XYH_YToHH_6b_MX_1000_MY_300/ntuple.root'],
                                               sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_1000_MY_400 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_1000_MY_400",
                                               sampletype = "mc",
                                               files      = [path["2018"]+'NMSSM_XYH_YToHH_6b_MX_1000_MY_400/ntuple.root'],
                                               sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_1000_MY_500 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_1000_MY_500",
                                               sampletype = "mc",
                                               files      = [path["2018"]+'NMSSM_XYH_YToHH_6b_MX_1000_MY_500/ntuple.root'],
                                               sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_1000_MY_600 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_1000_MY_600",
                                               sampletype = "mc",
                                               files      = [path["2018"]+'NMSSM_XYH_YToHH_6b_MX_1000_MY_600/ntuple.root'],
                                               sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_1000_MY_700 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_1000_MY_700",
                                               sampletype = "mc",
                                               files      = [path["2018"]+'NMSSM_XYH_YToHH_6b_MX_1000_MY_700/ntuple.root'],
                                               sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_1000_MY_800 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_1000_MY_800",
                                               sampletype = "mc",
                                               files      = [path["2018"]+'NMSSM_XYH_YToHH_6b_MX_1000_MY_800/ntuple.root'],
                                               sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_1100_MY_300 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_1100_MY_300",
                                               sampletype = "mc",
                                               files      = [path["2018"]+'NMSSM_XYH_YToHH_6b_MX_1100_MY_300/ntuple.root'],
                                               sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_1100_MY_400 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_1100_MY_400",
                                               sampletype = "mc",
                                               files      = [path["2018"]+'NMSSM_XYH_YToHH_6b_MX_1100_MY_400/ntuple.root'],
                                               sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_1100_MY_500 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_1100_MY_500",
                                               sampletype = "mc",
                                               files      = [path["2018"]+'NMSSM_XYH_YToHH_6b_MX_1100_MY_500/ntuple.root'],
                                               sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_1100_MY_600 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_1100_MY_600",
                                               sampletype = "mc",
                                               files      = [path["2018"]+'NMSSM_XYH_YToHH_6b_MX_1100_MY_600/ntuple.root'],
                                               sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_1100_MY_700 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_1100_MY_700",
                                               sampletype = "mc",
                                               files      = [path["2018"]+'NMSSM_XYH_YToHH_6b_MX_1100_MY_700/ntuple.root'],
                                               sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_1100_MY_800 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_1100_MY_800",
                                               sampletype = "mc",
                                               files      = [path["2018"]+'NMSSM_XYH_YToHH_6b_MX_1100_MY_800/ntuple.root'],
                                               sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_1100_MY_900 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_1100_MY_900",
                                               sampletype = "mc",
                                               files      = [path["2018"]+'NMSSM_XYH_YToHH_6b_MX_1100_MY_900/ntuple.root'],
                                               sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_1200_MY_300 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_1200_MY_300",
                                               sampletype = "mc",
                                               files      = [path["2018"]+'NMSSM_XYH_YToHH_6b_MX_1200_MY_300/ntuple.root'],
                                               sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_1200_MY_400 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_1200_MY_400",
                                               sampletype = "mc",
                                               files      = [path["2018"]+'NMSSM_XYH_YToHH_6b_MX_1200_MY_400/ntuple.root'],
                                               sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_1200_MY_500 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_1200_MY_500",
                                               sampletype = "mc",
                                               files      = [path["2018"]+'NMSSM_XYH_YToHH_6b_MX_1200_MY_500/ntuple.root'],
                                               sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_1200_MY_600 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_1200_MY_600",
                                               sampletype = "mc",
                                               files      = [path["2018"]+'NMSSM_XYH_YToHH_6b_MX_1200_MY_600/ntuple.root'],
                                               sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_1200_MY_700 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_1200_MY_700",
                                               sampletype = "mc",
                                               files      = [path["2018"]+'NMSSM_XYH_YToHH_6b_MX_1200_MY_700/ntuple.root'],
                                               sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_1200_MY_800 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_1200_MY_800",
                                               sampletype = "mc",
                                               files      = [path["2018"]+'NMSSM_XYH_YToHH_6b_MX_1200_MY_800/ntuple.root'],
                                               sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})
NMSSM_XYH_YToHH_6b_MX_1200_MY_900 = sam.Sample(name       = "NMSSM_XYH_YToHH_6b_MX_1200_MY_900",
                                               sampletype = "mc",
                                               files      = [path["2018"]+'NMSSM_XYH_YToHH_6b_MX_1200_MY_900/ntuple.root'],
                                               sampledesc = {**lumiMap["2018"], 'xs' : 0.3, 'xs_units' : 'pb'})

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
'''

# Marina's samples
directories["2018"] = '/store/user/mkolosov/HHHTo6B/Summer2018UL_29Sep2022_withoutLeptonVeto/'
path["2018"] = "".join([redirector, directories["2018"]])

TTJets = sam.Sample(name       = "TTJets",
                    sampletype = "mc",
                    files      = [path["2018"]+'TTJets/ntuple.root'],
                    sampledesc = {**lumiMap["2018"], 'xs' : xs.get("TTJets", energy), 'xs_units' : 'pb'})

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

dsetGroups = {}
dsetGroups["NMSSM_XYH_YToHH_6b"] = {"2018" : [], "2017" : [], "2016" : []}
dsetGroups["Data"]               = {"2018" : [], "2017" : [], "2016" : []}
dsetGroups["TT"]                 = {"2018" : [], "2017" : [], "2016" : []}
dsetGroups["QCD"]                = {"2018" : [], "2017" : [], "2016" : []}

# 2018 Samples:
dsetGroups["NMSSM_XYH_YToHH_6b"]["2018"] = [NMSSM_XYH_YToHH_6b_MX_450_MY_300,
                                            NMSSM_XYH_YToHH_6b_MX_500_MY_300,
                                            NMSSM_XYH_YToHH_6b_MX_600_MY_300,
                                            NMSSM_XYH_YToHH_6b_MX_600_MY_400,
                                            NMSSM_XYH_YToHH_6b_MX_700_MY_300,
                                            NMSSM_XYH_YToHH_6b_MX_700_MY_400,
                                            NMSSM_XYH_YToHH_6b_MX_700_MY_500,
                                            NMSSM_XYH_YToHH_6b_MX_800_MY_300,
                                            NMSSM_XYH_YToHH_6b_MX_800_MY_400,
                                            NMSSM_XYH_YToHH_6b_MX_800_MY_500,
                                            NMSSM_XYH_YToHH_6b_MX_800_MY_600,
                                            NMSSM_XYH_YToHH_6b_MX_900_MY_300,
                                            NMSSM_XYH_YToHH_6b_MX_900_MY_400,
                                            NMSSM_XYH_YToHH_6b_MX_900_MY_500,
                                            NMSSM_XYH_YToHH_6b_MX_900_MY_600,
                                            NMSSM_XYH_YToHH_6b_MX_900_MY_700,
                                            NMSSM_XYH_YToHH_6b_MX_1000_MY_300,
                                            NMSSM_XYH_YToHH_6b_MX_1000_MY_400,
                                            NMSSM_XYH_YToHH_6b_MX_1000_MY_500,
                                            NMSSM_XYH_YToHH_6b_MX_1000_MY_600,
                                            NMSSM_XYH_YToHH_6b_MX_1000_MY_700,
                                            NMSSM_XYH_YToHH_6b_MX_1100_MY_800,
                                            NMSSM_XYH_YToHH_6b_MX_1100_MY_900,
                                            NMSSM_XYH_YToHH_6b_MX_1200_MY_300,
                                            NMSSM_XYH_YToHH_6b_MX_1200_MY_400,
                                            NMSSM_XYH_YToHH_6b_MX_1200_MY_500,
                                            NMSSM_XYH_YToHH_6b_MX_1200_MY_600,
                                            NMSSM_XYH_YToHH_6b_MX_1200_MY_700,
                                            NMSSM_XYH_YToHH_6b_MX_1200_MY_800,
                                            NMSSM_XYH_YToHH_6b_MX_1200_MY_900]

dsetGroups["TT"]["2018"] = [TTJets]
dsetGroups["QCD"]["2018"] = [QCD_bEnriched_HT100to200,
                             QCD_bEnriched_HT200to300,
                             QCD_bEnriched_HT300to500,
                             QCD_bEnriched_HT500to700,
                             QCD_bEnriched_HT700to1000,
                             QCD_bEnriched_HT1000to1500,
                             QCD_bEnriched_HT1500to2000,
                             QCD_bEnriched_HT2000toInf]
dsetGroups["Data"]["2018"] = [JetHT_Run2018A,
                              JetHT_Run2018B,
                              JetHT_Run2018C,
                              JetHT_Run2018D]

